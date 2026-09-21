#!/usr/bin/env python3
"""Run a small, preregistered match schedule through run_match.py."""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w") as output:
        output.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)
    directory_fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_file(parser, path, expected_sha256, label):
    path = Path(path)
    if not path.is_file():
        parser.error(f"{label} is missing: {path}")
    actual = sha256(path)
    if actual != expected_sha256:
        parser.error(f"{label} SHA-256 mismatch: expected {expected_sha256}, got {actual}")


def verify_identity_files(parser, identity, label):
    optional_files = (
        ("build_sidecar", "build_sidecar_sha256", "build sidecar"),
        ("source_patch", "source_patch_sha256", "source patch"),
        ("ai_config", "ai_config_sha256", "AI config"),
    )
    for path_key, hash_key, description in optional_files:
        if path_key in identity or hash_key in identity:
            if not identity.get(path_key) or not identity.get(hash_key):
                parser.error(f"{label} must freeze both {path_key} and {hash_key}")
            verify_file(parser, identity[path_key], identity[hash_key], f"{label} {description}")
    if identity.get("build_sidecar"):
        try:
            sidecar = json.loads(Path(identity["build_sidecar"]).read_text())
        except (OSError, json.JSONDecodeError) as error:
            parser.error(f"{label} build sidecar is unreadable: {error}")
        if sidecar.get("binary_sha256") != identity.get("sha256"):
            parser.error(f"{label} build sidecar does not identify the frozen module")
        source_manifest = identity.get("source_manifest_sha256")
        if source_manifest is not None:
            if sidecar.get("source_manifest_sha256") != source_manifest:
                parser.error(f"{label} build sidecar does not identify the frozen source manifest")
            source_files = sidecar.get("source_files")
            if not isinstance(source_files, list) or not source_files or any(not isinstance(path, str) for path in source_files):
                parser.error(f"{label} build sidecar lacks a source file manifest")
            digest = hashlib.sha256()
            for source_name in source_files:
                source_path = Path(source_name)
                if not source_path.is_file():
                    parser.error(f"{label} source manifest file is missing: {source_name}")
                digest.update(f"{sha256(source_path)}  {source_name}\n".encode())
            if digest.hexdigest() != source_manifest:
                parser.error(f"{label} source manifest SHA-256 mismatch")


def verify_schedule_inputs(parser, schedule):
    """Fail before creating an experiment ledger if optional frozen inputs drift."""
    optional_files = (
        ("launcher", "launcher_sha256", "launcher"),
        ("launcher_sidecar", "launcher_sidecar_sha256", "launcher sidecar"),
        ("eval_plan", "eval_plan_sha256", "evaluation plan"),
        ("provenance_registry", "provenance_registry_sha256", "provenance registry"),
    )
    for path_key, hash_key, label in optional_files:
        if hash_key in schedule:
            if not schedule.get(path_key):
                parser.error(f"schedule freezes {hash_key} without {path_key}")
            verify_file(parser, schedule[path_key], schedule[hash_key], label)
    for collection, label in ((schedule.get("game_data_files", []), "game-data file"),
                              (schedule.get("required_files", []), "required file")):
        for item in collection:
            if not isinstance(item, dict) or not item.get("path") or not item.get("sha256"):
                parser.error(f"{label} entries require path and sha256")
            verify_file(parser, item["path"], item["sha256"], label)
    verify_identity_files(parser, schedule["candidate"], "candidate")
    for name, opponent in schedule["opponents"].items():
        verify_identity_files(parser, opponent, f"opponent {name}")
    if schedule.get("launcher_sidecar"):
        try:
            sidecar = json.loads(Path(schedule["launcher_sidecar"]).read_text())
        except (OSError, json.JSONDecodeError) as error:
            parser.error(f"launcher sidecar is unreadable: {error}")
        for artifact in sidecar.get("artifacts", []):
            if not artifact.get("path") or not artifact.get("sha256"):
                parser.error("launcher sidecar artifact lacks path or sha256")
            verify_file(parser, artifact["path"], artifact["sha256"], "launcher-sidecar artifact")


def wilson(wins, games):
    if not games:
        return None
    z = 1.959963984540054
    p = wins / games
    denominator = 1 + z * z / games
    center = (p + z * z / (2 * games)) / denominator
    radius = z * math.sqrt(p * (1 - p) / games + z * z / (4 * games * games)) / denominator
    return [max(0.0, center - radius), min(1.0, center + radius)]


