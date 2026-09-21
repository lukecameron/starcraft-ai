import copy
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit_kestrel_modular_replay", ROOT / "scripts/audit_kestrel_modular_replay.py"
)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class KestrelModularReplayAuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source.rep"
        self.archive = self.root / "archive.rep"
        self.source.write_bytes(b"replay-bytes")
        self.archive.write_bytes(b"replay-bytes")
        digest = hashlib.sha256(b"replay-bytes").hexdigest()
        self.manifest = {
            "run_id": "test-run",
            "status": "completed",
            "outcome_verified": True,
            "launch_error": None,
            "players": [
                {"player": 1, "name": "ZZZKBot Zerg", "race": "Zerg", "return_code": 0,
                 "result_metadata": {"winner": True, "frame_count": 101}},
                {"player": 2, "name": "Kestrel Modular v1", "race": "Protoss", "return_code": 0,
                 "result_metadata": {"winner": False, "frame_count": 101}},
            ],
            "terminal_events": [
                {"event": "kill_client", "source": "controller_not_occupied_after_action", "action_id": 87},
                {"event": "kill_client", "source": "transport_callback", "action_id": -1},
            ],
            "replays": [
                {"player": 1, "source_path": str(self.source), "path": str(self.archive), "sha256": digest, "size_bytes": 13},
                {"player": 2, "source_path": str(self.source), "path": str(self.archive), "sha256": digest, "size_bytes": 13},
            ],
        }
        self.diagnostic = {
            "ended": True,
            "winner": False,
            "frame_count": 100,
            "lone_zealot_hold_release_frame": -1,
            "lone_zealot_hold_anchor": {"x": 100, "y": 200},
            "lone_zealot_hold_close_threat_events": [{
                "accepted": True, "frame": 10, "target_position": {"x": 120, "y": 220},
                "held_unit_id": 55, "target_id": 56,
            }],
            "lone_zealot_hold_unit_lifecycles": [{"unit_id": 55}],
        }
        self.parsed = {
            "exists": True,
            "sha256": hashlib.sha256(b"replay-bytes").hexdigest(),
            "size_bytes": 13,
            "screp_exit_code": 0,
            "json_valid": True,
            "parse_error_commands": None,
            "frames": 100,
            "header_players": [
                {"ID": 0, "Name": "ZZZKBot Zerg", "Race": {"Name": "Zerg"}},
                {"ID": 1, "Name": "Kestrel Modular v1", "Race": {"Name": "Protoss"}},
            ],
            "commands": [
                {"PlayerID": 1, "Frame": 5, "Order": {"Name": "Move"}, "Pos": {"X": 100, "Y": 200}, "UnitTag": 900},
                {"PlayerID": 1, "Frame": 12, "Order": {"Name": "Attack1"}, "Pos": {"X": 120, "Y": 220}, "UnitTag": 901},
            ],
        }

    def tearDown(self):
        self.temp.cleanup()

    def run_audit(self, manifest=None, diagnostic=None, parsed=None):
        with patch.object(AUDIT, "_screp", return_value=copy.deepcopy(parsed or self.parsed)):
            return AUDIT.audit_match(
                manifest or self.manifest, diagnostic or self.diagnostic, self.root / "screp", 2,
                manifest_path=self.root / "manifest.json", diagnostic_path=self.root / "diagnostic.json",
            )

    def test_valid_row_passes_and_reports_unsupported_unit_identity(self):
        result = self.run_audit()
        self.assertTrue(result["pass"], result["issues"])
        mechanism = result["evidence"]["mechanism"]
        self.assertEqual(mechanism["unit_identity_matching"], "unsupported")
        self.assertEqual(mechanism["close_threat_events"][0]["matches"], 1)

    def test_nonzero_exit_and_nonreciprocal_winner_fail(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["players"][1]["return_code"] = 1
        manifest["players"][0]["result_metadata"]["winner"] = True
        manifest["players"][1]["result_metadata"]["winner"] = True
        result = self.run_audit(manifest=manifest)
        self.assertFalse(result["pass"])
        self.assertIn("nonzero_player_exit", result["issues"])
        self.assertIn("winner_not_reciprocal", result["issues"])

    def test_unregistered_terminal_kill_action_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["terminal_events"][0]["action_id"] = 88
        result = self.run_audit(manifest=manifest)
        self.assertFalse(result["pass"])
        self.assertIn(
            "terminal_kill_event_not_allowed:controller_not_occupied_after_action/88",
            result["issues"],
        )

    def test_source_archive_hash_mismatch_is_durable_issue(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["replays"][1]["sha256"] = "0" * 64
        result = self.run_audit(manifest=manifest)
        self.assertFalse(result["pass"])
        self.assertIn("source_replay_hash_mismatch:2", result["issues"])
        self.assertIn("archive_replay_hash_mismatch:2", result["issues"])

    def test_attack_move_and_close_threat_target_mismatch_fail(self):
        parsed = copy.deepcopy(self.parsed)
        parsed["commands"].append({"PlayerID": 1, "Frame": 20, "Order": {"Name": "AttackMove"}, "Pos": {"X": 100, "Y": 200}})
        parsed["commands"][1]["Pos"] = {"X": 121, "Y": 220}
        result = self.run_audit(parsed=parsed)
        self.assertFalse(result["pass"])
        self.assertIn("pre_release_attack_move:1", result["issues"])
        self.assertIn("close_threat_target_mismatch:10", result["issues"])

    def test_reactivated_hold_epochs_match_later_attack1_rows(self):
        diagnostic = copy.deepcopy(self.diagnostic)
        diagnostic.update({
            "lone_zealot_hold_release_frame": 3537,
            "lone_zealot_hold_close_threat_events": [
                {"accepted": True, "frame": 3756, "target_position": {"x": 3747, "y": 1749}},
                {"accepted": True, "frame": 4485, "target_position": {"x": 3835, "y": 1898}},
            ],
            "lone_zealot_hold_unit_lifecycles": [
                {"unit_id": 160, "first_seen_frame": 2931, "last_seen_frame": 3534},
                {"unit_id": 166, "first_seen_frame": 3729, "last_seen_frame": 3840},
                {"unit_id": 174, "first_seen_frame": 4380, "last_seen_frame": 4578},
            ],
        })
        parsed = copy.deepcopy(self.parsed)
        parsed["commands"] = [
            # The first release precedes these ordinary attacks.  They must
            # not be mistaken for hold commands or close-threat evidence.
            {"PlayerID": 1, "Frame": 3539, "Order": {"Name": "AttackMove"}, "Pos": {"X": 3744, "Y": 1792}},
            {"PlayerID": 1, "Frame": 3560, "Order": {"Name": "Attack1"}, "Pos": {"X": 3626, "Y": 1518}},
            {"PlayerID": 1, "Frame": 3731, "Order": {"Name": "Move"}, "Pos": {"X": 100, "Y": 200}},
            {"PlayerID": 1, "Frame": 3758, "Order": {"Name": "Attack1"}, "Pos": {"X": 3747, "Y": 1749}},
            {"PlayerID": 1, "Frame": 4382, "Order": {"Name": "Move"}, "Pos": {"X": 100, "Y": 200}},
            {"PlayerID": 1, "Frame": 4487, "Order": {"Name": "Attack1"}, "Pos": {"X": 3835, "Y": 1898}},
        ]
        result = self.run_audit(diagnostic=diagnostic, parsed=parsed)
        self.assertTrue(result["pass"], result["issues"])
        mechanism = result["evidence"]["mechanism"]
        self.assertEqual([event["matches"] for event in mechanism["close_threat_events"]], [1, 1])
        self.assertEqual(mechanism["hold_active_attack1_frames"], [3758, 4487])
        self.assertEqual(mechanism["hold_active_attack_move_frames"], [])
        self.assertEqual(mechanism["pre_release_attack1_frames"], [])

    def test_attack_move_is_rejected_only_inside_hold_interval(self):
        diagnostic = copy.deepcopy(self.diagnostic)
        diagnostic.update({
            "lone_zealot_hold_release_frame": 100,
            "lone_zealot_hold_unit_lifecycles": [
                {"unit_id": 55, "first_seen_frame": 10, "last_seen_frame": 20},
                {"unit_id": 56, "first_seen_frame": 200, "last_seen_frame": 220},
            ],
        })
        parsed = copy.deepcopy(self.parsed)
        parsed["commands"] = [
            {"PlayerID": 1, "Frame": 50, "Order": {"Name": "AttackMove"}, "Pos": {"X": 100, "Y": 200}},
            {"PlayerID": 1, "Frame": 202, "Order": {"Name": "AttackMove"}, "Pos": {"X": 100, "Y": 200}},
        ]
        result = self.run_audit(diagnostic=diagnostic, parsed=parsed)
        self.assertFalse(result["pass"])
        self.assertIn("pre_release_attack_move:1", result["issues"])
        self.assertEqual(result["evidence"]["mechanism"]["hold_active_attack_move_frames"], [202])

    def test_release_cutoff_fallback_preserves_legacy_attack_move_gate(self):
        diagnostic = copy.deepcopy(self.diagnostic)
        diagnostic["lone_zealot_hold_release_frame"] = 100
        diagnostic["lone_zealot_hold_unit_lifecycles"] = [{"unit_id": 55}]
        parsed = copy.deepcopy(self.parsed)
        parsed["commands"] = [
            {"PlayerID": 1, "Frame": 50, "Order": {"Name": "AttackMove"}, "Pos": {"X": 100, "Y": 200}},
            {"PlayerID": 1, "Frame": 101, "Order": {"Name": "AttackMove"}, "Pos": {"X": 100, "Y": 200}},
        ]
        result = self.run_audit(diagnostic=diagnostic, parsed=parsed)
        self.assertFalse(result["pass"])
        self.assertIn("pre_release_attack_move:1", result["issues"])
        self.assertEqual(result["evidence"]["mechanism"]["hold_active_attack_move_frames"], [50])

    def test_parse_error_race_and_frame_mismatch_fail(self):
        parsed = copy.deepcopy(self.parsed)
        parsed["parse_error_commands"] = [{"Frame": 4}]
        parsed["frames"] = 99
        parsed["header_players"][1]["Race"] = {"Name": "Terran"}
        result = self.run_audit(parsed=parsed)
        self.assertFalse(result["pass"])
        self.assertTrue(any(issue.startswith("screp_parse_errors:") for issue in result["issues"]))
        self.assertTrue(any(issue.startswith("replay_race_mismatch:") for issue in result["issues"]))
        self.assertTrue(any(issue.startswith("header_callback_frame_mismatch:") for issue in result["issues"]))


if __name__ == "__main__":
    unittest.main()
