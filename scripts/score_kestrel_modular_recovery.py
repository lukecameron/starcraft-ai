#!/usr/bin/env python3
"""Validate commandability evidence for a Kestrel Modular recovery build."""

import argparse
import json
from pathlib import Path

try:
    from scripts.score_kestrel_modular_v1 import validate_record
except ModuleNotFoundError:
    from score_kestrel_modular_v1 import validate_record


WORKER_FIELDS = (
    "worker_gather_preflight_skips",
    "worker_cargo_deferrals",
    "worker_accepted_gather_commands",
    "worker_builder_preflight_skips",
    "worker_builder_cargo_deferrals",
)


def validate_recovery_record(record):
    result = validate_record(record)
    issues = list(result["issues"])
    mechanism_issues = list(result["mechanism_issues"])

    for key in WORKER_FIELDS:
        value = record.get(key) if isinstance(record, dict) else None
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            issues.append(f"{key} is not a nonnegative integer")

    categories = record.get("command_categories", {}) if isinstance(record, dict) else {}
    gather = categories.get("gather", {}) if isinstance(categories, dict) else {}
    attempted = gather.get("attempted") if isinstance(gather, dict) else None
    rejected = gather.get("rejected") if isinstance(gather, dict) else None
    accepted = record.get("worker_accepted_gather_commands") if isinstance(record, dict) else None
    if all(isinstance(value, int) and not isinstance(value, bool)
           for value in (attempted, rejected, accepted)):
        if accepted != attempted - rejected:
            issues.append("worker accepted gather count does not reconcile with command accounting")
        if accepted == 0:
            mechanism_issues.append("no gather assignment was accepted")

    build = categories.get("build", {}) if isinstance(categories, dict) else {}
    build_attempted = build.get("attempted") if isinstance(build, dict) else None
    build_rejected = build.get("rejected") if isinstance(build, dict) else None
    events = record.get("construction_events") if isinstance(record, dict) else None
    if (isinstance(build_attempted, int) and not isinstance(build_attempted, bool)
            and isinstance(build_rejected, int) and not isinstance(build_rejected, bool)
            and isinstance(events, list)):
        accepted_builds = build_attempted - build_rejected
        if len(events) != accepted_builds:
            issues.append("construction events do not reconcile with accepted build commands")
        if accepted_builds == 0:
            mechanism_issues.append("no build command was accepted")

    complete = not issues
    return {
        **result,
        "complete": complete,
        "mechanisms_pass": complete and not mechanism_issues,
        "issues": issues,
        "mechanism_issues": mechanism_issues,
        "recovery_gate": "gather-commandability",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("telemetry", type=Path)
    args = parser.parse_args()
    result = validate_recovery_record(json.loads(args.telemetry.read_text()))
    print(json.dumps(result, sort_keys=True))
    return 0 if result["complete"] and result["mechanisms_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
