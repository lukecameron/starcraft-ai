# ZZZKBot native ARM64 port

This spike builds the upstream ZZZKBot 1.7 source as a native macOS ARM64 BWAPI module. The source is pinned to `chriscoxe/ZZZKBot` revision `7183e37b6b416ea53c1040c83e639a3a3c395eed` (2025-10-23). Its `LICENSE.txt` declares GNU LGPL version 3 and the checkout includes the GPL and LGPL license texts.

## Build

The checkout lives at `third_party/zzzkbot` and remains uncommitted project data. Build it with:

```sh
scripts/build_zzzkbot.sh
```

The script checks the immutable ZZZKBot and OpenBW BWAPI revisions, rejects any tracked change outside the exact port patch and any untracked compiled source, applies `patches/zzzkbot-native-arm64.patch` when needed, uses at most four compile jobs, and writes:

- `build/zzzkbot/lib/ZZZKBot.dylib`
- `build/zzzkbot/lib/ZZZKBot.dylib.build.json`

The patch keeps the gameplay logic intact. It makes DLL exports portable, preserves the original Windows `DllMain`, supplies the POSIX `localtime_s` equivalent, and makes integer values stored in BWAPI client-info pointers explicit through `intptr_t`. OpenBW's BWAPI adapter throws from `getRandomSeed()`, so the port writes zero only to ZZZKBot's diagnostic learning-file field on non-Windows builds; the value is not used for decisions. The `_WIN32` path retains the upstream call and is suitable for the official Windows BWAPI route.

Passive smoke-test instrumentation records `onEnd`, LF3, and maximum Drone, Spawning Pool, and Zergling counts in `bwapi-data/write/zzzkbot-port.json`. It does not issue commands or affect decisions. Upstream learning data continues to use isolated `bwapi-data/read` and `bwapi-data/write` directories. Each runner game starts with empty learning state unless the caller stages files there.

## End-to-end evidence

The completed instrumented game is recorded at `artifacts/runs/20260920T020354-3439da878c87/game-0001/manifest.json`. It ran ZZZKBot as Zerg against the diagnostic WorkerRush module as Protoss on Benzene through two native OpenBW clients. Both launchers exited normally in 1.46 seconds after 4,250 corroborating opponent frames. ZZZKBot's `onEnd` record reports a win at frame 4,281, LF3, a maximum of four Drones, one Spawning Pool, and twelve Zerglings. WorkerRush independently reports a loss, LF3, 30 accepted commands, and zero rejected commands.

The harness marks the game `incomplete` and `outcome_verified: false` because ZZZKBot does not implement the harness-specific `MATCH_RESULT_PATH` contract. Its passive record and normal learning-file `onEnd` result corroborate the winner, but this is not represented as a harness-verified score. Both player replays were archived. The player-one replay is `artifacts/replays/2026/09/20/20260920T020354-3439da878c87/game-0001-player-1-1.rep`, SHA-256 `24c7058bdc8405a0f5449f2333b54128734812055d86beb7ceffd8dc5eb51af0`.

The first pre-fix match remains at `artifacts/runs/20260920T015839-f57964f4d137/game-0001/manifest.json`. It timed out after OpenBW rejected the diagnostic `getRandomSeed()` call. A second successful pre-instrumentation game remains at `artifacts/runs/20260920T020158-26a87130580b/game-0001/manifest.json`.

The cross-port game against McRave is recorded at `artifacts/runs/20260920T020618-09905c5f8fef/game-0001/manifest.json`. It completed and produced opposing verified `onEnd` results: McRave won at frame 9,520 and ZZZKBot lost at frame 9,489. Durable completion took 15.05 seconds at 632.77 logical frames per wall second. Peak whole-process RSS was 46,678,016 bytes for OpenBW plus ZZZKBot and 486,965,248 bytes for OpenBW plus McRave. Both reported LF3. ZZZKBot reached four Drones, one Spawning Pool, and twelve simultaneous Zerglings; McRave ended with twelve Drones, two Hatcheries, one Spawning Pool, and seventeen Zerglings.

Both archived cross-port replays parse successfully with `screp`. Their command streams agree and show plausible production: player 0 issued morph/build commands for thirteen Drones, three Hatcheries, one Spawning Pool, seventeen Zerglings, an Extractor, a Creep Colony, a Spire, and three Overlords; player 1 issued commands for two Drones, one Spawning Pool, thirty Zerglings, and three Extractors. The archived SHA-256 values are `1011b24d33424835275e721a4e3dfc865a0f2e68357ea6dfad11cfdcc38689d6` and `020ed21efd9397a4d538ae001fd3008e9b7bd582d25b1fc244d2fbd9fe7d1614`.

OpenBW currently derives the match seed from random client identifiers. The replay contains the actual seed, but this runner does not yet control fixed seeds or start slots. Results therefore represent a native compatibility and behavior smoke test, not a matched deterministic benchmark.

## Benchmark identity

This artifact identifies the public source revision and its binary exactly. It does not establish that the build is byte-for-byte or behaviorally identical to the ZZZKBot binary currently deployed on BASIL or any other ladder. Treat ladder ratings and historical results as context, not as measurements of this local build.

## License notices

ZZZKBot declares GNU LGPL version 3. The upstream `LICENSE.txt`, GNU LGPL text (`COPYING.LESSER.txt`), and referenced GNU GPL text (`COPYING.txt`) are preserved under `ports/zzzkbot/`.
