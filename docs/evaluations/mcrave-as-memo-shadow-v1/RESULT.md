# McRave per-search A* memoization shadow result

Decision: **PASS for the registered per-call equivalence question**. The one permitted trial completed normally. Across 13,611 valid real-policy `generateAS` calls, the memoized shadow produced zero reachability, bit-exact distance, or ordered-tile mismatches. It covered 9,164 valid flying calls and 4,447 valid ground calls, and both registered invalid-endpoint probes also matched.

The candidate reduced combined supplied-callback evaluations from 1,892,712,022 to 169,940,460, a reduction of 1,722,771,562 calls or **91.02%**. Heuristic evaluations fell from 635,495,670 to 84,970,230 (86.63%); walkability evaluations fell from 1,257,216,352 to 84,970,230 (93.24%). The candidate called each supplied function only on its first request for a tile within each search. Its caches were recreated for every call and did not cross searches, frames, units, or callback closures.

This passes the preregistered requirement of at least 1,000 valid calls, both real-policy movement classes, two invalid probes, zero output mismatches, non-increasing counts for each callback kind, and a strict combined reduction. No callback-state mutation was observed, consistent with the prior source review of all seven callback families.

## Match and integrity

The sole run was `20260920T044920-ce26d75af106`, Destination, McRave Zerg as player 1 versus UAlbertaBot Terran, with engine and McRave seed 3001. It used frozen logging engine `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb` and diagnostic module `daeab5c471b2714e61c27cfcf30fd705aff062fae841ff25acc9e6eebd608ae9`.

Both processes exited zero after 101.854 elapsed seconds, below the 120-second cap. McRave reported victory at frame 26,973 and UAlbertaBot reported defeat at frame 26,942. The outcome was verified and opposing. Neither stderr contained `insync_hash_mismatch`. The terminal diagnostic pattern was the ordinary winner-side `controller_not_occupied_after_action` after action 87 and loser-side `transport_callback`; there was no contradictory winner metadata. McRave-plus-engine used 97.471 CPU seconds and peaked at 493,568,000 bytes RSS. Those figures include the engine and shadow overhead.

Both replay files were copied and hashed: player 1, 1,090,386 bytes, SHA-256 `941ec8d2109475b760bf7d03fb0e3bd3598df105ee7c0759f1d0568582e030e7`; player 2, 1,087,178 bytes, SHA-256 `369baf08dd8c93d1cef769308bc6abd9f6bdfb4379811ff411c02a9b07cfdb02`. Replay playback was not validated, so these records establish durable emission and hashing rather than semantic playback.

## Evidence and limits

The authoritative match manifest is `artifacts/runs/20260920T044920-ce26d75af106/game-0001/manifest.json`. Frozen copies of the manifest, final shadow summary and both stderr logs are under `artifacts/experiments/mcrave-as-memo-shadow-v1/results`. The final summary SHA-256 is `54eeead73775bfe4f4979c9cb579c6648b81331ec40d6684caf2860ae16fd226`; the frozen manifest SHA-256 is `a4f981a4f3761a1f412ab98e67e5ce89e43351f3ba2feef09372772bfb8624b1`.

The diagnostic module and sidecar are under `artifacts/experiments/mcrave-as-memo-shadow-v1/build`. Native OpenBW compilation and all 114 official-BWAPI-header translation units passed with four jobs. The source delta is `shadow.patch`, SHA-256 `e1735ff8b340a4a115c7024f6d80d4328bee6f7e8c59a1a3bef610dc63afea9f`, applied over frozen candidate `ddc0415a3312bcfbc94f1e0efebe28e3ea1f5a4db739a7ae666567bc89b36c7f`.

Production A* remained authoritative throughout the run; the shadow did not issue game commands or mutate the production path or unreachable cache. This one scenario supports a separate production memoization candidate. Its 264.8 durable frames/s includes executing both algorithms, fresh diagnostic allocations and summary writes, so it is not a production throughput estimate or evidence of a speedup. It is also not a strength evaluation or rating result. A production candidate still requires source review, compilation checks and its own preregistered engineering gate.
