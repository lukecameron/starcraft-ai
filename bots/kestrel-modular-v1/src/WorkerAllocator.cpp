#include "kestrel/WorkerAllocator.h"

#include <algorithm>
#include <limits>
#include <vector>

namespace kestrel {

bool WorkerAllocator::gather(BWAPI::Unit worker, BWAPI::Unit target, CommandArbiter& commands) {
    if (!worker || !target) return false;
    if (worker->isCarryingMinerals() || worker->isCarryingGas()) {
        ++stats_.cargoDeferrals;
        return false;
    }
    if (!worker->canGather(target)) {
        ++stats_.gatherPreflightSkips;
        return false;
    }
    if (!commands.issue(worker->gather(target), CommandKind::Gather)) return false;
    ++stats_.acceptedGatherCommands;
    return true;
}

BWAPI::Unit WorkerAllocator::findBuilder(const WorldSnapshot& state, int scoutId, int builderId,
                                         BWAPI::UnitType type, BWAPI::TilePosition tile) {
    BWAPI::Unit best = nullptr;
    int bestDistance = std::numeric_limits<int>::max();
    const BWAPI::Position position(tile);
    for (auto worker : state.ownUnits) {
        if (!worker || !worker->exists() || !worker->isCompleted() ||
            worker->getType() != BWAPI::UnitTypes::Protoss_Probe) continue;
        if (worker->getID() == scoutId || worker->getID() == builderId || worker->isConstructing() || worker->isGatheringGas()) continue;
        if (worker->isCarryingMinerals() || worker->isCarryingGas()) {
            ++stats_.builderCargoDeferrals;
            continue;
        }
        if (!worker->canBuild(type, tile)) {
            ++stats_.builderPreflightSkips;
            continue;
        }
        const int distance = worker->getDistance(position);
        if (!best || distance < bestDistance ||
            (distance == bestDistance && worker->getID() < best->getID())) {
            best = worker;
            bestDistance = distance;
        }
    }
    return best;
}

void WorkerAllocator::tick(const WorldSnapshot& state, int scoutId, int builderId, CommandArbiter& commands) {
    std::vector<BWAPI::Unit> workers;
    for (auto worker : state.ownUnits) {
        if (worker && worker->exists() && worker->isCompleted() && worker->getType() == BWAPI::UnitTypes::Protoss_Probe &&
            worker->getID() != scoutId && worker->getID() != builderId && !worker->isConstructing()) workers.push_back(worker);
    }
    std::sort(workers.begin(), workers.end(), [](BWAPI::Unit a, BWAPI::Unit b) { return a->getID() < b->getID(); });

    std::vector<BWAPI::Unit> assimilators;
    for (auto unit : state.ownUnits) {
        if (unit && unit->exists() && unit->isCompleted() && unit->getType() == BWAPI::UnitTypes::Protoss_Assimilator)
            assimilators.push_back(unit);
    }
    std::sort(assimilators.begin(), assimilators.end(), [](BWAPI::Unit a, BWAPI::Unit b) { return a->getID() < b->getID(); });
    const int desiredGas = state.gas < 250 ? std::min(3, static_cast<int>(workers.size())) : 0;
    int keptGas = 0;
    const bool haveGasTarget = !assimilators.empty();
    for (auto worker : workers) {
        if (!worker || !worker->exists() || !worker->isCompleted() || worker->getType() != BWAPI::UnitTypes::Protoss_Probe) continue;
        BWAPI::Unit target = nullptr;
        int best = std::numeric_limits<int>::max();
        const bool retainGas = haveGasTarget && worker->isGatheringGas() && keptGas < desiredGas;
        if (retainGas) {
            ++keptGas;
            continue;
        }
        if (haveGasTarget && keptGas < desiredGas) {
            for (auto assimilator : assimilators) {
                const int distance = worker->getDistance(assimilator);
                if (distance < best) { best = distance; target = assimilator; }
            }
            if (target && gather(worker, target, commands)) {
                ++keptGas;
                continue;
            }
        }
        target = nullptr;
        best = std::numeric_limits<int>::max();
        {
            for (auto mineral : state.mineralsFields) {
                if (!mineral || !mineral->exists()) continue;
                const int distance = worker->getDistance(mineral);
                if (distance < best) { best = distance; target = mineral; }
            }
        }
        if (target && !worker->isGatheringMinerals()) gather(worker, target, commands);
    }
}

}  // namespace kestrel
