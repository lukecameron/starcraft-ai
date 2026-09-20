# Kestrel v0 native smoke result

**Decision: compatibility gate passed; behavior gate failed. Do not use v0 as an opponent or strength baseline.**

The single registered attempt ran as `20260920T060144-b9ed2a9e5aad`. Both launcher processes exited zero, the callbacks reported opposing results, and Kestrel lost at local frame 6,885 while WorkerRush won at frame 6,916. No `insync_hash_mismatch` appeared. Both replay files were copied and `screp` parsed both successfully. This is structural parser evidence rather than deterministic replay playback.

The game completed 6,916 logical frames in 1.1478 seconds through durable archival, or 6,025.4 logical frames per wall second. Kestrel recorded 0.087341 CPU seconds across 6,886 callbacks, 0.006041 ms callback p99, and a 1.77333 ms maximum. The short worker-rush trajectory does not characterize representative late-game throughput.

The behavior gate failed. Kestrel issued 11 probe-training commands, 13 pylon build commands, 42 gateway build commands, and scouting/attack-move commands outside its starting base. It issued no zealot or dragoon training command before elimination. The replay command stream therefore shows economy, supply/build attempts, and scouting, but not a completed production-and-combat lifecycle. Repeated gateway placement commands from frame 2,438 through 3,716 also expose missing construction-order suppression while a worker is trying to reach or place a building.

The exact evidence is in `artifacts/runs/20260920T060144-b9ed2a9e5aad/game-0001/manifest.json`. The player-one replay SHA-256 is `5d81c85008b2e4b4c39e67c52ce43b42fc2c46435b721a3ceb5547a098c59626`; the player-two replay SHA-256 is `ddc9d95cd7dade9e170c509814cb94ef1a625012835c4d3a821c112e6f060225`.

The next probe should first suppress duplicate pending construction commands and use an economy-oriented opponent long enough to exercise gateway completion and combat-unit production. That source change and probe require a new build identity and preregistration; this failed result remains unchanged.
