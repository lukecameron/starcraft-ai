import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from scripts import score_kestrel_hillclimb as scorer


class KestrelScorecardTests(TestCase):
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
                    {"player": 2, "name": "Opponent", "return_code": 0, "result_metadata": {"winner": True}},
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
            self.assertEqual(len(result["replays"]), 2)
