#!/usr/bin/env python3
"""Score archived Kestrel games from manifests, diagnostics, and screp replays.

This is an exploratory instrument, not an Elo estimator or promotion gate. It
reads an experiment ledger, match manifests, Kestrel scalar/JSONL diagnostics,
and archived replays. Every input path, hash check, parser result, and
heuristic is retained in the output scorecard so a later decision can review
the raw evidence.
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
    rejection_free = rejected == 0
    if winner is True:
        grade = "win"
    elif winner is not False:
        grade = "unverified"
    elif not rejection_free:
        grade = "partial_loss"
    elif production_score >= 3 and survival_score == 3 and isinstance(frames, int) and frames >= 12000:
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
        "rejection_free": rejection_free,
        "note": "Descriptive heuristic only: thresholds are max counters and terminal metadata, not a causal measure of strength or hidden-state survival.",
    }


def _counter(categories: object, name: str, index: int = 0) -> int:
    if not isinstance(categories, dict):
        return 0
    value = categories.get(name)
    if isinstance(value, list) and len(value) > index and isinstance(value[index], int):
        return value[index]
    return 0


def _resolve_path(path: object, root: Path) -> Path | None:
    if not isinstance(path, str) or not path:
        return None
    candidate = Path(path)
    return candidate if candidate.is_absolute() else (root / candidate).resolve()


def _metadata_int(metadata: dict[str, object], name: str, default: int) -> int:
    value = metadata.get(name)
    return value if isinstance(value, int) and not isinstance(value, bool) else default


def _metadata_list(metadata: dict[str, object], name: str) -> list[object]:
    value = metadata.get(name)
    return value if isinstance(value, list) else []


def _normalise_race(race: object) -> str | None:
    if not isinstance(race, str):
        return None
    value = race.strip().lower()
    return value if value in {"zerg", "terran", "protoss", "random"} else None


def _emergency_batches(frames: list[object], sizes: list[object], ids: list[object]) -> tuple[list[dict[str, object]], list[str]]:
    """Build reviewable assignment batches from v33's parallel telemetry arrays."""
    flags: list[str] = []
    if len(frames) != len(sizes):
        flags.append("assignment_trace_length_mismatch")
    batches: list[dict[str, object]] = []
    offset = 0
    for index, raw_size in enumerate(sizes):
        size = raw_size if isinstance(raw_size, int) and not isinstance(raw_size, bool) else None
        frame = frames[index] if index < len(frames) else None
        if size is None or size < 0:
            flags.append("assignment_trace_invalid_size")
            size = 0
        batch_ids = ids[offset:offset + size]
        if len(batch_ids) != size:
            flags.append("assignment_trace_id_count_mismatch")
        batches.append({"index": index, "frame": frame, "size": size, "probe_ids": batch_ids})
        offset += size
    if offset != len(ids):
        flags.append("assignment_trace_unconsumed_ids")
    return batches, flags


