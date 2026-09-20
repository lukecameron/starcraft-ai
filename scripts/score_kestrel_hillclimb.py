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
import re
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


def _metadata_bool(metadata: dict[str, object], name: str, default: bool) -> bool:
    value = metadata.get(name)
    return value if isinstance(value, bool) else default


def _normalise_race(race: object) -> str | None:
    if not isinstance(race, str):
        return None
    value = race.strip().lower()
    return value if value in {"zerg", "terran", "protoss", "random"} else None


def _candidate_generation(candidate_name: object) -> str | None:
    """Resolve a policy generation from the schedule's candidate display name."""
    if not isinstance(candidate_name, str):
        return None
    match = re.search(r"(?:^|[^a-z0-9])v(43|42|41|40|38|37|36)(?:[^a-z0-9]|$)", candidate_name.lower())
    return f"v{match.group(1)}" if match else None


def _diagnostic_generation(metadata: dict[str, object], candidate_name: object = None) -> str:
    """Identify the Kestrel telemetry generation from the candidate and fields.

    v36 intentionally keeps the v35 construction and emergency episode fields,
    so the candidate name supplies the policy-generation disambiguation while
    field-based detection remains the fallback for archived diagnostics.
    """
    candidate_generation = _candidate_generation(candidate_name)
    if candidate_generation in {"v36", "v37", "v38", "v40", "v41", "v42", "v43"}:
        return candidate_generation
    if any(name in metadata for name in (
        "zerg_second_zealot_probe_reserve_active_frames",
        "second_zealot_train_frame",
        "zerg_second_zealot_probe_reserve_block_count",
    )):
        return "v43"
    if any(name in metadata for name in (
        "zerg_five_probe_policy_active_frames",
        "zerg_five_probe_pylon_accepted_frame",
        "zerg_five_probe_pylon_accepted",
    )):
        return "v42"
    if "zerg_pre_pylon_probe_reserve_frames" in metadata:
        return "v41"
    if any(name.startswith("gateway_probe_") for name in metadata):
        return "v40"
    if any(name in metadata for name in (
        "shared_target_selections", "shared_target_frames", "shared_target_ids",
    )):
        return "v38"
    if any(name in metadata for name in (
        "range_upgrade_eligibility_frame", "seventh_pylon_accepted_frame",
        "fifth_gateway_accepted_frame", "max_pylon_cap",
        "max_post_core_gateway_cap",
    )):
        return "v37"
    if any(name in metadata for name in (
        "accepted_build_pre_command_counts",
        "emergency_episode_ids",
        "emergency_assignment_episode_ids",
    )):
        return "v35"
    if any(name in metadata for name in (
        "emergency_army_three_release_events",
        "emergency_release_army_three_flags",
        "zerg_offense_stage_state_frames",
    )):
        return "v34"
    if any(name in metadata for name in (
        "emergency_army_two_release_events",
        "emergency_release_army_two_flags",
    )):
        return "v33"
    return "legacy"


def _construction_pending_summary(metadata: dict[str, object], opponent_race: str | None = None,
                                  generation: str | None = None) -> dict[str, object]:
    """Validate v35's pre-command construction bookkeeping observations.

    v35 deliberately records the accepted-build arrays rather than exposing
    evaluator state.  The current/current-completed milestone fields are the
    public self-state observations used to check that an accepted request was
    eventually reflected by the engine.  Older diagnostics have no arrays and
    remain ``legacy_absent``.
    """
    generation = generation or _diagnostic_generation(metadata)
    names = (
        "accepted_build_frames",
        "accepted_build_type_ids",
        "accepted_build_pre_command_counts",
        "accepted_build_post_command_counts",
    )
    feature_present = any(name in metadata for name in names)
    if not feature_present:
        return {
            "generation": "legacy",
            "telemetry_status": "legacy_absent",
            "fields_present": [],
            "missing_fields": [],
            "invalid_fields": [],
            "accepted_builds": {"rows": [], "frames": [], "type_ids": [],
                                 "pre_command_counts": [], "post_command_counts": []},
            "timing": {},
            "checks": {"trace_aligned": True, "baseline_values": True,
                        "milestone_order": True, "gateway_sequence_observed": None},
            "quantitative_grade": {"score": 0, "max_score": 100, "grade": "legacy_absent"},
            "review_flags": [],
            "opportunity_notes": [],
            "note": "v35 construction telemetry is absent from this archived candidate.",
        }

    present = [name for name in names if name in metadata]
    missing = [name for name in names if name not in metadata]
    arrays = {name: _metadata_list(metadata, name) for name in names}
    invalid_fields = [name for name in names if name in metadata and not isinstance(metadata[name], list)]
    review_flags: list[str] = []
    if invalid_fields:
        review_flags.append("construction_trace_type_mismatch")
    lengths = {name: len(value) for name, value in arrays.items()}
    if len(set(lengths.values())) > 1:
        review_flags.append("construction_trace_length_mismatch")

    row_count = min(lengths.values(), default=0)
    rows: list[dict[str, object]] = []
    for index in range(row_count):
        row = {
            "index": index,
            "accepted_frame": arrays["accepted_build_frames"][index],
            "type_id": arrays["accepted_build_type_ids"][index],
            "pre_command_count": arrays["accepted_build_pre_command_counts"][index],
            "post_command_count": arrays["accepted_build_post_command_counts"][index],
        }
        rows.append(row)
        for key in ("accepted_frame", "type_id", "pre_command_count", "post_command_count"):
            if not isinstance(row[key], int) or isinstance(row[key], bool):
                review_flags.append("construction_trace_value_type_mismatch")
        for key in ("accepted_frame", "type_id", "pre_command_count", "post_command_count"):
            if isinstance(row[key], int) and row[key] < 0:
                review_flags.append("construction_trace_negative_value")
        if (isinstance(row["pre_command_count"], int) and isinstance(row["post_command_count"], int)
                and row["post_command_count"] < row["pre_command_count"]):
            review_flags.append("post_command_count_below_baseline")
        if (isinstance(row["pre_command_count"], int) and isinstance(row["post_command_count"], int)
                and row["post_command_count"] > row["pre_command_count"] + 1):
            review_flags.append("post_command_count_jump")

    frames = arrays["accepted_build_frames"]
    if any(isinstance(previous, int) and isinstance(current, int) and current < previous
           for previous, current in zip(frames, frames[1:])):
        review_flags.append("accepted_build_frames_not_ordered")

    timing_names = (
        "first_pylon_accepted_frame", "first_pylon_current_frame", "first_pylon_completed_frame",
        "sixth_pylon_accepted_frame", "sixth_pylon_current_frame", "sixth_pylon_completed_frame",
        "first_gateway_accepted_frame", "first_gateway_current_frame", "first_gateway_completed_frame",
        "second_gateway_current_frame", "second_gateway_completed_frame",
        "first_zealot_train_frame", "first_zealot_completed_frame",
    )
    timing = {name: _metadata_int(metadata, name, -1) for name in timing_names}
    milestone_groups = (
        ("first_pylon", ("first_pylon_accepted_frame", "first_pylon_current_frame", "first_pylon_completed_frame")),
        ("sixth_pylon", ("sixth_pylon_accepted_frame", "sixth_pylon_current_frame", "sixth_pylon_completed_frame")),
        ("first_gateway", ("first_gateway_accepted_frame", "first_gateway_current_frame", "first_gateway_completed_frame")),
        ("second_gateway", ("second_gateway_current_frame", "second_gateway_completed_frame")),
        ("first_zealot", ("first_zealot_train_frame", "first_zealot_completed_frame")),
    )
    for label, group in milestone_groups:
        group_values = [timing[name] for name in group]
        if any(value < 0 for value in group_values):
            # A later milestone is not allowed to exist without its earlier
            # public observation, but an unobserved suffix is valid for a
            # game that ended before construction completed.
            first_missing = next((index for index, value in enumerate(group_values) if value < 0), None)
            if first_missing is not None and any(value >= 0 for value in group_values[first_missing + 1:]):
                review_flags.append(f"{label}_milestone_gap")
        for previous, current in zip(group_values, group_values[1:]):
            if previous >= 0 and current >= 0 and current < previous:
                review_flags.append(f"{label}_milestone_order")

    gateway_rows = [row for row in rows if row.get("type_id") == 160]
    gateway_accepted_frames = [row["accepted_frame"] for row in gateway_rows]
    second_gateway_accepted_frame = gateway_accepted_frames[1] if len(gateway_accepted_frames) >= 2 else -1
    if timing["first_gateway_accepted_frame"] >= 0 and (
            not gateway_accepted_frames or gateway_accepted_frames[0] != timing["first_gateway_accepted_frame"]):
        review_flags.append("first_gateway_acceptance_trace_mismatch")
    if timing["second_gateway_current_frame"] >= 0:
        if second_gateway_accepted_frame < 0:
            review_flags.append("second_gateway_acceptance_missing")
        elif second_gateway_accepted_frame > timing["second_gateway_current_frame"]:
            review_flags.append("second_gateway_acceptance_after_current")
    gateway_sequence_observed = (
        second_gateway_accepted_frame >= 0
        and timing["second_gateway_current_frame"] >= second_gateway_accepted_frame
    )
    checks = {
        "trace_aligned": not any(flag.startswith("construction_trace") for flag in review_flags),
        "baseline_values": not any(flag in {"post_command_count_below_baseline", "post_command_count_jump",
                                             "accepted_build_frames_not_ordered"}
                                    or flag.startswith("construction_trace_negative") for flag in review_flags),
        "milestone_order": not any(flag.endswith("milestone_order") or flag.endswith("milestone_gap") for flag in review_flags),
        "gateway_sequence_observed": gateway_sequence_observed if gateway_rows else None,
    }
    if missing:
        review_flags.append("construction_required_fields_missing")
    if not review_flags:
        grade = "pass" if rows else "untested"
    else:
        grade = "review"
    score_checks = [value for value in checks.values() if isinstance(value, bool)]
    return {
        "generation": generation if generation in {"v35", "v36", "v37", "v38", "v40", "v41", "v42", "v43"} else "v35",
        "telemetry_status": "complete" if not missing and not invalid_fields else "partial",
        "fields_present": present,
        "missing_fields": missing,
        "invalid_fields": invalid_fields,
        "accepted_builds": {
            "rows": rows,
            "frames": arrays["accepted_build_frames"],
            "type_ids": arrays["accepted_build_type_ids"],
            "pre_command_counts": arrays["accepted_build_pre_command_counts"],
            "post_command_counts": arrays["accepted_build_post_command_counts"],
            "gateway_accepted_frames": gateway_accepted_frames,
            "second_gateway_accepted_frame": second_gateway_accepted_frame,
        },
        "timing": timing,
        "checks": checks,
        "quantitative_grade": {
            "score": round(100 * sum(score_checks) / len(score_checks)) if score_checks else 0,
            "max_score": 100,
            "grade": grade,
        },
        "review_flags": sorted(set(review_flags)),
        "opportunity_notes": [] if rows else ["construction_acceptance_unobserved"],
        "note": "v35 accepted-build arrays record public pre/post count observations; current/completed timing fields are the public release evidence.",
    }


def _v42_treatment_summary(metadata: dict[str, object], opponent_race: str | None = None) -> dict[str, object]:
    """Validate v42's bounded five-Probe opening treatment telemetry."""
    names = (
        "zerg_five_probe_policy_active_frames",
        "zerg_five_probe_pylon_accepted",
        "zerg_five_probe_pylon_accepted_frame",
    )
    present = [name for name in names if name in metadata]
    missing = [name for name in names if name not in metadata]
    invalid: list[str] = []
    flags: list[str] = []
    active = metadata.get(names[0])
    accepted = metadata.get(names[1])
    accepted_frame = metadata.get(names[2])
    if names[0] in metadata and (not isinstance(active, int) or isinstance(active, bool)):
        invalid.append(names[0])
        flags.append("zerg_five_probe_policy_active_frames_type_mismatch")
    if names[1] in metadata and not isinstance(accepted, bool):
        invalid.append(names[1])
        flags.append("zerg_five_probe_pylon_accepted_type_mismatch")
    if names[2] in metadata and (not isinstance(accepted_frame, int) or isinstance(accepted_frame, bool)):
        invalid.append(names[2])
        flags.append("zerg_five_probe_pylon_accepted_frame_type_mismatch")
    flags.extend(f"{name}_missing" for name in missing)
    race = _normalise_race(opponent_race)
    if race is None:
        known_zerg = metadata.get("known_zerg")
        if isinstance(known_zerg, bool):
            race = "zerg" if known_zerg else "non-zerg"
    first_pylon = metadata.get("first_pylon_accepted_frame")
    first_pylon_valid = isinstance(first_pylon, int) and not isinstance(first_pylon, bool)
    if race == "zerg":
        if isinstance(active, int) and not isinstance(active, bool) and active <= 0:
            flags.append("zerg_five_probe_policy_active_frames_not_positive")
        if accepted is not True:
            flags.append("zerg_five_probe_pylon_accepted_not_true")
        if isinstance(accepted_frame, int) and not isinstance(accepted_frame, bool):
            if accepted_frame < 0:
                flags.append("zerg_five_probe_pylon_accepted_frame_negative")
            elif first_pylon_valid and accepted_frame != first_pylon:
                flags.append("zerg_five_probe_pylon_accepted_frame_mismatch")
    elif race in {"terran", "protoss", "random", "non-zerg"}:
        if active != 0:
            flags.append("non_zerg_five_probe_policy_active_frames_nonzero")
        if accepted is not False:
            flags.append("non_zerg_five_probe_pylon_accepted_not_false")
        if accepted_frame != -1:
            flags.append("non_zerg_five_probe_pylon_accepted_frame_not_minus_one")
    else:
        flags.append("zerg_five_probe_treatment_race_unknown")
    checks = {
        "active_frames_positive": race != "zerg" or (isinstance(active, int) and not isinstance(active, bool) and active > 0),
        "pylon_accepted_true_for_zerg": race != "zerg" or accepted is True,
        "accepted_frame_nonnegative_for_zerg": race != "zerg" or (isinstance(accepted_frame, int) and not isinstance(accepted_frame, bool) and accepted_frame >= 0),
        "accepted_frame_matches_first_pylon": race != "zerg" or not first_pylon_valid or accepted_frame == first_pylon,
        "non_zerg_inactive": race not in {"terran", "protoss", "random", "non-zerg"} or (active == 0 and accepted is False and accepted_frame == -1),
    }
    return {
        "generation": "v42",
        "telemetry_status": "complete" if not missing and not invalid else "partial",
        "fields_present": present,
        "missing_fields": missing,
        "invalid_fields": sorted(set(invalid)),
        "active_frames": active if isinstance(active, int) and not isinstance(active, bool) else None,
        "pylon_accepted": accepted if isinstance(accepted, bool) else None,
        "pylon_accepted_frame": accepted_frame if isinstance(accepted_frame, int) and not isinstance(accepted_frame, bool) else None,
        "checks": checks,
        "quantitative_grade": {"score": round(100 * sum(value for value in checks.values()) / len(checks)),
                               "max_score": 100, "grade": "pass" if not flags else "review"},
        "review_flags": sorted(set(flags)),
    }


