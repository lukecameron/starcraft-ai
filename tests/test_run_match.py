import contextlib
import json
import hashlib
import io
import importlib.util
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_match.py"
SPEC = importlib.util.spec_from_file_location("run_match", RUNNER)
run_match = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(run_match)


FAKE_LAUNCHER = '''#!/usr/bin/env python3
import json, os, pathlib, sys, time
if os.environ.get("FAKE_LAUNCHED_PATH"):
    pathlib.Path(os.environ["FAKE_LAUNCHED_PATH"]).write_text("launched")
mode = os.environ.get("FAKE_MODE", "success")
if mode == "startup":
    print("test-only startup failure", file=sys.stderr)
    raise SystemExit(7)
if mode in ("sleep", "interrupt"):
    time.sleep(30)
replay = pathlib.Path(os.environ["BWAPI_CONFIG_AUTO_MENU__SAVE_REPLAY"])
replay.write_bytes(b"test-only-replay-" + os.environ["BWAPI_CONFIG_AUTO_MENU__RACE"].encode())
pathlib.Path(os.environ["MATCH_RESULT_PATH"]).write_text(json.dumps({"frame_count": 240, "winner": os.environ["BWAPI_CONFIG_AUTO_MENU__RACE"] == "Terran", "ended": True}))
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

    def test_socket_preflight_preserves_restricted_bind_error(self):
        class RestrictedSocket:
            def __init__(self, family, kind):
                self.family = family
                self.kind = kind
                self.closed = False

            def bind(self, path):
                self.path = path
                raise PermissionError(1, "Operation not permitted")

            def close(self):
                self.closed = True

        socket_dir = self.root / "socket"
        socket_dir.mkdir()
        with patch.object(run_match.socket, "socket", RestrictedSocket):
            with self.assertRaisesRegex(OSError, r"OpenBW AF_UNIX socket preflight failed.*game\.socket") as raised:
                run_match.preflight_socket_directory(socket_dir)
        self.assertIn("Operation not permitted", str(raised.exception))
        self.assertFalse((socket_dir / "game.socket").exists())

    def test_socket_preflight_failure_is_durable_before_popen(self):
        with patch.object(run_match, "preflight_socket_directory",
                          side_effect=OSError("OpenBW AF_UNIX socket preflight failed for test/game.socket: EPERM")):
            with contextlib.redirect_stdout(io.StringIO()):
                result = run_match.main(self.command()[2:])
        self.assertEqual(result, 1)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "failed")
        self.assertEqual(manifest["termination_reason"], "launch_error")
        self.assertEqual(manifest["players"], [])
        self.assertIn("AF_UNIX socket preflight failed", manifest["launch_error"])

    def test_socket_preflight_removes_successfully_bound_probe(self):
        class ProbeSocket:
            def bind(self, path):
                Path(path).write_bytes(b"probe")

            def close(self):
                pass

        socket_dir = self.root / "socket"
        socket_dir.mkdir()
        with patch.object(run_match.socket, "socket", return_value=ProbeSocket()):
            run_match.preflight_socket_directory(socket_dir)
        self.assertFalse((socket_dir / "game.socket").exists())

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
            'pathlib.Path(os.environ["MATCH_RESULT_PATH"])',
            'pathlib.Path("bwapi-data/write/diagnostic.json")').replace('"frame_count": 240', '"frame_count": 321')
        self.launcher.write_text(launcher)
        completed = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["logical_frame_count"], 321)
        self.assertEqual(len(manifest["players"][0]["write_state"]), 1)

    def test_packaged_ai_config_is_snapshotted_and_checked(self):
        ai = self.root / "AI"
        ai.mkdir()
        config = ai / "config.json"
        config.write_text('{"strategy":"normal"}')
        sidecar = {"binary_sha256": hashlib.sha256(self.bot1.read_bytes()).hexdigest(),
                   "ai_files": [{"path": "config.json", "sha256": hashlib.sha256(config.read_bytes()).hexdigest()}]}
        Path(str(self.bot1) + ".build.json").write_text(json.dumps(sidecar))
        self.launcher.write_text(self.launcher.read_text().replace(
            'mode = os.environ.get',
            'assert pathlib.Path("bwapi-data/AI/config.json").read_text() == \'{"strategy":"normal"}\'\nmode = os.environ.get'))
        completed = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        manifest = json.loads(self.manifests()[0].read_text())
        archived = Path(manifest["inputs"]["players"][0]["ai_files"][0]["path"])
        self.assertFalse(archived.is_symlink())
        config.write_text('{"strategy":"changed"}')
        self.assertEqual(archived.read_text(), '{"strategy":"normal"}')
        completed = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1)
        failed = [json.loads(path.read_text()) for path in self.manifests()
                  if json.loads(path.read_text())["status"] == "failed"]
        self.assertEqual(len(failed), 1)
        self.assertIn("Missing or changed AI file", failed[0]["launch_error"])
        self.assertEqual(failed[0]["players"], [])

    def test_timeout_is_recorded_without_fake_result_or_replay(self):
        completed = subprocess.run(self.command("0.15"), env={**dict(__import__("os").environ), "FAKE_MODE": "sleep"},
                                   text=True, capture_output=True, timeout=5)
        self.assertEqual(completed.returncode, 1)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "timed_out")
        self.assertEqual(manifest["termination_reason"], "wall_timeout")
        self.assertEqual(manifest["replays"], [])
        self.assertIsNone(manifest["result"])

    def test_controlled_seed_cannot_silently_use_an_unsupported_engine(self):
        completed = subprocess.run(self.command() + ["--seed", "42"], text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "failed")
        self.assertEqual(manifest["players"], [])
        self.assertIn("scenario-capable", manifest["launch_error"])

    def test_unsupported_bot_seed_fails_durably_before_popen(self):
        marker = self.root / "launched"
        completed = subprocess.run(self.command() + ["--bot-seed1", "42"],
                                   env={**dict(__import__("os").environ), "FAKE_LAUNCHED_PATH": str(marker)},
                                   text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "failed")
        self.assertEqual(manifest["players"], [])
        self.assertFalse(marker.exists())
        self.assertIn("binary-matched sidecar", manifest["launch_error"])

    def test_bot_seeds_are_isolated_and_inherited_seed_is_cleared(self):
        for bot in (self.bot1, self.bot2):
            Path(str(bot) + ".build.json").write_text(json.dumps({
                "binary_sha256": hashlib.sha256(bot.read_bytes()).hexdigest(),
                "bot_rng_control": {"env": "MATCH_BOT_SEED"},
            }))
        completed = subprocess.run(self.command() + ["--bot-seed1", "11", "--bot-seed2", "22"],
                                   env={**dict(__import__("os").environ), "MATCH_BOT_SEED": "999"},
                                   text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["reproducibility"]["bot_seeds"], [11, 22])
        self.assertEqual([player["bot_seed"] for player in manifest["inputs"]["players"]], [11, 22])
        self.assertEqual([item["environment"]["MATCH_BOT_SEED"]
                          for item in manifest["launch_configuration"]], ["11", "22"])

    def test_inherited_bot_seed_is_absent_when_not_requested(self):
        self.launcher.write_text(self.launcher.read_text().replace(
            'mode = os.environ.get', 'assert "MATCH_BOT_SEED" not in os.environ\nmode = os.environ.get'))
        completed = subprocess.run(self.command(), env={**dict(__import__("os").environ), "MATCH_BOT_SEED": "999"},
                                   text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["reproducibility"]["bot_seeds"], [None, None])
        self.assertNotIn("MATCH_BOT_SEED", manifest["launch_configuration"][0]["environment"])

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
            '"ended": True', '"ended": False'))
        completed = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "incomplete")
        self.assertEqual(len(manifest["replays"]), 2)

    def test_replay_without_terminal_metadata_is_not_success(self):
        self.launcher.write_text(self.launcher.read_text().replace(
            'pathlib.Path(os.environ["MATCH_RESULT_PATH"]).write_text', '# no metadata: '))
        completed = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "incomplete")
        self.assertFalse(manifest["outcome_verified"])

    def test_malformed_frame_metadata_still_finalizes(self):
        self.launcher.write_text(self.launcher.read_text().replace('"frame_count": 240', '"frame_count": "bad"'))
        completed = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1)
        manifest = json.loads(self.manifests()[0].read_text())
        self.assertEqual(manifest["status"], "incomplete")
        self.assertIn("frame_count", manifest["players"][0]["result_metadata_note"])
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
