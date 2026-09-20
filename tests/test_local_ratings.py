import json
import math
from pathlib import Path
import tempfile
import unittest

from scripts.local_ratings import ELO_PER_LOGIT, build_league, connected_components, contrast, fit_bt


class RatingModelTest(unittest.TestCase):
    def test_balanced_results_have_equal_strength_and_shrink_with_evidence(self):
        nodes = ["a", "b"]
        theta, cov = fit_bt(nodes, [("a", "b"), ("b", "a")])
        row = contrast(theta, cov, 0, 1)
        self.assertEqual(row["rating"], 1000)
        theta2, cov2 = fit_bt(nodes, [("a", "b"), ("b", "a")] * 50)
        self.assertLess(contrast(theta2, cov2, 0, 1)["high"] - 1000, row["high"] - 1000)
        self.assertEqual(contrast(theta2, cov2, 1, 1), {"rating": 1000.0, "low": 1000.0, "high": 1000.0})

    def test_sweep_is_finite_symmetric_and_prior_sensitive(self):
        theta, cov = fit_bt(["a", "b"], [("a", "b")] * 10)
        reverse, reverse_cov = fit_bt(["a", "b"], [("b", "a")] * 10)
        self.assertGreater(theta[0], theta[1])
        self.assertAlmostEqual(theta[0], -reverse[0])
        self.assertAlmostEqual(cov[0][0], reverse_cov[0][0])
        self.assertTrue(math.isfinite(contrast(theta, cov, 0, 1)["high"]))
        wide, _ = fit_bt(["a", "b"], [("a", "b")] * 10, 800)
        self.assertGreater(wide[0] - wide[1], theta[0] - theta[1])

    def test_fit_agrees_with_independent_one_dimensional_grid(self):
        # Two players: integrate out the unidentifiable common location.
        # Difference prior variance is 2*sigma². Validate MAP against a fine
        # grid independent of Newton gradient/Hessian implementation.
        pairs = [("a", "b")] * 7 + [("b", "a")] * 3
        theta, cov = fit_bt(["a", "b"], pairs)
        sigma = 400 / ELO_PER_LOGIT
        def loss(d):
            p = 1 / (1 + math.exp(-d))
            return -7 * math.log(p) - 3 * math.log1p(-p) + d * d / (4 * sigma * sigma)
        grid = [x / 10000 for x in range(-20000, 20001)]
        expected = min(grid, key=loss)
        self.assertAlmostEqual(theta[0] - theta[1], expected, delta=0.0001)
        # Finite-difference curvature for the contrast matches full covariance.
        d = theta[0] - theta[1]
        h = .001
        curvature = (loss(d+h) + loss(d-h) - 2*loss(d)) / (h*h)
        variance = cov[0][0] + cov[1][1] - 2*cov[0][1]
        self.assertAlmostEqual(variance, 1/curvature, places=6)

    def test_relabeling_and_game_order_do_not_change_estimates(self):
        games = [("a", "b")] * 5 + [("b", "c")] * 4 + [("c", "a")] * 2
        first, _ = fit_bt(["a", "b", "c"], games)
        second, _ = fit_bt(["c", "a", "b"], list(reversed(games)))
        self.assertAlmostEqual(first[0], second[1])
        self.assertAlmostEqual(first[1], second[2])
        self.assertAlmostEqual(first[2], second[0])

    def test_disconnected_components_are_not_ranked_together(self):
        games = [{"nodes": ["a", "b"]}, {"nodes": ["c", "d"]}, {"nodes": ["b", "e"]}]
        self.assertEqual(connected_components(games), [["a", "b", "e"], ["c", "d"]])

    def test_clean_deploy_keeps_published_ratings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config").mkdir()
            (root / "config/local-ratings.json").write_text(json.dumps({"experiments": ["calibration"]}))
            fallback = {"components": [{"id": "retained"}]}
            self.assertEqual(build_league(root, [], fallback), fallback)

class RatingEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "config").mkdir()
        self.public = []
        self.reviewed = {}

    def run_fixture(self, run_id, seed=1, race="Protoss", engine="engine", config_sha="settings", winner=True, experiment="calibration", build="module-a"):
        from scripts.local_ratings import file_hash
        folder = self.root / "artifacts/runs" / run_id
        folder.mkdir(parents=True)
        players, inputs, replays = [], [], []
        for side in (1, 2):
            stderr = folder / f"{side}.log"
            stderr.write_text("normal end")
            replay = folder / f"{side}.rep"
            replay.write_bytes(b"replay fixture")
            result = {"ended": True, "winner": winner if side == 1 else False, "latency_frames": 3}
            players.append({"player": side, "return_code": 0, "result_metadata": result, "stderr": {"path": str(stderr)}})
            inputs.append({"player": side, "race": race if side == 1 else "Zerg", "bot_module": {"sha256": build if side == 1 else "module-b"}, "ai_files": [{"path": "config.json", "sha256": config_sha}] if side == 1 else []})
            replays.append({"player": side, "path": str(replay), "sha256": file_hash(replay)})
        manifest = {"run_id": run_id, "experiment_id": experiment, "finished_at": run_id, "status": "completed", "outcome_verified": True, "players": players, "replays": replays,
                    "inputs": {"players": inputs, "launcher": {"sha256": engine}, "engine_libraries": [{"path": "lib.dylib", "sha256": engine}], "game_data": [{"sha256": "mpq"}], "map": {"sha256": "map", "configured_path": "map.scx"}},
                    "rules": {"wall_timeout_seconds": 180}, "platform": {"machine": "arm64"},
                    "reproducibility": {"learning_state": "empty isolated read/write directories for each player", "random_seed": seed}}
        path = folder / "manifest.json"
        path.write_text(json.dumps(manifest))
        self.reviewed[run_id] = file_hash(path)
        self.public.append({"run_id": run_id, "players": [{"player": 1, "bot": "A"}, {"player": 2, "bot": "B"}]})
        return path

    def league(self):
        (self.root / "config/local-ratings.json").write_text(json.dumps({"experiments": ["calibration"], "reviewed_runs": self.reviewed}))
        return build_league(self.root, self.public)

    def test_duplicate_scenario_is_counted_once_but_changed_seed_is_new(self):
        self.run_fixture("run1")
        self.run_fixture("run2")
        self.run_fixture("run3", seed=2)
        league = self.league()
        self.assertEqual(league["reviewed_games"], 2)
        self.assertEqual(len(league["excluded"]), 1)
        self.assertIn("duplicate", league["excluded"][0]["reason"])

    def test_race_build_and_config_change_create_separate_nodes(self):
        self.run_fixture("run1")
        self.run_fixture("run2", race="Terran")
        self.run_fixture("run3", config_sha="new config")
        self.run_fixture("run4", build="new module")
        league = self.league()
        self.assertEqual(len(league["components"]), 1)
        self.assertEqual(len(league["components"][0]["rows"]), 5)
        rows = [row for row in league["components"][0]["rows"] if row["name"] == "A"]
        self.assertTrue(all(row["games"] == 1 for row in rows))

    def test_engine_regimes_and_unselected_diagnostics_are_separate(self):
        self.run_fixture("run1")
        self.run_fixture("run2", engine="other engine")
        self.run_fixture("run3", experiment="diagnostic")
        league = self.league()
        self.assertEqual(len(league["components"]), 2)
        self.assertEqual(league["reviewed_games"], 2)

    def test_conflicting_results_pending_review_and_changed_manifest_excluded(self):
        self.run_fixture("run1", winner=False)
        self.run_fixture("run2", seed=2)
        self.reviewed.pop("run2")
        path = self.run_fixture("run3", seed=3)
        path.write_text(path.read_text()+"\n")
        league = self.league()
        self.assertEqual(league["reviewed_games"], 0)
        self.assertEqual(len(league["excluded"]), 3)
        self.assertFalse(league["components"])


if __name__ == "__main__":
    unittest.main()
