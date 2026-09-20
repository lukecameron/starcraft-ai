#include <BWAPI.h>

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdio>
#include <ctime>
#include <fstream>
#include <limits>
#include <unordered_map>
#include <vector>

#ifdef _WIN32
#define KESTREL_EXPORT __declspec(dllexport)
#else
#define KESTREL_EXPORT __attribute__((visibility("default")))
#endif

namespace {

class Kestrel final : public BWAPI::AIModule {
    using Clock = std::chrono::steady_clock;

    int scoutId_ = -1;
    int builderId_ = -1;
    int commands_ = 0;
    int rejected_ = 0;
    enum CommandCategory { BuildCommand, TrainCommand, GatherCommand, AttackCommand, CommandCategoryCount };
    std::array<int, CommandCategoryCount> attemptedByCategory_{{0, 0, 0, 0}};
    std::array<int, CommandCategoryCount> rejectedByCategory_{{0, 0, 0, 0}};
    std::array<int, BWAPI::Errors::Enum::MAX> errors_{};
    int latency_ = -1;
    int nextStartIndex_ = 0;
    BWAPI::UnitType pendingBuildType_ = BWAPI::UnitTypes::None;
    int pendingBuildBaseline_ = 0;
    int pendingBuildFrame_ = -10000;
    int pendingBuildFirstFrame_ = -10000;
    int maxProbes_ = 0;
    int maxPylons_ = 0;
    int maxGateways_ = 0;
    int maxZealots_ = 0;
    int maxDragoons_ = 0;
    int gasWorkerGuardEvents_ = 0;
    int gasWorkerBuildAttempts_ = 0;
    int buildUnitBusyRejections_ = 0;
    struct AttackRequest {
        int targetId;
        int frame;
    };
    std::unordered_map<int, AttackRequest> attackRequests_;
    double callbackCpuSeconds_ = 0.0;
    std::vector<double> callbackMs_;

    static std::vector<BWAPI::Unit> sorted(const BWAPI::Unitset& units) {
        std::vector<BWAPI::Unit> result(units.begin(), units.end());
        std::sort(result.begin(), result.end(), [](BWAPI::Unit a, BWAPI::Unit b) {
            return a->getID() < b->getID();
        });
        return result;
    }

    bool issue(bool accepted, CommandCategory category) {
        ++commands_;
        ++attemptedByCategory_[category];
        if (!accepted) {
            ++rejected_;
            ++rejectedByCategory_[category];
            const int error = BWAPI::Broodwar->getLastError().getID();
            if (error >= 0 && error < BWAPI::Errors::Enum::MAX) ++errors_[static_cast<size_t>(error)];
            if (category == BuildCommand && error == BWAPI::Errors::Enum::Unit_Busy) ++buildUnitBusyRejections_;
        }
        return accepted;
    }