def _emergency_bridge_summary(metadata: dict[str, object], opponent_race: str | None = None) -> dict[str, object]:
    """Normalize v33 emergency-worker telemetry while retaining v31/v32 absence."""
    scalar_defaults = {
        "emergency_trigger_frame": -1,
        "emergency_trigger_events": 0,
        "emergency_assignments": 0,
        "emergency_assignment_batches": 0,
        "emergency_first_assignment_frame": -1,
        "emergency_first_assignment_size": 0,
        "emergency_max_assignment_batch": 0,
        "emergency_peak_defenders": 0,
        "emergency_current_defenders": 0,
        "emergency_accepted_attack_orders": 0,
        "emergency_releases": 0,
        "emergency_first_release_frame": -1,
        "emergency_threat_clear_release_events": 0,
        "emergency_threat_clear_released_defenders": 0,
        "emergency_first_threat_clear_release_frame": -1,
        "emergency_army_two_release_events": 0,
        "emergency_army_two_released_defenders": 0,
        "emergency_first_army_two_release_frame": -1,
        "emergency_defender_deaths": 0,
        "emergency_build_selection_exclusions": 0,
        "emergency_economy_exclusions": 0,
        "emergency_post_release_gather_orders": 0,
        "emergency_post_release_build_orders": 0,
        "emergency_army_at_trigger": -1,
        "emergency_local_combat_at_trigger": -1,
    }
    required = tuple(scalar_defaults) + (
        "emergency_assigned_probe_ids", "emergency_assignment_frames", "emergency_assignment_sizes",
        "emergency_release_frames", "emergency_release_sizes", "emergency_release_army_two_flags",
    )
    present = [name for name in required if name in metadata]
    missing = [name for name in required if name not in metadata]
    invalid_scalars = [name for name in scalar_defaults
                       if name in metadata and (not isinstance(metadata[name], int) or isinstance(metadata[name], bool))]
    invalid_lists = [name for name in required[len(scalar_defaults):]
                     if name in metadata and not isinstance(metadata[name], list)]
    values = {name: _metadata_int(metadata, name, default) for name, default in scalar_defaults.items()}
    assigned_ids = _metadata_list(metadata, "emergency_assigned_probe_ids")
    assignment_frames = _metadata_list(metadata, "emergency_assignment_frames")
    assignment_sizes = _metadata_list(metadata, "emergency_assignment_sizes")
    release_frames = _metadata_list(metadata, "emergency_release_frames")
    release_sizes = _metadata_list(metadata, "emergency_release_sizes")
    release_flags = _metadata_list(metadata, "emergency_release_army_two_flags")
    assignment_batches, trace_flags = _emergency_batches(assignment_frames, assignment_sizes, assigned_ids)

    release_trace_flags: list[str] = []
    if not (len(release_frames) == len(release_sizes) == len(release_flags)):
        release_trace_flags.append("release_trace_length_mismatch")
    release_trace: list[dict[str, object]] = []
    for index in range(min(len(release_frames), len(release_sizes), len(release_flags))):
        flag = release_flags[index]
        reason = "army_two" if flag == 1 else "threat_clear" if flag == 0 else "unknown"
        if flag not in (0, 1):
            release_trace_flags.append("release_trace_invalid_reason")
        release_trace.append({"index": index, "frame": release_frames[index], "size": release_sizes[index],
                              "army_two": flag, "reason": reason})

    race = _normalise_race(opponent_race)
    if race is None:
        known_zerg = metadata.get("known_zerg")
        if isinstance(known_zerg, bool):
            race = "zerg" if known_zerg else "non-zerg"
    expected_active = race == "zerg"
    expected_inactive = race in {"terran", "protoss", "non-zerg"}
    review_flags = list(trace_flags) + release_trace_flags
    opportunity_notes: list[str] = []
    if invalid_scalars:
        review_flags.append("emergency_scalar_type_mismatch")
    if invalid_lists:
        review_flags.append("emergency_trace_type_mismatch")
    if values["emergency_assignments"] != len(assigned_ids):
        review_flags.append("assignment_total_id_count_mismatch")
    if values["emergency_assignment_batches"] != len(assignment_batches):
        review_flags.append("assignment_batch_count_mismatch")
    if values["emergency_assignments"] != sum(batch["size"] for batch in assignment_batches):
        review_flags.append("assignment_total_size_mismatch")
    if assignment_batches and values["emergency_first_assignment_frame"] != assignment_batches[0]["frame"]:
        review_flags.append("first_assignment_frame_mismatch")
    if assignment_batches and values["emergency_first_assignment_size"] != assignment_batches[0]["size"]:
        review_flags.append("first_assignment_size_mismatch")
    if assignment_sizes and values["emergency_max_assignment_batch"] != max(assignment_sizes):
        review_flags.append("max_assignment_batch_mismatch")
    if values["emergency_peak_defenders"] < values["emergency_current_defenders"]:
        review_flags.append("current_defenders_exceed_peak")
    if values["emergency_peak_defenders"] > 2 or values["emergency_current_defenders"] > 2:
        review_flags.append("emergency_defender_cap_exceeded")
    if any(isinstance(size, int) and size > 2 for size in assignment_sizes):
        review_flags.append("assignment_batch_cap_exceeded")
    if values["emergency_assignments"] > 0 and values["emergency_trigger_events"] <= 0:
        review_flags.append("assignment_without_trigger")
    if values["emergency_assignments"] > 0 and values["emergency_trigger_frame"] < 0:
        review_flags.append("assignment_without_trigger_frame")
    if values["emergency_trigger_events"] > 0 and values["emergency_trigger_frame"] < 0:
        review_flags.append("trigger_without_trigger_frame")
    if values["emergency_trigger_events"] > 0 and values["emergency_assignments"] == 0:
        # A qualifying trigger can legitimately find no eligible Probe (for
        # example while the leave-four floor is active). This is descriptive
        # opportunity evidence, not a malformed telemetry trace.
        opportunity_notes.append("trigger_without_assignment")
    if values["emergency_accepted_attack_orders"] > 0 and values["emergency_assignments"] <= 0:
        review_flags.append("attack_without_assignment")
    if values["emergency_releases"] > 0 and values["emergency_assignments"] <= 0:
        review_flags.append("release_without_assignment")
    if values["emergency_current_defenders"] > values["emergency_assignments"]:
        review_flags.append("current_defenders_exceed_assignments")

    trace_reason_counts = {
        "threat_clear": sum(item["reason"] == "threat_clear" for item in release_trace),
        "army_two": sum(item["reason"] == "army_two" for item in release_trace),
        "unknown": sum(item["reason"] == "unknown" for item in release_trace),
    }
    if release_trace and values["emergency_releases"] != sum(
        size for size in release_sizes if isinstance(size, int) and not isinstance(size, bool)
    ):
        review_flags.append("release_defender_total_mismatch")
    if trace_reason_counts["threat_clear"] != values["emergency_threat_clear_release_events"]:
        review_flags.append("threat_clear_release_event_mismatch")
    if trace_reason_counts["army_two"] != values["emergency_army_two_release_events"]:
        review_flags.append("army_two_release_event_mismatch")
    threat_clear_sizes = sum(
        size for size, item in zip(release_sizes, release_trace)
        if item["reason"] == "threat_clear" and isinstance(size, int) and not isinstance(size, bool)
    )
    army_two_sizes = sum(
        size for size, item in zip(release_sizes, release_trace)
        if item["reason"] == "army_two" and isinstance(size, int) and not isinstance(size, bool)
    )
    if threat_clear_sizes != values["emergency_threat_clear_released_defenders"]:
        review_flags.append("threat_clear_release_defender_mismatch")
    if army_two_sizes != values["emergency_army_two_released_defenders"]:
        review_flags.append("army_two_release_defender_mismatch")
    if release_trace and values["emergency_first_release_frame"] != release_trace[0]["frame"]:
        review_flags.append("first_release_frame_mismatch")
    first_threat_clear = next((item["frame"] for item in release_trace if item["reason"] == "threat_clear"), None)
    first_army_two = next((item["frame"] for item in release_trace if item["reason"] == "army_two"), None)
    if first_threat_clear is not None and values["emergency_first_threat_clear_release_frame"] != first_threat_clear:
        review_flags.append("first_threat_clear_frame_mismatch")
    if first_army_two is not None and values["emergency_first_army_two_release_frame"] != first_army_two:
        review_flags.append("first_army_two_frame_mismatch")
    if values["emergency_releases"] > 0 and not release_trace:
        review_flags.append("release_total_without_release_trace")
    if values["emergency_threat_clear_release_events"] + values["emergency_army_two_release_events"] > 0 and not release_trace:
        review_flags.append("release_reason_without_release_trace")

    if expected_inactive:
        inactive_values = [values[name] for name in scalar_defaults if name not in {
            "emergency_trigger_frame",
            "emergency_first_assignment_frame", "emergency_first_release_frame",
            "emergency_first_threat_clear_release_frame", "emergency_first_army_two_release_frame",
            "emergency_army_at_trigger", "emergency_local_combat_at_trigger",
        }]
        if any(value != 0 for value in inactive_values):
            review_flags.append("non_zerg_emergency_activity")
        if any(values[name] != -1 for name in (
            "emergency_first_assignment_frame", "emergency_first_release_frame",
            "emergency_first_threat_clear_release_frame", "emergency_first_army_two_release_frame",
            "emergency_army_at_trigger", "emergency_local_combat_at_trigger",
        )):
            review_flags.append("non_zerg_emergency_sentinel_mismatch")
        if assigned_ids or assignment_frames or assignment_sizes or release_frames or release_sizes or release_flags:
            review_flags.append("non_zerg_emergency_trace_nonempty")

    assignments = values["emergency_assignments"]
    releases = values["emergency_releases"]
    recovery_status = "observed" if releases > 0 and (
        values["emergency_post_release_gather_orders"] > 0 or values["emergency_post_release_build_orders"] > 0
    ) else "untested" if releases == 0 else "unobserved"
    checks = {
        "telemetry_complete": not missing,
        "assignment_trace_consistent": not any(flag.startswith("assignment_") or flag.startswith("first_assignment") or flag.startswith("max_assignment") for flag in review_flags),
        "defender_cap": "emergency_defender_cap_exceeded" not in review_flags and "assignment_batch_cap_exceeded" not in review_flags,
        "accepted_attack_observed": values["emergency_accepted_attack_orders"] > 0 if assignments else None,
        "release_trace_consistent": not any(flag.startswith("release_") or flag.startswith("threat_clear_release") or flag.startswith("army_two_release") for flag in review_flags),
        "non_zerg_sentinels": expected_inactive and not any(flag.startswith("non_zerg_") for flag in review_flags) if expected_inactive else None,
        "recovery": recovery_status,
    }
    scored_checks = [value for value in checks.values() if isinstance(value, bool)]
    score = round(100 * sum(scored_checks) / len(scored_checks)) if scored_checks else 0
    if expected_inactive:
        grade = "pass" if checks["non_zerg_sentinels"] else "review"
    elif expected_active and assignments == 0:
        grade = "untested" if not review_flags else "review"
    elif review_flags:
        grade = "review"
    else:
        grade = "pass" if all(value is not False for value in checks.values() if isinstance(value, (bool, type(None)))) else "partial"
    return {
        "opponent_race": race,
        "expected_active": expected_active,
        "expected_inactive": expected_inactive,
        "telemetry_status": "complete" if not missing else "legacy_absent" if len(present) == 0 else "partial",
        "fields_present": present,
        "missing_fields": missing,
        "invalid_fields": invalid_scalars + invalid_lists,
        "trigger": {name.removeprefix("emergency_"): values[name] for name in (
            "emergency_trigger_frame", "emergency_trigger_events", "emergency_army_at_trigger", "emergency_local_combat_at_trigger")},
        "assignments": {
            "total": assignments,
            "batches": values["emergency_assignment_batches"],
            "first_frame": values["emergency_first_assignment_frame"],
            "first_size": values["emergency_first_assignment_size"],
            "max_batch": values["emergency_max_assignment_batch"],
            "peak_defenders": values["emergency_peak_defenders"],
            "current_defenders": values["emergency_current_defenders"],
            "accepted_attack_orders": values["emergency_accepted_attack_orders"],
            "probe_ids": assigned_ids,
            "frames": assignment_frames,
            "sizes": assignment_sizes,
            "batch_trace": assignment_batches,
        },
        "releases": {
            "total_defenders": releases,
            "first_frame": values["emergency_first_release_frame"],
            "threat_clear_events": values["emergency_threat_clear_release_events"],
            "threat_clear_defenders": values["emergency_threat_clear_released_defenders"],
            "first_threat_clear_frame": values["emergency_first_threat_clear_release_frame"],
            "army_two_events": values["emergency_army_two_release_events"],
            "army_two_defenders": values["emergency_army_two_released_defenders"],
            "first_army_two_frame": values["emergency_first_army_two_release_frame"],
            "frames": release_frames,
            "sizes": release_sizes,
            "army_two_flags": release_flags,
            "reason_counts": trace_reason_counts,
            "trace": release_trace,
        },
        "exclusions": {
            "build_selection": values["emergency_build_selection_exclusions"],
            "economy": values["emergency_economy_exclusions"],
            "total": values["emergency_build_selection_exclusions"] + values["emergency_economy_exclusions"],
        },
        "recovery": {
            "status": recovery_status,
            "post_release_gather_orders": values["emergency_post_release_gather_orders"],
            "post_release_build_orders": values["emergency_post_release_build_orders"],
        },
        "defender_deaths": values["emergency_defender_deaths"],
        "checks": checks,
        "quantitative_grade": {"score": score, "max_score": 100, "grade": grade},
        "review_flags": sorted(set(review_flags)),
        "opportunity_notes": sorted(set(opportunity_notes)),
        "note": "v33 emergency bridge counters are descriptive telemetry. Assignment totals count probe identities; release totals count released defenders; release reason counters count release events.",
    }


