# Stardust native benchmark port

Stardust is pinned at upstream commit `22d93d7a55d0a0494384474a456fd7ee26baee97` and retained under the license copied to `ports/stardust/LICENSE`. The license permits modification and local use, but copies or substantial derivatives may not be submitted to a public StarCraft tournament without written author permission. This port is for local benchmarking only. It is not a submission variant, and no author-contact or submission claim is made.

## Source and ABI plan

Upstream's macOS build compiles a bundled OpenBW/BWAPI tree. That tree is not ABI-compatible with this project's pinned OpenBW BWAPI revision `48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2`: Stardust's copy adds public virtual methods and types including `ExactPosition`, `Unit::getExactPosition`, gather-path simulation, and state-copy APIs. Compiling against those headers and loading against this project's library would make virtual calls unsafe even if it linked.

`ports/stardust/CMakeLists.txt` therefore compiles the full Stardust gameplay source and its vendored BWEM, FAP, nlohmann, bitsery, cppcrc, zstd, and zstdstream dependencies while excluding the bundled BWAPI/OpenBW and test-opponent trees. The module links only this project's pinned `libBWAPILIB`. Upstream already provides portable `extern "C"` exports for `gameInit` and `newAIModule`; no entrypoint shim is required.

The build selects Stardust's standard BWAPI path with `IS_OPENBW=0`. This is the same source path used by its official-game tournament build. It retains strategy, combat, production, building placement, worker control, BWEM, FAP, opponent learning, mining path lookup and solver, gather/return resend logic, and takeover scheduling. The excluded bundled-OpenBW branches are limited to:

- capturing `ExactPosition` solely for mining path-loss and missing-path statistics and verbose logging;
- recording the bundled engine's BW unit ID alongside the public BWAPI unit ID in CherryVis;
- formatting those two diagnostic fields.

The normal path constructs the mining solver's `PositionAndVelocity` from Stardust's `MyWorker` position, Brood War heading, and full-precision velocity fields. The optimizer remains initialized and invoked; no strategy or gameplay subsystem is compiled out to satisfy the local ABI.

The small native adapter patch adds only runner result telemetry in `bwapi-data/write/diagnostic.json`. It reports frame, terminal winner, end state, and runtime latency without changing bot decisions. `onFrame` refreshes the nonterminal record every 240 frames so a bounded timeout retains real progress evidence; `onEnd` writes the authoritative terminal record.

## Reproducible build

When the shared compile window is free, build with:

```sh
scripts/build_stardust.sh
```

The script requires the exact Stardust, local OpenBW BWAPI, and official BWAPI revisions; rejects extra compiled source; requires the tracked checkout diff to equal `patches/stardust-native-arm64.patch`; uses Apple Clang, C++20, Release, Ninja, and at most four jobs; compiles an object-only official BWAPI 4.4 header target; and writes `build/stardust/Stardust.dylib.build.json` with source, patch, compiler, API-mode, and binary hashes.

## Verification

The 2026-09-20 build completed with Apple Clang 21.0.0. The official BWAPI 4.4 object-only check compiled all 147 Stardust gameplay translation units with `-Wall -Werror` and all 16 vendored BWEM translation units. BWEM is compiled as a separate object target so its lowercase `base.h` resolves within BWEM on macOS's case-insensitive filesystem; its existing upstream warnings use the same suppression as the linked runtime BWEM library. The runtime module exports both `gameInit` and `newAIModule`.

The frozen compatibility package is `artifacts/builds/b6097c9a5d972afc4d687ed51f0d001af36f50a93dc625d66eb546bd02f6080c/stardust-native-arm64`. Its binary SHA-256 is `b6097c9a5d972afc4d687ed51f0d001af36f50a93dc625d66eb546bd02f6080c`; its source patch SHA-256 is `2896086d8dbc69bfcf547060d765ec8cbb5f02025491a9592c2153bf448673a6`; and its copied license SHA-256 is `2fbba08e073d6bda1f0ca479ba999c88fc01bb29aa3ad8cdd6501e9322688cac`.

Run `20260920T040347-2c639d48312b` exercised frozen Stardust as Protoss against WorkerRush Zerg on Benzene with controlled engine seed 5201 and a 120-second limit. Both launcher processes exited 0 with empty stderr, opposing terminal results, LF3, and no rejected WorkerRush commands. Stardust won at its local frame 20,432. Durable archival took 10.367 seconds. Both native replays were retained and validated: player 1 SHA-256 `b383b4d89ac96a3146243d2ed2c948f37d91aa18decf817dae42c0114bb8563f`, player 2 SHA-256 `40f2f04bedb50863f238570f9f07801443f38aad6c6359bc30b516e75a3782a3`. The exact manifest is `artifacts/runs/20260920T040347-2c639d48312b/game-0001/manifest.json`.

This single game establishes native ABI interoperability and execution of the normal tournament gameplay path. It does not estimate playing strength, timing representativeness, tournament eligibility, or broader map and matchup compatibility. The engine seed fixes engine initialization; Stardust's own wall-clock or address-dependent behavior is not controlled by this smoke test.