    void writeResult(bool ended, bool won = false) const {
        std::vector<double> samples = callbackMs_;
        std::sort(samples.begin(), samples.end());
        const double p99 = samples.empty() ? 0.0 : samples[(samples.size() - 1) * 99 / 100];
        const double maximum = samples.empty() ? 0.0 : samples.back();
        auto& game = *BWAPI::BroodwarPtr;
        std::ofstream out("bwapi-data/write/diagnostic.json.tmp", std::ios::trunc);
        out << "{\"schema_version\":1,\"bot\":\"Kestrel\""
            << ",\"frame_count\":" << game.getFrameCount()
            << ",\"ended\":" << (ended ? "true" : "false")
            << ",\"winner\":" << (ended ? (won ? "true" : "false") : "null")
            << ",\"latency_frames\":" << latency_
            << ",\"command_count\":" << commands_
            << ",\"rejected_commands\":" << rejected_
            << ",\"command_categories\":{\"build\":[" << attemptedByCategory_[BuildCommand] << ',' << rejectedByCategory_[BuildCommand]
            << "],\"train\":[" << attemptedByCategory_[TrainCommand] << ',' << rejectedByCategory_[TrainCommand]
            << "],\"gather\":[" << attemptedByCategory_[GatherCommand] << ',' << rejectedByCategory_[GatherCommand]
            << "],\"attack\":[" << attemptedByCategory_[AttackCommand] << ',' << rejectedByCategory_[AttackCommand] << "]}"
            << ",\"command_error_counts\":{"
            << "\"unit_busy\":" << errors_[BWAPI::Errors::Enum::Unit_Busy]
            << ",\"incompatible_state\":" << errors_[BWAPI::Errors::Enum::Incompatible_State]
            << ",\"insufficient_minerals\":" << errors_[BWAPI::Errors::Enum::Insufficient_Minerals]
            << ",\"insufficient_gas\":" << errors_[BWAPI::Errors::Enum::Insufficient_Gas]
            << ",\"insufficient_supply\":" << errors_[BWAPI::Errors::Enum::Insufficient_Supply]
            << ",\"unbuildable_location\":" << errors_[BWAPI::Errors::Enum::Unbuildable_Location]
            << ",\"unreachable_location\":" << errors_[BWAPI::Errors::Enum::Unreachable_Location]
            << ",\"unable_to_hit\":" << errors_[BWAPI::Errors::Enum::Unable_To_Hit]
            << ",\"invalid_parameter\":" << errors_[BWAPI::Errors::Enum::Invalid_Parameter]
            << ",\"unknown\":" << errors_[BWAPI::Errors::Enum::Unknown] << "}"
            << ",\"callback_count\":" << callbackMs_.size()
            << ",\"callback_cpu_seconds\":" << callbackCpuSeconds_
            << ",\"callback_wall_p99_ms\":" << p99
            << ",\"callback_wall_max_ms\":" << maximum
            << ",\"max_probes\":" << maxProbes_
            << ",\"max_pylons\":" << maxPylons_
            << ",\"max_gateways\":" << maxGateways_
            << ",\"max_zealots\":" << maxZealots_
            << ",\"max_dragoons\":" << maxDragoons_
            << ",\"gas_worker_guard_events\":" << gasWorkerGuardEvents_
            << ",\"gas_worker_build_attempts\":" << gasWorkerBuildAttempts_
            << ",\"build_unit_busy_rejections\":" << buildUnitBusyRejections_
            << "}\n";
        out.close();
        if (out) {
            std::remove("bwapi-data/write/diagnostic.json");
            std::rename("bwapi-data/write/diagnostic.json.tmp", "bwapi-data/write/diagnostic.json");
        }
    }

    BWAPI::Unit unitById(int id) const {
        if (id < 0) return nullptr;
        for (auto unit : BWAPI::Broodwar->self()->getUnits()) {
            if (unit->getID() == id && unit->exists()) return unit;
        }
        return nullptr;
    }

    void recordGasWorkerGuard(BWAPI::Unit worker, const char* context) {
        ++gasWorkerGuardEvents_;
        std::ofstream out("bwapi-data/write/gas-worker-guard.jsonl", std::ios::app);
        out << "{\"frame\":" << BWAPI::Broodwar->getFrameCount()
            << ",\"worker_id\":" << worker->getID()
            << ",\"order_id\":" << worker->getOrder().getID()
            << ",\"context\":\"" << context << "\"}\n";
    }

    BWAPI::Unit availableProbe(bool allowScout = false) {
        for (auto unit : sorted(BWAPI::Broodwar->self()->getUnits())) {
            if (!unit->exists() || !unit->isCompleted() || unit->getType() != BWAPI::UnitTypes::Protoss_Probe) continue;
            if (!allowScout && unit->getID() == scoutId_) continue;
            if (unit->isGatheringGas()) {
                recordGasWorkerGuard(unit, "available_probe");
                continue;
            }
            if (!unit->isConstructing()) return unit;
        }
        return nullptr;
    }

    int count(BWAPI::UnitType type, bool completedOnly = false) const {
        return completedOnly ? BWAPI::Broodwar->self()->completedUnitCount(type)
                             : BWAPI::Broodwar->self()->allUnitCount(type);
    }

    bool constructionPending() {
        if (pendingBuildType_ == BWAPI::UnitTypes::None) return false;
        if (count(pendingBuildType_) > pendingBuildBaseline_) {
            pendingBuildType_ = BWAPI::UnitTypes::None;
            builderId_ = -1;
            return false;
        }
        const int frame = BWAPI::Broodwar->getFrameCount();
        if (frame - pendingBuildFrame_ < 240) return true;
        BWAPI::Unit builder = unitById(builderId_);
        if (builder && frame - pendingBuildFirstFrame_ < 480 &&
            (builder->isConstructing() || builder->getOrder() == BWAPI::Orders::PlaceBuilding)) {
            pendingBuildFrame_ = frame;
            return true;
        }
        return false;
    }

