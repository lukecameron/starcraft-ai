#pragma once

#include "kestrel/CommandArbiter.h"
#include "kestrel/WorldMemory.h"

#include <unordered_set>
#include <vector>

namespace kestrel {

class SquadController {
public:
    struct Stats {
        int loneHoldActiveSamples = 0;
        int loneHoldSuppressionSamples = 0;
        int loneHoldUniqueUnits = 0;
        int loneHoldHomeMoveAttempts = 0;
        int loneHoldHomeMoveAccepted = 0;
        int loneHoldReleaseFrame = -1;
        std::vector<BWAPI::Position> loneHoldAcceptedHomeMoveTargets;
    };

    void reset() {
        holdUntilFrame_ = -1;
        loneHoldWasActive_ = false;
        suppressedUnits_.clear();
        stats_ = Stats{};
    }
    void tick(const WorldSnapshot& state, WorldMemory& memory, CommandArbiter& commands,
              bool allowRallyAttack);
    const Stats& stats() const { return stats_; }

private:
    int holdUntilFrame_ = -1;
    bool loneHoldWasActive_ = false;
    std::unordered_set<int> suppressedUnits_;
    Stats stats_;
};

}  // namespace kestrel
