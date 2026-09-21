#pragma once

#include "kestrel/CommandArbiter.h"
#include "kestrel/Types.h"

#include <vector>

namespace kestrel {

class ProductionController {
public:
    struct ReserveSample {
        int frame = -1;
        int availableMinerals = 0;
        int reserve = 0;
        int preSecondZealotAcceptance = 0;
    };

    void reset();
    void tick(const WorldSnapshot& state, const Plan& plan, CommandArbiter& commands);
    int acceptedZealotTrains() const { return acceptedZealotTrains_; }
    int secondZealotTrainFrame() const { return secondZealotTrainFrame_; }
    const std::vector<int>& acceptedProbeTrainFrames() const { return acceptedProbeTrainFrames_; }
    const std::vector<ReserveSample>& reserveActive() const { return reserveActive_; }
    const std::vector<ReserveSample>& reserveBlocks() const { return reserveBlocks_; }

private:
    int acceptedZealotTrains_ = 0;
    int secondZealotTrainFrame_ = -1;
    std::vector<int> acceptedProbeTrainFrames_;
    std::vector<ReserveSample> reserveActive_;
    std::vector<ReserveSample> reserveBlocks_;
};

}  // namespace kestrel