    bool build(BWAPI::UnitType type, BWAPI::TilePosition near) {
        const int frame = BWAPI::Broodwar->getFrameCount();
        if (constructionPending()) return false;
        BWAPI::Unit worker = unitById(builderId_);
        if (worker && worker->isGatheringGas()) {
            recordGasWorkerGuard(worker, "reuse_builder");
            worker = nullptr;
        }
        if (!worker || worker->isConstructing() || worker->getID() == scoutId_) worker = availableProbe();
        if (!worker) return false;
        const BWAPI::TilePosition tile = BWAPI::Broodwar->getBuildLocation(type, near, 32, false);
        if (!tile.isValid()) return false;
        builderId_ = worker->getID();
        if (worker->isGatheringGas()) ++gasWorkerBuildAttempts_;
        const bool accepted = issue(worker->build(type, tile), BuildCommand);
        if (accepted) {
            pendingBuildType_ = type;
            pendingBuildBaseline_ = count(type);
            pendingBuildFrame_ = frame;
            pendingBuildFirstFrame_ = frame;
        }
        return accepted;
    }

    bool buildAssimilator() {
        const int frame = BWAPI::Broodwar->getFrameCount();
        if (constructionPending()) return false;
        BWAPI::Unit worker = availableProbe();
        if (!worker) return false;
        BWAPI::Unit best = nullptr;
        int bestDistance = std::numeric_limits<int>::max();
        const BWAPI::Position home(BWAPI::Broodwar->self()->getStartLocation());
        for (auto geyser : BWAPI::Broodwar->getGeysers()) {
            if (!geyser->exists()) continue;
            const int distance = geyser->getDistance(home);
            if (distance < bestDistance) { bestDistance = distance; best = geyser; }
        }
        if (!best || bestDistance > 400) return false;
        builderId_ = worker->getID();
        if (worker->isGatheringGas()) ++gasWorkerBuildAttempts_;
        const bool accepted = issue(worker->build(BWAPI::UnitTypes::Protoss_Assimilator, best->getTilePosition()), BuildCommand);
        if (accepted) {
            pendingBuildType_ = BWAPI::UnitTypes::Protoss_Assimilator;
            pendingBuildBaseline_ = count(pendingBuildType_);
            pendingBuildFrame_ = frame;
            pendingBuildFirstFrame_ = frame;
        }
        return accepted;
    }

    void trainUnits() {
        const int probes = count(BWAPI::UnitTypes::Protoss_Probe);
        for (auto unit : sorted(BWAPI::Broodwar->self()->getUnits())) {
            if (!unit->exists() || !unit->isCompleted() || unit->isTraining()) continue;
            const BWAPI::UnitType type = unit->getType();
            if (type == BWAPI::UnitTypes::Protoss_Nexus && probes < 28 && BWAPI::Broodwar->self()->minerals() >= 50 &&
                unit->canTrain(BWAPI::UnitTypes::Protoss_Probe)) {
                issue(unit->train(BWAPI::UnitTypes::Protoss_Probe), TrainCommand);
            } else if (type == BWAPI::UnitTypes::Protoss_Gateway) {
                if (count(BWAPI::UnitTypes::Protoss_Cybernetics_Core, true) > 0 &&
                    BWAPI::Broodwar->self()->minerals() >= 125 && BWAPI::Broodwar->self()->gas() >= 50 &&
                    unit->canTrain(BWAPI::UnitTypes::Protoss_Dragoon)) {
                    issue(unit->train(BWAPI::UnitTypes::Protoss_Dragoon), TrainCommand);
                } else if (BWAPI::Broodwar->self()->minerals() >= 100 && unit->canTrain(BWAPI::UnitTypes::Protoss_Zealot)) {
                    issue(unit->train(BWAPI::UnitTypes::Protoss_Zealot), TrainCommand);
                }
            }
        }
    }

