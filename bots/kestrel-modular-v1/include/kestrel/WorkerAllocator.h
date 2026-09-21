#pragma once

#include "kestrel/CommandArbiter.h"
#include "kestrel/Types.h"

namespace kestrel {

class WorkerAllocator {
public:
    BWAPI::Unit findBuilder(const WorldSnapshot& state, int scoutId, int builderId) const;
    void tick(const WorldSnapshot& state, int scoutId, int builderId, CommandArbiter& commands);
};

}  // namespace kestrel
