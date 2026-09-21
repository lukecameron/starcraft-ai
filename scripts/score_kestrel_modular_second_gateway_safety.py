#!/usr/bin/env python3
"""Score the Kestrel Modular known-Zerg second-Gateway safety gate.

This candidate-specific diagnostic score composes the registered modular
leash-hysteresis score with the frozen public-self-state ordering rule. It is
not a replay-integrity or Elo scorer.
"""

import argparse
import json
from pathlib import Path

try:
    from scripts.score_kestrel_modular_leash_hysteresis import (
        validate_leash_hysteresis_record,
    )
except ModuleNotFoundError:
    from score_kestrel_modular_leash_hysteresis import validate_leash_hysteresis_record


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def validate_second_gateway_safety_evidence(record):
    """Return structural and mechanism issues for the frozen ordering gate."""

    issues = []
    mechanism_issues = []
    if not isinstance(record, dict):
        return ["telemetry is not an object"], []

    if record.get("known_zerg") is not True:
        mechanism_issues.append("known-Zerg observation was not recorded")

    accepted_trains = record.get("accepted_zealot_trains")
    if not _is_int(accepted_trains) or accepted_trains < 0:
        issues.append("accepted_zealot_trains is not a nonnegative integer")
    elif accepted_trains < 2:
        mechanism_issues.append("two Zealot trains were not accepted")

    second_completed = record.get("second_zealot_completed_frame")
    if not _is_int(second_completed):
        issues.append("second_zealot_completed_frame is not an integer")
    elif second_completed < 0:
        mechanism_issues.append("second completed Zealot was not observed")

    max_zealots = record.get("max_zealots")
    if not _is_int(max_zealots) or max_zealots < 0:
        issues.append("max_zealots is not a nonnegative integer")
    elif max_zealots < 2:
        mechanism_issues.append("two completed Zealots did not overlap")

    second_gateway = record.get("second_gateway_accepted_frame")
    if not _is_int(second_gateway):
        issues.append("second_gateway_accepted_frame is not an integer")
    elif second_gateway >= 0 and _is_int(second_completed) and second_completed >= 0:
        if second_gateway < second_completed:
            mechanism_issues.append(
                "second Gateway was accepted before the second Zealot completion"
            )
    elif second_gateway >= 0:
        issues.append(
            "second Gateway acceptance is present without a valid completion frame"
        )

    hold_release = record.get("lone_zealot_hold_release_frame")
    if not _is_int(hold_release):
        issues.append("lone_zealot_hold_release_frame is not an integer")
    elif hold_release < 0:
        mechanism_issues.append("lone-Zealot hold did not release")
    elif (
        hold_release >= 0
        and _is_int(second_completed)
        and second_completed >= 0
        and hold_release != second_completed
    ):
        mechanism_issues.append("hold release does not equal second completion")

    return issues, mechanism_issues


def validate_record(record):
    base = validate_leash_hysteresis_record(record)
    ordering_issues, ordering_mechanism_issues = validate_second_gateway_safety_evidence(record)
    issues = list(base["issues"]) + ordering_issues
    mechanism_issues = list(base["mechanism_issues"]) + ordering_mechanism_issues
    complete = not issues
    return {
        **base,
        "complete": complete,
        "mechanisms_pass": complete and not mechanism_issues,
        "decision": "pass-to-five-game-screen" if complete and not mechanism_issues else "reject",
        "issues": issues,
        "mechanism_issues": mechanism_issues,
        "candidate_gate": "second-gateway-safety",
        "second_gateway_censoring": (
            "An absent second_gateway_accepted_frame (-1) is an acceptable censored "
            "observation through the fixed row's end; it does not establish a later "
            "non-request."
        ),
        "elo_eligible": False,
    }


score_record = validate_record
validate_record_for_candidate = validate_record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("telemetry", type=Path)
    args = parser.parse_args()
    result = validate_record(json.loads(args.telemetry.read_text()))
    print(json.dumps(result, sort_keys=True))
    return 0 if result["complete"] and result["mechanisms_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