    void constructOpening() {
        auto self = BWAPI::Broodwar->self();
        const BWAPI::TilePosition home = self->getStartLocation();
        const int supplyUsed = self->supplyUsed();
        const int supplyTotal = self->supplyTotal();
        if (constructionPending()) return;
        const int pylons = count(BWAPI::UnitTypes::Protoss_Pylon);
        const int completedPylons = count(BWAPI::UnitTypes::Protoss_Pylon, true);
        if (supplyTotal - supplyUsed <= 4 && pylons < 5 && pylons == completedPylons && self->minerals() >= 100) {
            if (build(BWAPI::UnitTypes::Protoss_Pylon, home)) return;
        }
        const int gateways = count(BWAPI::UnitTypes::Protoss_Gateway);
        if (supplyUsed >= 18 && gateways < 1 && self->minerals() >= 150) {
            if (build(BWAPI::UnitTypes::Protoss_Gateway, home)) return;
        }
        if (supplyUsed >= 26 && gateways < 2 && self->minerals() >= 150) {
            if (build(BWAPI::UnitTypes::Protoss_Gateway, home)) return;
        }
        if (gateways > 0 && count(BWAPI::UnitTypes::Protoss_Assimilator) < 1 && self->minerals() >= 100) {
            if (buildAssimilator()) return;
        }
        if (count(BWAPI::UnitTypes::Protoss_Assimilator, true) > 0 &&
            count(BWAPI::UnitTypes::Protoss_Cybernetics_Core) < 1 && self->minerals() >= 200) {
            if (build(BWAPI::UnitTypes::Protoss_Cybernetics_Core, home)) return;
        }
        if (count(BWAPI::UnitTypes::Protoss_Cybernetics_Core, true) > 0 && gateways < 4 && self->minerals() >= 250) {
            build(BWAPI::UnitTypes::Protoss_Gateway, home);
        }
    }

    void assignEconomy() {
        auto self = BWAPI::Broodwar->self();
        int gasWorkers = 0;
        for (auto worker : self->getUnits()) {
            if (worker->exists() && worker->getType() == BWAPI::UnitTypes::Protoss_Probe && worker->isGatheringGas()) ++gasWorkers;
        }
        for (auto worker : sorted(self->getUnits())) {
            if (!worker->exists() || !worker->isCompleted() || worker->getType() != BWAPI::UnitTypes::Protoss_Probe) continue;
            if (worker->getID() == scoutId_ || worker->getID() == builderId_ || worker->isConstructing() || worker->isGatheringMinerals() || worker->isGatheringGas()) continue;
            BWAPI::Unit target = nullptr;
            int best = std::numeric_limits<int>::max();
            const bool wantGas = count(BWAPI::UnitTypes::Protoss_Assimilator, true) > 0 && self->gas() < 250 && gasWorkers < 3;
            const BWAPI::Unitset& resources = wantGas ? self->getUnits() : BWAPI::Broodwar->getMinerals();
            for (auto resource : resources) {
                if (!resource->exists()) continue;
                if (wantGas && resource->getType() != BWAPI::UnitTypes::Protoss_Assimilator) continue;
                const int distance = worker->getDistance(resource);
                if (distance < best) { best = distance; target = resource; }
            }
            if (target && issue(worker->gather(target), GatherCommand) && wantGas) ++gasWorkers;
        }
    }

    BWAPI::Unit visibleEnemyTarget(BWAPI::Unit from) const {
        const auto previous = attackRequests_.find(from->getID());
        if (previous != attackRequests_.end()) {
            BWAPI::Unit retained = BWAPI::Broodwar->getUnit(previous->second.targetId);
            if (retained && retained->exists() && retained->isVisible() && retained->isDetected() && !retained->isFlying() &&
                BWAPI::Broodwar->self()->isEnemy(retained->getPlayer())) {
                return retained;
            }
        }
        BWAPI::Unit target = nullptr;
        int best = std::numeric_limits<int>::max();
        for (auto enemy : BWAPI::Broodwar->getAllUnits()) {
            if (!enemy->exists() || !enemy->isVisible() || !BWAPI::Broodwar->self()->isEnemy(enemy->getPlayer())) continue;
            if (enemy->isFlying() || !enemy->isDetected()) continue;
            const int distance = from->getDistance(enemy);
            if (distance < best) { best = distance; target = enemy; }
        }
        return target;
    }

    BWAPI::Position unexploredStart(BWAPI::Unit from) {
        std::vector<BWAPI::TilePosition> starts(BWAPI::Broodwar->getStartLocations().begin(), BWAPI::Broodwar->getStartLocations().end());
        std::sort(starts.begin(), starts.end(), [](BWAPI::TilePosition a, BWAPI::TilePosition b) {
            if (a.x != b.x) return a.x < b.x;
            return a.y < b.y;
        });
        if (starts.empty()) return BWAPI::Positions::None;
        for (size_t offset = 0; offset < starts.size(); ++offset) {
            const size_t index = (static_cast<size_t>(nextStartIndex_) + offset) % starts.size();
            const auto tile = starts[index];
            if (tile == BWAPI::Broodwar->self()->getStartLocation() || BWAPI::Broodwar->isExplored(tile)) continue;
            nextStartIndex_ = static_cast<int>((index + 1) % starts.size());
            return BWAPI::Position(tile.x * 32 + 64, tile.y * 32 + 48);
        }
        BWAPI::Player enemy = BWAPI::Broodwar->enemy();
        if (enemy && enemy->getStartLocation().isValid() && BWAPI::Broodwar->isExplored(enemy->getStartLocation())) {
            return BWAPI::Position(enemy->getStartLocation());
        }
        (void)from;
        return BWAPI::Positions::None;
    }

