#!/usr/bin/env python3
"""Score archived hill-climb games from manifests and screp replay commands.

This is an exploratory instrument, not an Elo estimator or promotion gate. It
only reads an experiment ledger, match manifests, and archived replays. Every
input path, hash check, parser result, and heuristic is retained in the output
scorecard so a later decision can review the raw evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w") as output:
        json.dump(value, output, indent=2, sort_keys=True)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


def outcome_performance(candidate_result: dict[str, object]) -> dict[str, object]:
    """Classify result metadata without treating replay commands as outcomes."""
    winner = candidate_result.get("winner")
    frames = candidate_result.get("frame_count")
    probes = candidate_result.get("max_probes")
    gateways = candidate_result.get("max_gateways")
    zealots = candidate_result.get("max_zealots") or 0
    dragoons = candidate_result.get("max_dragoons") or 0
    rejected = candidate_result.get("rejected_commands")
    categories = candidate_result.get("command_categories") or {}
    train_count = (categories.get("train") or [0])[0] if isinstance(categories, dict) else 0
    build_count = (categories.get("build") or [0])[0] if isinstance(categories, dict) else 0
    attack_count = (categories.get("attack") or [0])[0] if isinstance(categories, dict) else 0
    production_fields = {
        "probes_at_least_10": isinstance(probes, int) and probes >= 10,
        "gateway_completed_or_observed": isinstance(gateways, int) and gateways >= 1,
        "combat_units_at_least_3": isinstance(zealots, int) and isinstance(dragoons, int) and zealots + dragoons >= 3,
        "accepted_train_commands": isinstance(train_count, int) and train_count > 0,
        "accepted_build_commands": isinstance(build_count, int) and build_count > 0,
    }
    early_threat_survival = {
        "survived_opening_window": isinstance(frames, int) and frames >= 9000,
        "reached_worker_threshold": production_fields["probes_at_least_10"],
        "reached_combat_threshold": production_fields["combat_units_at_least_3"],
    }
    production_score = sum(production_fields.values())
    survival_score = sum(early_threat_survival.values())
    if winner is True:
        grade = "win"
    elif winner is not False:
        grade = "unverified"
    elif production_score >= 3 and survival_score >= 2:
        grade = "competitive_loss"
    elif production_score >= 2 or survival_score >= 1:
        grade = "partial_loss"
    else:
        grade = "early_loss"
    return {
        "grade": grade,
        "production_score": production_score,
        "survival_score": survival_score,
        "production_fields": production_fields,
        "early_threat_survival": early_threat_survival,
        "command_counts": {"train": train_count, "build": build_count, "attack": attack_count},
        "rejected_commands": rejected,
        "note": "Descriptive heuristic only: thresholds are max counters and terminal metadata, not a causal measure of strength or hidden-state survival.",
    }


def parse_replay(path: Path, screp: Path) -> dict[str, object]:
    result: dict[str, object] = {
        "path": str(path),
        "sha256": sha256(path) if path.is_file() else None,
        "exists": path.is_file(),
    }
    if not path.is_file():
        result["grade"] = "missing"
        return result
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json") as parsed_output:
        completed = subprocess.run(
            [str(screp), "-cmds=true", "-computed=true", "-map=false", "-indent=false", str(path)],
            stdout=parsed_output,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        parsed_output.seek(0)
        try:
            parsed = json.load(parsed_output) if completed.returncode == 0 else None
        except json.JSONDecodeError:
            parsed = None
    result["screp_exit_code"] = completed.returncode
    result["stderr"] = completed.stderr[-2000:]
    header = parsed.get("Header") if isinstance(parsed, dict) else None
    commands = parsed.get("Commands") if isinstance(parsed, dict) else None
    rows = commands.get("Cmds") if isinstance(commands, dict) else None
    parse_errors = commands.get("ParseErrCmds") if isinstance(commands, dict) else None
    rows = rows if isinstance(rows, list) else []
    result["frames"] = header.get("Frames") if isinstance(header, dict) else None
    result["parse_error_commands"] = parse_errors
    result["command_count"] = len(rows)
    type_counts: dict[str, int] = {}
    order_counts: dict[str, int] = {}
    build_units: list[str] = []
    morph_units: list[str] = []
    first_frames: dict[str, int | None] = {"build": None, "production": None, "attack": None, "harvest": None}
    for row in rows:
        if not isinstance(row, dict):
            continue
        command_type = (row.get("Type") or {}).get("Name")
        order = (row.get("Order") or {}).get("Name")
        if isinstance(command_type, str):
            type_counts[command_type] = type_counts.get(command_type, 0) + 1
        if isinstance(order, str):
            order_counts[order] = order_counts.get(order, 0) + 1
        frame = row.get("Frame")
        frame = frame if isinstance(frame, int) else None
        if command_type == "Build":
            if first_frames["build"] is None:
                first_frames["build"] = frame
            unit = (row.get("Unit") or {}).get("Name")
            if isinstance(unit, str) and unit not in build_units:
                build_units.append(unit)
        if command_type in {"Train", "Unit Morph", "Building Morph", "Research", "Upgrade"}:
            if first_frames["production"] is None:
                first_frames["production"] = frame
            unit = (row.get("Unit") or {}).get("Name")
            if isinstance(unit, str) and unit not in morph_units:
                morph_units.append(unit)
        if isinstance(order, str) and order.startswith("Attack"):
            if first_frames["attack"] is None:
                first_frames["attack"] = frame
        if isinstance(order, str) and order.startswith("Harvest"):
            if first_frames["harvest"] is None:
                first_frames["harvest"] = frame
    attacks = sum(value for name, value in order_counts.items() if name.startswith("Attack"))
    harvests = sum(value for name, value in order_counts.items() if name.startswith("Harvest"))
    has_categories = {
        "economy": harvests > 0,
        "construction": bool(build_units),
        "production": bool(morph_units),
        "combat": attacks > 0,
    }
    categories = sum(has_categories.values())
    result.update({
        "type_counts": dict(sorted(type_counts.items())),
        "order_counts": dict(sorted(order_counts.items())),
        "build_units": build_units,
        "production_units": morph_units,
        "first_frames": first_frames,
        "attack_orders": attacks,
        "harvest_orders": harvests,
        "signals": has_categories,
        "heuristic_score": categories * 25,
        "heuristic_grade": "strong" if categories == 4 else "partial" if categories >= 2 else "weak",
        "note": "Command-derived exploratory signals only; replay commands do not prove command acceptance or hidden state.",
    })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--artifacts-dir", default="artifacts")
    parser.add_argument("--screp", default=".tools/screp/screp")
    parser.add_argument("--output", help="Scorecard path; defaults to the experiment directory.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    experiment_dir = (root / args.artifacts_dir / "experiments" / args.experiment_id).resolve()
    ledger_path = experiment_dir / "manifest.json"
    schedule_path = experiment_dir / "schedule.json"
    if not ledger_path.is_file():
        parser.error(f"missing experiment ledger: {ledger_path}")
    ledger = json.loads(ledger_path.read_text())
    schedule = json.loads(schedule_path.read_text()) if schedule_path.is_file() else {}
    candidate_spec = schedule.get("candidate") or {}
    candidate_name = candidate_spec.get("name") or "Kestrel"
    candidate_sha = candidate_spec.get("sha256")
    screp = (root / args.screp).resolve()
    games = []
    for record in ledger.get("games", []):
        manifest_path = Path(record.get("match_manifest", ""))
        if not manifest_path.is_absolute():
            manifest_path = (root / manifest_path).resolve()
        game = {"index": record.get("index"), "record": record, "manifest_path": str(manifest_path)}
        if not manifest_path.is_file():
            game["error"] = "missing_match_manifest"
            games.append(game)
            continue
        manifest = json.loads(manifest_path.read_text())
        players = manifest.get("players", [])
        def is_candidate(player: dict) -> bool:
            if player.get("name") == candidate_name:
                return True
            environment = player.get("environment") or {}
            module_path = str(environment.get("BWAPI_CONFIG_AI__AI") or "")
            if candidate_sha and candidate_sha in module_path:
                return True
            metadata = player.get("result_metadata") or {}
            return metadata.get("bot") == candidate_name or (candidate_name.split()[0] == metadata.get("bot"))

        candidate = next((p for p in players if is_candidate(p)), None)
        if candidate is None:
            game["error"] = f"candidate_player_not_found:{candidate_name}"
            games.append(game)
            continue
        candidate_player = candidate.get("player")
        candidate_result = candidate.get("result_metadata") or {}
        replay = next((r for r in manifest.get("replays", []) if r.get("player") == candidate_player), None)
        game.update({
            "run_id": manifest.get("run_id"),
            "candidate_player": candidate_player,
            "status": manifest.get("status"),
            "outcome_verified": manifest.get("outcome_verified"),
            "candidate_result_metadata": candidate_result,
            "candidate_outcome": "win" if candidate_result.get("winner") is True else "loss" if candidate_result.get("winner") is False else "unknown",
            "elapsed_seconds": manifest.get("elapsed_seconds"),
            "durable_completion_seconds": manifest.get("durable_completion_seconds"),
            "terminal_frames": candidate_result.get("frame_count"),
            "durable_fps": manifest.get("durable_logical_frames_per_wall_second"),
            "short_game": isinstance(manifest.get("elapsed_seconds"), (int, float)) and manifest["elapsed_seconds"] <= 300,
            "outcome_performance": outcome_performance(candidate_result),
        })
        if not replay:
            game["error"] = "candidate_replay_missing"
        else:
            replay_path = Path(replay.get("path", ""))
            game["replay"] = parse_replay(replay_path, screp)
            game["replay"]["manifest_sha256"] = replay.get("sha256")
            game["replay"]["manifest_hash_matches"] = game["replay"].get("sha256") == replay.get("sha256")
        games.append(game)
    valid = [g for g in games if isinstance(g.get("replay"), dict) and g["replay"].get("exists")]
    aggregate = {"games": len(games), "scored_replays": len(valid),
                 "grades": {grade: sum(g["replay"].get("heuristic_grade") == grade for g in valid)
                            for grade in ("strong", "partial", "weak", "missing")},
                 "candidate_outcomes": {outcome: sum(g.get("candidate_outcome") == outcome for g in games)
                                        for outcome in ("win", "loss", "unknown")},
                 "outcome_performance_grades": {grade: sum((g.get("outcome_performance") or {}).get("grade") == grade for g in games)
                                                 for grade in ("win", "competitive_loss", "partial_loss", "early_loss", "unverified")},
                 "short_games": sum(g.get("short_game") is True for g in games),
                 "signals": {name: sum(g["replay"].get("signals", {}).get(name, False) for g in valid)
                             for name in ("economy", "construction", "production", "combat")}}
    output = Path(args.output).resolve() if args.output else experiment_dir / "hillclimb-scorecard.json"
    scorecard = {"schema_version": 1, "experiment_id": args.experiment_id,
                 "candidate_name": candidate_name, "ledger_path": str(ledger_path),
                 "ledger_sha256": sha256(ledger_path), "schedule_path": str(schedule_path) if schedule_path.is_file() else None,
                 "screp": str(screp), "measurement_scope": "One candidate-owned replay per archived game.",
                 "aggregate": aggregate, "games": games,
                 "decision_note": "Exploratory hill-climb scorecard only; do not use as Elo, a promotion gate, or tournament evidence."}
    atomic_json(output, scorecard)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
