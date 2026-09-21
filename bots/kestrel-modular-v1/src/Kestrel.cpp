#include <BWAPI.h>

#include "kestrel/CommandArbiter.h"
#include "kestrel/ConstructionController.h"
#include "kestrel/ProductionController.h"
#include "kestrel/ScoutingController.h"
#include "kestrel/SquadController.h"
#include "kestrel/StrategyPlanner.h"
#include "kestrel/Telemetry.h"
#include "kestrel/WorldMemory.h"
#include "kestrel/WorldState.h"
#include "kestrel/WorkerAllocator.h"

#include <algorithm>
#include <chrono>

#ifdef _WIN32
#define KESTREL_EXPORT __declspec(dllexport)
#else
#define KESTREL_EXPORT __attribute__((visibility("default")))
#endif

namespace {

class KestrelModular final : public BWAPI::AIModule {
public:
    void onStart() override {
        commands_.reset();
        planner_.reset();
        production_.reset();
        construction_.reset();
        workers_.reset();
        telemetry_.reset();
        squads_.reset();
        scoutId_ = -1;
        builderId_ = -1;
        world_.observe(BWAPI::BroodwarPtr);
        memory_.reset(world_.snapshot());
        telemetry_.write(world_.snapshot(), commands_, planner_, production_, construction_, workers_, squads_, false, false);
    }

    void onFrame() override {
        const auto start = std::chrono::steady_clock::now();
        world_.observe(BWAPI::BroodwarPtr);
        memory_.update(world_.snapshot());
        construction_.observe(world_.snapshot());
        const kestrel::WorldSnapshot& state = world_.snapshot();
        if (!BWAPI::BroodwarPtr || !state.home.isValid() || BWAPI::BroodwarPtr->isReplay()) return;
        const int cadence = std::max(1, state.latencyFrames);
        if (state.frame % cadence != 0) return;

        // The order is part of the architecture contract: observe, remember,
        // plan, allocate, produce, construct, scout, fight, record.
        const kestrel::Plan plan = planner_.decide(state, construction_.pending(state));
        workers_.tick(state, scoutId_, builderId_, commands_);
        production_.tick(state, plan, commands_);
        if (construction_.tick(state, plan.build, scoutId_, builderId_, commands_, workers_)) {
            planner_.onBuildAccepted(plan.build.type, state.frame);
        }
        scouting_.tick(state, memory_, commands_, scoutId_, builderId_, plan.scout);
        if (state.count(BWAPI::UnitTypes::Protoss_Zealot, true) +
            state.count(BWAPI::UnitTypes::Protoss_Dragoon, true) > 0) {
            squads_.tick(state, memory_, commands_, plan.attack);
        }
        while (production_.acceptedZealotTrains() > planner_.opening().acceptedZealotTrains) {
            planner_.onTrainAccepted(BWAPI::UnitTypes::Protoss_Zealot, state.frame);
        }
        const double callbackMs = std::chrono::duration<double, std::milli>(
            std::chrono::steady_clock::now() - start).count();
        telemetry_.sample(state, commands_, planner_, production_, callbackMs);
        if (state.frame % 240 == 0) telemetry_.write(state, commands_, planner_, production_, construction_, workers_, squads_, false, false);
    }

    void onEnd(bool won) override {
        world_.observe(BWAPI::BroodwarPtr);
        planner_.observe(world_.snapshot());
        construction_.observe(world_.snapshot());
        telemetry_.write(world_.snapshot(), commands_, planner_, production_, construction_, workers_, squads_, true, won);
    }

private:
    kestrel::WorldState world_;
    kestrel::WorldMemory memory_;
    kestrel::CommandArbiter commands_;
    kestrel::StrategyPlanner planner_;
    kestrel::WorkerAllocator workers_;
    kestrel::ProductionController production_;
    kestrel::ConstructionController construction_;
    kestrel::ScoutingController scouting_;
    kestrel::SquadController squads_;
    kestrel::Telemetry telemetry_;
    int scoutId_ = -1;
    int builderId_ = -1;
};

}  // namespace

extern "C" KESTREL_EXPORT void gameInit(BWAPI::Game* game) { BWAPI::BroodwarPtr = game; }
extern "C" KESTREL_EXPORT BWAPI::AIModule* newAIModule() { return new KestrelModular(); }
