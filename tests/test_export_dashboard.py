import json
import tempfile
import unittest
from pathlib import Path

from scripts.export_dashboard import absolutize_replays, architecture_systems, export, identity_for, public_manifest


class ExportDashboardTest(unittest.TestCase):
    def test_binary_sha_overrides_family_identity_and_unknown_falls_back(self):
        identities = {"McRave.dylib": {"ownership": "project", "origin": "port", "upstream_name": "McRave", "author": "Christian McCrave", "source_url": "https://github.com/Cmccrave/McRave", "sha256_overrides": {"fork-sha": {"origin": "fork", "author": None}}}}
        self.assertEqual(identity_for("McRave.dylib", identities, "port-sha")["origin"], "port")
        fork = identity_for("McRave.dylib", identities, "fork-sha")
        self.assertEqual(fork["origin"], "fork")
        self.assertEqual(fork["author"], "Christian McCrave")
        self.assertEqual(fork["source_url"], "https://github.com/Cmccrave/McRave")
        self.assertEqual(identity_for("Unknown.dylib", identities, "anything")["ownership"], "unknown")

    def test_named_original_identity_is_used_for_modular_match_and_replay(self):
        identities = {"KestrelModular.dylib": {
            "name": "Kestrel Modular v1", "ownership": "project", "origin": "original",
            "upstream_name": None, "author": "Luke Cameron",
            "author_url": "https://github.com/lukecameron",
            "source_url": "https://github.com/lukecameron/starcraft-ai/tree/main/bots/kestrel-modular-v1",
        }}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(json.dumps({
                "run_id": "modular-run",
                "inputs": {"players": [{"player": 1, "name": "Kestrel Modular v1",
                    "race": "Protoss", "bot_module": {"path": "/private/build/KestrelModular.dylib",
                    "sha256": "m" * 64}}]},
                "players": [], "replays": [{"player": 1, "size_bytes": 1, "sha256": "r" * 64,
                    "path": "/private/replay.rep"}],
            }))
            public = public_manifest(path, identities)
            player, replay = public["players"][0], public["replays"][0]
            self.assertEqual(player["display_name"], "Kestrel Modular v1")
            self.assertEqual(player["bot"], "Kestrel Modular v1")
            self.assertEqual(player["ownership"], "project")
            self.assertEqual(player["origin"], "original")
            self.assertEqual(replay["display_name"], "Kestrel Modular v1")
            self.assertEqual(replay["bot"], "Kestrel Modular v1")

    def test_tracked_architecture_source_is_exported_with_modular_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs/architecture.md").write_text(
                "| System | Owns | Public inputs and outputs |\n"
                "| --- | --- | --- |\n"
                "| `WorldState` | The public world snapshot | Snapshot |\n"
                "| `CommandArbiter` | Command accounting | Commands |\n",
                encoding="utf-8",
            )
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({
                "run_id": "architecture-run",
                "inputs": {"players": [{"player": 1, "name": "Kestrel Modular v1",
                    "race": "Protoss", "bot_module": {"path": "/build/KestrelModular.dylib",
                    "sha256": "m" * 64}}]},
                "players": [], "replays": [],
            }))
            identities = {"KestrelModular.dylib": {
                "name": "Kestrel Modular v1", "ownership": "project", "origin": "original",
                "author": "Luke Cameron", "source_url": "https://example.test/source",
                "architecture_source": "docs/architecture.md",
                "architecture_source_url": "https://example.test/architecture",
            }}
            self.assertEqual(architecture_systems(root, "docs/architecture.md")[0]["name"], "WorldState")
            player = public_manifest(manifest, identities, root)["players"][0]
            self.assertEqual(player["architecture_source"], "docs/architecture.md")
            self.assertEqual(player["architecture_source_url"], "https://example.test/architecture")
            self.assertEqual([system["name"] for system in player["architecture_systems"]], ["WorldState", "CommandArbiter"])

    def test_startup_attempt_keeps_bot_identity_before_process_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(json.dumps({"inputs": {"players": [{"player": 1, "name": "Local McRave", "race": "Zerg", "bot_module": {"path": "/private/build/McRave.dylib"}}]}, "players": []}))
            public = public_manifest(path, {"McRave.dylib": {"ownership": "project", "origin": "port", "upstream_name": "McRave", "author_url": "https://github.com/Cmccrave"}})
            self.assertEqual(public["players"][0]["name"], "Local McRave")
            self.assertEqual(public["players"][0]["origin"], "port")
            self.assertNotIn("/private/build", json.dumps(public))

    def test_updated_experiment_notes_override_old_published_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dashboard").mkdir()
            (root / "config").mkdir()
            (root / "dashboard/index.html").write_text("ok")
            (root / "dashboard/data.json").write_text(json.dumps({"experiments": [{"id": "seed", "status": "planned", "notes": "Not done"}]}))
            (root / "config/experiments.json").write_text(json.dumps({"experiments": [{"id": "seed", "status": "completed", "notes": "Verified"}]}))
            public = export(root, root / "out")
            self.assertEqual(public["experiments"][0]["status"], "completed")
            self.assertEqual(public["experiments"][0]["notes"], "Verified")

    def test_sparse_experiment_index_does_not_erase_configured_details(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dashboard").mkdir(); (root / "dashboard/index.html").write_text("ok")
            (root / "config").mkdir()
            (root / "config/experiments.json").write_text(json.dumps({"experiments": [{"id": "station", "title": "Station coordinates", "date": "2026-09-20", "hypothesis": "Configured hypothesis", "notes": "Configured notes", "conclusion": "Configured conclusion", "status": "planned"}]}))
            sparse = root / "artifacts/experiments/mcrave-station-coordinates-v1/manifest.json"; sparse.parent.mkdir(parents=True)
            sparse.write_text(json.dumps({"experiment_id": "station", "status": "completed", "runs": [], "controls": {}}))
            public = export(root, root / "out")
            item = public["experiments"][0]
            self.assertEqual(item["status"], "completed")
            self.assertEqual(item["title"], "Station coordinates")
            self.assertEqual(item["hypothesis"], "Configured hypothesis")
            self.assertEqual(item["date"], "2026-09-20")
            self.assertEqual(item["conclusion"], "Configured conclusion")
            self.assertNotIn("games", item)

    def test_shared_target_scorecard_metrics_are_public_but_trace_arrays_are_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dashboard").mkdir(); (root / "dashboard/index.html").write_text("ok")
            (root / "config").mkdir()
            (root / "config/experiments.json").write_text(json.dumps({"experiments": []}))
            experiment = root / "artifacts/experiments/shared/manifest.json"; experiment.parent.mkdir(parents=True)
            experiment.write_text(json.dumps({"experiment_id": "shared", "status": "completed", "games": [{"index": 1, "run_id": "run-1"}]}))
            (experiment.parent / "hillclimb-scorecard.json").write_text(json.dumps({
                "schema_version": 1,
                "aggregate": {"games": 1, "shared_target": {"accepted": 12}},
                "games": [{"index": 1, "run_id": "run-1", "shared_target": {
                    "counters": {"shared_target_accepted": 9, "shared_target_attempts": 10, "shared_target_selections": 11, "shared_target_correction_opportunities": 5, "shared_target_switches": 2, "shared_target_non_zerg_selections": 7, "shared_target_rejects": 1, "shared_target_illegal_selections": 0},
                    "coordinated_accepted_selections": 4,
                    "multi_participant_selections": 6,
                    "max_participants": 3,
                    "generation": "v38",
                    "quantitative_grade": {"grade": "pass", "score": 100},
                    "review_flags": [],
                    "trace": {"shared_target_frames": list(range(1000))}
                }}]
            }))
            public = export(root, root / "out")
            shared = public["experiments"][0]["scorecard"]["games"][0]["shared_target"]
            self.assertEqual(shared["accepted"], 9)
            self.assertEqual(shared["attempts"], 10)
            self.assertEqual(shared["selections"], 11)
            self.assertEqual(shared["multi_participant_selections"], 6)
            self.assertEqual(shared["coordinated_accepted_selections"], 4)
            self.assertEqual(shared["correction_opportunities"], 5)
            self.assertEqual(shared["shared_target_non_zerg_selections"], 7)
            self.assertEqual(shared["shared_target_rejects"], 1)
            self.assertEqual(shared["shared_target_illegal_selections"], 0)
            self.assertEqual(shared["max_participants"], 3)
            self.assertEqual(shared["quantitative_grade"]["grade"], "pass")
            self.assertNotIn("shared_target_frames", json.dumps(public))

    def test_scorecard_rows_retain_terminal_status_and_classification_for_speed_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dashboard").mkdir(); (root / "dashboard/index.html").write_text("ok")
            (root / "config").mkdir()
            experiment = root / "artifacts/experiments/timeout/manifest.json"; experiment.parent.mkdir(parents=True)
            experiment.write_text(json.dumps({"experiment_id": "timeout", "status": "completed", "games": []}))
            (experiment.parent / "hillclimb-scorecard.json").write_text(json.dumps({
                "aggregate": {},
                "games": [{"run_id": "run-timeout", "status": "timed_out", "durable_fps": 8126,
                           "record": {"classification": "timeout"}, "outcome_verified": False}]
            }))
            game = export(root, root / "out")["experiments"][0]["scorecard"]["games"][0]
            self.assertEqual(game["run_id"], "run-timeout")
            self.assertEqual(game["status"], "timed_out")
            self.assertEqual(game["classification"], "timeout")
            self.assertFalse(game["outcome_verified"])

    def test_dashboard_labels_local_context_speed_validity_and_replay_links(self):
        source = Path(__file__).resolve().parents[1] / "dashboard/index.html"
        html = source.read_text(encoding="utf-8")
        self.assertIn("Local component:", html)
        self.assertIn("not a BASIL rating or tournament prediction", html)
        self.assertIn("Prior sensitivity (prior SD)", html)
        self.assertIn("data-replay-run", html)
        self.assertIn('href="#replay-${esc(runId)}"', html)
        self.assertIn("No replay archived", html)
        self.assertIn("find(item=>item.run_id===runId)", html)
        self.assertIn("Speed unavailable", html)
        self.assertIn("Durable speed is not a valid completed-game measurement.", html)
        self.assertIn("originNames={original:'Original',port:'Port',fork:'Fork'", html)
        self.assertIn("p.display_name||p.bot", html)
        self.assertIn(".join(' + ')", html)
        self.assertNotIn("Port/Fork", html)

    def test_dashboard_bot_profile_surfaces_build_status_and_tracked_systems(self):
        source = Path(__file__).resolve().parents[1] / "dashboard/index.html"
        html = source.read_text(encoding="utf-8")
        self.assertIn("Build identity", html)
        self.assertIn("Current experiment status", html)
        self.assertIn("Composed systems", html)
        self.assertIn("architecture_systems", html)
        self.assertIn("architecture_source_url", html)
        self.assertIn("function renderBots(){return renderBotProfile()}", html)

    def test_export_allowlists_manifest_and_names_bot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "artifacts/runs/run-1").mkdir(parents=True)
            (root / "config").mkdir()
            (root / "dashboard").mkdir()
            (root / "dashboard/index.html").write_text("<html>ok</html>")
            replay = root / "artifacts/runs/run-1/game.rep"
            replay.write_bytes(b"replay")
            (root / "config/experiments.json").write_text('{"experiments": []}')
            (root / "config/opponents.json").write_text('{"opponents": [], "provisional_buckets": []}')
            (root / "config/bot-identities.json").write_text(json.dumps({"bots": {"WorkerRush.dylib": {"ownership": "project", "origin": "original", "upstream_name": "WorkerRush", "author": "Project", "author_url": "https://example.test/author", "source_url": "https://example.test/source"}}}))
            (root / "artifacts/runs/run-1/manifest.json").write_text(json.dumps({
                "run_id": "run-1", "status": "completed", "purpose": "test",
                "players": [{"player": 1, "environment": {"BWAPI_CONFIG_AI__AI": "/private/secret/WorkerRush.dylib", "BWAPI_CONFIG_AUTO_MENU__RACE": "Protoss"}, "return_code": 0, "result_metadata": {"ended": True, "winner": True, "frame_count": 10}}],
                "replays": [{"player": 1, "size_bytes": 6, "sha256": "a" * 64, "path": str(replay)}],
            }))
            snapshot = export(root, root / "out")
            public = json.loads((root / "out/data.json").read_text())
            self.assertEqual(snapshot["runs"][0]["players"][0]["bot"], "WorkerRush")
            self.assertEqual(snapshot["runs"][0]["players"][0]["origin"], "original")
            self.assertEqual(snapshot["runs"][0]["replays"][0]["author_url"], "https://example.test/author")
            self.assertNotIn("/private/secret", json.dumps(public))
            self.assertNotIn("environment", json.dumps(public))
            self.assertNotIn(str(replay), json.dumps(public))
            self.assertEqual(public["runs"][0]["replays"][0]["replay_path"], "replays/run-1-1-1.rep")
            self.assertEqual((root / "out/replays/run-1-1-1.rep").read_bytes(), b"replay")
            self.assertEqual((root / "out/index.html").read_text(), "<html>ok</html>")

    def test_clean_ci_preserves_snapshot_histories_and_absolute_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dashboard").mkdir()
            (root / "dashboard/index.html").write_text("<html>ok</html>")
            replay_url = "https://immutable.example/replays/run-1-1-1.rep"
            snapshot = {"runs": [{"run_id": "run-1", "replays": [{"replay_path": replay_url}]}],
                        "experiments": [], "ratings": [], "rating_buckets": [],
                        "basil_history": [{"id": "bot", "date": "2026-01-01", "rating": 1}],
                        "local_elo_history": [{"id": "exp:bot", "date": "2026-01-02", "rating": 2}]}
            (root / "dashboard/data.json").write_text(json.dumps(snapshot))
            public = export(root, root / "out")
            self.assertEqual(public["runs"][0]["replays"][0]["replay_path"], replay_url)
            self.assertEqual(public["basil_history"], snapshot["basil_history"])
            self.assertEqual(public["local_elo_history"], snapshot["local_elo_history"])

    def test_artifact_experiment_is_allowlisted_and_history_is_retained(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dashboard").mkdir(); (root / "dashboard/index.html").write_text("ok")
            (root / "dashboard/data.json").write_text(json.dumps({"basil_history": [], "local_elo_history": [{"id": "old", "date": "d", "rating": 3}]}))
            experiment = root / "artifacts/experiments/quick/manifest.json"; experiment.parent.mkdir(parents=True)
            experiment.write_text(json.dumps({"experiment_id": "quick", "status": "completed", "started_at": "2026-09-20T00:00:00Z", "finished_at": "2026-09-20T00:01:00Z", "hypothesis": "h", "decision": "c", "secret_path": "/private/secret", "summary": {"by_opponent": {"ZZZK": {"relative_elo_advantage": 42}}}, "games": [{"index": 1, "opponent": "ZZZK", "map": "Benzene", "candidate_player": 1, "status": "finished", "classification": "win", "command": ["secret"], "measurements": {"durable_completion_seconds": 1.5, "logical_frame_count": 10}}]}))
            first = export(root, root / "one")
            second = export(root, root / "two")
            self.assertEqual(first["experiments"][0]["conclusion"], "c")
            self.assertEqual(first["experiments"][0]["runner_notes"], "c")
            self.assertNotIn("decision", first["experiments"][0])
            self.assertNotIn("secret", json.dumps(first))
            self.assertEqual(len(second["local_elo_history"]), 2)
            self.assertEqual(second["local_elo_history"][-1]["rating"], 42)

    def test_runner_advice_preserves_reviewed_verdict_and_conclusion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dashboard").mkdir(); (root / "dashboard/index.html").write_text("ok")
            (root / "config").mkdir()
            reviewed = {"id": "cohort", "decision": "REJECT", "conclusion": "One crash fails the compatibility gate."}
            (root / "config/experiments.json").write_text(json.dumps({"experiments": [reviewed]}))
            artifact = root / "artifacts/experiments/cohort/manifest.json"; artifact.parent.mkdir(parents=True)
            artifact.write_text(json.dumps({"experiment_id": "cohort", "status": "completed", "decision": "Investigate failures."}))
            item = export(root, root / "out")["experiments"][0]
            self.assertEqual(item["decision"], "REJECT")
            self.assertEqual(item["conclusion"], reviewed["conclusion"])
            self.assertEqual(item["status"], "completed")
            # The published snapshot alone must retain the same verdict on Pages.
            (root / "dashboard/data.json").write_text(json.dumps({"experiments": [item]}))
            artifact.unlink()
            self.assertEqual(export(root, root / "out")["experiments"][0], item)

    def test_absolutize_replays_preserves_existing_immutable_urls(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.json"
            path.write_text(json.dumps({"runs": [{"replays": [{"replay_path": "replays/a.rep"}, {"replay_path": "https://old.example/replays/b.rep"}]}]}))
            absolutize_replays(path, "https://new.example/")
            replays = json.loads(path.read_text())["runs"][0]["replays"]
            self.assertEqual(replays[0]["replay_path"], "https://new.example/replays/a.rep")
            self.assertEqual(replays[1]["replay_path"], "https://old.example/replays/b.rep")


if __name__ == "__main__":
    unittest.main()
