# McRave Support JPS memoization production quick result

Decision: **REJECT for engineering acceptance; do not adopt.** Four valid completed games independently fail the fixed 384 durable frames/s minimum, and both all-attempt and clean-game aggregates are below 384. Game 3 also produced two winner callbacks and remains unscored, so terminal-integrity evidence is incomplete, but that invalid result does not erase the established performance failures. All-attempt aggregate throughput was 183,116 frames / 485.048 seconds = **377.5 frames/s**. The nine clean games aggregated 175,270 frames / 477.959 seconds = **366.7 frames/s**.

| Game | Opponent/map | Result integrity | Frames/s | Candidate user CPU s | Peak RSS MiB |
|---:|---|---|---:|---:|---:|
| 1 | ZZZK / Benzene | clean win | 677.6 | 17.586 | 462.9 |
| 2 | ZZZK / Benzene | clean win | 640.2 | 22.131 | 463.0 |
| 3 | ZZZK / Destination | two winners, unscored | 1106.8 | 6.584 | 458.0 |
| 4 | ZZZK / Destination | clean win | 626.1 | 22.625 | 461.8 |
| 5 | UAlberta-P / Benzene | clean win | 421.3 | 40.759 | 464.4 |
| 6 | UAlberta-P / Destination | clean win | **332.6** | 36.094 | 465.9 |
| 7 | UAlberta-P / Benzene | clean win | 452.3 | 29.349 | 465.0 |
| 8 | UAlberta-T / Destination | clean win | **237.9** | 109.914 | 474.1 |
| 9 | UAlberta-T / Benzene | clean win | **370.8** | 47.859 | 464.9 |
| 10 | UAlberta-T / Destination | clean win | **284.5** | 103.365 | 469.4 |

The candidate processes consumed 436.266 user CPU seconds and 5.469 system CPU seconds in total; peak observed candidate RSS was 497,172,480 bytes (474.1 MiB). All ten launcher pairs exited normally and emitted two replays each. All 20 archived replays parsed successfully with the existing `screp` parser. No stderr contains `insync_hash_mismatch`, a crash, or a sanitizer signature.

Game 3 reproduces the known old-engine terminal race: player 1 observed `transport_callback` at frame 7,813, then player 2 observed `controller_not_occupied_after_action` with action 9 at frame 7,814; both later dispatched winner callbacks. This is invalid outcome evidence rather than a draw or candidate win.

Only historical rows 1, 2, 4, and 9 met the preregistered 1% terminal-frame comparability condition against frozen baseline `04521bef...`. Candidate user CPU per frame was lower by 6.47%, 11.80%, 7.99%, and 4.09%, respectively, while candidate peak RSS differed by -0.34%, -0.18%, -0.02%, and -0.28%. This consistent secondary signal supports retaining the isolated candidate for further investigation, but it cannot override the absolute slow-tail failures or the invalid tenth-clean-game requirement. No strength or rating conclusion follows from the nine observed wins.

The next performance investigation should remain on the two slow Destination/UAlberta-T rows. Support predicate memoization reduced measured work in isolation, but games 8 and 10 still dominate elapsed time; a fresh production profile on the corrected engine should identify the remaining subsystem before another optimization is proposed.
