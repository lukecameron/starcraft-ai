#pragma once

#include "kestrel/CommandArbiter.h"
#include "kestrel/StrategyPlanner.h"
#include "kestrel/ProductionController.h"
#include "kestrel/ConstructionController.h"
#include "kestrel/SquadController.h"
#include "kestrel/WorkerAllocator.h"

#include <vector>

namespace kestrel {

class Telemetry {
public:
    void reset();
    void sample(const WorldSnapshot& state, const CommandArbiter& commands,
                const StrategyPlanner& strategy, const ProductionController& production,
                double callbackMs);
    void write(const WorldSnapshot& state, const CommandArbiter& commands,
               const StrategyPlanner& strategy, const ProductionController& production,
               const ConstructionController& construction, const WorkerAllocator& workers,
               const SquadController& squads,
               bool ended, bool won) const;

private:
    std::vector<double> callbackMs_;
    int maxProbes_ = 0;
    int maxPylons_ = 0;
    int maxGateways_ = 0;
    int maxZealots_ = 0;
    int maxDragoons_ = 0;
    int fourProbeFrames_ = 0;
};

}  // namespace kestrel
