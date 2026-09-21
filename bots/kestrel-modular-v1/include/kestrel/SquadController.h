#pragma once

#include "kestrel/CommandArbiter.h"
#include "kestrel/WorldMemory.h"

#include <unordered_set>
#include <vector>

namespace kestrel {

class SquadController {
public:
    struct CloseThreatEvent {
        int frame = -1;
        int heldUnitId = -1;
        int targetId = -1;
        BWAPI::Position heldUnitPosition = BWAPI::Positions::None;
        BWAPI::Position targetPosition = BWAPI::Positions::None;
        bool accepted = false;
    };

    struct HeldUnitLifecycle {
        int unitId = -1;
        int firstSeenFrame = -1;
        int lastSeenFrame = -1;
        int closeThreatSamples = 0;
        int closeThreatAttackAttempts = 0;
        int closeThreatAttackAccepted = 0;
        int closeThreatAttackRejected = 0;
        int firstCloseThreatFrame = -1;
        int lastCloseThreatFrame = -1;
        int anchorMoveAttempts = 0;
        int anchorMoveAccepted = 0;
        int leashBlockSamples = 0;
        int leashMoveAttempts = 0;
        int leashMoveAccepted = 0;
        int leashMoveRejected = 0;
        int leashMoveCoalesced = 0;
        int maxAnchorDistance = 0;
    };

    struct Stats {
        int loneHoldActiveSamples = 0;
        int loneHoldSuppressionSamples = 0;
        int loneHoldUniqueUnits = 0;
        int loneHoldHomeMoveAttempts = 0;
        int loneHoldHomeMoveAccepted = 0;
        int loneHoldReleaseFrame = -1;
        std::vector<BWAPI::Position> loneHoldAcceptedHomeMoveTargets;
        int loneHoldLeashBlockSamples = 0;
        int loneHoldLeashMoveAttempts = 0;
        int loneHoldLeashMoveAccepted = 0;
        int loneHoldLeashMoveRejected = 0;
        int loneHoldLeashMoveCoalesced = 0;
        int loneHoldMaxAnchorDistance = 0;
        int loneHoldCloseThreatSamples = 0;
        int loneHoldCloseThreatFirstFrame = -1;
        int loneHoldCloseThreatAttackAttempts = 0;
        int loneHoldCloseThreatAttackAccepted = 0;
        int loneHoldCloseThreatAttackRejected = 0;
        std::vector<int> loneHoldCloseThreatAcceptedFrames;
        std::vector<int> loneHoldCloseThreatAcceptedHeldUnitIds;
        std::vector<int> loneHoldCloseThreatAcceptedTargetIds;
        std::vector<BWAPI::Position> loneHoldCloseThreatAcceptedHeldPositions;
        std::vector<BWAPI::Position> loneHoldCloseThreatAcceptedTargetPositions;
        std::vector<CloseThreatEvent> loneHoldCloseThreatEvents;
        std::vector<HeldUnitLifecycle> loneHoldUnitLifecycles;
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
    HeldUnitLifecycle& lifecycleFor(int unitId, int frame);

    int holdUntilFrame_ = -1;
    bool loneHoldWasActive_ = false;
    std::unordered_set<int> suppressedUnits_;
    Stats stats_;
};

}  // namespace kestrel
