# Kestrel v8 first-zealot priority result

**Decision: reject v8. The timing mechanism worked, but the registered lifecycle and directional defense gates failed. Keep v7 as the baseline.**

Both candidate games completed cleanly with zero launcher exits, opposing callbacks, no state-hash mismatch, two `screp`-readable replays, zero rejected commands, and throughput well above 384 frames per second. Kestrel lost both games.

| Row | Run | First enemy contact | First zealot train | First completed combat unit | Max probes / zealots | Own probe losses | Local terminal frame | Durable frames/s |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| Cached v7 control, Benzene 6103 | `20260920T063735-568f09f7d3a0` | replay first attack at 2,642 | 3,416 | not instrumented | 15 / 3 | not instrumented | 6,327 | 2,943.6 |
| V8 matched, Benzene 6103 | `20260920T064202-95acc7e7959a` | 2,172 | 3,020 | 3,623 | 13 / 2 | 16 | 6,265 | 2,904.2 |
| V8 held-out, Heartbreak Ridge 6105 | `20260920T064215-e798f5386b3a` | 2,410 | 3,140 | 3,743 | 11 / 2 | 14 | 5,645 | 3,556.3 |

The exact-row mechanism gate passed. V8's first zealot train at frame 3,020 was 396 frames earlier than v7's frame 3,416 and earlier than the registered frame-3,116 threshold. Its assimilator command followed at 3,026, so no gas was purchased before the first zealot request. The held-out row followed the same ordering: zealot at 3,140 and assimilator at 3,146.

The implementation uses current `allUnitCount(Protoss_Zealot/Dragoon)`, not a persistent “first unit queued” flag. In both observed games OpenBW/BWAPI reflected the accepted zealot train in that count by the next six-frame policy poll: probe training and the assimilator resumed six frames after the first zealot command, hundreds of frames before the telemetry-recorded completion. Thus the initial reservation ran as intended. Source review also shows a latent semantic difference from a strictly one-time priority: if every current and queued combat unit later disappears, the reservation can reactivate. The preserved replay and aggregate telemetry do not establish whether that branch occurred. Because v8 is rejected on its registered gates, no corrected candidate is created from this result; any future use of the idea must use an explicit persistent flag and a new evaluation.

Earlier training did not solve the registered survival problem. On Benzene the first globally visible enemy preceded the first completed combat unit by 1,451 frames; on Heartbreak Ridge the gap was 1,333 frames. This telemetry includes distant scout contact and is not a base-exposure timestamp. Replay inspection later confirmed that each first zealot fought near home rather than chasing the scout's distant contact. Kestrel recorded only two simultaneous zealots in each game and lost 16 and 14 probes respectively. The matched candidate ended at local frame 6,265, 62 frames earlier than v7's 6,327, so the directional defense gate failed. The held-out row also failed its registered lifecycle floor of 12 probes and three zealots, reaching 11 and two.

This result rejects broad mineral reservation as the next defense step. It sacrifices probe production but cannot overcome gateway plus zealot construction time after enemy contact. The next Zerg-defense hypothesis should act with existing workers when a visible ground threat reaches the starting base, while leaving v7's economy and production timing intact. That requires a separately frozen candidate and evaluation.

Replay SHA-256 values are `f68cc4e898f9444b69d736caa386b1982ab873b7773a2f746345c24f857f0ee6` and `8e9784f5bd71a6c63a818ca23d93133e61d777b06a9fe32e760736680e2ef817` for Benzene, and `4003b1780e576ef09571c8c839852e58148be4eebecf370fb4a90466df70fc07` and `dadd523820f6971bacf5609040084d289dd97bdc93daa1ad6946c9ac9afb8870` for Heartbreak Ridge.