def _v43_treatment_summary(metadata: dict[str, object], opponent_race: str | None = None) -> dict[str, object]:
    """Validate v43's post-second-Gateway Probe reserve telemetry."""
    names = (
        "second_zealot_train_frame",
        "zerg_second_zealot_probe_reserve_active_frames",
        "zerg_second_zealot_probe_reserve_block_frames",
        "zerg_second_zealot_probe_reserve_block_minerals",
        "zerg_second_zealot_probe_reserve_block_count",
        "zerg_second_zealot_probe_reserve",
    )
    present = [name for name in names if name in metadata]
    missing = [name for name in names if name not in metadata]
    invalid: list[str] = []
    flags: list[str] = []
    second_frame = metadata.get(names[0])
    active = metadata.get(names[1])
    block_frames = metadata.get(names[2])
    block_minerals = metadata.get(names[3])
    block_count = metadata.get(names[4])
    reserve = metadata.get(names[5])
    for name, value in ((names[0], second_frame), (names[1], active), (names[4], block_count), (names[5], reserve)):
        if name in metadata and (not isinstance(value, int) or isinstance(value, bool)):
            invalid.append(name)
            flags.append(f"{name}_type_mismatch")
    if names[2] in metadata and not isinstance(block_frames, list):
        invalid.append(names[2])
        flags.append("zerg_second_zealot_probe_reserve_block_frames_type_mismatch")
    if names[3] in metadata and not isinstance(block_minerals, list):
        invalid.append(names[3])
        flags.append("zerg_second_zealot_probe_reserve_block_minerals_type_mismatch")
    flags.extend(f"{name}_missing" for name in missing)
    race = _normalise_race(opponent_race)
    if race is None:
        known_zerg = metadata.get("known_zerg")
        if isinstance(known_zerg, bool):
            race = "zerg" if known_zerg else "non-zerg"
    frame_values = block_frames if isinstance(block_frames, list) else []
    mineral_values = block_minerals if isinstance(block_minerals, list) else []
    if len(frame_values) != len(mineral_values):
        flags.append("reserve_trace_length_mismatch")
    if isinstance(block_count, int) and not isinstance(block_count, bool) and block_count != len(frame_values):
        flags.append("reserve_block_count_mismatch")
    if any(not isinstance(value, int) or isinstance(value, bool) for value in frame_values):
        flags.append("reserve_block_frame_type_mismatch")
    if any(not isinstance(value, int) or isinstance(value, bool) for value in mineral_values):
        flags.append("reserve_block_mineral_type_mismatch")
    if any(current < previous for previous, current in zip(frame_values, frame_values[1:])
           if isinstance(previous, int) and isinstance(current, int)):
        flags.append("reserve_block_frames_not_ordered")
    if any(isinstance(value, int) and not isinstance(value, bool) and not 50 <= value < 150 for value in mineral_values):
        flags.append("reserve_block_minerals_out_of_range")
    gateway_frame = metadata.get("second_gateway_current_frame")
    accepted_trains = metadata.get("accepted_zealot_trains")
    if race == "zerg":
        if not isinstance(active, int) or isinstance(active, bool) or active <= 0:
            flags.append("zerg_second_zealot_probe_reserve_active_frames_not_positive")
        if not isinstance(second_frame, int) or isinstance(second_frame, bool) or second_frame < 0:
            flags.append("zerg_second_zealot_train_frame_not_observed")
        if not isinstance(accepted_trains, int) or isinstance(accepted_trains, bool) or accepted_trains < 2:
            flags.append("zerg_second_zealot_acceptance_count_below_two")
        if isinstance(gateway_frame, int) and isinstance(second_frame, int) and second_frame < gateway_frame:
            flags.append("second_zealot_train_before_second_gateway")
        if isinstance(gateway_frame, int) and any(isinstance(frame, int) and frame < gateway_frame for frame in frame_values):
            flags.append("reserve_block_before_second_gateway")
        if isinstance(second_frame, int) and any(isinstance(frame, int) and frame >= second_frame for frame in frame_values):
            flags.append("reserve_block_after_second_zealot")
        if reserve != 100:
            flags.append("zerg_second_zealot_probe_reserve_threshold_mismatch")
    elif race in {"terran", "protoss", "random", "non-zerg"}:
        if active != 0:
            flags.append("non_zerg_second_zealot_probe_reserve_active_frames_nonzero")
        if frame_values or mineral_values or block_count != 0:
            flags.append("non_zerg_second_zealot_probe_reserve_activity")
    else:
        flags.append("second_zealot_reserve_race_unknown")
    checks = {
        "reserve_trace_aligned": "reserve_trace_length_mismatch" not in flags,
        "reserve_block_count": "reserve_block_count_mismatch" not in flags,
        "reserve_block_frames_ordered": "reserve_block_frames_not_ordered" not in flags,
        "reserve_block_minerals_in_range": "reserve_block_minerals_out_of_range" not in flags,
        "second_zealot_accepted": race != "zerg" or "zerg_second_zealot_train_frame_not_observed" not in flags,
        "non_zerg_inactive": race not in {"terran", "protoss", "random", "non-zerg"} or not any(
            flag.startswith("non_zerg_second_zealot_probe_reserve") for flag in flags),
    }
    return {
        "generation": "v43",
        "telemetry_status": "complete" if not missing and not invalid else "partial",
        "fields_present": present,
        "missing_fields": missing,
        "invalid_fields": sorted(set(invalid)),
        "second_zealot_train_frame": second_frame if isinstance(second_frame, int) and not isinstance(second_frame, bool) else None,
        "active_frames": active if isinstance(active, int) and not isinstance(active, bool) else None,
        "reserve_block_frames": frame_values,
        "reserve_block_minerals": mineral_values,
        "reserve_block_count": block_count if isinstance(block_count, int) and not isinstance(block_count, bool) else None,
        "reserve": reserve if isinstance(reserve, int) and not isinstance(reserve, bool) else None,
        "checks": checks,
        "quantitative_grade": {"score": round(100 * sum(value for value in checks.values()) / len(checks)),
                               "max_score": 100, "grade": "pass" if not flags else "review"},
        "review_flags": sorted(set(flags)),
    }


def _probe_reserve_summary(metadata: dict[str, object], opponent_race: str | None = None,
                           generation: str | None = None) -> dict[str, object]:
    """Validate v36's known-Zerg Probe reserve window telemetry."""
    generation = generation or _diagnostic_generation(metadata)
    names = (
        "accepted_probe_train_frames", "probe_reserve_block_frames",
        "probe_reserve_block_minerals", "opening_probe_reserve",
        "max_opening_probe_reserve",
        "first_probe_reserve_window_frame", "probe_reserve_window_end_frame",
        "probe_reserve_block_count",
    )
    pre_pylon_name = "zerg_pre_pylon_probe_reserve_frames"
    v42_names = (
        "zerg_five_probe_policy_active_frames",
        "zerg_five_probe_pylon_accepted",
        "zerg_five_probe_pylon_accepted_frame",
    )
    v43_names = (
        "second_zealot_train_frame",
        "zerg_second_zealot_probe_reserve_active_frames",
        "zerg_second_zealot_probe_reserve_block_frames",
        "zerg_second_zealot_probe_reserve_block_minerals",
        "zerg_second_zealot_probe_reserve_block_count",
        "zerg_second_zealot_probe_reserve",
    )
    feature_present = any(name in metadata for name in names) or (
        generation == "v41" and pre_pylon_name in metadata
    ) or (generation == "v42" and any(name in metadata for name in v42_names)) or (
        generation == "v43" and any(name in metadata for name in v43_names)
    )
    if not feature_present:
        if generation in {"v36", "v37", "v38", "v40", "v41", "v42", "v43"}:
            required_names = (names + (pre_pylon_name,) if generation == "v41" else
                              names + v42_names if generation == "v42" else
                              names + v42_names + v43_names if generation == "v43" else names)
            return {
                "generation": generation,
                "telemetry_status": "partial",
                "fields_present": [],
                "missing_fields": list(required_names),
                "invalid_fields": [],
                "accepted_probe_train_frames": [],
                "reserve_blocks": {"frames": [], "minerals": [], "count": 0},
                "window": {"start_frame": -1, "end_frame": -1, "threshold": 250},
                "zerg_pre_pylon_probe_reserve_frames": None,
                "v42_treatment": _v42_treatment_summary(metadata, opponent_race) if generation in {"v42", "v43"} else None,
                "v43_treatment": _v43_treatment_summary(metadata, opponent_race) if generation == "v43" else None,
                "checks": {"trace_aligned": False, "block_count": False, "block_frames_ordered": False,
                            "block_minerals_in_range": False, "window_ordered": False,
                            "probe_train_absence": False, "post_window_resumption": None,
                            "non_zerg_inactive": None, "max_reserve_threshold": False},
                "quantitative_grade": {"score": 0, "max_score": 100, "grade": "review"},
                "review_flags": ["probe_reserve_required_fields_missing"],
                "opportunity_notes": ["reserve_telemetry_missing"],
            }
        return {
            "generation": "legacy",
            "telemetry_status": "legacy_absent",
            "fields_present": [],
            "missing_fields": [],
            "invalid_fields": [],
            "accepted_probe_train_frames": [],
            "reserve_blocks": {"frames": [], "minerals": [], "count": 0},
            "window": {"start_frame": -1, "end_frame": -1, "threshold": 250},
            "checks": {"trace_aligned": True, "block_count": True, "block_frames_ordered": True,
                        "block_minerals_in_range": True, "window_ordered": True,
                        "probe_train_absence": True, "post_window_resumption": None,
                        "non_zerg_inactive": None, "max_reserve_threshold": None},
            "quantitative_grade": {"score": 0, "max_score": 100, "grade": "legacy_absent"},
            "review_flags": [],
            "opportunity_notes": [],
        }

    list_names = ("accepted_probe_train_frames", "probe_reserve_block_frames", "probe_reserve_block_minerals")
    required_names = (names + (pre_pylon_name,) if generation == "v41" else
                      names + v42_names if generation == "v42" else
                      names + v42_names + v43_names if generation == "v43" else names)
    present = [name for name in required_names if name in metadata]
    missing = [name for name in required_names if name not in metadata]
    if pre_pylon_name in metadata and pre_pylon_name not in present:
        present.append(pre_pylon_name)
    arrays = {name: _metadata_list(metadata, name) for name in list_names}
    invalid_fields = [name for name in list_names if name in metadata and not isinstance(metadata[name], list)]
    invalid_scalars = [name for name in names[len(list_names):]
                       if name in metadata and (not isinstance(metadata[name], int) or isinstance(metadata[name], bool))]
    pre_pylon_value = metadata.get(pre_pylon_name)
    pre_pylon_invalid = pre_pylon_name in metadata and (
        not isinstance(pre_pylon_value, int) or isinstance(pre_pylon_value, bool)
    )
    if pre_pylon_invalid:
        invalid_scalars.append(pre_pylon_name)
    review_flags: list[str] = []
    if invalid_fields:
        review_flags.append("probe_reserve_trace_type_mismatch")
    if invalid_scalars:
        review_flags.append("probe_reserve_scalar_type_mismatch")
    if generation == "v41":
        if pre_pylon_name not in metadata:
            review_flags.append("zerg_pre_pylon_probe_reserve_frames_missing")
        elif pre_pylon_invalid:
            review_flags.append("zerg_pre_pylon_probe_reserve_frames_type_mismatch")
    v42_treatment = _v42_treatment_summary(metadata, opponent_race) if generation in {"v42", "v43"} else None
    if v42_treatment is not None:
        prefix = "v42:" if generation == "v42" else "v43:retained_v42:"
        review_flags.extend(f"{prefix}{flag}" for flag in v42_treatment["review_flags"])
    v43_treatment = _v43_treatment_summary(metadata, opponent_race) if generation == "v43" else None
    if v43_treatment is not None:
        review_flags.extend(f"v43:{flag}" for flag in v43_treatment["review_flags"])
    accepted = arrays["accepted_probe_train_frames"]
    block_frames = arrays["probe_reserve_block_frames"]
    block_minerals = arrays["probe_reserve_block_minerals"]
    if len(block_frames) != len(block_minerals):
        review_flags.append("probe_reserve_trace_length_mismatch")
    block_count = _metadata_int(metadata, "probe_reserve_block_count", 0)
    if block_count != len(block_frames):
        review_flags.append("probe_reserve_block_count_mismatch")
    for values, type_flag in ((accepted, "probe_train_frame_type_mismatch"),
                              (block_frames, "probe_reserve_frame_type_mismatch"),
                              (block_minerals, "probe_reserve_mineral_type_mismatch")):
        if any(not isinstance(value, int) or isinstance(value, bool) for value in values):
            review_flags.append(type_flag)
    if any(isinstance(previous, int) and isinstance(current, int) and current < previous
           for previous, current in zip(accepted, accepted[1:])):
        review_flags.append("probe_train_frames_not_ordered")
    if any(isinstance(previous, int) and isinstance(current, int) and current < previous
           for previous, current in zip(block_frames, block_frames[1:])):
        review_flags.append("probe_reserve_block_frames_not_ordered")
    if any(isinstance(value, int) and not 200 <= value < 300 for value in block_minerals):
        review_flags.append("probe_reserve_block_minerals_out_of_range")

    window_start = _metadata_int(metadata, "first_probe_reserve_window_frame", -1)
    window_end = _metadata_int(metadata, "probe_reserve_window_end_frame", -1)
    first_pylon = _metadata_int(metadata, "first_pylon_accepted_frame", -1)
    second_gateway = _metadata_int(metadata, "second_gateway_current_frame", -1)
    race = _normalise_race(opponent_race)
    if race is None:
        known_zerg = metadata.get("known_zerg")
        if isinstance(known_zerg, bool):
            race = "zerg" if known_zerg else "non-zerg"
    expected_inactive = race in {"terran", "protoss", "non-zerg"}
    cadence = max(6, _metadata_int(metadata, "latency_frames", 6))
    if race == "zerg" and first_pylon >= 0:
        if window_start < 0:
            review_flags.append("probe_reserve_window_start_missing")
        elif window_start < first_pylon:
            review_flags.append("probe_reserve_window_before_first_pylon")
        elif window_start > first_pylon + cadence:
            review_flags.append("probe_reserve_window_start_delayed")
    if window_end >= 0 and window_start >= 0 and window_end < window_start:
        review_flags.append("probe_reserve_window_end_before_start")
    if race == "zerg" and second_gateway >= 0:
        if window_end < 0:
            review_flags.append("probe_reserve_window_end_missing")
        elif window_end < second_gateway:
            review_flags.append("probe_reserve_window_end_before_second_gateway")
        elif window_end >= second_gateway + cadence:
            review_flags.append("probe_reserve_window_end_delayed")
    in_opening_window = (first_pylon >= 0 and second_gateway >= 0 and
                         first_pylon <= second_gateway)
    if in_opening_window and any(isinstance(frame, int) and first_pylon <= frame < second_gateway for frame in accepted):
        review_flags.append("probe_train_during_pre_second_gateway_window")
    post_window_train = window_end >= 0 and any(isinstance(frame, int) and frame >= window_end for frame in accepted)
    max_reserve = _metadata_int(metadata, "max_opening_probe_reserve", 0)
    if race == "zerg" and max_reserve != 250:
        review_flags.append("probe_reserve_max_threshold_mismatch")
    if expected_inactive and max_reserve != 0:
        review_flags.append("non_zerg_probe_reserve_max_threshold_mismatch")
    if expected_inactive and (accepted or block_frames or block_minerals or block_count != 0 or
                              _metadata_int(metadata, "opening_probe_reserve", 0) != 0 or
                              window_start != -1 or window_end != -1):
        review_flags.append("non_zerg_probe_reserve_activity")
    if generation == "v41" and not pre_pylon_invalid and pre_pylon_name in metadata:
        if race == "zerg" and pre_pylon_value <= 0:
            review_flags.append("zerg_pre_pylon_probe_reserve_frames_not_positive")
        elif expected_inactive and pre_pylon_value != 0:
            review_flags.append("non_zerg_pre_pylon_probe_reserve_frames_nonzero")
    if missing:
        review_flags.append("probe_reserve_required_fields_missing")
    checks = {
        "trace_aligned": "probe_reserve_trace_length_mismatch" not in review_flags,
        "block_count": "probe_reserve_block_count_mismatch" not in review_flags,
        "block_frames_ordered": "probe_reserve_block_frames_not_ordered" not in review_flags,
        "block_minerals_in_range": "probe_reserve_block_minerals_out_of_range" not in review_flags,
        "window_ordered": not any(flag.startswith("probe_reserve_window") for flag in review_flags),
        "probe_train_absence": "probe_train_during_pre_second_gateway_window" not in review_flags,
        "post_window_resumption": post_window_train if window_end >= 0 else None,
        "max_reserve_threshold": not any(flag.endswith("max_threshold_mismatch") for flag in review_flags),
        "non_zerg_inactive": (not any(flag.startswith("non_zerg_probe_reserve") or
                                       flag.startswith("non_zerg_pre_pylon_probe")
                                       for flag in review_flags)
                              if expected_inactive else None),
    }
    scored_checks = [value for value in checks.values() if isinstance(value, bool)]
    if expected_inactive:
        v42_ok = v42_treatment is None or v42_treatment["quantitative_grade"]["grade"] == "pass"
        v43_ok = v43_treatment is None or v43_treatment["quantitative_grade"]["grade"] == "pass"
        grade = "pass" if checks["non_zerg_inactive"] and v42_ok and v43_ok else "review"
    elif not review_flags:
        grade = "pass" if block_frames else "untested"
    else:
        grade = "review"
    return {
        "generation": generation if generation in {"v36", "v37", "v38", "v40", "v41", "v42", "v43"} else "legacy" if not feature_present else "v36",
        "telemetry_status": "complete" if not missing and not invalid_fields and not invalid_scalars else "partial",
        "fields_present": present,
        "missing_fields": missing,
        "invalid_fields": sorted(set(invalid_fields + invalid_scalars +
                                      (v42_treatment["invalid_fields"] if v42_treatment else []) +
                                      (v43_treatment["invalid_fields"] if v43_treatment else []))),
        "accepted_probe_train_frames": accepted,
        "reserve_blocks": {"frames": block_frames, "minerals": block_minerals, "count": block_count},
        "window": {"start_frame": window_start, "end_frame": window_end, "threshold": 250},
        "zerg_pre_pylon_probe_reserve_frames": pre_pylon_value if pre_pylon_name in metadata else None,
        "v42_treatment": v42_treatment,
        "v43_treatment": v43_treatment,
        "checks": checks,
        "quantitative_grade": {"score": round(100 * sum(scored_checks) / len(scored_checks)) if scored_checks else 0,
                               "max_score": 100, "grade": grade},
        "review_flags": sorted(set(review_flags)),
        "opportunity_notes": [] if block_frames else ["reserve_block_opportunity_unobserved"],
    }


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


