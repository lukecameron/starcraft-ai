# McRave ZvZ 9Pool candidate matched evaluation result

**Decision: ADOPT FOR INDEPENDENT CONFIRMATION.** The frozen treatment passed every preregistered directional and engineering guard. This advances one narrow candidate to another evaluation; it does not adopt 9Pool as production policy or establish a general strength improvement.

The treatment won 7/8 matched cells versus control's 6/8. The treatment converted both Heartbreak Ridge effective cells from losses to wins. The other two effective cells were wins in both arms, so the effective subset contained two benefits among four cells and no treatment-loss/control-win regression. There were no both-loss effective pairs, so the registered median survival-frame metric is unavailable.

## Fixed decision guards

| Guard | Observed | Result |
|---|---|---|
| All 16 attempts valid | 16/16 | pass |
| Treatment wins more cells | 7 versus 6 | pass |
| At least two effective cells | 4 | pass |
| At least half effective cells benefit | 2/4 | pass |
| No effective treatment-loss/control-win regression | 0 | pass |
| Every treatment game at least 384 durable fps | minimum 631.9 | pass |
| Treatment player-1 CPU/frame at most 110% of control | 100.43% | pass |

The control win proportion was 0.750 with descriptive Wilson 95% interval [0.409, 0.929]. Treatment was 0.875 [0.529, 0.978]. These intervals treat the eight outcomes as independent even though fixed starts and bot seeds pair the arms, so they are descriptive and do not control the decision.

## Matched outcomes

| Cell | Seed | Map | Control selection | Treatment override | Control | Treatment | Registered interpretation |
|---|---:|---|---|---|---|---|---|
| 1 | 1001 | Benzene | 9Pool | 9Pool to 9Pool | win | win | no-op, neutral |
| 2 | 1001 | Heartbreak Ridge | 9Pool | 9Pool to 9Pool | win | loss | no-op difference; outside effective regression guard |
| 3 | 6301 | Benzene | Gaspool | Gaspool to 9Pool | win | win | effective, neutral |
| 4 | 6301 | Heartbreak Ridge | Gaspool | Gaspool to 9Pool | loss | win | effective benefit |
| 5 | 1002 | Benzene | Overpool | Overpool to 9Pool | win | win | effective, neutral |
| 6 | 1002 | Heartbreak Ridge | Overpool | Overpool to 9Pool | loss | win | effective benefit |
| 7 | 8202 | Benzene | 9Pool | 9Pool to 9Pool | win | win | no-op, neutral |
| 8 | 8202 | Heartbreak Ridge | 9Pool | 9Pool to 9Pool | win | win | no-op, neutral |

Cell 2 is important contrary evidence: two source-equivalent 9Pool arms with the same engine seed, bot seed, map and slot produced different outcomes. The treatment's extra log and idempotent setter should not alter policy, but this engine setup has previously shown that fixed seeds do not guarantee identical trajectories. The two effective Heartbreak flips therefore satisfy the registered directional bar but are not sufficient causal evidence for production adoption.

## Integrity and engineering evidence

The serial executor session `5362` exited zero and durably recorded every attempt in `artifacts/experiments/mcrave-zvz-9pool-candidate-v1/execution-ledger.json` (SHA-256 `f2be448665b0040e98a99a0cf70b08186fe7def7e3052dec8e30bf449c9757f9`). Every game had two zero launcher return codes, opposing Boolean terminal results, and no `insync_hash_mismatch`. All 16 showed the ordinary terminal diagnostic pattern: winner-side `controller_not_occupied_after_action` after action 87 and loser-side `transport_callback`. No crash, timeout, contradictory outcome, or stop-rule event occurred.

All 32 replay copies match their manifest hashes, parse structurally with screp 1.13.4, contain two Zerg players, and end one frame before the owning terminal callback. The retained parser ledger is `artifacts/experiments/mcrave-zvz-9pool-candidate-v1/replay-validation.json` (SHA-256 `f0d0b71fc3cb6f7b50e27636b78da7b014cd21b85eea2377176dfb2e97c5cd1c`). This validates hashes and headers, not deterministic playback.

Control player-1 launchers used 134.133 CPU seconds over 105,269 logical frames, or 0.00127419 seconds/frame. Treatment used 141.448 seconds over 110,539 frames, or 0.00127962 seconds/frame, a 0.43% increase. Peak sampled player-1 RSS was 488,914,944 bytes for control and 490,553,344 bytes for treatment. These measurements include each player's OpenBW engine and loaded bot module; match duration and policy trajectory affect them.

The derived calculation ledger is `artifacts/experiments/mcrave-zvz-9pool-candidate-v1/analysis.json`. The treatment module is `fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa`; its full patch is `f4a4d92df63ecf5cea055bf9edaa8eee8076819b68dbb46866eb9efaffa90650`, and the one-variable incremental diff is `bf8f5cef78ff7dc4c431b7758e3555d2cf3e1a55ed7a70dbf618f7b48a6d18f7`.

## Required confirmation

The next evaluation should use independent bot and engine seeds, include both maps plus at least one additional ZvZ map, and retain unmodified learning as the control. It should focus on cases whose control selects Gaspool or Overpool and include enough no-op 9Pool controls to estimate trajectory noise. The result should require a treatment advantage larger than the observed no-op disagreement and should add at least one independent ZvZ opponent before any production decision.
