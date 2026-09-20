# Match records

`scripts/run_match.py` launches exactly two native BWAPILauncher processes for one OpenBW match. Each player gets an isolated working directory and private `bwapi-data/read` and `bwapi-data/write` state. Both processes share one unique `OPENBW_LOCAL_AUTO_DIRECTORY`; game assets are symlinked from the supplied game-data directory.

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

The game-data directory must contain the exact OpenBW filenames `Patch_rt.mpq`, `StarDat.mpq`, and `BrooDat.mpq`, plus the configured map. The launcher runs with the UI disabled, LAN automation, and `LOCAL_AUTO` transport. Source inspection verified that `OpenBWData/BW/BWData.cpp` resets the multiplayer latency to 3 logical frames on every map load and `Game::getLatencyFrames()` returns that value directly; no configuration override was found. This matches the project's LF3 convention. Runtime confirmation from the diagnostic module remains pending. With no UI, OpenBW's frame loop does not sleep; game-speed configuration affects only the UI branch.

Every invocation first writes `artifacts/runs/<run-id>/game-0001/manifest.json` with status `launching`, updates it to `running`, then replaces it atomically with a terminal record. A copy at `artifacts/runs/<run-id>/manifest.json` supports run-level discovery. Terminal records survive normal failure, wall timeout, SIGINT, and SIGTERM. They include exact command and relevant environment, input SHA-256 hashes, child return codes, logs, resource measurements, and replay archival records. Per-player CPU and peak RSS cover that player's BWAPILauncher process, including its OpenBW engine and loaded module. End-to-end elapsed time covers harness setup through replay archival and terminal-manifest preparation; filesystem durability is completed immediately afterward.

The harness first looks for the test/integration hook `MATCH_RESULT_PATH`, then for the tournament-compatible `bwapi-data/write/diagnostic.json`. A bot may write a JSON object there from its actual game callbacks, for example `{"winner": true, "frame_count": 12345, "ended": true, "latency_frames": 3}`. The harness preserves that object without inferring missing fields. It also inventories and hashes every regular file in the player's write-state directory. Until a bot emits metadata, result and logical-frame fields remain null. A zero launcher return code is not treated as proof of a healthy game; stderr is retained and marked because BWAPILauncher catches some startup errors. A match without an archived replay is terminally recorded as failed rather than silently accepted as complete.

Every `.rep` actually emitted anywhere in a player's isolated directory is copied byte-for-byte to `artifacts/replays/YYYY/MM/DD/<run-id>/`, fsynced, and recorded with size and SHA-256. The harness never manufactures a replay, result, adjudicated outcome, or rating. When no replay exists, the manifest records a reason and keeps both players' logs. Failed and interrupted games remain first-class records.

Run the lifecycle tests with:

```sh
python3 -m unittest tests/test_run_match.py -v
```

Those tests use a tiny explicitly test-only fake launcher to exercise successful archival, timeout, startup failure, interruption, hashes, and replay byte preservation. They do not validate OpenBW gameplay or replay parsability.
