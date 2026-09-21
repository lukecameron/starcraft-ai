#include "kestrel/Telemetry.h"
#include "kestrel/CombatPolicy.h"

#include <algorithm>
#include <chrono>
#include <cstdio>
#include <fstream>

namespace kestrel {

void Telemetry::reset() {
    callbackMs_.clear();
    maxProbes_ = maxPylons_ = maxGateways_ = maxZealots_ = maxDragoons_ = fourProbeFrames_ = 0;
}

void Telemetry::sample(const WorldSnapshot& state, const CommandArbiter& commands,
                       const StrategyPlanner& strategy, const ProductionController& production,
                       double callbackMs) {
    callbackMs_.push_back(callbackMs);
    maxProbes_ = std::max(maxProbes_, state.count(BWAPI::UnitTypes::Protoss_Probe));
    maxPylons_ = std::max(maxPylons_, state.count(BWAPI::UnitTypes::Protoss_Pylon));
    maxGateways_ = std::max(maxGateways_, state.count(BWAPI::UnitTypes::Protoss_Gateway));
    maxZealots_ = std::max(maxZealots_, state.count(BWAPI::UnitTypes::Protoss_Zealot));
    maxDragoons_ = std::max(maxDragoons_, state.count(BWAPI::UnitTypes::Protoss_Dragoon));
    const OpeningInputs& opening = strategy.opening();
    if (opening.knownZerg && opening.completedProbes >= 4 && opening.firstPylonAcceptedFrame < 0) ++fourProbeFrames_;
    (void)commands;
    (void)production;
}

void Telemetry::write(const WorldSnapshot& state, const CommandArbiter& commands,
                      const StrategyPlanner& strategy, const ProductionController& production,
                      const ConstructionController& construction, const WorkerAllocator& workers,
                      const SquadController& squads,
                      bool ended, bool won) const {
    std::ofstream out("bwapi-data/write/diagnostic.json.tmp", std::ios::trunc);
    const auto& stats = commands.stats();
    const auto& policy = strategy.telemetry();
    const char* categoryNames[] = {"build", "train", "gather", "attack", "scout"};
    bool closeThreatOriginsWithinLeash = true;
    for (const auto& event : squads.stats().loneHoldCloseThreatEvents) {
        const int dx = event.heldUnitPosition.x - loneZealotHoldAnchor(state.home).x;
        const int dy = event.heldUnitPosition.y - loneZealotHoldAnchor(state.home).y;
        if (dx * dx + dy * dy > loneZealotLeashRadius * loneZealotLeashRadius) {
            closeThreatOriginsWithinLeash = false;
            break;
        }
    }
    auto writeArray = [&out](const std::vector<int>& values) {
        out << '[';
        for (size_t i = 0; i < values.size(); ++i) {
            if (i) out << ',';
            out << values[i];
        }
        out << ']';
    };
    auto writePositions = [&out](const std::vector<BWAPI::Position>& values) {
        out << '[';
        for (size_t i = 0; i < values.size(); ++i) {
            if (i) out << ',';
            out << "{\"x\":" << values[i].x << ",\"y\":" << values[i].y << '}';
        }
        out << ']';
    };
    out << "{\"schema_version\":3,\"telemetry_schema\":\"kestrel-modular-v1\",\"bot\":\"Kestrel Modular v1\""
        << ",\"frame_count\":" << state.frame
        << ",\"known_zerg\":" << (state.knownZerg ? "true" : "false")
        << ",\"ended\":" << (ended ? "true" : "false")
        << ",\"winner\":" << (ended ? (won ? "true" : "false") : "null")
        << ",\"architecture\":\"world-memory-strategy-economy-production-construction-scout-squad-arbiter\""
        << ",\"command_count\":" << stats.attempted
        << ",\"rejected_commands\":" << stats.rejected
        << ",\"worker_gather_preflight_skips\":" << workers.stats().gatherPreflightSkips
        << ",\"worker_cargo_deferrals\":" << workers.stats().cargoDeferrals
        << ",\"worker_accepted_gather_commands\":" << workers.stats().acceptedGatherCommands
        << ",\"worker_builder_preflight_skips\":" << workers.stats().builderPreflightSkips
        << ",\"worker_builder_cargo_deferrals\":" << workers.stats().builderCargoDeferrals
        << ",\"lone_zealot_hold_active_samples\":" << squads.stats().loneHoldActiveSamples
        << ",\"lone_zealot_hold_suppression_samples\":" << squads.stats().loneHoldSuppressionSamples
        << ",\"lone_zealot_hold_unique_units\":" << squads.stats().loneHoldUniqueUnits
        << ",\"lone_zealot_hold_home_move_attempts\":" << squads.stats().loneHoldHomeMoveAttempts
        << ",\"lone_zealot_hold_home_move_accepted\":" << squads.stats().loneHoldHomeMoveAccepted
        << ",\"lone_zealot_hold_release_frame\":" << squads.stats().loneHoldReleaseFrame
        << ",\"lone_zealot_hold_leash_radius\":" << loneZealotLeashRadius
        << ",\"lone_zealot_hold_leash_block_samples\":" << squads.stats().loneHoldLeashBlockSamples
        << ",\"lone_zealot_hold_leash_move_attempts\":" << squads.stats().loneHoldLeashMoveAttempts
        << ",\"lone_zealot_hold_leash_move_accepted\":" << squads.stats().loneHoldLeashMoveAccepted
        << ",\"lone_zealot_hold_leash_move_rejected\":" << squads.stats().loneHoldLeashMoveRejected
        << ",\"lone_zealot_hold_leash_move_coalesced\":" << squads.stats().loneHoldLeashMoveCoalesced
        << ",\"lone_zealot_hold_leash_max_anchor_distance\":" << squads.stats().loneHoldMaxAnchorDistance
        << ",\"lone_zealot_hold_close_threat_radius\":" << loneZealotCloseThreatRadius
        << ",\"lone_zealot_hold_close_threat_attack_origins_within_leash\":"
        << (closeThreatOriginsWithinLeash ? "true" : "false")
        << ",\"lone_zealot_hold_anchor\":{\"start_tile_x\":" << state.home.x
        << ",\"start_tile_y\":" << state.home.y
        << ",\"x\":" << loneZealotHoldAnchor(state.home).x
        << ",\"y\":" << loneZealotHoldAnchor(state.home).y << '}'
        << ",\"lone_zealot_hold_home_move_accepted_targets\":[";
    for (size_t i = 0; i < squads.stats().loneHoldAcceptedHomeMoveTargets.size(); ++i) {
        if (i) out << ',';
        const BWAPI::Position target = squads.stats().loneHoldAcceptedHomeMoveTargets[i];
        out << "{\"x\":" << target.x << ",\"y\":" << target.y << '}';
    }
    out << ']'
        << ",\"lone_zealot_hold_close_threat_samples\":" << squads.stats().loneHoldCloseThreatSamples
        << ",\"lone_zealot_hold_close_threat_first_frame\":" << squads.stats().loneHoldCloseThreatFirstFrame
        << ",\"lone_zealot_hold_close_threat_attack_attempts\":" << squads.stats().loneHoldCloseThreatAttackAttempts
        << ",\"lone_zealot_hold_close_threat_attack_accepted\":" << squads.stats().loneHoldCloseThreatAttackAccepted
        << ",\"lone_zealot_hold_close_threat_attack_rejected\":" << squads.stats().loneHoldCloseThreatAttackRejected
        << ",\"lone_zealot_hold_close_threat_accepted_frames\":";
    writeArray(squads.stats().loneHoldCloseThreatAcceptedFrames);
    out << ",\"lone_zealot_hold_close_threat_accepted_held_unit_ids\":";
    writeArray(squads.stats().loneHoldCloseThreatAcceptedHeldUnitIds);
    out << ",\"lone_zealot_hold_close_threat_accepted_target_ids\":";
    writeArray(squads.stats().loneHoldCloseThreatAcceptedTargetIds);
    out << ",\"lone_zealot_hold_close_threat_accepted_held_positions\":";
    writePositions(squads.stats().loneHoldCloseThreatAcceptedHeldPositions);
    out << ",\"lone_zealot_hold_close_threat_accepted_target_positions\":";
    writePositions(squads.stats().loneHoldCloseThreatAcceptedTargetPositions);
    out << ",\"lone_zealot_hold_close_threat_events\":[";
    for (size_t i = 0; i < squads.stats().loneHoldCloseThreatEvents.size(); ++i) {
        if (i) out << ',';
        const auto& event = squads.stats().loneHoldCloseThreatEvents[i];
        out << "{\"frame\":" << event.frame
            << ",\"held_unit_id\":" << event.heldUnitId
            << ",\"target_id\":" << event.targetId
            << ",\"held_unit_position\":{\"x\":" << event.heldUnitPosition.x
            << ",\"y\":" << event.heldUnitPosition.y << '}'
            << ",\"target_position\":{\"x\":" << event.targetPosition.x
            << ",\"y\":" << event.targetPosition.y << '}'
            << ",\"accepted\":" << (event.accepted ? "true" : "false") << '}';
    }
    out << "],\"lone_zealot_hold_unit_lifecycles\":[";
    for (size_t i = 0; i < squads.stats().loneHoldUnitLifecycles.size(); ++i) {
        if (i) out << ',';
        const auto& lifecycle = squads.stats().loneHoldUnitLifecycles[i];
        out << "{\"unit_id\":" << lifecycle.unitId
            << ",\"first_seen_frame\":" << lifecycle.firstSeenFrame
            << ",\"last_seen_frame\":" << lifecycle.lastSeenFrame
            << ",\"close_threat_samples\":" << lifecycle.closeThreatSamples
            << ",\"close_threat_attack_attempts\":" << lifecycle.closeThreatAttackAttempts
            << ",\"close_threat_attack_accepted\":" << lifecycle.closeThreatAttackAccepted
            << ",\"close_threat_attack_rejected\":" << lifecycle.closeThreatAttackRejected
            << ",\"first_close_threat_frame\":" << lifecycle.firstCloseThreatFrame
            << ",\"last_close_threat_frame\":" << lifecycle.lastCloseThreatFrame
            << ",\"anchor_move_attempts\":" << lifecycle.anchorMoveAttempts
            << ",\"anchor_move_accepted\":" << lifecycle.anchorMoveAccepted
            << ",\"leash_block_samples\":" << lifecycle.leashBlockSamples
            << ",\"leash_move_attempts\":" << lifecycle.leashMoveAttempts
            << ",\"leash_move_accepted\":" << lifecycle.leashMoveAccepted
            << ",\"leash_move_rejected\":" << lifecycle.leashMoveRejected
            << ",\"leash_move_coalesced\":" << lifecycle.leashMoveCoalesced
            << ",\"max_anchor_distance\":" << lifecycle.maxAnchorDistance << '}';
    }
    out << ']'
        << ",\"max_probes\":" << maxProbes_
        << ",\"max_pylons\":" << maxPylons_
        << ",\"max_gateways\":" << maxGateways_
        << ",\"max_zealots\":" << maxZealots_
        << ",\"max_dragoons\":" << maxDragoons_
        << ",\"zerg_four_probe_policy_active_frames\":" << fourProbeFrames_
        << ",\"zerg_four_probe_pylon_accepted\":" << (policy.zergFourProbePylonAccepted ? "true" : "false")
        << ",\"zerg_four_probe_pylon_accepted_frame\":" << policy.zergFourProbePylonAcceptedFrame
        << ",\"zerg_four_probe_pylon_completed_probe_count\":" << policy.zergFourProbePylonCompletedProbeCount
        << ",\"zerg_four_probe_pylon_completed_frame\":" << policy.zergFourProbePylonCompletedFrame
        << ",\"accepted_probe_train_frames\":";
    writeArray(production.acceptedProbeTrainFrames());
    out << ",\"accepted_zealot_trains\":" << production.acceptedZealotTrains()
        << ",\"second_zealot_train_frame\":" << production.secondZealotTrainFrame()
        << ",\"callback_count\":" << callbackMs_.size()
        << ",\"callback_wall_max_ms\":" << (callbackMs_.empty() ? 0.0 : *std::max_element(callbackMs_.begin(), callbackMs_.end()))
        << ",\"first_pylon_accepted_frame\":" << strategy.firstPylonAcceptedFrame()
        << ",\"first_pylon_current_frame\":" << strategy.firstPylonCurrentFrame()
        << ",\"first_gateway_accepted_frame\":" << strategy.firstGatewayAcceptedFrame()
        << ",\"first_gateway_current_frame\":" << strategy.firstGatewayCurrentFrame()
        << ",\"second_gateway_accepted_frame\":" << strategy.secondGatewayAcceptedFrame()
        << ",\"second_gateway_current_frame\":" << strategy.secondGatewayCurrentFrame()
        << ",\"second_zealot_completed_frame\":" << strategy.secondZealotCompletedFrame()
        << ",\"reserve_active_frames\":";
    {
        std::vector<int> values;
        for (const auto& sample : production.reserveActive()) values.push_back(sample.frame);
        writeArray(values);
    }
    out << ",\"reserve_active_minerals\":";
    {
        std::vector<int> values;
        for (const auto& sample : production.reserveActive()) values.push_back(sample.availableMinerals);
        writeArray(values);
    }
    out << ",\"reserve_active_reserves\":";
    {
        std::vector<int> values;
        for (const auto& sample : production.reserveActive()) values.push_back(sample.reserve);
        writeArray(values);
    }
    out << ",\"reserve_block_frames\":";
    {
        std::vector<int> values;
        for (const auto& sample : production.reserveBlocks()) values.push_back(sample.frame);
        writeArray(values);
    }
    out << ",\"reserve_block_minerals\":";
    {
        std::vector<int> values;
        for (const auto& sample : production.reserveBlocks()) values.push_back(sample.availableMinerals);
        writeArray(values);
    }
    out << ",\"reserve_block_reserves\":";
    {
        std::vector<int> values;
        for (const auto& sample : production.reserveBlocks()) values.push_back(sample.reserve);
        writeArray(values);
    }
    out << ",\"reserve_block_pre_acceptance_flags\":";
    {
        std::vector<int> values;
        for (const auto& sample : production.reserveBlocks()) values.push_back(sample.preSecondZealotAcceptance);
        writeArray(values);
    }
    out << ",\"construction_events\":[";
    for (size_t i = 0; i < construction.events().size(); ++i) {
        if (i) out << ',';
        const auto& event = construction.events()[i];
        out << "{\"type_id\":" << event.typeId
            << ",\"baseline\":" << event.baseline
            << ",\"accepted_frame\":" << event.acceptedFrame
            << ",\"current_frame\":" << event.currentFrame
            << ",\"completed_frame\":" << event.completedFrame << '}';
    }
    out << "],\"command_categories\":{";
    for (size_t i = 0; i < 5; ++i) {
        if (i) out << ',';
        out << '\"' << categoryNames[i] << "\":{\"attempted\":" << stats.attemptedByKind[i]
            << ",\"rejected\":" << stats.rejectedByKind[i] << '}';
    }
    out << "},\"command_error_counts\":{\"unit_busy\":"
        << stats.errors[BWAPI::Errors::Enum::Unit_Busy] << "}}\n";
    out.close();
    if (out) {
        std::remove("bwapi-data/write/diagnostic.json");
        std::rename("bwapi-data/write/diagnostic.json.tmp", "bwapi-data/write/diagnostic.json");
    }
}

}  // namespace kestrel
