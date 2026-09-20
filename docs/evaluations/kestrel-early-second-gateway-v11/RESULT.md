# Kestrel v11 early second-Gateway result

**Decision: REJECT. The second Gateway started earlier, but it completed after the first home threat in both games. Only one completed Zealot was present in the registered overlap window, below the threshold of two, and both games failed the production/lifecycle guard.**

The fixed two-game schedule ran once under session `52986`. Both games completed with both launchers returning zero, reciprocal winner callbacks, no state-hash mismatch, two `screp`-parseable replay copies, and zero rejected commands. Kestrel lost both games. No trial was excluded.

## Registered decision

The primary metric was:

```text
min(max_home_zealots_before_first_loss across both games)
```

The observed values were `min(1, 1) = 1` completed Zealot within the 12-tile home radius after the first home threat and before the first Zealot loss. The adoption threshold was at least `2` in both games. The primary bar therefore failed.

| Row | Run | Gateways current | Gateways complete | First home threat / attackers | Zealot trains | Home overlap before first loss | First Zealot loss | Max Zealots | Local terminal |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| Benzene 6103 | `20260920T071134-0c1c99b3cdfb` | 2,394 / 2,904 | 3,365 / 3,875 | 3,704 / 1 | 3,396 | 1 | 4,244 | 1 | 6,296 |
| Heartbreak Ridge 6104 | `20260920T071137-c12df661de50` | 2,154 / 2,894 | 3,125 / 3,865 | 3,590 / 1 | 3,144 / 3,762 / 4,122 | 1 | 3,988 | 2 | 5,459 |

The mechanism guard required the second Gateway to become current by frame 3,000 and complete before the first home threat. It became current by 2,904 and 2,894, so the first half passed. It completed 171 and 275 frames after the home threat, so the completion requirement failed in both games.

Replay commands independently show Gateway build requests at frames 1,958 and 2,756 on Benzene and 2,054 and 2,762 on Heartbreak Ridge. The delay between an accepted build order and the telemetry's current-unit observation reflects worker travel and construction start. The second Gateway then needed roughly another thousand frames to finish. Moving it before gas was insufficient to make two production buildings available before pressure reached home.

The production/lifecycle guard also failed. Benzene issued only one Zealot train and reached a maximum of one current/completed Zealot. Heartbreak Ridge issued three trains but reached a maximum of two. Neither reached three current/completed Zealots or won. Both did reach two Gateways, scout, and combat, and both maintained zero command rejection.

The policy behaved as written. Benzene requested its Assimilator at frame 3,098, after the second Gateway was current, and Heartbreak Ridge requested gas at 3,752. Benzene later requested a Cybernetics Core at 4,094. These are v7's unchanged post-two-Gateway choices. Their later resource effects are descriptive because the registered failure already occurs at second-Gateway completion and local overlap.

The first own Probe losses occurred at frames 2,919 and 3,084, before home threats at 3,704 and 3,590. Their ordering again distinguishes the distant scout loss from local pressure. At the first home threat neither game had a completed Zealot. Each reached one local completed defender before its first Zealot died, but never two.

Durable throughput was 2,972.5 and 3,538.2 logical frames/s, above the 384 package-validity floor. These short instrumented games do not support a performance comparison. The two losses and terminal frames are also insufficient for a strength claim.

## Interpretation and limit

This result falsifies the narrow v11 hypothesis: changing only second-Gateway priority does not create overlapping defenders before the first defender dies. It does not prove an exhaustive cause for Kestrel's early-game weakness. The timing evidence shows that by the time one Gateway exists and the bot can fund, place, construct, and complete the second, ZZZK's pressure is already inside the registered home radius.

The next source question should concern earlier opening production timing, including the first Gateway's supply threshold and command-to-construction delay. No further policy follows automatically from two trajectories. Canonical v7 remains unchanged, and v11 is not retained for a broader strength comparison.

## Preserved evidence

- Plan: `docs/evaluations/kestrel-early-second-gateway-v11/EVAL_PLAN.md`
- Schedule and incremental manifest: `artifacts/experiments/kestrel-early-second-gateway-v11/`
- Source SHA-256: `e1cfd1c9b369a755044f4652cfbfad2d2cb4d444df0a33c2ad279375551a79b6`
- Patch SHA-256: `85d6fb714e9bdb7fe43e7c3d6bb6d03c6a9603a8264bad5ebba54ee940d995d0`
- Module SHA-256: `e997841c5f173d5218f7599ab60b9dc391335f8a45788f69df3fea3bc740f49c`
- Benzene replay SHA-256: `2beff3135f9b1d9132b1338912d2197c9fdece22bb2ac9cc1ce4d0c33ed34ded`, `278f8a10cf66c133b46ed25ea6eaabc678e5f26c8c518e1a4bdf985466bcc181`
- Heartbreak Ridge replay SHA-256: `b93539b3039319268c82314bb1083784b3e80ec13bf18abf55e2741d78c817d7`, `f04da9616574b8244185d419ce90e9a101b925e532ce80053031c87d428267a2`