def elo_advantage(wins, games):
    if not games:
        return None
    if wins == 0:
        return "-Infinity"
    if wins == games:
        return "Infinity"
    p = wins / games
    return 400 * math.log10(p / (1 - p))


def elo_from_probability(probability):
    if probability == 0:
        return "-Infinity"
    if probability == 1:
        return "Infinity"
    return 400 * math.log10(probability / (1 - probability))


def summarize(records, opponents):
    result = {}
    for opponent in opponents:
        rows = [r for r in records if r["opponent"] == opponent]
        scored = [r for r in rows if r["classification"] in ("win", "loss")]
        wins = sum(r["classification"] == "win" for r in scored)
        games = len(scored)
        failures = {}
        for row in rows:
            if row["classification"] not in ("win", "loss"):
                failures[row["classification"]] = failures.get(row["classification"], 0) + 1
        interval = wilson(wins, games)
        result[opponent] = {
            "wins": wins,
            "losses": games - wins,
            "scored_games": games,
            "scheduled_games": len(rows),
            "failures": failures,
            "win_rate": wins / games if games else None,
            "wilson_95": interval,
            "relative_elo_advantage": elo_advantage(wins, games),
            "relative_elo_95_from_wilson": [elo_from_probability(interval[0]), elo_from_probability(interval[1])] if interval else None,
            "relative_elo_note": "Relative to this opponent only; point estimate is infinite at observed 0% or 100%."
        }
    pooled = [r for r in records if r["classification"] in ("win", "loss")]
    wins = sum(r["classification"] == "win" for r in pooled)
    return {
        "by_opponent": result,
        "pooled_cohort": {"wins": wins, "losses": len(pooled) - wins, "scored_games": len(pooled),
                          "win_rate": wins / len(pooled) if pooled else None,
                          "note": "Descriptive pooled cohort score; no aggregate Elo across heterogeneous opponents."}
    }


def classify(match, candidate_player, runner_return_code=0):
    codes = [p.get("return_code") for p in match.get("players", [])]
    reason = match.get("termination_reason")
    if reason == "wall_timeout":
        return "timeout"
    if any(code not in (0, None) for code in codes):
        return "crash"
    # run_match also returns nonzero when clean child exits have unusable results.
    # Preserve that specific evidence instead of calling it a launcher failure.
    if reason == "children_exited" and codes == [0, 0] and not match.get("outcome_verified"):
        return "missing_or_inconsistent_metadata"
    if runner_return_code != 0:
        return "launcher_failure"
    if match.get("status") != "completed" or not match.get("outcome_verified"):
        return "missing_or_inconsistent_metadata"
    results = match.get("result") or []
    if (len(results) != 2 or
            not all(isinstance(result, dict) and isinstance(result.get("winner"), bool) for result in results) or
            {result["winner"] for result in results} != {True, False}):
        return "missing_or_inconsistent_metadata"
    winner = results[candidate_player - 1].get("winner")
    if not isinstance(winner, bool):
        return "missing_or_inconsistent_metadata"
    return "win" if winner else "loss"


