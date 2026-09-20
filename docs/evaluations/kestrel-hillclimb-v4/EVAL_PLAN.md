# Kestrel v24 shared-target focus hill-climb

Registered 2026-09-20 after v23 rejected the three-local-Zealot hold. v24 restores the v22 two-local home hold and earlier-tech policy, then changes only combat target selection: after the hold releases, completed Zealots and Dragoons share the first currently visible, detected, non-flying enemy target selected through the existing public BWAPI observation path. If that target is no longer valid, the existing per-unit selector remains the fallback.

The change targets the reviewed fight diagnostic, where the first and second Zealots reached the local fight separately, and the v23 result, where increasing the hold threshold did not rescue the early Zerg lane. It does not read hidden state, alter construction or economy, or claim a causal win from a short screen.

Run exactly five candidate games concurrently against the same frozen opponent gradient with fresh engine seeds 9831 through 9835, maps Benzene, Destination, Heartbreak Ridge, Circuit Breaker and Benzene, and Kestrel slots P1/P2/P1/P2/P1 respectively. Use a 300-second game cap and 900-second cohort cap, omit unsupported `MATCH_BOT_SEED` flags, preserve every manifest/log/replay, and do not retry or replace attempts.

Review verified outcomes, local home overlap, first threat/loss frames, production, command errors, shared-target order evidence, descriptive replay signals and durable throughput. This exploratory run cannot update Elo or promote a build.