    void scoutAndFight() {
        const int army = count(BWAPI::UnitTypes::Protoss_Zealot, true) + count(BWAPI::UnitTypes::Protoss_Dragoon, true);
        if (scoutId_ < 0 && count(BWAPI::UnitTypes::Protoss_Probe) >= 9) {
            for (auto probe : sorted(BWAPI::Broodwar->self()->getUnits())) {
                if (probe->exists() && probe->isCompleted() && probe->getType() == BWAPI::UnitTypes::Protoss_Probe &&
                    probe->getID() != builderId_ && !probe->isConstructing()) {
                    scoutId_ = probe->getID();
                    break;
                }
            }
        }
        for (auto unit : sorted(BWAPI::Broodwar->self()->getUnits())) {
            if (!unit->exists() || !unit->isCompleted()) continue;
            const bool combat = unit->getType() == BWAPI::UnitTypes::Protoss_Zealot || unit->getType() == BWAPI::UnitTypes::Protoss_Dragoon;
            const bool scout = unit->getID() == scoutId_;
            if (!combat && !scout) continue;
            if (unit->isAttacking() && unit->getOrderTarget()) continue;
            BWAPI::Unit enemy = visibleEnemyTarget(unit);
            if (enemy) {
                const int frame = BWAPI::Broodwar->getFrameCount();
                const auto previous = attackRequests_.find(unit->getID());
                const bool targetChanged = previous == attackRequests_.end() || previous->second.targetId != enemy->getID();
                const int retryFrames = 96;
                if (targetChanged || frame - previous->second.frame >= retryFrames) {
                    issue(unit->attack(enemy), AttackCommand);
                    attackRequests_[unit->getID()] = {enemy->getID(), frame};
                }
                continue;
            }
            attackRequests_.erase(unit->getID());
            BWAPI::Position target = BWAPI::Positions::None;
            if (scout || army >= 4) target = unexploredStart(unit);
            if (target.isValid() && unit->getTargetPosition() != target) issue(unit->attack(target), AttackCommand);
        }
    }

    void play() {
        auto& game = *BWAPI::BroodwarPtr;
        if (!game.self() || game.isReplay()) return;
        maxProbes_ = std::max(maxProbes_, count(BWAPI::UnitTypes::Protoss_Probe));
        maxPylons_ = std::max(maxPylons_, count(BWAPI::UnitTypes::Protoss_Pylon));
        maxGateways_ = std::max(maxGateways_, count(BWAPI::UnitTypes::Protoss_Gateway));
        maxZealots_ = std::max(maxZealots_, count(BWAPI::UnitTypes::Protoss_Zealot));
        maxDragoons_ = std::max(maxDragoons_, count(BWAPI::UnitTypes::Protoss_Dragoon));
        const int frame = game.getFrameCount();
        const int cadence = std::max(6, game.getLatencyFrames());
        if (frame % cadence != 0) return;
        assignEconomy();
        trainUnits();
        constructOpening();
        scoutAndFight();
    }

public:
    void onStart() override {
        latency_ = BWAPI::Broodwar->getLatencyFrames();
        std::remove("bwapi-data/write/gas-worker-guard.jsonl");
        writeResult(false);
    }

    void onFrame() override {
        const auto wallStart = Clock::now();
        const std::clock_t cpuStart = std::clock();
        play();
        callbackCpuSeconds_ += static_cast<double>(std::clock() - cpuStart) / CLOCKS_PER_SEC;
        callbackMs_.push_back(std::chrono::duration<double, std::milli>(Clock::now() - wallStart).count());
        if (BWAPI::Broodwar->getFrameCount() % 240 == 0) writeResult(false);
    }

    void onEnd(bool won) override { writeResult(true, won); }
};

} // namespace

extern "C" KESTREL_EXPORT void gameInit(BWAPI::Game* game) { BWAPI::BroodwarPtr = game; }
extern "C" KESTREL_EXPORT BWAPI::AIModule* newAIModule() { return new Kestrel(); }
