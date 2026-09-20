# Stardust empty-timer repair result

## Outcome: passed

The single registered probe, run `20260920T044353-8b83e0831afe`, passed every correctness condition. Both launchers returned zero, winner callbacks opposed each other, the game completed at frame 13,922, and neither client reported an in-sync hash mismatch.

The changed producer path was exercised repeatedly. It logged eight bounded `producer_recovered` events, beginning at frame 924. The defensive `consumer_fail_closed` path was never used. This shows the candidate repaired the confirmed producer invariant violation and allowed the same frozen scenario to continue through a complete game.

The player-1 replay SHA-256 is `32ca63766d702c91d66c4497ccc9f9e27812717401a8ed682869928cb13e29bd`; player 2 is `cbde289fed2a5a99cd17bc569e0999a6883e6c6f2c9182d16ca1301839995be9`. Stardust issued 36 Probe train commands, 27 building commands, and 35 combat-unit train commands covering Zealots, Dragoons, and Corsairs. The terminal diagnostic paths were the expected post-defeat `controller_not_occupied_after_action` on the survivor and transport closure on the already-ended loser.

The native and official-header builds passed. The frozen repair module SHA-256 is `1039975842c6edea71043e0da091ff21ad5311fd3ddbeb568cf89b364f7d28aa`. The full patch from pristine Stardust is [stardust-emptytimer-repair.patch](../../../patches/stardust-emptytimer-repair.patch), SHA-256 `cd3a3555459c481f5bf4b3455a8604cb4443d10ba2c68b31118f475f0d187325`. The incremental patch applied after the existing native-port patch is [stardust-emptytimer-repair.incremental.patch](../../../patches/stardust-emptytimer-repair.incremental.patch), SHA-256 `1b36295a1116658cbcea65cc817429ef2032d998077cc5b0036e4418ef39b3e5`.

This one probe supports the bounded correctness repair only. It does not establish reliability across the four-game cohort, throughput, rating, or strength.
