#!/usr/bin/env python3
"""Launch and durably archive one two-player OpenBW/BWAPI match."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid

SCHEMA_VERSION = 1
RACES = ("Terran", "Protoss", "Zerg", "Random")
REQUIRED_MPQS = ("Patch_rt.mpq", "StarDat.mpq", "BrooDat.mpq")
RECORDED_RUNTIME_ENV = {"DYLD_LIBRARY_PATH", "DYLD_INSERT_LIBRARIES", "ASAN_OPTIONS", "UBSAN_OPTIONS", "LSAN_OPTIONS"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump(value, output, indent=2, sort_keys=True)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def artifact(path: Path) -> dict[str, object]:
    return {"path": str(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}


def binary_artifact(path: Path) -> dict[str, object]:
    record = artifact(path)
    sidecar = Path(str(path) + ".build.json")
    if not sidecar.is_file():
        record["build_provenance_status"] = "no build sidecar; source identity not verified"
        return record
    try:
        provenance = json.loads(sidecar.read_text())
        if provenance.get("binary_sha256") != record["sha256"]:
            raise ValueError("build sidecar does not match current binary")
        record["build_provenance"] = provenance
        record["build_provenance_file"] = artifact(sidecar)
        record["build_provenance_status"] = "binary hash matches build sidecar"
    except (ValueError, OSError, AttributeError) as error:
        record["build_provenance_status"] = str(error)
    return record


def link_game_data(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True)
    for item in source.iterdir():
        if item.name == "bwapi-data":
            continue
        (destination / item.name).symlink_to(item.resolve(), target_is_directory=item.is_dir())
    private = destination / "bwapi-data"
    for name in ("AI", "read", "write"):
        (private / name).mkdir(parents=True, exist_ok=True)


def snapshot_ai_data(bot: Path, work: Path, player_input: dict[str, object]) -> None:
    """Copy the module's packaged AI files so later source edits cannot affect play."""
    source = bot.resolve().parent / "AI"
    destination = work / "bwapi-data" / "AI"
    files = []
    if source.is_dir():
        for path in sorted(source.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"AI bundle must contain ordinary files, not symlinks: {path}")
            if not path.is_file():
                continue
            relative = path.relative_to(source)
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            files.append({"relative_path": str(relative), "source_path": str(path), **artifact(target)})
    player_input["ai_files"] = files
    actual = {item["relative_path"]: item["sha256"] for item in files}
    provenance = player_input["bot_module"].get("build_provenance", {})
    for expected in provenance.get("ai_files", []):
        if actual.get(expected["path"]) != expected["sha256"]:
            raise ValueError(f"Missing or changed AI file for {bot.name}: {expected['path']}")


def player_environment(args: argparse.Namespace, player: int, work: Path, socket_dir: Path) -> tuple[dict[str, str], Path, Path]:
    bot = (args.bot1 if player == 1 else args.bot2).resolve()
    race = args.race1 if player == 1 else args.race2
    name = args.name1 if player == 1 else args.name2
    raw_replay = work / "replay.rep"
    result_path = work / "bwapi-data" / "write" / "result.json"
    env = {key: value for key, value in os.environ.items()
           if not key.startswith(("OPENBW_", "BWAPI_CONFIG_", "MATCH_"))}
    env.update(
        {
            "OPENBW_ENABLE_UI": "0",
            # One known peer per game: avoid LOCAL_AUTO's directory discovery,
            # which can leave two simultaneous launchers waiting in the lobby.
            "OPENBW_LAN_MODE": "LOCAL",
            "OPENBW_LOCAL_PATH": str(socket_dir / "game.socket"),
            "BWAPI_CONFIG_AI__AI": str(bot),
            "BWAPI_CONFIG_AUTO_MENU__AUTO_MENU": "LAN",
            "BWAPI_CONFIG_AUTO_MENU__RACE": race,
            "BWAPI_CONFIG_AUTO_MENU__CHARACTER_NAME": f"{name} {race}"[:24],
            "BWAPI_CONFIG_AUTO_MENU__MAP": args.map,
            "BWAPI_CONFIG_AUTO_MENU__GAME": args.game_name,
            "BWAPI_CONFIG_AUTO_MENU__GAME_TYPE": "MELEE",
            "BWAPI_CONFIG_AUTO_MENU__WAIT_FOR_MIN_PLAYERS": "2",
            "BWAPI_CONFIG_AUTO_MENU__WAIT_FOR_MAX_PLAYERS": "2",
            "BWAPI_CONFIG_AUTO_MENU__AUTO_RESTART": "OFF",
            # BWAPI's replay name formatter rejects long absolute paths. The
            # launcher CWD is already the isolated player directory.
            "BWAPI_CONFIG_AUTO_MENU__SAVE_REPLAY": raw_replay.name,
            "MATCH_RESULT_PATH": str(result_path),
        }
    )
    if args.library_path:
        env["DYLD_LIBRARY_PATH"] = str(args.library_path.resolve())
    if args.seed is not None:
        env["OPENBW_SCENARIO_SEED"] = str(args.seed)
        env["OPENBW_SCENARIO_PLAYER_ID"] = str(player)
    return env, raw_replay, result_path


