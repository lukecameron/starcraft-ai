# OpenBW terminal kill-path diagnostic v1

## Method

This logging-only build labels every `kill_client(false)` caller and records frame, sync frame, local and peer slots, controller/victory state, command ID, and hash details. The launcher records its terminal callback boundaries. It uses pinned BWAPI `48124ba…`, OpenBW `4b046d5…`, and the accepted scenario/lifetime patch without changing game or synchronization behavior.

For `kill_client` events, `game_frame` is OpenBW's engine frame at the event. Launcher markers use BWAPI's `getFrameCount()`. `onGameEnd()` calls `initializeData()`, so launcher markers after `launcher_on_game_end_complete` show the reset BWAPI counter (zero) and are ordering markers rather than terminal engine-frame measurements.

- OpenBW diagnostic patch SHA-256: `a9aa6c164650da6c730f3176a783fdddac6259289d6a38842e3c260401a729d1`
- Launcher diagnostic patch SHA-256: `c0011bf233e010ac6eb391933867a75be835ccd6c29b214532dfecef0ad32cb6`
- Diagnostic `libOpenBWData.dylib` SHA-256: `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb`
- Diagnostic launcher SHA-256: `562bcfa32919f95c8771607f88b779798f3e7343ab1d0f2befbe67a4071f083d`

Two trials were preregistered and run once each. Instrumented timing is not used as performance evidence.

## Rebuild

Apply [openbw-kill-diagnostics.patch](../../../patches/openbw-kill-diagnostics.patch) to a pristine OpenBW checkout at `4b046d5f65302b10cb0a745f0fecd37ec85b20a8`. This is the complete diff used by the diagnostic build: it includes the accepted scenario and lifetime changes as well as kill-source logging. Do not apply `openbw-scenarios.patch` first. Apply [bwapi-terminal-diagnostics.patch](../../../patches/bwapi-terminal-diagnostics.patch) to a pristine BWAPI checkout at `48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2`; that patch is an independent launcher-only diff.

Configure and build the isolated checkouts with:

```sh
git -C third_party/openbw-outcome-diagnostic apply patches/openbw-kill-diagnostics.patch
git -C third_party/bwapi-outcome-diagnostic apply patches/bwapi-terminal-diagnostics.patch
.tools/engine/bin/cmake \
  -S third_party/bwapi-outcome-diagnostic \
  -B third_party/bwapi-outcome-diagnostic/build-arm64 \
  -G Ninja \
  -DCMAKE_MAKE_PROGRAM="$PWD/.tools/engine/bin/ninja" \
  -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DOPENBW_DIR="$PWD/third_party/openbw-outcome-diagnostic" \
  -DOPENBW_ENABLE_UI=OFF
.tools/engine/bin/cmake --build third_party/bwapi-outcome-diagnostic/build-arm64 --parallel 4
```

The exact tested package, including launcher, libraries, and provenance sidecar, is frozen at `artifacts/builds/27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb/openbw-kill-path-diagnostic/`. Future exact-input diagnostics can use that package directly.

## Results

The WorkerRush versus Idle control, run `20260920T041950-ef7fd1a4b7a0`, completed with verified opposing callbacks. Idle observed defeat at frame 3,382. WorkerRush observed victory at frame 3,413, exactly 31 frames later. On the survivor, the first reason-6 event was `controller_not_occupied_after_action` at game frame 3,384: the peer already had controller 10 and victory state 2, and the processed command was ID 87 (`Leave Game`). On the already-ended loser, a later transport callback observed the still-active winner. The result remained WorkerRush win and Idle loss.

The exact competitive attempt, run `20260920T042014-eaa6bbea4b79`, also completed with verified opposing callbacks. UAlbertaBot observed defeat at frame 20,804; McRave observed victory at frame 20,835, again exactly 31 frames later. McRave's process classified the peer at frame 20,806 through `controller_not_occupied_after_action`, with controller 10, victory state 2, and command ID 87. UAlbertaBot's already-ended process later observed a transport callback. No in-sync hash mismatch occurred.

## Interpretation

The control establishes the normal melee ordering from source and runtime evidence: defeat commits in one trigger pass, and the survivor's victory commits at the next pass 31 frames later. A reason-6 replay command after defeat can be routine cleanup from `controller_not_occupied_after_action`; it does not by itself establish outcome corruption.

Neither registered attempt reproduced the historical reciprocal winner failure, so that failure's initiating kill path remains unknown. In the historical replays, both reason-6 commands precede the corresponding winning callbacks, including a drop of the still-viable UAlbertaBot side. That pattern is inconsistent with the routine post-defeat ordering observed here. An in-sync hash mismatch or a bidirectional transport failure remains plausible, but neither is proven without diagnostic logs from a reproducing run. No semantic repair is justified from this two-run diagnostic alone.

Raw preregistration, patches, build logs, normalized events, manifests, stderr, and replays are preserved under `artifacts/experiments/openbw-kill-path-diagnostic-v1`, `artifacts/runs`, and `artifacts/replays`.
