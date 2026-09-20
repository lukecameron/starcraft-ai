# Kestrel v10 Zerg-defense production result

**Decision: reject v10. Delaying technology advanced all three Zealot requests and produced clean command behavior, but it did not reach a fourth train, missed the registered third-Zealot timing threshold, and failed lifecycle in both games. Keep v7 as the baseline.**

Both fixed candidate games completed with zero launcher exits, opposing winner callbacks, no state-hash mismatch, two `screp`-parseable replay copies, and zero rejected commands. Kestrel lost both games.

| Row | Run | Zealot train frames | Max Zealots | Gas / Core request | Home threat | First worker loss | Local terminal | Durable frames/s |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| Cached v7, Benzene 6103 | `20260920T063735-568f09f7d3a0` | 3,416 / 4,082 / 4,226 | 3 | gas 2,528 / no Core | not instrumented | not instrumented | 6,327 | 2,943.6 |
| V10, Benzene 6103 | `20260920T065835-c63b3213ff8c` | 3,056 / 3,854 / 4,094 | 2 | none / none | 3,713 | 2,918 | 5,893 | 2,894.4 |
| V10, Heartbreak Ridge 6105 | `20260920T065837-abeb0ce86bea` | 3,170 / 4,040 / 4,040 | 2 | none / none | 3,586 | 4,233 | 5,769 | 3,392.6 |

The mechanism itself behaved consistently. Neither candidate game requested an Assimilator or Cybernetics Core before terminal defeat. Each built two Gateways, continued Probe and Pylon production, and issued three accepted Zealot trains. Heartbreak Ridge issued its second and third trains from the two Gateways in the same replay frame. No Dragoon or wrong-race unit appeared.

On the matched Benzene row, the first, second, and third Zealot requests advanced by 360, 228, and 132 frames respectively. The registered third-train gate required at least a 200-frame improvement, frame 4,026 or earlier, so frame 4,094 fails. Neither candidate reached a fourth accepted train, and each reported at most two current/completed Zealots. Both therefore fail the registered lifecycle gate as well. The no-gas state is expected because the phase completion condition was never reached; the test provides no observation of normal technology resuming after four queued Zealots.

The new telemetry separates global contact from local exposure. Benzene's first Probe loss at frame 2,918 occurred 795 frames before the first visible, detected ground enemy entered the 12-tile home radius at frame 3,713. Its timing and replay context are consistent with the scouting Probe, and it cannot be evidence of a visible enemy already inside the registered home radius. Heartbreak Ridge recorded the home threat at 3,586 and first Probe loss at 4,233. This distinction confirms that prior `first_enemy_contact` values could not be used as base-attack times.

The matched candidate ended at frame 5,893, 434 frames earlier than v7's frame 6,327. That outcome is descriptive because the policies do not execute deterministically, but it provides no directional reason to retain a candidate that already failed its mechanism timing and lifecycle bars. A longer loss would likewise not have established strength.

V10 establishes a useful narrow result: removing unrealized gas spending advances early Zealot requests without command-quality regressions, but the current two-Gateway economy still does not produce four queued Zealots before this pressure ends the game. The result does not support mixing in rejected v8's Probe reservation or v9's worker pull, and it does not justify threshold tuning from these two trajectories.

Replay SHA-256 values are `2f6b7f9902b45cdb6c0ed878781a296271239e3ebb1496d89ae5d8330711b10d` and `af9d4bcc023b1a57eec9c82ab742d98bd4d2e6b932853449ee19ed5fba77bafc` for Benzene, and `6a4d2bb7f559ee8125550da7398e017ba0db179db65a9cfd3da96ebe4b4128b7` and `ec25e3e2a35898a3abe7e8839c41ac5a03da5f88708c10d8dca422f8bfb33bce` for Heartbreak Ridge.