def validate_schedule(parser, schedule):
    required = ("experiment_id", "hypothesis", "stop_condition", "purpose", "launcher",
                "library_path", "game_data_dir", "candidate", "opponents", "games")
    missing = [key for key in required if key not in schedule]
    if missing:
        parser.error("schedule missing: " + ", ".join(missing))
    if not schedule["hypothesis"] or not schedule["stop_condition"]:
        parser.error("schedule must preregister hypothesis and stop_condition")
    if not isinstance(schedule["games"], list) or not schedule["games"]:
        parser.error("schedule has no games")
    if "concurrency" in schedule and (type(schedule["concurrency"]) is not int or schedule["concurrency"] < 1):
        parser.error("schedule concurrency must be a positive integer")
    if "stop_after_consecutive_invalid" in schedule and (
            type(schedule["stop_after_consecutive_invalid"]) is not int or
            schedule["stop_after_consecutive_invalid"] < 1):
        parser.error("schedule stop_after_consecutive_invalid must be a positive integer")
    for index, game in enumerate(schedule["games"], 1):
        if game.get("opponent") not in schedule["opponents"]:
            parser.error(f"game {index} names an unknown opponent")
        if game.get("candidate_player") not in (1, 2):
            parser.error(f"game {index} candidate_player must be 1 or 2")
        if not isinstance(game.get("map"), str) or not game["map"]:
            parser.error(f"game {index} requires a map")
        seed = game.get("scenario_seed")
        if type(seed) is not int or not 0 <= seed <= 0xFFFFFFFF:
            parser.error(f"game {index} scenario_seed must be a uint32")
        for key in ("candidate_bot_seed", "opponent_bot_seed"):
            if key in game and (type(game[key]) is not int or not 0 <= game[key] <= 0xFFFFFFFF):
                parser.error(f"game {index} {key} must be a uint32")
    for name, opponent in schedule["opponents"].items():
        if opponent.get("race") not in ("Terran", "Protoss", "Zerg", "Random"):
            parser.error(f"opponent {name} has an invalid race")
        if not all(opponent.get(key) for key in ("name", "path", "sha256")):
            parser.error(f"opponent {name} lacks frozen identity fields")
    candidate = schedule["candidate"]
    if candidate.get("race") not in ("Terran", "Protoss", "Zerg", "Random") or not candidate.get("name") or not candidate.get("sha256"):
        parser.error("candidate lacks valid name, race, or SHA-256")


def match_measurements(match):
    rss = {}
    for player in match.get("players", []):
        usage = player.get("resource_usage") or {}
        rss[str(player.get("player"))] = usage.get("peak_rss_raw")
    return {"elapsed_seconds": match.get("elapsed_seconds"),
            "durable_completion_seconds": match.get("durable_completion_seconds"),
            "logical_frame_count": match.get("logical_frame_count"),
            "logical_frames_per_wall_second": match.get("logical_frames_per_wall_second"),
            "peak_rss_raw_by_player": rss}


def command_for(args, schedule, game, candidate, opponent):
    candidate_player = game["candidate_player"]
    players = ({"path": str(candidate), "name": schedule["candidate"]["name"], "race": schedule["candidate"]["race"]}, opponent)
    if candidate_player == 2:
        players = (opponent, players[0])
    command = [sys.executable, str(Path(args.runner).resolve()),
               "--launcher", schedule["launcher"], "--library-path", schedule["library_path"],
               "--game-data-dir", schedule["game_data_dir"], "--map", game["map"],
               "--bot1", players[0]["path"], "--race1", players[0]["race"], "--name1", players[0]["name"],
               "--bot2", players[1]["path"], "--race2", players[1]["race"], "--name2", players[1]["name"],
               "--purpose", schedule["purpose"], "--experiment-id", schedule["experiment_id"],
               "--wall-timeout", str(schedule["wall_timeout_seconds"]), "--artifacts-dir", args.artifacts_dir]
    if "scenario_seed" in game:
        command += ["--seed", str(game["scenario_seed"])]
    bot_seeds = [None, None]
    bot_seeds[candidate_player - 1] = game.get("candidate_bot_seed")
    bot_seeds[2 - candidate_player] = game.get("opponent_bot_seed")
    for player, bot_seed in enumerate(bot_seeds, 1):
        if bot_seed is not None:
            command += [f"--bot-seed{player}", str(bot_seed)]
    return command


