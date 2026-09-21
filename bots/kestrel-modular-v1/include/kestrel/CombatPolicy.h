#pragma once

namespace kestrel {

inline bool holdLoneZealot(bool knownZerg, int completedZealots) {
    return knownZerg && completedZealots < 2;
}

}  // namespace kestrel
