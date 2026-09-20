# Stardust native-port cohort compatibility check

Registered `2026-09-20T04:25:30.023051+00:00` before any trial. The frozen schedule is `config/quick-stardust-cohort-v1.json`.

## Question and hypothesis

Can frozen native Stardust module `b6097c9a5d972afc4d687ed51f0d001af36f50a93dc625d66eb546bd02f6080c` complete representative games against ZZZKBot Zerg and UAlbertaBot Terran through the standard BWAPI path, show plausible Protoss economy and production, and meet the existing coarse engineering throughput bar?

The hypothesis passes only if all four games complete with verified opposing results, no crash or timeout, plausible race-appropriate gameplay, at least 384 durable logical frames per wall second in every game, and at least 384 aggregate frames per durable second (`sum(logical_frame_count) / sum(durable_completion_seconds)`). A failure of any condition fails the engineering gate. Instrumented engine logging is part of the measured execution, so results characterize this frozen diagnostic package rather than an uninstrumented production engine.

## Frozen schedule and controls

The engine is the logging-only frozen package whose `libOpenBWData.dylib` SHA-256 is `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb`. Opponents are frozen ZZZKBot `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748` and UAlbertaBot `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`.

Run exactly four games, serially (`--concurrency 1`), with a 120-second cap per game:

1. Stardust player 1 versus ZZZKBot on Benzene, engine seed 5202.
2. Stardust player 2 versus ZZZKBot on Benzene, engine seed 5202.
3. Stardust player 1 versus UAlbertaBot Terran on Destination, engine seed 5301.
4. Stardust player 2 versus UAlbertaBot Terran on Destination, engine seed 5301.

Each runner invocation creates empty isolated learning directories. No bot seed is supplied because these frozen modules do not declare the runner's explicit bot-RNG control contract. Swapping player assignment checks both protocol positions; it is not a deterministic paired strength comparison.

Run with the existing batch entry point after root review and release of the compile/game window:

```sh
python3 scripts/run_batch.py \
  --schedule config/quick-stardust-cohort-v1.json \
  --candidate artifacts/builds/b6097c9a5d972afc4d687ed51f0d001af36f50a93dc625d66eb546bd02f6080c/stardust-native-arm64/Stardust.dylib \
  --concurrency 1
```

## Stopping, retention, and interpretation

Stop after the four registered games or after the existing batch rule observes two consecutive infrastructure failures. Preserve every completion, timeout, crash, inconsistent result, replay, diagnostic, and runner log. Do not retry, replace a game, or select another seed after seeing results.

For every game, inspect Stardust’s replay command stream and record separately whether it contains worker-production commands, building-production commands, and combat-unit commands. Record any idle or wrong-race anomaly. If any category is absent or the client-local replay view is ambiguous, classify compatibility as inconclusive rather than silently passing it. A clean completion also requires opposing winner callbacks, both launcher return codes zero, and no `insync_hash_mismatch` event in either client diagnostic stderr. Record the first diagnostic kill source from each client, plus per-game and aggregate durable throughput, CPU/RSS, callbacks, and outcome verification. The four matchup outcomes support only a coarse descriptive ordering within this cohort. A 0% or 100% observed score has no finite Elo estimate at this sample size; do not present an infinite value as a rating. This evaluation cannot establish an absolute BASIL rating, calibrated strength, or promotion decision.
