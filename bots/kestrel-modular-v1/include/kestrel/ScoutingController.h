#pragma once

#include "kestrel/CommandArbiter.h"
#include "kestrel/WorldMemory.h"

namespace kestrel {

class ScoutingController {
public:
    void tick(const WorldSnapshot& state, WorldMemory& memory, CommandArbiter& commands,
              int& scoutId, int builderId, bool enabled);
};

}  // namespace kestrel
