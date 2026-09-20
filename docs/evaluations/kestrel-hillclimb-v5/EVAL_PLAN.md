# Kestrel v25 combat-target priority hill-climb

Registered 2026-09-20 after v24 rejected shared-target focus. v25 restores the v22 two-local home hold and two-train tech policy and changes only `visibleEnemyTarget`: among currently visible, detected, non-flying enemy units, units whose public type can attack are preferred, with distance breaking ties. The old nearest-target fallback remains for a combat-free visible set.

This tests the replay diagnosis that early defenders may spend attack orders on workers or other noncombat targets while hostile combat units remain. It uses only public BWAPI observations and does not change construction, economy, or hidden-state access.

Run exactly five candidate games concurrently against ZZZKBot on Benzene, UAlbertaBot-Terran on Destination, UAlbertaBot-Protoss on Heartbreak Ridge, McRave-9Pool-treatment on Circuit Breaker, and Stardust-repaired on Benzene, with fresh engine seeds 9841 through 9845 and Kestrel slots P1/P2/P1/P2/P1. Use a 300-second game cap and 900-second cohort cap, omit unsupported bot-seed flags, preserve every manifest/log/replay, and do not retry or replace attempts.

Review verified outcomes, early-threat and first-loss frames, local Zealot overlap, production, command errors, target-order evidence, descriptive replay signals and durable throughput. This exploratory screen cannot update Elo or promote a build.
