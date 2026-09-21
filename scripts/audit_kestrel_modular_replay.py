#!/usr/bin/env python3
"""Audit one Kestrel Modular hold match and its archived replay copies.

This is an integrity/mechanism gate, not a strength scorer.  It deliberately
keeps the checks close to the registered replay gates: the manifest proves the
match lifecycle, screp proves the replay stream, and the candidate diagnostic
supplies the public callback evidence used to line up the hold commands.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any


ALLOWED_KILL_EVENTS = {
    ("controller_not_occupied_after_action", 87),
    ("transport_callback", -1),
}


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _resolve(path: object, root: Path) -> Path | None:
    if not isinstance(path, str) or not path:
        return None
    candidate = Path(path)
    return candidate if candidate.is_absolute() else (root / candidate).resolve()


def _int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _race(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip().lower()
    return {"zerg": "zerg", "terran": "terran", "protoss": "protoss", "toss": "protoss"}.get(value)


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w") as output:
        json.dump(value, output, indent=2, sort_keys=True)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


def _player_metadata(player: dict[str, Any]) -> dict[str, Any]:
    value = player.get("result_metadata")
    return value if isinstance(value, dict) else {}


def _player_names(player: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for value in (
        player.get("name"),
        (_player_metadata(player).get("bot")),
        (player.get("environment") or {}).get("BWAPI_CONFIG_AUTO_MENU__CHARACTER_NAME")
        if isinstance(player.get("environment"), dict) else None,
    ):
        if isinstance(value, str) and value:
            names.add(value)
    return names


def _players(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in manifest.get("players", []) if isinstance(item, dict)]


def _candidate(manifest: dict[str, Any], number: int) -> dict[str, Any] | None:
    return next((p for p in _players(manifest) if p.get("player") == number), None)


def _read_json(path: Path) -> tuple[Any, str | None]:
    try:
        return json.loads(path.read_text()), None
    except (OSError, json.JSONDecodeError) as error:
        return None, f"{type(error).__name__}: {error}"


def _kill_events(manifest: dict[str, Any], root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Collect kill_client diagnostics from manifest-provided event arrays/logs."""
    events: list[dict[str, Any]] = []
    issues: list[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("event") == "kill_client":
                events.append(value)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(manifest.get("terminal_events"))
    visit(manifest.get("terminal_kill_events"))
    for player in _players(manifest):
        stderr = player.get("stderr")
        log_path = _resolve(stderr.get("path"), root) if isinstance(stderr, dict) else None
        if not log_path or not log_path.is_file():
            continue
        try:
            lines = log_path.read_text().splitlines()
        except OSError as error:
            issues.append(f"terminal_log_read:{log_path}:{type(error).__name__}")
            continue
        for line in lines:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict) and row.get("event") == "kill_client":
                events.append(row)

    # Preserve order while avoiding duplicate events if both manifest and logs
    # retain the same diagnostic row.
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for event in events:
        key = json.dumps(event, sort_keys=True, separators=(",", ":"))
        if key not in seen:
            seen.add(key)
            unique.append(event)
        source = event.get("source")
        action_id = event.get("action_id")
        valid = (source, action_id) in ALLOWED_KILL_EVENTS
        if not valid:
            issues.append(f"terminal_kill_event_not_allowed:{source}/{action_id}")
    return unique, sorted(set(issues))


