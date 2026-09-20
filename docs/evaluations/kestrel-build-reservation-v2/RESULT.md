# Kestrel v2 build-reservation probe result

**Decision: compatibility and original behavior gates passed; the fix-specific command-count gate failed. Keep v2 as a functioning development baseline, but investigate remaining command churn before a strength probe.**

The one registered attempt completed as `20260920T060713-1258ac57a72c`. Both launchers exited zero, callbacks reported opposing outcomes, no `insync_hash_mismatch` appeared, and `screp` parsed both preserved replays. Kestrel won at local frame 8,559; WorkerRush lost at frame 8,528. The win is not a strength claim.

The original behavior gate passed. Lifetime telemetry recorded 27 probes, five pylons, four gateways, nine zealots, and two dragoons. The replay contains probe, pylon, gateway, assimilator, cybernetics-core, zealot, and dragoon production commands, plus scouting outside the starting base and combat orders after army production. It contains no wrong-race production.

The diagnosed worker-order cancellation was materially reduced but did not satisfy the registered fix-specific threshold. V0 issued 55 pylon plus gateway build commands and produced no combat unit. V2 issued 11 pylon plus five gateway commands, totaling 16 against the preregistered maximum of 12, while completing the production lifecycle. The accepted build sequence is bounded rather than occurring every six frames; examples include the initial pylon commands at frames 998 and 1,238, exactly one 240-frame retry interval apart. The remaining retries mean this part of the gate fails and should not be reinterpreted after the result.

The match completed 8,559 logical frames in 1.3104 seconds through durable archival, or 6,531.6 logical frames per wall second. Kestrel recorded 0.043925 CPU seconds across 8,560 callbacks, 0.009583 ms callback p99, and a 2.215 ms maximum. The short fixture is not representative late-game performance. Telemetry also reports 636 attempted commands and 316 rejected commands; replay inspection attributes substantial churn to repeated moving-enemy attack orders, which is a separate bounded-policy issue.

The authoritative manifest is `artifacts/runs/20260920T060713-1258ac57a72c/game-0001/manifest.json`. The player-one replay SHA-256 is `1f685f283360399158a1dfd2d0a983cb00dd6010612389ba6269d8e175f44c35`; the player-two replay SHA-256 is `e4efbd226f0de208fd9d1bd60631cabbdb676ee74526f69b56e917c74a2b8dbf`.

The next source change should suppress redundant combat orders while retaining responsive target changes. Any test of that change needs a new binary identity and preregistration. V2 remains the first Kestrel build with a complete native economy-to-combat lifecycle and a clean official-header compile, but it is not yet a validated strength anchor.
