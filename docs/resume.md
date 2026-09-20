# Resume

Checkpoint: 2026-09-20, initial engine milestone.

- **Best validated competitive build:** none. `build/bots/WorkerRush.dylib` and `Idle.dylib` are original diagnostic fixtures only.
- **Working command:** README diagnostic command. Requires local socket permission in this agent sandbox.
- **Evidence:** `artifacts/runs/20260920T015245-8d1cc76f5e12/` and updated-harness run `20260920T015722-17e3dc11ff1d/`. Each records module/map hashes, logs, callback results and archived replays. Game data remains local under `third_party/game-data/`.
- **Parallel work at checkpoint:** Sol `harness_sol` ports McRave; Sol `engine_sol` ports ZZZKBot; Luna `wiki_luna` independently parses the archived replay. Each tracks its own bounded process/session and logs. Do not start conflicting edits while those tasks are active.
- **Next decision:** assess ported bots' actual gameplay and cost, then choose the first reusable candidate. Current McRave requires author permission before derivative submission under SSCAIT's recent-update clause; development and local benchmarking can proceed. No public contact or submission authorized.
- **Remaining evaluation gaps:** diverse runnable anchors, representative late-game performance, controlled seeds/starts, compact scheduling/rating uncertainty, official Win32 linking and runtime validation.

Read `docs/experiments.md`, `docs/compatibility-debt.md` and `config/opponents.json` before making strength claims or starting more simulations.
