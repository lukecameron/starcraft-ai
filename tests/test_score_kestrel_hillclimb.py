import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from scripts import score_kestrel_hillclimb as scorer


class KestrelScorecardTests(TestCase):
    def test_outcome_performance_accepts_structured_command_categories(self):
        result = scorer.outcome_performance({
            "winner": False,
            "frame_count": 5304,
            "max_probes": 6,
            "max_gateways": 2,
            "max_zealots": 2,
            "max_dragoons": 0,
            "rejected_commands": 0,
            "command_categories": {
                "train": {"attempted": 4, "rejected": 1},
                "build": {"attempted": 3, "rejected": 0},
                "attack": {"attempted": 7, "rejected": 2},
            },
        })

        self.assertEqual(result["command_counts"], {"train": 3, "build": 3, "attack": 5})
        self.assertTrue(result["production_fields"]["accepted_train_commands"])
        self.assertTrue(result["production_fields"]["accepted_build_commands"])

    @staticmethod
    def v33_metadata() -> dict[str, object]:
        metadata: dict[str, object] = {
            "schema_version": 1,
            "emergency_trigger_frame": 90,
            "emergency_trigger_events": 1,
            "emergency_assignments": 3,
            "emergency_assignment_batches": 2,
            "emergency_first_assignment_frame": 100,
            "emergency_first_assignment_size": 2,
            "emergency_max_assignment_batch": 2,
            "emergency_peak_defenders": 2,
            "emergency_current_defenders": 0,
            "emergency_accepted_attack_orders": 4,
            "emergency_releases": 3,
            "emergency_first_release_frame": 200,
            "emergency_threat_clear_release_events": 1,
            "emergency_threat_clear_released_defenders": 2,
            "emergency_first_threat_clear_release_frame": 200,
            "emergency_army_two_release_events": 1,
            "emergency_army_two_released_defenders": 1,
            "emergency_first_army_two_release_frame": 300,
            "emergency_defender_deaths": 0,
            "emergency_build_selection_exclusions": 2,
            "emergency_economy_exclusions": 3,
            "emergency_post_release_gather_orders": 1,
            "emergency_post_release_build_orders": 1,
            "emergency_army_at_trigger": 0,
            "emergency_local_combat_at_trigger": 0,
            "emergency_assigned_probe_ids": [101, 102, 103],
            "emergency_assignment_frames": [100, 120],
            "emergency_assignment_sizes": [2, 1],
            "emergency_release_frames": [200, 300],
            "emergency_release_sizes": [2, 1],
            "emergency_release_army_two_flags": [0, 1],
        }
        return metadata

    @staticmethod
    def v34_metadata() -> dict[str, object]:
        return {
            "schema_version": 1,
            "known_zerg": True,
            "emergency_trigger_frame": 90,
            "emergency_trigger_events": 1,
            "emergency_assignments": 2,
            "emergency_assignment_batches": 1,
            "emergency_first_assignment_frame": 100,
            "emergency_first_assignment_size": 2,
            "emergency_max_assignment_batch": 2,
            "emergency_peak_defenders": 2,
            "emergency_current_defenders": 0,
            "emergency_accepted_attack_orders": 2,
            "emergency_releases": 2,
            "emergency_first_release_frame": 300,
            "emergency_threat_clear_release_events": 0,
            "emergency_threat_clear_released_defenders": 0,
            "emergency_first_threat_clear_release_frame": -1,
            "emergency_army_three_release_events": 1,
            "emergency_army_three_released_defenders": 2,
            "emergency_first_army_three_release_frame": 300,
            "emergency_defender_deaths": 0,
            "emergency_build_selection_exclusions": 1,
            "emergency_economy_exclusions": 1,
            "emergency_post_release_gather_orders": 1,
            "emergency_post_release_build_orders": 0,
            "emergency_army_at_trigger": 2,
            "emergency_local_combat_at_trigger": 2,
            "emergency_assigned_probe_ids": [101, 102],
            "emergency_assignment_frames": [100],
            "emergency_assignment_sizes": [2],
            "emergency_release_frames": [300],
            "emergency_release_sizes": [2],
            "emergency_release_army_three_flags": [1],
            "zerg_offense_stage_released": True,
            "zerg_offense_stage_remote_target_events": 2,
            "zerg_offense_stage_unique_units": 2,
            "zerg_offense_stage_pre_release_remote_blocks": 2,
            "zerg_offense_stage_pre_release_remote_orders": 0,
            "zerg_offense_stage_pre_release_remote_attempts": 2,
            "zerg_offense_stage_pre_release_remote_accepts": 0,
            "zerg_offense_stage_post_release_remote_attempts": 1,
            "zerg_offense_stage_post_release_remote_accepts": 1,
            "zerg_offense_stage_local_defense_attack_orders": 1,
            "zerg_offense_stage_home_move_attempts": 2,
            "zerg_offense_stage_home_move_orders": 2,
            "zerg_offense_stage_home_move_accepts": 2,
            "zerg_offense_stage_home_move_cooldown_blocks": 1,
            "zerg_offense_stage_home_move_repeat_orders": 1,
            "zerg_offense_stage_min_accepted_repeat_interval": 96,
            "zerg_offense_stage_home_target_orders": 2,
            "zerg_offense_stage_release_events": 1,
            "zerg_offense_stage_reset_events": 0,
            "zerg_offense_stage_restage_events": 0,
            "first_zerg_offense_stage_suppression_frame": 90,
            "first_zerg_offense_stage_frame": 50,
            "first_zerg_offense_stage_threshold_frame": 100,
            "first_zerg_offense_stage_release_frame": 100,
            "first_zerg_offense_stage_reset_frame": -1,
            "zerg_offense_stage_release_army": 9,
            "zerg_offense_stage_release_surplus": 6,
            "zerg_offense_stage_latch_clear_frame": -1,
            "zerg_offense_stage_latch_clear_cause": "none",
            "zerg_offense_stage_first_zero_after_release_frame": -1,
            "zerg_offense_stage_peak_surplus": 6,
            "zerg_offense_stage_current_surplus": 5,
            "zerg_offense_stage_release_unit_ids": [201, 202, 203, 204, 205, 206],
            "zerg_offense_stage_state_frames": [0, 50, 100, 200],
            "zerg_offense_stage_state_army": [3, 4, 9, 8],
            "zerg_offense_stage_state_reserve": [3, 3, 3, 3],
            "zerg_offense_stage_state_surplus": [0, 2, 6, 5],
            "zerg_offense_stage_state_codes": [0, 0, 1, 1],
            "zerg_offense_stage_state_cause_codes": [0, 0, 2, 0],
        }

    @staticmethod
    def v35_metadata() -> dict[str, object]:
        metadata = KestrelScorecardTests.v34_metadata()
        metadata.update({
            "accepted_build_frames": [20, 50, 75],
            "accepted_build_type_ids": [156, 160, 160],
            "accepted_build_pre_command_counts": [0, 0, 0],
            "accepted_build_post_command_counts": [0, 0, 0],
            "first_pylon_accepted_frame": 20,
            "first_pylon_current_frame": 30,
            "first_pylon_completed_frame": 40,
            "first_gateway_accepted_frame": 50,
            "first_gateway_current_frame": 60,
            "first_gateway_completed_frame": 70,
            "second_gateway_current_frame": 90,
            "second_gateway_completed_frame": 100,
            "first_zealot_train_frame": 71,
            "first_zealot_completed_frame": 80,
            "emergency_episode_current_id": 1,
            "emergency_episode_current_assignment_count": 0,
            "emergency_episode_threat_present": False,
            "emergency_episode_ids": [1],
            "emergency_episode_start_frames": [90],
            "emergency_episode_reset_frames": [250],
            "emergency_episode_assignment_counts": [2],
            "emergency_episode_cap_blocks": 1,
            "emergency_episode_cap_block_frames": [200],
            "emergency_episode_cap_block_counts": [2],
            "emergency_assignment_episode_ids": [1, 1],
        })
        return metadata

    @staticmethod
    def v36_metadata() -> dict[str, object]:
        metadata = KestrelScorecardTests.v35_metadata()
        metadata.update({
            "accepted_probe_train_frames": [40, 150],
            "probe_reserve_block_frames": [60, 90],
            "probe_reserve_block_minerals": [220, 299],
            "opening_probe_reserve": 250,
            "max_opening_probe_reserve": 250,
            "first_probe_reserve_window_frame": 50,
            "probe_reserve_window_end_frame": 150,
            "probe_reserve_block_count": 2,
            "first_pylon_accepted_frame": 50,
            "second_gateway_current_frame": 150,
        })
        return metadata

    @staticmethod
    def v37_metadata() -> dict[str, object]:
        metadata = KestrelScorecardTests.v36_metadata()
        metadata.update({
            "max_pylon_cap": 10,
            "max_post_core_gateway_cap": 6,
            "range_upgrade_eligibility_frame": 600,
            "range_upgrade_bank_start_frame": 600,
            "range_upgrade_bank_block_count": 2,
            "range_upgrade_attempt_frame": 720,
            "range_upgrade_accepted_frame": 720,
            "range_upgrade_completion_frame": 1200,
            "range_upgrade_attempts": 1,
            "range_upgrade_accepted": 1,
            "range_upgrade_completions": 1,
            "range_upgrade_max_bank_minerals": 150,
            "range_upgrade_max_bank_gas": 150,
            "seventh_pylon_accepted_frame": 800,
            "seventh_pylon_current_frame": 830,
            "seventh_pylon_completed_frame": 900,
            "fifth_gateway_accepted_frame": 1000,
            "fifth_gateway_current_frame": 1030,
            "fifth_gateway_completed_frame": 1100,
        })
        return metadata

    @staticmethod
    def v38_metadata() -> dict[str, object]:
        metadata = KestrelScorecardTests.v37_metadata()
        metadata.update({
            "shared_target_selections": 2,
            "shared_target_attempts": 2,
            "shared_target_accepted": 2,
            "shared_target_non_zerg_selections": 0,
            "shared_target_illegal_selections": 0,
            "shared_target_switches": 0,
            "shared_target_rejects": 0,
            "shared_target_correction_opportunities": 0,
            "shared_target_frames": [1300, 1400],
            "shared_target_ids": [501, 501],
            "shared_target_participant_counts": [2, 2],
            "shared_target_eligible_counts": [2, 2],
            "shared_target_ordered_counts": [0, 2],
            "shared_target_local_counts": [2, 2],
            "shared_target_attempt_counts": [2, 0],
            "shared_target_accepted_counts": [2, 0],
            "shared_target_participant_ids": [10, 11, 10, 11],
        })
        return metadata

    @staticmethod
    def v40_metadata() -> dict[str, object]:
        metadata = KestrelScorecardTests.v38_metadata()
        metadata.update({
            "gateway_probe_selection_frames": [50, 75],
            "gateway_probe_selection_ordinals": [1, 2],
            "gateway_probe_selection_builder_ids": [101, 101],
            "gateway_probe_selection_tile_xs": [12, 13],
            "gateway_probe_selection_tile_ys": [20, 20],
            "gateway_probe_selection_builder_distances": [30, 25],
            "gateway_probe_selection_eligible_counts": [2, 2],
            "gateway_probe_selection_min_eligible_distances": [30, 25],
            "gateway_probe_selection_candidate_counts": [3, 3],
            "gateway_probe_selection_candidate_truncated": [0, 0],
            "gateway_probe_candidate_ids": [101, 102, 103, 101, 102, 104],
            "gateway_probe_candidate_distances": [30, 30, 35, 25, 25, 31],
            "gateway_probe_candidate_reason_codes": [0, 0, 4, 0, 0, 5],
        })
        return metadata

    @staticmethod
    def v41_metadata() -> dict[str, object]:
        metadata = KestrelScorecardTests.v40_metadata()
        metadata["zerg_pre_pylon_probe_reserve_frames"] = 12
        return metadata

    @staticmethod
    def v42_metadata() -> dict[str, object]:
        metadata = KestrelScorecardTests.v40_metadata()
        metadata.update({
            "zerg_five_probe_policy_active_frames": 35,
            "zerg_five_probe_pylon_accepted": True,
            "zerg_five_probe_pylon_accepted_frame": metadata["first_pylon_accepted_frame"],
        })
        return metadata

    def test_v42_generation_inherits_prior_checks_without_requiring_v41_scalar(self):
        metadata = self.v42_metadata()
        candidate_name = "Kestrel-v42-five-probe-pylon"

        self.assertEqual(scorer._candidate_generation(candidate_name), "v42")
        self.assertEqual(scorer._diagnostic_generation(metadata, candidate_name), "v42")
        self.assertEqual(scorer._diagnostic_generation(metadata), "v42")
        self.assertEqual(scorer._construction_pending_summary(metadata, "Zerg", "v42")["generation"], "v42")
        self.assertEqual(scorer._emergency_episode_summary(metadata, "Zerg", "v42")["generation"], "v42")
        self.assertEqual(scorer._emergency_bridge_summary(metadata, "Zerg", "v42")["generation"], "v42")
        self.assertEqual(scorer._zerg_offense_stage_summary(metadata, "Zerg", "v42")["generation"], "v42")
        self.assertEqual(scorer._scaling_summary(metadata, "v42")["generation"], "v42")
        self.assertEqual(scorer._shared_target_summary(metadata, "Zerg", "v42")["generation"], "v42")
        self.assertEqual(scorer._gateway_probe_summary(metadata, "v42")["generation"], "v42")

        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v42")
        self.assertEqual(summary["generation"], "v42")
        self.assertEqual(summary["v42_treatment"]["quantitative_grade"]["grade"], "pass")
        self.assertEqual(summary["v42_treatment"]["active_frames"], 35)
        self.assertTrue(summary["v42_treatment"]["pylon_accepted"])
        self.assertEqual(summary["v42_treatment"]["pylon_accepted_frame"], metadata["first_pylon_accepted_frame"])
        self.assertIsNone(summary["zerg_pre_pylon_probe_reserve_frames"])
        self.assertNotIn("zerg_pre_pylon_probe_reserve_frames_missing", summary["review_flags"])

    def test_v42_treatment_requires_positive_zerg_activation_and_accepted_pylon(self):
        metadata = self.v42_metadata()
        metadata["zerg_five_probe_policy_active_frames"] = 0
        metadata["zerg_five_probe_pylon_accepted"] = False
        metadata["zerg_five_probe_pylon_accepted_frame"] = -1

        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v42")

        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("v42:zerg_five_probe_policy_active_frames_not_positive", summary["review_flags"])
        self.assertIn("v42:zerg_five_probe_pylon_accepted_not_true", summary["review_flags"])
        self.assertIn("v42:zerg_five_probe_pylon_accepted_frame_negative", summary["review_flags"])

    def test_v42_treatment_requires_complete_scalar_types_and_alignment(self):
        missing = self.v42_metadata()
        del missing["zerg_five_probe_pylon_accepted_frame"]
        missing_summary = scorer._probe_reserve_summary(missing, "Zerg", "v42")
        self.assertEqual(missing_summary["quantitative_grade"]["grade"], "review")
        self.assertIn("v42:zerg_five_probe_pylon_accepted_frame_missing", missing_summary["review_flags"])

        malformed = self.v42_metadata()
        malformed["zerg_five_probe_policy_active_frames"] = True
        malformed["zerg_five_probe_pylon_accepted"] = 1
        malformed_summary = scorer._probe_reserve_summary(malformed, "Zerg", "v42")
        self.assertEqual(malformed_summary["quantitative_grade"]["grade"], "review")
        self.assertIn("v42:zerg_five_probe_policy_active_frames_type_mismatch", malformed_summary["review_flags"])
        self.assertIn("v42:zerg_five_probe_pylon_accepted_type_mismatch", malformed_summary["review_flags"])
        self.assertIn("zerg_five_probe_policy_active_frames", malformed_summary["invalid_fields"])

        mismatch = self.v42_metadata()
        mismatch["zerg_five_probe_pylon_accepted_frame"] += 1
        mismatch_summary = scorer._probe_reserve_summary(mismatch, "Zerg", "v42")
        self.assertEqual(mismatch_summary["quantitative_grade"]["grade"], "review")
        self.assertIn("v42:zerg_five_probe_pylon_accepted_frame_mismatch", mismatch_summary["review_flags"])

    def test_v42_non_zerg_requires_inactive_treatment_sentinels(self):
        metadata = self.v42_metadata()
        metadata.update({
            "zerg_five_probe_policy_active_frames": 0,
            "zerg_five_probe_pylon_accepted": False,
            "zerg_five_probe_pylon_accepted_frame": -1,
            "accepted_probe_train_frames": [],
            "probe_reserve_block_frames": [],
            "probe_reserve_block_minerals": [],
            "opening_probe_reserve": 0,
            "max_opening_probe_reserve": 0,
            "first_probe_reserve_window_frame": -1,
            "probe_reserve_window_end_frame": -1,
            "probe_reserve_block_count": 0,
        })
        summary = scorer._probe_reserve_summary(metadata, "Terran", "v42")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertTrue(summary["v42_treatment"]["checks"]["non_zerg_inactive"])

        metadata["zerg_five_probe_pylon_accepted_frame"] = 0
        summary = scorer._probe_reserve_summary(metadata, "Terran", "v42")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("v42:non_zerg_five_probe_pylon_accepted_frame_not_minus_one", summary["review_flags"])

    def test_v41_generation_retains_all_prior_diagnostic_checks_and_exposes_new_scalar(self):
        metadata = self.v41_metadata()
        candidate_name = "Kestrel-v41-zerg-two-gateway-bank"

        self.assertEqual(scorer._candidate_generation(candidate_name), "v41")
        self.assertEqual(scorer._diagnostic_generation(metadata, candidate_name), "v41")
        self.assertEqual(scorer._diagnostic_generation(metadata), "v41")
        self.assertEqual(scorer._construction_pending_summary(metadata, "Zerg", "v41")["generation"], "v41")
        self.assertEqual(scorer._emergency_episode_summary(metadata, "Zerg", "v41")["generation"], "v41")
        self.assertEqual(scorer._emergency_bridge_summary(metadata, "Zerg", "v41")["generation"], "v41")
        self.assertEqual(scorer._zerg_offense_stage_summary(metadata, "Zerg", "v41")["generation"], "v41")
        self.assertEqual(scorer._scaling_summary(metadata, "v41")["generation"], "v41")
        self.assertEqual(scorer._shared_target_summary(metadata, "Zerg", "v41")["generation"], "v41")
        self.assertEqual(scorer._gateway_probe_summary(metadata, "v41")["generation"], "v41")

        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v41")
        self.assertEqual(summary["generation"], "v41")
        self.assertEqual(summary["zerg_pre_pylon_probe_reserve_frames"], 12)
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertNotIn("zerg_pre_pylon_probe_reserve_frames_missing", summary["review_flags"])

    def test_v41_probe_reserve_requires_positive_zerg_pre_pylon_scalar(self):
        metadata = self.v41_metadata()
        metadata["zerg_pre_pylon_probe_reserve_frames"] = 0

        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v41")

        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("zerg_pre_pylon_probe_reserve_frames_not_positive", summary["review_flags"])

    def test_v41_probe_reserve_requires_scalar_and_rejects_malformed_values(self):
        missing = self.v41_metadata()
        del missing["zerg_pre_pylon_probe_reserve_frames"]
        missing_summary = scorer._probe_reserve_summary(missing, "Zerg", "v41")
        self.assertEqual(missing_summary["telemetry_status"], "partial")
        self.assertEqual(missing_summary["quantitative_grade"]["grade"], "review")
        self.assertIn("zerg_pre_pylon_probe_reserve_frames_missing", missing_summary["review_flags"])

        malformed = self.v41_metadata()
        malformed["zerg_pre_pylon_probe_reserve_frames"] = True
        malformed_summary = scorer._probe_reserve_summary(malformed, "Zerg", "v41")
        self.assertEqual(malformed_summary["quantitative_grade"]["grade"], "review")
        self.assertIn("zerg_pre_pylon_probe_reserve_frames_type_mismatch", malformed_summary["review_flags"])
        self.assertIn("zerg_pre_pylon_probe_reserve_frames", malformed_summary["invalid_fields"])

    def test_v41_probe_reserve_requires_zero_pre_pylon_scalar_for_non_zerg(self):
        metadata = self.v41_metadata()
        metadata.update({
            "accepted_probe_train_frames": [],
            "probe_reserve_block_frames": [],
            "probe_reserve_block_minerals": [],
            "opening_probe_reserve": 0,
            "max_opening_probe_reserve": 0,
            "first_probe_reserve_window_frame": -1,
            "probe_reserve_window_end_frame": -1,
            "probe_reserve_block_count": 0,
            "zerg_pre_pylon_probe_reserve_frames": 0,
        })
        summary = scorer._probe_reserve_summary(metadata, "Terran", "v41")

        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertTrue(summary["checks"]["non_zerg_inactive"])
        self.assertEqual(summary["review_flags"], [])

        metadata["zerg_pre_pylon_probe_reserve_frames"] = 1
        summary = scorer._probe_reserve_summary(metadata, "Terran", "v41")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("non_zerg_pre_pylon_probe_reserve_frames_nonzero", summary["review_flags"])

    def test_v40_probe_reserve_does_not_require_v41_scalar(self):
        summary = scorer._probe_reserve_summary(self.v40_metadata(), "Zerg", "v40")

        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertIsNone(summary["zerg_pre_pylon_probe_reserve_frames"])
        self.assertNotIn("zerg_pre_pylon_probe_reserve_frames_missing", summary["review_flags"])

    def test_v40_generation_and_gateway_probe_summary_prove_two_selections(self):
        metadata = self.v40_metadata()
        self.assertEqual(scorer._candidate_generation("Kestrel-v40-nearest-gateway-probe"), "v40")
        self.assertEqual(scorer._diagnostic_generation(metadata, "Kestrel-v40-nearest-gateway-probe"), "v40")

        summary = scorer._gateway_probe_summary(metadata, "v40")

        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertTrue(summary["proof_sufficient"])
        self.assertEqual(summary["selection_count"], 2)
        self.assertTrue(summary["checks"]["nearest_distance_and_tie_break"])
        self.assertEqual(summary["selections"][1]["builder_id"], 101)
        self.assertEqual(summary["review_flags"], [])

    def test_v40_gateway_probe_rejects_tie_break_and_truncation(self):
        metadata = self.v40_metadata()
        metadata["gateway_probe_selection_builder_ids"] = [102, 101]
        metadata["gateway_probe_selection_candidate_truncated"] = [1, 0]

        summary = scorer._gateway_probe_summary(metadata, "v40")

        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("gateway_probe_selection_row_0_truncated", summary["review_flags"])
        self.assertIn("gateway_probe_selection_row_0_builder_tie_break_failure", summary["review_flags"])

    def test_v40_gateway_probe_requires_complete_aligned_arrays_and_build_frames(self):
        metadata = self.v40_metadata()
        metadata["gateway_probe_candidate_distances"] = [30]
        metadata["accepted_build_frames"] = [20, 51, 75]

        summary = scorer._gateway_probe_summary(metadata, "v40")

        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("gateway_probe_candidate_trace_partition_mismatch", summary["review_flags"])
        self.assertIn("gateway_probe_gateway_build_frame_mismatch_0", summary["review_flags"])

    def test_v40_score_match_and_aggregate_retain_generation_and_proof(self):
        metadata = self.v40_metadata()
        metadata.update({"ended": True, "winner": False, "frame_count": 1000,
                         "command_categories": {}, "rejected_commands": 0})
        candidate_name = "Kestrel-v40-nearest-gateway-probe"
        manifest = {
            "run_id": "v40-gateway-probe-propagation",
            "status": "completed",
            "outcome_verified": True,
            "players": [
                {"player": 1, "name": candidate_name, "return_code": 0, "result_metadata": metadata},
                {"player": 2, "name": "Opponent", "return_code": 0,
                 "environment": {"BWAPI_CONFIG_AUTO_MENU__RACE": "Zerg"},
                 "result_metadata": {"winner": True}},
            ],
            "replays": [],
        }
        result = scorer.score_kestrel_match(manifest, Path("manifest.json"), Path("screp"),
                                            candidate_name=candidate_name)

        self.assertEqual(result["diagnostic"]["telemetry_generation"], "v40")
        self.assertEqual(result["gateway_probe"]["generation"], "v40")
        self.assertTrue(result["gateway_probe"]["proof_sufficient"])
        self.assertEqual(result["gateway_probe"]["quantitative_grade"]["grade"], "pass")
        aggregate = scorer._aggregate_gateway_probe([result["gateway_probe"]])
        self.assertEqual(aggregate["generations"]["v40"], 1)
        self.assertEqual(aggregate["complete_two_selection_games"], 1)
        self.assertEqual(aggregate["selection_rows"], 2)

    def test_v37_scaling_summary_validates_upgrade_caps_and_milestones(self):
        summary = scorer._scaling_summary(self.v37_metadata(), "v37")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertEqual(summary["caps"], {"max_pylons": 10, "max_gateways": 6})
        self.assertTrue(summary["checks"]["milestone_order"])
        self.assertEqual(summary["upgrade"]["range_upgrade_accepted"], 1)

    def test_v37_scaling_without_eligibility_is_untested(self):
        metadata = self.v37_metadata()
        metadata["range_upgrade_eligibility_frame"] = -1
        metadata["range_upgrade_bank_start_frame"] = -1
        metadata["range_upgrade_attempt_frame"] = -1
        metadata["range_upgrade_accepted_frame"] = -1
        metadata["range_upgrade_completion_frame"] = -1
        metadata["range_upgrade_attempts"] = 0
        metadata["range_upgrade_accepted"] = 0
        metadata["range_upgrade_completions"] = 0
        summary = scorer._scaling_summary(metadata, "v37")
        self.assertEqual(summary["quantitative_grade"]["grade"], "untested")
        self.assertIn("range_upgrade_opportunity_unobserved", summary["opportunity_notes"])

    def test_v37_scaling_malformed_required_telemetry_is_review(self):
        metadata = self.v37_metadata()
        del metadata["fifth_gateway_completed_frame"]
        metadata["range_upgrade_accepted"] = 2
        summary = scorer._scaling_summary(metadata, "v37")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("scaling_required_fields_missing", summary["review_flags"])
        self.assertIn("range_upgrade_count_out_of_range", summary["review_flags"])

    def test_v37_scaling_accept_before_terminal_is_partial_not_integrity_review(self):
        metadata = self.v37_metadata()
        metadata["range_upgrade_completion_frame"] = -1
        metadata["range_upgrade_completions"] = 0
        summary = scorer._scaling_summary(metadata, "v37")
        self.assertEqual(summary["quantitative_grade"]["grade"], "partial")
        self.assertEqual(summary["review_flags"], [])
        self.assertIn("range_upgrade_accepted_not_completed_before_terminal", summary["opportunity_notes"])

    def test_v37_scaling_banking_before_terminal_is_partial_not_integrity_review(self):
        metadata = self.v37_metadata()
        metadata["range_upgrade_attempt_frame"] = -1
        metadata["range_upgrade_accepted_frame"] = -1
        metadata["range_upgrade_completion_frame"] = -1
        metadata["range_upgrade_attempts"] = 0
        metadata["range_upgrade_accepted"] = 0
        metadata["range_upgrade_completions"] = 0
        summary = scorer._scaling_summary(metadata, "v37")
        self.assertEqual(summary["quantitative_grade"]["grade"], "partial")
        self.assertEqual(summary["review_flags"], [])
        self.assertIn("range_upgrade_banking_before_terminal", summary["opportunity_notes"])

    def test_v37_scaling_partial_structure_milestone_is_not_integrity_review(self):
        metadata = self.v37_metadata()
        metadata["seventh_pylon_current_frame"] = -1
        metadata["seventh_pylon_completed_frame"] = -1
        summary = scorer._scaling_summary(metadata, "v37")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertEqual(summary["review_flags"], [])
        self.assertIn("seventh_pylon_accepted_not_current_before_terminal", summary["opportunity_notes"])

    def test_v36_candidate_name_retains_v35_and_v34_schema_checks(self):
        metadata = self.v36_metadata()
        self.assertEqual(scorer._diagnostic_generation(metadata), "v35")
        self.assertEqual(scorer._diagnostic_generation(metadata, "Kestrel-v36-opening-reserve"), "v36")

        construction = scorer._construction_pending_summary(metadata, "Zerg", "v36")
        self.assertEqual(construction["generation"], "v36")
        episode = scorer._emergency_episode_summary(metadata, "Zerg", "v36")
        self.assertEqual(episode["generation"], "v36")
        bridge = scorer._emergency_bridge_summary(metadata, "Zerg", "v36")
        self.assertEqual(bridge["generation"], "v36")
        self.assertEqual(bridge["release_threshold"], 3)
        self.assertEqual(bridge["episodes"]["generation"], "v36")
        stage = scorer._zerg_offense_stage_summary(metadata, "Zerg", "v36")
        self.assertEqual(stage["generation"], "v36")

    def test_v37_candidate_retains_v36_v35_and_v34_schema_checks(self):
        metadata = self.v37_metadata()
        self.assertEqual(scorer._diagnostic_generation(metadata, "Kestrel-v37-post-opening-scaling"), "v37")
        self.assertEqual(scorer._construction_pending_summary(metadata, "Zerg", "v37")["generation"], "v37")
        self.assertEqual(scorer._probe_reserve_summary(metadata, "Zerg", "v37")["generation"], "v37")
        self.assertEqual(scorer._emergency_episode_summary(metadata, "Zerg", "v37")["generation"], "v37")
        bridge = scorer._emergency_bridge_summary(metadata, "Zerg", "v37")
        self.assertEqual(bridge["release_threshold"], 3)
        self.assertEqual(bridge["episodes"]["generation"], "v37")
        self.assertEqual(scorer._zerg_offense_stage_summary(metadata, "Zerg", "v37")["generation"], "v37")

    def test_v38_shared_target_summary_validates_aligned_trace_and_counters(self):
        metadata = self.v38_metadata()
        summary = scorer._shared_target_summary(metadata, "Zerg", "v38")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertEqual(summary["counters"]["shared_target_attempts"], 2)
        self.assertTrue(summary["checks"]["trace_aligned"])
        self.assertTrue(summary["checks"]["switches_consistent"])

    def test_v38_shared_target_without_selection_is_untested(self):
        metadata = self.v38_metadata()
        for name in (
            "shared_target_selections", "shared_target_attempts", "shared_target_accepted",
            "shared_target_switches", "shared_target_rejects", "shared_target_correction_opportunities",
        ):
            metadata[name] = 0
        for name in (
            "shared_target_frames", "shared_target_ids", "shared_target_participant_counts",
            "shared_target_eligible_counts", "shared_target_ordered_counts", "shared_target_local_counts",
            "shared_target_attempt_counts", "shared_target_accepted_counts", "shared_target_participant_ids",
        ):
            metadata[name] = []
        summary = scorer._shared_target_summary(metadata, "Zerg", "v38")
        self.assertEqual(summary["quantitative_grade"]["grade"], "untested")
        self.assertIn("shared_target_opportunity_unobserved", summary["opportunity_notes"])

    def test_v38_shared_target_single_participant_is_untested(self):
        metadata = self.v38_metadata()
        metadata["shared_target_participant_counts"] = [1, 1]
        metadata["shared_target_eligible_counts"] = [1, 1]
        metadata["shared_target_ordered_counts"] = [1, 1]
        metadata["shared_target_local_counts"] = [0, 0]
        metadata["shared_target_attempt_counts"] = [1, 1]
        metadata["shared_target_accepted_counts"] = [1, 1]
        metadata["shared_target_participant_ids"] = [10, 10]
        summary = scorer._shared_target_summary(metadata, "Zerg", "v38")
        self.assertEqual(summary["quantitative_grade"]["grade"], "untested")
        self.assertEqual(summary["multi_participant_selections"], 0)
        self.assertIn("shared_target_multi_participant_opportunity_unobserved", summary["opportunity_notes"])

    def test_v38_shared_target_partial_local_count_is_review(self):
        metadata = self.v38_metadata()
        metadata["shared_target_local_counts"] = [1, 0]
        summary = scorer._shared_target_summary(metadata, "Zerg", "v38")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("shared_target_local_count_partial", summary["review_flags"])

    def test_v38_shared_target_multi_participant_without_accept_is_untested(self):
        metadata = self.v38_metadata()
        metadata["shared_target_attempts"] = 0
        metadata["shared_target_accepted"] = 0
        metadata["shared_target_attempt_counts"] = [0, 0]
        metadata["shared_target_accepted_counts"] = [0, 0]
        summary = scorer._shared_target_summary(metadata, "Zerg", "v38")
        self.assertEqual(summary["quantitative_grade"]["grade"], "untested")
        self.assertEqual(summary["multi_participant_selections"], 2)
        self.assertEqual(summary["coordinated_accepted_selections"], 0)
        self.assertIn("shared_target_accepted_command_unobserved", summary["opportunity_notes"])

    def test_v38_shared_target_trailing_participant_id_is_review(self):
        metadata = self.v38_metadata()
        metadata["shared_target_participant_ids"].append(99)
        summary = scorer._shared_target_summary(metadata, "Zerg", "v38")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("shared_target_participant_trace_total_mismatch", summary["review_flags"])

    def test_v38_shared_target_summary_exposes_aggregate_counter_fields(self):
        metadata = self.v38_metadata()
        metadata["shared_target_rejects"] = 0
        metadata["shared_target_illegal_selections"] = 0
        metadata["shared_target_non_zerg_selections"] = 0
        summary = scorer._shared_target_summary(metadata, "Zerg", "v38")
        self.assertEqual(summary["counters"]["shared_target_rejects"], 0)
        self.assertEqual(summary["counters"]["shared_target_illegal_selections"], 0)
        self.assertEqual(summary["counters"]["shared_target_non_zerg_selections"], 0)

    def test_v38_shared_target_malformed_or_divergent_trace_is_review(self):
        metadata = self.v38_metadata()
        del metadata["shared_target_ids"]
        metadata["shared_target_correction_opportunities"] = 1
        summary = scorer._shared_target_summary(metadata, "Zerg", "v38")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("shared_target_required_fields_missing", summary["review_flags"])
        self.assertEqual(summary["counters"]["shared_target_correction_opportunities"], 1)

    def test_v38_shared_target_malformed_row_counts_return_review(self):
        metadata = self.v38_metadata()
        metadata["shared_target_participant_counts"] = ["bad", {"count": 2}]
        metadata["shared_target_eligible_counts"] = [2, 2]
        summary = scorer._shared_target_summary(metadata, "Zerg", "v38")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("shared_target_count_invalid", summary["review_flags"])

    def test_v38_shared_target_unhashable_participant_ids_return_review(self):
        metadata = self.v38_metadata()
        metadata["shared_target_participant_ids"] = [[10], 11, 10, 11]
        summary = scorer._shared_target_summary(metadata, "Zerg", "v38")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("shared_target_participant_id_type_mismatch", summary["review_flags"])

    def test_v38_shared_target_negative_correction_opportunities_return_review(self):
        metadata = self.v38_metadata()
        metadata["shared_target_correction_opportunities"] = -1
        summary = scorer._shared_target_summary(metadata, "Zerg", "v38")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("shared_target_negative_counter_correction_opportunities", summary["review_flags"])

    def test_v38_candidate_retains_prior_schema_checks_and_generation(self):
        metadata = self.v38_metadata()
        self.assertEqual(scorer._diagnostic_generation(metadata, "Kestrel-v38-shared-target"), "v38")
        self.assertEqual(scorer._construction_pending_summary(metadata, "Zerg", "v38")["generation"], "v38")
        self.assertEqual(scorer._probe_reserve_summary(metadata, "Zerg", "v38")["generation"], "v38")
        self.assertEqual(scorer._emergency_episode_summary(metadata, "Zerg", "v38")["generation"], "v38")
        self.assertEqual(scorer._zerg_offense_stage_summary(metadata, "Zerg", "v38")["generation"], "v38")
        self.assertEqual(scorer._scaling_summary(metadata, "v38")["generation"], "v38")

    def test_score_match_propagates_v38_shared_target_to_game(self):
        metadata = self.v38_metadata()
        metadata.update({"ended": True, "winner": False, "frame_count": 1000,
                         "command_categories": {}, "rejected_commands": 0})
        candidate_name = "Kestrel-v38-shared-target"
        manifest = {
            "run_id": "v38-shared-target-propagation",
            "status": "completed",
            "outcome_verified": True,
            "players": [
                {"player": 1, "name": candidate_name, "return_code": 0, "result_metadata": metadata},
                {"player": 2, "name": "Opponent", "return_code": 0,
                 "environment": {"BWAPI_CONFIG_AUTO_MENU__RACE": "Zerg"},
                 "result_metadata": {"winner": True}},
            ],
            "replays": [],
        }
        result = scorer.score_kestrel_match(manifest, Path("manifest.json"), Path("screp"),
                                            candidate_name=candidate_name)
        self.assertEqual(result["shared_target"]["generation"], "v38")
        self.assertEqual(result["shared_target"]["multi_participant_selections"], 2)
        self.assertEqual(result["shared_target"]["coordinated_accepted_selections"], 1)

    def test_v36_probe_reserve_summary_checks_alignment_window_and_resumption(self):
        summary = scorer._probe_reserve_summary(self.v36_metadata(), "Zerg", "v36")
        self.assertEqual(summary["generation"], "v36")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertEqual(summary["reserve_blocks"]["count"], 2)
        self.assertTrue(summary["checks"]["probe_train_absence"])
        self.assertTrue(summary["checks"]["post_window_resumption"])

    def test_v36_probe_reserve_window_allows_next_cadence_after_gateway_current(self):
        metadata = self.v36_metadata()
        metadata["latency_frames"] = 3
        metadata["probe_reserve_window_end_frame"] = 155
        metadata["accepted_probe_train_frames"] = [40, 155]
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v36")
        self.assertTrue(summary["checks"]["window_ordered"])
        self.assertTrue(summary["checks"]["post_window_resumption"])

        metadata["probe_reserve_window_end_frame"] = 156
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v36")
        self.assertIn("probe_reserve_window_end_delayed", summary["review_flags"])

    def test_v36_probe_reserve_without_block_opportunity_is_untested(self):
        metadata = self.v36_metadata()
        metadata["probe_reserve_block_frames"] = []
        metadata["probe_reserve_block_minerals"] = []
        metadata["probe_reserve_block_count"] = 0
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v36")
        self.assertEqual(summary["quantitative_grade"]["grade"], "untested")
        self.assertIn("reserve_block_opportunity_unobserved", summary["opportunity_notes"])

    def test_v36_probe_reserve_summary_rejects_bad_minerals_and_non_zerg_activity(self):
        metadata = self.v36_metadata()
        metadata["probe_reserve_block_minerals"] = [199, 300]
        metadata["max_opening_probe_reserve"] = 0
        summary = scorer._probe_reserve_summary(metadata, "Terran", "v36")
        self.assertIn("probe_reserve_block_minerals_out_of_range", summary["review_flags"])
        self.assertIn("non_zerg_probe_reserve_activity", summary["review_flags"])
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")

    def test_v36_missing_reserve_telemetry_is_reviewable(self):
        summary = scorer._probe_reserve_summary(self.v35_metadata(), "Zerg", "v36")
        self.assertEqual(summary["generation"], "v36")
        self.assertEqual(summary["telemetry_status"], "partial")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("probe_reserve_required_fields_missing", summary["review_flags"])

    def test_v35_extracts_construction_baselines_and_episode_trace(self):
        metadata = self.v35_metadata()

        construction = scorer._construction_pending_summary(metadata, "Zerg")
        self.assertEqual(construction["generation"], "v35")
        self.assertEqual(construction["quantitative_grade"]["grade"], "pass")
        self.assertEqual(construction["accepted_builds"]["rows"][1], {
            "index": 1, "accepted_frame": 50, "type_id": 160,
            "pre_command_count": 0, "post_command_count": 0,
        })
        self.assertEqual(construction["accepted_builds"]["second_gateway_accepted_frame"], 75)
        self.assertTrue(construction["checks"]["gateway_sequence_observed"])
        self.assertEqual(construction["timing"]["second_gateway_current_frame"], 90)

        episode = scorer._emergency_episode_summary(metadata, "Zerg")
        self.assertEqual(episode["quantitative_grade"]["grade"], "pass")
        self.assertEqual(episode["episodes"], [{"index": 0, "id": 1, "start_frame": 90,
                                                  "reset_frame": 250, "assignment_count": 2}])
        self.assertEqual(episode["reset_frames"], [250])
        self.assertEqual(episode["assignments"]["batches"][0]["episode_id"], 1)
        self.assertTrue(episode["checks"]["per_episode_cap"])
        self.assertTrue(episode["checks"]["cap_block_alignment"])

        bridge = scorer._emergency_bridge_summary(metadata, "Zerg")
        self.assertEqual(bridge["generation"], "v35")
        self.assertEqual(bridge["release_threshold"], 3)
        self.assertEqual(bridge["episodes"]["assignment_cap"], 2)
        self.assertTrue(bridge["checks"]["episode_state_consistent"])

    def test_v35_episode_aggregate_counts_list_shaped_assignment_ids(self):
        aggregate = scorer._aggregate_emergency_episode_summaries([{
            "episodes": [{"index": 0, "id": 1, "start_frame": 90, "reset_frame": 250,
                          "assignment_count": 2}],
            "assignments": {"episode_ids": [1, 1]},
            "cap_blocks": {"total": 1},
            "quantitative_grade": {"grade": "pass"},
            "review_flags": [],
        }])

        self.assertEqual(aggregate["episode_count"], 1)
        self.assertEqual(aggregate["assignments"], 2)
        self.assertEqual(aggregate["review_flags"], {})

    def test_v35_episode_summary_rejects_duplicate_probe_and_misaligned_cap_trace(self):
        metadata = self.v35_metadata()
        metadata["emergency_assigned_probe_ids"] = [101, 101]
        metadata["emergency_episode_cap_block_counts"] = [1]

        summary = scorer._emergency_episode_summary(metadata, "Zerg")

        self.assertIn("episode_assignment_ids_duplicate", summary["review_flags"])
        self.assertIn("episode_cap_block_below_cap", summary["review_flags"])
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")

    def test_v35_non_zerg_episode_and_construction_fields_must_be_inactive(self):
        metadata = self.v35_metadata()
        metadata["known_zerg"] = False
        for name in (
            "emergency_trigger_frame", "emergency_first_assignment_frame", "emergency_first_release_frame",
            "emergency_first_threat_clear_release_frame", "emergency_first_army_three_release_frame",
            "emergency_army_at_trigger", "emergency_local_combat_at_trigger",
        ):
            metadata[name] = -1
        for name in (
            "emergency_trigger_events", "emergency_assignments", "emergency_assignment_batches",
            "emergency_first_assignment_size", "emergency_max_assignment_batch", "emergency_peak_defenders",
            "emergency_current_defenders", "emergency_accepted_attack_orders", "emergency_releases",
            "emergency_threat_clear_release_events", "emergency_threat_clear_released_defenders",
            "emergency_army_three_release_events", "emergency_army_three_released_defenders", "emergency_defender_deaths",
            "emergency_build_selection_exclusions", "emergency_economy_exclusions",
            "emergency_post_release_gather_orders", "emergency_post_release_build_orders",
            "emergency_episode_current_id", "emergency_episode_current_assignment_count", "emergency_episode_cap_blocks",
        ):
            metadata[name] = 0
        metadata.update({
            "emergency_episode_threat_present": False,
            "emergency_assigned_probe_ids": [], "emergency_assignment_frames": [], "emergency_assignment_sizes": [],
            "emergency_release_frames": [], "emergency_release_sizes": [], "emergency_release_army_three_flags": [],
            "emergency_episode_ids": [], "emergency_episode_start_frames": [], "emergency_episode_reset_frames": [],
            "emergency_episode_assignment_counts": [], "emergency_episode_cap_block_frames": [],
            "emergency_episode_cap_block_counts": [], "emergency_assignment_episode_ids": [],
        })
        construction = scorer._construction_pending_summary(metadata, "Terran")
        episode = scorer._emergency_episode_summary(metadata, "Terran")
        self.assertTrue(episode["checks"]["non_zerg_inactive"])
        self.assertEqual(episode["quantitative_grade"]["grade"], "pass")
        self.assertEqual(construction["quantitative_grade"]["grade"], "pass")

    def test_v33_emergency_bridge_exposes_batches_reasons_exclusions_and_recovery(self):
        summary = scorer._emergency_bridge_summary(self.v33_metadata(), "Zerg")

        self.assertEqual(summary["telemetry_status"], "complete")
        self.assertEqual(summary["assignments"]["batch_trace"], [
            {"index": 0, "frame": 100, "size": 2, "probe_ids": [101, 102]},
            {"index": 1, "frame": 120, "size": 1, "probe_ids": [103]},
        ])
        self.assertEqual(summary["releases"]["reason_counts"], {"threat_clear": 1, "army_two": 1, "unknown": 0})
        self.assertEqual(summary["exclusions"], {"build_selection": 2, "economy": 3, "total": 5})
        self.assertEqual(summary["recovery"]["status"], "observed")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertEqual(summary["review_flags"], [])

    def test_v33_non_zerg_emergency_telemetry_requires_zero_and_sentinel_values(self):
        metadata = self.v33_metadata()
        for name in (
            "emergency_trigger_frame", "emergency_first_assignment_frame", "emergency_first_release_frame",
            "emergency_first_threat_clear_release_frame", "emergency_first_army_two_release_frame",
            "emergency_army_at_trigger", "emergency_local_combat_at_trigger",
        ):
            metadata[name] = -1
        for name in (
            "emergency_trigger_events", "emergency_assignments", "emergency_assignment_batches",
            "emergency_first_assignment_size", "emergency_max_assignment_batch", "emergency_peak_defenders",
            "emergency_current_defenders", "emergency_accepted_attack_orders", "emergency_releases",
            "emergency_threat_clear_release_events", "emergency_threat_clear_released_defenders",
            "emergency_army_two_release_events", "emergency_army_two_released_defenders", "emergency_defender_deaths",
            "emergency_build_selection_exclusions", "emergency_economy_exclusions",
            "emergency_post_release_gather_orders", "emergency_post_release_build_orders",
        ):
            metadata[name] = 0
        metadata.update({
            "emergency_assigned_probe_ids": [], "emergency_assignment_frames": [], "emergency_assignment_sizes": [],
            "emergency_release_frames": [], "emergency_release_sizes": [], "emergency_release_army_two_flags": [],
        })

        summary = scorer._emergency_bridge_summary(metadata, "Terran")

        self.assertTrue(summary["checks"]["non_zerg_sentinels"])
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertEqual(summary["review_flags"], [])

    def test_v33_emergency_bridge_flags_scalar_trace_inconsistencies_for_review(self):
        metadata = self.v33_metadata()
        metadata["emergency_assignments"] = 2

        summary = scorer._emergency_bridge_summary(metadata, "Zerg")

        self.assertIn("assignment_total_id_count_mismatch", summary["review_flags"])
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")

    def test_v33_trigger_without_eligible_probe_is_an_opportunity_note(self):
        metadata = self.v33_metadata()
        for name in (
            "emergency_first_assignment_frame", "emergency_first_release_frame",
            "emergency_first_threat_clear_release_frame", "emergency_first_army_two_release_frame",
        ):
            metadata[name] = -1
        for name in (
            "emergency_assignments", "emergency_assignment_batches", "emergency_first_assignment_size",
            "emergency_max_assignment_batch", "emergency_peak_defenders", "emergency_current_defenders",
            "emergency_accepted_attack_orders", "emergency_releases", "emergency_threat_clear_release_events",
            "emergency_threat_clear_released_defenders", "emergency_army_two_release_events",
            "emergency_army_two_released_defenders", "emergency_build_selection_exclusions",
            "emergency_economy_exclusions", "emergency_post_release_gather_orders",
            "emergency_post_release_build_orders",
        ):
            metadata[name] = 0
        metadata.update({
            "emergency_assigned_probe_ids": [], "emergency_assignment_frames": [], "emergency_assignment_sizes": [],
            "emergency_release_frames": [], "emergency_release_sizes": [], "emergency_release_army_two_flags": [],
        })

        summary = scorer._emergency_bridge_summary(metadata, "Zerg")

        self.assertEqual(summary["opportunity_notes"], ["trigger_without_assignment"])
        self.assertEqual(summary["review_flags"], [])
        self.assertEqual(summary["quantitative_grade"]["grade"], "untested")

    def test_v34_extracts_army_three_release_and_staged_offense_trace(self):
        metadata = self.v34_metadata()

        bridge = scorer._emergency_bridge_summary(metadata, "Zerg")
        self.assertEqual(bridge["generation"], "v34")
        self.assertEqual(bridge["release_threshold"], 3)
        self.assertEqual(bridge["releases"]["reason_counts"], {"threat_clear": 0, "army_three": 1, "unknown": 0})
        self.assertEqual(bridge["releases"]["army_three_events"], 1)
        self.assertEqual(bridge["quantitative_grade"]["grade"], "pass")
        self.assertEqual(bridge["review_flags"], [])

        stage = scorer._zerg_offense_stage_summary(metadata, "Zerg")
        self.assertEqual(stage["generation"], "v34")
        self.assertEqual(stage["state"]["codes"], [0, 0, 1, 1])
        self.assertEqual(stage["state"]["cause_codes"], [0, 0, 2, 0])
        self.assertEqual(stage["release"]["unit_ids"], [201, 202, 203, 204, 205, 206])
        self.assertEqual(stage["remote_offense"]["pre_release_blocks"], 2)
        self.assertEqual(stage["home_moves"]["min_accepted_repeat_interval"], 96)
        self.assertEqual(stage["quantitative_grade"]["grade"], "pass")
        self.assertEqual(stage["review_flags"], [])

    def test_v34_unexercised_threshold_is_untested_without_review_flag(self):
        metadata = self.v34_metadata()
        for name in (
            "zerg_offense_stage_released", "zerg_offense_stage_remote_target_events",
            "zerg_offense_stage_unique_units", "zerg_offense_stage_pre_release_remote_blocks",
            "zerg_offense_stage_pre_release_remote_attempts", "zerg_offense_stage_home_move_attempts",
            "zerg_offense_stage_home_move_orders", "zerg_offense_stage_home_move_accepts",
            "zerg_offense_stage_home_move_repeat_orders",
            "zerg_offense_stage_home_target_orders", "zerg_offense_stage_release_events",
            "zerg_offense_stage_reset_events", "zerg_offense_stage_restage_events",
            "zerg_offense_stage_peak_surplus", "zerg_offense_stage_current_surplus",
        ):
            metadata[name] = False if name == "zerg_offense_stage_released" else 0
        metadata.update({
            "first_zerg_offense_stage_frame": 100,
            "first_zerg_offense_stage_suppression_frame": -1,
            "first_zerg_offense_stage_threshold_frame": -1,
            "first_zerg_offense_stage_release_frame": -1,
            "zerg_offense_stage_release_army": -1,
            "zerg_offense_stage_release_surplus": -1,
            "zerg_offense_stage_release_unit_ids": [],
            "zerg_offense_stage_state_frames": [0, 100],
            "zerg_offense_stage_state_army": [0, 3],
            "zerg_offense_stage_state_reserve": [0, 3],
            "zerg_offense_stage_state_surplus": [0, 2],
            "zerg_offense_stage_state_codes": [0, 0],
            "zerg_offense_stage_state_cause_codes": [0, 0],
        })
        metadata["zerg_offense_stage_current_surplus"] = 2
        stage = scorer._zerg_offense_stage_summary(metadata, "Zerg")
        self.assertEqual(stage["quantitative_grade"]["grade"], "untested")
        self.assertIn("threshold_six_unobserved", stage["opportunity_notes"])
        self.assertEqual(stage["review_flags"], [])

    def test_v34_non_zerg_stage_fields_must_remain_inactive(self):
        metadata = self.v34_metadata()
        for name, value in list(metadata.items()):
            if name.startswith("zerg_offense_stage_"):
                if isinstance(value, bool):
                    metadata[name] = False
                elif isinstance(value, list):
                    metadata[name] = []
                elif isinstance(value, str):
                    metadata[name] = "none"
                elif "frame" in name or name.endswith(("army", "surplus", "interval")):
                    metadata[name] = -1
                else:
                    metadata[name] = 0
        for name in (
            "first_zerg_offense_stage_suppression_frame", "first_zerg_offense_stage_frame",
            "first_zerg_offense_stage_threshold_frame", "first_zerg_offense_stage_release_frame",
            "first_zerg_offense_stage_reset_frame",
        ):
            metadata[name] = -1
        metadata["zerg_offense_stage_current_surplus"] = 0
        metadata["zerg_offense_stage_peak_surplus"] = 0
        metadata["zerg_offense_stage_release_surplus"] = -1
        stage = scorer._zerg_offense_stage_summary(metadata, "Terran")
        self.assertTrue(stage["checks"]["non_zerg_sentinels"])
        self.assertEqual(stage["quantitative_grade"]["grade"], "pass")
        self.assertEqual(stage["review_flags"], [])

    def test_diagnostic_summary_collects_scalars_and_optional_events(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            metadata_path = root / "bwapi-data" / "write" / "diagnostic.json"
            metadata_path.parent.mkdir(parents=True)
            metadata_path.write_text("{}\n")
            (metadata_path.parent / "kestrel-diagnostic.jsonl").write_text(
                '{"record":"event","event":"first_home_threat","frame":120}\n'
                '{"record":"event","event":"accepted_command","command":"train","frame":130}\n'
            )
            metadata = {
                "schema_version": 1,
                "metadata_path": str(metadata_path),
                "frame_count": 900,
                "command_categories": {"train": [4, 1], "build": [2, 0]},
                "rejected_commands": 1,
                "first_home_threat_frame": 120,
                "first_home_combat_loss_frame": 240,
                "first_early_zerg_stage_suppression_frame": 100,
                "early_zerg_stage_home_move_orders": 3,
                "early_zerg_stage_remote_attack_orders": 1,
                "zerg_reserve_peak": 3,
                "zerg_reserve_remote_order_blocks": 2,
                "zerg_first_reserve_three_frame": 300,
                "zerg_reserved_local_at_first_home_threat": 2,
                "zerg_first_accepted_surplus_release_frame": 500,
                "zerg_first_accepted_surplus_release_army": 4,
                "zerg_nonreserve_remote_attack_orders": 1,
            }

            summary = scorer._diagnostic_summary(metadata, root)

            self.assertEqual(summary["attempted_commands"], 6)
            self.assertEqual(summary["rejected_commands"], 1)
            self.assertAlmostEqual(summary["rejection_rate"], 1 / 6)
            self.assertEqual(summary["defense"]["first_home_threat_frame"], 120)
            self.assertEqual(summary["reserve_offense"]["remote_attack_orders"], 1)
            self.assertEqual(summary["reserve_offense"]["zerg_reserve_peak"], 3)
            self.assertEqual(summary["reserve_offense"]["zerg_reserve_remote_order_blocks"], 2)
            self.assertEqual(summary["reserve_offense"]["zerg_first_reserve_three_frame"], 300)
            self.assertEqual(summary["reserve_offense"]["zerg_reserved_local_at_first_home_threat"], 2)
            self.assertEqual(summary["reserve_offense"]["zerg_first_accepted_surplus_release_frame"], 500)
            self.assertEqual(summary["reserve_offense"]["zerg_first_accepted_surplus_release_army"], 4)
            self.assertEqual(summary["reserve_offense"]["zerg_nonreserve_remote_attack_orders"], 1)
            self.assertEqual(summary["emergency_bridge"]["telemetry_status"], "legacy_absent")
            self.assertTrue(summary["events"]["parse_ok"])
            self.assertEqual(summary["events"]["first_frames"]["first_home_threat"], 120)

    def test_parse_replay_reports_parse_and_archival_inputs(self):
        with TemporaryDirectory() as directory:
            replay = Path(directory) / "game.rep"
            replay.write_bytes(b"replay")
            payload = {
                "Header": {"Frames": 98},
                "Commands": {
                    "Cmds": [
                        {"Type": {"Name": "Train"}, "Order": {"Name": "Train"}, "Frame": 10,
                         "Unit": {"Name": "Probe"}},
                        {"Type": {"Name": "Build"}, "Order": {"Name": "PlaceProtossBuilding"}, "Frame": 20,
                         "Unit": {"Name": "Pylon"}},
                    ],
                    "ParseErrCmds": [],
                },
            }

            def fake_run(command, *, stdout, stderr, text, check):
                json.dump(payload, stdout)
                stdout.flush()
                return SimpleNamespace(returncode=0, stderr="")

            with patch.object(scorer.subprocess, "run", side_effect=fake_run):
                result = scorer.parse_replay(replay, Path("screp"))

            self.assertTrue(result["json_valid"])
            self.assertEqual(result["size_bytes"], 6)
            self.assertEqual(result["frames"], 98)
            self.assertEqual(result["command_count"], 2)
            self.assertEqual(result["parse_error_commands"], [])

    def test_parse_replay_filters_command_signals_without_losing_whole_replay_count(self):
        with TemporaryDirectory() as directory:
            replay = Path(directory) / "game.rep"
            replay.write_bytes(b"replay")
            payload = {
                "Header": {"Frames": 98, "Players": [
                    {"ID": 0, "Name": "Kestrel-v1"},
                    {"ID": 2, "Name": "Opponent Z"},
                ]},
                "Commands": {"Cmds": [
                    {"PlayerID": 0, "Type": {"Name": "Build"}, "Order": {"Name": "PlaceProtossBuilding"}, "Frame": 10,
                     "Unit": {"Name": "Pylon"}},
                    {"PlayerID": 0, "Type": {"Name": "Train"}, "Order": {"Name": "Train"}, "Frame": 20,
                     "Unit": {"Name": "Probe"}},
                    {"PlayerID": 2, "Type": {"Name": "Targeted Order"}, "Order": {"Name": "AttackMove"}, "Frame": 30},
                    {"PlayerID": 2, "Type": {"Name": "Targeted Order"}, "Order": {"Name": "Harvest1"}, "Frame": 40},
                ], "ParseErrCmds": []},
            }

            def fake_run(command, *, stdout, stderr, text, check):
                json.dump(payload, stdout)
                stdout.flush()
                return SimpleNamespace(returncode=0, stderr="")

            with patch.object(scorer.subprocess, "run", side_effect=fake_run):
                whole = scorer.parse_replay(replay, Path("screp"))
                candidate = scorer.parse_replay(replay, Path("screp"), player_id=0)

            self.assertEqual(whole["command_count"], 4)
            self.assertEqual(whole["whole_replay_command_count"], 4)
            self.assertEqual(candidate["command_count"], 2)
            self.assertEqual(candidate["whole_replay_command_count"], 4)
            self.assertEqual(candidate["attack_orders"], 0)
            self.assertEqual(candidate["build_units"], ["Pylon"])
            self.assertEqual(candidate["command_filter_status"], "filtered")

    def test_replay_owner_resolution_stays_unresolved_when_header_identity_is_ambiguous(self):
        parsed = {"header": {"Players": [
            {"ID": 0, "Name": "bwapi", "Race": {"Name": "Protoss"}},
            {"ID": 2, "Name": "bwapi", "Race": {"Name": "Protoss"}},
        ]}}
        candidate = {"player": 1, "name": "Kestrel-v1", "environment": {"BWAPI_CONFIG_AUTO_MENU__RACE": "Protoss"}}
        opponent = {"player": 2, "name": "Opponent", "environment": {"BWAPI_CONFIG_AUTO_MENU__RACE": "Protoss"}}

        resolution = scorer._resolve_replay_command_owner(parsed, candidate, [candidate, opponent], "Kestrel-v1")

        self.assertEqual(resolution["status"], "unresolved")
        self.assertIsNone(resolution["player_id"])
        self.assertEqual(resolution["reason"], "no_verified_header_owner")

    def test_score_match_uses_filtered_candidate_commands_and_keeps_whole_parse(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            diagnostic_path = root / "diagnostic.json"
            metadata = {"schema_version": 1, "bot": "Kestrel", "ended": True, "winner": False,
                        "frame_count": 1000, "command_categories": {"build": [1, 0], "train": [1, 0]},
                        "rejected_commands": 0}
            diagnostic_path.write_text(json.dumps(metadata) + "\n")
            candidate_replay = root / "candidate.rep"
            opponent_replay = root / "opponent.rep"
            candidate_replay.write_bytes(b"candidate")
            opponent_replay.write_bytes(b"opponent")

            def replay_record(player, path):
                return {"player": player, "path": str(path),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "size_bytes": path.stat().st_size, "archival_status": "copied"}

            players = [
                {"player": 1, "name": "Kestrel-v1", "return_code": 0,
                 "environment": {"BWAPI_CONFIG_AUTO_MENU__CHARACTER_NAME": "Kestrel-v1 Pr",
                                  "BWAPI_CONFIG_AUTO_MENU__RACE": "Protoss"},
                 "result_metadata": metadata},
                {"player": 2, "name": "Opponent", "return_code": 0,
                 "environment": {"BWAPI_CONFIG_AUTO_MENU__CHARACTER_NAME": "Opponent Z",
                                  "BWAPI_CONFIG_AUTO_MENU__RACE": "Zerg"},
                 "result_metadata": {"winner": True}},
            ]
            manifest = {"run_id": "owner-filter", "status": "completed", "outcome_verified": True,
                        "players": players, "replays": [replay_record(1, candidate_replay), replay_record(2, opponent_replay)]}

            def fake_parse(path, screp, player_id=None):
                filtered = player_id is not None
                return {"path": str(path), "exists": True, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "size_bytes": path.stat().st_size, "screp_exit_code": 0, "json_valid": True,
                        "parse_error_commands": [], "frames": 999, "whole_replay_command_count": 4,
                        "command_count": 2 if filtered else 4,
                        "heuristic_grade": "partial" if filtered else "strong",
                        "heuristic_score": 50 if filtered else 100,
                        "signals": {"economy": True, "construction": True, "production": True, "combat": filtered},
                        "header": {"Players": [{"ID": 0, "Name": "Kestrel-v1 Pr"},
                                                   {"ID": 2, "Name": "Opponent Z"}]},
                        "header_players": [{"ID": 0, "Name": "Kestrel-v1 Pr"},
                                           {"ID": 2, "Name": "Opponent Z"}],
                        "command_owner_id": player_id}

            with patch.object(scorer, "parse_replay", side_effect=fake_parse):
                result = scorer.score_kestrel_match(manifest, root / "manifest.json", Path("screp"),
                                                    candidate_name="Kestrel-v1", root=root)

            self.assertEqual(result["candidate_replay_owner_resolution"]["status"], "resolved_exact_name")
            self.assertEqual(result["candidate_replay_owner_resolution"]["player_id"], 0)
            self.assertEqual(result["replay"]["heuristic_score"], 50)
            self.assertEqual(result["replay"]["heuristic_status"], "owner_filtered")
            self.assertEqual(result["replay_whole"]["heuristic_score"], 100)
            self.assertEqual(result["replays"][1]["command_owner_resolution"]["player_id"], 2)

    def test_score_match_combines_integrity_outcome_defense_and_replay_fidelity(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            diagnostic_path = root / "diagnostic.json"
            diagnostic_path.write_text("{}\n")
            candidate_replay = root / "candidate.rep"
            opponent_replay = root / "opponent.rep"
            candidate_replay.write_bytes(b"candidate")
            opponent_replay.write_bytes(b"opponent")

            def replay_record(player, path):
                return {"player": player, "path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "size_bytes": path.stat().st_size, "archival_status": "copied"}

            metadata = {
                "schema_version": 1,
                "bot": "Kestrel",
                "metadata_path": str(diagnostic_path),
                "ended": True,
                "winner": False,
                "frame_count": 1000,
                "command_categories": {"build": [2, 0], "train": [8, 0], "gather": [4, 0], "attack": [5, 0]},
                "rejected_commands": 0,
                "max_probes": 10,
                "max_gateways": 2,
                "max_zealots": 3,
                "first_home_army_threat_frame": 600,
                "first_home_threat_frame": 600,
                "first_home_combat_loss_frame": 800,
                "local_combat_at_first_home_army_threat": 2,
                "global_combat_at_first_home_army_threat": 3,
                "first_early_zerg_stage_suppression_frame": 500,
                "early_zerg_stage_home_move_orders": 4,
                "early_zerg_stage_remote_attack_orders": 0,
            }
            diagnostic_path.write_text(json.dumps(metadata) + "\n")
            manifest = {
                "run_id": "run-1",
                "status": "completed",
                "outcome_verified": True,
                "elapsed_seconds": 2,
                "durable_completion_seconds": 2.1,
                "durable_logical_frames_per_wall_second": 500,
                "inputs": {"map": {"configured_path": "map.scx"}},
                "players": [
                    {"player": 1, "name": "Kestrel-v1", "return_code": 0, "result_metadata": metadata},
                    {"player": 2, "name": None, "return_code": 0,
                     "environment": {"BWAPI_CONFIG_AUTO_MENU__RACE": "Terran"},
                     "result_metadata": {"winner": True}},
                ],
                "replays": [replay_record(1, candidate_replay), replay_record(2, opponent_replay)],
            }
            parsed = {
                "path": "unused",
                "exists": True,
                "sha256": "",
                "size_bytes": 0,
                "screp_exit_code": 0,
                "json_valid": True,
                "parse_error_commands": [],
                "frames": 999,
                "heuristic_grade": "strong",
                "heuristic_score": 100,
                "signals": {"economy": True, "construction": True, "production": True, "combat": True},
            }

            def fake_parse(path, screp):
                value = dict(parsed)
                value["path"] = str(path)
                value["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                value["size_bytes"] = path.stat().st_size
                return value

            with patch.object(scorer, "parse_replay", side_effect=fake_parse):
                result = scorer.score_kestrel_match(manifest, root / "manifest.json", Path("screp"),
                                                    root=root, record={"opponent": "Opponent fallback"})

            self.assertEqual(result["candidate_outcome"], "loss")
            self.assertEqual(result["integrity"]["grade"], "valid")
            self.assertTrue(result["integrity"]["all_replays_hash_match"])
            self.assertTrue(result["integrity"]["all_replays_parse_ok"])
            self.assertEqual(result["survival"]["threat_to_loss_frames"], 200)
            self.assertEqual(result["defense"]["local_combat_at_first_home_army_threat"], 2)
            self.assertEqual(result["reserve_offense"]["home_move_orders"], 4)
            self.assertEqual(result["opponent_race"], "terran")
            self.assertEqual(result["opponent"], "Opponent fallback")
            self.assertTrue(result["emergency_bridge"]["expected_inactive"])
            self.assertEqual(len(result["replays"]), 2)

    def test_score_match_exposes_v36_probe_reserve_and_integrity_review(self):
        metadata = self.v36_metadata()
        metadata.pop("max_opening_probe_reserve")
        candidate_name = "Kestrel-v36-opening-reserve"
        manifest = {
            "run_id": "v36-reserve-review",
            "status": "completed",
            "outcome_verified": True,
            "players": [
                {"player": 1, "name": candidate_name, "return_code": 0, "result_metadata": metadata},
                {"player": 2, "name": "ZZZK-v1", "return_code": 0,
                 "environment": {"BWAPI_CONFIG_AUTO_MENU__RACE": "Zerg"},
                 "result_metadata": {"winner": True}},
            ],
            "replays": [],
        }
        result = scorer.score_kestrel_match(manifest, Path("manifest.json"), Path("screp"),
                                            candidate_name=candidate_name)

        self.assertEqual(result["probe_reserve"]["generation"], "v36")
        self.assertIn("probe_reserve_required_fields_missing", result["probe_reserve"]["review_flags"])
        self.assertIn("probe_reserve_review", result["integrity"]["reasons"])
