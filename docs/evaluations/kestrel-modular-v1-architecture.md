# Kestrel Modular v1 architecture

 Kestrel Modular v1 is the first tracked successor candidate to the validated
 Kestrel opening bot. It lives in `bots/kestrel-modular-v1` so the
current bot and all of its evaluation identities remain frozen.

The candidate is intentionally a composition of small systems with explicit
state ownership:

| System | Owns | Public inputs and outputs |
| --- | --- | --- |
| `WorldState` | The current self snapshot, visible enemy snapshot, resources and map starts | Reads BWAPI public state; produces `WorldSnapshot` |
| `WorldMemory` | Last-seen enemy positions and a persistent scout target | Consumes visible snapshots; never reads replay or evaluator state |
| `StrategyPlanner` | Opening phase, reserves, build priorities and attack/scout gates | Consumes the snapshot and construction status; produces `Plan` |
| `WorkerAllocator` | Builder selection and mineral/owned-assimilator assignment | Consumes the snapshot; preflights public BWAPI commandability and emits gather commands through the arbiter |
| `ProductionController` | Nexus/Gateway train decisions and Zealot counters | Consumes `Plan`; emits train commands through the arbiter |
| `ConstructionController` | One-build-at-a-time lifecycle, baseline and builder ownership | Consumes `BuildIntent`; emits build commands through the arbiter |
| `ScoutingController` | Probe selection and exploration movement | Consumes `WorldMemory`; emits scout movement through the arbiter |
| `SquadController` | Zealot/Dragoon visible-target attacks, home threat holding and rally | Consumes visible state and memory; emits attack commands through the arbiter |
| `CommandArbiter` | Deduplication, command categories, rejected commands and BWAPI error counts | The only gameplay command accounting boundary |
| `Telemetry` | Durable diagnostics and architecture identity | Reads owned state; writes `bwapi-data/write/diagnostic.json` |

The live tick is fixed and documented in `src/Kestrel.cpp`: observe, remember,
plan, allocate workers, produce units, construct, scout, fight, then record.
The planner owns opening counters; the construction controller owns build
lifecycle; the arbiter owns command accounting. No system reaches into another
system's private state. Construction has a separate neutral-geyser placement
path for Assimilators, while gas workers target only owned Assimilators. Scout
targets persist until their start tile is observed as explored. Squads hold the
home radius for a short public-threat window before rallying outward. The
telemetry sample includes the callback wall-time measurement and separates
accepted command frames from the later observed current frames for the first
Pylon and Gateways.

The opening retains the strongest proven behavior that can be carried forward:
the Zerg four-Probe first-Pylon gate from v45, the 250-mineral pre-second-
Gateway reserve, and the 100-mineral reserve until the second Zealot train.
Those mechanics are isolated in `OpeningPolicy.h`, which has a standalone unit
test including the acceptance boundary: the Probe freeze ends when the Pylon
command is accepted, even if the building has not appeared in the next
observation yet. The rest of the candidate adds the architecture needed for
future work: map-aware scouting, persistent visible-enemy memory, deterministic
reallocation of up to three workers to owned Assimilators, construction
lifecycle, squad targeting and centralized command diagnostics. Scout movement
uses a deduplicated `move` command; attack-move remains reserved for combat
squads. When the home radius is threatened, squads select only nearby visible
threats or rally home and cannot chase an unrelated map-wide target.
An attacking squad member is retargeted when a new home threat appears unless
its current order target is still a visible nearby threat. A missing scout ID
is cleared before replacement selection, so a dead scout cannot permanently
disable exploration.
World snapshots and production queues are ordered by stable unit ID. Combat
targeting checks each unit's ground and air weapon, so Dragoons can defend
against visible flying threats while Zealots ignore targets they cannot hit.
Worker reassignment preserves mineral and gas return trips and checks the exact
resource target with BWAPI's public `canGather` predicate. Temporarily
uninterruptible workers are skipped instead of producing rejected commands.
Telemetry separates these preflight skips and cargo deferrals from actual
gather command attempts and accepted assignments.
Builder selection follows the same commandability boundary: after the exact
build tile is known, it preserves cargo returns, checks `canBuild(type, tile)`,
and chooses the nearest eligible Probe with unit ID as the deterministic
tie-breaker. Builder preflight skips and cargo deferrals are reported
separately from issued build commands.

Telemetry is explicitly tagged `kestrel-modular-v1`. It preserves the exact
four-Probe Pylon acceptance/completion boundary, ordered accepted Probe train
frames, second-Zealot train and completion frames, reserve-active and
eligible-Nexus reserve-active frame/available-mineral/value histories and
genuine reserve-block histories with same-callback order-aware acceptance
flags, construction
accepted/current/completed events, and attempted/rejected counts for every
command category. `scripts/score_kestrel_modular_v1.py` validates this schema
and reports diagnostic completeness only; it always marks the record as
ineligible for Elo and rejects legacy v45-shaped records.

Validation begins with build-only checks. Native OpenBW and official BWAPI
4.4.0 header lanes must compile with C++14, warnings as errors, and Release
configuration. The unit test exercises the Zerg gate, both mineral reserves,
and the non-Zerg control. Lifecycle/source checks verify that every system is
instantiated and participates in the ordered frame tick. The dashboard identity
may be registered before gameplay so every later artifact is labelled
Ours/Original, but no strength, rating, or promotion claim precedes a real
engine evaluation.
`scripts/build_kestrel_modular.sh` runs both header lanes and the unit test,
then writes a sidecar binding the binary to a sorted per-file source manifest.

The incremental experiment path is deliberately bounded:

1. Run one Zerg lifecycle smoke, preserving modular telemetry and both replay
   copies, before making any strength claim.
2. If the smoke passes, run the registered five-opponent screen and compare its
   qualitative and quantitative behavior with canonical Kestrel v13 evidence.
3. Add one system change per preregistered batch: worker assignment, scouting,
   squad target selection, then midgame production.
4. Promote only a candidate that improves the preregistered primary metric on
   held-out maps and retains zero command-rejection and lifecycle regressions.

Official BWAPI runtime execution remains unverified in this environment. The
candidate still uses only the portable BWAPI interface and has a separate
official-header object target so API drift remains visible.