def main():
    parser = argparse.ArgumentParser(description="Run and incrementally archive a small evaluation schedule.")
    parser.add_argument("--schedule", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--runner", default=str(Path(__file__).with_name("run_match.py")))
    parser.add_argument("--artifacts-dir", default="artifacts")
    parser.add_argument("--concurrency", type=int)
    parser.add_argument("--no-publish", action="store_true", help="Skip the configured completion hook (tests/local inspection).")
    args = parser.parse_args()
    if args.concurrency is not None and args.concurrency < 1:
        parser.error("--concurrency must be positive")

    schedule_path = Path(args.schedule).resolve()
    candidate = Path(args.candidate).resolve()
    schedule = json.loads(schedule_path.read_text())
    validate_schedule(parser, schedule)
    scheduled_concurrency = schedule.get("concurrency")
    if args.concurrency is None:
        args.concurrency = scheduled_concurrency or 2
    elif scheduled_concurrency is not None and args.concurrency != scheduled_concurrency:
        parser.error(f"--concurrency {args.concurrency} does not match frozen schedule concurrency {scheduled_concurrency}")
    verify_schedule_inputs(parser, schedule)
    candidate_hash = sha256(candidate)
    if candidate_hash != schedule["candidate"].get("sha256"):
        parser.error("candidate SHA-256 does not match the frozen schedule")
    opponent_identities = {}
    for name, opponent in schedule["opponents"].items():
        path = Path(opponent["path"]).resolve()
        actual_hash = sha256(path)
        if actual_hash != opponent.get("sha256"):
            parser.error(f"opponent {name} SHA-256 does not match the frozen schedule")
        opponent_identities[name] = {"path": str(path), "sha256": actual_hash, "race": opponent["race"]}
    experiment_dir = Path(args.artifacts_dir).resolve() / "experiments" / schedule["experiment_id"]
    experiment_dir.mkdir(parents=True, exist_ok=False)
    persisted_schedule = experiment_dir / "schedule.json"
    atomic_json(persisted_schedule, schedule)
    logs_dir = experiment_dir / "runner-logs"
    logs_dir.mkdir()
    manifest_path = experiment_dir / "manifest.json"
    records = [{"index": index, "opponent": game["opponent"], "map": game["map"],
                "candidate_player": game["candidate_player"], "status": "pending"}
               for index, game in enumerate(schedule["games"], 1)]
    batch_started = time.monotonic()
    invalid_stop = schedule.get("stop_after_consecutive_invalid", 2)
    ledger = {"schema_version": 1, "experiment_id": schedule["experiment_id"], "started_at": utc_now(),
              "finished_at": None, "status": "running", "hypothesis": schedule["hypothesis"],
              "stop_condition": schedule["stop_condition"], "candidate": {"path": str(candidate), "sha256": candidate_hash},
              "opponents": opponent_identities,
              "schedule": {"path": str(persisted_schedule), "sha256": sha256(persisted_schedule)},
              "concurrency": args.concurrency, "infrastructure_stop_after_consecutive": invalid_stop,
              "measurement_scope": "Batch wall time includes runner launch, games, and incremental archival; per-game measurements come from run_match.",
              "games": records, "summary": summarize([], schedule["opponents"])}
    atomic_json(manifest_path, ledger)

    stopping = False
    stop_started = None
    running = {}
    def stop(_signum, _frame):
        nonlocal stopping, stop_started
        stopping = True
        stop_started = stop_started or time.monotonic()
        for process in running:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    next_game = 0
    consecutive_infrastructure_failures = 0
    stopped_by_failure_rule = False
    batch_error = None
    infrastructure_classes = {"crash", "timeout", "missing_or_inconsistent_metadata", "launcher_failure"}
    try:
        while next_game < len(records) or running:
            while not stopping and consecutive_infrastructure_failures < invalid_stop and next_game < len(records) and len(running) < args.concurrency:
                game = schedule["games"][next_game]
                opponent = schedule["opponents"][game["opponent"]]
                command = command_for(args, schedule, game, candidate, opponent)
                stdout_path = logs_dir / f"game-{next_game + 1:04d}.stdout.log"
                stderr_path = logs_dir / f"game-{next_game + 1:04d}.stderr.log"
                stdout_file = stdout_path.open("w")
                stderr_file = stderr_path.open("w")
                try:
                    process = subprocess.Popen(command, stdout=stdout_file, stderr=stderr_file, text=True, start_new_session=True)
                except OSError as error:
                    stdout_file.close(); stderr_file.close()
                    records[next_game].update({"status": "finished", "classification": "launcher_failure",
                                               "launch_error": repr(error), "finished_at": utc_now()})
                    next_game += 1
                    consecutive_infrastructure_failures += 1
                    atomic_json(manifest_path, ledger)
                    continue
                records[next_game].update({"status": "running", "command": command, "started_at": utc_now(),
                                           "runner_pid": process.pid, "runner_stdout": str(stdout_path),
                                           "runner_stderr": str(stderr_path)})
                running[process] = {"index": next_game, "stdout": stdout_file, "stderr": stderr_file,
                                    "stdout_path": stdout_path}
                next_game += 1
                atomic_json(manifest_path, ledger)
            if consecutive_infrastructure_failures >= invalid_stop and not running:
                stopped_by_failure_rule = True
                for record in records[next_game:]:
                    record.update({"status": "skipped", "classification": "stopped_after_repeated_infrastructure_failure"})
                next_game = len(records)
            if not running:
                break
            time.sleep(0.05)
            if stopping and stop_started is not None and time.monotonic() - stop_started > 10:
                for process in running:
                    if process.poll() is None:
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
            for process, state in list(running.items()):
                if process.poll() is None:
                    continue
                state["stdout"].close(); state["stderr"].close()
                index = state["index"]
                record = records[index]
                record.update({"finished_at": utc_now(), "runner_return_code": process.returncode})
                try:
                    stdout = state["stdout_path"].read_text()
                    candidates = [line.strip() for line in stdout.splitlines() if line.strip().endswith("manifest.json")]
                    if not candidates or not Path(candidates[-1]).is_file():
                        raise ValueError("runner did not print a readable manifest path")
                    match_path = Path(candidates[-1]).resolve()
                    match = json.loads(match_path.read_text())
                    classification = classify(match, record["candidate_player"], process.returncode)
                    record.update({"status": "finished", "match_manifest": str(match_path),
                                   "classification": classification, "measurements": match_measurements(match)})
                except (OSError, ValueError, json.JSONDecodeError) as error:
                    record.update({"status": "finished", "classification": "launcher_failure", "finalization_error": repr(error)})
                del running[process]
                if record["classification"] in infrastructure_classes:
                    consecutive_infrastructure_failures += 1
                else:
                    consecutive_infrastructure_failures = 0
                ledger["summary"] = summarize([r for r in records if "classification" in r], schedule["opponents"])
                atomic_json(manifest_path, ledger)
    except Exception as error:
        batch_error = repr(error)
    finally:
        for process, state in list(running.items()):
            if process.poll() is None:
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                    process.wait(timeout=10)
                except (ProcessLookupError, subprocess.TimeoutExpired):
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.wait()
            state["stdout"].close(); state["stderr"].close()
            record = records[state["index"]]
            if record["status"] == "running":
                record.update({"status": "finished", "classification": "launcher_failure",
                               "runner_return_code": process.returncode,
                               "finalization_error": batch_error or "batch stopped before runner finalization",
                               "finished_at": utc_now()})

    if stopping:
        ledger["status"] = "interrupted"
    elif batch_error:
        ledger["status"] = "failed"
        ledger["batch_error"] = batch_error
    elif stopped_by_failure_rule:
        ledger["status"] = "stopped_after_repeated_infrastructure_failure"
    else:
        ledger["status"] = "completed"
    ledger["finished_at"] = utc_now()
    ledger["elapsed_seconds"] = time.monotonic() - batch_started
    ledger["runner_notes"] = "Results await evaluation against the registered acceptance criteria. No playing-strength promotion is implied."
    ledger["summary"] = summarize([r for r in records if "classification" in r], schedule["opponents"])
    atomic_json(manifest_path, ledger)
    hook = schedule.get("publish_hook")
    if hook and not args.no_publish:
        hook_path = Path(hook).resolve()
        hook_log = logs_dir / "publish-hook.log"
        environment = os.environ.copy()
        environment["EXPERIMENT_MANIFEST"] = str(manifest_path)
        with hook_log.open("w") as output:
            try:
                hook_process = subprocess.Popen([str(hook_path)], stdout=output, stderr=subprocess.STDOUT,
                                                env=environment, text=True, start_new_session=True,
                                                cwd=Path(__file__).resolve().parents[1])
                try:
                    hook_return_code = hook_process.wait(timeout=90)
                except subprocess.TimeoutExpired:
                    os.killpg(hook_process.pid, signal.SIGTERM)
                    try:
                        hook_process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        os.killpg(hook_process.pid, signal.SIGKILL)
                        hook_process.wait()
                    raise
                ledger["publish_hook"] = {"path": str(hook_path), "pid": hook_process.pid,
                                          "return_code": hook_return_code,
                                          "log": str(hook_log)}
            except (OSError, subprocess.TimeoutExpired) as error:
                ledger["publish_hook"] = {"path": str(hook_path), "error": repr(error), "log": str(hook_log)}
        atomic_json(manifest_path, ledger)
    elif hook and args.no_publish:
        ledger["publish_hook"] = {"path": str(Path(hook).resolve()), "status": "skipped_by_cli"}
        atomic_json(manifest_path, ledger)
    print(manifest_path)
    return 0 if ledger["status"] == "completed" else (130 if ledger["status"] == "interrupted" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
