import importlib.util
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("run_batch", ROOT / "scripts/run_batch.py")
run_batch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(run_batch)


class BatchSummaryTests(unittest.TestCase):
    def test_wilson_and_relative_elo_endpoints(self):
        summary = run_batch.summarize([
            {"opponent": "a", "classification": "win"},
            {"opponent": "a", "classification": "win"},
            {"opponent": "b", "classification": "loss"},
            {"opponent": "b", "classification": "timeout"},
        ], {"a": {}, "b": {}})
        self.assertEqual(summary["by_opponent"]["a"]["relative_elo_advantage"], "Infinity")
        self.assertEqual(summary["by_opponent"]["b"]["relative_elo_advantage"], "-Infinity")
        self.assertEqual(summary["by_opponent"]["b"]["failures"], {"timeout": 1})
        self.assertEqual(summary["pooled_cohort"]["scored_games"], 3)

    def test_zero_exit_without_verified_metadata_is_not_scored(self):
        match = {"status": "completed", "outcome_verified": False,
                 "termination_reason": "children_exited", "players": [{"return_code": 0}, {"return_code": 0}],
                 "result": [{"winner": True}, {"winner": False}]}
        self.assertEqual(run_batch.classify(match, 1), "missing_or_inconsistent_metadata")

    def test_runner_failure_or_nonopposing_results_are_not_scored(self):
        match = {"status": "completed", "outcome_verified": True,
                 "termination_reason": "children_exited", "players": [{"return_code": 0}, {"return_code": 0}],
                 "result": [{"winner": True}, {"winner": False}]}
        self.assertEqual(run_batch.classify(match, 1, 1), "launcher_failure")
        match["result"] = [{"winner": True}, {"winner": True}]
        self.assertEqual(run_batch.classify(match, 1), "missing_or_inconsistent_metadata")

    def test_bot_seed_command_mapping_follows_swapped_player_assignment(self):
        args = argparse.Namespace(runner="runner.py", artifacts_dir="artifacts")
        schedule = {"launcher": "launcher", "library_path": "lib", "game_data_dir": "data",
                    "purpose": "test", "experiment_id": "test", "wall_timeout_seconds": 1,
                    "candidate": {"name": "candidate", "race": "Zerg"}}
        opponent = {"name": "opponent", "race": "Terran", "path": "opponent.so"}
        game = {"candidate_player": 2, "map": "map.scx", "scenario_seed": 7,
                "candidate_bot_seed": 11, "opponent_bot_seed": 22}
        command = run_batch.command_for(args, schedule, game, Path("candidate.so"), opponent)
        self.assertEqual(command[command.index("--bot-seed1") + 1], "22")
        self.assertEqual(command[command.index("--bot-seed2") + 1], "11")

    def test_schedule_rejects_boolean_and_out_of_range_bot_seeds(self):
        base = {"experiment_id": "test", "hypothesis": "h", "stop_condition": "s", "purpose": "p",
                "launcher": "l", "library_path": "lib", "game_data_dir": "data",
                "candidate": {"name": "c", "race": "Zerg", "sha256": "x"},
                "opponents": {"o": {"name": "o", "race": "Terran", "path": "o", "sha256": "y"}},
                "games": [{"opponent": "o", "map": "m", "candidate_player": 1,
                           "scenario_seed": 1, "candidate_bot_seed": True}]}
        with self.assertRaises(SystemExit):
            run_batch.validate_schedule(argparse.ArgumentParser(), base)
        base["games"][0]["candidate_bot_seed"] = 0
        base["games"][0]["opponent_bot_seed"] = 0x100000000
        with self.assertRaises(SystemExit):
            run_batch.validate_schedule(argparse.ArgumentParser(), base)

    def test_timeout_and_child_crash_take_precedence_over_runner_failure(self):
        timeout = {"termination_reason": "wall_timeout", "players": [{"return_code": -15}, {"return_code": -15}]}
        self.assertEqual(run_batch.classify(timeout, 1, 1), "timeout")
        crash = {"termination_reason": "children_exited", "players": [{"return_code": -11}, {"return_code": 0}]}
        self.assertEqual(run_batch.classify(crash, 1, 1), "crash")


