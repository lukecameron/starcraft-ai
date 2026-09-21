#include "kestrel/WorldMemory.h"

#include <algorithm>
#include <limits>

namespace kestrel {

void WorldMemory::reset(const WorldSnapshot& state) {
    nextStart_ = 0;
    activeScoutTile_ = BWAPI::TilePositions::None;
    activeScoutTarget_ = BWAPI::Positions::None;
    enemies_.clear();
    update(state);
}

void WorldMemory::update(const WorldSnapshot& state) {
    for (auto enemy : state.visibleEnemies) {
        if (!enemy) continue;
        enemies_[enemy->getID()] = {enemy->getPosition(), enemy->getType(), state.frame};
    }
}

BWAPI::Position WorldMemory::scoutTarget(const WorldSnapshot& state) {
    if (state.starts.empty()) return BWAPI::Positions::None;
    if (activeScoutTile_.isValid()) {
        for (const StartLocation& start : state.starts) {
            if (start.tile == activeScoutTile_ && !start.explored) return activeScoutTarget_;
        }
        activeScoutTile_ = BWAPI::TilePositions::None;
        activeScoutTarget_ = BWAPI::Positions::None;
    }
    for (size_t offset = 0; offset < state.starts.size(); ++offset) {
        const size_t index = (static_cast<size_t>(nextStart_) + offset) % state.starts.size();
        const StartLocation& start = state.starts[index];
        if (start.tile == state.home || start.explored) continue;
        nextStart_ = static_cast<int>((index + 1) % state.starts.size());
        activeScoutTile_ = start.tile;
        activeScoutTarget_ = BWAPI::Position(start.tile.x * 32 + 64, start.tile.y * 32 + 48);
        return activeScoutTarget_;
    }
    return BWAPI::Positions::None;
}

BWAPI::Unit WorldMemory::nearestVisibleEnemy(BWAPI::Unit from, const WorldSnapshot& state) const {
    if (!from) return nullptr;
    BWAPI::Unit result = nullptr;
    int distance = std::numeric_limits<int>::max();
    for (auto enemy : state.visibleEnemies) {
        if (!enemy) continue;
        const BWAPI::WeaponType weapon = enemy->isFlying() ? from->getType().airWeapon() : from->getType().groundWeapon();
        if (weapon == BWAPI::WeaponTypes::None) continue;
        const int candidate = from->getDistance(enemy);
        if (candidate < distance || (candidate == distance && result && enemy->getID() < result->getID())) {
            distance = candidate;
            result = enemy;
        }
    }
    return result;
}

}  // namespace kestrel
