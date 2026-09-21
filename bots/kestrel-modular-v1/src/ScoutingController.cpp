#include "kestrel/ScoutingController.h"

namespace kestrel {

void ScoutingController::tick(const WorldSnapshot& state, WorldMemory& memory, CommandArbiter& commands,
                              int& scoutId, int builderId, bool enabled) {
    bool scoutPresent = false;
    if (scoutId >= 0) {
        for (auto unit : state.ownUnits) {
            if (unit && unit->exists() && unit->getID() == scoutId) { scoutPresent = true; break; }
        }
        if (!scoutPresent) scoutId = -1;
    }
    if (!enabled) return;
    if (scoutId < 0 && state.count(BWAPI::UnitTypes::Protoss_Probe) >= 9) {
        for (auto probe : state.ownUnits) {
            if (!probe || !probe->exists() || !probe->isCompleted() || probe->getType() != BWAPI::UnitTypes::Protoss_Probe) continue;
            if (probe->getID() != builderId && !probe->isConstructing() && !probe->isGatheringGas()) {
                scoutId = probe->getID();
                break;
            }
        }
    }
    if (scoutId < 0) return;
    for (auto unit : state.ownUnits) {
        if (!unit || !unit->exists() || unit->getID() != scoutId) continue;
        if (unit->isAttacking() && unit->getOrderTarget()) return;
        const BWAPI::Position target = memory.scoutTarget(state);
        if (target.isValid() && unit->getTargetPosition() != target) commands.move(unit, target, state.frame);
        return;
    }
}

}  // namespace kestrel
