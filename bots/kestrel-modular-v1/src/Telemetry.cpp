#include "kestrel/Telemetry.h"

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
                      const ConstructionController& construction, bool ended, bool won) const {
    std::ofstream out("bwapi-data/write/diagnostic.json.tmp", std::ios::trunc);
    const auto& stats = commands.stats();
    const auto& policy = strategy.telemetry();
    const char* categoryNames[] = {"build", "train", "gather", "attack", "scout"};
    auto writeArray = [&out](const std::vector<int>& values) {
        out << '[';
        for (size_t i = 0; i < values.size(); ++i) {
            if (i) out << ',';
            out << values[i];
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
