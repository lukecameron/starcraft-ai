# Kestrel v22 three-change hill-climb screen

Registered 2026-09-20 after the five-game v19 replay screen. This is an exploratory improvement batch, not an Elo cohort or promotion gate. The baseline was 0/5 wins with five valid replays and zero Kestrel command rejections; one early Zerg game ended before tech, one Protoss game was threatened before the first Zealot, and the longer games reached Dragoons but still lost.

## Shortlist and implementation

The candidate combines three small changes selected from the replay evidence:

1. Apply the existing public home-threat Zealot hold to every matchup, not only known Zerg. The Protoss-pressure replay first threatened at frame 2,430 and recorded only one local defender.
2. Release the hold using the number of completed Zealots within 12 tiles of home, matching the reviewed local-overlap metric, rather than the global completed-Zealot count.
3. Against known Zerg, permit Assimilator and Cybernetics Core construction after two accepted Zealot trains instead of four, addressing the early Benzene replay's zero post-first-train structures and repeated Heartbreak production misses.

The candidate is based on the frozen v19 source and retains its lone-Zealot hold, gas-worker guard, public-observation boundary, production policy and all other behavior. The exact source, patch, compiler and binary hashes are in the build sidecar.

## Fixed next screen

Run exactly five Kestrel-v22 candidate games concurrently, one against each frozen local opponent used by the recovery baseline:

| Game | Opponent | Race | Map | Engine seed | Kestrel slot |
| --- | --- | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Zerg | Benzene | 9811 | P1 |
| 2 | UAlbertaBot-Terran | Terran | Destination | 9812 | P2 |
| 3 | UAlbertaBot-Protoss | Protoss | Heartbreak Ridge | 9813 | P1 |
| 4 | McRave-9Pool-treatment | Zerg | Circuit Breaker | 9814 | P2 |
| 5 | Stardust-repaired | Protoss | Benzene | 9815 | P1 |

The wall cap is 300 seconds per game and 900 seconds for the cohort. Unsupported `MATCH_BOT_SEED` flags are omitted. No retries or replacement attempts are allowed. Every manifest, runner log and replay is retained.

## Review rule

After completion, score the candidate-owned replay for outcome, terminal frame count, durable throughput, command rejection, local completed-Zealot overlap before first loss, accepted Zealot trains, post-first-train structures, and the existing descriptive economy/construction/production/combat signals. A shorter game is a descriptive signal only. The candidate is useful if it improves the observed early-threat/tech signals without introducing command errors or throughput failures; this screen alone cannot establish Elo or justify production promotion.
