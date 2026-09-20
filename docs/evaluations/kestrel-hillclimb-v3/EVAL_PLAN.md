# Kestrel v23 three-local-Zealot hold refinement

Registered 2026-09-20 after the v22 five-game screen. This is an exploratory hill-climb continuation, not an Elo cohort or promotion gate.

The v22 candidate retained the public home-threat latch and two-train tech unlock. It reached three local Zealots in the Protoss and Stardust lanes, but ZZZK still ended the opening before tech and the batch produced zero wins. v23 changes only the local hold release threshold from two to three completed Zealots within 12 tiles of home. The race-general threat latch, local counting, two-train gas/Core unlock and all other behavior remain byte-identical to v22.

Run exactly five candidate games concurrently against the same frozen opponent gradient, with fresh engine seeds and no `MATCH_BOT_SEED` flags:

| Game | Opponent | Race | Map | Engine seed | Kestrel slot |
| --- | --- | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Zerg | Benzene | 9821 | P1 |
| 2 | UAlbertaBot-Terran | Terran | Destination | 9822 | P2 |
| 3 | UAlbertaBot-Protoss | Protoss | Heartbreak Ridge | 9823 | P1 |
| 4 | McRave-9Pool-treatment | Zerg | Circuit Breaker | 9824 | P2 |
| 5 | Stardust-repaired | Protoss | Benzene | 9825 | P1 |

Use a 300-second per-game cap, a 900-second cohort cap, concurrency five, and no retries or replacements. Retain every manifest, runner log and replay. Score candidate outcomes, early-threat survival, local Zealot overlap, accepted production, command rejections, descriptive replay signals and durable throughput. Shorter games remain a descriptive signal only.

A useful result is an observed survival or conversion improvement without command or integrity regressions. This run cannot update Elo or promote a production build by itself.
