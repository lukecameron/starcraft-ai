# Experiment ledger

No validated competitive incumbent exists. Diagnostic fixtures are never rating anchors.

| Date / experiment | Question and stopping rule | Evidence | Decision |
| --- | --- | --- | --- |
| 2026-09-20 native engine | Can native ARM64 OpenBW load two modules and finish a game with replays? Stop build spike after 15 minutes or a concrete blocker. | Engine compiled; initial startup failed without MPQs; authorized Blizzard StarEdit data and SSCAIT maps resolved it. | Retain native route. |
| 2026-09-20 first multiplayer | Can a complete legal-observation diagnostic game run without GUI/audio? 120 s wall cap. | Archive runs `20260920T015054-18fd4974d193`, `20260920T015129-85962e13b704`: long paths; `20260920T015225-d4f6cbd53aa6`: sandbox denies sockets. | Relative replay filename, short temporary socket directory, approved unsandboxed launch. Preserve failures. |
| 2026-09-20 diagnostic completion | Does WorkerRush beat Idle and emit real replays? | `20260920T015245-8d1cc76f5e12`: 5614 frames, 1.536 s, two replays, LF3 reported by both clients, opposing winner callbacks. Replay loads and process completes. | Runtime milestone reached; no Elo/competitive throughput claim. |
| 2026-09-20 archive integration | Do input hashes, terminal records and durable completion work with the actual engine? | `20260920T015722-17e3dc11ff1d`, complete game; six Python lifecycle tests pass including timeout, interrupt, startup failure and incomplete replay. | Retain archival harness. Replays still require independent parser/playback validation. |
| 2026-09-20 competitive bot ports | Can current McRave and ZZZKBot run natively without disabling gameplay? Initially 15 min per compile spike, <=4 jobs each. | In progress; source revisions pinned in opponent manifest. | Await compilation and actual matches before base choice. |

Source/binary revisions must accompany future promotion comparisons. The present launcher derives randomized engine seeds through upstream client IDs: no matched deterministic scenario control exists yet. Repeated fixture results are not independent strength evidence.
