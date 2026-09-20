# StarCraft AI

Native OpenBW development and evaluation for a competitive Brood War bot. The [project brief](bwapi-autonomous-project-brief.md) defines the goal and constraints.

## Current state

Native ARM64 OpenBW runs unattended games with our ports of McRave, ZZZKBot and UAlbertaBot. The first controlled ten-game cross-race batch completed seven games cleanly, with one peer engine shutdown crash and two timeouts. Its operational-reference decision is [inconclusive](docs/evaluations/quick-baseline-v1/RESULT.md); clean-game throughput averaged 380.5 frames/s, below the 384 frames/s target. There is no calibrated Elo, measured strategic improvement, or tournament-ready package yet.

The [progress dashboard](https://starcraft-ai.pages.dev/) publishes experiments, hypotheses, conclusions, provenance and replay downloads. Replay links use the [dgant OpenBW viewer](https://dgant.github.io/openbw-replay-viewer/).

- [Engine build, game data and replay checks](docs/engine-spike.md)
- [Match runner and durable records](docs/match-records.md)
- [Environment](docs/environment.md), [competition requirements](docs/compliance.md), [official-game compatibility](docs/compatibility-debt.md)
- [Opponent source/rating manifest](config/opponents.json), [research inventory](docs/research/wiki-inventory.md), [decisions](docs/decisions.md)
- [Current reference build](config/baseline.json), [performance evidence](docs/performance.md), [resume state](docs/resume.md)

## Build and run the native ports

Follow the [engine setup](docs/engine-spike.md) first, including the local game-data layout. The current McRave source includes an optimization candidate under evaluation; the frozen reference in `config/baseline.json` remains separate. Clone the bot and official-header dependencies at their pinned revisions:

```sh
git clone https://github.com/Cmccrave/McRave.git third_party/mcrave
git -C third_party/mcrave checkout 7d1719a22d8b896f957abae50e2ea5efff974fe2
git clone https://github.com/chriscoxe/ZZZKBot.git third_party/zzzkbot
git -C third_party/zzzkbot checkout 7183e37b6b416ea53c1040c83e639a3a3c395eed
git clone --branch v4.4.0 https://github.com/bwapi/bwapi.git third_party/bwapi-official
git -C third_party/bwapi-official checkout 7687da8abc4726f8366401f11ab648d421385793
scripts/build_mcrave.sh
scripts/build_zzzkbot.sh
python3 scripts/run_match.py \
  --launcher third_party/bwapi/build-arm64/bin/BWAPILauncher \
  --library-path third_party/bwapi/build-arm64/lib \
  --bot1 build/zzzkbot/lib/ZZZKBot.dylib --race1 Zerg \
  --bot2 build/mcrave/McRave.dylib --race2 Zerg \
  --game-data-dir third_party/game-data/runtime \
  --map 'sscai/(2)Benzene.scx' \
  --purpose 'native bot baseline check' --wall-timeout 120
```

The [McRave port](docs/mcrave-port.md) also compiles all 114 translation units against official BWAPI 4.4.0 headers. The [ZZZKBot port](docs/zzzkbot-port.md) preserves its policy and documents one unsupported diagnostic API call. Build scripts apply saved patches; downloaded source and binaries remain local. McRave is a provisional development reference: a derivative submission needs author permission under SSCAIT's recent-update rule.

## Run the diagnostic

Follow the engine document to clone pinned sources, install the project-local build tools and source the MPQs/maps. Then:

```sh
scripts/engine-build.sh
scripts/build_diagnostics.sh
python3 scripts/run_match.py \
  --launcher third_party/bwapi/build-arm64/bin/BWAPILauncher \
  --library-path third_party/bwapi/build-arm64/lib \
  --bot1 build/bots/WorkerRush.dylib --race1 Protoss \
  --bot2 build/bots/Idle.dylib --race2 Protoss \
  --game-data-dir third_party/game-data/runtime \
  --map 'sscai/(2)Benzene.scx' \
  --purpose 'complete diagnostic game and replay archival' \
  --wall-timeout 120
```

On a restricted macOS agent host, Unix-domain socket creation requires an approved unsandboxed run. A sandboxed failure remains recorded. Source, downloaded dependencies, game assets and bulk run artifacts are separate: `third_party/`, `.tools/`, `build/`, `data/` and `artifacts/` are ignored by Git.

Run archival lifecycle checks with `python3 -m unittest discover -s tests -v`. These use explicit test-only subprocesses; they do not substitute for real engine matches.

## Next milestone

Repair the reproduced engine shutdown lifetime error and profile the slow cross-race scenarios. Controlled seeds, packaged Terran/Protoss opponents, and the first ten-game evaluation are available. Expand representative performance and replay synchronization checks, then restore the Win32 runtime lane. An apparent gain must beat a matched incumbent and survive held-out validation before promotion.
