#pragma once

#include "kestrel/CommandArbiter.h"
#include "kestrel/Types.h"

namespace kestrel {

class WorkerAllocator {
public:
    struct Stats {
        int gatherPreflightSkips = 0;
        int cargoDeferrals = 0;
        int acceptedGatherCommands = 0;
        int builderPreflightSkips = 0;
        int builderCargoDeferrals = 0;
    };

    void reset() { stats_ = Stats{}; }
    BWAPI::Unit findBuilder(const WorldSnapshot& state, int scoutId, int builderId,
                            BWAPI::UnitType type, BWAPI::TilePosition tile);
    void tick(const WorldSnapshot& state, int scoutId, int builderId, CommandArbiter& commands);
    const Stats& stats() const { return stats_; }

private:
    bool gather(BWAPI::Unit worker, BWAPI::Unit target, CommandArbiter& commands);
    Stats stats_;
};

}  // namespace kestrel
