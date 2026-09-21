import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "kestrel_modular_leash_hysteresis",
    ROOT / "scripts/score_kestrel_modular_leash_hysteresis.py",
)
SCORER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCORER)


class KestrelModularLeashHysteresisTest(unittest.TestCase):
    @staticmethod
    def valid_record():
        return {
            "telemetry_schema": "kestrel-modular-v1",
            "frame_count": 5000,
            "latency_frames": 3,
            "ended": True,
            "known_zerg": True,
            "command_count": 7,
            "rejected_commands": 0,
            "callback_count": 5000,
            "zerg_four_probe_pylon_accepted": True,
            "zerg_four_probe_pylon_accepted_frame": 100,
            "zerg_four_probe_pylon_completed_probe_count": 4,
            "zerg_four_probe_pylon_completed_frame": 150,
            "first_pylon_accepted_frame": 100,
            "accepted_probe_train_frames": [200],
            "accepted_zealot_trains": 2,
            "second_zealot_train_frame": 250,
            "second_zealot_completed_frame": 3800,
            "first_gateway_accepted_frame": 200,
            "reserve_active_frames": [150],
            "reserve_active_minerals": [90],
            "reserve_active_reserves": [50],
            "reserve_block_frames": [150],
            "reserve_block_minerals": [90],
            "reserve_block_reserves": [50],
            "reserve_block_pre_acceptance_flags": [1],
            "construction_events": [{
                "type_id": 1,
                "baseline": 0,
                "accepted_frame": 100,
                "current_frame": 110,
                "completed_frame": 150,
            }, {
                "type_id": 2,
                "baseline": 0,
                "accepted_frame": 200,
                "current_frame": 210,
                "completed_frame": 250,
            }],
            "command_categories": {
                "build": {"attempted": 2, "rejected": 0},
                "train": {"attempted": 2, "rejected": 0},
                "gather": {"attempted": 1, "rejected": 0},
                "attack": {"attempted": 1, "rejected": 0},
                "scout": {"attempted": 1, "rejected": 0},
            },
            "command_error_counts": {"unit_busy": 0},
            "lone_zealot_hold_active_samples": 20,
            "lone_zealot_hold_suppression_samples": 10,
            "lone_zealot_hold_unique_units": 1,
            "lone_zealot_hold_home_move_attempts": 1,
            "lone_zealot_hold_home_move_accepted": 1,
            "lone_zealot_hold_release_frame": 3800,
            "lone_zealot_hold_anchor": {
                "start_tile_x": 10, "start_tile_y": 20, "x": 384, "y": 688,
            },
            "lone_zealot_hold_home_move_accepted_targets": [{"x": 384, "y": 688}],
            "lone_zealot_hold_leash_radius": 96,
            "lone_zealot_hold_return_release_radius": 48,
            "lone_zealot_hold_return_entries": 1,
            "lone_zealot_hold_return_active_samples": 1,
            "lone_zealot_hold_return_releases": 1,
            "lone_zealot_hold_return_move_attempts": 1,
            "lone_zealot_hold_return_move_accepted": 1,
            "lone_zealot_hold_return_move_rejected": 0,
            "lone_zealot_hold_return_move_coalesced": 0,
            "lone_zealot_hold_leash_block_samples": 1,
            "lone_zealot_hold_leash_move_attempts": 1,
            "lone_zealot_hold_leash_move_accepted": 1,
            "lone_zealot_hold_leash_move_rejected": 0,
            "lone_zealot_hold_leash_move_coalesced": 0,
            "lone_zealot_hold_leash_max_anchor_distance": 96,
            "lone_zealot_hold_close_threat_samples": 1,
            "lone_zealot_hold_close_threat_radius": 160,
            "lone_zealot_hold_close_threat_attack_origins_within_leash": True,
            "lone_zealot_hold_close_threat_first_frame": 100,
            "lone_zealot_hold_close_threat_attack_attempts": 1,
            "lone_zealot_hold_close_threat_attack_accepted": 1,
            "lone_zealot_hold_close_threat_attack_rejected": 0,
            "lone_zealot_hold_close_threat_accepted_frames": [110],
            "lone_zealot_hold_close_threat_accepted_held_unit_ids": [7],
            "lone_zealot_hold_close_threat_accepted_target_ids": [42],
            "lone_zealot_hold_close_threat_accepted_held_positions": [{"x": 384, "y": 688}],
            "lone_zealot_hold_close_threat_accepted_target_positions": [{"x": 440, "y": 688}],
            "lone_zealot_hold_close_threat_events": [{
                "frame": 110,
                "held_unit_id": 7,
                "target_id": 42,
                "held_unit_position": {"x": 384, "y": 688},
                "target_position": {"x": 440, "y": 688},
                "accepted": True,
            }],
            "lone_zealot_hold_unit_lifecycles": [{
                "unit_id": 7,
                "first_seen_frame": 90,
                "last_seen_frame": 3800,
                "close_threat_samples": 1,
                "close_threat_attack_attempts": 1,
                "close_threat_attack_accepted": 1,
                "close_threat_attack_rejected": 0,
                "first_close_threat_frame": 100,
                "last_close_threat_frame": 100,
                "anchor_move_attempts": 1,
                "anchor_move_accepted": 1,
                "leash_block_samples": 1,
                "leash_move_attempts": 1,
                "leash_move_accepted": 1,
                "leash_move_rejected": 0,
                "leash_move_coalesced": 0,
                "max_anchor_distance": 96,
                "return_entries": 1,
                "return_active_samples": 1,
                "return_releases": 1,
                "return_move_attempts": 1,
                "return_move_accepted": 1,
                "return_move_rejected": 0,
                "return_move_coalesced": 0,
            }],
        }

    def test_valid_diagnostic_passes_but_replay_integrity_remains_separate(self):
        result = SCORER.validate_leash_hysteresis_record(self.valid_record())
        self.assertTrue(result["complete"])
        self.assertTrue(result["mechanisms_pass"])
        self.assertEqual(result["decision"], "pass-to-five-game-screen")
        self.assertTrue(result["replay_integrity_gates_separate"])
        self.assertFalse(result["elo_eligible"])

    def test_incomplete_required_opening_construction_fails(self):
        record = self.valid_record()
        record["construction_events"][0]["completed_frame"] = -1
        result = SCORER.validate_leash_hysteresis_record(record)
        self.assertIn(
            "first_pylon opening construction lifecycle did not complete",
            result["mechanism_issues"],
        )
        self.assertFalse(result["mechanisms_pass"])

    def test_incomplete_optional_late_construction_is_retained_without_failure(self):
        record = self.valid_record()
        record["construction_events"].append({
            "type_id": 3,
            "baseline": 1,
            "accepted_frame": 3000,
            "current_frame": -1,
            "completed_frame": -1,
        })
        record["command_categories"]["build"]["attempted"] += 1
        record["command_count"] += 1
        result = SCORER.validate_leash_hysteresis_record(record)
        self.assertTrue(result["complete"])
        self.assertTrue(result["mechanisms_pass"])
        incomplete = result["construction"]["optional_incomplete_construction_events"]
        self.assertEqual(len(incomplete), 1)
        self.assertEqual(incomplete[0]["accepted_frame"], 3000)

    def test_empty_evidence_is_rejected(self):
        result = SCORER.validate_leash_hysteresis_record({})
        self.assertFalse(result["complete"])
        self.assertFalse(result["mechanisms_pass"])
        self.assertTrue(any("missing lone_zealot_hold_return_entries" in issue
                            for issue in result["issues"]))

    def test_coalesced_only_move_does_not_count_as_issued_accepted_move(self):
        record = self.valid_record()
        record.update({
            "lone_zealot_hold_leash_block_samples": 1,
            "lone_zealot_hold_leash_move_attempts": 0,
            "lone_zealot_hold_leash_move_accepted": 0,
            "lone_zealot_hold_leash_move_coalesced": 1,
        })
        lifecycle = record["lone_zealot_hold_unit_lifecycles"][0]
        lifecycle.update({
            "leash_block_samples": 1,
            "leash_move_attempts": 0,
            "leash_move_accepted": 0,
            "leash_move_coalesced": 1,
        })
        result = SCORER.validate_leash_hysteresis_record(record)
        self.assertIn("no actually issued accepted leash move was observed", result["mechanism_issues"])

    def test_off_leash_flag_is_rejected(self):
        record = self.valid_record()
        record["lone_zealot_hold_close_threat_attack_origins_within_leash"] = False
        result = SCORER.validate_leash_hysteresis_record(record)
        self.assertIn("close-threat attack origins were not all within the leash", result["mechanism_issues"])

    def test_missing_release_or_second_zealot_overlap_is_rejected(self):
        record = self.valid_record()
        record["lone_zealot_hold_release_frame"] = -1
        record["second_zealot_completed_frame"] = -1
        result = SCORER.validate_leash_hysteresis_record(record)
        self.assertIn("lone-Zealot hold did not release", result["mechanism_issues"])
        self.assertIn("two completed Zealots were not observed", result["mechanism_issues"])

    def test_unit_busy_is_rejected_even_when_total_rejections_are_zero(self):
        record = self.valid_record()
        record["command_error_counts"]["unit_busy"] = 1
        result = SCORER.validate_leash_hysteresis_record(record)
        self.assertIn("one or more Unit_Busy errors were recorded", result["mechanism_issues"])

    def test_close_threat_radius_is_candidate_specific(self):
        record = self.valid_record()
        record["lone_zealot_hold_close_threat_radius"] = 256
        result = SCORER.validate_leash_hysteresis_record(record)
        self.assertIn("close-threat radius must equal 160", result["mechanism_issues"])


if __name__ == "__main__":
    unittest.main()
