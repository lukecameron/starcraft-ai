# McRave–ZZZK Heartbreak Ridge loss analysis

Status: descriptive replay review only. These observations do not establish a map effect, an opening-strength ranking, or a promotion decision.

## Replay evidence

The two Heartbreak Ridge losses were parsed from the retained `.screp.json` files. The comparison win is the retained Benzene game from the quick calibration run.

| run | map | McRave seed / slot | McRave Pool | first McRave Zergling | first defensive colony / Sunken | replay frames |
| --- | --- | --- | ---: | ---: | --- | ---: |
| `20260920T060306-47ba9d7473b9` | Heartbreak Ridge | `6301` / P1 | 2124 | 3372 | Colony 3227 / Sunken 3578 | 6295 |
| `20260920T060306-9cf5c734d9b3` | Heartbreak Ridge | `6301` / P2 | 2113 | 3361 | Colony 3050 / Sunken 3400 | 6915 |
| `20260920T045544-8acfc489271f` | Benzene | `1001` / P1 | 1499 | 2736 | Colony 3532 / Sunken 3864 | 13766 |

ZZZK's first Pool and first Zerglings were near frames 917/2159 and 861/2103 in the two Heartbreak games, versus 805/2047 in the Benzene comparison. Thus both Heartbreak losses show McRave's Pool and first-ling timings roughly 600 frames later than this comparison, while ZZZK's early timings are similar. This is a useful target for a controlled opening probe, not a causal explanation of the losses.

The two losses both use McRave bot seed `6301`; the Benzene win uses `1001`. The map SHA, player slot, and opponent/default RNG also differ. Therefore the approximately 600-frame delay may reflect opening selection or other seeded behavior rather than Heartbreak Ridge. The command stream does not expose a selected build name, so these replays cannot be labeled as `12Hatch`, `9Pool`, or another exact opener.

## Source and build-selection context

The McRave 04521 source selects the ZvZ opener through `Source/McRave/Builds/Zerg/ZergBuildOrder.cpp` (`opener()` dispatches to `ZvZ()`). `Source/McRave/Builds/All/Learning.cpp` uses the default ZvZ tuple `Z_PoolLair`, `Z_9Pool`, `Z_1HatchMuta` when no learning result is available, but its learned-build path reads the isolated `bwapi-data/read` or `write` learning file and adds `rand() % randomness` to UCB selection. The ZvZ pool/hatch implementation in `Source/McRave/Builds/Zerg/ZvZ/ZvZ_PoolHatch.cpp` contains distinct `ZvZ_PH_Overpool` and `ZvZ_PH_12Pool` paths.

The calibration manifests used empty per-run learning directories. Even so, seed-dependent random selection and the source's multiple ZvZ paths mean that replay timings alone cannot identify which opener ran. No strategy change is inferred here.

## Small controlled probe

Run four short, retained matches before changing strategy: both Heartbreak Ridge and Benzene, with McRave seeds `1001` and `6301`, keeping the opponent revision, map files, learning directories, engine build, and player slots fixed. A second four-game block can swap the slots if the first block shows a slot interaction.

Add startup telemetry to the existing diagnostic path for the selected build/opener/transition and frame timestamps for the first Extractor, Pool, Hatchery/Overlord, first Zergling, first Creep Colony, and first Sunken. Record ZZZK's first Pool/ling timestamps in the same manifest. Keep learning directories empty and preserve each replay and manifest. Compare seed and map effects only after the opener labels are present; do not force an opening or call a map effect from this two-loss sample.
