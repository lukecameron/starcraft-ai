#pragma once

namespace kestrel {

// This is deliberately independent of BWAPI so the opening decisions can be
// tested without a live engine. The caller supplies only public self-state.
struct OpeningInputs {
    bool knownZerg = false;
    int completedProbes = 0;
    int firstPylonCurrentFrame = -1;
    int firstPylonAcceptedFrame = -1;
    int secondGatewayCurrentFrame = -1;
    int acceptedZealotTrains = 0;
};

struct OpeningDecision {
    bool suppressProbeBeforeFirstPylon = false;
    bool requestFirstPylon = false;
    int probeReserve = 0;
};

inline OpeningDecision decideOpening(const OpeningInputs& state, int minerals) {
    OpeningDecision result;
    if (!state.knownZerg) return result;

    // The opening gate ends at command acceptance. A construction becoming
    // visible a cadence later must not extend the Probe freeze.
    result.suppressProbeBeforeFirstPylon =
        state.completedProbes >= 4 && state.firstPylonAcceptedFrame < 0;
    result.requestFirstPylon = result.suppressProbeBeforeFirstPylon &&
        state.firstPylonCurrentFrame < 0 && minerals >= 100;

    if (state.firstPylonCurrentFrame < 0) {
        result.probeReserve = 250;
    } else if (state.secondGatewayCurrentFrame < 0) {
        result.probeReserve = 250;
    } else if (state.acceptedZealotTrains < 2) {
        result.probeReserve = 100;
    }
    return result;
}

}  // namespace kestrel
