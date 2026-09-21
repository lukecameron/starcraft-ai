#!/usr/bin/env python3
"""Validate the public-state lone-Zealot hold in Kestrel Modular telemetry."""

import argparse
import json
from pathlib import Path

try:
    from scripts.score_kestrel_modular_recovery import validate_recovery_record
except ModuleNotFoundError:
    from score_kestrel_modular_recovery import validate_recovery_record


NONNEGATIVE_FIELDS = (
    "lone_zealot_hold_active_samples",
    "lone_zealot_hold_suppression_samples",
    "lone_zealot_hold_unique_units",
    "lone_zealot_hold_home_move_attempts",
    "lone_zealot_hold_home_move_accepted",
)


def validate_hold_evidence(record):
    issues = []
    mechanism_issues = []
    if not isinstance(record, dict):
        return ["telemetry is not an object"], []

    for key in NONNEGATIVE_FIELDS:
        value = record.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            issues.append(f"{key} is not a nonnegative integer")

    release = record.get("lone_zealot_hold_release_frame")
    if not isinstance(release, int) or isinstance(release, bool) or release < -1:
        issues.append("lone_zealot_hold_release_frame is not an integer at least -1")

    attempts = record.get("lone_zealot_hold_home_move_attempts")
    accepted = record.get("lone_zealot_hold_home_move_accepted")
    if (isinstance(attempts, int) and not isinstance(attempts, bool)
            and isinstance(accepted, int) and not isinstance(accepted, bool)
            and accepted > attempts):
        issues.append("accepted lone-hold home moves exceed attempts")

    if record.get("known_zerg") is True:
        active = record.get("lone_zealot_hold_active_samples")
        suppressions = record.get("lone_zealot_hold_suppression_samples")
        unique = record.get("lone_zealot_hold_unique_units")
        second_complete = record.get("second_zealot_completed_frame")
        if not isinstance(active, int) or isinstance(active, bool) or active <= 0:
            mechanism_issues.append("lone-Zealot hold was not active")
        if not isinstance(suppressions, int) or isinstance(suppressions, bool) or suppressions <= 0:
            mechanism_issues.append("no lone-Zealot target suppression was observed")
        if not isinstance(unique, int) or isinstance(unique, bool) or unique <= 0:
            mechanism_issues.append("no completed Zealot exercised the hold")
        if not isinstance(second_complete, int) or isinstance(second_complete, bool) or second_complete < 0:
            mechanism_issues.append("second completed Zealot did not release the hold")
        elif release != second_complete:
            mechanism_issues.append("hold release does not match the second-Zealot completion frame")

    return issues, mechanism_issues


def validate_hold_record(record):
    result = validate_recovery_record(record)
    issues = list(result["issues"])
    mechanism_issues = list(result["mechanism_issues"])
    hold_issues, hold_mechanism_issues = validate_hold_evidence(record)
    issues.extend(hold_issues)
    mechanism_issues.extend(hold_mechanism_issues)
    complete = not issues
    return {
        **result,
        "complete": complete,
        "mechanisms_pass": complete and not mechanism_issues,
        "issues": issues,
        "mechanism_issues": mechanism_issues,
        "recovery_gate": "lone-zealot-hold",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("telemetry", type=Path)
    args = parser.parse_args()
    result = validate_hold_record(json.loads(args.telemetry.read_text()))
    print(json.dumps(result, sort_keys=True))
    return 0 if result["complete"] and result["mechanisms_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
