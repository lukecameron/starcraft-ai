# McRave A* bounds throughput check

Registered 2026-09-20T04:32:26.763398+00:00, before any trial. Frozen schedule: `config/quick-as-bounds-schedule.json`. Candidate `ddc0415a3312bcfbc94f1e0efebe28e3ea1f5a4db739a7ae666567bc89b36c7f`, full source patch `ac7c61e58cc6e1b4f01623eea08faf1ab5c390ff2f5699b02701496d5d04592a`, diagnostic engine `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb`. Native and all 114 official-header translation units compile. The preceding same-input shadow matched all 13,439 paths and callback counts; independent source review passed.

## Question and decision

Does the production candidate complete all ten fixed scenarios with clean opposing results and at least 384 durable logical frames per wall second in every game and in aggregate? Primary metric is each manifest's logical_frame_count / durable_completion_seconds, including both bots, engine, initialization, logging and archive completion. Aggregate is sum(frames) / sum(durable seconds). No timing excludes opponent or startup cost.

An engineering ADOPT requires ten clean completions, no crash, timeout, contradictory metadata or diagnostic insync_hash_mismatch, and both throughput conditions. Valid complete measurement below the performance bar is REJECT; infrastructure or incomplete evidence is INCONCLUSIVE and prevents adoption. No result promotes playing strength or assigns a BASIL rating. The c49 reference remains retained regardless.

## Execution

Reuse all ten opponent/map/player/engine-seed/bot-seed scenarios from quick-mcrave-coordinate-cache-v1, changing only the candidate and logging-only engine package. Concurrency is two; wall cap is 120 seconds per game. Empty isolated learning state. No planned compile, other match, profiling, or replay playback overlaps. Ordinary desktop background activity is not controlled and must not be claimed absent.

Stop after ten attempts or the existing two-consecutive-infrastructure-failures rule. Never replace a failed game, retry a seed, or change the bar after results. Preserve all raw manifests, terminal logs and emitted replays; inspect every client's diagnostic events. Frozen scenarios are not a new held-out strength test. Engine/build and stochastic trajectories differ from historical measurements, so this is an absolute engineering gate, not a causal speedup comparison.

Report per-game and aggregate throughput, candidate-plus-engine CPU/RSS with scope, win/loss/failure counts, Wilson intervals and finite uncalibrated opponent-relative Elo. Infinite small-sample estimates are not ratings. A failure identifies the next bounded investigation rather than changing the acceptance threshold.
