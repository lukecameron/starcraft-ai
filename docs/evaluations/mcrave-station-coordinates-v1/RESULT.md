# McRave station-coordinate diagnostic result

Completed 2026-09-20. The actual Destination colony-placement path reproduced the relative-coordinate defect, and the one-line candidate restored the station-defense coordinate invariant. Both games completed with verified opposing outcomes and zero launcher return codes. This is correctness evidence for the coordinate change, not a strength comparison.

## Actual-path observation

The observation-only baseline module, SHA-256 `454404a6937f56940b81354c923b0f2f74267abca3412fe231e21204d16a7744`, ran as `20260920T034044-719571d92fba`. At the first Creep Colony request, frame 3,504, the owned station had base tile `(64,118)` and four defense entries. One entry was `(0,-3)`: it was out of map bounds, failed `TilePosition::isValid`, was 64 tiles left and 121 tiles above its owning base, and exactly matched the relative Zerg offset selected in `Station::findZergLocations`. The remaining entries `(65,121)`, `(68,118)`, and `(68,121)` were in bounds and near the base. At observation time all three had a builder and creep ready, buildable unused terrain, no larva or egg overlap, and no enemy within the 32-pixel blocking threshold.

The candidate module, SHA-256 `5fed1ec386773e40d8a437df3e1418bb6618ae296f6a2f95ae6c25ed29cb8a62`, ran as `20260920T034112-72902ec44f57`. It differed from the baseline source at one policy line:

```cpp
defenses.insert(base->Location() + defense);
```

At its first Creep Colony request, also frame 3,504, the station base was `(64,118)`. Its defense set contained `(64,115)`, `(65,121)`, `(68,118)`, and `(68,121)`. Every entry was in map bounds and within four tiles of the owning base. The corrected `(64,115)` entry retained the intended `(0,-3)` displacement and passed every recorded placement predicate at observation time.

The instrumentation records candidate facts through read-only duplicate queries immediately before normal selection; it does not replace or reorder the normal placement calls. The exact instrumentation and coordinate-only patches are frozen with the experiment.

## Accepted commands and outcomes

Both game paths exercised a legal colony placement. Independently decoded replays show that the baseline issued accepted Creep Colony build commands at `(65,121)` on frames 3,531 and 3,609. The candidate issued an accepted Creep Colony build at the newly corrected `(64,115)` entry on frame 3,542. This confirms that the corrected entry is consumable by the normal placement path. The baseline later lost at frame 7,691/7,722; the candidate won at frame 16,092/16,061.

The result difference is not attributed to this fix. The controlled OpenBW scenario seed and McRave bot seed were both 1002, but ZZZKBot has no declared bot RNG seed, and its positions already differed in the two frame-3,504 observations. The two runs therefore do not support a causal win or strength claim. The baseline also had three other legal station candidates and successfully issued a colony command, so the original quick-baseline loss cannot be assigned solely to the relative entry.

The experiment does establish the narrower contract: upstream inserts a relative tile into a collection whose other producers and consumers use absolute map tiles; the defect occurs in the real game path; and adding the base location restores the invariant while producing a legal accepted build when selected. Combined with the historical unguarded `blockGrid[256][256]` consumer, the observed negative entry is also a concrete input capable of the previously repaired out-of-bounds write. It is still not a captured writer trace for a particular old crash.

## Durable evidence

The experiment index is `artifacts/experiments/mcrave-station-coordinates-v1/manifest.json`. It hashes the registered source patch, observation patch, one-line candidate patch, both isolated modules and provenance sidecars, copied run manifests, diagnostic JSONL, and independently parsed replay inputs.

- Baseline replay SHA-256: `ff18091412b66f2dba14ff614f6fa65431ddae102c8faac51b70e0c8437dc53d`.
- Candidate replay SHA-256: `8a701bd2f3615cfbd8c3968c2a6de9117c5274256f2c39870faa72d6ef46eee6`.
- Seeded source patch SHA-256: `2ab7cf14886558baf032079231ddd16d4e0d62e687317d46722b93048b7913df`.
- Observation patch SHA-256: `1b3d63c358e3590bf8d78929627cc0aad07ebe82b05f2de4fe1400fece5c05e2`.
- Coordinate-only patch SHA-256: `a927194dbf835b7496413af19c9c26e7c35ec6a59b96586cccdcf7ddf1ee7659`.

No canonical McRave source, canonical patch, baseline configuration, or rating was changed by this experiment.

## Lead decision

On 2026-09-20, the project lead accepted the one-line absolute-coordinate change for canonical integration as a correctness repair. The decision does not promote McRave on strength, change the frozen `c49ee3c4…` reference, or attribute the candidate's win to this repair. Canonical build identity and package evidence are recorded separately after the shared compile window becomes available.