def _player_race(player: object) -> str | None:
    if not isinstance(player, dict):
        return None
    environment = player.get("environment") if isinstance(player.get("environment"), dict) else {}
    return _normalise_race(environment.get("BWAPI_CONFIG_AUTO_MENU__RACE"))


def read_diagnostic_events(metadata: dict[str, object], root: Path) -> dict[str, object]:
    """Read an optional Kestrel JSONL trace beside its scalar diagnostic."""
    metadata_path = _resolve_path(metadata.get("metadata_path"), root)
    search_dir = metadata_path.parent if metadata_path else None
    candidates = sorted(search_dir.glob("*.jsonl")) if search_dir and search_dir.is_dir() else []
    path = next((item for item in candidates if "kestrel" in item.name.lower() or "diagnostic" in item.name.lower()), None)
    result: dict[str, object] = {
        "path": str(path) if path else None,
        "exists": bool(path and path.is_file()),
        "parse_ok": None,
        "line_count": 0,
        "malformed_lines": 0,
        "event_counts": {},
        "first_frames": {},
    }
    if not path:
        return result
    event_counts: dict[str, int] = {}
    first_frames: dict[str, int] = {}
    try:
        with path.open() as source:
            for line in source:
                if not line.strip():
                    continue
                result["line_count"] = int(result["line_count"]) + 1
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    result["malformed_lines"] = int(result["malformed_lines"]) + 1
                    continue
                if not isinstance(row, dict):
                    result["malformed_lines"] = int(result["malformed_lines"]) + 1
                    continue
                event = row.get("event") if row.get("record") == "event" else None
                if isinstance(event, str):
                    event_counts[event] = event_counts.get(event, 0) + 1
                    frame = row.get("frame")
                    if isinstance(frame, int) and event not in first_frames:
                        first_frames[event] = frame
    except OSError as error:
        result["error"] = f"{type(error).__name__}: {error}"
    result["event_counts"] = dict(sorted(event_counts.items()))
    result["first_frames"] = dict(sorted(first_frames.items()))
    result["parse_ok"] = result.get("malformed_lines") == 0 and "error" not in result
    return result


