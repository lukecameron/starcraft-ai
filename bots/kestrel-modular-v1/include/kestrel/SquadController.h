#pragma once

#include "kestrel/CommandArbiter.h"
#include "kestrel/WorldMemory.h"

namespace kestrel {

class SquadController {
public:
    void reset() { holdUntilFrame_ = -1; }
    void tick(const WorldSnapshot& state, WorldMemory& memory, CommandArbiter& commands,
              bool allowRallyAttack);

private:
    int holdUntilFrame_ = -1;
};

}  // namespace kestrel
