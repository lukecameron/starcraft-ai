# Kestrel v9 visible-threat worker-defense result

**Decision: reject v9. The worker-defense mechanism executed as designed, but both games failed the registered lifecycle gate and the matched game ended earlier than v7. Keep v7 as the development baseline.**

The fixed two-game schedule ran once, serially. Both games returned zero from both launchers, produced opposing winner callbacks, contained no `insync_hash_mismatch`, and produced two `screp`-parseable replay copies. The runner's `launcher_error_detected` field is true because the adopted engine writes its structured terminal-drain diagnostics to stderr; inspection found only the expected terminal controller/transport events, not a state-hash error.

| Row | Run | Contact | Defense trigger / max defenders | First combat unit | Max probes / gates / zealots | Worker losses | Local terminal | Durable frames/s |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| Cached v7 control, Benzene 6103 | `20260920T063735-568f09f7d3a0` | not instrumented | none | not instrumented | 15 / 2 / 3 | not instrumented | 6,327 | 2,943.6 |
| V9, Benzene 6103 | `20260920T064926-fec5e08f179d` | 2,163 | 3,834 / 6 | 3,635 | 15 / 2 / 1 | 18 | 6,110 | 3,004.7 |
| V9, Heartbreak Ridge 6105 | `20260920T064928-c44db719d1cb` | 2,434 | 3,588 / 6 | 3,797 | 14 / 1 / 2 | 16 | 5,614 | 3,580.8 |

The mechanism gate passed. In the Benzene replay, six unit tags that had previously received mineral-harvest orders received `Attack1` at replay frame 3,836, two frames after the bot's recorded defense trigger. Heartbreak Ridge likewise shows six selected units attack at frame 3,590. Later mineral-harvest commands to former attacking worker tags appear in both replays, providing direct evidence that released defenders could return to economy handling. Telemetry bounded simultaneous defenders at six in both games. This evidence uses public commands and bot observations; it does not infer hidden enemy state.

Role consistency was corrected before launch. The originally frozen but unrun `7518c14…` build could select a newly assigned defender as a builder later in the same callback. The timestamped plan amendment replaced it with tested build `cf3e8409…`, whose construction selector excludes defender IDs. No game used the superseded build.

The registered acceptance gates failed. Benzene produced only one zealot and ended locally at frame 6,110, 217 frames earlier than v7's matched-input frame 6,327. Heartbreak Ridge produced two zealots and ended at frame 5,614. Both therefore missed the three-zealot lifecycle floor, and Benzene missed the directional survival gate. Command rejection remained below 5%: 1/84 on Benzene and 2/64 on Heartbreak Ridge, all recorded as busy attack requests. Throughput exceeded 384 frames/s in both games, but these short runs do not support a performance comparison.

V9 confirms that a legal, bounded worker pull can be implemented without economy assignment immediately replacing defense orders. It does not show that this policy improves early survival. The large losses, 18 and 16 probes, and reduced combat production indicate that the current always-six nearest-probe response is too costly or tactically weak for retention. No tactical follow-up is inferred from two trajectories, and this result does not change Kestrel's rating or strength status.

Replay SHA-256 values are `62464b49c387a543ad9fc7795a0fde92586e151f13492e7e1c4fe43d355605e8` and `2f9885fe41541a1b9fbf7ab9f56139b1968d9a0e01f305a43c997d8a603a5965` for Benzene, and `43231b81b9e1bf38cff48420138b6c18edca037b9d762befa2c61cf81f8493ed` and `57feb1be47d9b8a17e8fcbe43fea7354516e0808e4b348a6c005c2701d00108f` for Heartbreak Ridge.