def _diagnostic_summary(metadata: dict[str, object], root: Path, opponent_race: str | None = None) -> dict[str, object]:
    categories = metadata.get("command_categories")
    errors = metadata.get("command_error_counts")
    metadata_path = _resolve_path(metadata.get("metadata_path"), root)
    metadata_file: dict[str, object] | None = None
    metadata_file_error: str | None = None
    if metadata_path and metadata_path.is_file():
        try:
            loaded = json.loads(metadata_path.read_text())
            metadata_file = loaded if isinstance(loaded, dict) else None
            if metadata_file is None:
                metadata_file_error = "diagnostic_not_object"
        except (OSError, json.JSONDecodeError) as error:
            metadata_file_error = f"{type(error).__name__}: {error}"
    comparable_keys = ("schema_version", "frame_count", "ended", "winner", "rejected_commands", "command_count")
    metadata_mismatches = [key for key in comparable_keys if metadata_file is not None and key in metadata_file and metadata_file.get(key) != metadata.get(key)]
    attempted = sum(_counter(categories, name, 0) for name in ("build", "train", "gather", "attack"))
    rejected_by_category = sum(_counter(categories, name, 1) for name in ("build", "train", "gather", "attack"))
    rejected = metadata.get("rejected_commands")
    rejected = rejected if isinstance(rejected, int) else rejected_by_category
    command_count = metadata.get("command_count")
    command_count = command_count if isinstance(command_count, int) else attempted
    result: dict[str, object] = {
        "schema_version": metadata.get("schema_version"),
        "metadata_path": metadata.get("metadata_path"),
        "metadata_exists": bool(metadata_path and metadata_path.is_file()),
        "metadata_file_parse_ok": metadata_file is not None and metadata_file_error is None,
        "metadata_file_mismatches": metadata_mismatches,
        "metadata_file_error": metadata_file_error,
        "ended": metadata.get("ended"),
        "winner": metadata.get("winner"),
        "frame_count": metadata.get("frame_count"),
        "latency_frames": metadata.get("latency_frames"),
        "command_count": command_count,
        "attempted_commands": attempted,
        "rejected_commands": rejected,
        "rejection_rate": (rejected / attempted) if attempted else None,
        "command_categories": categories if isinstance(categories, dict) else {},
        "command_error_counts": errors if isinstance(errors, dict) else {},
        "economy": {
            "max_probes": metadata.get("max_probes"),
            "max_pylons": metadata.get("max_pylons"),
            "gas_worker_guard_events": metadata.get("gas_worker_guard_events"),
            "gas_worker_build_attempts": metadata.get("gas_worker_build_attempts"),
        },
        "production": {
            "max_gateways": metadata.get("max_gateways"),
            "max_zealots": metadata.get("max_zealots"),
            "max_dragoons": metadata.get("max_dragoons"),
            "accepted_zealot_trains": metadata.get("accepted_zealot_trains"),
            "accepted_structures_after_first_zealot": metadata.get("accepted_structures_after_first_zealot"),
            "first_pylon_accepted_frame": metadata.get("first_pylon_accepted_frame"),
            "first_gateway_accepted_frame": metadata.get("first_gateway_accepted_frame"),
            "first_gateway_completed_frame": metadata.get("first_gateway_completed_frame"),
            "first_zealot_train_frame": metadata.get("first_zealot_train_frame"),
            "first_zealot_completed_frame": metadata.get("first_zealot_completed_frame"),
        },
    }
    result["defense"] = {
        "first_home_threat_frame": metadata.get("first_home_threat_frame"),
        "first_home_army_threat_frame": metadata.get("first_home_army_threat_frame"),
        "first_local_engagement_frame": metadata.get("first_local_engagement_frame"),
        "first_home_combat_loss_frame": metadata.get("first_home_combat_loss_frame", metadata.get("first_home_zealot_loss_frame")),
        "local_combat_at_first_home_army_threat": metadata.get("local_combat_at_first_home_army_threat"),
        "global_combat_at_first_home_army_threat": metadata.get("global_combat_at_first_home_army_threat"),
        "max_local_completed_zealots_before_loss": metadata.get("max_local_completed_zealots_before_loss"),
        "max_completed_combat_units": metadata.get("max_completed_combat_units"),
    }
    result["reserve_offense"] = {
        "suppression_frame": metadata.get("first_early_zerg_stage_suppression_frame"),
        "home_move_attempts": metadata.get("early_zerg_stage_home_move_attempts", 0),
        "home_move_orders": metadata.get("early_zerg_stage_home_move_orders", 0),
        "home_target_orders": metadata.get("early_zerg_stage_home_target_orders", 0),
        "remote_target_events": metadata.get("early_zerg_stage_remote_target_events", 0),
        "remote_attack_orders": metadata.get("early_zerg_stage_remote_attack_orders", 0),
        "release_attack_orders": metadata.get("early_zerg_stage_release_attack_orders", 0),
        "release_frame": metadata.get("first_early_zerg_stage_release_frame"),
        "release_army": metadata.get("early_zerg_stage_release_army"),
        "max_army": metadata.get("early_zerg_stage_max_army"),
        "local_two_frame": metadata.get("first_early_zerg_stage_local_two_frame"),
        # v32's explicit reserve telemetry; retain the v31 stage counters above
        # so scorecards remain comparable across the policy generations.
        "zerg_reserve_current": metadata.get("zerg_reserve_current"),
        "zerg_reserve_recruit_events": metadata.get("zerg_reserve_recruit_events"),
        "zerg_reserve_death_events": metadata.get("zerg_reserve_death_events"),
        "zerg_reserve_peak": metadata.get("zerg_reserve_peak"),
        "zerg_reserve_size_at_first_home_threat": metadata.get("zerg_reserve_size_at_first_home_threat"),
        "zerg_reserve_current_surplus": metadata.get("zerg_reserve_current_surplus"),
        "zerg_reserve_max_surplus": metadata.get("zerg_reserve_max_surplus"),
        "zerg_reserve_local_threat_events": metadata.get("zerg_reserve_local_threat_events"),
        "zerg_reserve_remote_threat_events": metadata.get("zerg_reserve_remote_threat_events"),
        "zerg_reserve_remote_order_blocks": metadata.get("zerg_reserve_remote_order_blocks"),
        "zerg_reserve_local_attack_orders": metadata.get("zerg_reserve_local_attack_orders"),
        "zerg_reserve_remote_attack_orders": metadata.get("zerg_reserve_remote_attack_orders"),
        "zerg_reserve_home_move_attempts": metadata.get("zerg_reserve_home_move_attempts"),
        "zerg_reserve_home_move_orders": metadata.get("zerg_reserve_home_move_orders"),
        "zerg_reserve_home_move_cooldown_blocks": metadata.get("zerg_reserve_home_move_cooldown_blocks"),
        "zerg_reserve_home_move_repeat_orders": metadata.get("zerg_reserve_home_move_repeat_orders"),
        "zerg_reserve_home_move_repeat_units": metadata.get("zerg_reserve_home_move_repeat_units"),
        "zerg_reserve_home_move_max_accepted_per_unit": metadata.get("zerg_reserve_home_move_max_accepted_per_unit"),
        "zerg_reserve_home_move_min_accepted_repeat_interval": metadata.get("zerg_reserve_home_move_min_accepted_repeat_interval"),
        "zerg_first_reserve_three_frame": metadata.get("zerg_first_reserve_three_frame"),
        "zerg_reserved_local_at_first_home_threat": metadata.get("zerg_reserved_local_at_first_home_threat"),
        "zerg_first_accepted_surplus_release_frame": metadata.get("zerg_first_accepted_surplus_release_frame"),
        "zerg_first_accepted_surplus_release_army": metadata.get("zerg_first_accepted_surplus_release_army"),
        "zerg_nonreserve_remote_attack_orders": metadata.get("zerg_nonreserve_remote_attack_orders"),
    }
    result["events"] = read_diagnostic_events(metadata, root)
    result["emergency_bridge"] = _emergency_bridge_summary(metadata, opponent_race)
    return result


