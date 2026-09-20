# McRave Grids direct-bounds performance screen result

**REJECT.** The candidate does not advance to independent performance validation. Aggregate treatment CPU/frame was 107.43% of control, missing the required maximum of 95%. Two paired regressions also exceeded the 110% guard. All integrity, memory, and outcome guards passed, so this is a valid negative performance result rather than an inconclusive cohort.

## Fixed-gate results

| Gate | Observed | Result |
|---|---:|---|
| Aggregate treatment/control CPU/frame | 107.43% | Fail; required ≤95% |
| Worst paired treatment/control CPU/frame | 115.43% | Fail; required every pair ≤110% |
| Maximum treatment/control peak RSS | 103.34% | Pass; required ≤105% |
| McRave losses, treatment/control | 0 / 0 | Pass; treatment no worse |
| Integrity-valid attempts | 8 / 8 | Pass |

Aggregate control CPU/frame was 0.00215347 seconds and treatment was 0.00231338 seconds, calculated from summed McRave process CPU and frames exactly as registered. The four treatment/control paired CPU/frame ratios were 94.13%, 115.43%, 110.22%, and 101.53%. The small four-pair sample and substantial same-seed trajectory variation limit precision, but the preregistered aggregate and pair guards both independently reject advancement.

## Every attempt

| Attempt | Pair/arm | Map, slot | Frames | McRave CPU s/frame | Peak RSS bytes | Durable FPS | Outcome |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | 1 control | Benzene, P1 | 15,255 | 0.00219496 | 489,586,688 | 418.75 | win |
| 2 | 1 treatment | Benzene, P1 | 15,100 | 0.00206612 | 486,457,344 | 438.61 | win |
| 3 | 2 treatment | Destination, P2 | 29,174 | 0.00248040 | 507,412,480 | 362.22 | win |
| 4 | 2 control | Destination, P2 | 17,177 | 0.00214878 | 486,653,952 | 428.71 | win |
| 5 | 3 control | Benzene, P2 | 20,277 | 0.00215021 | 491,028,480 | 419.49 | win |
| 6 | 3 treatment | Benzene, P2 | 27,314 | 0.00237000 | 503,119,872 | 376.25 | win |
| 7 | 4 treatment | Destination, P1 | 17,146 | 0.00215673 | 486,817,792 | 431.33 | win |
| 8 | 4 control | Destination, P1 | 16,619 | 0.00212420 | 486,096,896 | 434.21 | win |

Attempts 3 and 6 were below the existing 384-fps floor. The overall engineering budget therefore remains unresolved, independently of the failed advancement decision. No earlier performance bar changes.

## Integrity and evidence

Runner session `66424` completed all eight attempts in 400.504 active seconds. Every launcher pair returned zero, emitted opposing terminal results with `outcome_verified: true`, and recorded only the reviewed terminal-drain kill events. All 16 replay copies matched their manifest hashes and passed full screp command-stream parsing, race checks, frame checks, and parser-error checks. There was no crash, timeout, hash mismatch, contradictory outcome, unrelated kill source, retry, replacement, or exclusion.

The durable ledger is `artifacts/experiments/mcrave-grids-bounds-performance-v1/paired-ledger.json` (SHA-256 `c55a2e49f24b2721c81ae3ea156b5f9ea30a8d0681a1ebd73331c56f0bd79880`). Derived calculations are in `analysis.json` (SHA-256 `cfcc90eb784768bada67eea9ed876348928addd6ea2cd2a1754d55111e9a3867`). The registered source schedule SHA-256 is `7635521a28f9bf963409fea5eb31c62b71aca4ee8855005923a0b2116befae8c`; the runner's normalized frozen copy is `0047cc265c5ce7255bfbb0f975f7115432f3997f3d63b2f82f4a91152f686738`.

The one-line bounds replacement remains source-equivalent in the preceding shadow, but this screen supplies no evidence that it improves end-to-end performance. It is not advanced or adopted, and no further experiment follows from this result.
