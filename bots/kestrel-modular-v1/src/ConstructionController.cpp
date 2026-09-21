#include "kestrel/ConstructionController.h"

namespace kestrel {

void ConstructionController::reset() {
    pendingType_ = BWAPI::UnitTypes::None;
    baseline_ = 0;
    builderId_ = -1;
    acceptedFrame_ = -1;
    events_.clear();
}

void ConstructionController::observe(const WorldSnapshot& state) {
    for (auto& event : events_) {
        if (event.currentFrame < 0 && state.count(BWAPI::UnitType(event.typeId)) > event.baseline)
            event.currentFrame = state.frame;
        if (event.completedFrame < 0 && state.count(BWAPI::UnitType(event.typeId), true) > event.baseline)
            event.completedFrame = state.frame;
    }
}

void ConstructionController::clear(int& externalBuilderId) {
    pendingType_ = BWAPI::UnitTypes::None;
    baseline_ = 0;
    builderId_ = -1;
    acceptedFrame_ = -1;
    externalBuilderId = -1;
}

bool ConstructionController::pending(const WorldSnapshot& state) const {
    if (pendingType_ == BWAPI::UnitTypes::None) return false;
    if (state.count(pendingType_) > baseline_) return false;
    return state.frame - acceptedFrame_ < 480;
}

bool ConstructionController::tick(const WorldSnapshot& state, const BuildIntent& intent, int scoutId,
                                   int& builderId, CommandArbiter& commands, WorkerAllocator& workers) {
    if (pendingType_ != BWAPI::UnitTypes::None && state.count(pendingType_) > baseline_) clear(builderId);
    if (pendingType_ != BWAPI::UnitTypes::None && state.frame - acceptedFrame_ >= 480) clear(builderId);
    if (pending(state) || !intent.valid()) return false;
    BWAPI::Unit builder = workers.findBuilder(state, scoutId, builderId);
    if (!builder) return false;
    BWAPI::TilePosition tile = intent.near;
    if (intent.type == BWAPI::UnitTypes::Protoss_Assimilator) {
        BWAPI::Unit best = nullptr;
        int bestDistance = 1 << 30;
        const BWAPI::Position home(state.home);
        for (auto geyser : state.geysers) {
            if (!geyser || !geyser->exists()) continue;
            bool occupied = false;
            for (auto unit : state.ownUnits) {
                if (unit && unit->exists() && unit->getType() == BWAPI::UnitTypes::Protoss_Assimilator &&
                    unit->getDistance(geyser) < 64) { occupied = true; break; }
            }
            if (occupied) continue;
            const int distance = geyser->getDistance(home);
            if (distance < bestDistance) { bestDistance = distance; best = geyser; }
        }
        if (!best) return false;
        tile = best->getTilePosition();
    } else {
        tile = BWAPI::Broodwar->getBuildLocation(intent.type, intent.near, 32, false);
    }
    if (!tile.isValid()) return false;
    const bool accepted = commands.issue(builder->build(intent.type, tile), CommandKind::Build);
    if (!accepted) return false;
    builderId = builder->getID();
    builderId_ = builder->getID();
    pendingType_ = intent.type;
    baseline_ = state.count(intent.type);
    acceptedFrame_ = state.frame;
    events_.push_back({intent.type.getID(), baseline_, state.frame, -1, -1});
    return true;
}

}  // namespace kestrel
