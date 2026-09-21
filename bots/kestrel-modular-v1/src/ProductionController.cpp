#include "kestrel/ProductionController.h"

#include <algorithm>

namespace kestrel {

void ProductionController::reset() {
    acceptedZealotTrains_ = 0;
    secondZealotTrainFrame_ = -1;
    acceptedProbeTrainFrames_.clear();
    reserveActive_.clear();
    reserveBlocks_.clear();
}

void ProductionController::tick(const WorldSnapshot& state, const Plan& plan, CommandArbiter& commands) {
    std::vector<BWAPI::Unit> gateways;
    std::vector<BWAPI::Unit> nexuses;
    for (auto unit : state.ownUnits) {
        if (!unit || !unit->exists() || !unit->isCompleted() || unit->isTraining()) continue;
        if (unit->getType() == BWAPI::UnitTypes::Protoss_Gateway) gateways.push_back(unit);
        if (unit->getType() == BWAPI::UnitTypes::Protoss_Nexus) nexuses.push_back(unit);
    }
    const auto byId = [](BWAPI::Unit left, BWAPI::Unit right) { return left->getID() < right->getID(); };
    std::sort(gateways.begin(), gateways.end(), byId);
    std::sort(nexuses.begin(), nexuses.end(), byId);

    // Reserve the selected construction before issuing production commands.
    // BWAPI updates resources asynchronously, so every accepted command also
    // debits this callback-local ledger.
    const int constructionReserve = plan.build.valid() ? plan.build.type.mineralPrice() : 0;
    int availableMinerals = std::max(0, state.minerals - constructionReserve);
    int availableGas = state.gas;

    if (plan.trainCombat) {
        for (auto gateway : gateways) {
            const bool canDragoon = state.count(BWAPI::UnitTypes::Protoss_Cybernetics_Core, true) > 0 &&
                availableMinerals >= 125 && availableGas >= 50 &&
                gateway->canTrain(BWAPI::UnitTypes::Protoss_Dragoon);
            if (canDragoon) {
                if (commands.issue(gateway->train(BWAPI::UnitTypes::Protoss_Dragoon), CommandKind::Train)) {
                    availableMinerals -= 125;
                    availableGas -= 50;
                }
            } else if (availableMinerals >= 100 && gateway->canTrain(BWAPI::UnitTypes::Protoss_Zealot)) {
                if (commands.issue(gateway->train(BWAPI::UnitTypes::Protoss_Zealot), CommandKind::Train)) {
                    availableMinerals -= 100;
                    ++acceptedZealotTrains_;
                    if (acceptedZealotTrains_ == 2) secondZealotTrainFrame_ = state.frame;
                }
            }
        }
    }

    int predictedProbes = state.count(BWAPI::UnitTypes::Protoss_Probe);
    for (auto nexus : nexuses) {
        if (!plan.trainProbes || predictedProbes >= 28 ||
            !nexus->canTrain(BWAPI::UnitTypes::Protoss_Probe)) continue;
        int effectiveReserve = plan.probeReserve;
        if (effectiveReserve == 100 && acceptedZealotTrains_ >= 2) effectiveReserve = 0;
        if (effectiveReserve > 0) {
            const ReserveSample sample{state.frame, availableMinerals, effectiveReserve,
                                       acceptedZealotTrains_ < 2 ? 1 : 0};
            reserveActive_.push_back(sample);
            if (availableMinerals >= 50 && availableMinerals < 50 + effectiveReserve)
                reserveBlocks_.push_back(sample);
        }
        if (availableMinerals < 50 + effectiveReserve) continue;
        if (commands.issue(nexus->train(BWAPI::UnitTypes::Protoss_Probe), CommandKind::Train)) {
            availableMinerals -= 50;
            ++predictedProbes;
            acceptedProbeTrainFrames_.push_back(state.frame);
        }
    }
}

}  // namespace kestrel
