#include "kestrel/SquadController.h"

#include "kestrel/CombatPolicy.h"

namespace kestrel {

SquadController::HeldUnitLifecycle& SquadController::lifecycleFor(int unitId, int frame) {
    for (auto& lifecycle : stats_.loneHoldUnitLifecycles) {
        if (lifecycle.unitId == unitId) {
            lifecycle.lastSeenFrame = frame;
            return lifecycle;
        }
    }
    HeldUnitLifecycle lifecycle;
    lifecycle.unitId = unitId;
    lifecycle.firstSeenFrame = frame;
    lifecycle.lastSeenFrame = frame;
    stats_.loneHoldUnitLifecycles.push_back(lifecycle);
    return stats_.loneHoldUnitLifecycles.back();
}

void SquadController::tick(const WorldSnapshot& state, WorldMemory& memory, CommandArbiter& commands,
                           bool allowRallyAttack) {
    const int army = state.count(BWAPI::UnitTypes::Protoss_Zealot, true) +
                     state.count(BWAPI::UnitTypes::Protoss_Dragoon, true);
    const int completedZealots = state.count(BWAPI::UnitTypes::Protoss_Zealot, true);
    const bool loneZealotHold = holdLoneZealot(state.knownZerg, completedZealots);
    if (loneZealotHold) {
        ++stats_.loneHoldActiveSamples;
        loneHoldWasActive_ = true;
    } else if (loneHoldWasActive_ && stats_.loneHoldReleaseFrame < 0 && completedZealots >= 2) {
        stats_.loneHoldReleaseFrame = state.frame;
    }
    const BWAPI::Position home(state.home);
    const BWAPI::Position loneHoldHome = loneZealotHoldAnchor(state.home);
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
        if (loneZealotHold && type == BWAPI::UnitTypes::Protoss_Zealot) {
            HeldUnitLifecycle& lifecycle = lifecycleFor(unit->getID(), state.frame);
            ++stats_.loneHoldSuppressionSamples;
            if (suppressedUnits_.insert(unit->getID()).second)
                stats_.loneHoldUniqueUnits = static_cast<int>(suppressedUnits_.size());

            BWAPI::Unit closeThreat = nullptr;
            int nearestThreat = 1 << 30;
            for (auto candidate : state.visibleEnemies) {
                if (!candidate || !candidate->exists() || !candidate->isVisible() || !candidate->isDetected()) continue;
                if (type.groundWeapon() == BWAPI::WeaponTypes::None ||
                    candidate->isFlying() || candidate->getType().groundWeapon() == BWAPI::WeaponTypes::None) continue;
                if (candidate->getDistance(loneHoldHome) > loneZealotCloseThreatRadius) continue;
                const int distance = unit->getDistance(candidate);
                if (distance < nearestThreat ||
                    (distance == nearestThreat && closeThreat && candidate->getID() < closeThreat->getID())) {
                    nearestThreat = distance;
                    closeThreat = candidate;
                }
            }

            if (closeThreat) {
                ++stats_.loneHoldCloseThreatSamples;
                if (stats_.loneHoldCloseThreatFirstFrame < 0)
                    stats_.loneHoldCloseThreatFirstFrame = state.frame;
                ++lifecycle.closeThreatSamples;
                if (lifecycle.firstCloseThreatFrame < 0)
                    lifecycle.firstCloseThreatFrame = state.frame;
                lifecycle.lastCloseThreatFrame = state.frame;
                bool issued = false;
                const bool accepted = commands.attack(unit, closeThreat, state.frame, &issued);
                if (issued) {
                    ++stats_.loneHoldCloseThreatAttackAttempts;
                    ++lifecycle.closeThreatAttackAttempts;
                    CloseThreatEvent event;
                    event.frame = state.frame;
                    event.heldUnitId = unit->getID();
                    event.targetId = closeThreat->getID();
                    event.heldUnitPosition = unit->getPosition();
                    event.targetPosition = closeThreat->getPosition();
                    event.accepted = accepted;
                    stats_.loneHoldCloseThreatEvents.push_back(event);
                    if (accepted) {
                        ++stats_.loneHoldCloseThreatAttackAccepted;
                        ++lifecycle.closeThreatAttackAccepted;
                        stats_.loneHoldCloseThreatAcceptedFrames.push_back(state.frame);
                        stats_.loneHoldCloseThreatAcceptedHeldUnitIds.push_back(unit->getID());
                        stats_.loneHoldCloseThreatAcceptedTargetIds.push_back(closeThreat->getID());
                        stats_.loneHoldCloseThreatAcceptedHeldPositions.push_back(unit->getPosition());
                        stats_.loneHoldCloseThreatAcceptedTargetPositions.push_back(closeThreat->getPosition());
                    } else {
                        ++stats_.loneHoldCloseThreatAttackRejected;
                        ++lifecycle.closeThreatAttackRejected;
                    }
                }
                continue;
            }

            if (unit->getDistance(home) > 128 && !unit->isMoving()) {
                ++stats_.loneHoldHomeMoveAttempts;
                ++lifecycle.anchorMoveAttempts;
                if (commands.move(unit, loneHoldHome, state.frame)) {
                    ++stats_.loneHoldHomeMoveAccepted;
                    ++lifecycle.anchorMoveAccepted;
                    stats_.loneHoldAcceptedHomeMoveTargets.push_back(loneHoldHome);
                }
            }
            continue;
        }
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
