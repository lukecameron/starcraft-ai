# Quick evaluation batch

`scripts/run_batch.py` is a small coordinator around `scripts/run_match.py`. It persists the complete schedule before launching a game, runs at most two independent games concurrently, and atomically rewrites `artifacts/experiments/<experiment-id>/manifest.json` whenever a game starts or finishes. Each single-game archive remains authoritative for commands, environment, resource measurements, telemetry, logs, and replay hashes.

The first schedule is `config/quick-schedule.json`. It preregisters ten games: four against ZZZKBot Zerg, three against UAlbertaBot Protoss, and three against UAlbertaBot Terran. Benzene and Destination each appear five times. McRave launches as player 1 five times and player 2 five times. The candidate and opponent SHA-256 values identify frozen binaries before any process starts. Scenario seeds are paired where direct launch-order comparisons are useful; their meaning depends on the engine contract recorded by each game manifest.

Run only after the controlled-seed engine and all frozen modules are available:

```sh
python3 scripts/run_batch.py \
  --schedule config/quick-schedule.json \
  --candidate artifacts/builds/c49ee3c4b20a2772f1bfca03249c182d32a7238f9453a7a568990a188a1c4c65/McRave.dylib \
  --concurrency 2
```

Each game has a 120-second wall limit inside `run_match.py`. Interrupting the batch stops the exact active runner process groups and leaves the experiment ledger and every completed or failed game archive in place.

Only games with a completed, verified outcome, zero child return codes, and boolean opposing result metadata enter wins and losses. Crashes, timeouts, launcher failures, and missing or inconsistent metadata remain separate counts. Two consecutive infrastructure failures stop new launches; games already running are allowed to archive their results. For each opponent the ledger reports the observed win rate, a 95% Wilson interval, relative Elo advantage `400 log10(p/(1-p))`, and the corresponding transformed Wilson interval. Zero and one produce explicit negative and positive infinity because this ten-game batch cannot estimate finite point-estimate endpoints. Relative Elo is reported per opponent only. The pooled cohort win rate is descriptive and has no aggregate Elo because the opponents are heterogeneous and uncalibrated. The intervals are nominal conditional summaries: paired seeds and starts improve comparison control but make an independence assumption questionable at this sample size.

Each game record links the authoritative match manifest and copies its end-to-end elapsed time, durable completion time, logical frame throughput, and whole-process peak RSS per player. The experiment ledger reports total batch wall time, which includes runner startup and incremental archival.

After a successfully completed schedule, the configured `scripts/publish_dashboard.sh` hook runs with `EXPERIMENT_MANIFEST` pointing at the finalized ledger. Its output and return code are recorded separately in `runner-logs/publish-hook.log`; publication failure does not change match results or the experiment status.

The batch is a short compatibility and behavior loop. Compilation and game generation performed before the batch are not included in its game timing, and ten openings on two maps are not a representative strength suite. The preregistered decision is to investigate any failure and collect a larger comparison. This baseline follows a crash fix, so its results do not measure a strategic gain.
