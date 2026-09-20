# OpenBW socket teardown lifetime repair

## Registered engineering check

The archived pre-fix reproduction is `artifacts/runs/20260920T025029-fe8a87ea13f5/manifest.json`: controlled seed 1002 on Destination, ZZZKBot Zerg as player 1 and McRave Zerg as player 2. Gameplay ended with opposing result metadata and both replays, then the losing ZZZKBot launcher exited on SIGSEGV. macOS report `BWAPILauncher-2026-09-20-125043.ips` faults in `sync_server_asio_socket::async_release` while Asio destroys a pending read operation during `io_service` shutdown. The earlier McRave teardown crash has the same stack, so this is an engine lifecycle defect rather than bot policy behavior.

Before changing the source, the launcher, `libOpenBWData.dylib`, build sidecar, exact source patch, and failure references were frozen under `artifacts/builds/e8cf9b6caaadaf5cdda2e51e0897e3b85d4bd905166cb2860ff215cb4ed789fb/engine-before-teardown-fix/`.

The bounded acceptance check is:

1. Source review must establish that every `async_handle_t` construction carries a teardown guard whose lifetime extends through `io_service` member destruction. Constructors, copies, and destructors must avoid dereferencing a client once teardown begins.
2. Rebuild the pinned OpenBW/BWAPI release with the exact combined patch and record binary, library, compiler, revision, and patch hashes.
3. Repeat the exact seed-1002 Destination ZZZKBot-player-1/McRave-player-2 fixture with the frozen bot binaries and 120-second limit. Both launchers must exit zero after verified opposing onEnd metadata; replay archives must remain present.
4. Run a focused instrumented check if the build supports AddressSanitizer without changing gameplay. It is supporting lifetime evidence and cannot replace the release reproduction.

A clean result repairs an engine teardown failure only. It does not change or validate bot strength, and it does not authorize another evaluation batch.

## Repair and evidence

`sync_server_asio_socket` declared its Asio `io_service` before its client list. C++ destroys members in reverse declaration order, so the client list was already gone when `io_service` shutdown destroyed queued read handlers. Each handler owned an `async_handle_t`; its destructor decremented `client_t::async_count` through the dangling pointer and could call `async_release` with the client's stale list iterator. Both crash reports fault at that exact release path during `task_io_service::shutdown_service`.

The repair adds a `shutting_down` guard before `io_service`, which makes the guard the last relevant member destroyed. The server destructor raises the guard before member destruction starts. `async_handle_t` receives that guard through the sole construction helper, preserves it in copies, and checks it before either a copy increments or a destructor decrements the client reference count. All three asynchronous client operations use that helper: queued writes and the two read scheduling paths. Normal client release behavior is unchanged while the server is live.

The canonical combined patch is `patches/openbw-scenarios.patch`, SHA-256 `27a66cbe6066380eae72efb1ae5d58058226957577fa7dc7e3ab4197b4a04a19`. `scripts/engine-build.sh` rebuilt pinned BWAPI `48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2` and OpenBW `4b046d5f65302b10cb0a745f0fecd37ec85b20a8` using Apple clang 21.0.0. The release engine is frozen under `artifacts/builds/527b537903be9a77fcdd9c71a1db55b5f95d9ea3fe727433758078c24a0a2a3e/openbw-teardown-fix/`. Its relevant hashes are:

- `BWAPILauncher`: `0d552c0e4deb4cdaa3bc88136fd0189313b7b9066919c3884c0df528440ec94b` (unchanged because the repaired code is in a dynamic library)
- `libOpenBWData.dylib`: `527b537903be9a77fcdd9c71a1db55b5f95d9ea3fe727433758078c24a0a2a3e`
- `libBWAPI.dylib`: `5e6c8248e2238636720264e463018cd638915f3677540abc0aa649d2a40c905e`
- `libBWAPILIB.dylib`: `7871583246c975ab788fc88d9490decd4eb9cb797e842aa741e3da69a2ff4702`

