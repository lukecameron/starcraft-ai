import json
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_match.py"


FAKE_LAUNCHER = '''#!/usr/bin/env python3
import json, os, pathlib, sys, time
mode = os.environ.get("FAKE_MODE", "success")
if mode == "startup":
    print("test-only startup failure", file=sys.stderr)
    raise SystemExit(7)
if mode in ("sleep", "interrupt"):
    time.sleep(30)
replay = pathlib.Path(os.environ["BWAPI_CONFIG_AUTO_MENU__SAVE_REPLAY"])
replay.write_bytes(b"test-only-replay-" + os.environ["BWAPI_CONFIG_AUTO_MENU__RACE"].encode())
pathlib.Path(os.environ["MATCH_RESULT_PATH"]).write_text(json.dumps({"frame_count": 240, "winner": True}))
'''


class RunMatchTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.launcher = self.root / "fake_launcher.py"
        self.launcher.write_text(FAKE_LAUNCHER)
        self.launcher.chmod(0o755)
        self.data = self.root / "data"
        (self.data / "maps").mkdir(parents=True)
        (self.data / "maps/test.scx").write_bytes(b"map")
        for name in ("Patch_rt.mpq", "StarDat.mpq", "BrooDat.mpq"):
            (self.data / name).write_bytes(name.encode())
        self.bot1 = self.root / "one.so"
        self.bot2 = self.root / "two.so"
        self.bot1.write_bytes(b"one")
        self.bot2.write_bytes(b"two")

    def tearDown(self):
        self.temp.cleanup()

    def command(self, timeout="3"):
        return [sys.executable, str(RUNNER), "--launcher", str(self.launcher), "--bot1", str(self.bot1),
                "--race1", "Terran", "--bot2", str(self.bot2), "--race2", "Zerg", "--map", "maps/test.scx",
                "--game-data-dir", str(self.data), "--purpose", "test-only fake lifecycle", "--wall-timeout", timeout,
                "--artifacts-dir", str(self.root / "artifacts")]

    def manifests(self):
        return list((self.root / "artifacts/runs").glob("*/game-0001/manifest.json"))

    def test_success_archives_real_emitted_bytes_and_metadata(self):
        completed = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "completed")
        self.assertEqual(manifest["logical_frame_count"], 240)
        self.assertEqual(len(manifest["replays"]), 2)
        for replay in manifest["replays"]:
            path = Path(replay["path"])
            self.assertTrue(path.read_bytes().startswith(b"test-only-replay-"))
            self.assertEqual(len(replay["sha256"]), 64)
        self.assertEqual(manifest["inputs"]["players"][0]["bot_module"]["sha256"],
                         "7692c3ad3540bb803c020b3aee66cd8887123234ea0c6e7143c0add73ff431ed")

    def test_tournament_write_path_is_used_as_result_fallback(self):
        launcher = self.launcher.read_text().replace(
            'pathlib.Path(os.environ["MATCH_RESULT_PATH"]).write_text(json.dumps({"frame_count": 240, "winner": True}))',
            'p = pathlib.Path("bwapi-data/write/diagnostic.json"); p.write_text(json.dumps({"frame_count": 321, "winner": False}))')
        self.launcher.write_text(launcher)
        completed = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["logical_frame_count"], 321)
        self.assertEqual(len(manifest["players"][0]["write_state"]), 1)

    def test_timeout_is_recorded_without_fake_result_or_replay(self):
        completed = subprocess.run(self.command("0.15"), env={**dict(__import__("os").environ), "FAKE_MODE": "sleep"},
                                   text=True, capture_output=True, timeout=5)
        self.assertEqual(completed.returncode, 1)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "timed_out")
        self.assertEqual(manifest["termination_reason"], "wall_timeout")
        self.assertEqual(manifest["replays"], [])
        self.assertIsNone(manifest["result"])

    def test_failed_startup_is_durable(self):
        completed = subprocess.run(self.command(), env={**dict(__import__("os").environ), "FAKE_MODE": "startup"},
                                   text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "failed")
        self.assertEqual([p["return_code"] for p in manifest["players"]], [7, 7])
        self.assertIn("startup failure", Path(manifest["players"][0]["stderr"]["path"]).read_text())

    def test_partial_replay_and_unfinished_callback_are_not_a_completed_match(self):
        self.launcher.write_text(self.launcher.read_text().replace(
            '"winner": True', '"winner": None, "ended": False'))
        completed = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "incomplete")
        self.assertEqual(len(manifest["replays"]), 2)

    def test_interrupt_finalizes_manifest(self):
        process = subprocess.Popen(self.command(), env={**dict(__import__("os").environ), "FAKE_MODE": "interrupt"},
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            if self.manifests() and json.loads(self.manifests()[0].read_text())["status"] == "running":
                break
            time.sleep(0.02)
        process.send_signal(signal.SIGINT)
        process.communicate(timeout=5)
        self.assertEqual(process.returncode, 128 + signal.SIGINT)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "interrupted")
        self.assertEqual(manifest["termination_reason"], f"signal_{signal.SIGINT}")


if __name__ == "__main__":
    unittest.main()
