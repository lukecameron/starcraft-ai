# Kestrel v5 loss analysis

This is a replay and source review of the two registered v5 losses. It does not evaluate the current v6 source and does not treat either game as a strength estimate.

## What the replays show

The ZZZK game was run `20260920T062152-c192464ca3eb` on Benzene. Kestrel was player 0 and ended at frame 6482. Its diagnostic recorded 124 attempted commands and 54 rejected commands (43.5%), with maxima of 15 probes, 2 pylons, 2 gateways, 3 zealots, and 0 dragoons. The parsed accepted command stream places Kestrel's first Pylon at frame 998, first Gateway at 2006, second Gateway at 2246, Assimilator at 2576, and first Zealot train at 3404. ZZZK's Spawning Pool was placed at 845; its Zerglings morphed at 2087, 2089, 2427, 2429, 2769, 2771, 3105, and 3107. Kestrel therefore had no recorded combat unit before the first four Zergling pairs had entered the stream, and it never recorded a Dragoon.

The UAlberta game was run `20260920T062203-44a429a08fed` on Destination. Kestrel was player 1 and ended at frame 16371. Its diagnostic recorded 841 attempted commands and 357 rejected commands (42.4%), with maxima of 28 probes, 5 pylons, 4 gateways, 3 zealots, and 7 dragoons. Its first Pylon, Gateway, Assimilator, and Cybernetics Core build commands were at frames 1022, 2060, 2696, and 4208; the first Dragoon trains were at 5630 and 5630. UAlberta's first Barracks command was at 2250 and its first Marine train at 3858. Kestrel eventually produced a larger army here, but the replay still records the loss.

These are accepted replay commands and timing facts. The diagnostic counter is only an aggregate: v5's `issue()` increments `commands_` and `rejected_` from the BWAPI boolean return but does not record a rejection reason or frame. The replay cannot prove that a particular missing building or unit was caused by a rejected command. The command rejection problem is real at the aggregate level, while the opening delay is an accepted-behavior observation.

## Earliest actionable weakness

Against ZZZK, the earliest clear weakness is the opening's combat timing and worker-defense posture. `Kestrel.cpp` v5 trains from completed Gateways only when the periodic `trainUnits()` pass sees sufficient minerals, while `constructOpening()` queues a second Gateway at supply 26 and then prioritizes the Assimilator. The accepted stream shows the consequence: a Pool-first Zerg reaches repeated Zergling morphs before Kestrel has a Zealot, and the only early attack commands are scout-style target orders before the first Zealot. This supports an opening-response hypothesis; it does not show an illegal command or prove that the Zerglings caused the final loss.

The UAlberta replay is consistent with the same policy risk at a different scale: the Core and first Dragoons arrive late relative to the Terran production ramp, while the aggregate rejection rate remains high. Its longer trajectory and different map/opponent mean it should not be merged with the ZZZK timing as one measured effect.

## One follow-up hypothesis

For a new preregistered probe, hold the v5 engine, maps, opponent revisions, and seeds fixed and instrument the first completed combat unit, first enemy contact, first worker-defense command, and every `issue()` rejection with command category and frame. Compare the existing opening with one narrowly defined early-defense policy that reserves the first Gateway for a Zealot before adding the second Gateway or Assimilator when an early Zerg threat is visible. The hypothesis is that this reduces the ZZZK loss's pre-combat exposure and rejected attack churn without reducing the UAlberta game's eventual production; it should be accepted only on per-opponent command/replay gates, not on this two-game outcome alone.
