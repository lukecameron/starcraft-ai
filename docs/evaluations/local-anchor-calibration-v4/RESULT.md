# Current-engine local anchor calibration v4 result

**INCLUDE proposed, pending lead registry review.** All 12 registered games completed cleanly and satisfy the preregistered evidence-inclusion rule. The cohort adds six direct UAlberta Protoss–ZZZK games and six UAlberta Protoss–Terran games without changing binaries, engine, learning state, timeout, or rating method.

## Direct evidence

UAlberta Protoss beat UAlberta Terran 5–1. It won both Benzene slots, split the Heartbreak Ridge slots, and won both Destination slots. ZZZK beat UAlberta Protoss 5–1; the UAlberta win was the player-2 Benzene game. The slot-balanced map cells remain correlated observations rather than twelve independent draws.

| Attempts | Edge and cell | UAlberta Protoss results | Durable FPS |
|---|---|---|---|
| 1–2 | vs Terran, Benzene 9401, P1/P2 | win, win | 2387.1, 2736.2 |
| 3–4 | vs ZZZK, Destination 9404, P1/P2 | loss, loss | 2942.8, 2791.3 |
| 5–6 | vs Terran, Heartbreak Ridge 9402, P1/P2 | win, loss | 2807.4, 1768.6 |
| 7–8 | vs ZZZK, Circuit Breaker 9405, P1/P2 | loss, loss | 2589.2, 2931.1 |
| 9–10 | vs Terran, Destination 9403, P1/P2 | win, win | 3290.4, 1944.8 |
| 11–12 | vs ZZZK, Benzene 9406, P1/P2 | loss, win | 3101.0, 3076.5 |

Timing is descriptive only. No throughput or resource threshold was registered.

## Unchanged-model calculation

The table applies the existing Gaussian-prior Bradley–Terry MAP, 400 Elo prior SD and approximate 95% Laplace contrasts. The after column pools the proposed 12 games with the 36 reviewed v2/v3 games. ZZZK 1000 remains an arbitrary coordinate.

| Exact node | Before W–L, estimate (95% interval) | After W–L, estimate (95% interval) | After prior SD 200 / 800 |
|---|---|---|---|
| Stardust Protoss `1039975842c6` | 16–0, 1426.8 (994.8–1858.9) | 16–0, 1453.6 (1025.7–1881.5) | 1282.7 / 1645.1 |
| ZZZKBot Zerg `ce796a5d49d7` | 7–5, 1000.0 | 12–6, 1000.0 | 1000.0 / 1000.0 |
| McRave Zerg `04521befa41b` | 8–12, 836.8 (536.4–1137.1) | 8–12, 872.0 (605.6–1138.5) | 891.3 / 861.9 |
| UAlbertaBot Protoss `75ac4f6bb44e` | 2–10, 535.3 (139.2–931.5) | 8–16, 669.1 (396.2–942.0) | 746.5 / 630.3 |
| UAlbertaBot Terran `75ac4f6bb44e` | 3–9, 579.6 (220.3–938.9) | 4–14, 562.1 (266.6–857.5) | 660.1 / 515.2 |

The new missing reference edge and additional close-node games reduce some conditional intervals, but estimates remain wide and prior-sensitive. The scalar model does not fit map, slot, matchup style, or dependence between paired cells. These values are uncalibrated local coordinates, not BASIL ratings or tournament predictions.

## Integrity and proposed inclusion

Runner session `72978`, PID `96809`, completed all attempts in 46.273 active seconds. Every game had two zero child return codes, opposing terminal metadata, `outcome_verified: true`, and only the reviewed terminal-drain diagnostics. All 24 replay copies match their manifest hashes and passed full screp command-stream parsing, expected-race checks, owner-frame checks, and parser-error checks. There was no crash, timeout, hash mismatch, contradictory outcome, unrelated kill source, retry, replacement, or exclusion.

The durable ledger is `artifacts/experiments/local-anchor-calibration-v4/paired-ledger.json` (SHA-256 `04cfc4d3ccca6f3bf0479b808ca1e71c244f31181a80931c56d6dea18abf7724`). Calculations are in `analysis.json` (SHA-256 `0b0e19828e335728284b17598676ec2bb23f66078f2c55815209b7707ad46c6d`). The proposed run-to-manifest-hash map is [PROPOSED_INCLUSION.json](PROPOSED_INCLUSION.json) (SHA-256 `5dc70df68cda4d0582cb78f0f0666348d0c0b4a938a9648ae9171e0e6bff80dd`). The lead must still pin those hashes and add the experiment/cohort to `config/local-ratings.json`; this result does not edit that registry.

Inclusion extends the existing exact-build local display only. It does not promote a bot or authorize another experiment.

Lead decision: ADOPT for display evidence. The lead verified all twelve final manifest hashes, reciprocal outcomes, and all twenty-four replay hashes, pinned the proposed set in `config/local-ratings.json`, and recomputed the unchanged model. The extension joins the existing current component with five nodes and 48 games; its own coverage is three nodes and twelve games. No bot promotion follows.
