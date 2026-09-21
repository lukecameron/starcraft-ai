#include "kestrel/OpeningPolicy.h"
#include "kestrel/CombatPolicy.h"

#include <iostream>

int main() {
    const kestrel::OpeningInputs zerg{true, 4, -1, -1, -1, 0};
    const kestrel::OpeningDecision beforePylon = kestrel::decideOpening(zerg, 100);
    if (!beforePylon.suppressProbeBeforeFirstPylon || !beforePylon.requestFirstPylon || beforePylon.probeReserve != 250) return 1;

    const kestrel::OpeningInputs acceptedButNotObserved{true, 4, -1, 120, -1, 0};
    const kestrel::OpeningDecision afterAcceptance = kestrel::decideOpening(acceptedButNotObserved, 100);
    if (afterAcceptance.suppressProbeBeforeFirstPylon || afterAcceptance.requestFirstPylon) return 5;

    const kestrel::OpeningInputs afterPylon{true, 5, 120, 120, -1, 0};
    const kestrel::OpeningDecision beforeSecondGateway = kestrel::decideOpening(afterPylon, 200);
    if (beforeSecondGateway.suppressProbeBeforeFirstPylon || beforeSecondGateway.probeReserve != 250) return 2;

    const kestrel::OpeningInputs beforeSecondZealot{true, 8, 120, 120, 900, 1};
    if (kestrel::decideOpening(beforeSecondZealot, 150).probeReserve != 100) return 3;

    const kestrel::OpeningInputs otherRace{false, 4, -1, -1, -1, 0};
    const kestrel::OpeningDecision neutral = kestrel::decideOpening(otherRace, 100);
    if (neutral.suppressProbeBeforeFirstPylon || neutral.probeReserve != 0) return 4;

    if (kestrel::canRequestKnownZergSecondGateway(true, 900, -1, -1)) return 14;
    if (!kestrel::canRequestKnownZergSecondGateway(true, 900, -1, 1600)) return 15;
    if (kestrel::canRequestKnownZergSecondGateway(true, 900, 1700, 1600)) return 16;
    if (kestrel::canRequestKnownZergSecondGateway(false, 900, -1, 1600)) return 17;

    if (!kestrel::holdLoneZealot(true, 0)) return 6;
    if (!kestrel::holdLoneZealot(true, 1)) return 7;
    if (kestrel::holdLoneZealot(true, 2)) return 8;
    if (kestrel::holdLoneZealot(false, 1)) return 9;
    const BWAPI::Position holdAnchor = kestrel::loneZealotHoldAnchor(BWAPI::TilePosition(10, 20));
    if (holdAnchor != BWAPI::Position(384, 688)) return 10;
    if (kestrel::loneZealotLeashRadius != 96) return 11;
    if (kestrel::loneZealotReturnReleaseRadius != 48) return 12;
    if (kestrel::loneZealotCloseThreatRadius != 160) return 13;
    return 0;
}
