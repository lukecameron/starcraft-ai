# Destination loss analysis

This note examines game 3 of `quick-mcrave-crashfix-baseline-v1`, run `20260920T025025-914278200f55`. It is a completed, outcome-verified game on Destination with scenario seed `1002`: McRave Zerg was launcher player 1 and lost to ZZZKBot Zerg. Both launchers returned zero and both terminal callbacks agreed. McRave reported frame 6,110 with one Drone and no Hatchery, Pool, or Zerglings; ZZZKBot reported a win at frame 6,141 and a maximum of 13 Zerglings. The manifest fixes the engine, module, map, and replay hashes.

## Raw evidence

The McRave log selected `PoolLairGaspool1HatchMuta`. It first logged attempts to produce Zerglings at frame 2,720, classified the opposing 4 Pool as possible at 3,471, likely at 3,483, and confirmed at 4,311. It first reported `Couldn't find a position to build Zerg_Creep_Colony` at frame 3,600 and repeated the failure through frame 4,901. From frame 5,412 it instead repeatedly failed to place a Hatchery. The durable sources are:

- `artifacts/runs/20260920T025025-914278200f55/game-0001/manifest.json`
- `artifacts/runs/20260920T025025-914278200f55/game-0001/player-1/bwapi-data/write/logger.txt`
- `artifacts/replays/2026/09/20/20260920T025025-914278200f55/game-0001-player-1-1.rep`, SHA-256 `6cf33bf9eb92686084e0c79372ed4fff606511acfb803fe01bd8afcd7a6e6cdc`

The replay was decoded independently with:

```sh
.tools/screp/screp -cmds -header -computed=false -indent=true \
  -outfile /tmp/quick-baseline-loss.json \
  artifacts/replays/2026/09/20/20260920T025025-914278200f55/game-0001-player-1-1.rep
```

The replay identifies McRave as replay player ID 1 and ZZZKBot as replay player ID 0. McRave's accepted economy and production commands include Drone morphs at frames 2, 354, 523, 767, and 917; Overlord at 1,224; Extractor at tile `(64,113)` at 1,374; another Drone at 1,507; Spawning Pool at tile `(61,114)` at 2,035; three more Drones at 2,163, 2,346, and 2,526; and Zergling morph commands at 3,274, 3,282, and 3,401. There is no accepted Creep Colony build command. ZZZKBot's accepted Pool build is at frame 835 and its Zergling morphs begin at 2,077. At frame 3,401 its units receive repeated right-click commands toward `(2112,3824)`, the area of McRave's bottom start, before McRave's first colony-placement failure at 3,600.

The repeated `Producing Zerg_Zergling` messages are not proof of accepted commands. `Producing.cpp::produce` calls `train`, ignores its Boolean result, updates local accounting, and logs success unconditionally. The parsed replay is the evidence for commands accepted by the engine.

The placement failure is consistent with existing policy. Before 3:30, `Planning.cpp::isBuildable` rejects a candidate when a non-worker, non-building enemy ground unit is within a box distance of 32 pixels. It also rejects used or unbuildable terrain, and creep buildings require both a builder and creep ready on arrival. `findDefenseLocation` tries the pocket defense and station defense set before wall and block fallbacks. The current log records only the final failure, so it does not identify which predicate rejected each candidate.

On the evidence available, this is most likely a normal strategy/placement-policy loss to a faster rush: McRave chose an economic opener, detected the rush after enemy Zerglings existed, issued only three accepted Zergling morph commands, and never issued a colony build before losing its main. The relevant Planning and Producing behavior is upstream behavior rather than a native-port change.

## Separate Station coordinate defect

`BWEB::Station::defenses` has an absolute map-tile contract. The other producers add `base->Location()` before insertion: `addIfPlaceable` inserts its computed absolute `placement`, and `findDefenses` inserts an absolute `tile`. Every inspected consumer also uses entries as absolute coordinates: Planning converts an entry directly to a map `Position`, Buildings compares it directly with a building tile, Wall compares it with wall tiles, and `Block::initialize` passes it directly to `addToBlockGrid`.

The Zerg secondary-location path violates that contract. It validates `base->Location() + defense`, inserts the medium and small locations as `base->Location() + offset`, but inserts the raw relative `defense` offset. The constructor subsequently calls `findDefenses`, then `cleanup`; cleanup reserves every entry but does not remove or normalize the relative one. This line is unchanged from upstream commit `7d1719a22d8b896f957abae50e2ea5efff974fe2`, so it is an upstream gameplay defect rather than a native-port regression.

This also gives a concrete source path for the earlier block-grid memory corruption. Some Zerg defense offsets are negative, including `(0,-3)`, `(-3,-2)`, and `(-2,-2)`. `Block::initialize` forwards every station defense to the historical `addToBlockGrid`, whose upstream implementation indexed the fixed `blockGrid[256][256]` without checking either coordinate. A surviving negative relative entry therefore causes an out-of-bounds write. The current port's bounds check prevents that write. This call chain proves that the Station defect *can* cause the repaired class of corruption; it does not prove which coordinate caused a particular historical crash because no writer watchpoint captured the offending value. Positive relative entries remain in bounds but refer to unrelated tiles near the map origin.

The Station defect can also deprive Planning of one intended absolute defense candidate, but the current replay and log do not show the candidate set or rejection reasons. It therefore does not establish that the defect caused this loss.

## Bounded diagnostic plan

After the current isolated performance gate, run one diagnostic baseline on Destination with the same frozen engine, launcher assignment, scenario seed 1002, bot binaries, and explicit McRave bot seed. Preserve the remaining opponent nondeterminism if ZZZKBot still lacks bot-seed control. The diagnostic build should add records only; it must not change candidate ordering or policy.

For the first requested Creep Colony, record the station base tile, pocket tile, complete defense set, and every candidate in evaluation order. For each candidate record the exact rejection facts already computed by Planning: coordinate validity, larva or egg overlap, pathability, planned/used footprint, terrain buildability, nearby enemy identity and box distance, builder availability, and creep readiness. Separately record the attempted `Unit::build` return value and confirm acceptance from the archived replay. Add an initialization record that marks each station defense as absolute/in-map and records its distance from the owning base.

The coordinate contract is clear enough that the candidate source fix is exactly one line:

```cpp
defenses.insert(base->Location() + defense);
```

Do not promote it from this analysis alone. Compare the diagnostic-only baseline with that one-line candidate under identical controls. The acceptance evidence is that all station defense entries are absolute and in-map, the intended candidate appears in the same ordered evaluation, and any changed build command is explained by the recorded predicate results. A win by itself is not evidence of correctness.

## Uncertainties

- The replay records accepted commands, not McRave's rejected API calls or internal candidate ordering.
- The generic placement log does not distinguish enemy proximity, creep timing, builder availability, reservation, terrain, larva/egg overlap, or path rejection.
- Scenario seed 1002 controls OpenBW starts and simulation RNG. This historical run did not record a McRave bot RNG seed, and ZZZKBot currently has no declared bot-seed hook.
- The Station coordinate defect is source-proven. Its role in this loss and its role in any one historical teardown crash remain unproven without the proposed records or a captured invalid write.
