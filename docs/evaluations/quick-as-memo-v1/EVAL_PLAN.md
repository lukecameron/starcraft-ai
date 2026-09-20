# McRave per-search memoization throughput gate

Registered 2026-09-20T04:55:10.160981+00:00, before any production trial. Schedule: `config/quick-as-memo-schedule.json`. Candidate `04521befa41bb3873783b215493abf3a071414d2a5315cdea68fc7a67f4415ec`, full source patch `2d7b64f1cad12a8ab05e78cc9f76366b1bc5bc9446746c41cdf445884d4316cb`; engine `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb`. Root source review passed. Native and all 114 official-header translation units compile. The preceding shadow compared 13,611 valid calls without output mismatches and reduced combined callback evaluations by 91.02%; this does not establish production speed.

## Question and fixed decision

Does the production candidate complete all ten registered scenarios with clean opposing results and at least 384 durable logical frames per wall second in every game and in aggregate? Measure each game's logical_frame_count / durable_completion_seconds, including both engines, bots, startup, logging and archival. Aggregate is sum(frames) / sum(durable seconds), not total batch wall time.

ADOPT as an engineering baseline requires ten clean completions, no crash, timeout, contradictory result or diagnostic insync_hash_mismatch, and both throughput conditions. Complete valid evidence below the speed threshold is REJECT; incomplete or infrastructure-invalid evidence is INCONCLUSIVE. None of these decisions promotes playing strength or assigns an absolute rating. Preserve the c49 reference and all earlier failed candidates.

## Execution and evidence

Use the exact ten opponent/map/player/engine-seed/bot-seed rows from quick-mcrave-as-bounds-v1; only the candidate changes. Two games run concurrently, each with a 120-second cap and isolated empty learning state. No planned compilation, other simulation, profiling or replay playback overlaps. Ordinary desktop background activity is uncontrolled.

Stop after ten attempts or the existing two-consecutive-infrastructure-failures rule. No retry, replacement, seed change or adaptive schedule. Keep every raw manifest, stderr and emitted replay; inspect both clients' diagnostics even when their outcomes oppose. Report per-game and aggregate throughput, scoped candidate-plus-engine CPU/RSS, failures, wins/losses, Wilson intervals and the limitations of infinite small-sample relative Elo estimates. Validate archived replays with the existing parser after collection.

The scenarios are reused and trajectories can differ despite seeds. This is an absolute engineering gate, not a causal speedup comparison or held-out strength evaluation. Callback memoization is valid only for the reviewed synchronous read-only callbacks and current map-size bounds; future callback changes require fresh review.
