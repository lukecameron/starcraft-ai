# Stardust empty-timer repair cohort check

Registered `2026-09-20T04:45:44.592395+00:00` before launch. The frozen schedule is `config/stardust-repaired-cohort-v1.json`. The rejected original cohort remains unchanged.

## Question and gate

Does frozen repair module `1039975842c6edea71043e0da091ff21ad5311fd3ddbeb568cf89b364f7d28aa` complete the same four cross-race scenarios that exposed the empty-timer crash?

The gate passes only if all four games complete with zero launcher return codes, verified opposing winner callbacks, no `insync_hash_mismatch`, and replay evidence for Stardust worker production, building production, and combat-unit commands. Every game and the aggregate `sum(logical_frame_count) / sum(durable_completion_seconds)` must reach 384 durable frames/s. Any crash, timeout, inconsistent result, missing evidence category, or ambiguous replay view fails the gate.

## Frozen schedule

Run serially with a 120-second cap and empty isolated learning state:

1. Stardust player 1 versus ZZZKBot Zerg on Benzene, engine seed 5202.
2. Stardust player 2 versus ZZZKBot Zerg on Benzene, engine seed 5202.
3. Stardust player 1 versus UAlbertaBot Terran on Destination, engine seed 5301.
4. Stardust player 2 versus UAlbertaBot Terran on Destination, engine seed 5301.

The engine is frozen logging package `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb`; opponents remain ZZZKBot `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748` and UAlbertaBot `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`. No bot seed is supplied. Record every bounded `producer_recovered` line as an observed lower bound on fallback use; require zero `consumer_fail_closed` lines.

Run exactly once with publishing disabled:

```sh
python3 scripts/run_batch.py \
  --schedule config/stardust-repaired-cohort-v1.json \
  --candidate artifacts/builds/1039975842c6edea71043e0da091ff21ad5311fd3ddbeb568cf89b364f7d28aa/stardust-emptytimer-repair/Stardust.dylib \
  --concurrency 1 \
  --no-publish
```

Stop after four attempts or after the existing two-consecutive-infrastructure-failure rule. Preserve all failures; do not retry, replace, or select another seed. Results establish only bounded compatibility of this repair artifact. They do not establish a causal speed change, rating, or strength promotion.
