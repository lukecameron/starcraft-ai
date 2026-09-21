#include "kestrel/WorldState.h"

#include <algorithm>

#include <algorithm>

namespace kestrel {

void WorldState::observe(BWAPI::Game* game) {
    snapshot_ = WorldSnapshot{};
    if (!game || !game->self()) return;
    snapshot_.frame = game->getFrameCount();
    snapshot_.latencyFrames = std::max(1, game->getLatencyFrames());
    snapshot_.minerals = game->self()->minerals();
    snapshot_.gas = game->self()->gas();
    snapshot_.supplyUsed = game->self()->supplyUsed();
    snapshot_.supplyTotal = game->self()->supplyTotal();
    snapshot_.home = game->self()->getStartLocation();
    const BWAPI::Player enemy = game->enemy();
    snapshot_.knownZerg = enemy && enemy->getRace() == BWAPI::Races::Zerg;

    for (auto unit : game->self()->getUnits()) snapshot_.ownUnits.push_back(unit);
    for (auto unit : game->getAllUnits()) {
        if (!unit || !unit->exists() || !unit->isVisible() || !unit->isDetected()) continue;
        if (game->self()->isEnemy(unit->getPlayer())) snapshot_.visibleEnemies.push_back(unit);
    }
    for (auto unit : game->getMinerals()) snapshot_.mineralsFields.push_back(unit);
    for (auto unit : game->getGeysers()) snapshot_.geysers.push_back(unit);
    for (auto tile : game->getStartLocations()) {
        snapshot_.starts.push_back({tile, game->isExplored(tile)});
    }
    const auto byUnitId = [](BWAPI::Unit left, BWAPI::Unit right) {
        return left->getID() < right->getID();
    };
    std::sort(snapshot_.ownUnits.begin(), snapshot_.ownUnits.end(), byUnitId);
    std::sort(snapshot_.visibleEnemies.begin(), snapshot_.visibleEnemies.end(), byUnitId);
    std::sort(snapshot_.mineralsFields.begin(), snapshot_.mineralsFields.end(), byUnitId);
    std::sort(snapshot_.geysers.begin(), snapshot_.geysers.end(), byUnitId);
    std::sort(snapshot_.starts.begin(), snapshot_.starts.end(), [](const StartLocation& left, const StartLocation& right) {
        if (left.tile.x != right.tile.x) return left.tile.x < right.tile.x;
        return left.tile.y < right.tile.y;
    });
}

}  // namespace kestrel
