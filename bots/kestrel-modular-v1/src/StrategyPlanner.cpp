#include "kestrel/StrategyPlanner.h"

namespace kestrel {

void StrategyPlanner::reset() {
    opening_ = OpeningInputs{};
    firstGatewayCurrentFrame_ = -1;
    firstGatewayAcceptedFrame_ = -1;
    secondGatewayAcceptedFrame_ = -1;
    secondZealotTrainFrame_ = -1;
    secondZealotCompletedFrame_ = -1;
    telemetry_ = Telemetry{};
}

void StrategyPlanner::observe(const WorldSnapshot& state) {
    opening_.knownZerg = state.knownZerg;
    if (state.count(BWAPI::UnitTypes::Protoss_Pylon) > 0 && opening_.firstPylonCurrentFrame < 0)
        opening_.firstPylonCurrentFrame = state.frame;
    if (state.count(BWAPI::UnitTypes::Protoss_Gateway) > 0 && firstGatewayCurrentFrame_ < 0)
        firstGatewayCurrentFrame_ = state.frame;
    if (state.count(BWAPI::UnitTypes::Protoss_Gateway) >= 2 && opening_.secondGatewayCurrentFrame < 0)
        opening_.secondGatewayCurrentFrame = state.frame;
    if (telemetry_.zergFourProbePylonAccepted && telemetry_.zergFourProbePylonCompletedFrame < 0 &&
        state.count(BWAPI::UnitTypes::Protoss_Pylon, true) > 0) {
        telemetry_.zergFourProbePylonCompletedFrame = state.frame;
    }
    if (state.count(BWAPI::UnitTypes::Protoss_Zealot, true) >= 2 && secondZealotCompletedFrame_ < 0) {
        secondZealotCompletedFrame_ = state.frame;
    }
}

void StrategyPlanner::onBuildAccepted(BWAPI::UnitType type, int frame) {
    if (type == BWAPI::UnitTypes::Protoss_Pylon) {
        if (opening_.firstPylonAcceptedFrame < 0) opening_.firstPylonAcceptedFrame = frame;
        if (opening_.knownZerg && opening_.completedProbes == 4 && !telemetry_.zergFourProbePylonAccepted) {
            telemetry_.zergFourProbePylonAccepted = true;
            telemetry_.zergFourProbePylonAcceptedFrame = frame;
            telemetry_.zergFourProbePylonCompletedProbeCount = opening_.completedProbes;
        }
    } else if (type == BWAPI::UnitTypes::Protoss_Gateway) {
        if (firstGatewayAcceptedFrame_ < 0) firstGatewayAcceptedFrame_ = frame;
        else if (secondGatewayAcceptedFrame_ < 0) secondGatewayAcceptedFrame_ = frame;
    }
}

void StrategyPlanner::onTrainAccepted(BWAPI::UnitType type, int frame) {
    if (type == BWAPI::UnitTypes::Protoss_Zealot) {
        ++opening_.acceptedZealotTrains;
        if (opening_.acceptedZealotTrains == 2) secondZealotTrainFrame_ = frame;
    }
}

Plan StrategyPlanner::decide(const WorldSnapshot& state, bool constructionPending) {
    observe(state);
    opening_.completedProbes = state.count(BWAPI::UnitTypes::Protoss_Probe, true);
    const OpeningDecision opening = decideOpening(opening_, state.minerals);
    Plan result;
    result.probeReserve = opening.probeReserve;
    result.trainProbes = !opening.suppressProbeBeforeFirstPylon;
    result.scout = opening_.completedProbes >= 9;
    result.attack = state.count(BWAPI::UnitTypes::Protoss_Zealot, true) +
                        state.count(BWAPI::UnitTypes::Protoss_Dragoon, true) >= 4;

    const BWAPI::TilePosition home = state.home;
    const int pylons = state.count(BWAPI::UnitTypes::Protoss_Pylon);
    const int completedPylons = state.count(BWAPI::UnitTypes::Protoss_Pylon, true);
    const int gateways = state.count(BWAPI::UnitTypes::Protoss_Gateway);
    if (!constructionPending && opening.requestFirstPylon && pylons == completedPylons && pylons == 0) {
        result.build = {BWAPI::UnitTypes::Protoss_Pylon, home};
    } else if (!constructionPending && state.supplyTotal - state.supplyUsed <= 4 && pylons < 5 && pylons == completedPylons && state.canSpend(100)) {
        result.build = {BWAPI::UnitTypes::Protoss_Pylon, home};
    } else if (!constructionPending && state.knownZerg && opening_.firstPylonAcceptedFrame >= 0 &&
               firstGatewayCurrentFrame_ < 0 && state.canSpend(150)) {
        result.build = {BWAPI::UnitTypes::Protoss_Gateway, home};
    } else if (!constructionPending && !state.knownZerg && state.supplyUsed >= 18 && gateways < 1 && state.canSpend(150)) {
        result.build = {BWAPI::UnitTypes::Protoss_Gateway, home};
    } else if (!constructionPending &&
               canRequestKnownZergSecondGateway(
                   state.knownZerg, firstGatewayCurrentFrame_,
                   opening_.secondGatewayCurrentFrame, secondZealotCompletedFrame_) &&
               state.canSpend(150)) {
        result.build = {BWAPI::UnitTypes::Protoss_Gateway, home};
    } else if (!constructionPending && !state.knownZerg && state.supplyUsed >= 26 && gateways < 2 && state.canSpend(150)) {
        result.build = {BWAPI::UnitTypes::Protoss_Gateway, home};
    } else if (!constructionPending && gateways > 0 && state.count(BWAPI::UnitTypes::Protoss_Assimilator) < 1 &&
               (!state.knownZerg || opening_.acceptedZealotTrains >= 2) && state.canSpend(100)) {
        result.build = {BWAPI::UnitTypes::Protoss_Assimilator, home};
    } else if (!constructionPending && state.count(BWAPI::UnitTypes::Protoss_Assimilator, true) > 0 &&
               state.count(BWAPI::UnitTypes::Protoss_Cybernetics_Core) < 1 &&
               (!state.knownZerg || opening_.acceptedZealotTrains >= 2) && state.canSpend(200)) {
        result.build = {BWAPI::UnitTypes::Protoss_Cybernetics_Core, home};
    } else if (!constructionPending && state.count(BWAPI::UnitTypes::Protoss_Cybernetics_Core, true) > 0 &&
               gateways < 4 && state.canSpend(250)) {
        result.build = {BWAPI::UnitTypes::Protoss_Gateway, home};
    }
    return result;
}

}  // namespace kestrel