def _replay_fidelity(parsed: dict[str, object], replay: dict[str, object], diagnostic: dict[str, object]) -> dict[str, object]:
    recorded_hash = replay.get("sha256")
    actual_hash = parsed.get("sha256")
    recorded_size = replay.get("size_bytes")
    actual_size = parsed.get("size_bytes")
    parse_ok = parsed.get("screp_exit_code") == 0 and parsed.get("json_valid") is True
    parse_errors = parsed.get("parse_error_commands")
    parse_errors_ok = parse_errors in (None, [], 0)
    replay_frames = parsed.get("frames")
    diagnostic_frames = diagnostic.get("frame_count")
    frame_delta = replay_frames - diagnostic_frames if isinstance(replay_frames, int) and isinstance(diagnostic_frames, int) else None
    return {
        "archival_status": replay.get("archival_status"),
        "exists": parsed.get("exists") is True,
        "size_matches": recorded_size is None or actual_size == recorded_size,
        "hash_recorded": isinstance(recorded_hash, str),
        "hash_matches": isinstance(recorded_hash, str) and actual_hash == recorded_hash,
        "screp_parse_ok": parse_ok,
        "parse_errors_ok": parse_errors_ok,
        "frames": replay_frames,
        "diagnostic_frames": diagnostic_frames,
        "frame_delta": frame_delta,
        "frame_within_one": frame_delta is not None and abs(frame_delta) <= 1,
    }