def _screp(path: Path, screp: Path) -> dict[str, Any]:
    """Run screp once and retain raw command rows for mechanism checks."""
    result: dict[str, Any] = {
        "path": str(path),
        "exists": path.is_file(),
        "sha256": sha256(path),
        "size_bytes": path.stat().st_size if path.is_file() else None,
        "screp_exit_code": None,
        "json_valid": False,
        "parse_error_commands": None,
        "header": None,
        "header_players": [],
        "frames": None,
        "commands": [],
    }
    if not path.is_file():
        return result
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json") as output:
        try:
            completed = subprocess.run(
                [str(screp), "-cmds=true", "-computed=true", "-map=false", "-indent=false", str(path)],
                stdout=output, stderr=subprocess.PIPE, text=True, check=False,
            )
        except OSError as error:
            result["stderr"] = f"{type(error).__name__}: {error}"
            result["screp_exit_code"] = -1
            return result
        output.seek(0)
        try:
            parsed = json.load(output) if completed.returncode == 0 else None
        except json.JSONDecodeError:
            parsed = None
    result["screp_exit_code"] = completed.returncode
    result["stderr"] = completed.stderr[-2000:]
    result["json_valid"] = isinstance(parsed, dict)
    header = parsed.get("Header") if isinstance(parsed, dict) else None
    commands = parsed.get("Commands") if isinstance(parsed, dict) else None
    rows = commands.get("Cmds") if isinstance(commands, dict) else None
    parse_errors = commands.get("ParseErrCmds") if isinstance(commands, dict) else None
    result["header"] = header if isinstance(header, dict) else None
    result["header_players"] = header.get("Players", []) if isinstance(header, dict) and isinstance(header.get("Players"), list) else []
    result["frames"] = header.get("Frames") if isinstance(header, dict) else None
    result["parse_error_commands"] = parse_errors
    result["commands"] = rows if isinstance(rows, list) else []
    result["command_count"] = len(result["commands"])
    return result


def _expected_races(manifest: dict[str, Any]) -> dict[int, str | None]:
    return {p.get("player"): _race(p.get("race")) for p in _players(manifest) if _int(p.get("player"))}


def _header_owner(parsed: dict[str, Any], candidate: dict[str, Any], number: int) -> tuple[int | None, str]:
    headers = parsed.get("header_players") if isinstance(parsed.get("header_players"), list) else []
    names = _player_names(candidate)
    exact = [item for item in headers if isinstance(item, dict) and item.get("Name") in names]
    if len(exact) == 1 and _int(exact[0].get("ID")):
        return exact[0]["ID"], "resolved_exact_name"
    # A numbered fallback remains useful for screp fixtures whose Header omits
    # names, but the evidence says explicitly that this was positional.
    expected = number - 1
    positional = [item for item in headers if isinstance(item, dict) and item.get("ID") == expected]
    if len(positional) == 1:
        return expected, "resolved_protocol_slot"
    return None, "unresolved"


def _is_order(row: dict[str, Any], name: str) -> bool:
    return ((row.get("Order") or {}).get("Name") == name)


def _pos(row: dict[str, Any]) -> tuple[int, int] | None:
    point = row.get("Pos")
    if not isinstance(point, dict) or not _int(point.get("X")) or not _int(point.get("Y")):
        return None
    return point["X"], point["Y"]


def _hold_active_intervals(diagnostic: dict[str, Any]) -> list[tuple[int, int]] | None:
    """Return replay-frame windows in which lone-Zealot hold commands apply.

    Lifecycle frames are callback frames.  Replay command rows are recorded
    two frames later at LF3, so extend each lifecycle's upper bound by two
    frames.  Older diagnostics only exposed the first release frame; retain
    that representation as a conservative prefix window and use an unbounded
    window when no release evidence exists.
    """
    lifecycles = diagnostic.get("lone_zealot_hold_unit_lifecycles")
    intervals: list[tuple[int, int]] = []
    if isinstance(lifecycles, list):
        for lifecycle in lifecycles:
            if not isinstance(lifecycle, dict):
                continue
            first = lifecycle.get("first_seen_frame")
            last = lifecycle.get("last_seen_frame")
            if _int(first) and _int(last) and first >= 0 and last >= first:
                intervals.append((first, last + 2))
    if intervals:
        return intervals

    release = diagnostic.get("lone_zealot_hold_release_frame")
    if _int(release) and release >= 0:
        return [(0, release - 1)]
    return None