class BatchLifecycleTests(unittest.TestCase):
    def test_schedule_is_persisted_and_results_are_incremental(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = root / "candidate.dylib"
            candidate.write_bytes(b"candidate")
            opponent = root / "opponent.dylib"
            opponent.write_bytes(b"opponent")
            runner = root / "fake_runner.py"
            runner.write_text(textwrap.dedent("""
                import argparse, json, pathlib, uuid
                p=argparse.ArgumentParser(); p.add_argument('--artifacts-dir'); p.add_argument('--bot1'); p.add_argument('--bot2')
                args, _=p.parse_known_args(); out=pathlib.Path(args.artifacts_dir)/('fake-'+uuid.uuid4().hex)/'manifest.json'
                out.parent.mkdir(parents=True); candidate_player=1 if 'candidate' in args.bot1 else 2
                results=[{'winner': candidate_player == 1}, {'winner': candidate_player == 2}]
                json.dump({'status':'completed','outcome_verified':True,'termination_reason':'children_exited',
                           'players':[{'return_code':0},{'return_code':0}],'result':results},out.open('w'))
                print(out)
            """))
            schedule = root / "schedule.json"
            schedule.write_text(json.dumps({
                "experiment_id": "test-batch", "hypothesis": "test hypothesis", "stop_condition": "two games",
                "purpose": "tests only", "wall_timeout_seconds": 1, "launcher": "launcher", "library_path": "lib",
                "game_data_dir": "data", "publish_hook": str(root / "publish.sh"),
                "candidate": {"name": "candidate", "race": "Zerg", "sha256": hashlib.sha256(b"candidate").hexdigest()},
                "opponents": {"op": {"name": "op", "race": "Terran", "path": str(opponent), "sha256": hashlib.sha256(b"opponent").hexdigest()}},
                "games": [{"opponent": "op", "map": "a.scx", "candidate_player": 1, "scenario_seed": 1},
                          {"opponent": "op", "map": "b.scx", "candidate_player": 2, "scenario_seed": 2}]
            }))
            (root / "publish.sh").write_text(textwrap.dedent(f"""\
                #!{sys.executable}
                import json, os
                from pathlib import Path
                manifest = json.loads(Path(os.environ['EXPERIMENT_MANIFEST']).read_text())
                Path(os.environ['EXPERIMENT_MANIFEST']).with_name('hook-observed.json').write_text(json.dumps({{
                    'status': manifest['status'], 'decision': manifest['decision'], 'cwd': os.getcwd()
                }}))
            """))
            (root / "publish.sh").chmod(0o755)
            completed = subprocess.run([sys.executable, str(ROOT / "scripts/run_batch.py"), "--schedule", str(schedule),
                                        "--candidate", str(candidate), "--runner", str(runner),
                                        "--artifacts-dir", str(root / "artifacts"), "--concurrency", "2"],
                                       text=True, capture_output=True, timeout=10)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            manifest = json.loads((root / "artifacts/experiments/test-batch/manifest.json").read_text())
            self.assertEqual(manifest["status"], "completed")
            self.assertEqual([game["classification"] for game in manifest["games"]], ["win", "win"])
            self.assertEqual(manifest["summary"]["by_opponent"]["op"]["wins"], 2)
            self.assertEqual(manifest["publish_hook"]["return_code"], 0)
            observed = json.loads((root / "artifacts/experiments/test-batch/hook-observed.json").read_text())
            self.assertEqual(observed["status"], "completed")
            self.assertIn("collect a larger comparison", observed["decision"])
            self.assertEqual(observed["cwd"], str(ROOT))
            self.assertEqual(json.loads((root / "artifacts/experiments/test-batch/schedule.json").read_text()), json.loads(schedule.read_text()))

    def test_interrupt_stops_the_exact_runner_group_and_preserves_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = root / "candidate.dylib"
            candidate.write_bytes(b"candidate")
            opponent = root / "opponent.dylib"
            opponent.write_bytes(b"opponent")
            runner = root / "slow_runner.py"
            runner.write_text("import os,time,pathlib\npathlib.Path(%r).write_text(str(os.getpid()))\ntime.sleep(60)\n" % str(root / "pid"))
            schedule = root / "schedule.json"
            schedule.write_text(json.dumps({
                "experiment_id": "interrupt-batch", "hypothesis": "test", "stop_condition": "interrupt",
                "purpose": "tests only", "wall_timeout_seconds": 120, "launcher": "launcher", "library_path": "lib",
                "game_data_dir": "data", "candidate": {"name": "candidate", "race": "Zerg", "sha256": hashlib.sha256(b"candidate").hexdigest()},
                "opponents": {"op": {"name": "op", "race": "Terran", "path": str(opponent), "sha256": hashlib.sha256(b"opponent").hexdigest()}},
                "games": [{"opponent": "op", "map": "a.scx", "candidate_player": 1, "scenario_seed": 1}]
            }))
            process = subprocess.Popen([sys.executable, str(ROOT / "scripts/run_batch.py"), "--schedule", str(schedule),
                                        "--candidate", str(candidate), "--runner", str(runner),
                                        "--artifacts-dir", str(root / "artifacts")])
            deadline = time.monotonic() + 5
            while not (root / "pid").exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertTrue((root / "pid").exists())
            process.send_signal(signal.SIGINT)
            self.assertEqual(process.wait(timeout=5), 130)
            manifest = json.loads((root / "artifacts/experiments/interrupt-batch/manifest.json").read_text())
            self.assertEqual(manifest["status"], "interrupted")
            child_pid = int((root / "pid").read_text())
            with self.assertRaises(ProcessLookupError):
                os.kill(child_pid, 0)


if __name__ == "__main__":
    unittest.main()
