#pragma once

#include "kestrel/CommandArbiter.h"
#include "kestrel/Types.h"
#include "kestrel/WorkerAllocator.h"

#include <vector>

namespace kestrel {

class ConstructionController {
public:
    struct Event {
        int typeId = -1;
        int baseline = 0;
        int acceptedFrame = -1;
        int currentFrame = -1;
        int completedFrame = -1;
    };

    void reset();
    void observe(const WorldSnapshot& state);
    bool pending(const WorldSnapshot& state) const;
    bool tick(const WorldSnapshot& state, const BuildIntent& intent, int scoutId,
              int& builderId, CommandArbiter& commands, WorkerAllocator& workers);
    const std::vector<Event>& events() const { return events_; }

private:
    void clear(int& externalBuilderId);
    BWAPI::UnitType pendingType_ = BWAPI::UnitTypes::None;
    int baseline_ = 0;
    int builderId_ = -1;
    int acceptedFrame_ = -1;
    std::vector<Event> events_;
};

}  // namespace kestrel
