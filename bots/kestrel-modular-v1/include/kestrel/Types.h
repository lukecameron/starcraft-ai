#pragma once

#include <BWAPI.h>

#include <vector>

namespace kestrel {

enum class CommandKind { Build, Train, Gather, Attack, Scout };

struct StartLocation {
    BWAPI::TilePosition tile;
    bool explored = false;
};

struct WorldSnapshot {
    int frame = 0;
    int latencyFrames = 6;
    bool knownZerg = false;
    int minerals = 0;
    int gas = 0;
    int supplyUsed = 0;
    int supplyTotal = 0;
    BWAPI::TilePosition home;
    std::vector<BWAPI::Unit> ownUnits;
    std::vector<BWAPI::Unit> visibleEnemies;
    std::vector<BWAPI::Unit> mineralsFields;
    std::vector<BWAPI::Unit> geysers;
    std::vector<StartLocation> starts;

    int count(BWAPI::UnitType type, bool completedOnly = false) const {
        int result = 0;
        for (auto unit : ownUnits) {
            if (!unit || !unit->exists() || unit->getType() != type) continue;
            if (!completedOnly || unit->isCompleted()) ++result;
        }
        return result;
    }

    bool canSpend(int cost, int reserve = 0) const {
        return minerals >= cost + reserve;
    }
};

struct BuildIntent {
    BWAPI::UnitType type = BWAPI::UnitTypes::None;
    BWAPI::TilePosition near;
    bool valid() const { return type != BWAPI::UnitTypes::None && near.isValid(); }
};

struct Plan {
    int probeReserve = 0;
    bool trainProbes = true;
    bool trainCombat = true;
    BuildIntent build;
    bool scout = false;
    bool attack = false;
};

}  // namespace kestrel
