# Kestrel v13 local-anchor repeat result

- Registered plan: `EVAL_PLAN.md`, SHA-256 `00a8dcf9c2afa08f13cbf7f5405e4a41d72e0849d4d5f62ee35a26f2969d5806`.
- Frozen schedule: `schedule.json`, SHA-256 `cbb9ff46ce5dd389b78306b64d0686c78b33165465f174639829763ea42d7c5f`.
- Decision: **INCONCLUSIVE**. The registered stop rule halted the repeat after one consecutive invalid attempt; no retry or replacement was used, and no result entered the local Elo cohort.

Attempt 1 (`20260920T091629-94ed2c02ee7a`) completed validly with both replay copies parsed and hashes verified. Attempt 2 (`20260920T091639-16fed6a67ab7`) stopped before a verified terminal result: the runner returned 1, emitted no replay copies, and recorded `outcome_not_verified`, `replay_count_not_two`, `status_not_completed` and `terminal_results_not_opposing`. The invalid attempt is preserved in the ledger and run artifacts.

This does not change the v1 anchor or Kestrel's rating. The preserved attempt-1 replay remains visible in the dashboard as an experimental run, while the repeat stays out of `config/local-ratings.json` until a separately preregistered valid cohort is completed.

Full ledger: `artifacts/experiments/kestrel-local-anchor-v2/paired-ledger.json`.
