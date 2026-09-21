#pragma once

#include <BWAPI.h>

namespace kestrel {

constexpr int loneZealotCloseThreatRadius = 256;

inline bool holdLoneZealot(bool knownZerg, int completedZealots) {
    return knownZerg && completedZealots < 2;
}

// Keep this anchor local to the lone-hold retreat. Other squad destinations
// continue to use their existing public-state coordinates.
inline BWAPI::Position loneZealotHoldAnchor(BWAPI::TilePosition start) {
    return BWAPI::Position(start.x * 32 + 64, start.y * 32 + 48);
}

}  // namespace kestrel