def score_kestrel_match(manifest: dict[str, object], manifest_path: Path, screp: Path,
                        candidate_name: str = "Kestrel", candidate_sha: str | None = None,
                        root: Path | None = None) -> dict[str, object]:
    """Return a reviewable, descriptive summary for one archived match."""
    root = root or Path(__file__).resolve().parents[1]
    players = manifest.get("players") if isinstance(manifest.get("players"), list) else []

    def is_candidate(player: object) -> bool:
        if not isinstance(player, dict):
            return False
        if player.get("name") == candidate_name:
            return True
        metadata = player.get("result_metadata") if isinstance(player.get("result_metadata"), dict) else {}
        environment = player.get("environment") if isinstance(player.get("environment"), dict) else {}
        module_path = str(environment.get("BWAPI_CONFIG_AI__AI") or "")
        return metadata.get("bot") == candidate_name or (candidate_name.split()[0] == metadata.get("bot")) or bool(candidate_sha and candidate_sha in module_path)

    candidate = next((item for item in players if is_candidate(item)), None)
    opponent_player = next((p for p in players if isinstance(p, dict) and p is not candidate), None)
    opponent_race = _player_race(opponent_player)
    game: dict[str, object] = {
        "manifest_path": str(manifest_path),
        "run_id": manifest.get("run_id"),
        "status": manifest.get("status"),
        "outcome_verified": manifest.get("outcome_verified"),
        "opponent": opponent_player.get("name") if isinstance(opponent_player, dict) else None,
        "opponent_race": opponent_race,
        "map": ((manifest.get("inputs") or {}).get("map") or {}).get("configured_path") if isinstance(manifest.get("inputs"), dict) else None,
    }
    if not isinstance(candidate, dict):
        game["error"] = f"candidate_player_not_found:{candidate_name}"
        game["integrity"] = {"grade": "invalid", "reasons": [game["error"]]}
        return game
    diagnostic_metadata = candidate.get("result_metadata") if isinstance(candidate.get("result_metadata"), dict) else {}
    candidate_player = candidate.get("player")
    replay_records = [r for r in manifest.get("replays", []) if isinstance(r, dict)]
    candidate_replay = next((r for r in replay_records if r.get("player") == candidate_player), None)
    diagnostic = _diagnostic_summary(diagnostic_metadata, root, opponent_race)
    game.update({
        "candidate_player": candidate_player,
        "candidate_result_metadata": diagnostic_metadata,
        "candidate_outcome": "win" if diagnostic_metadata.get("winner") is True else "loss" if diagnostic_metadata.get("winner") is False else "unknown",
        "terminal_frames": diagnostic_metadata.get("frame_count"),
        "elapsed_seconds": manifest.get("elapsed_seconds"),
        "durable_completion_seconds": manifest.get("durable_completion_seconds"),
        "durable_fps": manifest.get("durable_logical_frames_per_wall_second"),
        "short_game": isinstance(manifest.get("elapsed_seconds"), (int, float)) and manifest["elapsed_seconds"] <= 300,
        "diagnostic": diagnostic,
        "emergency_bridge": diagnostic["emergency_bridge"],
        "outcome_performance": outcome_performance(diagnostic_metadata),
    })
    parsed_replays: list[dict[str, object]] = []
    for replay in replay_records:
        replay_path = _resolve_path(replay.get("path"), root)
        parsed = parse_replay(replay_path, screp) if replay_path else {"exists": False, "sha256": None, "screp_exit_code": None, "json_valid": False}
        parsed["manifest_sha256"] = replay.get("sha256")
        parsed["manifest_size_bytes"] = replay.get("size_bytes")
        parsed["manifest_hash_matches"] = parsed.get("sha256") == replay.get("sha256") if replay.get("sha256") else False
        parsed["manifest_size_matches"] = parsed.get("size_bytes") == replay.get("size_bytes") if replay.get("size_bytes") is not None else False
        parsed["player"] = replay.get("player")
        parsed_replays.append(parsed)
    candidate_parsed = next((p for p in parsed_replays if p.get("player") == candidate_player), None)
    if candidate_replay is not None and candidate_parsed is not None:
        game["replay"] = candidate_parsed
        game["replay_fidelity"] = _replay_fidelity(candidate_parsed, candidate_replay, diagnostic)
        # Preserve the old command-derived fields at the game level.
        for key in ("heuristic_grade", "heuristic_score", "signals", "first_frames", "attack_orders", "harvest_orders", "build_units", "production_units"):
            if key in candidate_parsed:
                game[key] = candidate_parsed[key]
    else:
        game["error"] = "candidate_replay_missing"
        game["replay_fidelity"] = {"exists": False, "hash_matches": False, "screp_parse_ok": False, "parse_errors_ok": False}
    game["replays"] = [{
        "player": replay.get("player"),
        "path": parsed.get("path"),
        "fidelity": _replay_fidelity(parsed, replay, diagnostic if replay.get("player") == candidate_player else {}),
    } for replay, parsed in zip(replay_records, parsed_replays)]
    integrity_reasons: list[str] = []
    if manifest.get("status") != "completed": integrity_reasons.append("manifest_not_completed")
    if manifest.get("outcome_verified") is not True: integrity_reasons.append("outcome_not_verified")
    if candidate.get("return_code") not in (None, 0): integrity_reasons.append("candidate_return_code")
    if diagnostic.get("metadata_exists") is False: integrity_reasons.append("diagnostic_missing")
    if diagnostic.get("metadata_exists") and diagnostic.get("metadata_file_parse_ok") is not True: integrity_reasons.append("diagnostic_parse")
    if diagnostic.get("metadata_file_mismatches"): integrity_reasons.append("diagnostic_mismatch")
    if (diagnostic.get("emergency_bridge") or {}).get("review_flags"): integrity_reasons.append("emergency_mechanism_review")
    if not candidate_parsed: integrity_reasons.append("candidate_replay_missing")
    if candidate_parsed and not candidate_parsed.get("manifest_hash_matches"): integrity_reasons.append("candidate_replay_hash")
    if any(not item["fidelity"].get("hash_matches") for item in game["replays"]): integrity_reasons.append("replay_hash")
    if any(not item["fidelity"].get("screp_parse_ok") or not item["fidelity"].get("parse_errors_ok") for item in game["replays"]): integrity_reasons.append("replay_parse")
    game["integrity"] = {
        "grade": "valid" if not integrity_reasons else "review",
        "reasons": sorted(set(integrity_reasons)),
        "all_replays_hash_match": bool(game["replays"]) and all(item["fidelity"].get("hash_matches") for item in game["replays"]),
        "all_replays_parse_ok": bool(game["replays"]) and all(item["fidelity"].get("screp_parse_ok") and item["fidelity"].get("parse_errors_ok") for item in game["replays"]),
    }
    defense = diagnostic["defense"]
    threat = defense.get("first_home_army_threat_frame")
    if not isinstance(threat, int) or threat < 0:
        threat = defense.get("first_home_threat_frame")
    loss = defense.get("first_home_combat_loss_frame")
    game["survival"] = {
        "terminal_frames": diagnostic.get("frame_count"),
        "replay_frames": (game.get("replay") or {}).get("frames"),
        "durable_fps": game.get("durable_fps"),
        "throughput_at_least_384_fps": isinstance(game.get("durable_fps"), (int, float)) and game["durable_fps"] >= 384,
        "first_threat_frame": threat,
        "first_army_threat_frame": defense.get("first_home_army_threat_frame"),
        "first_home_combat_loss_frame": loss,
        "threat_to_loss_frames": loss - threat if isinstance(threat, int) and isinstance(loss, int) and threat >= 0 and loss >= 0 else None,
        "survived_opening_window": isinstance(diagnostic.get("frame_count"), int) and diagnostic["frame_count"] >= 9000,
    }
    game["defense"] = defense
    game["reserve_offense"] = diagnostic["reserve_offense"]
    return game


