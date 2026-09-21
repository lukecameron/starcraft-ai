#pragma once

#include "kestrel/Types.h"

namespace kestrel {

class WorldState {
public:
    void observe(BWAPI::Game* game);
    const WorldSnapshot& snapshot() const { return snapshot_; }

private:
    WorldSnapshot snapshot_;
};

}  // namespace kestrel
