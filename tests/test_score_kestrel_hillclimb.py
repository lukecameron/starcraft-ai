import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from scripts import score_kestrel_hillclimb as scorer


class KestrelScorecardTests(TestCase):
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
                    {"player": 2, "name": "Opponent", "return_code": 0,
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
                result = scorer.score_kestrel_match(manifest, root / "manifest.json", Path("screp"), root=root)

            self.assertEqual(result["candidate_outcome"], "loss")
            self.assertEqual(result["integrity"]["grade"], "valid")
            self.assertTrue(result["integrity"]["all_replays_hash_match"])
            self.assertTrue(result["integrity"]["all_replays_parse_ok"])
            self.assertEqual(result["survival"]["threat_to_loss_frames"], 200)
            self.assertEqual(result["defense"]["local_combat_at_first_home_army_threat"], 2)
            self.assertEqual(result["reserve_offense"]["home_move_orders"], 4)
            self.assertEqual(result["opponent_race"], "terran")
            self.assertTrue(result["emergency_bridge"]["expected_inactive"])
            self.assertEqual(len(result["replays"]), 2)