def parse_replay(path: Path, screp: Path) -> dict[str, object]:
    result: dict[str, object] = {
        "path": str(path),
        "sha256": sha256(path) if path.is_file() else None,
        "size_bytes": path.stat().st_size if path.is_file() else None,
        "exists": path.is_file(),
        "json_valid": False,
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
    result["json_valid"] = isinstance(parsed, dict)
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
        manifest_path = _resolve_path(record.get("match_manifest"), root) if isinstance(record, dict) else None
        game = {"index": record.get("index") if isinstance(record, dict) else None,
                "record": record,
                "manifest_path": str(manifest_path) if manifest_path else None}
        if not manifest_path or not manifest_path.is_file():
            game["error"] = "missing_match_manifest"
            game["integrity"] = {"grade": "invalid", "reasons": ["missing_match_manifest"]}
            games.append(game)
            continue
        try:
            manifest = json.loads(manifest_path.read_text())
        except (OSError, json.JSONDecodeError) as error:
            game["error"] = f"invalid_match_manifest:{type(error).__name__}"
            game["integrity"] = {"grade": "invalid", "reasons": [game["error"]]}
            games.append(game)
            continue
        game.update(score_kestrel_match(manifest, manifest_path, screp, candidate_name, candidate_sha, root))
        games.append(game)
    valid = [g for g in games if isinstance(g.get("replay"), dict) and g["replay"].get("exists")]
    aggregate = {"games": len(games), "scored_replays": len(valid),
                 "grades": {grade: sum(g["replay"].get("heuristic_grade") == grade for g in valid)
                            for grade in ("strong", "partial", "weak", "missing")},
                 "candidate_outcomes": {outcome: sum(g.get("candidate_outcome") == outcome for g in games)
                                        for outcome in ("win", "loss", "unknown")},
                 "outcome_performance_grades": {grade: sum((g.get("outcome_performance") or {}).get("grade") == grade for g in games)
                                                 for grade in ("win", "competitive_loss", "partial_loss", "early_loss", "unverified")},
                 "integrity_grades": {grade: sum((g.get("integrity") or {}).get("grade") == grade for g in games)
                                      for grade in ("valid", "review", "invalid")},
                 "short_games": sum(g.get("short_game") is True for g in games),
                 "signals": {name: sum(g["replay"].get("signals", {}).get(name, False) for g in valid)
                             for name in ("economy", "construction", "production", "combat")},
                 "replay_hash_matches": sum((g.get("integrity") or {}).get("all_replays_hash_match") is True for g in games),
                 "replay_parse_complete": sum((g.get("integrity") or {}).get("all_replays_parse_ok") is True for g in games),
                 "throughput_at_least_384_fps": sum((g.get("survival") or {}).get("throughput_at_least_384_fps") is True for g in games),
                 "command_rejection_free": sum((g.get("diagnostic") or {}).get("rejected_commands") == 0 for g in games),
                 "actual_threat_observed": sum(isinstance((g.get("survival") or {}).get("first_army_threat_frame"), int) and (g.get("survival") or {}).get("first_army_threat_frame") >= 0 for g in games)}
    bridge_games = [g.get("emergency_bridge") for g in games if isinstance(g.get("emergency_bridge"), dict)]
    bridge_review_flags: dict[str, int] = {}
    bridge_opportunity_notes: dict[str, int] = {}
    bridge_reason_counts = {"threat_clear": 0, "army_two": 0, "unknown": 0}
    for bridge in bridge_games:
        for flag in bridge.get("review_flags", []):
            bridge_review_flags[flag] = bridge_review_flags.get(flag, 0) + 1
        for note in bridge.get("opportunity_notes", []):
            bridge_opportunity_notes[note] = bridge_opportunity_notes.get(note, 0) + 1
        for reason, count in (bridge.get("releases") or {}).get("reason_counts", {}).items():
            if reason in bridge_reason_counts and isinstance(count, int):
                bridge_reason_counts[reason] += count
    aggregate["emergency_bridge"] = {
        "games": len(bridge_games),
        "observed": sum((bridge.get("assignments") or {}).get("total", 0) > 0 for bridge in bridge_games),
        "grades": {grade: sum((bridge.get("quantitative_grade") or {}).get("grade") == grade for bridge in bridge_games)
                   for grade in ("pass", "partial", "untested", "review")},
        "score_sum": sum((bridge.get("quantitative_grade") or {}).get("score", 0) for bridge in bridge_games),
        "max_score_sum": sum((bridge.get("quantitative_grade") or {}).get("max_score", 0) for bridge in bridge_games),
        "assignments": sum((bridge.get("assignments") or {}).get("total", 0) for bridge in bridge_games),
        "assignment_batches": sum((bridge.get("assignments") or {}).get("batches", 0) for bridge in bridge_games),
        "accepted_attack_orders": sum((bridge.get("assignments") or {}).get("accepted_attack_orders", 0) for bridge in bridge_games),
        "release_defenders": sum((bridge.get("releases") or {}).get("total_defenders", 0) for bridge in bridge_games),
        "release_reason_events": bridge_reason_counts,
        "recovery": {status: sum((bridge.get("recovery") or {}).get("status") == status for bridge in bridge_games)
                     for status in ("observed", "unobserved", "untested")},
        "non_zerg_sentinel_passes": sum((bridge.get("checks") or {}).get("non_zerg_sentinels") is True for bridge in bridge_games),
        "opportunity_notes": dict(sorted(bridge_opportunity_notes.items())),
        "review_flags": dict(sorted(bridge_review_flags.items())),
    }
    output = Path(args.output).resolve() if args.output else experiment_dir / "hillclimb-scorecard.json"
    scorecard = {"schema_version": 1, "experiment_id": args.experiment_id,
                 "candidate_name": candidate_name, "ledger_path": str(ledger_path),
                 "ledger_sha256": sha256(ledger_path), "schedule_path": str(schedule_path) if schedule_path.is_file() else None,
                 "screp": str(screp), "measurement_scope": "One Kestrel diagnostic plus every replay copy archived for each game.",
                 "aggregate": aggregate, "games": games,
                 "decision_note": "Exploratory hill-climb scorecard only; do not use as Elo, a promotion gate, or tournament evidence."}
    atomic_json(output, scorecard)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