The exact release regression is `artifacts/runs/20260920T030014-a9f28a767c13/game-0001/manifest.json`. ZZZKBot lost and McRave won with verified opposing callbacks; both launchers returned zero, both stderr logs were empty, and both replays were archived. It completed 9,396 logical frames in 13.543 seconds. The player replay hashes are `76c659a0da731f9be17cdba606467f3a21845462c2cb56334c1aad23edae7964` and `58732755198186578cdeb7f9bcd7d8ab40b90583feec9d5975d12bfb2bf098bb`. No new macOS crash report appeared.

The first ASan attempt, `artifacts/runs/20260920T030331-626756454df6/game-0001/manifest.json`, exposed a separate pre-existing stack-use-after-scope in `syncer_t::sync`: an asynchronous timer callback retains the address of local `timed_out`. It aborted before teardown, so it is retained as a diagnostic failure and is not evidence for this repair. Rebuilding with Clang's stack-scope instrumentation disabled allowed AddressSanitizer to exercise the target teardown path while retaining heap and ordinary stack checking. Run `artifacts/runs/20260920T030621-c0f36e271e80/game-0001/manifest.json` completed with verified opposing results, both launchers at return code zero, empty sanitizer stderr, and two archived replays. That run took 45.697 seconds and reached 15,720 frames; instrumentation changed bot timing and game trajectory, so its result is memory-lifetime evidence rather than a deterministic gameplay comparison.

## Asynchronous timer state repair

The initial ASan failure above was a real second lifetime defect. In `syncer_t::sync`, the 50 ms callback captured stack-local `timed_out` by reference. A scheduled action could make the loop return before the timer fired, leaving the callback to write the expired stack variable later. `final_sync` used the same unsafe pattern with a 250 ms timer. The repair allocates each completion flag with `std::make_shared<bool>`, captures that shared state by value in the handler, and reads it through the shared pointer in the waiting loop. This preserves the existing timeout and timer replacement behavior while keeping state alive until Asio destroys or invokes the callback.

An initial shared-state build used patch SHA-256 `ca1f35651a380d2523983963e9138080b898bbb3418fb21060e1db281b4f7a16`, but review found two remaining `final_sync` predicates testing the shared pointer rather than `*timed_out`. Its runs and `30dc2600…` library are preserved as superseded diagnostic evidence and are not acceptance evidence. The corrected full combined patch is SHA-256 `73c2716d76e53c81f0dca4637634ce25b8c21dfa94ffba40e81737a434547d2e`. The corrected release `libOpenBWData.dylib` is SHA-256 `f1a32e5a3dc64b8c62a17788488d36594dd95b13ef124637795b5aca4c846c42` and is frozen with its dependent libraries, launcher, sidecar, patch, and validation record under `artifacts/builds/f1a32e5a3dc64b8c62a17788488d36594dd95b13ef124637795b5aca4c846c42/openbw-timer-lifetime-fix/`. The prior teardown-only `527b5379…` library remains preserved separately.

Corrected release run `artifacts/runs/20260920T031316-047d7cddf7d5/game-0001/manifest.json` repeated the seed-1002 Destination fixture. It completed with a verified ZZZKBot loss and McRave win, both launcher return codes zero, empty stderr, and both replays archived. It reached 9,644 frames in 12.364 seconds.

The final instrumented build uses default Clang AddressSanitizer stack-use-after-scope instrumentation; it does not carry the earlier diagnostic `-fno-sanitize-address-use-after-scope` exemption. Corrected run `artifacts/runs/20260920T031425-8bf5f2dec3b9/game-0001/manifest.json` completed with opposing verified results, both return codes zero, empty sanitizer stderr, and both replays archived. It reached 10,047 frames in 21.669 seconds. The exact configure, build, options, and match command are preserved in `artifacts/spikes/openbw-teardown/asan-full-build-command.txt`.
