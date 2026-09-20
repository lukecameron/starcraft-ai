# McRave versus UAlbertaBot Zerg compatibility result

**Result: INCONCLUSIVE.** Both registered games proved that the frozen UAlbertaBot executes its configured Zerg production path and completed with clean terminal integrity, but the second game reached only 314.6 durable logical frames per wall second, below the fixed 384-fps compatibility bar. There was no retry.

| Run | Map | McRave slot | Outcome | Frames | Durable fps | UAB first Drone / Pool / Zergling |
|---|---|---:|---|---:|---:|---|
| `20260920T071352-783c238a4157` | Benzene | P1 | McRave win | 15,007 | 418.8 | 2 / 1,018 / 2,311 |
| `20260920T071429-e83ebd600032` | Destination | P2 | McRave win | 26,105 | 314.6 | 2 / 1,004 / 2,306 |

UAlbertaBot issued 10 Drone morphs, one Spawning Pool build, and 23 Zergling morphs in the first replay; it issued 13, one, and 20 respectively in the second. The complete command-derived evidence is `artifacts/experiments/mcrave-ualberta-zerg-compat-v1/production-evidence.json` (SHA-256 `d58e4d4084fcc9842d438d0408a6014c948048acab01d83eedfdcb1aac764851`). Both full command streams parsed with no parser-error commands.

The UAlbertaBot callback telemetry reported zero workers, combat units, and production buildings in both games. Source inspection shows that `writePortResult()` counts the current `Broodwar->self()->getUnits()` set (`third_party/ualbertabot/UAlbertaBot/Source/UAlbertaBotModule.cpp`, lines 27-35) and `onEnd()` calls it before returning (lines 101-107), so these fields are a snapshot of surviving units at the terminal callback. UAlbertaBot lost both games and had been eliminated; zero is therefore consistent with the source contract and does not contradict the earlier production commands. The fields are not cumulative production counters and must not be described that way in a broader comparison.

Both launch pairs exited zero and reported opposing terminal outcomes. All four replay copies matched their manifest hashes, parsed through the full screp command stream, contained Zerg/Zerg headers, and ended one frame before the owning callback. Each game recorded only the reviewed terminal-drain cleanup diagnostics: winner-side `controller_not_occupied_after_action` with action 87 and loser-side `transport_callback` with action -1. There was no hash mismatch, crash, timeout, unexpected kill source, or contradictory outcome. The durable execution ledger is `artifacts/experiments/mcrave-ualberta-zerg-compat-v1/paired-ledger.json`.

The 314.6-fps failure means this two-game preflight does not authorize treating UAlbertaBot Zerg as a performance-qualified broader-opponent lane. Its gameplay compatibility is established. The next step is a separately registered performance diagnosis of the slow Destination cell or a broader comparison whose engineering bar explicitly accounts for this measured workload. These outcomes are not included in the ZZZKBot confirmation and make no strength claim.

## Process measurements and next diagnostic

On Benzene, the McRave-side process used 32.979 CPU seconds over 15,007 logical frames (0.0021976 seconds/frame) and peaked at 463.9 MiB RSS. The UAlbertaBot-side process used 6.137 seconds (0.00040894/frame) and peaked at 53.0 MiB. On Destination, McRave used 76.289 seconds over 26,105 frames (0.0029224/frame) and peaked at 478.8 MiB; UAlbertaBot used 12.102 seconds (0.00046359/frame) and peaked at 58.5 MiB.

Combined process CPU/frame rose 29.9% in the slower game. McRave-side CPU/frame rose 33.0%, UAlbertaBot-side CPU/frame rose 13.4%, and the McRave-side increase accounts arithmetically for 93.0% of the combined increase. Each process includes its own OpenBW engine plus loaded bot, and the games differ in map, slot, seed, duration and realized state. This identifies the McRave-side process as the first profiling target; it does not identify a causal function or prove a map effect.

The highest-value next diagnostic is one preregistered reproduction of the exact Destination seed-9202 cell with an external sample of the McRave-side process after at least frame 15,000. Keep source and configuration frozen, require a complete ten-second sample or classify it inconclusive, and report non-overlapping inclusive subsystem shares. Do not use that instrumented run as throughput or strength evidence.
