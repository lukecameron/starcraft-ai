# StarCraft AI

Native OpenBW development and evaluation for a competitive Brood War bot. The [project brief](bwapi-autonomous-project-brief.md) defines the goal and constraints.

## Current state

Native ARM64 OpenBW runs unattended games with our ports/forks of McRave, ZZZKBot, UAlbertaBot and Stardust, plus **Kestrel**, our independently written Protoss bot. Kestrel builds an economy and army and beats a worker-rush diagnostic, but has not yet beaten the real benchmark opponents. Version7 passed its registered command-quality checks; early-defense strategy remains under evaluation.

The [current engine](config/engine.json) fixes a reproduced terminal disconnect race that could report both players as winners. All six registered regression/control games passed, with twelve parsed replays and matching shared command histories. Use the [current-engine build instructions](docs/engine-terminal-drain.md) for new experiments; historical schedules retain their original binaries.

[Local league estimates](docs/local-ratings.md) distinguish exact bot builds and engine/settings regimes, exclude invalid games and report uncertainty. The current-engine cohort has24 valid games across four maps; the older engine retains nine valid games out of twelve separately. Intervals remain wide. These estimates are not BASIL ratings. No strategic improvement or tournament-ready package is claimed yet.

The [progress dashboard](https://starcraft-ai.pages.dev/) publishes experiments, hypotheses, conclusions, provenance and replay downloads. Replay links use the [dgant OpenBW viewer](https://dgant.github.io/openbw-replay-viewer/).

- [Current engine and regression evidence](docs/engine-terminal-drain.md), [initial setup and game data](docs/engine-spike.md)
- [Kestrel original bot and build history](docs/kestrel-bot.md), [local rating methodology](docs/local-ratings.md)
- [Match runner and durable records](docs/match-records.md)
- [Environment](docs/environment.md), [competition requirements](docs/compliance.md), [official-game compatibility](docs/compatibility-debt.md)
- [Opponent source/rating manifest](config/opponents.json), [research inventory](docs/research/wiki-inventory.md), [decisions](docs/decisions.md)
- [Current reference build](config/baseline.json), [performance evidence](docs/performance.md), [resume state](docs/resume.md)

## Build and run the native ports

Follow the [engine setup](docs/engine-spike.md) for game data, then the [current-engine build](docs/engine-terminal-drain.md). The current McRave source includes an optimization candidate under evaluation; the frozen reference in `config/baseline.json` remains separate. Clone the bot and official-header dependencies at their pinned revisions:

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
  --launcher third_party/bwapi-terminal-drain/build-arm64/bin/BWAPILauncher \
  --library-path third_party/bwapi-terminal-drain/build-arm64/lib \
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

Collect a fresh connected rating cohort on the repaired engine, improve Kestrel’s early defense, and test McRave’s path-search optimization against the fixed ten-game performance gate. Keep command quality separate from strategic strength. Expand held-out maps and seeds, then restore the Win32 runtime lane. An apparent gain must beat a matched incumbent and survive held-out validation before promotion.
