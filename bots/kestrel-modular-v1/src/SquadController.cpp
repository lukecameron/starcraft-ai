#include "kestrel/SquadController.h"

namespace kestrel {

void SquadController::tick(const WorldSnapshot& state, WorldMemory& memory, CommandArbiter& commands,
                           bool allowRallyAttack) {
    const int army = state.count(BWAPI::UnitTypes::Protoss_Zealot, true) +
                     state.count(BWAPI::UnitTypes::Protoss_Dragoon, true);
    const BWAPI::Position home(state.home);
    bool homeThreat = false;
    for (auto enemy : state.visibleEnemies) {
        if (enemy && enemy->getDistance(home) <= 400) { homeThreat = true; break; }
    }
    if (homeThreat) holdUntilFrame_ = state.frame + 240;
    const bool holdingHome = homeThreat || state.frame < holdUntilFrame_;
    for (auto unit : state.ownUnits) {
        if (!unit || !unit->exists() || !unit->isCompleted()) continue;
        const BWAPI::UnitType type = unit->getType();
        if (type != BWAPI::UnitTypes::Protoss_Zealot && type != BWAPI::UnitTypes::Protoss_Dragoon) continue;
        if (unit->isAttacking() && unit->getOrderTarget() && !holdingHome) continue;
        if (unit->isAttacking() && unit->getOrderTarget() && holdingHome) {
            const BWAPI::Unit currentTarget = unit->getOrderTarget();
            bool currentTargetIsHomeThreat = false;
            for (auto candidate : state.visibleEnemies) {
                if (candidate && candidate->getID() == currentTarget->getID() &&
                    candidate->getDistance(home) <= 400) {
                    currentTargetIsHomeThreat = true;
                    break;
                }
            }
            if (currentTargetIsHomeThreat) continue;
        }
        BWAPI::Unit enemy = nullptr;
        if (holdingHome) {
            int nearest = 1 << 30;
            for (auto candidate : state.visibleEnemies) {
                if (!candidate || candidate->getDistance(home) > 400) continue;
                const BWAPI::WeaponType weapon = candidate->isFlying() ? type.airWeapon() : type.groundWeapon();
                if (weapon == BWAPI::WeaponTypes::None) continue;
                const int distance = unit->getDistance(candidate);
                if (distance < nearest || (distance == nearest && enemy && candidate->getID() < enemy->getID())) {
                    nearest = distance;
                    enemy = candidate;
                }
            }
        } else if (allowRallyAttack) {
            enemy = memory.nearestVisibleEnemy(unit, state);
        }
        if (enemy) {
            commands.attack(unit, enemy, state.frame);
        } else if (holdingHome) {
            if (unit->getDistance(home) > 192) commands.attackMove(unit, home, state.frame);
        } else if (allowRallyAttack && army >= 4) {
            const BWAPI::Position target = memory.scoutTarget(state);
            if (target.isValid()) commands.attackMove(unit, target, state.frame);
        } else if (unit->getDistance(home) > 192) {
            commands.attackMove(unit, home, state.frame);
        }
    }
}

}  // namespace kestrel
