# Match records

`scripts/run_match.py` launches exactly two native BWAPILauncher processes for one OpenBW match. Each player gets an isolated working directory and private `bwapi-data/read` and `bwapi-data/write` state. Both processes share one unique short `OPENBW_LOCAL_PATH`; game assets are symlinked from the supplied game-data directory.

Example:

```sh
python3 scripts/run_match.py \
  --launcher third_party/bwapi/build-arm64/bin/BWAPILauncher \
  --library-path third_party/bwapi/build-arm64/lib \
  --bot1 path/to/one.dylib --race1 Terran \
  --bot2 path/to/two.dylib --race2 Zerg \
  --map 'maps/(4)Fighting Spirit.scx' \
  --game-data-dir /path/to/starcraft-data \
  --purpose 'engine integration smoke test' \
  --wall-timeout 1800
```

The game-data directory must contain the exact OpenBW filenames `Patch_rt.mpq`, `StarDat.mpq`, and `BrooDat.mpq`, plus the configured map. The launcher runs with the UI disabled, LAN automation, and direct `LOCAL` transport. Source inspection verified that `OpenBWData/BW/BWData.cpp` resets the multiplayer latency to 3 logical frames on every map load and `Game::getLatencyFrames()` returns that value directly; no configuration override was found. This matches the project's LF3 convention. Both diagnostic clients also reported runtime latency of 3 frames. With no UI, OpenBW's frame loop does not sleep; game-speed configuration affects only the UI branch.

Every invocation first writes `artifacts/runs/<run-id>/game-0001/manifest.json` with status `launching`, updates it to `running`, then replaces it atomically with a terminal record. A copy at `artifacts/runs/<run-id>/manifest.json` supports run-level discovery. Terminal records survive normal failure, wall timeout, SIGINT, and SIGTERM. They include exact command and relevant environment, input SHA-256 hashes, child return codes, logs, resource measurements, and replay archival records. Per-player CPU and peak RSS cover that player's BWAPILauncher process, including its OpenBW engine and loaded module. End-to-end elapsed time covers harness setup through replay archival and terminal-manifest preparation; filesystem durability is completed immediately afterward.

`--seed` controls the OpenBW scenario RNG used for race and starting-slot draws when the verified engine supports it. Optional `--bot-seed1` and `--bot-seed2` independently pass an unsigned 32-bit `MATCH_BOT_SEED` to the corresponding module. A bot seed is accepted only when the module hash matches a build sidecar declaring `bot_rng_control.env` as `MATCH_BOT_SEED`. Requested and omitted values are recorded per player and in `reproducibility`; omission preserves the bot's native default. The launcher removes inherited `MATCH_*` variables before adding requested values, so one player's seed cannot leak to the other.

The harness first looks for the test/integration hook `MATCH_RESULT_PATH`, then for the tournament-compatible `bwapi-data/write/diagnostic.json`. A bot may write a JSON object there from its actual game callbacks, for example `{"winner": true, "frame_count": 12345, "ended": true, "latency_frames": 3}`. The harness preserves that object without inferring missing fields. It also inventories and hashes every regular file in the player's write-state directory. Until a bot emits metadata, result and logical-frame fields remain null. A zero launcher return code is not treated as proof of a healthy game; stderr is retained and marked because BWAPILauncher catches some startup errors. A match without an archived replay is terminally recorded as failed rather than silently accepted as complete.

Every `.rep` actually emitted anywhere in a player's isolated directory is copied byte-for-byte to `artifacts/replays/YYYY/MM/DD/<run-id>/`, fsynced, and recorded with size and SHA-256. The harness never manufactures a replay, result, adjudicated outcome, or rating. When no replay exists, the manifest records a reason and keeps both players' logs. Failed and interrupted games remain first-class records.

Completion requires two well-formed terminal callbacks with opposing winner flags, plus archived replay output and healthy process exits. Missing or contradictory metadata produces `incomplete`, not success. Invalid metadata is retained on disk with an error in the terminal manifest. Replay parsing and playback are separate validation steps; a `.rep` filename alone proves neither.

Runtime LF3 has now been confirmed by both diagnostic clients. The transient socket directory is a short `/tmp/scai-*` path to fit macOS Unix-domain socket limits and is removed only after the exact child processes are reaped. `launch_configuration` and `live_processes` are saved while the game runs. Build sidecars are copied into provenance only when their binary hash matches. MPQ and engine-library hashes distinguish behavior-affecting inputs.

`durable_completion_seconds` includes replay persistence and the first durable terminal manifests. Writing that timing value itself incurs two final small JSON writes beyond the measurement. Callback timing from the diagnostic fixture excludes its periodic JSON writes; whole-process CPU and end-to-end time include them.

Run the lifecycle tests with:

```sh
python3 -m unittest tests/test_run_match.py -v
```

Those tests use a tiny explicitly test-only fake launcher to exercise successful archival, timeout, startup failure, interruption, hashes, and replay byte preservation. They do not validate OpenBW gameplay or replay parsability.

Instrumentation overrides (`DYLD_INSERT_LIBRARIES`, `ASAN_OPTIONS`, `UBSAN_OPTIONS`, `LSAN_OPTIONS`) are recorded when present, so sanitizer probes remain distinguishable from ordinary performance runs. Replay files and their archive directory are flushed before the terminal record.

Bots are named from their module filename (or explicit `--name1` / `--name2`); future replay player names include that name and race. Early historical replays contain the upstream default `bwapi`, so their identities must be resolved from the game manifest. Optional `--experiment-id` links a game to the public experiment ledger.

If the bot package has a sibling `AI/` directory, the runner copies its files into the isolated `bwapi-data/AI/`, records their hashes, and checks any `ai_files` requirements in the matching binary sidecar. Config edits after launch cannot change a running game. Fresh `read` and `write` directories remain separate.
