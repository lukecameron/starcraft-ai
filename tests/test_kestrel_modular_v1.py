import re
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "bots/kestrel-modular-v1"


class KestrelModularV1Test(unittest.TestCase):
    def setUp(self):
        self.kestrel = (SOURCE / "src/Kestrel.cpp").read_text()
        self.cmake = (SOURCE / "CMakeLists.txt").read_text()
        self.architecture = (ROOT / "docs/evaluations/kestrel-modular-v1-architecture.md").read_text()

    def test_all_systems_are_real_translation_units_and_wired(self):
        systems = [
            "WorldState", "WorldMemory", "StrategyPlanner", "WorkerAllocator",
            "ProductionController", "ConstructionController", "ScoutingController",
            "SquadController", "CommandArbiter", "Telemetry",
        ]
        for system in systems:
            self.assertTrue((SOURCE / f"src/{system}.cpp").exists(), system)
            self.assertIn(system, self.kestrel, system)
            self.assertIn(system, self.architecture, system)
        self.assertEqual(self.kestrel.count("WorldSnapshot"), 1)

    def test_tick_order_and_lifecycle_hooks_are_explicit(self):
        order = [
            "world_.observe", "memory_.update", "planner_.decide", "workers_.tick",
            "production_.tick", "construction_.tick", "scouting_.tick", "squads_.tick",
            "telemetry_.sample",
        ]
        positions = [self.kestrel.index(item) for item in order]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("void onStart() override", self.kestrel)
        self.assertIn("void onFrame() override", self.kestrel)
        self.assertIn("void onEnd(bool won) override", self.kestrel)

    def test_command_boundary_and_public_observation_only(self):
        arbiter = (SOURCE / "src/CommandArbiter.cpp").read_text()
        world = (SOURCE / "src/WorldState.cpp").read_text()
        self.assertIn("CommandKind::", arbiter)
        self.assertIn("getLastError", arbiter)
        self.assertNotIn("readReplay", self.kestrel + arbiter + world)
        self.assertNotIn("getReplay", self.kestrel + arbiter + world)
        self.assertIn("isVisible()", world)
        self.assertIn("isDetected()", world)

    def test_subsystems_have_stateful_operational_paths(self):
        allocator = (SOURCE / "src/WorkerAllocator.cpp").read_text()
        construction = (SOURCE / "src/ConstructionController.cpp").read_text()
        memory = (SOURCE / "src/WorldMemory.cpp").read_text()
        squad = (SOURCE / "src/SquadController.cpp").read_text()
        telemetry = (SOURCE / "src/Telemetry.cpp").read_text()
        self.assertIn("Protoss_Assimilator", allocator)
        self.assertIn("desiredGas", allocator)
        self.assertIn("isGatheringGas", allocator)
        self.assertIn("isGatheringMinerals", allocator)
        self.assertIn("isCarryingMinerals", allocator)
        self.assertIn("isCarryingGas", allocator)
        self.assertIn("canGather(target)", allocator)
        self.assertIn("getBuildLocation", construction)
        self.assertIn("Protoss_Assimilator", construction)
        self.assertIn("activeScoutTile_", memory)
        self.assertIn("holdUntilFrame_", squad)
        self.assertIn("CommandKind::Attack", (SOURCE / "src/CommandArbiter.cpp").read_text())
        self.assertIn("bool CommandArbiter::move", (SOURCE / "src/CommandArbiter.cpp").read_text())
        self.assertIn("commands.move", (SOURCE / "src/ScoutingController.cpp").read_text())
        self.assertIn("allowRallyAttack", squad)
        self.assertIn("getDistance(home) > 400", squad)
        self.assertIn("currentTargetIsHomeThreat", squad)
        self.assertIn("scoutPresent", (SOURCE / "src/ScoutingController.cpp").read_text())
        self.assertIn("scoutId = -1", (SOURCE / "src/ScoutingController.cpp").read_text())
        self.assertIn("!probe->isGatheringGas()", (SOURCE / "src/ScoutingController.cpp").read_text())
        self.assertIn("airWeapon()", memory)
        self.assertIn("callbackMs_.push_back", telemetry)
        self.assertIn("telemetry_schema\\\":\\\"kestrel-modular-v1", telemetry)
        for field in (
            "zerg_four_probe_pylon_accepted",
            "zerg_four_probe_pylon_accepted_frame",
            "zerg_four_probe_pylon_completed_probe_count",
            "accepted_probe_train_frames",
            "second_zealot_train_frame",
            "reserve_active_reserves",
            "reserve_block_pre_acceptance_flags",
            "construction_events",
            "command_categories",
            "worker_gather_preflight_skips",
            "worker_cargo_deferrals",
            "worker_accepted_gather_commands",
            "worker_builder_preflight_skips",
            "worker_builder_cargo_deferrals",
            "lone_zealot_hold_active_samples",
            "lone_zealot_hold_suppression_samples",
            "lone_zealot_hold_unique_units",
            "lone_zealot_hold_home_move_attempts",
            "lone_zealot_hold_home_move_accepted",
            "lone_zealot_hold_release_frame",
        ):
            self.assertIn(field, telemetry)
        construction_header = (SOURCE / "include/kestrel/ConstructionController.h").read_text()
        self.assertIn("struct Event", construction_header)
        self.assertIn("events()", construction_header)
        opening = (SOURCE / "include/kestrel/OpeningPolicy.h").read_text()
        self.assertIn("firstPylonAcceptedFrame", opening)
        self.assertIn("firstPylonCurrentFrame", opening)

    def test_build_has_native_official_and_unit_lanes(self):
        self.assertIn("KestrelModular", self.cmake)
        self.assertIn("KestrelModularOfficialHeaders", self.cmake)
        self.assertIn("KestrelModularUnitTests", self.cmake)
        self.assertIn("add_test", self.cmake)
        build_script = (ROOT / "scripts/build_kestrel_modular.sh").read_text()
        self.assertIn("KestrelModularOfficialHeaders", build_script)
        self.assertIn("source_manifest_sha256", build_script)
        self.assertIn("ctest", build_script)

    def test_modular_scorecard_refuses_legacy_or_incomplete_records(self):
        scorecard = (ROOT / "scripts/score_kestrel_modular_v1.py").read_text()
        self.assertIn('telemetry_schema") != "kestrel-modular-v1"', scorecard)
        self.assertIn('"elo_eligible": False', scorecard)
        self.assertIn("reserve_block_pre_acceptance_flags", scorecard)

        spec = importlib.util.spec_from_file_location(
            "modular_score", ROOT / "scripts/score_kestrel_modular_v1.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        malformed = module.validate_record({"telemetry_schema": "kestrel-modular-v1"})
        self.assertFalse(malformed["complete"])

    def test_scorecard_enforces_semantic_event_ordering(self):
        spec = importlib.util.spec_from_file_location(
            "modular_score_semantics", ROOT / "scripts/score_kestrel_modular_v1.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        record = {
            "telemetry_schema": "kestrel-modular-v1", "frame_count": 1000,
            "ended": True, "known_zerg": True, "command_count": 1,
            "rejected_commands": 0, "callback_count": 1,
            "zerg_four_probe_pylon_accepted": True,
            "zerg_four_probe_pylon_accepted_frame": 100,
            "zerg_four_probe_pylon_completed_probe_count": 5,
            "zerg_four_probe_pylon_completed_frame": 200,
            "first_pylon_accepted_frame": 100,
            "accepted_probe_train_frames": [101], "accepted_zealot_trains": 0,
            "second_zealot_train_frame": -1, "second_zealot_completed_frame": -1,
            "reserve_active_frames": [], "reserve_active_minerals": [],
            "reserve_active_reserves": [], "reserve_block_frames": [],
            "reserve_block_minerals": [], "reserve_block_reserves": [],
            "reserve_block_pre_acceptance_flags": [], "construction_events": [],
            "command_categories": {
                "build": {"attempted": 1, "rejected": 0},
                "train": {"attempted": 0, "rejected": 0},
                "gather": {"attempted": 0, "rejected": 0},
                "attack": {"attempted": 0, "rejected": 0},
                "scout": {"attempted": 0, "rejected": 0},
            },
        }
        result = module.validate_record(record)
        self.assertFalse(result["complete"])
        self.assertTrue(any("exactly four" in issue for issue in result["issues"]))

    def test_recovery_scorecard_requires_and_reconciles_worker_commandability(self):
        spec = importlib.util.spec_from_file_location(
            "modular_recovery_score", ROOT / "scripts/score_kestrel_modular_recovery.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        malformed = module.validate_recovery_record({"telemetry_schema": "kestrel-modular-v1"})
        self.assertFalse(malformed["complete"])
        self.assertTrue(any("worker_gather_preflight_skips" in issue for issue in malformed["issues"]))

    def test_hold_scorecard_reconciles_public_release_evidence(self):
        spec = importlib.util.spec_from_file_location(
            "modular_hold_score", ROOT / "scripts/score_kestrel_modular_hold.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        record = {
            "known_zerg": True,
            "second_zealot_completed_frame": 3800,
            "lone_zealot_hold_active_samples": 200,
            "lone_zealot_hold_suppression_samples": 100,
            "lone_zealot_hold_unique_units": 1,
            "lone_zealot_hold_home_move_attempts": 1,
            "lone_zealot_hold_home_move_accepted": 1,
            "lone_zealot_hold_release_frame": 3800,
        }
        self.assertEqual(module.validate_hold_evidence(record), ([], []))
        record["lone_zealot_hold_release_frame"] = 3803
        _, mechanism_issues = module.validate_hold_evidence(record)
        self.assertIn("hold release does not match the second-Zealot completion frame", mechanism_issues)


if __name__ == "__main__":
    unittest.main()
