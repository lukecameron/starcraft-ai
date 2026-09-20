# Kestrel v31 early-Zerg squad-staging recovery

Registered 2026-09-20 after `kestrel-hillclimb-v10` launched in a restricted execution context where all ten launchers failed to connect to their per-game Unix-domain transports. Those attempts are preserved as infrastructure failures with null logical frame counts, no terminal metadata and no replays.

This recovery uses the exact hypothesis, candidate, policy, telemetry, mechanism gates, integrity gates, regression gates and advancement rule in [`../kestrel-hillclimb-v10/EVAL_PLAN.md`](../kestrel-hillclimb-v10/EVAL_PLAN.md). It runs outside the restricted socket sandbox. It remains an exploratory screen and cannot update Elo or replace canonical Kestrel v13.

## Recovery invariants

- Candidate remains Kestrel v31 binary `5ff164dc9dfd5c555837f110002f3907838891c6fdc95a8960cc48f12e47e107`, source `347414e122c0b59311588a50e4c003a03b6dd61fb4081b1e01b0a750cc0de928`, Protoss, Ours/Original.
- Engine remains `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Five games run concurrently with 300-second per-game caps and a 900-second cohort cap.
- The five maps, opponents, player slots and engine seeds are identical to v10: 9901 through 9905. No replacement, reseeding or unsupported `MATCH_BOT_SEED` flag is used.
- Every manifest, log, diagnostic and replay is retained. Candidate-owned replays are scored only after integrity review.
