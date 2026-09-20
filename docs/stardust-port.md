# Stardust native benchmark fork

The current provisional local opponent is our repaired native fork of [Stardust](https://github.com/bmnielsen/Stardust) by [Bruce Mackenzie Nielsen](https://github.com/bmnielsen). It is pinned to upstream commit `22d93d7a55d0a0494384474a456fd7ee26baee97`; the frozen module has SHA-256 `1039975842c6edea71043e0da091ff21ad5311fd3ddbeb568cf89b364f7d28aa` and is stored in `artifacts/builds/1039975842c6edea71043e0da091ff21ad5311fd3ddbeb568cf89b364f7d28aa/stardust-emptytimer-repair/`.

This artifact must be described as **Ours / Fork**, with upstream authorship retained. Its evidence establishes compatibility with this local OpenBW evaluator only. It does not inherit an upstream or BASIL rating, establish playing strength, or establish tournament eligibility.

Stardust's license is copied to `ports/stardust/LICENSE`. It permits modification and local use, but copies or substantial derivatives may not be submitted to a public StarCraft tournament without written author permission. This project uses the fork only for local benchmarking.

## Current evidence

The evidence chain preserves both the original failure and the repair:

- The [original four-game cohort](evaluations/stardust-cohort-v1/RESULT.md) is rejected. Its first game crashed in `MiningOptimization::PatchOccupiedForecast::PatchOccupiedForecast`; three later clean games do not override that failure.
- The [empty-timer diagnostic](evaluations/stardust-emptytimer-diagnostic-v1/RESULT.md) confirmed that the producer can exhaust the singleton timer set `{0}`. That violation provides a concrete route to the original faulting reverse-iterator operation, although the original crash did not record its exact timer set.
- The [repair probe](evaluations/stardust-emptytimer-repair-v1/RESULT.md) completed the formerly failing seed and matchup with opposing terminal results, no state-hash mismatch, plausible gameplay, and bounded recovery telemetry.
- The [repaired four-game cohort](evaluations/stardust-repaired-cohort-v1/RESULT.md) passed all registered compatibility gates. All four games completed cleanly; each game exceeded 384 frames per second; the aggregate rate was 2,059.4 frames per second; and replay evidence contained worker, building, and combat-unit production commands. This remains a local compatibility result rather than a strength comparison.

The repair preserves the normal nonempty timer path. When the optimization exhausts all timer candidates, it restores the conservative pre-cycle domain `{1..8}`, after which the existing cycle produces `{0..7}`. A defensive consumer check marks the patch fully saturated and returns from construction if an empty set nevertheless reaches it. Recovery logging is bounded and does not expose private game state to policy code.

## Source and ABI plan

Upstream's macOS build compiles a bundled OpenBW/BWAPI tree. That tree is not ABI-compatible with this project's pinned OpenBW BWAPI revision `48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2`: Stardust's copy adds public virtual methods and types including `ExactPosition`, `Unit::getExactPosition`, gather-path simulation, and state-copy APIs. Compiling against those headers and loading against this project's library would make virtual calls unsafe even if it linked.

`ports/stardust/CMakeLists.txt` therefore compiles the full Stardust gameplay source and its vendored BWEM, FAP, nlohmann, bitsery, cppcrc, zstd, and zstdstream dependencies while excluding the bundled BWAPI/OpenBW and test-opponent trees. The module links only this project's pinned `libBWAPILIB`. Upstream already provides portable `extern "C"` exports for `gameInit` and `newAIModule`; no entrypoint shim is required.

The build selects Stardust's standard BWAPI path with `IS_OPENBW=0`, the source path used by its official-game tournament build. It retains strategy, combat, production, building placement, worker control, BWEM, FAP, opponent learning, mining path lookup and solver, gather/return resend logic, and takeover scheduling. The excluded bundled-OpenBW branches are limited to diagnostic fields and mining statistics that depend on its incompatible API extensions. The native adapter adds runner result telemetry in `bwapi-data/write/diagnostic.json`; it does not alter bot decisions.

## Direct reproducible build

Use a separate checkout so the current port tree and the original failed artifact remain unchanged. The full repair patch includes the native adapter and the empty-timer repair, so apply it directly to a pristine checkout; do not apply `stardust-native-arm64.patch` first.

```sh
git clone https://github.com/bmnielsen/Stardust.git third_party/stardust-repaired
git -C third_party/stardust-repaired checkout 22d93d7a55d0a0494384474a456fd7ee26baee97
git -C third_party/stardust-repaired apply "$PWD/patches/stardust-emptytimer-repair.patch"

.tools/engine/bin/cmake \
  -S ports/stardust \
  -B build/stardust-repaired \
  -G Ninja \
  -DCMAKE_MAKE_PROGRAM="$PWD/.tools/engine/bin/ninja" \
  -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release \
  -DSTARDUST_SOURCE_ROOT="$PWD/third_party/stardust-repaired" \
  -DBWAPI_ROOT="$PWD/third_party/bwapi" \
  -DBWAPI_BUILD="$PWD/third_party/bwapi/build-arm64" \
  -DBWAPI_OFFICIAL_ROOT="$PWD/third_party/bwapi-official"

.tools/engine/bin/cmake --build build/stardust-repaired \
  --target StardustOfficialHeaders --parallel 4
.tools/engine/bin/cmake --build build/stardust-repaired \
  --target Stardust --parallel 4
```

These commands assume the project's pinned BWAPI/OpenBW, official BWAPI, CMake, and Ninja dependencies are already present at the paths shown. The full patch SHA-256 is `cd3a3555459c481f5bf4b3455a8604cb4443d10ba2c68b31118f475f0d187325`. `patches/stardust-emptytimer-repair.incremental.patch` is retained only for reproducing the repair on an already native-patched checkout.

The verified repair build used Apple Clang 21.0.0, C++20, Release mode, Ninja, and at most four compile jobs. The native module and the `StardustOfficialHeaders` object-only compatibility target both compiled successfully. The frozen package includes the module, provenance sidecar, full and incremental patches, and copied license.

## Historical original smoke

The original native port produced module SHA-256 `b6097c9a5d972afc4d687ed51f0d001af36f50a93dc625d66eb546bd02f6080c`, frozen under `artifacts/builds/b6097c9a5d972afc4d687ed51f0d001af36f50a93dc625d66eb546bd02f6080c/stardust-native-arm64/`. Run `20260920T040347-2c639d48312b` completed against WorkerRush and established basic native ABI interoperability and execution of Stardust's normal gameplay path.

That smoke result is historical. The later original cohort exposed the empty-timer failure, so the `b609…` package is rejected as the current opponent. It does not supersede the repaired `103997…` compatibility evidence above.
