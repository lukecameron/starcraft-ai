#pragma once

#include "kestrel/Types.h"

#include <array>
#include <unordered_map>

namespace kestrel {

class CommandArbiter {
public:
    struct Stats {
        int attempted = 0;
        int rejected = 0;
        std::array<int, 5> attemptedByKind{{0, 0, 0, 0, 0}};
        std::array<int, 5> rejectedByKind{{0, 0, 0, 0, 0}};
        std::array<int, BWAPI::Errors::Enum::MAX> errors{};
    };

    void reset();
    bool issue(bool accepted, CommandKind kind);
    // `issued` distinguishes a real BWAPI attack call from local coalescing.
    // The default keeps existing callers source-compatible.
    bool attack(BWAPI::Unit unit, BWAPI::Unit target, int frame, bool* issued = nullptr);
    bool attackMove(BWAPI::Unit unit, BWAPI::Position target, int frame);
    bool move(BWAPI::Unit unit, BWAPI::Position target, int frame);
    const Stats& stats() const { return stats_; }

private:
    struct AttackRequest { int targetId = -1; BWAPI::Position target; int frame = -10000; CommandKind kind = CommandKind::Attack; };
    static size_t index(CommandKind kind) { return static_cast<size_t>(kind); }
    Stats stats_;
    std::unordered_map<int, AttackRequest> attacks_;
};

}  // namespace kestrel
