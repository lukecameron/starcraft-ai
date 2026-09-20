# StarCraft AI

Native OpenBW development and evaluation for a competitive Brood War bot. The [project brief](bwapi-autonomous-project-brief.md) defines the goal and constraints.

## Current state

Native ARM64 OpenBW builds and completes an unattended two-player diagnostic match. WorkerRush versus Idle on Benzene finished in 1.54 seconds with two emitted replays. This is a runtime fixture, not a competitive baseline. There is no validated candidate, local Elo estimate, or tournament-ready package yet.

- [Engine build, game data and replay checks](docs/engine-spike.md)
- [Match runner and durable records](docs/match-records.md)
- [Environment](docs/environment.md), [competition requirements](docs/compliance.md), [official-game compatibility](docs/compatibility-debt.md)
- [Opponent source/rating manifest](config/opponents.json), [research inventory](docs/research/wiki-inventory.md), [decisions](docs/decisions.md)

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

Validate native McRave and a diverse opponent cohort, including cheap low-rated anchors; verify replay playback and complete-match performance; then run a compact calibration before assigning any local strength bracket. An apparent gain must beat a matched incumbent and survive held-out validation before promotion.
