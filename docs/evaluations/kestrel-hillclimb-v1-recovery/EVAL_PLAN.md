# Kestrel replay hill-climb baseline recovery

Registered 2026-09-20 after `kestrel-hillclimb-v1` stopped at launcher preflight. Its five attempts are preserved as infrastructure failures with no game, replay or outcome. The frozen v19 Kestrel sidecar does not declare `MATCH_BOT_SEED`, so the recovery keeps the same matrix and engine seeds while omitting unsupported per-bot seed flags.

This recovery uses the objective, scorecard and decision rule in [`../kestrel-hillclimb-v1/EVAL_PLAN.md`](../kestrel-hillclimb-v1/EVAL_PLAN.md). It is still an exploratory screen, not an Elo cohort or promotion gate.

## Recovery invariants

- Candidate remains Kestrel v19 binary `f02db8b97e01482f897a0f481c11a92f0cd5bc21f4629abea1f5a6d113b44b9a`, Protoss, Ours/Original.
- Engine remains `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Five games run concurrently with 300-second per-game caps and a 900-second cohort cap.
- The five maps, opponents, player slots and engine seeds are identical to v1: 9801 through 9805. No replacement, reseeding or unsupported `MATCH_BOT_SEED` flag is used.
- Every manifest and replay is retained. Candidate-owned replays are scored with `scripts/score_kestrel_hillclimb.py` after completion.