def _mechanism_audit(parsed: dict[str, Any], diagnostic: dict[str, Any], owner_id: int | None) -> dict[str, Any]:
    known_zerg = diagnostic.get("known_zerg")
    policy_status = (
        "applicable"
        if known_zerg is True
        else "not_applicable_non_zerg"
        if known_zerg is False
        else "checked_without_race_metadata"
    )
    # The lone-Zealot hold and close-threat checks describe the Zerg-specific
    # opening policy.  A non-Zerg row can legitimately contain long streams of
    # ordinary Attack1/AttackMove commands; do not classify those commands as
    # policy violations.  Keep all replay integrity checks in audit_match,
    # which run independently of this optional mechanism policy.
    if known_zerg is False:
        return {
            "owner_id": owner_id,
            "known_zerg": False,
            "policy_applicability": "not_applicable",
            "policy_status": policy_status,
            "policy_status_reason": "diagnostic_known_zerg_false",
            "release_frame": None,
            "pre_release_attack1_frames": [],
            "pre_release_attack_move_frames": [],
            "hold_active_intervals": None,
            "hold_active_attack1_frames": [],
            "hold_active_attack_move_frames": [],
            "close_threat_events": [],
            "move_commands": [],
            "anchor": None,
            "unit_identity_matching": "not_applicable",
            "unit_identity_note": "Zerg-specific hold policy was not evaluated",
            "issues": [],
        }

    issues: list[str] = []
    release = diagnostic.get("lone_zealot_hold_release_frame")
    release = release if _int(release) and release >= 0 else None
    rows = [r for r in parsed.get("commands", []) if isinstance(r, dict) and r.get("PlayerID") == owner_id] if owner_id is not None else []
    hold_intervals = _hold_active_intervals(diagnostic)

    def hold_active(row: dict[str, Any]) -> bool:
        frame = row.get("Frame")
        if not _int(frame):
            return False
        return hold_intervals is None or any(start <= frame <= end for start, end in hold_intervals)

    # Accepted close-threat events are diagnostic callback evidence.  Match
    # their replay commands against every candidate-owned Attack1 row because
    # later one-Zealot epochs can occur after the first release.  The
    # hold-only policy checks below still use active lifecycle windows, so
    # ordinary post-release attacks remain outside the hold gate.
    attack_rows = [r for r in rows if _is_order(r, "Attack1")]
    hold_attack_rows = [r for r in attack_rows if hold_active(r)]
    attack_move_rows = [r for r in rows if hold_active(r) and _is_order(r, "AttackMove")]
    legacy_before = lambda row: release is None or (_int(row.get("Frame")) and row["Frame"] < release)
    legacy_attack_move_rows = [r for r in rows if legacy_before(r) and _is_order(r, "AttackMove")]
    events = diagnostic.get("lone_zealot_hold_close_threat_events")
    events = events if isinstance(events, list) else []
    accepted = [e for e in events if isinstance(e, dict) and e.get("accepted") is True]
    attack_by_frame: dict[int, list[dict[str, Any]]] = {}
    for row in attack_rows:
        if _int(row.get("Frame")):
            attack_by_frame.setdefault(row["Frame"], []).append(row)
    event_evidence: list[dict[str, Any]] = []
    expected_frames: set[int] = set()
    for index, event in enumerate(accepted):
        frame = event.get("frame")
        expected = frame + 2 if _int(frame) else None
        if expected is None:
            issues.append(f"close_threat_event_invalid_frame:{index}")
            continue
        expected_frames.add(expected)
        matches = attack_by_frame.get(expected, [])
        evidence: dict[str, Any] = {"index": index, "event_frame": frame, "expected_replay_frame": expected, "matches": len(matches)}
        if len(matches) != 1:
            issues.append(f"close_threat_attack1_count:{frame}:{len(matches)}")
        elif event.get("target_position") is not None:
            actual = _pos(matches[0])
            target = event.get("target_position")
            expected_pos = (target.get("x"), target.get("y")) if isinstance(target, dict) and _int(target.get("x")) and _int(target.get("y")) else None
            evidence["replay_target"] = actual
            evidence["diagnostic_target"] = expected_pos
            if expected_pos is None:
                issues.append(f"close_threat_target_coordinates_invalid:{frame}")
            elif actual is None:
                issues.append(f"close_threat_target_coordinates_missing:{frame}")
            elif actual != expected_pos:
                issues.append(f"close_threat_target_mismatch:{frame}")
        event_evidence.append(evidence)
    for row in hold_attack_rows:
        if _int(row.get("Frame")) and row["Frame"] not in expected_frames:
            issues.append(f"unmatched_pre_release_attack1:{row['Frame']}")
    if attack_move_rows:
        issues.append(f"pre_release_attack_move:{len(attack_move_rows)}")

    anchor = diagnostic.get("lone_zealot_hold_anchor")
    anchor_pos = (anchor.get("x"), anchor.get("y")) if isinstance(anchor, dict) and _int(anchor.get("x")) and _int(anchor.get("y")) else None
    move_rows = [r for r in rows if hold_active(r) and _is_order(r, "Move")]
    lifecycle = diagnostic.get("lone_zealot_hold_unit_lifecycles")
    held_ids = {item.get("unit_id") for item in lifecycle or [] if isinstance(item, dict) and _int(item.get("unit_id"))}
    held_ids.update(e.get("held_unit_id") for e in accepted if _int(e.get("held_unit_id")))
    mapped_moves = [r for r in move_rows if r.get("UnitTag") in held_ids]
    identity_status = "resolved" if move_rows and mapped_moves else "unsupported"
    # screp UnitTag values are usually replay-local and cannot be joined to
    # BWAPI unit IDs.  Coordinates remain a conservative check for all exposed
    # hold-window Move commands, while the report records the identity limit.
    checked_moves = move_rows
    bad_moves = [r for r in checked_moves if anchor_pos is not None and _pos(r) != anchor_pos]
    if anchor_pos is None and checked_moves:
        issues.append("hold_anchor_missing")
    if bad_moves:
        issues.append(f"held_move_target_mismatch:{len(bad_moves)}")
    return {
        "owner_id": owner_id,
        "known_zerg": known_zerg,
        "policy_applicability": "applicable" if known_zerg is True else "unknown",
        "policy_status": policy_status,
        "policy_status_reason": "diagnostic_known_zerg_true" if known_zerg is True else "diagnostic_missing_known_zerg",
        "release_frame": release,
        # Keep the legacy fields for consumers of the original report schema.
        # The interval-scoped fields below are the authoritative hold checks.
        "pre_release_attack1_frames": [r.get("Frame") for r in attack_rows if release is None or (_int(r.get("Frame")) and r["Frame"] < release)],
        "pre_release_attack_move_frames": [r.get("Frame") for r in legacy_attack_move_rows],
        "hold_active_intervals": [
            {"start_frame": start, "end_frame": end}
            for start, end in hold_intervals
        ] if hold_intervals is not None else None,
        "hold_active_attack1_frames": [r.get("Frame") for r in hold_attack_rows],
        "hold_active_attack_move_frames": [r.get("Frame") for r in attack_move_rows],
        "close_threat_events": event_evidence,
        "move_commands": [{"frame": r.get("Frame"), "target": _pos(r), "unit_tag": r.get("UnitTag")} for r in move_rows],
        "anchor": anchor_pos,
        "unit_identity_matching": identity_status,
        "unit_identity_note": "screp replay UnitTag values did not match diagnostic BWAPI unit IDs" if identity_status == "unsupported" else "replay UnitTag matched diagnostic held-unit IDs",
        "issues": sorted(set(issues)),
    }


