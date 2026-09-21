#include "kestrel/CommandArbiter.h"

#include <BWAPI.h>

namespace kestrel {

void CommandArbiter::reset() {
    stats_ = Stats{};
    attacks_.clear();
}

bool CommandArbiter::issue(bool accepted, CommandKind kind) {
    ++stats_.attempted;
    ++stats_.attemptedByKind[index(kind)];
    if (accepted) return true;
    ++stats_.rejected;
    ++stats_.rejectedByKind[index(kind)];
    const int error = BWAPI::Broodwar->getLastError().getID();
    if (error >= 0 && error < BWAPI::Errors::Enum::MAX) ++stats_.errors[static_cast<size_t>(error)];
    return false;
}

bool CommandArbiter::attack(BWAPI::Unit unit, BWAPI::Unit target, int frame, bool* issued) {
    if (issued) *issued = false;
    if (!unit || !target) return false;
    const auto previous = attacks_.find(unit->getID());
    if (previous != attacks_.end() && previous->second.kind == CommandKind::Attack &&
        previous->second.targetId == target->getID() &&
        frame - previous->second.frame < 96) return true;
    if (issued) *issued = true;
    const bool accepted = issue(unit->attack(target), CommandKind::Attack);
    if (accepted) attacks_[unit->getID()] = {target->getID(), BWAPI::Positions::None, frame, CommandKind::Attack};
    return accepted;
}

bool CommandArbiter::attackMove(BWAPI::Unit unit, BWAPI::Position target, int frame) {
    if (!unit || !target.isValid()) return false;
    const auto previous = attacks_.find(unit->getID());
    if (previous != attacks_.end() && previous->second.kind == CommandKind::Attack &&
        previous->second.targetId < 0 && previous->second.target == target &&
        frame - previous->second.frame < 96) return true;
    const bool accepted = issue(unit->attack(target), CommandKind::Attack);
    if (accepted) attacks_[unit->getID()] = {-1, target, frame, CommandKind::Attack};
    return accepted;
}

bool CommandArbiter::move(BWAPI::Unit unit, BWAPI::Position target, int frame, bool* issued) {
    if (issued) *issued = false;
    if (!unit || !target.isValid()) return false;
    const auto previous = attacks_.find(unit->getID());
    if (previous != attacks_.end() && previous->second.kind == CommandKind::Scout &&
        previous->second.targetId < 0 && previous->second.target == target &&
        frame - previous->second.frame < 96) return true;
    if (issued) *issued = true;
    const bool accepted = issue(unit->move(target), CommandKind::Scout);
    if (accepted) attacks_[unit->getID()] = {-1, target, frame, CommandKind::Scout};
    return accepted;
}

}  // namespace kestrel
