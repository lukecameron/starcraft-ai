// Original diagnostic fixtures: useful for engine bring-up, never rating anchors.
// Uses only the public BWAPI surface shared by OpenBW and official BWAPI 4.4.0.
#include <BWAPI.h>
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <ctime>
#include <fstream>
#include <limits>
#include <vector>

#ifdef _WIN32
#define BOT_EXPORT __declspec(dllexport)
#else
#define BOT_EXPORT __attribute__((visibility("default")))
#endif

#ifndef DIAGNOSTIC_IDLE
#define DIAGNOSTIC_IDLE 0
#endif

namespace {
class DiagnosticModule final : public BWAPI::AIModule {
    using Clock = std::chrono::steady_clock;
    std::vector<double> callback_ms;
    double callback_cpu_seconds = 0;
    int commands = 0;
    int rejected_commands = 0;
    int first_latency = -1;

    void record(bool ended, bool won = false) const {
        // The bot writes only in the tournament-permitted write directory.
        // The local harness owns archive paths and hashes.
        std::ofstream out("bwapi-data/write/diagnostic.json.tmp");
        auto sorted = callback_ms;
        std::sort(sorted.begin(), sorted.end());
        const double p99 = sorted.empty() ? 0 : sorted[(sorted.size() - 1) * 99 / 100];
        const double maximum = sorted.empty() ? 0 : sorted.back();
        out << "{\"schema_version\":1,\"fixture\":\""
            << (DIAGNOSTIC_IDLE ? "idle" : "worker_rush")
            << "\",\"frame_count\":" << BWAPI::Broodwar->getFrameCount()
            << ",\"ended\":" << (ended ? "true" : "false")
            << ",\"winner\":" << (ended ? (won ? "true" : "false") : "null")
            << ",\"latency_frames\":" << first_latency
            << ",\"command_count\":" << commands
            << ",\"rejected_commands\":" << rejected_commands
            << ",\"callback_count\":" << callback_ms.size()
            << ",\"callback_cpu_seconds\":" << callback_cpu_seconds
            << ",\"callback_wall_p99_ms\":" << p99
            << ",\"callback_wall_max_ms\":" << maximum << "}\n";
        out.close();
        if (out) {
            // Windows rename cannot replace an existing file. The harness keeps
            // its own durable records; this diagnostic progress file is advisory.
            std::remove("bwapi-data/write/diagnostic.json");
            std::rename("bwapi-data/write/diagnostic.json.tmp", "bwapi-data/write/diagnostic.json");
        }
    }

    void play() {
        auto& game = *BWAPI::BroodwarPtr;
        if (DIAGNOSTIC_IDLE || !game.self() || game.isReplay()) return;
        const int frame = game.getFrameCount();
        const int latency = std::max(1, game.getLatencyFrames());
        if (frame % latency != 0) return;

        for (auto unit : game.self()->getUnits()) {
            if (!unit->exists() || !unit->isCompleted() || !unit->getType().isWorker()) continue;
            if (unit->getLastCommandFrame() > frame - latency) continue;
            BWAPI::Unit target = nullptr;
            int best = std::numeric_limits<int>::max();
            for (auto enemy : game.getAllUnits()) {
                if (!enemy->exists() || !enemy->isVisible() || !game.self()->isEnemy(enemy->getPlayer())) continue;
                if (enemy->isFlying() || !enemy->isDetected()) continue;
                const int distance = unit->getDistance(enemy);
                if (distance < best) { best = distance; target = enemy; }
            }
            bool issued = false;
            bool attempted = false;
            if (target) {
                if (unit->getOrderTarget() != target) {
                    attempted = true;
                    issued = unit->attack(target);
                }
            } else {
                // Start locations are public map information. An explored empty
                // location is skipped; no hidden enemy location is queried.
                BWAPI::Position destination = BWAPI::Positions::None;
                for (auto start : game.getStartLocations()) {
                    if (start == game.self()->getStartLocation() || game.isExplored(start)) continue;
                    const BWAPI::Position center(start.x * 32 + 64, start.y * 32 + 48);
                    const int distance = unit->getDistance(center);
                    if (distance < best) { best = distance; destination = center; }
                }
                if (destination.isValid() && unit->getTargetPosition() != destination) {
                    attempted = true;
                    issued = unit->attack(destination);
                }
            }
            if (attempted) { ++commands; if (!issued) ++rejected_commands; }
        }
    }

public:
    void onStart() override {
        first_latency = BWAPI::Broodwar->getLatencyFrames();
        record(false);
    }
    void onFrame() override {
        const auto start = Clock::now();
        const auto cpu_start = std::clock();
        play();
        callback_cpu_seconds += double(std::clock() - cpu_start) / CLOCKS_PER_SEC;
        callback_ms.push_back(std::chrono::duration<double, std::milli>(Clock::now() - start).count());
        if (BWAPI::Broodwar->getFrameCount() % 240 == 0) record(false);
    }
    void onEnd(bool won) override { record(true, won); }
};
}

extern "C" BOT_EXPORT void gameInit(BWAPI::Game* game) { BWAPI::BroodwarPtr = game; }
extern "C" BOT_EXPORT BWAPI::AIModule* newAIModule() { return new DiagnosticModule(); }
