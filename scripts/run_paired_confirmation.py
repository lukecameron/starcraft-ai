#!/usr/bin/env python3
"""Run one frozen serial paired schedule through run_match.py with durable checkpoints."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time


ALLOWED_KILL_EVENTS = {
    ("controller_not_occupied_after_action", 87),
    ("transport_callback", -1),
}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w") as output:
        json.dump(value, output, indent=2, sort_keys=True)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_schedule(schedule, root):
    for key in ("experiment_id", "eval_plan_sha256", "launcher", "library_path",
                "game_data_dir", "wall_timeout_seconds", "cohort_wall_cap_seconds",
                "stop_after_consecutive_invalid", "attempts"):
        require(key in schedule, f"schedule missing {key}")
    attempts = schedule["attempts"]
    require({(item.get("source"), item.get("action_id")) for item in schedule.get("allowed_kill_events", [])}
            == ALLOWED_KILL_EVENTS, "schedule allowed_kill_events differs from reviewed engine diagnostics")
    for item in schedule.get("required_files", []):
        path = (root / item["path"]).resolve()
        require(path.is_file() and sha256(path) == item["sha256"], f"required file mismatch {path}")
    require(isinstance(attempts, list) and attempts, "attempts must be a nonempty list")
    require([row.get("attempt") for row in attempts] == list(range(1, len(attempts) + 1)),
            "attempt numbers must be contiguous from 1")
    for row in attempts:
        for key in ("pair", "arm", "map", "scenario_seed", "candidate_player", "candidate", "opponent"):
            require(key in row, f"attempt {row.get('attempt')} missing {key}")
        require(row["candidate_player"] in (1, 2), "candidate_player must be 1 or 2")
        require(type(row["scenario_seed"]) is int and 0 <= row["scenario_seed"] <= 0xFFFFFFFF,
                "scenario_seed must be uint32")
        for identity in (row["candidate"], row["opponent"]):
            require(identity.get("race") in ("Terran", "Protoss", "Zerg", "Random"), "invalid race")
            path = (root / identity["path"]).resolve()
            require(path.is_file(), f"missing module {path}")
            require(sha256(path) == identity["sha256"], f"module hash mismatch {path}")
    pair_ids = sorted({row["pair"] for row in attempts})
    require(pair_ids == list(range(1, max(pair_ids) + 1)), "pair numbers must be contiguous")


def command(schedule, row, root, runner, artifacts_dir):
    candidate = row["candidate"]
    opponent = row["opponent"]
    players = [candidate, opponent]
    if row["candidate_player"] == 2:
        players.reverse()
    result = [sys.executable, str(runner),
              "--launcher", str((root / schedule["launcher"]).resolve()),
              "--library-path", str((root / schedule["library_path"]).resolve()),
              "--game-data-dir", str((root / schedule["game_data_dir"]).resolve()),
              "--map", row["map"],
              "--bot1", str((root / players[0]["path"]).resolve()), "--race1", players[0]["race"], "--name1", players[0]["name"],
              "--bot2", str((root / players[1]["path"]).resolve()), "--race2", players[1]["race"], "--name2", players[1]["name"],
              "--purpose", schedule["purpose"], "--experiment-id", schedule["experiment_id"],
              "--seed", str(row["scenario_seed"]), "--wall-timeout", str(schedule["wall_timeout_seconds"]),
              "--artifacts-dir", str(artifacts_dir)]
    candidate_seed = row.get("candidate_bot_seed")
    if candidate_seed is not None:
        result += [f"--bot-seed{row['candidate_player']}", str(candidate_seed)]
    return result


def inspect_manifest(manifest_path, screp):
    reasons = []
    review = []
    manifest = json.loads(manifest_path.read_text())
    players = manifest.get("players", [])
    if manifest.get("status") != "completed": reasons.append("status_not_completed")
    if manifest.get("outcome_verified") is not True: reasons.append("outcome_not_verified")
    if [player.get("return_code") for player in players] != [0, 0]: reasons.append("nonzero_child_exit")
    results = manifest.get("result")
    winners = [item.get("winner") for item in results] if isinstance(results, list) and all(isinstance(item, dict) for item in results) else []
    if len(winners) != 2 or not all(isinstance(value, bool) for value in winners) or set(winners) != {False, True}:
        reasons.append("terminal_results_not_opposing")
    kill_events = []
    for log in manifest_path.parent.glob("player-*/stderr.log"):
        for line in log.read_text(errors="replace").splitlines():
            if "insync_hash_mismatch" in line:
                reasons.append("insync_hash_mismatch")
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("event") == "kill_client":
                key = (event.get("source"), event.get("action_id"))
                kill_events.append({"player_log": str(log), "source": key[0], "action_id": key[1]})
                if key not in ALLOWED_KILL_EVENTS:
                    review.append(f"unrecognized_kill_event:{key[0]}:{key[1]}")
    replay_rows = []
    for replay in manifest.get("replays", []):
        path = Path(replay["path"])
        row = {"player": replay.get("player"), "path": str(path), "recorded_sha256": replay.get("sha256")}
        row["actual_sha256"] = sha256(path) if path.is_file() else None
        row["hash_matches"] = row["actual_sha256"] == row["recorded_sha256"]
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json") as parsed_output:
            parsed = subprocess.run([str(screp), "-cmds=true", "-computed=true", "-map=false", "-indent=false", str(path)],
                                    stdout=parsed_output, stderr=subprocess.PIPE, text=True)
            parsed_output.seek(0)
            try:
                parsed_json = json.load(parsed_output) if parsed.returncode == 0 else None
            except json.JSONDecodeError:
                parsed_json = None
        row["screp_exit_code"] = parsed.returncode
        header = parsed_json.get("Header") if isinstance(parsed_json, dict) else None
        commands = parsed_json.get("Commands") if isinstance(parsed_json, dict) else None
        parse_errors = commands.get("ParseErrCmds") if isinstance(commands, dict) else None
        row["parse_error_commands"] = parse_errors
        player_number = replay.get("player")
        owner = results[player_number - 1] if header and player_number in (1, 2) and isinstance(results, list) and len(results) == 2 and isinstance(results[player_number - 1], dict) else None
        row["header_frames"] = header.get("Frames") if header else None
        row["owner_callback_frame"] = owner.get("frame_count") if owner else None
        row["frame_matches"] = bool(header and owner and header.get("Frames") + 1 == owner.get("frame_count"))
        input_players = manifest.get("inputs", {}).get("players", []) if isinstance(manifest.get("inputs"), dict) else []
        expected_races = sorted(player.get("race") for player in input_players if isinstance(player, dict) and isinstance(player.get("race"), str))
        row["header_races"] = sorted(player["Race"]["Name"] for player in header["Players"]) if header else None
        row["races_match"] = bool(header and len(expected_races) == 2 and row["header_races"] == expected_races)
        replay_rows.append(row)
        if not row["hash_matches"]: reasons.append(f"replay_hash_player_{row['player']}")
        if parsed.returncode != 0: reasons.append(f"replay_parse_player_{row['player']}")
        if parsed_json is None: reasons.append(f"replay_json_player_{row['player']}")
        if parse_errors: reasons.append(f"replay_command_parse_errors_player_{row['player']}")
        if not row["frame_matches"]: reasons.append(f"replay_frame_player_{row['player']}")
        if not row["races_match"]: reasons.append(f"replay_race_player_{row['player']}")
    if len(replay_rows) != 2: reasons.append("replay_count_not_two")
    return manifest, sorted(set(reasons)), review, kill_events, replay_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schedule", required=True)
    parser.add_argument("--artifacts-dir", default="artifacts")
    parser.add_argument("--runner", default=str(Path(__file__).with_name("run_match.py")))
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    schedule_path = Path(args.schedule).resolve()
    schedule = json.loads(schedule_path.read_text())
    validate_schedule(schedule, root)
    if args.validate_only:
        print(f"valid schedule {sha256(schedule_path)}: {len(schedule['attempts'])} attempts")
        return 0

    artifacts_dir = (root / args.artifacts_dir).resolve()
    experiment_dir = artifacts_dir / "experiments" / schedule["experiment_id"]
    ledger_path = experiment_dir / "paired-ledger.json"
    schedule_hash = sha256(schedule_path)
    if ledger_path.exists():
        ledger = json.loads(ledger_path.read_text())
        require(ledger["schedule_sha256"] == schedule_hash, "existing ledger schedule hash mismatch")
        require(ledger.get("status") not in ("completed", "stopped_consecutive_invalid", "halted_review_required", "cohort_wall_cap"),
                f"ledger status {ledger.get('status')} requires reviewed resolution, not automatic resume")
        unresolved = [item for item in ledger.get("attempts", []) if item.get("status") == "running"]
        require(not unresolved, f"unresolved launched attempts require review: {[item.get('attempt') for item in unresolved]}")
    else:
        experiment_dir.mkdir(parents=True, exist_ok=False)
        frozen_schedule = experiment_dir / "schedule.json"
        atomic_json(frozen_schedule, schedule)
        ledger = {"schema_version": 1, "experiment_id": schedule["experiment_id"],
                  "eval_plan_sha256": schedule["eval_plan_sha256"], "schedule_sha256": schedule_hash,
                  "frozen_schedule_sha256": sha256(frozen_schedule), "started_at": utc_now(),
                  "status": "running", "attempts": [], "pairs": []}
        atomic_json(ledger_path, ledger)

    launched = {item["attempt"] for item in ledger["attempts"]}
    invalid_streak = ledger["attempts"][-1].get("consecutive_invalid", 0) if ledger["attempts"] else 0
    active_mark = time.monotonic()
    def checkpoint_elapsed():
        nonlocal active_mark
        now = time.monotonic()
        ledger["active_elapsed_seconds"] = ledger.get("active_elapsed_seconds", 0.0) + now - active_mark
        active_mark = now
    runner = Path(args.runner).resolve()
    screp = root / ".tools/screp/screp"
    active = None
    try:
        for row in schedule["attempts"]:
            if row["attempt"] in launched:
                continue
            checkpoint_elapsed()
            if ledger["active_elapsed_seconds"] >= schedule["cohort_wall_cap_seconds"]:
                ledger["status"] = "cohort_wall_cap"
                break
            record = {key: row[key] for key in ("attempt", "pair", "arm", "map", "scenario_seed", "candidate_player")}
            record.update({"status": "running", "started_at": utc_now()})
            ledger["attempts"].append(record)
            atomic_json(ledger_path, ledger)
            logs = experiment_dir / "runner-logs"
            logs.mkdir(exist_ok=True)
            stdout_path = logs / f"attempt-{row['attempt']:03d}.stdout.log"
            stderr_path = logs / f"attempt-{row['attempt']:03d}.stderr.log"
            cmd = command(schedule, row, root, runner, artifacts_dir)
            record["command"] = cmd
            with stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
                active = subprocess.Popen(cmd, cwd=root, stdout=stdout, stderr=stderr, start_new_session=True)
                record["runner_pid"] = active.pid
                atomic_json(ledger_path, ledger)
                while True:
                    checkpoint_elapsed()
                    remaining = schedule["cohort_wall_cap_seconds"] - ledger["active_elapsed_seconds"]
                    if remaining <= 0:
                        os.killpg(active.pid, signal.SIGTERM)
                        try:
                            active.wait(timeout=10)
                        except subprocess.TimeoutExpired:
                            os.killpg(active.pid, signal.SIGKILL)
                            active.wait()
                        record["runner_return_code"] = active.returncode
                        record["cohort_cap_during_attempt"] = True
                        break
                    try:
                        record["runner_return_code"] = active.wait(timeout=min(5.0, remaining))
                        break
                    except subprocess.TimeoutExpired:
                        checkpoint_elapsed()
                        atomic_json(ledger_path, ledger)
                active = None
            record["finished_at"] = utc_now()
            record["runner_stdout"] = str(stdout_path)
            record["runner_stderr"] = str(stderr_path)
            lines = stdout_path.read_text().strip().splitlines()
            manifest_path = Path(lines[-1]) if lines else None
            record["manifest_path"] = str(manifest_path) if manifest_path else None
            reasons = []
            review = []
            if record["runner_return_code"] != 0: reasons.append(f"runner_return_code_{record['runner_return_code']}")
            if not manifest_path or not manifest_path.is_file():
                reasons.append("missing_manifest")
            else:
                try:
                    manifest, found, review, kills, replays = inspect_manifest(manifest_path, screp)
                    reasons.extend(found)
                    record.update({"run_id": manifest.get("run_id"), "manifest_sha256": sha256(manifest_path),
                                   "kill_events": kills, "review_required": review, "replays": replays,
                                   "durable_fps": manifest.get("durable_logical_frames_per_wall_second")})
                except (OSError, ValueError, TypeError, KeyError, IndexError, json.JSONDecodeError) as error:
                    reasons.append(f"manifest_inspection_error:{type(error).__name__}")
                    record["inspection_error"] = str(error)
            record["invalid_reasons"] = sorted(set(reasons))
            record["status"] = "review_required" if review else ("valid" if not reasons else "invalid")
            invalid_streak = invalid_streak + 1 if reasons else 0
            record["consecutive_invalid"] = invalid_streak
            completed_pair = [item for item in ledger["attempts"] if item["pair"] == row["pair"]]
            expected_pair = [item for item in schedule["attempts"] if item["pair"] == row["pair"]]
            if len(completed_pair) == len(expected_pair):
                ledger["pairs"] = [item for item in ledger["pairs"] if item["pair"] != row["pair"]]
                ledger["pairs"].append({"pair": row["pair"], "checkpointed_at": utc_now(),
                                        "attempts": [item["attempt"] for item in completed_pair],
                                        "statuses": [item["status"] for item in completed_pair]})
            atomic_json(ledger_path, ledger)
            print(json.dumps({"attempt": row["attempt"], "pair": row["pair"], "arm": row["arm"],
                              "run_id": record.get("run_id"), "status": record["status"]}), flush=True)
            if record.get("cohort_cap_during_attempt"):
                ledger["status"] = "cohort_wall_cap"
                break
            if review:
                ledger["status"] = "halted_review_required"
                break
            if invalid_streak >= schedule["stop_after_consecutive_invalid"]:
                ledger["status"] = "stopped_consecutive_invalid"
                break
        else:
            ledger["status"] = "completed"
    except (KeyboardInterrupt, SystemExit):
        ledger["status"] = "interrupted"
        if active is not None:
            os.killpg(active.pid, signal.SIGTERM)
            try:
                active.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(active.pid, signal.SIGKILL)
                active.wait()
        raise
    finally:
        checkpoint_elapsed()
        ledger["finished_at"] = utc_now()
        atomic_json(ledger_path, ledger)
    return 0 if ledger["status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
