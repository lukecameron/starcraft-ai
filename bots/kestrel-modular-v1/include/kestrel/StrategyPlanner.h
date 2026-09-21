#pragma once

#include "kestrel/OpeningPolicy.h"
#include "kestrel/Types.h"

#include <vector>

namespace kestrel {

class StrategyPlanner {
public:
    struct Telemetry {
        bool zergFourProbePylonAccepted = false;
        int zergFourProbePylonAcceptedFrame = -1;
        int zergFourProbePylonCompletedProbeCount = -1;
        int zergFourProbePylonCompletedFrame = -1;
    };

    void reset();
    Plan decide(const WorldSnapshot& state, bool constructionPending);
    void onBuildAccepted(BWAPI::UnitType type, int frame);
    void onTrainAccepted(BWAPI::UnitType type, int frame);
    void observe(const WorldSnapshot& state);

    const OpeningInputs& opening() const { return opening_; }
    int secondZealotCompletedFrame() const { return secondZealotCompletedFrame_; }
    int firstPylonAcceptedFrame() const { return opening_.firstPylonAcceptedFrame; }
    int firstPylonCurrentFrame() const { return opening_.firstPylonCurrentFrame; }
    int firstGatewayAcceptedFrame() const { return firstGatewayAcceptedFrame_; }
    int firstGatewayCurrentFrame() const { return firstGatewayCurrentFrame_; }
    int secondGatewayAcceptedFrame() const { return secondGatewayAcceptedFrame_; }
    int secondGatewayCurrentFrame() const { return opening_.secondGatewayCurrentFrame; }
    int secondZealotTrainFrame() const { return secondZealotTrainFrame_; }
    const Telemetry& telemetry() const { return telemetry_; }

private:
    OpeningInputs opening_;
    int firstGatewayCurrentFrame_ = -1;
    int firstGatewayAcceptedFrame_ = -1;
    int secondGatewayAcceptedFrame_ = -1;
    int secondZealotTrainFrame_ = -1;
    int secondZealotCompletedFrame_ = -1;
    Telemetry telemetry_;
};

}  // namespace kestrel