def _emergency_episode_summary(metadata: dict[str, object], opponent_race: str | None = None,
                               generation: str | None = None) -> dict[str, object]:
    """Validate v35's cumulative two-Probe emergency threat episodes."""
    generation = generation or _diagnostic_generation(metadata)
    names = (
        "emergency_episode_current_id",
        "emergency_episode_current_assignment_count",
        "emergency_episode_threat_present",
        "emergency_episode_ids",
        "emergency_episode_start_frames",
        "emergency_episode_reset_frames",
        "emergency_episode_assignment_counts",
        "emergency_episode_cap_blocks",
        "emergency_episode_cap_block_frames",
        "emergency_episode_cap_block_counts",
        "emergency_assignment_episode_ids",
    )
    feature_present = any(name in metadata for name in names)
    if not feature_present:
        return {
            "generation": "legacy",
            "telemetry_status": "legacy_absent",
            "fields_present": [],
            "missing_fields": [],
            "invalid_fields": [],
            "assignment_cap": 2,
            "episodes": [],
            "reset_frames": [],
            "assignments": {"episode_ids": [], "batches": []},
            "cap_blocks": {"total": 0, "frames": [], "counts": []},
            "current": {"id": 0, "assignment_count": 0, "threat_present": False},
            "checks": {"episode_trace_aligned": True, "episode_ids_consistent": True,
                        "episode_reset_order": True, "assignment_episode_alignment": True,
                        "per_episode_cap": True, "cap_block_alignment": True,
                        "non_zerg_inactive": None},
            "quantitative_grade": {"score": 0, "max_score": 100, "grade": "legacy_absent"},
            "review_flags": [],
            "opportunity_notes": [],
        }

    present = [name for name in names if name in metadata]
    missing = [name for name in names if name not in metadata]
    list_names = (
        "emergency_episode_ids", "emergency_episode_start_frames", "emergency_episode_reset_frames",
        "emergency_episode_assignment_counts", "emergency_episode_cap_block_frames",
        "emergency_episode_cap_block_counts", "emergency_assignment_episode_ids",
    )
    arrays = {name: _metadata_list(metadata, name) for name in list_names}
    invalid_fields = [name for name in list_names if name in metadata and not isinstance(metadata[name], list)]
    invalid_scalars = [name for name in ("emergency_episode_current_id", "emergency_episode_current_assignment_count",
                                         "emergency_episode_cap_blocks")
                       if name in metadata and (not isinstance(metadata[name], int) or isinstance(metadata[name], bool))]
    if "emergency_episode_threat_present" in metadata and not isinstance(metadata["emergency_episode_threat_present"], bool):
        invalid_scalars.append("emergency_episode_threat_present")
    review_flags: list[str] = []
    if invalid_fields:
        review_flags.append("episode_trace_type_mismatch")
    if invalid_scalars:
        review_flags.append("episode_scalar_type_mismatch")
    current_id = _metadata_int(metadata, "emergency_episode_current_id", 0)
    current_count = _metadata_int(metadata, "emergency_episode_current_assignment_count", 0)
    threat_present = _metadata_bool(metadata, "emergency_episode_threat_present", False)
    cap_blocks = _metadata_int(metadata, "emergency_episode_cap_blocks", 0)
    episode_ids = arrays["emergency_episode_ids"]
    starts = arrays["emergency_episode_start_frames"]
    resets = arrays["emergency_episode_reset_frames"]
    episode_counts = arrays["emergency_episode_assignment_counts"]
    block_frames = arrays["emergency_episode_cap_block_frames"]
    block_counts = arrays["emergency_episode_cap_block_counts"]
    assignment_episode_ids = arrays["emergency_assignment_episode_ids"]
    if not (len(episode_ids) == len(starts) == len(episode_counts)):
        review_flags.append("episode_trace_length_mismatch")
    if len(block_frames) != len(block_counts) or cap_blocks != len(block_frames):
        review_flags.append("episode_cap_block_length_mismatch")

    row_count = min(len(episode_ids), len(starts), len(episode_counts))
    episodes = [{"index": index, "id": episode_ids[index], "start_frame": starts[index],
                 "reset_frame": resets[index] if index < len(resets) else None,
                 "assignment_count": episode_counts[index]} for index in range(row_count)]
    for row in episodes:
        if any(not isinstance(row[key], int) or isinstance(row[key], bool)
               for key in ("id", "start_frame", "assignment_count")):
            review_flags.append("episode_value_type_mismatch")
        if (isinstance(row["id"], int) and row["id"] <= 0) or (isinstance(row["start_frame"], int) and row["start_frame"] < 0) or (isinstance(row["assignment_count"], int) and not 0 <= row["assignment_count"] <= 2):
            review_flags.append("episode_value_out_of_range")
    if episode_ids != list(range(1, len(episode_ids) + 1)):
        review_flags.append("episode_ids_not_sequential")
    if any(isinstance(previous, int) and isinstance(current, int) and current <= previous
           for previous, current in zip(starts, starts[1:])):
        review_flags.append("episode_start_frames_not_ordered")
    expected_reset_count = len(starts) - (1 if threat_present and starts else 0)
    if len(resets) != expected_reset_count:
        review_flags.append("episode_reset_count_mismatch")
    for index, reset in enumerate(resets):
        if not isinstance(reset, int) or isinstance(reset, bool):
            review_flags.append("episode_reset_frame_type_mismatch")
            continue
        start = starts[index] if index < len(starts) else None
        next_start = starts[index + 1] if index + 1 < len(starts) else None
        if not isinstance(start, int) or reset <= start or (isinstance(next_start, int) and reset >= next_start):
            review_flags.append("episode_reset_outside_episode_boundary")
    if any(isinstance(previous, int) and isinstance(current, int) and current <= previous
           for previous, current in zip(resets, resets[1:])):
        review_flags.append("episode_reset_frames_not_ordered")

    base_batches, batch_flags = _emergency_batches(
        _metadata_list(metadata, "emergency_assignment_frames"),
        _metadata_list(metadata, "emergency_assignment_sizes"),
        _metadata_list(metadata, "emergency_assigned_probe_ids"),
    )
    review_flags.extend(f"episode_{flag}" for flag in batch_flags)
    assignment_rows: list[dict[str, object]] = []
    assignment_offset = 0
    for batch in base_batches:
        batch_size = batch["size"] if isinstance(batch["size"], int) else 0
        batch_episode_values = assignment_episode_ids[assignment_offset:assignment_offset + batch_size]
        if len(batch_episode_values) != batch_size:
            review_flags.append("assignment_episode_id_count_mismatch")
        batch_episode = batch_episode_values[0] if batch_episode_values else None
        if batch_episode_values and any(value != batch_episode for value in batch_episode_values):
            review_flags.append("assignment_batch_spans_episodes")
        assignment_rows.append({**batch, "episode_id": batch_episode, "episode_ids": batch_episode_values})
        assignment_offset += batch_size
    if assignment_offset != len(assignment_episode_ids):
        review_flags.append("assignment_episode_id_unconsumed")

    episode_assignment_ids: dict[int, list[object]] = {index: [] for index in range(1, len(episode_ids) + 1)}
    episode_assignment_frames: dict[int, list[object]] = {index: [] for index in episode_assignment_ids}
    for batch in assignment_rows:
        episode_id = batch["episode_id"]
        if not isinstance(episode_id, int) or episode_id not in episode_assignment_ids:
            review_flags.append("assignment_unknown_episode_id")
            continue
        episode_assignment_ids[episode_id].extend(batch["probe_ids"])
        episode_assignment_frames[episode_id].append(batch["frame"])
        start = starts[episode_id - 1] if episode_id - 1 < len(starts) else None
        end = resets[episode_id - 1] if episode_id - 1 < len(resets) else None
        if isinstance(batch["frame"], int) and (not isinstance(start, int) or batch["frame"] < start or (isinstance(end, int) and batch["frame"] >= end)):
            review_flags.append("assignment_frame_outside_episode")
    for episode_id, ids in episode_assignment_ids.items():
        valid_ids = [value for value in ids if isinstance(value, int) and not isinstance(value, bool)]
        if len(valid_ids) != len(ids):
            review_flags.append("episode_assignment_id_type_mismatch")
        if len(valid_ids) != len(set(valid_ids)):
            review_flags.append("episode_assignment_ids_duplicate")
        if len(ids) > 2:
            review_flags.append("episode_assignment_cap_exceeded")
        if episode_id - 1 < len(episode_counts) and episode_counts[episode_id - 1] != len(ids):
            review_flags.append("episode_assignment_count_mismatch")
    for index, frame in enumerate(block_frames):
        count = block_counts[index] if index < len(block_counts) else None
        if not isinstance(frame, int) or not isinstance(count, int) or isinstance(frame, bool) or isinstance(count, bool):
            review_flags.append("episode_cap_block_value_type_mismatch")
            continue
        if count < 2:
            review_flags.append("episode_cap_block_below_cap")
        matching: list[int] = []
        for episode_id in episode_assignment_frames:
            if episode_id - 1 >= len(starts) or not isinstance(starts[episode_id - 1], int):
                continue
            start = starts[episode_id - 1]
            end = resets[episode_id - 1] if episode_id - 1 < len(resets) else None
            if start <= frame and (not isinstance(end, int) or frame < end):
                matching.append(episode_id)
        if not matching:
            review_flags.append("episode_cap_block_outside_episode")
        elif count != len(episode_assignment_ids[matching[-1]]):
            review_flags.append("episode_cap_block_count_mismatch")
    if current_id < 0 or current_id > len(episode_ids) or current_count < 0 or current_count > 2:
        review_flags.append("episode_current_state_out_of_range")
    if threat_present and (current_id == 0 or (episode_counts and current_id != len(episode_counts))):
        review_flags.append("episode_current_id_mismatch")
    if threat_present and episode_counts and current_count != episode_counts[-1]:
        review_flags.append("episode_current_count_mismatch")
    if not threat_present and current_count != 0:
        review_flags.append("episode_current_count_not_reset")
    if missing:
        review_flags.append("episode_required_fields_missing")

    race = _normalise_race(opponent_race)
    if race is None:
        known_zerg = metadata.get("known_zerg")
        if isinstance(known_zerg, bool):
            race = "zerg" if known_zerg else "non-zerg"
    expected_inactive = race in {"terran", "protoss", "non-zerg"}
    if expected_inactive and (episode_ids or starts or resets or episode_counts or block_frames or block_counts or assignment_episode_ids or current_id != 0 or current_count != 0 or threat_present or cap_blocks != 0):
        review_flags.append("non_zerg_episode_activity")
    checks = {
        "episode_trace_aligned": "episode_trace_length_mismatch" not in review_flags and "episode_value_type_mismatch" not in review_flags,
        "episode_ids_consistent": not any(flag.startswith("episode_ids_") or flag == "episode_start_frames_not_ordered" for flag in review_flags),
        "episode_reset_order": not any(flag.startswith("episode_reset_") for flag in review_flags),
        "assignment_episode_alignment": not any(flag.startswith("assignment_") or flag.startswith("episode_assignment_") or flag.startswith("episode_frame") for flag in review_flags),
        "per_episode_cap": not any(flag.startswith("episode_assignment_cap") or flag in {"episode_assignment_ids_duplicate", "episode_assignment_id_type_mismatch", "episode_assignment_count_mismatch"} for flag in review_flags),
        "cap_block_alignment": not any(flag.startswith("episode_cap_block") for flag in review_flags),
        "non_zerg_inactive": expected_inactive and not any(flag.startswith("non_zerg_episode") for flag in review_flags) if expected_inactive else None,
    }
    bool_checks = [value for value in checks.values() if isinstance(value, bool)]
    if expected_inactive:
        grade = "pass" if checks["non_zerg_inactive"] else "review"
    elif not episodes and not review_flags:
        grade = "untested"
    else:
        grade = "pass" if not review_flags else "review"
    return {
        "generation": generation if generation in {"v35", "v36", "v37", "v38", "v40", "v41", "v42", "v43"} else "v35",
        "telemetry_status": "complete" if not missing and not invalid_fields else "partial",
        "fields_present": present,
        "missing_fields": missing,
        "invalid_fields": sorted(set(invalid_fields + invalid_scalars)),
        "assignment_cap": 2,
        "episodes": episodes,
        "reset_frames": resets,
        "assignments": {"episode_ids": assignment_episode_ids, "batches": assignment_rows},
        "cap_blocks": {"total": cap_blocks, "frames": block_frames, "counts": block_counts},
        "current": {"id": current_id, "assignment_count": current_count, "threat_present": threat_present},
        "checks": checks,
        "quantitative_grade": {"score": round(100 * sum(bool_checks) / len(bool_checks)) if bool_checks else 0,
                               "max_score": 100, "grade": grade},
        "review_flags": sorted(set(review_flags)),
        "opportunity_notes": [] if episodes else ["threat_episode_unobserved"],
        "note": "v35 episode telemetry is public-threat state; the registered cumulative assignment cap is two unique Probes per episode.",
    }


def _aggregate_emergency_episode_summaries(episode_games: list[dict[str, object]]) -> dict[str, object]:
    """Aggregate v35 episode summaries while preserving list-shaped traces."""
    review_flags: dict[str, int] = {}
    aggregate = {
        "games": len(episode_games),
        "observed": sum(bool(item.get("episodes")) for item in episode_games),
        "grades": {grade: sum((item.get("quantitative_grade") or {}).get("grade") == grade for item in episode_games)
                   for grade in ("pass", "untested", "review")},
        "episode_count": sum(len(item.get("episodes", [])) for item in episode_games),
        "assignments": sum(len((item.get("assignments") or {}).get("episode_ids", []))
                            for item in episode_games),
        "cap_blocks": sum((item.get("cap_blocks") or {}).get("total", 0) for item in episode_games),
        "review_flags": review_flags,
    }
    for item in episode_games:
        for flag in item.get("review_flags", []):
            review_flags[flag] = review_flags.get(flag, 0) + 1
    aggregate["review_flags"] = dict(sorted(review_flags.items()))
    return aggregate


