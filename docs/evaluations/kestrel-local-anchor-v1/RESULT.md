# Kestrel v13 local-anchor result

- Registered plan: `EVAL_PLAN.md`, SHA-256 `cd78a408a2f7af14cb5db84b0f7877c71929779c1c608da9110e03c12c43d551`.
- Frozen schedule: `schedule.json`, SHA-256 `3b8a15f3b7876b072f4483e77d09318f03cbd7cd51361be28f9afcb0ea3293c5`.
- Decision: **ADOPT for the reviewed local rating cohort**. This accepts the evidence into the dashboard's current-engine local league; it does not promote a bot or claim tournament strength.

All 12 preregistered attempts completed validly. Every game had opposing terminal callbacks, zero launcher exits, LF3, matching replay hashes and frames for both player copies, full replay parsing, and the frozen Kestrel v13, opponent, engine, game-data, map and seed identities. No retries or replacements were used.

Kestrel v13 scored **2–4 against UAlbertaBot-Terran** and **0–6 against ZZZKBot**, for **2–10 overall**. The Gaussian-prior Bradley–Terry fit (400 Elo prior SD, Laplace interval) places Kestrel at **497.9 [−26.2, 1021.9]** relative to the arbitrary ZZZKBot coordinate of 1000. UAlbertaBot-Terran is **629.7 [53.4, 1206.0]** in the same three-node component. The interval is wide because this is a 12-game Apple Silicon current-engine sample across three maps and two starting slots; map, matchup and tournament effects are not fitted.

Evidence runs:

- `20260920T090951-c88cf9575e7e`, `20260920T090956-5c28c97d0bee`
- `20260920T091003-d72bf34dde21`, `20260920T091007-f4716b7f1810`
- `20260920T091023-1e353369fe35`, `20260920T091029-320b6abfb58d`
- `20260920T091034-2ef465abd7c7`, `20260920T091036-f0d5e2e90f87`
- `20260920T091038-d157800d41e2`, `20260920T091040-29e80df3a9e1`
- `20260920T091041-1f8ba26a1a2a`, `20260920T091043-37c859020c1e`

The full ledger is retained at `artifacts/experiments/kestrel-local-anchor-v1/paired-ledger.json`; all run artifacts remain local and ignored by Git.
