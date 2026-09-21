#pragma once

#include "kestrel/Types.h"

#include <unordered_map>

namespace kestrel {

struct EnemyMemory {
    BWAPI::Position lastPosition;
    BWAPI::UnitType lastType = BWAPI::UnitTypes::None;
    int lastSeenFrame = -1;
};

class WorldMemory {
public:
    void reset(const WorldSnapshot& state);
    void update(const WorldSnapshot& state);
    // Returns a persistent target until the corresponding start tile is explored.
    BWAPI::Position scoutTarget(const WorldSnapshot& state);
    BWAPI::Unit nearestVisibleEnemy(BWAPI::Unit from, const WorldSnapshot& state) const;
    const std::unordered_map<int, EnemyMemory>& enemies() const { return enemies_; }

private:
    int nextStart_ = 0;
    BWAPI::TilePosition activeScoutTile_;
    BWAPI::Position activeScoutTarget_;
    std::unordered_map<int, EnemyMemory> enemies_;
};

}  // namespace kestrel
