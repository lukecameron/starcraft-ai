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
        self.assertIn("loneZealotLeashRadius", squad)
        self.assertIn("loneZealotReturnReleaseRadius", squad)
        self.assertIn("anchorDistance > loneZealotLeashRadius", squad)
        self.assertIn("returningToAnchor_", (SOURCE / "include/kestrel/SquadController.h").read_text())
        self.assertIn("loneZealotReturnReleaseRadius", squad)
        self.assertIn("loneHoldLeashBlockSamples", squad)
        self.assertIn("candidate->getDistance(loneHoldHome) > loneZealotCloseThreatRadius", squad)
        self.assertIn("candidate->getType().groundWeapon() == BWAPI::WeaponTypes::None", squad)
        self.assertIn("commands.attack(unit, closeThreat, state.frame, &issued)", squad)
        self.assertNotIn("commands.attackMove(unit, loneHoldHome", squad)
        arbiter_source = (SOURCE / "src/CommandArbiter.cpp").read_text()
        arbiter_header = (SOURCE / "include/kestrel/CommandArbiter.h").read_text()
        self.assertIn("bool* issued", arbiter_source)
        self.assertIn("bool* issued = nullptr", arbiter_header)
        self.assertIn("bool CommandArbiter::move", arbiter_source)
        self.assertIn("scoutPresent", (SOURCE / "src/ScoutingController.cpp").read_text())
        self.assertIn("scoutId = -1", (SOURCE / "src/ScoutingController.cpp").read_text())
        self.assertIn("!probe->isGatheringGas()", (SOURCE / "src/ScoutingController.cpp").read_text())
        self.assertIn("airWeapon()", memory)
        self.assertIn("callbackMs_.push_back", telemetry)
        self.assertIn("telemetry_schema\\\":\\\"kestrel-modular-v1", telemetry)
        self.assertIn('<< ",\\\"latency_frames\\\":" << state.latencyFrames', telemetry)
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
            "lone_zealot_hold_anchor",
            "lone_zealot_hold_home_move_accepted_targets",
            "lone_zealot_hold_leash_radius",
            "lone_zealot_hold_leash_block_samples",
            "lone_zealot_hold_leash_move_attempts",
            "lone_zealot_hold_leash_move_accepted",
            "lone_zealot_hold_leash_move_rejected",
            "lone_zealot_hold_leash_move_coalesced",
            "lone_zealot_hold_leash_max_anchor_distance",
            "lone_zealot_hold_return_release_radius",
            "lone_zealot_hold_return_entries",
            "lone_zealot_hold_return_active_samples",
            "lone_zealot_hold_return_releases",
            "lone_zealot_hold_return_move_attempts",
            "lone_zealot_hold_return_move_accepted",
            "lone_zealot_hold_return_move_rejected",
            "lone_zealot_hold_return_move_coalesced",
            "lone_zealot_hold_close_threat_samples",
            "lone_zealot_hold_close_threat_radius",
            "lone_zealot_hold_close_threat_attack_origins_within_leash",
            "lone_zealot_hold_close_threat_first_frame",
            "lone_zealot_hold_close_threat_attack_attempts",
            "lone_zealot_hold_close_threat_attack_accepted",
            "lone_zealot_hold_close_threat_attack_rejected",
            "lone_zealot_hold_close_threat_accepted_frames",
            "lone_zealot_hold_close_threat_accepted_held_unit_ids",
            "lone_zealot_hold_close_threat_accepted_target_ids",
            "lone_zealot_hold_close_threat_accepted_held_positions",
            "lone_zealot_hold_close_threat_accepted_target_positions",
            "lone_zealot_hold_close_threat_events",
            "lone_zealot_hold_unit_lifecycles",
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
            "latency_frames": 3,
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
            "lone_zealot_hold_close_threat_samples": 0,
            "lone_zealot_hold_close_threat_radius": 160,
            "lone_zealot_hold_close_threat_first_frame": -1,
            "lone_zealot_hold_close_threat_attack_attempts": 0,
            "lone_zealot_hold_close_threat_attack_accepted": 0,
            "lone_zealot_hold_close_threat_attack_rejected": 0,
            "lone_zealot_hold_close_threat_accepted_frames": [],
            "lone_zealot_hold_close_threat_accepted_held_unit_ids": [],
            "lone_zealot_hold_close_threat_accepted_target_ids": [],
            "lone_zealot_hold_close_threat_accepted_held_positions": [],
            "lone_zealot_hold_close_threat_accepted_target_positions": [],
            "lone_zealot_hold_close_threat_events": [],
            "lone_zealot_hold_unit_lifecycles": [],
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

    def _close_threat_record(self):
        return {
            "telemetry_schema": "kestrel-modular-v1",
            "latency_frames": 3,
            "lone_zealot_hold_close_threat_samples": 2,
            "lone_zealot_hold_close_threat_radius": 160,
            "lone_zealot_hold_leash_radius": 96,
            "lone_zealot_hold_leash_block_samples": 0,
            "lone_zealot_hold_leash_move_attempts": 0,
            "lone_zealot_hold_leash_move_accepted": 0,
            "lone_zealot_hold_leash_move_rejected": 0,
            "lone_zealot_hold_leash_move_coalesced": 0,
            "lone_zealot_hold_leash_max_anchor_distance": 60,
            "lone_zealot_hold_return_release_radius": 48,
            "lone_zealot_hold_return_entries": 0,
            "lone_zealot_hold_return_active_samples": 0,
            "lone_zealot_hold_return_releases": 0,
            "lone_zealot_hold_return_move_attempts": 0,
            "lone_zealot_hold_return_move_accepted": 0,
            "lone_zealot_hold_return_move_rejected": 0,
            "lone_zealot_hold_return_move_coalesced": 0,
            "lone_zealot_hold_close_threat_attack_origins_within_leash": True,
            "lone_zealot_hold_anchor": {"start_tile_x": 117, "start_tile_y": 56, "x": 3808, "y": 1840},
            "lone_zealot_hold_close_threat_first_frame": 90,
            "lone_zealot_hold_close_threat_attack_attempts": 1,
            "lone_zealot_hold_close_threat_attack_accepted": 1,
            "lone_zealot_hold_close_threat_attack_rejected": 0,
            "lone_zealot_hold_close_threat_accepted_frames": [100],
            "lone_zealot_hold_close_threat_accepted_held_unit_ids": [7],
            "lone_zealot_hold_close_threat_accepted_target_ids": [42],
            "lone_zealot_hold_close_threat_accepted_held_positions": [{"x": 3800, "y": 1800}],
            "lone_zealot_hold_close_threat_accepted_target_positions": [{"x": 3860, "y": 1800}],
            "lone_zealot_hold_close_threat_events": [{
                "frame": 100, "held_unit_id": 7, "target_id": 42,
                "held_unit_position": {"x": 3800, "y": 1800},
                "target_position": {"x": 3860, "y": 1800}, "accepted": True,
            }],
            "lone_zealot_hold_unit_lifecycles": [{
                "unit_id": 7, "first_seen_frame": 90, "last_seen_frame": 100,
                "close_threat_samples": 2, "close_threat_attack_attempts": 1,
                "close_threat_attack_accepted": 1, "close_threat_attack_rejected": 0,
                "first_close_threat_frame": 90, "last_close_threat_frame": 100,
                "anchor_move_attempts": 0, "anchor_move_accepted": 0,
                "leash_block_samples": 0, "leash_move_attempts": 0,
                "leash_move_accepted": 0, "leash_move_rejected": 0,
                "leash_move_coalesced": 0, "max_anchor_distance": 60,
                "return_entries": 0, "return_active_samples": 0,
                "return_releases": 0, "return_move_attempts": 0,
                "return_move_accepted": 0, "return_move_rejected": 0,
                "return_move_coalesced": 0,
            }],
        }

    def _load_close_threat_scorecard(self):
        spec = importlib.util.spec_from_file_location(
            "modular_score_close_threat", ROOT / "scripts/score_kestrel_modular_v1.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_close_threat_scorecard_reconciles_attempts_and_events(self):
        module = self._load_close_threat_scorecard()
        record = self._close_threat_record()
        result = module.validate_record(record)
        self.assertFalse(any("close-threat" in issue for issue in result["issues"]))
        record["lone_zealot_hold_close_threat_attack_rejected"] = 1
        result = module.validate_record(record)
        self.assertIn("close-threat attack attempts do not reconcile with acceptance and rejection", result["issues"])
        record["lone_zealot_hold_close_threat_attack_rejected"] = 0
        record["lone_zealot_hold_close_threat_radius"] = 159
        result = module.validate_record(record)
        self.assertIn("lone_zealot_hold_close_threat_radius must equal 160", result["issues"])

    def test_close_threat_scorecard_rejects_accepted_event_with_empty_arrays(self):
        module = self._load_close_threat_scorecard()
        record = self._close_threat_record()
        for key in (
                "lone_zealot_hold_close_threat_accepted_frames",
                "lone_zealot_hold_close_threat_accepted_held_unit_ids",
                "lone_zealot_hold_close_threat_accepted_target_ids",
                "lone_zealot_hold_close_threat_accepted_held_positions",
                "lone_zealot_hold_close_threat_accepted_target_positions"):
            record[key] = []
        result = module.validate_record(record)
        self.assertTrue(any("length does not match accepted attacks" in issue for issue in result["issues"]))

    def test_close_threat_scorecard_rejects_empty_lifecycles(self):
        module = self._load_close_threat_scorecard()
        record = self._close_threat_record()
        record["lone_zealot_hold_unit_lifecycles"] = []
        result = module.validate_record(record)
        self.assertIn("close-threat evidence has no held-unit lifecycle records", result["issues"])
        self.assertIn("close-threat event has no held-unit lifecycle", result["issues"])

    def test_close_threat_scorecard_reconciles_command_category(self):
        module = self._load_close_threat_scorecard()
        record = self._close_threat_record()
        record["command_categories"] = {
            category: {"attempted": 0, "rejected": 0}
            for category in ("build", "train", "gather", "attack", "scout")
        }
        result = module.validate_record(record)
        self.assertIn("close-threat attempts exceed issued attack commands", result["issues"])

    def test_leash_scorecard_reconciles_moves_and_attack_origins(self):
        module = self._load_close_threat_scorecard()
        record = self._close_threat_record()
        record["lone_zealot_hold_leash_block_samples"] = 3
        record["lone_zealot_hold_leash_move_attempts"] = 1
        record["lone_zealot_hold_leash_move_accepted"] = 1
        record["lone_zealot_hold_leash_move_coalesced"] = 2
        record["lone_zealot_hold_return_entries"] = 1
        record["lone_zealot_hold_return_active_samples"] = 3
        record["lone_zealot_hold_return_releases"] = 1
        record["lone_zealot_hold_return_move_attempts"] = 1
        record["lone_zealot_hold_return_move_accepted"] = 1
        record["lone_zealot_hold_return_move_coalesced"] = 2
        record["lone_zealot_hold_unit_lifecycles"][0].update({
            "leash_block_samples": 3, "leash_move_attempts": 1,
            "leash_move_accepted": 1, "leash_move_rejected": 0,
            "leash_move_coalesced": 2, "max_anchor_distance": 100,
            "return_entries": 1, "return_active_samples": 3,
            "return_releases": 1, "return_move_attempts": 1,
            "return_move_accepted": 1, "return_move_rejected": 0,
            "return_move_coalesced": 2,
        })
        record["lone_zealot_hold_leash_max_anchor_distance"] = 100
        result = module.validate_record(record)
        self.assertFalse(any("leash" in issue for issue in result["issues"]))
        record["lone_zealot_hold_leash_move_coalesced"] = 1
        result = module.validate_record(record)
        self.assertIn("leash blocks do not reconcile with actual and coalesced moves", result["issues"])
        record = self._close_threat_record()
        record["lone_zealot_hold_close_threat_events"][0]["held_unit_position"] = {"x": 3700, "y": 1840}
        result = module.validate_record(record)
        self.assertIn("close-threat attack origin exceeded leash radius", result["issues"])

    def test_return_hysteresis_scorecard_reconciles_and_does_not_require_activity(self):
        module = self._load_close_threat_scorecard()
        record = self._close_threat_record()
        record["lone_zealot_hold_return_entries"] = 1
        record["lone_zealot_hold_return_active_samples"] = 3
        record["lone_zealot_hold_return_releases"] = 1
        record["lone_zealot_hold_return_move_attempts"] = 1
        record["lone_zealot_hold_return_move_accepted"] = 1
        record["lone_zealot_hold_return_move_coalesced"] = 2
        record["lone_zealot_hold_leash_block_samples"] = 3
        record["lone_zealot_hold_leash_move_attempts"] = 1
        record["lone_zealot_hold_leash_move_accepted"] = 1
        record["lone_zealot_hold_leash_move_coalesced"] = 2
        record["lone_zealot_hold_leash_max_anchor_distance"] = 100
        record["lone_zealot_hold_unit_lifecycles"][0].update({
            "return_entries": 1, "return_active_samples": 3,
            "return_releases": 1, "return_move_attempts": 1,
            "return_move_accepted": 1, "return_move_rejected": 0,
            "return_move_coalesced": 2,
            "leash_block_samples": 3, "leash_move_attempts": 1,
            "leash_move_accepted": 1, "leash_move_rejected": 0,
            "leash_move_coalesced": 2, "max_anchor_distance": 100,
        })
        result = module.validate_record(record)
        self.assertFalse(any("return" in issue for issue in result["issues"]))

        record["lone_zealot_hold_return_move_coalesced"] = 1
        result = module.validate_record(record)
        self.assertIn("return active samples do not reconcile with move outcomes", result["issues"])

        record = self._close_threat_record()
        record["lone_zealot_hold_return_releases"] = 1
        result = module.validate_record(record)
        self.assertIn("return releases exceed return entries", result["issues"])
        self.assertFalse(any("return activity was not observed" in issue for issue in result["mechanism_issues"]))

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
            "lone_zealot_hold_anchor": {"start_tile_x": 10, "start_tile_y": 20, "x": 384, "y": 688},
            "lone_zealot_hold_home_move_accepted_targets": [{"x": 384, "y": 688}],
        }
        self.assertEqual(module.validate_hold_evidence(record), ([], []))
        record["lone_zealot_hold_home_move_accepted_targets"][0]["x"] = 320
        issues, _ = module.validate_hold_evidence(record)
        self.assertIn("accepted lone-hold move did not target the public base center", issues)
        record["lone_zealot_hold_home_move_accepted_targets"][0]["x"] = 384
        record["lone_zealot_hold_release_frame"] = 3803
        _, mechanism_issues = module.validate_hold_evidence(record)
        self.assertIn("hold release does not match the second-Zealot completion frame", mechanism_issues)


if __name__ == "__main__":
    unittest.main()
