# McRave Support JPS memoization production quick gate

Registered 2026-09-20T06:16:11Z and amended 2026-09-20T06:16:59Z, before any production-candidate game. The amendment replaces an initial four-game paired draft with the established ten-game engineering gate so a small favorable subset cannot bypass the existing slow-tail requirement.

## Hypothesis and frozen inputs

Support-only, fresh per-search boolean predicate memoization lets the frozen candidate complete the established ten scenarios cleanly at no less than 384 durable logical frames per wall second in every game and in aggregate.

Run frozen candidate `436cfa74fa34c267f7404777a3170be0202485bdc7224d15fb30b85f02c5644e` through the exact ten rows, order, maps, opponents, player assignments, engine seeds, and candidate bot seeds in `config/quick-support-jps-memo-schedule.json` at SHA-256 `dd92ed048b6b8ed7037e6f84f210e011402116934501e2ac29e2c85d95f7bdf4`. The new schedule preserves the earlier operational rows while correcting its stale A* title and hypothesis and setting the frozen Support JPS candidate identity. Keep the frozen old engine `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb`, concurrency two, 120-second per-game cap, publication behavior, and existing two-consecutive-infrastructure-failure stop rule. Run one batch with no retries, replacements, seed changes, or adaptive scheduling.

The earlier frozen baseline `04521befa41bb3873783b215493abf3a071414d2a5315cdea68fc7a67f4415ec` used this same schedule and engine in `artifacts/experiments/quick-mcrave-as-memo-v1/manifest.json`. Report paired per-row CPU/frame and RSS differences where both historical and candidate attempts are clean and their terminal frames differ by no more than 1%. These historical comparisons are secondary because the runs were collected at different times; they do not replace the absolute gate.

## Measurements and fixed decision rule

Measure each game's logical frame count divided by its durable completion seconds, including both launchers, startup, logging, and archival. Aggregate throughput is sum of frames divided by sum of durable seconds. Also report per-game McRave user/system CPU, peak RSS, terminal frame/outcome, process return codes, replay status, hash/kill diagnostics, and the secondary matched historical comparisons.

**ADOPT as an engineering candidate** requires all ten attempts to complete with verified opposing terminal metadata, zero crash, timeout, contradictory result, or `insync_hash_mismatch`, at least 384 durable frames/s in every game, and at least 384 aggregate frames/s. A complete valid game below 384 or an aggregate below 384 is **REJECT**. Infrastructure-invalid or incomplete evidence is **INCONCLUSIVE** and prevents adoption. The historical comparison cannot override this rule.

This gate measures engineering fitness across the established small cohort. It does not establish playing strength, general map performance, causal speedup, or a calibrated rating. Preserve every attempt and stop after this cohort.