def terminate(processes: list[subprocess.Popen[bytes]], usage: dict[int, resource.struct_rusage]) -> None:
    for process in processes:
        if process.returncode is None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
    deadline = time.monotonic() + 2
    while time.monotonic() < deadline and any(p.returncode is None for p in processes):
        reap(processes, usage)
        time.sleep(0.02)
    for process in processes:
        if process.returncode is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
    # SIGKILL is asynchronous. Reap each exact child before collecting files or
    # deleting transport state, so no launcher survives a terminal record.
    for process in processes:
        if process.returncode is None:
            pid, status, stats = os.wait4(process.pid, 0)
            process.returncode = os.waitstatus_to_exitcode(status)
            usage[pid] = stats


def reap(processes: list[subprocess.Popen[bytes]], usage: dict[int, resource.struct_rusage]) -> None:
    for process in processes:
        if process.returncode is not None:
            continue
        try:
            pid, status, stats = os.wait4(process.pid, os.WNOHANG)
        except ChildProcessError:
            continue
        if pid:
            process.returncode = os.waitstatus_to_exitcode(status)
            usage[process.pid] = stats


def read_result(path: Path, fallback: Path) -> tuple[dict[str, object] | None, str | None]:
    selected = path if path.is_file() else fallback
    if not selected.is_file():
        return None, "bot did not emit MATCH_RESULT_PATH metadata"
    try:
        value = json.loads(selected.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("root is not an object")
        if type(value.get("frame_count")) is not int or value["frame_count"] < 0:
            raise ValueError("frame_count must be a nonnegative integer")
        if type(value.get("ended")) is not bool:
            raise ValueError("ended must be a boolean")
        if value["ended"] and type(value.get("winner")) is not bool:
            raise ValueError("terminal winner must be a boolean")
        value["metadata_path"] = str(selected)
        return value, None
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return None, f"invalid bot result metadata: {error}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--launcher", required=True, type=Path)
    parser.add_argument("--bot1", required=True, type=Path)
    parser.add_argument("--race1", required=True, choices=RACES)
    parser.add_argument("--name1", help="Display name; defaults to module filename")
    parser.add_argument("--bot2", required=True, type=Path)
    parser.add_argument("--race2", required=True, choices=RACES)
    parser.add_argument("--name2", help="Display name; defaults to module filename")
    parser.add_argument("--map", required=True, help="Map path as seen from the game-data directory")
    parser.add_argument("--game-data-dir", required=True, type=Path)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--experiment-id", help="Stable experiment ledger identity for dashboard grouping")
    parser.add_argument("--seed", type=int, help="Controlled uint32 engine seed before race and start-slot draws")
    parser.add_argument("--wall-timeout", required=True, type=float)
    parser.add_argument("--artifacts-dir", type=Path, default=Path("artifacts"))
    parser.add_argument("--library-path", type=Path)
    parser.add_argument("--game-name", default="openbw-match")
    args = parser.parse_args(argv)
    if not math.isfinite(args.wall_timeout) or args.wall_timeout <= 0:
        parser.error("--wall-timeout must be finite and positive")
    if args.seed is not None and not 0 <= args.seed <= 0xffffffff:
        parser.error("--seed must be an unsigned 32-bit integer")
    for label in ("launcher", "bot1", "bot2", "game_data_dir"):
        path = getattr(args, label)
        if not path.exists():
            parser.error(f"--{label.replace('_', '-')} does not exist: {path}")
    missing = [name for name in REQUIRED_MPQS if not (args.game_data_dir / name).is_file()]
    if missing:
        parser.error(f"--game-data-dir is missing required OpenBW files: {', '.join(missing)}")
    if Path(args.map).is_absolute() or not (args.game_data_dir / args.map).is_file():
        parser.error("--map must name a regular file relative to --game-data-dir")
    args.name1 = args.name1 or args.bot1.stem
    args.name2 = args.name2 or args.bot2.stem
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started_wall = time.monotonic()
    started_at = utc_now()
    run_id = f"{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:12]}"
    game_id = "game-0001"
    run_dir = args.artifacts_dir.resolve() / "runs" / run_id
    game_dir = run_dir / game_id
    replay_dir = args.artifacts_dir.resolve() / "replays" / dt.datetime.now(dt.timezone.utc).strftime("%Y/%m/%d") / run_id
    # sockaddr_un is only 104 bytes on macOS, including OpenBW's generated
    # filename. Keep transport outside the (possibly deeply nested) archive.
    socket_dir = Path(tempfile.mkdtemp(prefix="scai-", dir="/tmp"))
    manifest_path = game_dir / "manifest.json"
    replay_dir.mkdir(parents=True)

    inputs = {"launcher": binary_artifact(args.launcher.resolve()), "map": {"configured_path": args.map}, "players": []}
    inputs["game_data"] = [artifact(args.game_data_dir.resolve() / name) for name in REQUIRED_MPQS]
    if args.library_path:
        inputs["engine_libraries"] = [artifact(path) for path in sorted(args.library_path.resolve().glob("*.dylib"))]
    map_file = args.game_data_dir.resolve() / args.map
    if map_file.is_file():
        inputs["map"].update(artifact(map_file))
    else:
        inputs["map"]["hash_unavailable_reason"] = "configured map is not a regular file under game-data-dir"
    for number, (bot, race) in enumerate(((args.bot1, args.race1), (args.bot2, args.race2)), 1):
        inputs["players"].append({"player": number, "race": race,
                                  "name": args.name1 if number == 1 else args.name2,
                                  "bot_module": binary_artifact(bot.resolve())})

    manifest: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "game_id": game_id,
        "purpose": args.purpose,
        "experiment_id": args.experiment_id,
        "status": "launching",
        "started_at": started_at,
        "backend": "OpenBW via BWAPILauncher",
        "platform": {"sys_platform": sys.platform, "machine": os.uname().machine},
        "rules": {"latency": "LF3: OpenBW source hardcodes 3 logical frames; per-player metadata records runtime observations when available", "adjudication": "none", "wall_timeout_seconds": args.wall_timeout},
        "reproducibility": {
            "learning_state": "empty isolated read/write directories for each player",
            "random_seed": args.seed,
            "seed_semantics": "OpenBW LCG state before random-race and start-slot draws" if args.seed is not None else None,
            "protocol_player_ids": [1, 2] if args.seed is not None else None,
            "known_nondeterminism": (
                "Engine initialization controlled; bot wall-clock seeds, address-dependent ordering, or search budgets may still differ."
                if args.seed is not None else
                "OpenBW derives its start seed from random client IDs; replay contains the resulting seed."
            ),
        },
        "inputs": inputs,
        "measurement_scope": {
            "elapsed_seconds": "harness start through replay archival and terminal manifest preparation",
            "per_player_cpu_and_rss": "each BWAPILauncher process, including its OpenBW engine and loaded bot module; excludes descendants",
        },
        "players": [],
        "replays": [],
    }
    atomic_json(manifest_path, manifest)

    processes: list[subprocess.Popen[bytes]] = []
    usage: dict[int, resource.struct_rusage] = {}
    opened_logs: list[object] = []
    interrupted_signal: int | None = None
    timed_out = False
    launch_error: str | None = None
    player_runtime: list[tuple[Path, Path, Path, dict[str, str]]] = []
    old_handlers: dict[int, object] = {}

    def on_signal(signum: int, _frame: object) -> None:
        nonlocal interrupted_signal
        interrupted_signal = signum

    for signum in (signal.SIGINT, signal.SIGTERM):
        old_handlers[signum] = signal.signal(signum, on_signal)
    try:
        if args.seed is not None:
            provenance = inputs["launcher"].get("build_provenance", {})
            if not provenance.get("scenario_control") or not args.library_path:
                raise ValueError("Controlled --seed requires a verified scenario-capable engine sidecar and --library-path")
            expected = {Path(item["path"]).name: item["sha256"] for item in provenance.get("artifacts", [])}
            actual = {Path(item["path"]).name: item["sha256"] for item in inputs["engine_libraries"]}
            for name in ("libOpenBWData.dylib", "libBWAPI.dylib", "libBWAPILIB.dylib"):
                if name not in expected or actual.get(name) != expected[name]:
                    raise ValueError(f"Controlled engine library does not match build provenance: {name}")
        for number in (1, 2):
            work = game_dir / f"player-{number}"
            link_game_data(args.game_data_dir.resolve(), work)
            snapshot_ai_data(args.bot1 if number == 1 else args.bot2, work, inputs["players"][number - 1])
            env, raw_replay, result_path = player_environment(args, number, work, socket_dir)
            stdout_path, stderr_path = work / "stdout.log", work / "stderr.log"
            stdout_file, stderr_file = stdout_path.open("wb"), stderr_path.open("wb")
            opened_logs.extend((stdout_file, stderr_file))
            manifest.setdefault("launch_configuration", []).append({
                "player": number, "command": [str(args.launcher.resolve())], "cwd": str(work),
                "environment": {key: env[key] for key in sorted(env)
                                if key.startswith(("OPENBW_", "BWAPI_CONFIG_", "MATCH_")) or key in RECORDED_RUNTIME_ENV},
            })
            atomic_json(manifest_path, manifest)
            process = subprocess.Popen(
                [str(args.launcher.resolve())], cwd=work, env=env, stdout=stdout_file, stderr=stderr_file,
                stdin=subprocess.DEVNULL, start_new_session=True,
            )
            processes.append(process)
            player_runtime.append((raw_replay, result_path, work, env))
            manifest["live_processes"] = [{"pid": child.pid, "player": index + 1}
                                          for index, child in enumerate(processes)]
            atomic_json(manifest_path, manifest)
        manifest["status"] = "running"
        atomic_json(manifest_path, manifest)
        deadline = started_wall + args.wall_timeout
        while any(process.returncode is None for process in processes):
            reap(processes, usage)
            if interrupted_signal is not None:
                break
            if time.monotonic() >= deadline:
                timed_out = True
                break
            time.sleep(0.02)
    except (OSError, ValueError) as error:
        launch_error = f"{type(error).__name__}: {error}"
    finally:
        if any(process.returncode is None for process in processes):
            terminate(processes, usage)
        reap(processes, usage)
        for log in opened_logs:
            log.close()
        for signum, handler in old_handlers.items():
            signal.signal(signum, handler)
        shutil.rmtree(socket_dir)

    for number, process in enumerate(processes, 1):
        raw_replay, result_path, work, env = player_runtime[number - 1]
        result, result_error = read_result(result_path, work / "bwapi-data/write/diagnostic.json")
        stats = usage.get(process.pid)
        stderr_text = (work / "stderr.log").read_text(encoding="utf-8", errors="replace")
        player_record: dict[str, object] = {
            "player": number,
            "command": [str(args.launcher.resolve())],
            "cwd": str(work),
            "environment": {key: env[key] for key in sorted(env) if key.startswith(("OPENBW_", "BWAPI_CONFIG_", "MATCH_")) or key in RECORDED_RUNTIME_ENV},
            "return_code": process.returncode,
            "stdout": artifact(work / "stdout.log"),
            "stderr": artifact(work / "stderr.log"),
            "result_metadata": result,
            "result_metadata_note": result_error,
            "launcher_error_detected": bool(stderr_text.strip()) and process.returncode == 0,
            "write_state": [artifact(path) for path in sorted((work / "bwapi-data/write").rglob("*")) if path.is_file()],
        }
        if stats:
            player_record["resource_usage"] = {
                "user_cpu_seconds": stats.ru_utime,
                "system_cpu_seconds": stats.ru_stime,
                "peak_rss_raw": stats.ru_maxrss,
                "peak_rss_units": "bytes on macOS; KiB on Linux",
            }
        manifest["players"].append(player_record)

        candidates = sorted({path for path in work.rglob("*.rep") if path.is_file()})
        for ordinal, source in enumerate(candidates, 1):
            destination = replay_dir / f"{game_id}-player-{number}-{ordinal}.rep"
            shutil.copyfile(source, destination)
            with destination.open("rb") as replay_file:
                os.fsync(replay_file.fileno())
            manifest["replays"].append({"player": number, **artifact(destination), "source_path": str(source), "archival_status": "copied"})

    # Persist the archive directory entries as well as each replay's contents.
    # The manifest lives in another directory and cannot flush these entries.
    replay_directory_fd = os.open(replay_dir, os.O_RDONLY)
    try:
        os.fsync(replay_directory_fd)
    finally:
        os.close(replay_directory_fd)

    if not manifest["replays"]:
        manifest["replay_missing_reason"] = (
            "match was interrupted before replay archival" if interrupted_signal else
            "wall timeout expired before replay archival" if timed_out else
            "launcher startup failed" if launch_error else
            "BWAPILauncher produced no .rep file; inspect player logs"
        )
    results = [player.get("result_metadata") for player in manifest["players"]]
    manifest["result"] = results if any(results) else None
    manifest["logical_frame_count"] = max((int(r.get("frame_count", 0)) for r in results if isinstance(r, dict)), default=None)
    manifest["termination_reason"] = (
        f"signal_{interrupted_signal}" if interrupted_signal else "wall_timeout" if timed_out else
        "launch_error" if launch_error else "children_exited"
    )
    manifest["launch_error"] = launch_error
    manifest["outcome_verified"] = (
        len(results) == 2 and all(isinstance(result, dict) and result.get("ended") is True for result in results)
        and {result.get("winner") for result in results} == {True, False}
    )
    if interrupted_signal:
        manifest["status"] = "interrupted"
    elif timed_out:
        manifest["status"] = "timed_out"
    elif launch_error or any(p.returncode != 0 for p in processes) or not manifest["replays"]:
        manifest["status"] = "failed"
    elif manifest["outcome_verified"]:
        manifest["status"] = "completed"
    else:
        manifest["status"] = "incomplete"
    manifest["outcome_verification_scope"] = "opposing onEnd winner callbacks; replay determinism verified separately (clients may end on different frames)"
    manifest["replay_validation"] = "not performed by launcher; replay emission alone is not proof of valid playback"
    manifest["finished_at"] = utc_now()
    manifest["elapsed_seconds"] = time.monotonic() - started_wall
    frames = manifest["logical_frame_count"]
    manifest["logical_frames_per_wall_second"] = frames / manifest["elapsed_seconds"] if isinstance(frames, int) else None
    atomic_json(manifest_path, manifest)
    atomic_json(run_dir / "manifest.json", manifest)
    # Include the first durable terminal writes in the total; recording this
    # measurement incurs one additional small manifest write, stated explicitly.
    manifest["durable_completion_seconds"] = time.monotonic() - started_wall
    manifest["durable_logical_frames_per_wall_second"] = frames / manifest["durable_completion_seconds"] if isinstance(frames, int) else None
    atomic_json(manifest_path, manifest)
    atomic_json(run_dir / "manifest.json", manifest)
    print(manifest_path)
    if interrupted_signal:
        return 128 + interrupted_signal
    return 0 if manifest["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
