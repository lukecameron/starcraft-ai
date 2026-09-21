#!/usr/bin/env python3
"""Score the Kestrel Modular lone-Zealot leash-hysteresis diagnostic.

This is a candidate-specific mechanism score.  It consumes the bot's
diagnostic JSON and reuses the generic modular validator for structural
reconciliation.  Replay parsing, replay-to-callback matching, terminal
integrity, and other match-validity gates are deliberately separate and are
not established by this scorer.  A mechanism pass is therefore not Elo
evidence and does not make a replay-valid match.
"""

import argparse
import json
from pathlib import Path

try:
    from scripts.score_kestrel_modular_v1 import validate_record as _validate_generic_record
except ModuleNotFoundError:  # Running this file directly from scripts/.
    from score_kestrel_modular_v1 import validate_record as _validate_generic_record


SCHEMA = "kestrel-modular-v1"
LEASH_RADIUS = 96
LEASH_RETURN_RADIUS = 48
CLOSE_THREAT_RADIUS = 160

# The first names are the telemetry convention for this candidate.  The
# aliases keep the scorer readable against diagnostic fixtures produced while
# the C++ field was being named; a record still has to provide one complete
# entry/active/release triplet.
RETURN_COUNTER_FIELDS = {
    "entry": (
        "lone_zealot_hold_return_entries",
        "lone_zealot_hold_leash_return_entry_samples",
    ),
    "active": (
        "lone_zealot_hold_return_active_samples",
        "lone_zealot_hold_leash_return_active_samples",
    ),
    "release": (
        "lone_zealot_hold_return_releases",
        "lone_zealot_hold_leash_return_release_samples",
    ),
}
RETURN_RADIUS_FIELDS = (
    "lone_zealot_hold_leash_return_release_radius",
    "lone_zealot_hold_return_release_radius",
)


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _first_present(record, names):
    for name in names:
        if name in record:
            return name, record[name]
    return None, None


def _positive_counter(record, names, label, issues, mechanism_issues):
    name, value = _first_present(record, names)
    if name is None:
        issues.append(f"missing {names[0]}")
        return None
    if not _is_int(value) or value < 0:
        issues.append(f"{name} is not a nonnegative integer")
        return None
    if value <= 0:
        mechanism_issues.append(f"{label} was not observed")
    return value