def audit_match(manifest: dict[str, Any], diagnostic: dict[str, Any], screp: Path,
                candidate_player: int, *, manifest_path: Path | None = None,
                diagnostic_path: Path | None = None) -> dict[str, Any]:
    root = (manifest_path or Path.cwd()).resolve().parent
    issues: list[str] = []
    players = _players(manifest)
    candidate = _candidate(manifest, candidate_player)
    if candidate is None:
        issues.append(f"candidate_player_missing:{candidate_player}")

    if manifest.get("status") != "completed":
        issues.append("manifest_not_completed")
    if manifest.get("outcome_verified") is not True:
        issues.append("outcome_not_verified")
    if manifest.get("launch_error") not in (None, ""):
        issues.append("launch_error")
    if any(p.get("return_code") != 0 for p in players):
        issues.append("nonzero_player_exit")

    winners = [p for p in players if _player_metadata(p).get("winner") is True]
    losers = [p for p in players if _player_metadata(p).get("winner") is False]
    if len(players) != 2 or len(winners) != 1 or len(losers) != 1:
        issues.append("winner_not_reciprocal")
    if candidate and _int(candidate.get("player")) and diagnostic.get("winner") is not None:
        if diagnostic.get("winner") != _player_metadata(candidate).get("winner"):
            issues.append("candidate_diagnostic_winner_mismatch")

    kill_events, kill_issues = _kill_events(manifest, root)
    issues.extend(kill_issues)
    if not kill_events:
        issues.append("terminal_kill_events_missing")

    expected_races = _expected_races(manifest)
    replay_records = [r for r in manifest.get("replays", []) if isinstance(r, dict)]
    if len(replay_records) < 2:
        issues.append("replay_copies_missing")
    replay_evidence: list[dict[str, Any]] = []
    candidate_parse: dict[str, Any] | None = None
    owner_id: int | None = None
    for record in replay_records:
        source_path = _resolve(record.get("source_path"), root)
        archive_path = _resolve(record.get("path"), root)
        copies: list[dict[str, Any]] = []
        for label, path in (("source", source_path), ("archive", archive_path)):
            parsed = _screp(path, screp) if path else {"path": None, "exists": False, "sha256": None, "size_bytes": None, "screp_exit_code": None, "json_valid": False, "header_players": [], "commands": []}
            expected_hash = record.get("sha256")
            expected_size = record.get("size_bytes")
            if path is None or not parsed.get("exists"):
                issues.append(f"{label}_replay_missing:{record.get('player')}")
            if isinstance(expected_hash, str) and parsed.get("sha256") != expected_hash:
                issues.append(f"{label}_replay_hash_mismatch:{record.get('player')}")
            if _int(expected_size) and parsed.get("size_bytes") != expected_size:
                issues.append(f"{label}_replay_size_mismatch:{record.get('player')}")
            if source_path and archive_path and label == "archive" and copies and parsed.get("sha256") != copies[0].get("sha256"):
                issues.append(f"source_archive_hash_mismatch:{record.get('player')}")
            if source_path and archive_path and label == "archive" and copies and parsed.get("size_bytes") != copies[0].get("size_bytes"):
                issues.append(f"source_archive_size_mismatch:{record.get('player')}")
            if parsed.get("screp_exit_code") != 0 or parsed.get("json_valid") is not True:
                issues.append(f"screp_parse_failed:{label}:{record.get('player')}")
            if parsed.get("parse_error_commands") not in (None, [], 0):
                issues.append(f"screp_parse_errors:{label}:{record.get('player')}")
            header_players = parsed.get("header_players") or []
            expected_race = expected_races.get(record.get("player"))
            expected_header = [
                (protocol_player, race)
                for protocol_player, race in expected_races.items()
                if _int(protocol_player) and race is not None
            ]
            for protocol_player, race in expected_header:
                matching_header = next(
                    (p for p in header_players if isinstance(p, dict) and p.get("ID") == protocol_player - 1),
                    None,
                )
                if matching_header is None or _race((matching_header.get("Race") or {}).get("Name")) != race:
                    issues.append(f"replay_race_mismatch:{label}:{record.get('player')}:{race}")
                    break
            callback = _player_metadata(next((p for p in players if p.get("player") == record.get("player")), {})).get("frame_count")
            if not _int(parsed.get("frames")) or not _int(callback) or parsed["frames"] + 1 != callback:
                issues.append(f"header_callback_frame_mismatch:{label}:{record.get('player')}")
            copies.append({"kind": label, "path": str(path) if path else None, "sha256": parsed.get("sha256"), "size_bytes": parsed.get("size_bytes"), "screp_exit_code": parsed.get("screp_exit_code"), "json_valid": parsed.get("json_valid"), "parse_error_commands": parsed.get("parse_error_commands"), "header_frames": parsed.get("frames"), "header_players": parsed.get("header_players"), "command_count": parsed.get("command_count")})
            if record.get("player") == candidate_player and label == "archive":
                candidate_parse = parsed
                if candidate:
                    owner_id, owner_status = _header_owner(parsed, candidate, candidate_player)
                else:
                    owner_status = "unresolved"
                if owner_id is None:
                    issues.append("candidate_owner_unresolved")
        replay_evidence.append({"player": record.get("player"), "manifest_sha256": record.get("sha256"), "manifest_size_bytes": record.get("size_bytes"), "copies": copies})

    mechanism = _mechanism_audit(candidate_parse or {}, diagnostic, owner_id)
    issues.extend(mechanism["issues"])
    if candidate_parse is None:
        issues.append("candidate_replay_missing")

    result = {
        "schema_version": 1,
        "pass": not issues,
        "issues": sorted(set(issues)),
        "evidence": {
            "manifest": {"path": str(manifest_path) if manifest_path else None, "run_id": manifest.get("run_id"), "status": manifest.get("status"), "outcome_verified": manifest.get("outcome_verified"), "candidate_player": candidate_player, "candidate_name": candidate.get("name") if candidate else None},
            "players": [{"player": p.get("player"), "name": p.get("name"), "race": p.get("race"), "return_code": p.get("return_code"), "winner": _player_metadata(p).get("winner"), "frame_count": _player_metadata(p).get("frame_count")} for p in players],
            "terminal_kill_events": kill_events,
            "replays": replay_evidence,
            "candidate_diagnostic": {"path": str(diagnostic_path) if diagnostic_path else None, "frame_count": diagnostic.get("frame_count"), "winner": diagnostic.get("winner"), "release_frame": diagnostic.get("lone_zealot_hold_release_frame")},
            "mechanism": mechanism,
        },
    }
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, nargs="?")
    parser.add_argument("candidate_diagnostic", type=Path, nargs="?")
    parser.add_argument("screp", type=Path, nargs="?")
    parser.add_argument("candidate_player", type=int, nargs="?")
    parser.add_argument("--manifest", dest="manifest_option", type=Path)
    parser.add_argument("--candidate-diagnostic", dest="diagnostic_option", type=Path)
    parser.add_argument("--screp", dest="screp_option", type=Path)
    parser.add_argument("--candidate-player", dest="player_option", type=int)
    parser.add_argument("--output", type=Path, help="Durable JSON output path")
    args = parser.parse_args(argv)
    manifest_path = args.manifest_option or args.manifest
    diagnostic_path = args.diagnostic_option or args.candidate_diagnostic
    screp_path = args.screp_option or args.screp
    candidate_player = args.player_option if args.player_option is not None else args.candidate_player
    if manifest_path is None or diagnostic_path is None or screp_path is None or candidate_player is None:
        parser.error("manifest, candidate diagnostic, screp path, and candidate player are required")
    manifest, manifest_error = _read_json(manifest_path)
    diagnostic, diagnostic_error = _read_json(diagnostic_path)
    if not isinstance(manifest, dict):
        manifest = {}
    if not isinstance(diagnostic, dict):
        diagnostic = {}
    report = audit_match(manifest, diagnostic, screp_path, candidate_player, manifest_path=manifest_path, diagnostic_path=diagnostic_path)
    if manifest_error:
        report["issues"].append(f"manifest_parse:{manifest_error}")
    if diagnostic_error:
        report["issues"].append(f"diagnostic_parse:{diagnostic_error}")
    report["issues"] = sorted(set(report["issues"]))
    report["pass"] = not report["issues"]
    output = args.output or manifest_path.with_suffix(".replay-audit.json")
    _atomic_json(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