def _emergency_bridge_summary(metadata: dict[str, object], opponent_race: str | None = None,
                              generation: str | None = None) -> dict[str, object]:
    """Normalize v33/v34 emergency-worker telemetry and legacy absence."""
    generation = generation or _diagnostic_generation(metadata)
    army_generation = "three" if generation in {"v34", "v35", "v36", "v37", "v38", "v40", "v41", "v42", "v43"} else "two"
    army_event_key = f"emergency_army_{army_generation}_release_events"
    army_defender_key = f"emergency_army_{army_generation}_released_defenders"
    first_army_frame_key = f"emergency_first_army_{army_generation}_release_frame"
    army_flag_key = f"emergency_release_army_{army_generation}_flags"
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
        "emergency_defender_deaths": 0,
        "emergency_build_selection_exclusions": 0,
        "emergency_economy_exclusions": 0,
        "emergency_post_release_gather_orders": 0,
        "emergency_post_release_build_orders": 0,
        "emergency_army_at_trigger": -1,
        "emergency_local_combat_at_trigger": -1,
    }
    scalar_defaults[army_event_key] = 0
    scalar_defaults[army_defender_key] = 0
    scalar_defaults[first_army_frame_key] = -1
    required = tuple(scalar_defaults) + (
        "emergency_assigned_probe_ids", "emergency_assignment_frames", "emergency_assignment_sizes",
        "emergency_release_frames", "emergency_release_sizes", army_flag_key,
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
    release_flags = _metadata_list(metadata, army_flag_key)
    assignment_batches, trace_flags = _emergency_batches(assignment_frames, assignment_sizes, assigned_ids)

    release_trace_flags: list[str] = []
    if not (len(release_frames) == len(release_sizes) == len(release_flags)):
        release_trace_flags.append("release_trace_length_mismatch")
    release_trace: list[dict[str, object]] = []
    for index in range(min(len(release_frames), len(release_sizes), len(release_flags))):
        flag = release_flags[index]
        reason = f"army_{army_generation}" if flag == 1 else "threat_clear" if flag == 0 else "unknown"
        if flag not in (0, 1):
            release_trace_flags.append("release_trace_invalid_reason")
        release_trace.append({"index": index, "frame": release_frames[index], "size": release_sizes[index],
                              f"army_{army_generation}": flag, "reason": reason})

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
        f"army_{army_generation}": sum(item["reason"] == f"army_{army_generation}" for item in release_trace),
        "unknown": sum(item["reason"] == "unknown" for item in release_trace),
    }
    if release_trace and values["emergency_releases"] != sum(
        size for size in release_sizes if isinstance(size, int) and not isinstance(size, bool)
    ):
        review_flags.append("release_defender_total_mismatch")
    if trace_reason_counts["threat_clear"] != values["emergency_threat_clear_release_events"]:
        review_flags.append("threat_clear_release_event_mismatch")
    if trace_reason_counts[f"army_{army_generation}"] != values[army_event_key]:
        review_flags.append(f"army_{army_generation}_release_event_mismatch")
    threat_clear_sizes = sum(
        size for size, item in zip(release_sizes, release_trace)
        if item["reason"] == "threat_clear" and isinstance(size, int) and not isinstance(size, bool)
    )
    army_release_sizes = sum(
        size for size, item in zip(release_sizes, release_trace)
        if item["reason"] == f"army_{army_generation}" and isinstance(size, int) and not isinstance(size, bool)
    )
    if threat_clear_sizes != values["emergency_threat_clear_released_defenders"]:
        review_flags.append("threat_clear_release_defender_mismatch")
    if army_release_sizes != values[army_defender_key]:
        review_flags.append(f"army_{army_generation}_release_defender_mismatch")
    if release_trace and values["emergency_first_release_frame"] != release_trace[0]["frame"]:
        review_flags.append("first_release_frame_mismatch")
    first_threat_clear = next((item["frame"] for item in release_trace if item["reason"] == "threat_clear"), None)
    first_army_release = next((item["frame"] for item in release_trace if item["reason"] == f"army_{army_generation}"), None)
    if first_threat_clear is not None and values["emergency_first_threat_clear_release_frame"] != first_threat_clear:
        review_flags.append("first_threat_clear_frame_mismatch")
    if first_army_release is not None and values[first_army_frame_key] != first_army_release:
        review_flags.append(f"first_army_{army_generation}_frame_mismatch")
    if values["emergency_releases"] > 0 and not release_trace:
        review_flags.append("release_total_without_release_trace")
    if values["emergency_threat_clear_release_events"] + values[army_event_key] > 0 and not release_trace:
        review_flags.append("release_reason_without_release_trace")

    episode_summary = _emergency_episode_summary(metadata, opponent_race, generation) if generation in {"v35", "v36", "v37", "v38", "v40", "v41", "v42", "v43"} else None
    if episode_summary is not None:
        review_flags.extend(f"episode:{flag}" for flag in episode_summary.get("review_flags", []))

    if expected_inactive:
        inactive_values = [values[name] for name in scalar_defaults if name not in {
            "emergency_trigger_frame",
            "emergency_first_assignment_frame", "emergency_first_release_frame",
            "emergency_first_threat_clear_release_frame", first_army_frame_key,
            "emergency_army_at_trigger", "emergency_local_combat_at_trigger",
        }]
        if any(value != 0 for value in inactive_values):
            review_flags.append("non_zerg_emergency_activity")
        if any(values[name] != -1 for name in (
            "emergency_first_assignment_frame", "emergency_first_release_frame",
            "emergency_first_threat_clear_release_frame", first_army_frame_key,
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
        "release_trace_consistent": not any(flag.startswith("release_") or flag.startswith("threat_clear_release") or flag.startswith(f"army_{army_generation}_release") for flag in review_flags),
        "non_zerg_sentinels": expected_inactive and not any(flag.startswith("non_zerg_") for flag in review_flags) if expected_inactive else None,
        "recovery": recovery_status,
        "episode_state_consistent": (not episode_summary.get("review_flags")) if episode_summary is not None else None,
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
        "generation": generation,
        "release_threshold": 3 if army_generation == "three" else 2,
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
            "threshold": 3 if army_generation == "three" else 2,
            "total_defenders": releases,
            "first_frame": values["emergency_first_release_frame"],
            "threat_clear_events": values["emergency_threat_clear_release_events"],
            "threat_clear_defenders": values["emergency_threat_clear_released_defenders"],
            "first_threat_clear_frame": values["emergency_first_threat_clear_release_frame"],
            f"army_{army_generation}_events": values[army_event_key],
            f"army_{army_generation}_defenders": values[army_defender_key],
            f"first_army_{army_generation}_frame": values[first_army_frame_key],
            # Keep the v33 names available to callers that consume a stable
            # scorecard shape while exposing the v34 vocabulary above.
            "army_two_events": values["emergency_army_two_release_events"] if army_generation == "two" else 0,
            "army_two_defenders": values["emergency_army_two_released_defenders"] if army_generation == "two" else 0,
            "first_army_two_frame": values["emergency_first_army_two_release_frame"] if army_generation == "two" else -1,
            "army_three_events": values["emergency_army_three_release_events"] if army_generation == "three" else 0,
            "army_three_defenders": values["emergency_army_three_released_defenders"] if army_generation == "three" else 0,
            "first_army_three_frame": values["emergency_first_army_three_release_frame"] if army_generation == "three" else -1,
            "frames": release_frames,
            "sizes": release_sizes,
            f"army_{army_generation}_flags": release_flags,
            "army_two_flags": release_flags if army_generation == "two" else [],
            "army_three_flags": release_flags if army_generation == "three" else [],
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
        "episodes": episode_summary,
        "checks": checks,
        "quantitative_grade": {"score": score, "max_score": 100, "grade": grade},
        "review_flags": sorted(set(review_flags)),
        "opportunity_notes": sorted(set(opportunity_notes)),
        "note": "v33/v34 emergency bridge counters are descriptive telemetry. v35 adds cumulative continuous-threat episode checks. Assignment totals count probe identities; release totals count released defenders; release reason counters count release events.",
    }


def _player_race(player: object) -> str | None:
    if not isinstance(player, dict):
        return None
    environment = player.get("environment") if isinstance(player.get("environment"), dict) else {}
    return _normalise_race(environment.get("BWAPI_CONFIG_AUTO_MENU__RACE"))


def _zerg_offense_stage_summary(metadata: dict[str, object], opponent_race: str | None = None,
                                generation: str | None = None) -> dict[str, object]:
    """Validate v34's staged-offense scalar and parallel state traces.

    The v31-v33 diagnostics do not have these fields. Their absence is kept as
    ``legacy_absent`` so old scorecards remain useful and comparable.
    """
    generation = generation or _diagnostic_generation(metadata)
    scalar_defaults: dict[str, object] = {
        "zerg_offense_stage_released": False,
        "zerg_offense_stage_remote_target_events": 0,
        "zerg_offense_stage_unique_units": 0,
        "zerg_offense_stage_pre_release_remote_blocks": 0,
        "zerg_offense_stage_pre_release_remote_orders": 0,
        "zerg_offense_stage_pre_release_remote_attempts": 0,
        "zerg_offense_stage_pre_release_remote_accepts": 0,
        "zerg_offense_stage_post_release_remote_attempts": 0,
        "zerg_offense_stage_post_release_remote_accepts": 0,
        "zerg_offense_stage_local_defense_attack_orders": 0,
        "zerg_offense_stage_home_move_attempts": 0,
        "zerg_offense_stage_home_move_orders": 0,
        "zerg_offense_stage_home_move_accepts": 0,
        "zerg_offense_stage_home_move_cooldown_blocks": 0,
        "zerg_offense_stage_home_move_repeat_orders": 0,
        "zerg_offense_stage_min_accepted_repeat_interval": -1,
        "zerg_offense_stage_home_target_orders": 0,
        "zerg_offense_stage_release_events": 0,
        "zerg_offense_stage_reset_events": 0,
        "zerg_offense_stage_restage_events": 0,
        "first_zerg_offense_stage_suppression_frame": -1,
        "first_zerg_offense_stage_frame": -1,
        "first_zerg_offense_stage_threshold_frame": -1,
        "first_zerg_offense_stage_release_frame": -1,
        "first_zerg_offense_stage_reset_frame": -1,
        "zerg_offense_stage_release_army": -1,
        "zerg_offense_stage_release_surplus": -1,
        "zerg_offense_stage_latch_clear_frame": -1,
        "zerg_offense_stage_first_zero_after_release_frame": -1,
        "zerg_offense_stage_peak_surplus": 0,
        "zerg_offense_stage_current_surplus": 0,
    }
    list_names = (
        "zerg_offense_stage_release_unit_ids",
        "zerg_offense_stage_state_frames",
        "zerg_offense_stage_state_army",
        "zerg_offense_stage_state_reserve",
        "zerg_offense_stage_state_surplus",
        "zerg_offense_stage_state_codes",
        "zerg_offense_stage_state_cause_codes",
    )
    required = tuple(scalar_defaults) + list_names + ("zerg_offense_stage_latch_clear_cause",)
    present = [name for name in required if name in metadata]
    feature_present = any(name in metadata for name in required)
    missing = [name for name in required if name not in metadata] if feature_present else []
    invalid_scalars = [name for name, default in scalar_defaults.items()
                       if name in metadata and (
                           (isinstance(default, bool) and not isinstance(metadata[name], bool)) or
                           (isinstance(default, int) and not isinstance(default, bool) and
                            (not isinstance(metadata[name], int) or isinstance(metadata[name], bool)))
                       )]
    invalid_lists = [name for name in list_names if name in metadata and not isinstance(metadata[name], list)]
    if "zerg_offense_stage_latch_clear_cause" in metadata and not isinstance(metadata["zerg_offense_stage_latch_clear_cause"], str):
        invalid_scalars.append("zerg_offense_stage_latch_clear_cause")
    values = {}
    for name, default in scalar_defaults.items():
        raw = metadata.get(name, default)
        if isinstance(default, bool):
            values[name] = raw if isinstance(raw, bool) else default
        else:
            values[name] = raw if isinstance(raw, int) and not isinstance(raw, bool) else default
    raw_cause = metadata.get("zerg_offense_stage_latch_clear_cause", "none")
    values["zerg_offense_stage_latch_clear_cause"] = raw_cause if isinstance(raw_cause, str) else "none"
    arrays = {name: _metadata_list(metadata, name) for name in list_names}
    race = _normalise_race(opponent_race)
    if race is None:
        known_zerg = metadata.get("known_zerg")
        if isinstance(known_zerg, bool):
            race = "zerg" if known_zerg else "non-zerg"
    expected_active = race == "zerg"
    expected_inactive = race in {"terran", "protoss", "non-zerg"}
    review_flags: list[str] = []
    if feature_present and missing:
        review_flags.append("zerg_offense_required_fields_missing")
    opportunity_notes: list[str] = []
    if invalid_scalars:
        review_flags.append("zerg_offense_scalar_type_mismatch")
    if invalid_lists:
        review_flags.append("zerg_offense_trace_type_mismatch")

    lengths = {name: len(value) for name, value in arrays.items()}
    state_names = list_names[1:]
    state_lengths = {lengths[name] for name in state_names}
    if len(state_lengths) > 1:
        review_flags.append("zerg_offense_state_trace_length_mismatch")
    row_count = min((lengths[name] for name in state_names), default=0)
    rows: list[dict[str, object]] = []
    for index in range(row_count):
        row = {
            "index": index,
            "frame": arrays["zerg_offense_stage_state_frames"][index],
            "army": arrays["zerg_offense_stage_state_army"][index],
            "reserve": arrays["zerg_offense_stage_state_reserve"][index],
            "surplus": arrays["zerg_offense_stage_state_surplus"][index],
            "state": arrays["zerg_offense_stage_state_codes"][index],
            "cause": arrays["zerg_offense_stage_state_cause_codes"][index],
        }
        rows.append(row)
        for key in ("frame", "army", "reserve", "surplus", "state", "cause"):
            if not isinstance(row[key], int) or isinstance(row[key], bool):
                review_flags.append("zerg_offense_state_value_type_mismatch")
                row[key] = 0
        if isinstance(row["state"], int) and row["state"] not in (0, 1):
            review_flags.append("zerg_offense_unknown_state_code")
        if isinstance(row["cause"], int) and row["cause"] not in (0, 2, 4):
            review_flags.append("zerg_offense_unknown_cause_code")
        for key in ("frame", "army", "reserve", "surplus"):
            if isinstance(row[key], int) and row[key] < 0:
                review_flags.append("zerg_offense_negative_state_value")

    nonnegative_counter_names = (
        "zerg_offense_stage_remote_target_events", "zerg_offense_stage_unique_units",
        "zerg_offense_stage_pre_release_remote_blocks", "zerg_offense_stage_pre_release_remote_orders",
        "zerg_offense_stage_pre_release_remote_attempts", "zerg_offense_stage_pre_release_remote_accepts",
        "zerg_offense_stage_post_release_remote_attempts", "zerg_offense_stage_post_release_remote_accepts",
        "zerg_offense_stage_local_defense_attack_orders", "zerg_offense_stage_home_move_attempts",
        "zerg_offense_stage_home_move_orders", "zerg_offense_stage_home_move_accepts",
        "zerg_offense_stage_home_move_cooldown_blocks", "zerg_offense_stage_home_move_repeat_orders",
        "zerg_offense_stage_home_target_orders", "zerg_offense_stage_release_events",
        "zerg_offense_stage_reset_events", "zerg_offense_stage_restage_events",
        "zerg_offense_stage_peak_surplus", "zerg_offense_stage_current_surplus",
    )
    if any(values[name] < 0 for name in nonnegative_counter_names):
        review_flags.append("zerg_offense_negative_counter")
    if values["zerg_offense_stage_unique_units"] < 0:
        review_flags.append("zerg_offense_negative_unique_units")
    if values["zerg_offense_stage_home_move_orders"] > values["zerg_offense_stage_home_move_attempts"]:
        review_flags.append("zerg_offense_home_moves_exceed_attempts")
    if values["zerg_offense_stage_home_move_accepts"] != values["zerg_offense_stage_home_move_orders"]:
        review_flags.append("zerg_offense_home_move_accept_mismatch")
    if values["zerg_offense_stage_home_move_repeat_orders"] > values["zerg_offense_stage_home_move_orders"]:
        review_flags.append("zerg_offense_home_move_repeats_exceed_orders")
    interval = values["zerg_offense_stage_min_accepted_repeat_interval"]
    if isinstance(interval, int) and interval >= 0 and interval < 96:
        review_flags.append("zerg_offense_home_move_cadence_below_96")
    if values["zerg_offense_stage_pre_release_remote_blocks"] != values["zerg_offense_stage_pre_release_remote_attempts"]:
        review_flags.append("zerg_offense_remote_block_attempt_mismatch")
    if values["zerg_offense_stage_pre_release_remote_orders"] != values["zerg_offense_stage_pre_release_remote_accepts"]:
        review_flags.append("zerg_offense_pre_release_order_accept_mismatch")
    if values["zerg_offense_stage_pre_release_remote_accepts"] > 0:
        review_flags.append("zerg_offense_remote_attack_during_staging")
    if values["zerg_offense_stage_post_release_remote_accepts"] > values["zerg_offense_stage_post_release_remote_attempts"]:
        review_flags.append("zerg_offense_post_release_accepts_exceed_attempts")

    cause_release = [row for row in rows if row["cause"] == 2]
    cause_reset = [row for row in rows if row["cause"] == 4]
    if values["zerg_offense_stage_release_events"] != len(cause_release):
        review_flags.append("zerg_offense_release_event_count_mismatch")
    if values["zerg_offense_stage_reset_events"] != len(cause_reset):
        review_flags.append("zerg_offense_reset_event_count_mismatch")
    if values["zerg_offense_stage_restage_events"] != values["zerg_offense_stage_reset_events"]:
        review_flags.append("zerg_offense_restage_reset_count_mismatch")
    for row in cause_release:
        if row["state"] != 1 or row["surplus"] < 6:
            review_flags.append("zerg_offense_release_without_threshold")
    for row in cause_reset:
        if row["state"] != 0 or row["surplus"] != 0:
            review_flags.append("zerg_offense_reset_without_zero_surplus")
    if rows:
        first_positive = next((row for row in rows if row["surplus"] > 0), None)
        if first_positive and first_positive["state"] != 0:
            review_flags.append("zerg_offense_missing_initial_staging")
        if first_positive and values["first_zerg_offense_stage_frame"] != first_positive["frame"]:
            review_flags.append("zerg_offense_first_staging_frame_mismatch")
        first_threshold = next((row for row in rows if row["surplus"] >= 6), None)
        if first_threshold and values["first_zerg_offense_stage_threshold_frame"] != first_threshold["frame"]:
            review_flags.append("zerg_offense_threshold_frame_mismatch")
        if values["zerg_offense_stage_current_surplus"] != rows[-1]["surplus"]:
            review_flags.append("zerg_offense_current_surplus_mismatch")
        if _metadata_bool(metadata, "zerg_offense_stage_released", False) != (rows[-1]["state"] == 1):
            review_flags.append("zerg_offense_latch_state_mismatch")
        for previous, current in zip(rows, rows[1:]):
            if previous["state"] == 1 and current["state"] == 0 and current["surplus"] != 0:
                review_flags.append("zerg_offense_restage_with_positive_surplus")
            if previous["state"] == 0 and current["state"] == 1 and current["surplus"] < 6:
                review_flags.append("zerg_offense_release_below_threshold")
    elif feature_present and expected_active:
        opportunity_notes.append("state_trace_unobserved")

    release_ids = arrays["zerg_offense_stage_release_unit_ids"]
    if any(not isinstance(value, int) or isinstance(value, bool) for value in release_ids):
        review_flags.append("zerg_offense_release_id_type_mismatch")
    if len(set(release_ids)) != len(release_ids):
        review_flags.append("zerg_offense_release_ids_duplicate")
    if values["zerg_offense_stage_release_events"] > 0 and not release_ids:
        review_flags.append("zerg_offense_release_ids_missing")
    if cause_release:
        first_release = cause_release[0]
        if values["first_zerg_offense_stage_release_frame"] != first_release["frame"]:
            review_flags.append("zerg_offense_release_frame_mismatch")
        if values["zerg_offense_stage_release_army"] != first_release["army"]:
            review_flags.append("zerg_offense_release_army_mismatch")
        if values["zerg_offense_stage_release_surplus"] != first_release["surplus"]:
            review_flags.append("zerg_offense_release_surplus_mismatch")
    if values["zerg_offense_stage_reset_events"] > 0:
        if values["zerg_offense_stage_latch_clear_frame"] < 0 or values["zerg_offense_stage_first_zero_after_release_frame"] < 0:
            review_flags.append("zerg_offense_latch_clear_frame_missing")
        if values["zerg_offense_stage_latch_clear_cause"] != "surplus_zero":
            review_flags.append("zerg_offense_latch_clear_cause_mismatch")
    elif values["zerg_offense_stage_latch_clear_frame"] != -1 or values["zerg_offense_stage_first_zero_after_release_frame"] != -1:
        review_flags.append("zerg_offense_unexpected_latch_clear")
    if values["zerg_offense_stage_reset_events"] == 0 and values["zerg_offense_stage_latch_clear_cause"] != "none":
        review_flags.append("zerg_offense_unexpected_latch_clear_cause")

    if expected_active and feature_present:
        if values["zerg_offense_stage_peak_surplus"] < 6:
            opportunity_notes.append("threshold_six_unobserved")
        if values["zerg_offense_stage_remote_target_events"] == 0:
            opportunity_notes.append("remote_staging_opportunity_unobserved")
        if values["zerg_offense_stage_home_move_attempts"] == 0:
            opportunity_notes.append("home_move_opportunity_unobserved")
        if values["zerg_offense_stage_release_events"] > 0 and values["zerg_offense_stage_reset_events"] == 0:
            opportunity_notes.append("latch_clear_unobserved")

    inactive_values = []
    if expected_inactive and feature_present:
        for name, default in scalar_defaults.items():
            value = values[name]
            if value != default:
                inactive_values.append(name)
        if values["zerg_offense_stage_latch_clear_cause"] != "none":
            inactive_values.append("zerg_offense_stage_latch_clear_cause")
        if any(arrays[name] for name in list_names):
            inactive_values.extend(name for name in list_names if arrays[name])
        if inactive_values:
            review_flags.append("non_zerg_zerg_offense_activity")

    checks = {
        "telemetry_complete": feature_present and not missing,
        "state_trace_consistent": not any(flag.startswith("zerg_offense_state") or flag.startswith("zerg_offense_unknown") for flag in review_flags),
        "threshold_latch_consistent": not any(flag.startswith("zerg_offense_release") or flag.startswith("zerg_offense_reset") or flag.startswith("zerg_offense_restage") or flag.startswith("zerg_offense_latch") for flag in review_flags),
        "staging_blocks_remote": "zerg_offense_remote_attack_during_staging" not in review_flags,
        "home_move_cadence": "zerg_offense_home_move_cadence_below_96" not in review_flags,
        "non_zerg_sentinels": expected_inactive and not inactive_values if expected_inactive else None,
    }
    if not feature_present:
        grade = "legacy_absent"
        telemetry_status = "legacy_absent"
    elif expected_inactive:
        grade = "pass" if not review_flags else "review"
        telemetry_status = "complete" if not missing else "partial"
    elif expected_active and values["zerg_offense_stage_peak_surplus"] < 6 and not review_flags:
        grade = "untested"
        telemetry_status = "complete" if not missing else "partial"
    else:
        grade = "review" if review_flags else "pass"
        telemetry_status = "complete" if not missing else "partial"
    return {
        "generation": generation if feature_present and generation in {"v34", "v35", "v36", "v37", "v38", "v40", "v41", "v42", "v43"} else "v34" if feature_present else "legacy",
        "opponent_race": race,
        "expected_active": expected_active,
        "expected_inactive": expected_inactive,
        "telemetry_status": telemetry_status,
        "fields_present": present,
        "missing_fields": missing,
        "invalid_fields": sorted(set(invalid_scalars + invalid_lists)),
        "state_codes": {"home_staging": 0, "released_latched": 1},
        "cause_codes": {"steady": 0, "release_threshold": 2, "surplus_zero": 4},
        "release_threshold": 6,
        "state": {
            "rows": rows,
            "frames": arrays["zerg_offense_stage_state_frames"],
            "army": arrays["zerg_offense_stage_state_army"],
            "reserve": arrays["zerg_offense_stage_state_reserve"],
            "surplus": arrays["zerg_offense_stage_state_surplus"],
            "codes": arrays["zerg_offense_stage_state_codes"],
            "cause_codes": arrays["zerg_offense_stage_state_cause_codes"],
        },
        "release": {
            "events": values["zerg_offense_stage_release_events"],
            "frame": values["first_zerg_offense_stage_release_frame"],
            "army": values["zerg_offense_stage_release_army"],
            "surplus": values["zerg_offense_stage_release_surplus"],
            "unit_ids": release_ids,
            "threshold_frame": values["first_zerg_offense_stage_threshold_frame"],
        },
        "latch": {
            "released": values["zerg_offense_stage_released"],
            "reset_events": values["zerg_offense_stage_reset_events"],
            "restage_events": values["zerg_offense_stage_restage_events"],
            "clear_frame": values["zerg_offense_stage_latch_clear_frame"],
            "clear_cause": values["zerg_offense_stage_latch_clear_cause"],
            "first_zero_after_release_frame": values["zerg_offense_stage_first_zero_after_release_frame"],
        },
        "remote_offense": {
            "target_events": values["zerg_offense_stage_remote_target_events"],
            "pre_release_blocks": values["zerg_offense_stage_pre_release_remote_blocks"],
            "pre_release_attempts": values["zerg_offense_stage_pre_release_remote_attempts"],
            "pre_release_accepts": values["zerg_offense_stage_pre_release_remote_accepts"],
            "pre_release_orders": values["zerg_offense_stage_pre_release_remote_orders"],
            "post_release_attempts": values["zerg_offense_stage_post_release_remote_attempts"],
            "post_release_accepts": values["zerg_offense_stage_post_release_remote_accepts"],
            "local_defense_attack_orders": values["zerg_offense_stage_local_defense_attack_orders"],
        },
        "home_moves": {
            "attempts": values["zerg_offense_stage_home_move_attempts"],
            "orders": values["zerg_offense_stage_home_move_orders"],
            "accepts": values["zerg_offense_stage_home_move_accepts"],
            "cooldown_blocks": values["zerg_offense_stage_home_move_cooldown_blocks"],
            "repeat_orders": values["zerg_offense_stage_home_move_repeat_orders"],
            "min_accepted_repeat_interval": values["zerg_offense_stage_min_accepted_repeat_interval"],
            "home_target_orders": values["zerg_offense_stage_home_target_orders"],
        },
        "peak_surplus": values["zerg_offense_stage_peak_surplus"],
        "current_surplus": values["zerg_offense_stage_current_surplus"],
        "checks": checks,
        "quantitative_grade": {"grade": grade, "score": round(100 * sum(value for value in checks.values() if isinstance(value, bool)) / max(1, sum(isinstance(value, bool) for value in checks.values()))), "max_score": 100},
        "review_flags": sorted(set(review_flags)),
        "opportunity_notes": sorted(set(opportunity_notes)),
        "note": "v34 staged-offense counters and state rows are descriptive telemetry; unobserved registered opportunities are untested unless the evaluation cohort gate explicitly requires exercise.",
    }


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


def _scaling_summary(metadata: dict[str, object], generation: str | None = None) -> dict[str, object]:
    """Validate v37 scaling, range-upgrade, and production-cap telemetry."""
    generation = generation or _diagnostic_generation(metadata)
    required = (
        "max_pylon_cap", "max_post_core_gateway_cap",
        "range_upgrade_eligibility_frame", "range_upgrade_bank_start_frame",
        "range_upgrade_bank_block_count", "range_upgrade_attempt_frame",
        "range_upgrade_accepted_frame", "range_upgrade_completion_frame",
        "range_upgrade_attempts", "range_upgrade_accepted", "range_upgrade_completions",
        "range_upgrade_max_bank_minerals", "range_upgrade_max_bank_gas",
        "seventh_pylon_accepted_frame", "seventh_pylon_current_frame",
        "seventh_pylon_completed_frame", "fifth_gateway_accepted_frame",
        "fifth_gateway_current_frame", "fifth_gateway_completed_frame",
    )
    feature_present = generation in {"v37", "v38", "v40", "v41", "v42", "v43"} or any(name in metadata for name in required)
    if not feature_present:
        return {
            "generation": "legacy_absent", "telemetry_status": "legacy_absent",
            "fields_present": [], "missing_fields": [], "invalid_fields": [],
            "review_flags": [], "opportunity_notes": [],
            "checks": {}, "quantitative_grade": {"grade": "legacy_absent", "score": 0, "max_score": 0},
        }
    missing = [name for name in required if name not in metadata]
    invalid = [name for name in required if name in metadata and
               (not isinstance(metadata[name], int) or isinstance(metadata[name], bool))]
    flags: list[str] = []
    if missing:
        flags.append("scaling_required_fields_missing")
    if invalid:
        flags.append("scaling_field_type_mismatch")
    values = {name: _metadata_int(metadata, name, -1) for name in required}
    if values["max_pylon_cap"] != 10 or values["max_post_core_gateway_cap"] != 6:
        flags.append("scaling_cap_constant_mismatch")
    observed_pylons = _metadata_int(metadata, "max_pylons", -1)
    observed_gateways = _metadata_int(metadata, "max_gateways", -1)
    if observed_pylons > values["max_pylon_cap"]:
        flags.append("scaling_pylon_cap_exceeded")
    if observed_gateways > values["max_post_core_gateway_cap"]:
        flags.append("scaling_gateway_cap_exceeded")
    opportunity_notes: list[str] = []
    for prefix in ("seventh_pylon", "fifth_gateway"):
        accepted, current, completed = (
            values[f"{prefix}_{suffix}_frame"] for suffix in ("accepted", "current", "completed")
        )
        observed = [frame for frame in (accepted, current, completed) if frame >= 0]
        if current >= 0 and accepted < 0:
            flags.append(f"{prefix}_current_without_accept")
        if completed >= 0 and current < 0:
            flags.append(f"{prefix}_complete_without_current")
        if observed != sorted(observed):
            flags.append(f"{prefix}_milestone_order")
        if accepted < 0:
            opportunity_notes.append(f"{prefix}_opportunity_unobserved")
        elif current < 0:
            opportunity_notes.append(f"{prefix}_accepted_not_current_before_terminal")
        elif completed < 0:
            opportunity_notes.append(f"{prefix}_current_not_completed_before_terminal")
    eligibility = values["range_upgrade_eligibility_frame"]
    attempts = values["range_upgrade_attempts"]
    accepted_count = values["range_upgrade_accepted"]
    completion_count = values["range_upgrade_completions"]
    bank_start = values["range_upgrade_bank_start_frame"]
    attempt_frame = values["range_upgrade_attempt_frame"]
    accepted_frame = values["range_upgrade_accepted_frame"]
    completion_frame = values["range_upgrade_completion_frame"]
    if eligibility < 0:
        opportunity_notes.append("range_upgrade_opportunity_unobserved")
        if any(frame >= 0 for frame in (bank_start, attempt_frame, accepted_frame, completion_frame)) or any(
            value != 0 for value in (attempts, accepted_count, completion_count)
        ):
            flags.append("range_upgrade_activity_without_eligibility")
    else:
        if bank_start < eligibility:
            flags.append("range_upgrade_bank_start_missing_or_early")
        if accepted_count not in (0, 1) or completion_count not in (0, 1):
            flags.append("range_upgrade_count_out_of_range")
        if accepted_count > attempts:
            flags.append("range_upgrade_accept_count_exceeds_attempts")
        if attempts == 0:
            if any(frame >= 0 for frame in (attempt_frame, accepted_frame, completion_frame)) or accepted_count or completion_count:
                flags.append("range_upgrade_zero_attempt_trace_mismatch")
            else:
                opportunity_notes.append("range_upgrade_banking_before_terminal")
        else:
            if attempt_frame < bank_start:
                flags.append("range_upgrade_attempt_frame_missing_or_early")
            if accepted_count == 0:
                if accepted_frame >= 0 or completion_frame >= 0 or completion_count:
                    flags.append("range_upgrade_unaccepted_trace_mismatch")
                else:
                    opportunity_notes.append("range_upgrade_attempt_not_accepted")
            else:
                if accepted_frame < attempt_frame:
                    flags.append("range_upgrade_accepted_frame_missing_or_early")
                if completion_count == 0:
                    if completion_frame >= 0:
                        flags.append("range_upgrade_completion_frame_without_count")
                    else:
                        opportunity_notes.append("range_upgrade_accepted_not_completed_before_terminal")
                elif completion_frame < accepted_frame:
                    flags.append("range_upgrade_completion_frame_missing_or_early")
    for name in ("range_upgrade_bank_block_count", "range_upgrade_attempts",
                 "range_upgrade_accepted", "range_upgrade_completions",
                 "range_upgrade_max_bank_minerals", "range_upgrade_max_bank_gas"):
        if values[name] < 0:
            flags.append("scaling_negative_counter")
            break
    checks = {
        "required_fields": not missing and not invalid,
        "cap_constants": "scaling_cap_constant_mismatch" not in flags,
        "milestone_order": not any(
            flag.endswith("milestone_order") or flag.endswith("without_accept") or flag.endswith("without_current")
            for flag in flags
        ),
        "upgrade_trace": not any(flag.startswith("range_upgrade_") and flag != "range_upgrade_opportunity_unobserved" for flag in flags),
    }
    if flags:
        grade = "review"
    elif eligibility < 0:
        grade = "untested"
    elif completion_count != 1:
        grade = "partial"
    else:
        grade = "pass"
    return {
        "generation": generation if generation in {"v37", "v38", "v40", "v41", "v42", "v43"} else "v37", "telemetry_status": "complete" if not missing and not invalid else "partial",
        "fields_present": [name for name in required if name in metadata],
        "missing_fields": missing, "invalid_fields": invalid, "review_flags": sorted(set(flags)),
        "opportunity_notes": opportunity_notes, "checks": checks,
        "caps": {"max_pylons": values["max_pylon_cap"], "max_gateways": values["max_post_core_gateway_cap"]},
        "observed_caps": {"max_pylons": observed_pylons, "max_gateways": observed_gateways},
        "upgrade": {name: values[name] for name in required if name.startswith("range_upgrade_")},
        "milestones": {prefix: {suffix: values[f"{prefix}_{suffix}_frame"] for suffix in ("accepted", "current", "completed")}
                       for prefix in ("seventh_pylon", "fifth_gateway")},
        "quantitative_grade": {"grade": grade, "score": 100 if grade in {"pass", "untested"} else (60 if grade == "partial" else 0),
                                "max_score": 100},
    }


def _shared_target_summary(metadata: dict[str, object], opponent_race: str | None = None,
                           generation: str | None = None) -> dict[str, object]:
    """Validate v38 shared-visible-target traces and command counters."""
    generation = generation or _diagnostic_generation(metadata)
    scalar_names = (
        "shared_target_selections", "shared_target_attempts", "shared_target_accepted",
        "shared_target_non_zerg_selections", "shared_target_illegal_selections",
        "shared_target_switches", "shared_target_rejects", "shared_target_correction_opportunities",
    )
    list_names = (
        "shared_target_frames", "shared_target_ids", "shared_target_participant_counts",
        "shared_target_eligible_counts", "shared_target_ordered_counts",
        "shared_target_local_counts", "shared_target_attempt_counts",
        "shared_target_accepted_counts", "shared_target_participant_ids",
    )
    required = scalar_names + list_names
    feature_present = generation in {"v38", "v40", "v41", "v42", "v43"} or any(name in metadata for name in required)
    if not feature_present:
        return {
            "generation": "legacy_absent", "telemetry_status": "legacy_absent",
            "fields_present": [], "missing_fields": [], "invalid_fields": [],
            "checks": {}, "opportunity_notes": [], "review_flags": [],
            "trace": {name: [] for name in list_names},
            "quantitative_grade": {"grade": "legacy_absent", "score": 0, "max_score": 0},
        }
    missing = [name for name in required if name not in metadata]
    invalid = [name for name in required if name in metadata and
               ((name in scalar_names and (not isinstance(metadata[name], int) or isinstance(metadata[name], bool))) or
                (name in list_names and not isinstance(metadata[name], list)))]
    flags: list[str] = []
    if missing:
        flags.append("shared_target_required_fields_missing")
    if invalid:
        flags.append("shared_target_field_type_mismatch")
    values = {name: _metadata_int(metadata, name, 0) for name in scalar_names}
    arrays = {name: _metadata_list(metadata, name) for name in list_names}
    for name in scalar_names:
        raw_value = metadata.get(name)
        if isinstance(raw_value, int) and not isinstance(raw_value, bool) and raw_value < 0:
            flags.append(f"shared_target_negative_counter_{name.removeprefix('shared_target_')}")
    trace_lengths = {name: len(value) for name, value in arrays.items() if name != "shared_target_participant_ids"}
    if len(set(trace_lengths.values())) > 1:
        flags.append("shared_target_trace_length_mismatch")
    rows = min(trace_lengths.values(), default=0)
    frames = arrays["shared_target_frames"]
    ids = arrays["shared_target_ids"]
    participant_counts = arrays["shared_target_participant_counts"]
    eligible_counts = arrays["shared_target_eligible_counts"]
    ordered_counts = arrays["shared_target_ordered_counts"]
    local_counts = arrays["shared_target_local_counts"]
    attempt_counts = arrays["shared_target_attempt_counts"]
    accepted_counts = arrays["shared_target_accepted_counts"]
    participant_ids = arrays["shared_target_participant_ids"]
    if any(not isinstance(value, int) or isinstance(value, bool) for value in participant_ids):
        flags.append("shared_target_participant_id_type_mismatch")
    if any(isinstance(value, int) and not isinstance(value, bool) and value < 0 for value in participant_ids):
        flags.append("shared_target_participant_id_invalid")
    if len(frames) != rows or len(ids) != rows:
        flags.append("shared_target_trace_incomplete")
    if any(not isinstance(frames[index], int) or isinstance(frames[index], bool) or frames[index] < 0
           for index in range(rows)):
        flags.append("shared_target_frame_invalid")
    if any(current <= previous for previous, current in zip(frames, frames[1:])
           if isinstance(previous, int) and isinstance(current, int)):
        flags.append("shared_target_frames_not_ordered")
    if any(not isinstance(ids[index], int) or isinstance(ids[index], bool) or ids[index] < 0
           for index in range(rows)):
        flags.append("shared_target_id_invalid")
    row_arrays = (participant_counts, eligible_counts, ordered_counts, local_counts, attempt_counts, accepted_counts)
    row_valid = []
    for index in range(rows):
        valid = all(isinstance(array[index], int) and not isinstance(array[index], bool) and array[index] >= 0
                    for array in row_arrays)
        row_valid.append(valid)
    if not all(row_valid):
        flags.append("shared_target_count_invalid")
    participant_counts_valid = all(isinstance(value, int) and not isinstance(value, bool) and value >= 0
                                   for value in participant_counts[:rows])
    if participant_counts_valid and len(participant_ids) != sum(participant_counts[:rows]):
        flags.append("shared_target_participant_trace_total_mismatch")
    for index in range(rows):
        if not row_valid[index]:
            continue
        if participant_counts[index] != eligible_counts[index]:
            flags.append("shared_target_participant_eligible_mismatch")
        if ordered_counts[index] > eligible_counts[index] or local_counts[index] > eligible_counts[index]:
            flags.append("shared_target_order_count_exceeds_eligible")
        if local_counts[index] not in (0, eligible_counts[index]):
            flags.append("shared_target_local_count_partial")
        if attempt_counts[index] > participant_counts[index] or accepted_counts[index] > attempt_counts[index]:
            flags.append("shared_target_accept_count_exceeds_attempts")
        if not participant_counts_valid:
            continue
        start = sum(participant_counts[:index])
        end = start + participant_counts[index]
        row_ids = participant_ids[start:end]
        if len(row_ids) != participant_counts[index]:
            flags.append("shared_target_participant_trace_mismatch")
        if all(isinstance(value, int) and not isinstance(value, bool) for value in row_ids) and len(row_ids) != len(set(row_ids)):
            flags.append("shared_target_participant_ids_duplicate")
    valid_row_counts = all(row_valid)
    if values["shared_target_selections"] != rows:
        flags.append("shared_target_selection_count_mismatch")
    if valid_row_counts and values["shared_target_attempts"] != sum(attempt_counts[:rows]):
        flags.append("shared_target_attempt_count_mismatch")
    if valid_row_counts and values["shared_target_accepted"] != sum(accepted_counts[:rows]):
        flags.append("shared_target_accepted_count_mismatch")
    if values["shared_target_rejects"] != values["shared_target_attempts"] - values["shared_target_accepted"]:
        flags.append("shared_target_reject_count_mismatch")
    if all(isinstance(value, int) and not isinstance(value, bool) for value in ids[:rows]):
        expected_switches = sum(previous != current for previous, current in zip(ids[:rows], ids[1:rows]))
        if values["shared_target_switches"] != expected_switches:
            flags.append("shared_target_switch_count_mismatch")
    if values["shared_target_non_zerg_selections"] > values["shared_target_selections"]:
        flags.append("shared_target_non_zerg_count_exceeds_selections")
    race = _normalise_race(opponent_race)
    if race in {"terran", "protoss"} and values["shared_target_non_zerg_selections"] != values["shared_target_selections"]:
        flags.append("shared_target_non_zerg_sentinel_mismatch")
    if race == "zerg" and values["shared_target_non_zerg_selections"] != 0:
        flags.append("shared_target_zerg_sentinel_mismatch")
    if values["shared_target_illegal_selections"] != 0:
        flags.append("shared_target_illegal_selection")
    if values["shared_target_rejects"] != 0:
        flags.append("shared_target_rejected_command")
    multi_participant_selections = sum(1 for value in participant_counts[:rows]
                                       if isinstance(value, int) and not isinstance(value, bool) and value >= 2)
    coordinated_accepted_selections = sum(
        1 for index in range(rows)
        if isinstance(participant_counts[index], int) and not isinstance(participant_counts[index], bool)
        and participant_counts[index] >= 2
        and isinstance(accepted_counts[index], int) and not isinstance(accepted_counts[index], bool)
        and accepted_counts[index] >= 1
    )
    max_participants = max((value for value in participant_counts[:rows]
                            if isinstance(value, int) and not isinstance(value, bool)), default=0)
    opportunity_notes = []
    if not rows:
        opportunity_notes.append("shared_target_opportunity_unobserved")
    elif not multi_participant_selections:
        opportunity_notes.append("shared_target_multi_participant_opportunity_unobserved")
    elif not coordinated_accepted_selections:
        opportunity_notes.append("shared_target_accepted_command_unobserved")
    grade = "review" if flags else "pass" if coordinated_accepted_selections else "untested"
    return {
        "generation": generation if generation in {"v38", "v40", "v41", "v42", "v43"} else "v38", "telemetry_status": "complete" if not missing and not invalid else "partial",
        "fields_present": [name for name in required if name in metadata],
        "missing_fields": missing, "invalid_fields": invalid,
        "review_flags": sorted(set(flags)), "opportunity_notes": opportunity_notes,
        "trace": {name: arrays[name] for name in list_names},
        "counters": values,
        "max_participants": max_participants,
        "multi_participant_selections": multi_participant_selections,
        "coordinated_accepted_selections": coordinated_accepted_selections,
        "checks": {
            "required_fields": not missing and not invalid,
            "trace_aligned": "shared_target_trace_length_mismatch" not in flags,
            "frames_ordered": "shared_target_frames_not_ordered" not in flags,
            "target_ids_valid": "shared_target_id_invalid" not in flags,
            "participant_trace": not any(flag.startswith("shared_target_participant") for flag in flags),
            "counts_consistent": not any("count_mismatch" in flag or "exceeds" in flag for flag in flags),
            "local_count_shape": "shared_target_local_count_partial" not in flags,
            "multi_participant_opportunity": multi_participant_selections > 0,
            "switches_consistent": "shared_target_switch_count_mismatch" not in flags,
            "correction_opportunities": values["shared_target_correction_opportunities"],
            "no_invalid": values["shared_target_illegal_selections"] == 0 and values["shared_target_rejects"] == 0,
        },
        "quantitative_grade": {"grade": grade, "score": 100 if grade in {"pass", "untested"} else 0, "max_score": 100},
    }


def _gateway_probe_summary(metadata: dict[str, object], generation: str | None = None) -> dict[str, object]:
    """Validate v40's bounded nearest-Gateway-Probe selection proof.

    The candidate writes one row only after an accepted Gateway command, so a
    complete row can prove the public candidate set, nearest-distance choice,
    deterministic ID tie-break, and the corresponding accepted build frame.
    Flat candidate arrays are partitioned by the per-row candidate counts.
    """
    generation = generation or _diagnostic_generation(metadata)
    selection_names = (
        "gateway_probe_selection_frames",
        "gateway_probe_selection_ordinals",
        "gateway_probe_selection_builder_ids",
        "gateway_probe_selection_tile_xs",
        "gateway_probe_selection_tile_ys",
        "gateway_probe_selection_builder_distances",
        "gateway_probe_selection_eligible_counts",
        "gateway_probe_selection_min_eligible_distances",
        "gateway_probe_selection_candidate_counts",
        "gateway_probe_selection_candidate_truncated",
    )
    candidate_names = (
        "gateway_probe_candidate_ids",
        "gateway_probe_candidate_distances",
        "gateway_probe_candidate_reason_codes",
    )
    required = selection_names + candidate_names
    feature_present = generation in {"v40", "v41", "v42", "v43"} or any(name in metadata for name in required)
    if not feature_present:
        return {
            "generation": "legacy_absent", "telemetry_status": "legacy_absent",
            "fields_present": [], "missing_fields": [], "invalid_fields": [],
            "selections": [], "trace": {name: [] for name in required},
            "proof_sufficient": False, "review_flags": [], "opportunity_notes": [],
            "checks": {},
            "quantitative_grade": {"grade": "legacy_absent", "score": 0, "max_score": 0},
        }

    missing = [name for name in required if name not in metadata]
    invalid = [name for name in required if name in metadata and not isinstance(metadata[name], list)]
    arrays = {name: _metadata_list(metadata, name) for name in required}
    flags: list[str] = []
    if missing:
        flags.append("gateway_probe_required_fields_missing")
    if invalid:
        flags.append("gateway_probe_field_type_mismatch")

    selection_lengths = {name: len(arrays[name]) for name in selection_names}
    selection_rows = min(selection_lengths.values(), default=0)
    if len(set(selection_lengths.values())) > 1:
        flags.append("gateway_probe_selection_trace_length_mismatch")
    if any(len(arrays[name]) != selection_rows for name in selection_names):
        flags.append("gateway_probe_selection_trace_incomplete")

    def is_non_bool_int(value: object) -> bool:
        return isinstance(value, int) and not isinstance(value, bool)

    for name in selection_names:
        if any(not is_non_bool_int(value) for value in arrays[name][:selection_rows]):
            flags.append(f"gateway_probe_selection_{name.removeprefix('gateway_probe_selection_')}_type_mismatch")
    for name in candidate_names:
        if any(not is_non_bool_int(value) for value in arrays[name]):
            flags.append(f"gateway_probe_{name.removeprefix('gateway_probe_')}_type_mismatch")

    candidate_counts = arrays["gateway_probe_selection_candidate_counts"]
    counts_valid = all(is_non_bool_int(value) and value >= 0 for value in candidate_counts[:selection_rows])
    if any(is_non_bool_int(value) and value < 0 for value in candidate_counts[:selection_rows]):
        flags.append("gateway_probe_candidate_count_negative")
    expected_candidates = sum(candidate_counts[:selection_rows]) if counts_valid else None
    candidate_lengths = {name: len(arrays[name]) for name in candidate_names}
    if len(set(candidate_lengths.values())) > 1:
        flags.append("gateway_probe_candidate_trace_length_mismatch")
    if expected_candidates is not None and any(length != expected_candidates for length in candidate_lengths.values()):
        flags.append("gateway_probe_candidate_trace_partition_mismatch")

    allowed_reason_codes = {0, 1, 2, 3, 4, 5}
    reason_codes = arrays["gateway_probe_candidate_reason_codes"]
    if any(is_non_bool_int(value) and value not in allowed_reason_codes for value in reason_codes):
        flags.append("gateway_probe_reason_code_invalid")
    if any(is_non_bool_int(value) and value < 0 for value in arrays["gateway_probe_candidate_ids"]):
        flags.append("gateway_probe_candidate_id_invalid")
    if any(is_non_bool_int(value) and value < 0 for value in arrays["gateway_probe_candidate_distances"]):
        flags.append("gateway_probe_candidate_distance_invalid")

    truncation = arrays["gateway_probe_selection_candidate_truncated"]
    if any(is_non_bool_int(value) and value not in {0, 1} for value in truncation[:selection_rows]):
        flags.append("gateway_probe_truncation_flag_invalid")

    frames = arrays["gateway_probe_selection_frames"]
    ordinals = arrays["gateway_probe_selection_ordinals"]
    builder_ids = arrays["gateway_probe_selection_builder_ids"]
    builder_distances = arrays["gateway_probe_selection_builder_distances"]
    eligible_counts = arrays["gateway_probe_selection_eligible_counts"]
    minimum_distances = arrays["gateway_probe_selection_min_eligible_distances"]
    rows: list[dict[str, object]] = []
    candidate_offset = 0
    for index in range(selection_rows):
        count = candidate_counts[index] if is_non_bool_int(candidate_counts[index]) and candidate_counts[index] >= 0 else 0
        end = candidate_offset + count
        row_candidates = [
            {"id": candidate_id, "distance": candidate_distance, "reason_code": reason}
            for candidate_id, candidate_distance, reason in zip(
                arrays["gateway_probe_candidate_ids"][candidate_offset:end],
                arrays["gateway_probe_candidate_distances"][candidate_offset:end],
                arrays["gateway_probe_candidate_reason_codes"][candidate_offset:end],
            )
        ]
        candidate_offset = end
        row = {
            "index": index,
            "frame": frames[index],
            "ordinal": ordinals[index],
            "builder_id": builder_ids[index],
            "tile_x": arrays["gateway_probe_selection_tile_xs"][index],
            "tile_y": arrays["gateway_probe_selection_tile_ys"][index],
            "builder_distance": builder_distances[index],
            "eligible_count": eligible_counts[index],
            "minimum_eligible_distance": minimum_distances[index],
            "candidate_count": count,
            "candidate_truncated": truncation[index],
            "candidates": row_candidates,
        }
        rows.append(row)

        row_values = (frames[index], ordinals[index], builder_ids[index],
                      arrays["gateway_probe_selection_tile_xs"][index],
                      arrays["gateway_probe_selection_tile_ys"][index],
                      builder_distances[index], eligible_counts[index],
                      minimum_distances[index], count, truncation[index])
        if any(not is_non_bool_int(value) for value in row_values):
            continue
        if any(value < 0 for value in row_values[:8]) or row_values[8] < 0:
            flags.append(f"gateway_probe_selection_row_{index}_negative_value")
        if row_values[9] != 0:
            flags.append(f"gateway_probe_selection_row_{index}_truncated")
        if row_values[6] <= 0:
            flags.append(f"gateway_probe_selection_row_{index}_no_eligible_builder")

        candidate_ids = [item["id"] for item in row_candidates]
        eligible = [item for item in row_candidates if item["reason_code"] == 0]
        if len(eligible) != row_values[6]:
            flags.append(f"gateway_probe_selection_row_{index}_eligible_count_mismatch")
        selected = [item for item in eligible if item["id"] == row_values[2]]
        if len(selected) != 1:
            flags.append(f"gateway_probe_selection_row_{index}_selected_builder_occurrence")
        elif selected[0]["distance"] != row_values[5]:
            flags.append(f"gateway_probe_selection_row_{index}_selected_distance_mismatch")
        if eligible:
            nearest_distance = min(item["distance"] for item in eligible)
            nearest_ids = [item["id"] for item in eligible if item["distance"] == nearest_distance]
            if row_values[7] != nearest_distance:
                flags.append(f"gateway_probe_selection_row_{index}_minimum_distance_mismatch")
            if row_values[5] != nearest_distance:
                flags.append(f"gateway_probe_selection_row_{index}_nearest_distance_failure")
            if row_values[2] != min(nearest_ids):
                flags.append(f"gateway_probe_selection_row_{index}_builder_tie_break_failure")
        elif row_values[6] > 0:
            flags.append(f"gateway_probe_selection_row_{index}_eligible_trace_missing")
        if len(candidate_ids) != len(set(candidate_ids)):
            flags.append(f"gateway_probe_selection_row_{index}_candidate_id_duplicate")

    if any(not is_non_bool_int(value) or value < 0 for value in frames[:selection_rows]):
        flags.append("gateway_probe_selection_frame_invalid")
    if any(not is_non_bool_int(value) or value < 1 for value in ordinals[:selection_rows]):
        flags.append("gateway_probe_selection_ordinal_invalid")
    if ordinals[:selection_rows] != list(range(1, selection_rows + 1)):
        flags.append("gateway_probe_selection_ordinals_not_sequential")
    if any(is_non_bool_int(previous) and is_non_bool_int(current) and current <= previous
           for previous, current in zip(frames[:selection_rows], frames[1:selection_rows])):
        flags.append("gateway_probe_selection_frames_not_ordered")
    if selection_rows > 2:
        flags.append("gateway_probe_selection_count_exceeds_cap")

    # v40's accepted-build trace records type IDs and frames for all accepted
    # structures. The first Gateway rows must correspond one-for-one to the
    # bounded selection rows, using the same command frame.
    build_frames = _metadata_list(metadata, "accepted_build_frames")
    build_type_ids = _metadata_list(metadata, "accepted_build_type_ids")
    gateway_build_frames = [
        frame for frame, type_id in zip(build_frames, build_type_ids)
        if type_id == 160
    ]
    if selection_rows and (not build_frames or not build_type_ids):
        flags.append("gateway_probe_gateway_build_trace_missing")
    elif selection_rows and len(gateway_build_frames) < selection_rows:
        flags.append("gateway_probe_gateway_build_trace_incomplete")
    elif selection_rows:
        for index, frame in enumerate(frames[:selection_rows]):
            if gateway_build_frames[index] != frame:
                flags.append(f"gateway_probe_gateway_build_frame_mismatch_{index}")

    checks = {
        "required_fields": not missing and not invalid,
        "selection_arrays_aligned": "gateway_probe_selection_trace_length_mismatch" not in flags
        and "gateway_probe_selection_trace_incomplete" not in flags,
        "candidate_trace_partitioned": not any(flag.startswith("gateway_probe_candidate_trace") for flag in flags),
        "candidate_trace_complete": expected_candidates is not None and not any(
            flag.startswith("gateway_probe_candidate_trace") for flag in flags
        ),
        "untruncated": not any(flag.endswith("_truncated") for flag in flags),
        "reason_codes_legal": "gateway_probe_reason_code_invalid" not in flags,
        "nearest_distance_and_tie_break": not any(
            "nearest_distance_failure" in flag or "tie_break_failure" in flag for flag in flags
        ),
        "ordinal_frame_order": not any(
            flag.startswith("gateway_probe_selection_ordinal") or flag.startswith("gateway_probe_selection_frame")
            or flag == "gateway_probe_selection_frames_not_ordered" for flag in flags
        ),
        "accepted_gateway_alignment": not any(flag.startswith("gateway_probe_gateway_build") for flag in flags),
    }
    proof_sufficient = selection_rows >= 2 and not flags
    checks["two_selection_proof"] = proof_sufficient
    opportunity_notes = [] if selection_rows else ["gateway_probe_opportunity_unobserved"]
    grade = "review" if flags else "pass" if proof_sufficient else "untested"
    return {
        "generation": generation if generation in {"v40", "v41", "v42", "v43"} else "v40",
        "telemetry_status": "complete" if not missing and not invalid else "partial",
        "fields_present": [name for name in required if name in metadata],
        "missing_fields": missing, "invalid_fields": invalid,
        "selections": rows,
        "trace": {name: arrays[name] for name in required},
        "selection_count": selection_rows,
        "candidate_count": len(arrays["gateway_probe_candidate_ids"]),
        "proof_sufficient": proof_sufficient,
        "checks": checks,
        "review_flags": sorted(set(flags)),
        "opportunity_notes": opportunity_notes,
        "quantitative_grade": {"grade": grade, "score": 100 if grade in {"pass", "untested"} else 0,
                                "max_score": 100},
        "note": "v40 gateway-probe telemetry proves only the first two accepted public Gateway selections; it does not expose hidden state or prove causal strength.",
    }


def _diagnostic_summary(metadata: dict[str, object], root: Path, opponent_race: str | None = None,
                        candidate_name: object = None) -> dict[str, object]:
    generation = _diagnostic_generation(metadata, candidate_name)
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
    attempted = sum(_counter(categories, name, 0) for name in ("build", "train", "gather", "attack", "upgrade"))
    rejected_by_category = sum(_counter(categories, name, 1) for name in ("build", "train", "gather", "attack", "upgrade"))
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
            "second_zealot_train_frame": metadata.get("second_zealot_train_frame"),
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
    result["emergency_bridge"] = _emergency_bridge_summary(metadata, opponent_race, generation)
    result["telemetry_generation"] = generation
    result["construction_pending"] = _construction_pending_summary(metadata, opponent_race, generation)
    result["probe_reserve"] = _probe_reserve_summary(metadata, opponent_race, generation)
    result["zerg_offense_stage"] = _zerg_offense_stage_summary(metadata, opponent_race, generation)
    result["scaling"] = _scaling_summary(metadata, generation)
    result["shared_target"] = _shared_target_summary(metadata, opponent_race, generation)
    result["gateway_probe"] = _gateway_probe_summary(metadata, generation)
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


def _header_players(parsed: dict[str, object]) -> list[dict[str, object]]:
    header = parsed.get("header")
    players = header.get("Players") if isinstance(header, dict) else None
    return [player for player in players if isinstance(player, dict)] if isinstance(players, list) else []


def _player_names(player: dict[str, object], candidate_name: str | None = None) -> list[str]:
    names: list[str] = []
    for value in (
        player.get("name"),
        (player.get("environment") or {}).get("BWAPI_CONFIG_AUTO_MENU__CHARACTER_NAME")
        if isinstance(player.get("environment"), dict) else None,
        (player.get("result_metadata") or {}).get("bot")
        if isinstance(player.get("result_metadata"), dict) else None,
        candidate_name,
    ):
        if isinstance(value, str) and value and value not in names:
            names.append(value)
    return names


def _resolve_replay_command_owner(parsed: dict[str, object], process_player: object,
                                  all_players: list[object], candidate_name: str) -> dict[str, object]:
    """Resolve a process player's screp PlayerID only from verified evidence."""
    headers = _header_players(parsed)
    if not isinstance(process_player, dict):
        return {"status": "unresolved", "reason": "process_player_missing", "player_id": None}
    if not headers:
        return {"status": "unresolved", "reason": "replay_header_players_missing", "player_id": None}

    metadata = process_player.get("result_metadata") if isinstance(process_player.get("result_metadata"), dict) else {}
    is_candidate = process_player.get("name") == candidate_name or metadata.get("bot") == candidate_name
    names = _player_names(process_player, candidate_name if is_candidate else None)
    exact = [header for header in headers if isinstance(header.get("Name"), str) and header.get("Name") in names]
    if len(exact) == 1:
        owner = exact[0]
        owner_id = owner.get("ID")
        if isinstance(owner_id, int) and not isinstance(owner_id, bool):
            return {
                "status": "resolved_exact_name",
                "method": "exact_process_name",
                "player_id": owner_id,
                "header_name": owner.get("Name"),
            }
        return {"status": "unresolved", "reason": "header_player_id_invalid", "player_id": None}
    if len(exact) > 1:
        return {"status": "unresolved", "reason": "process_name_ambiguous", "player_id": None}

    return {"status": "unresolved", "reason": "no_verified_header_owner", "player_id": None}


def score_kestrel_match(manifest: dict[str, object], manifest_path: Path, screp: Path,
                        candidate_name: str = "Kestrel", candidate_sha: str | None = None,
                        root: Path | None = None, record: dict[str, object] | None = None) -> dict[str, object]:
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
        "opponent": (opponent_player.get("name") if isinstance(opponent_player, dict) else None)
                     or (record.get("opponent") if isinstance(record, dict) else None),
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
    diagnostic = _diagnostic_summary(diagnostic_metadata, root, opponent_race, candidate_name)
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
        "construction_pending": diagnostic["construction_pending"],
        "probe_reserve": diagnostic["probe_reserve"],
        "zerg_offense_stage": diagnostic["zerg_offense_stage"],
        "gateway_probe": diagnostic["gateway_probe"],
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
        process_player = next((p for p in players if isinstance(p, dict) and p.get("player") == replay.get("player")), None)
        owner = _resolve_replay_command_owner(parsed, process_player, players, candidate_name)
        parsed["command_owner_resolution"] = owner
        parsed_replays.append(parsed)
    candidate_parsed = next((p for p in parsed_replays if p.get("player") == candidate_player), None)
    if candidate_replay is not None and candidate_parsed is not None:
        owner = candidate_parsed.get("command_owner_resolution") or {"status": "unresolved", "reason": "owner_resolution_missing", "player_id": None}
        game["candidate_replay_owner_resolution"] = owner
        game["replay_whole"] = candidate_parsed
        filtered = None
        if owner.get("status", "").startswith("resolved") and isinstance(owner.get("player_id"), int):
            try:
                filtered = parse_replay(_resolve_path(candidate_replay.get("path"), root), screp,
                                        player_id=owner["player_id"])
            except TypeError as error:
                # Keep old tests/callers that replace parse_replay with a
                # legacy two-argument stub. Never fall back to whole-replay
                # heuristic counts when filtering is unavailable.
                if "player_id" not in str(error):
                    raise
                owner = {**owner, "status": "unresolved", "reason": "filtered_parser_unsupported", "player_id": None}
                game["candidate_replay_owner_resolution"] = owner
        game["replay"] = filtered or dict(candidate_parsed)
        if filtered is not None:
            for key in ("manifest_sha256", "manifest_size_bytes", "manifest_hash_matches", "manifest_size_matches", "player"):
                if key in candidate_parsed:
                    game["replay"][key] = candidate_parsed[key]
        if filtered is None:
            game["replay"]["heuristic_status"] = "owner_unresolved"
            game["replay"]["heuristic_grade"] = None
            game["replay"]["heuristic_score"] = None
            game["replay"]["signals"] = None
            game["replay"]["first_frames"] = None
            game["replay"]["attack_orders"] = None
            game["replay"]["harvest_orders"] = None
            game["replay"]["build_units"] = None
            game["replay"]["production_units"] = None
        else:
            game["replay"]["heuristic_status"] = "owner_filtered"
            game["replay"]["command_owner_resolution"] = owner
        game["replay_fidelity"] = _replay_fidelity(candidate_parsed, candidate_replay, diagnostic)
        # Preserve the old command-derived fields at the game level.
        for key in ("heuristic_grade", "heuristic_score", "signals", "first_frames", "attack_orders", "harvest_orders", "build_units", "production_units"):
            if key in game["replay"] and game["replay"][key] is not None:
                game[key] = game["replay"][key]
    else:
        game["error"] = "candidate_replay_missing"
        game["replay_fidelity"] = {"exists": False, "hash_matches": False, "screp_parse_ok": False, "parse_errors_ok": False}
    game["replays"] = [{
        "player": replay.get("player"),
        "path": parsed.get("path"),
        "command_owner_resolution": parsed.get("command_owner_resolution"),
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
    if (diagnostic.get("construction_pending") or {}).get("review_flags"): integrity_reasons.append("construction_mechanism_review")
    if (diagnostic.get("probe_reserve") or {}).get("review_flags"): integrity_reasons.append("probe_reserve_review")
    if (diagnostic.get("zerg_offense_stage") or {}).get("review_flags"): integrity_reasons.append("zerg_offense_stage_review")
    if (diagnostic.get("scaling") or {}).get("review_flags"): integrity_reasons.append("scaling_review")
    if (diagnostic.get("shared_target") or {}).get("review_flags"): integrity_reasons.append("shared_target_review")
    if (diagnostic.get("gateway_probe") or {}).get("review_flags"): integrity_reasons.append("gateway_probe_review")
    if not candidate_parsed: integrity_reasons.append("candidate_replay_missing")
    if candidate_parsed and not candidate_parsed.get("manifest_hash_matches"): integrity_reasons.append("candidate_replay_hash")
    if any(not item["fidelity"].get("hash_matches") for item in game["replays"]): integrity_reasons.append("replay_hash")
    if any(not item["fidelity"].get("screp_parse_ok") or not item["fidelity"].get("parse_errors_ok") for item in game["replays"]): integrity_reasons.append("replay_parse")
    if isinstance(candidate_parsed, dict) and "header_players" in candidate_parsed and (candidate_parsed.get("command_owner_resolution") or {}).get("status") != "resolved_exact_name":
        integrity_reasons.append("candidate_replay_owner_unresolved")
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
    game["scaling"] = diagnostic["scaling"]
    game["shared_target"] = diagnostic["shared_target"]
    return game


def parse_replay(path: Path, screp: Path, player_id: int | None = None) -> dict[str, object]:
    """Parse a replay, optionally restricting command-derived signals to one screp PlayerID.

    The parser always records whole-replay parse integrity. ``player_id`` only
    affects command-derived counters and is intentionally an exact integer
    match; callers must resolve it from replay-header evidence first.
    """
    result: dict[str, object] = {
        "path": str(path),
        "sha256": sha256(path) if path.is_file() else None,
        "size_bytes": path.stat().st_size if path.is_file() else None,
        "exists": path.is_file(),
        "json_valid": False,
        "command_owner_id": player_id,
        "command_filter_status": "whole_replay" if player_id is None else "requested",
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
    result["header"] = header if isinstance(header, dict) else None
    result["header_players"] = header.get("Players") if isinstance(header, dict) and isinstance(header.get("Players"), list) else None
    result["frames"] = header.get("Frames") if isinstance(header, dict) else None
    result["parse_error_commands"] = parse_errors
    result["whole_replay_command_count"] = len(rows)
    result["whole_replay_parse_error_commands"] = parse_errors
    selected_rows = rows if player_id is None else [row for row in rows if isinstance(row, dict) and row.get("PlayerID") == player_id]
    result["filtered_command_count"] = len(selected_rows)
    result["command_count"] = len(selected_rows)
    result["command_filter_status"] = "whole_replay" if player_id is None else "filtered"
    type_counts: dict[str, int] = {}
    order_counts: dict[str, int] = {}
    build_units: list[str] = []
    morph_units: list[str] = []
    first_frames: dict[str, int | None] = {"build": None, "production": None, "attack": None, "harvest": None}
    for row in selected_rows:
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


def _aggregate_gateway_probe(gateway_probe_games: list[dict[str, object]]) -> dict[str, object]:
    """Aggregate v40 proof without collapsing per-game review flags."""
    review_flags: dict[str, int] = {}
    opportunity_notes: dict[str, int] = {}
    aggregate: dict[str, object] = {
        "games": len(gateway_probe_games),
        "generations": {generation: sum(item.get("generation") == generation for item in gateway_probe_games)
                         for generation in ("v40", "v41", "v42", "v43", "legacy_absent")},
        "grades": {grade: sum((item.get("quantitative_grade") or {}).get("grade") == grade
                               for item in gateway_probe_games)
                   for grade in ("pass", "untested", "review", "legacy_absent")},
        "selection_rows": sum(item.get("selection_count", 0) for item in gateway_probe_games),
        "complete_two_selection_games": sum(item.get("proof_sufficient") is True for item in gateway_probe_games),
        "untruncated_games": sum((item.get("checks") or {}).get("untruncated") is True
                                  for item in gateway_probe_games),
        "nearest_tie_break_passes": sum((item.get("checks") or {}).get("nearest_distance_and_tie_break") is True
                                         for item in gateway_probe_games),
        "review_flags": review_flags,
        "opportunity_notes": opportunity_notes,
    }
    for item in gateway_probe_games:
        for flag in item.get("review_flags", []):
            review_flags[flag] = review_flags.get(flag, 0) + 1
        for note in item.get("opportunity_notes", []):
            opportunity_notes[note] = opportunity_notes.get(note, 0) + 1
    aggregate["review_flags"] = dict(sorted(review_flags.items()))
    aggregate["opportunity_notes"] = dict(sorted(opportunity_notes.items()))
    return aggregate


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
        game.update(score_kestrel_match(manifest, manifest_path, screp, candidate_name, candidate_sha, root, record))
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
    bridge_reason_counts = {"threat_clear": 0, "army_two": 0, "army_three": 0, "unknown": 0}
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
    episode_games = [
        (bridge.get("episodes") or {}) for bridge in bridge_games
        if isinstance(bridge.get("episodes"), dict) and (bridge.get("episodes") or {}).get("generation") in {"v35", "v36", "v37", "v38", "v40", "v41", "v42", "v43"}
    ]
    aggregate["emergency_bridge"]["episodes"] = _aggregate_emergency_episode_summaries(episode_games)
    stage_games = [g.get("zerg_offense_stage") for g in games if isinstance(g.get("zerg_offense_stage"), dict)]
    stage_review_flags: dict[str, int] = {}
    stage_opportunity_notes: dict[str, int] = {}
    aggregate["zerg_offense_stage"] = {
        "games": len(stage_games),
        "generations": {generation: sum(stage.get("generation") == generation for stage in stage_games)
                         for generation in ("v34", "v35", "v36", "v37", "v38", "v40", "v41", "v42", "v43", "legacy")},
        "grades": {grade: sum((stage.get("quantitative_grade") or {}).get("grade") == grade for stage in stage_games)
                   for grade in ("pass", "untested", "review", "legacy_absent")},
        "threshold_observed": sum((stage.get("peak_surplus") or 0) >= 6 for stage in stage_games),
        "release_events": sum((stage.get("release") or {}).get("events", 0) for stage in stage_games),
        "pre_release_remote_blocks": sum((stage.get("remote_offense") or {}).get("pre_release_blocks", 0) for stage in stage_games),
        "pre_release_remote_attempts": sum((stage.get("remote_offense") or {}).get("pre_release_attempts", 0) for stage in stage_games),
        "pre_release_remote_accepts": sum((stage.get("remote_offense") or {}).get("pre_release_accepts", 0) for stage in stage_games),
        "post_release_remote_attempts": sum((stage.get("remote_offense") or {}).get("post_release_attempts", 0) for stage in stage_games),
        "post_release_remote_accepts": sum((stage.get("remote_offense") or {}).get("post_release_accepts", 0) for stage in stage_games),
        "home_move_attempts": sum((stage.get("home_moves") or {}).get("attempts", 0) for stage in stage_games),
        "home_move_accepts": sum((stage.get("home_moves") or {}).get("accepts", 0) for stage in stage_games),
        "non_zerg_sentinel_passes": sum((stage.get("checks") or {}).get("non_zerg_sentinels") is True for stage in stage_games),
        "opportunity_notes": dict(sorted(stage_opportunity_notes.items())),
        "review_flags": dict(sorted(stage_review_flags.items())),
    }
    for stage in stage_games:
        for flag in stage.get("review_flags", []):
            stage_review_flags[flag] = stage_review_flags.get(flag, 0) + 1
        for note in stage.get("opportunity_notes", []):
            stage_opportunity_notes[note] = stage_opportunity_notes.get(note, 0) + 1
    aggregate["zerg_offense_stage"]["opportunity_notes"] = dict(sorted(stage_opportunity_notes.items()))
    aggregate["zerg_offense_stage"]["review_flags"] = dict(sorted(stage_review_flags.items()))
    construction_games = [g.get("construction_pending") for g in games if isinstance(g.get("construction_pending"), dict)]
    construction_review_flags: dict[str, int] = {}
    aggregate["construction_pending"] = {
        "games": len(construction_games),
        "generations": {generation: sum(item.get("generation") == generation for item in construction_games)
                         for generation in ("v35", "v36", "v37", "v38", "v40", "v41", "v42", "v43", "legacy")},
        "grades": {grade: sum((item.get("quantitative_grade") or {}).get("grade") == grade for item in construction_games)
                   for grade in ("pass", "untested", "review", "legacy_absent")},
        "accepted_builds": sum(len((item.get("accepted_builds") or {}).get("rows", [])) for item in construction_games),
        "gateway_sequence_observed": sum((item.get("checks") or {}).get("gateway_sequence_observed") is True for item in construction_games),
        "review_flags": construction_review_flags,
    }
    for item in construction_games:
        for flag in item.get("review_flags", []):
            construction_review_flags[flag] = construction_review_flags.get(flag, 0) + 1
    aggregate["construction_pending"]["review_flags"] = dict(sorted(construction_review_flags.items()))
    reserve_games = [g.get("probe_reserve") for g in games if isinstance(g.get("probe_reserve"), dict)]
    reserve_review_flags: dict[str, int] = {}
    aggregate["probe_reserve"] = {
        "games": len(reserve_games),
        "generations": {generation: sum(item.get("generation") == generation for item in reserve_games)
                         for generation in ("v36", "v37", "v38", "v40", "v41", "v42", "v43", "legacy")},
        "grades": {grade: sum((item.get("quantitative_grade") or {}).get("grade") == grade for item in reserve_games)
                   for grade in ("pass", "untested", "review", "legacy_absent")},
        "reserve_blocks": sum((item.get("reserve_blocks") or {}).get("count", 0) for item in reserve_games),
        "accepted_probe_trains": sum(len(item.get("accepted_probe_train_frames", [])) for item in reserve_games),
        "review_flags": reserve_review_flags,
    }
    for item in reserve_games:
        for flag in item.get("review_flags", []):
            reserve_review_flags[flag] = reserve_review_flags.get(flag, 0) + 1
    aggregate["probe_reserve"]["review_flags"] = dict(sorted(reserve_review_flags.items()))
    scaling_games = [g.get("scaling") for g in games if isinstance(g.get("scaling"), dict)]
    scaling_review_flags: dict[str, int] = {}
    scaling_opportunity_notes: dict[str, int] = {}
    aggregate["scaling"] = {
        "games": len(scaling_games),
        "generations": {generation: sum(item.get("generation") == generation for item in scaling_games)
                         for generation in ("v37", "v38", "v40", "v41", "v42", "v43", "legacy_absent")},
        "grades": {grade: sum((item.get("quantitative_grade") or {}).get("grade") == grade for item in scaling_games)
                   for grade in ("pass", "partial", "untested", "review", "legacy_absent")},
        "eligible": sum((item.get("upgrade") or {}).get("range_upgrade_eligibility_frame", -1) >= 0 for item in scaling_games),
        "accepted": sum((item.get("upgrade") or {}).get("range_upgrade_accepted", 0) for item in scaling_games),
        "completed": sum((item.get("upgrade") or {}).get("range_upgrade_completions", 0) for item in scaling_games),
        "seventh_pylon_observed": sum((item.get("milestones") or {}).get("seventh_pylon", {}).get("accepted", -1) >= 0 for item in scaling_games),
        "fifth_gateway_observed": sum((item.get("milestones") or {}).get("fifth_gateway", {}).get("accepted", -1) >= 0 for item in scaling_games),
        "review_flags": scaling_review_flags,
        "opportunity_notes": scaling_opportunity_notes,
    }
    for item in scaling_games:
        for flag in item.get("review_flags", []):
            scaling_review_flags[flag] = scaling_review_flags.get(flag, 0) + 1
        for note in item.get("opportunity_notes", []):
            scaling_opportunity_notes[note] = scaling_opportunity_notes.get(note, 0) + 1
    aggregate["scaling"]["review_flags"] = dict(sorted(scaling_review_flags.items()))
    aggregate["scaling"]["opportunity_notes"] = dict(sorted(scaling_opportunity_notes.items()))
    shared_target_games = [g.get("shared_target") for g in games if isinstance(g.get("shared_target"), dict)]
    shared_target_review_flags: dict[str, int] = {}
    shared_target_opportunity_notes: dict[str, int] = {}
    aggregate["shared_target"] = {
        "games": len(shared_target_games),
        "generations": {generation: sum(item.get("generation") == generation for item in shared_target_games)
                         for generation in ("v38", "v40", "v41", "v42", "v43", "legacy_absent")},
        "grades": {grade: sum((item.get("quantitative_grade") or {}).get("grade") == grade for item in shared_target_games)
                   for grade in ("pass", "untested", "review", "legacy_absent")},
        "selections": sum((item.get("counters") or {}).get("shared_target_selections", 0) for item in shared_target_games),
        "attempts": sum((item.get("counters") or {}).get("shared_target_attempts", 0) for item in shared_target_games),
        "accepted": sum((item.get("counters") or {}).get("shared_target_accepted", 0) for item in shared_target_games),
        "shared_target_rejects": sum((item.get("counters") or {}).get("shared_target_rejects", 0) for item in shared_target_games),
        "shared_target_illegal_selections": sum((item.get("counters") or {}).get("shared_target_illegal_selections", 0) for item in shared_target_games),
        "shared_target_non_zerg_selections": sum((item.get("counters") or {}).get("shared_target_non_zerg_selections", 0) for item in shared_target_games),
        "switches": sum((item.get("counters") or {}).get("shared_target_switches", 0) for item in shared_target_games),
        "correction_opportunities": sum((item.get("counters") or {}).get("shared_target_correction_opportunities", 0) for item in shared_target_games),
        "multi_participant_selections": sum(item.get("multi_participant_selections", 0) for item in shared_target_games),
        "coordinated_accepted_selections": sum(item.get("coordinated_accepted_selections", 0) for item in shared_target_games),
        "max_participants": max((item.get("max_participants", 0) for item in shared_target_games), default=0),
        "review_flags": shared_target_review_flags,
        "opportunity_notes": shared_target_opportunity_notes,
    }
    for item in shared_target_games:
        for flag in item.get("review_flags", []):
            shared_target_review_flags[flag] = shared_target_review_flags.get(flag, 0) + 1
        for note in item.get("opportunity_notes", []):
            shared_target_opportunity_notes[note] = shared_target_opportunity_notes.get(note, 0) + 1
    aggregate["shared_target"]["review_flags"] = dict(sorted(shared_target_review_flags.items()))
    aggregate["shared_target"]["opportunity_notes"] = dict(sorted(shared_target_opportunity_notes.items()))
    gateway_probe_games = [g.get("gateway_probe") for g in games if isinstance(g.get("gateway_probe"), dict)]
    aggregate["gateway_probe"] = _aggregate_gateway_probe(gateway_probe_games)
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