def validate_leash_hysteresis_evidence(record):
    """Return ``(structural_issues, mechanism_issues)`` for this candidate.

    Structural issues describe missing or malformed candidate telemetry.
    Mechanism issues describe a well-formed record that did not exercise the
    registered behavior.  The generic validator remains responsible for the
    detailed event/lifecycle reconciliation.
    """

    issues = []
    mechanism_issues = []
    if not isinstance(record, dict):
        return ["telemetry is not an object"], []

    if record.get("telemetry_schema") != SCHEMA:
        issues.append(f"telemetry_schema is not {SCHEMA}")

    if record.get("known_zerg") is not True:
        mechanism_issues.append("known-Zerg hold was not active")

    for key, label in (
        ("lone_zealot_hold_active_samples", "lone-Zealot hold activity"),
        ("lone_zealot_hold_suppression_samples", "lone-Zealot suppression"),
        ("lone_zealot_hold_unique_units", "held Zealot participation"),
    ):
        value = record.get(key)
        if not _is_int(value) or value < 0:
            issues.append(f"{key} is not a nonnegative integer")
        elif value <= 0:
            mechanism_issues.append(f"{label} was not observed")

    _positive_counter(
        record, RETURN_COUNTER_FIELDS["entry"], "leash return entry", issues, mechanism_issues
    )
    _positive_counter(
        record, RETURN_COUNTER_FIELDS["active"], "leash return active state", issues, mechanism_issues
    )
    _positive_counter(
        record, RETURN_COUNTER_FIELDS["release"], "leash return release", issues, mechanism_issues
    )

    radius = record.get("lone_zealot_hold_leash_radius")
    if not _is_int(radius):
        issues.append("lone_zealot_hold_leash_radius is not an integer")
    elif radius != LEASH_RADIUS:
        mechanism_issues.append(f"lone-Zealot leash radius must equal {LEASH_RADIUS}")

    return_radius_name, return_radius = _first_present(record, RETURN_RADIUS_FIELDS)
    if return_radius_name is None:
        issues.append(f"missing {RETURN_RADIUS_FIELDS[0]}")
    elif not _is_int(return_radius):
        issues.append(f"{return_radius_name} is not an integer")
    elif return_radius != LEASH_RETURN_RADIUS:
        mechanism_issues.append(
            f"leash return radius must equal {LEASH_RETURN_RADIUS}"
        )

    close_threat_radius = record.get("lone_zealot_hold_close_threat_radius")
    if not _is_int(close_threat_radius):
        issues.append("lone_zealot_hold_close_threat_radius is not an integer")
    elif close_threat_radius != CLOSE_THREAT_RADIUS:
        mechanism_issues.append(
            f"close-threat radius must equal {CLOSE_THREAT_RADIUS}"
        )

    leash_accepted = record.get("lone_zealot_hold_leash_move_accepted")
    if not _is_int(leash_accepted) or leash_accepted < 0:
        issues.append("lone_zealot_hold_leash_move_accepted is not a nonnegative integer")
    elif leash_accepted <= 0:
        mechanism_issues.append("no actually issued accepted leash move was observed")

    close_samples = record.get("lone_zealot_hold_close_threat_samples")
    close_accepted = record.get("lone_zealot_hold_close_threat_attack_accepted")
    if not _is_int(close_samples) or close_samples < 0:
        issues.append("lone_zealot_hold_close_threat_samples is not a nonnegative integer")
    elif close_samples <= 0:
        mechanism_issues.append("no close-threat sample was observed")
    if not _is_int(close_accepted) or close_accepted < 0:
        issues.append(
            "lone_zealot_hold_close_threat_attack_accepted is not a nonnegative integer"
        )
    elif close_accepted <= 0:
        mechanism_issues.append("no actually issued accepted close-threat attack was observed")

    rejected = record.get("rejected_commands")
    if not _is_int(rejected) or rejected < 0:
        issues.append("rejected_commands is not a nonnegative integer")
    elif rejected != 0:
        mechanism_issues.append("one or more BWAPI commands were rejected")

    error_counts = record.get("command_error_counts")
    if not isinstance(error_counts, dict):
        issues.append("command_error_counts is not an object")
    elif "unit_busy" not in error_counts:
        issues.append("missing command_error_counts.unit_busy")
    else:
        unit_busy = error_counts["unit_busy"]
        if not _is_int(unit_busy) or unit_busy < 0:
            issues.append("command_error_counts.unit_busy is not a nonnegative integer")
        elif unit_busy != 0:
            mechanism_issues.append("one or more Unit_Busy errors were recorded")

    origins_within = record.get("lone_zealot_hold_close_threat_attack_origins_within_leash")
    if origins_within is not True:
        if isinstance(origins_within, bool):
            mechanism_issues.append("close-threat attack origins were not all within the leash")
        else:
            issues.append(
                "lone_zealot_hold_close_threat_attack_origins_within_leash is not boolean"
            )

    accepted_trains = record.get("accepted_zealot_trains")
    second_complete = record.get("second_zealot_completed_frame")
    if not _is_int(accepted_trains) or accepted_trains < 0:
        issues.append("accepted_zealot_trains is not a nonnegative integer")
    elif accepted_trains < 2:
        mechanism_issues.append("two Zealot trains were not accepted")
    if not _is_int(second_complete):
        issues.append("second_zealot_completed_frame is not an integer")
    elif second_complete < 0:
        mechanism_issues.append("two completed Zealots were not observed")

    hold_release = record.get("lone_zealot_hold_release_frame")
    if not _is_int(hold_release):
        issues.append("lone_zealot_hold_release_frame is not an integer")
    elif hold_release < 0:
        mechanism_issues.append("lone-Zealot hold did not release")
    elif _is_int(second_complete) and second_complete >= 0 and hold_release != second_complete:
        mechanism_issues.append("hold release does not match the second-Zealot completion frame")

    return issues, mechanism_issues


def validate_leash_hysteresis_record(record):
    """Combine generic structural validation with candidate mechanism gates."""

    generic = _validate_generic_record(record)
    issues = list(generic["issues"])
    mechanism_issues = list(generic["mechanism_issues"])
    candidate_issues, candidate_mechanism_issues = validate_leash_hysteresis_evidence(record)
    issues.extend(candidate_issues)
    mechanism_issues.extend(candidate_mechanism_issues)
    complete = not issues
    mechanisms_pass = complete and not mechanism_issues
    return {
        **generic,
        "schema": SCHEMA,
        "complete": complete,
        "mechanisms_pass": mechanisms_pass,
        "decision": "pass-to-five-game-screen" if mechanisms_pass else "reject",
        "issues": issues,
        "mechanism_issues": mechanism_issues,
        "replay_integrity_gates_separate": True,
        "replay_integrity_separate": True,
        "replay_integrity_note": (
            "Replay parsing, terminal/result integrity, and replay-to-callback "
            "checks are separate evaluator gates; this diagnostic JSON score "
            "does not establish them."
        ),
        "elo_eligible": False,
        "candidate_gate": "lone-zealot-leash-hysteresis",
    }


# Short aliases make the public validator easy to discover while retaining a
# descriptive name for callers that score several modular candidates.
validate_record = validate_leash_hysteresis_record
validate_record_for_candidate = validate_leash_hysteresis_record
score_record = validate_leash_hysteresis_record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("telemetry", type=Path, help="diagnostic JSON emitted by the bot")
    args = parser.parse_args()
    result = validate_leash_hysteresis_record(json.loads(args.telemetry.read_text()))
    print(json.dumps(result, sort_keys=True))
    return 0 if result["complete"] and result["mechanisms_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
