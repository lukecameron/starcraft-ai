#!/usr/bin/env python3
"""Validate one Kestrel Modular v1 telemetry record.

This is a diagnostic completeness scorecard, not an Elo scorer. It refuses
legacy Kestrel/v45-shaped records so modular telemetry cannot be mislabelled.
"""

import argparse
import json
from pathlib import Path


REQUIRED = (
    "telemetry_schema",
    "frame_count",
    "ended",
    "known_zerg",
    "command_count",
    "rejected_commands",
    "zerg_four_probe_pylon_accepted",
    "zerg_four_probe_pylon_accepted_frame",
    "zerg_four_probe_pylon_completed_probe_count",
    "zerg_four_probe_pylon_completed_frame",
    "first_pylon_accepted_frame",
    "accepted_probe_train_frames",
    "accepted_zealot_trains",
    "second_zealot_train_frame",
    "second_zealot_completed_frame",
    "reserve_active_frames",
    "reserve_active_minerals",
    "reserve_active_reserves",
    "reserve_block_frames",
    "reserve_block_minerals",
    "reserve_block_reserves",
    "reserve_block_pre_acceptance_flags",
    "construction_events",
    "command_categories",
)


def validate_record(record):
    issues = []
    mechanism_issues = []
    if not isinstance(record, dict):
        return {
            "schema": "kestrel-modular-v1", "complete": False,
            "mechanisms_pass": False, "decision": "diagnostic-only",
            "issues": ["record is not an object"], "mechanism_issues": [],
            "elo_eligible": False,
        }
    if record.get("telemetry_schema") != "kestrel-modular-v1":
        issues.append("telemetry_schema is not kestrel-modular-v1")
    for key in REQUIRED:
        if key not in record:
            issues.append(f"missing {key}")

    def is_int(value):
        return isinstance(value, int) and not isinstance(value, bool)

    def require_int(key, minimum=None):
        value = record.get(key)
        if not is_int(value) or (minimum is not None and value < minimum):
            issues.append(f"{key} is not a valid integer")

    for key in ("frame_count", "command_count", "rejected_commands", "accepted_zealot_trains"):
        require_int(key, 0)
    for key in (
        "zerg_four_probe_pylon_accepted_frame",
        "zerg_four_probe_pylon_completed_probe_count",
        "zerg_four_probe_pylon_completed_frame",
        "first_pylon_accepted_frame",
        "second_zealot_train_frame",
        "second_zealot_completed_frame",
    ):
        require_int(key, -1)
    for key in ("ended", "known_zerg", "zerg_four_probe_pylon_accepted"):
        if not isinstance(record.get(key), bool):
            issues.append(f"{key} is not boolean")

    array_names = (
        "accepted_probe_train_frames", "reserve_active_frames",
        "reserve_active_minerals", "reserve_active_reserves",
        "reserve_block_frames", "reserve_block_minerals",
        "reserve_block_reserves", "reserve_block_pre_acceptance_flags",
    )
    arrays = {}
    for key in array_names:
        value = record.get(key)
        if not isinstance(value, list) or any(not is_int(item) for item in value):
            issues.append(f"{key} is not an integer array")
            arrays[key] = []
        else:
            arrays[key] = value

    for frames, values, name in (
        (arrays["reserve_active_frames"], arrays["reserve_active_minerals"], "reserve_active"),
        (arrays["reserve_active_frames"], arrays["reserve_active_reserves"], "reserve_reserves"),
        (arrays["reserve_block_frames"], arrays["reserve_block_minerals"], "reserve_block"),
        (arrays["reserve_block_frames"], arrays["reserve_block_reserves"], "reserve_block_reserves"),
        (arrays["reserve_block_frames"], arrays["reserve_block_pre_acceptance_flags"], "reserve_flags"),
    ):
        if len(frames) != len(values):
            issues.append(f"{name} frame/value lengths differ")

    categories = record.get("command_categories", {})
    if not isinstance(categories, dict):
        issues.append("command_categories is not an object")
        categories = {}
    attempted_total = rejected_total = 0
    for category in ("build", "train", "gather", "attack", "scout"):
        entry = categories.get(category)
        if not isinstance(entry, dict):
            issues.append(f"missing command category {category}")
            continue
        attempted = entry.get("attempted")
        rejected = entry.get("rejected")
        if not is_int(attempted) or not is_int(rejected) or attempted < 0 or rejected < 0 or rejected > attempted:
            issues.append(f"invalid command category {category}")
            continue
        attempted_total += attempted
        rejected_total += rejected
    if is_int(record.get("command_count")) and attempted_total != record["command_count"]:
        issues.append("command category attempts do not sum to command_count")
    if is_int(record.get("rejected_commands")) and rejected_total != record["rejected_commands"]:
        issues.append("command category rejections do not sum to rejected_commands")

    probe_frames = arrays["accepted_probe_train_frames"]
    if any(frame < 0 for frame in probe_frames) or probe_frames != sorted(probe_frames):
        issues.append("accepted Probe train frames are invalid or unordered")

    if record.get("zerg_four_probe_pylon_accepted"):
        accepted_frame = record.get("zerg_four_probe_pylon_accepted_frame")
        accepted_frame = accepted_frame if is_int(accepted_frame) else -1
        completed_frame = record.get("zerg_four_probe_pylon_completed_frame")
        completed_frame = completed_frame if is_int(completed_frame) else -1
        if accepted_frame < 0:
            issues.append("accepted four-Probe Pylon has no accepted frame")
        if record.get("zerg_four_probe_pylon_completed_probe_count") != 4:
            issues.append("accepted four-Probe Pylon did not have exactly four completed Probes")
        first_pylon = record.get("first_pylon_accepted_frame")
        if first_pylon != record.get("zerg_four_probe_pylon_accepted_frame"):
            issues.append("four-Probe and first-Pylon acceptance frames differ")
        if completed_frame >= 0 and completed_frame < accepted_frame:
            issues.append("four-Probe Pylon completion precedes acceptance")
        if any(frame <= accepted_frame for frame in probe_frames):
            issues.append("a Probe train was accepted before the four-Probe Pylon")

    if record.get("known_zerg"):
        if not record.get("zerg_four_probe_pylon_accepted"):
            mechanism_issues.append("Zerg four-Probe Pylon mechanism was not exercised successfully")
    elif record.get("zerg_four_probe_pylon_accepted"):
        issues.append("non-Zerg record reports Zerg four-Probe Pylon acceptance")

    second_train = record.get("second_zealot_train_frame")
    second_train = second_train if is_int(second_train) else -1
    second_complete = record.get("second_zealot_completed_frame")
    second_complete = second_complete if is_int(second_complete) else -1
    if is_int(record.get("accepted_zealot_trains")) and record["accepted_zealot_trains"] >= 2 and second_train < 0:
        issues.append("two accepted Zealots have no second train frame")
    if second_complete >= 0 and (second_train < 0 or second_complete < second_train):
        issues.append("second Zealot completion is not ordered after its train frame")

    active = list(zip(arrays["reserve_active_frames"], arrays["reserve_active_minerals"], arrays["reserve_active_reserves"]))
    blocks = list(zip(arrays["reserve_block_frames"], arrays["reserve_block_minerals"],
                      arrays["reserve_block_reserves"], arrays["reserve_block_pre_acceptance_flags"]))
    if arrays["reserve_active_frames"] != sorted(arrays["reserve_active_frames"]):
        issues.append("reserve-active frames are unordered")
    if arrays["reserve_block_frames"] != sorted(arrays["reserve_block_frames"]):
        issues.append("reserve-block frames are unordered")
    for frame, minerals, reserve in active:
        if frame < 0 or minerals < 0 or reserve <= 0:
            issues.append("invalid reserve-active sample")
            break
    for frame, minerals, reserve, pre_acceptance in blocks:
        if frame < 0 or minerals < 50 or minerals >= 50 + reserve or reserve <= 0 or pre_acceptance not in (0, 1):
            issues.append("invalid reserve-block sample")
            break
        if (frame, minerals, reserve) not in active:
            issues.append("reserve block is not an active eligible-Nexus sample")
            break
        if second_train >= 0 and ((frame < second_train) != bool(pre_acceptance)):
            issues.append("reserve-block acceptance flag is not order-aware")
            break
        if second_train < 0 and pre_acceptance != 1:
            issues.append("reserve block is marked post-acceptance without a second Zealot train")
            break

    events = record.get("construction_events")
    if not isinstance(events, list):
        issues.append("construction_events is not an array")
        events = []
    last_accepted = -1
    for event in events:
        if not isinstance(event, dict):
            issues.append("construction event is not an object")
            continue
        values = [event.get(key) for key in ("type_id", "baseline", "accepted_frame", "current_frame", "completed_frame")]
        if any(not is_int(value) for value in values):
            issues.append("construction event has non-integer fields")
            continue
        type_id, baseline, accepted, current, completed = values
        if type_id < 0 or baseline < 0 or accepted < 0 or accepted < last_accepted:
            issues.append("construction event identity or acceptance ordering is invalid")
        if current >= 0 and current < accepted:
            issues.append("construction current frame precedes acceptance")
        if completed >= 0 and (current < 0 or completed < current):
            issues.append("construction completion is not ordered after current")
        last_accepted = accepted

    if record.get("ended") is not True:
        mechanism_issues.append("final ended telemetry was not observed")
    if is_int(record.get("rejected_commands")) and record["rejected_commands"] != 0:
        mechanism_issues.append("one or more BWAPI commands were rejected")
    if record.get("known_zerg") and not active:
        mechanism_issues.append("eligible-Nexus reserve activity was not exercised")
    if record.get("known_zerg") and not blocks:
        mechanism_issues.append("eligible-Nexus reserve blocking was not exercised")
    if not events:
        mechanism_issues.append("construction lifecycle was not exercised")
    elif any(event.get("current_frame", -1) < 0 or event.get("completed_frame", -1) < 0
             for event in events if isinstance(event, dict)):
        mechanism_issues.append("one or more construction events did not complete")

    complete = not issues
    return {
        "schema": "kestrel-modular-v1",
        "complete": complete,
        "mechanisms_pass": complete and not mechanism_issues,
        "decision": "diagnostic-only",
        "issues": issues,
        "mechanism_issues": mechanism_issues,
        "elo_eligible": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("telemetry", type=Path)
    args = parser.parse_args()
    result = validate_record(json.loads(args.telemetry.read_text()))
    print(json.dumps(result, sort_keys=True))
    return 0 if result["complete"] and result["mechanisms_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
