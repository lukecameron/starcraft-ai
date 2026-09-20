# Resume

Checkpoint: 20 September 2026, 07:11 UTC. Continue the user's autonomous development request through **21 September 05:52 UTC** unless redirected or resources require a decision. User redeemed a reset personally; do not consume another. Their status question about the original bot was answered: Kestrel works end-to-end, but has not beaten a benchmark bot. We are testing its opening production timing.

## Authorization and ongoing work

- Direct `main` backups and Cloudflare Pages publication are authorized. No contact, tournament submission, purchases or additional reset redemption.
- Quota last checked approximately 07:09 UTC: 41% remaining (59% used). Recheck around 07:40, then every 30–60 minutes. Pace lead review between meaningful checkpoints; heartbeat supports continuation without idle polling. Two credits remain, requiring explicit per-credit approval.
- Active heartbeat `starcraft-development-while-away`: every 30 minutes, 48 scheduled runs, deadline in saved prompt. Inspect exact agents/sessions before launching anything. Stop follow-up at the deadline. Preserve all failed attempts and replays.
- **engine_sol read-only analysis:** v11 session 52986 completed, REJECT, report durable, window released. Now inspecting pre-first-Gateway trace resources/supply to assess whether threshold 18→16 alone can help or another constraint binds. No source/build/game authorized; canonical v7 unchanged.
- **harness_sol active:** two-game UAlberta Zerg compatibility session **68706**, durable ledger `artifacts/experiments/mcrave-ualberta-zerg-compat-v1/paired-ledger.json`. Exclusive game window. Registered plan SHA `870a55f78b68c50b4b84996c253bf8acbddd02079ec2eb3a18f338a0c3305d32`, schedule SHA `c76a7e7f9b1025cb90129c77ecb240a034e8b53760ebe265e0fc0a3a9462c5af`. Corrected runner SHA `98e256f9c11af11c6813d5f93c9d31c64ea23461be4d1a6231a2f6e73a19d626`: full replay parsing, restart refusal on unresolved/terminal states, exact-process cohort cap, malformed-record handling. Lead reviewed code and retained-fixture/subprocess tests. **No 64-game confirmation launch authorized yet**; inspect compatibility evidence first. Confirmation registered plan SHA starts `cb5b9883`, schedule `0376b74e`, under `docs/evaluations/mcrave-zvz-9pool-confirmation-v1/`.
- **opponents_luna idle:** bounded timing analysis agreed the first Gateway-to-Zealot pipeline is now the earliest target. No edits/builds/games. Engine agent will check resource feasibility before another policy change.
- Root owns `config/experiments.json`, `docs/kestrel-bot.md`, this resume and publication. Avoid overlapping edits without handoff.
- Local HTTP server session 85590, PID 1285, serves `public` at 127.0.0.1:8787. Chrome CLI works while Mac is locked; do not bypass the lock. Current browser is immutable a502c242, desktop 1200. Prior mobile 390 and desktop layout checks passed.

## Current engine

**Adopted:** engine `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`, launcher `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`. Exact paths in `config/engine.json`; rebuild route `docs/engine-terminal-drain.md`. Frozen flat package under `artifacts/builds/<engine-sha>/openbw-terminal-drain/`. Patch `patches/openbw-terminal-drain.patch`, SHA `787c642705c8181ac814ce68d44709e07a20116a5f02a0ad0950998e4ec5f2a8`.

The repair discards ordinary queued commands from defeated players before execution/replay recording and retains their transport until explicit leave or normal cleanup. It fixes the reproduced old-engine reciprocal-winner failure. Hash/control/error handling remains. Six registered targets/controls passed; all 12 replays parsed and 1,380,602 common commands matched. Subsequent 36 calibration games and 16 strategy screening games completed cleanly. This is not proof of all engine paths or Windows runtime.

Old f1/27ea packages, invalid results and schedules remain preserved. `scripts/engine-build.sh` builds the historical foundation; the current engine document gives the direct rebuild route.

## Kestrel, our original bot

Independent MIT Protoss policy, author Luke Cameron, `bots/kestrel/`, registry Ours/Original. Only public BWAPI observations. Native and official BWAPI 4.4 header compilation pass; official Win32 runtime remains unverified. Build and reconstruction instructions: `docs/kestrel-bot.md`, `scripts/build_kestrel.sh`.

**Canonical accepted v7 command/lifecycle baseline:** `2facbf970d4a4fd131564d3d02cd3966bcadc50e13e08256a1a92d3886013d3e`, package `<sha>/kestrel-v7/`. Combined source SHA `34f43843f762ed32c7052eda64e324db8fe6b4204dd48f94692d84df5d2b18f1`; `config/kestrel-baseline.json` points to it. Tracked source is restored byte-for-byte v7. Candidate sources remain isolated under third_party with tracked reconstruction patches.

V7 passed command checks: zero train or attack rejections in two full losses. ZZZK run `20260920T063735-568f09f7d3a0`: 2,944 fps, max 3 Zealots. UAlberta Terran `20260920T063750-d32c98d8cbcc`: 1,465 fps, max 28 Probes, 4 Gateways, 5 Zealots and 10 Dragoons; 4% gather-only command rejection. V2 beat the WorkerRush diagnostic, but no Kestrel version has yet beaten ZZZK or UAlberta. Do not call Kestrel a rating anchor or a competitive success.

Recent rejected candidates:

- V8 `fd799d9e…`: first Zealot train 396 frames earlier, but both games failed lifecycle/survival bars. Current-count reservation could reactivate after army loss; recorded deviation, unadopted.
- V9 tested `cf3e8409…`: six-Probe worker defense executed legally, but both games lost earlier with less army. Unrun `7518…` was corrected before launch for builder/defender role conflict. Keep both identities.
- V10 `2c029177…`: delay gas/Core until four queued/current Zealots against known Zerg. Both games had zero rejected commands, but third train advanced only 132 frames against the registered 200-frame bar; no fourth Zealot queued, max two completed. REJECT. Forward patch `patches/kestrel-v7-to-v10.patch`.

**Latest diagnostic:** isolated instrumentation-only v7 `084160cc9afcee500a54a851f434388c462ab00d81aa60536f47ab217f68d1ef`, run `20260920T070255-f110c96947fd`. Clean loss, two parsed replay copies. At frame 3,720 there were 166 minerals, an unfinished first Zealot and five local Zerglings. First Zealot attacked at 3,740 and died at 3,823. Second Gateway only requested at 3,672; second Zealot attacked at 4,580 and died at 4,725 against at least eight lings. The units engaged locally but separately. Gas was already built/staffed; no Core or Dragoon realized. This supports an earlier-capacity experiment, not a general causal or strength claim. Full evidence `docs/evaluations/kestrel-fight-diagnostic-v1/RESULT.md`, patch `patches/kestrel-v7-fight-diagnostic.patch`, public trace SHA `e3f7e880f12155ddc0006b745169a268e27994fb58bc7e793f2e4773ca8e41f4`.

Earlier replay analyses distinguish scout contact/death from home exposure. Attack destinations alone do not prove arrival. V11 should test completed-defender overlap before the first defender dies. A separate later macro defect is the five-Pylon cap (49 supply); do not mix it into opening experiments.

## Local Elo evidence

Gaussian-prior Bradley–Terry MAP, 400 Elo prior SD, approximate 95% Laplace contrast intervals and 200/800 sensitivity. ZZZK 1000 is an arbitrary reference, not BASIL. Exact module/race/AI-config nodes; engine, game-data, platform, latency, learning and timeout define regimes. Invalid, unreviewed, duplicate and diagnostic games excluded. Reviewed final-manifest hashes in `config/local-ratings.json` gate inclusion.

**Current v2 + v3:** 36/36 clean games across four maps, all 72 replay copies hash/parse/owner-frame/race checked. Five exact nodes: Stardust `103997…` 16–0, estimate 1426.8 [994.8,1858.9]; ZZZK `ce796…` 7–5, reference 1000; McRave `04521…` 8–12, 836.8 [536.4,1137.1]; UAlberta Terran `75ac…` 3–9, 579.6 [220.3,938.9]; UAlberta Protoss same module 2–10, 535.3 [139.2,931.5]. V3 added direct edges Stardust–ZZZK 4–0, McRave–UABP 4–0 and McRave–UABT 3–1. These are descriptive observations, not code-change effects.

V2 and v3 pool because exact regimes match; cohorts are coverage metadata. Historical v1 remains separate: nine clean of twelve attempts, three reciprocal-winner invalids; full cohort rejected. Current/historical labeling is explicit. Wide conditional intervals, priors and map/style effects limit precision. Calibration throughput is descriptive because compilation could overlap; some games fell below 384 fps. Forty-three Python tests passed after the cohort-model changes.

## McRave and fork experiments

Reference `c49ee3c4…` remains in `config/baseline.json`; no robust strategy promotion. Canonical checkout `98df…` is unadopted. Ratings use frozen A* memo fork `04521befa41bb3873783b215493abf3a071414d2a5315cdea68fc7a67f4415ec`. All derivatives retain Christian McCrave attribution.

Support-JPS shadow `5860af09…` showed 16,773 comparisons with zero path/distance/reachability differences and 65.65% fewer callback evaluations. Production `436cfa74fa34c267f7404777a3170be0202485bdc7224d15fb30b85f02c5644e` failed its old-engine engineering gate: nine clean games, one reciprocal-winner invalid; four valid games below 384 fps. The valid performance failures remain failures despite the engine issue. It is the frozen experimental control for current 9Pool work, not an accepted incumbent.

The four-game opener diagnostic `3314c66d…` established the selected opener varied with seed: 1001 chose 9Pool on both maps; 6301 chose Gaspool. All games clean; two 9Pool wins and two Gaspool losses are diagnostic, not proof.

**9Pool screening completed:** treatment `fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa`, full patch `patches/mcrave-zvz-9pool-candidate.patch`. Normal learning/RNG calls remain; only the PoolLair ZvZ opener becomes 9Pool. Native and 114 official-header translation units passed. Session 5362 completed and released the window.

Sixteen games, eight matched pairs: treatment 7/8 wins, control 6/8. Four effective changed-opener pairs: two Heartbreak losses became wins, two Benzene pairs both won, no effective regression. A no-op Heartbreak pair flipped from control win to treatment loss, showing residual variation. All 16 valid, all 32 replay copies reviewed; minimum treatment 631.9 fps, CPU/frame ratio 1.00426. Registered screening gates passed **only to advance to independent confirmation**, not production adoption. Final screening plan SHA `58d67c23937f348e4de0249c1cf8d4157f9184c0c0f62a636f1659e19346c7a8`; result `docs/evaluations/mcrave-zvz-9pool-candidate-v1/RESULT.md`.

Confirmation draft: 32 pairs/64 games, fresh seeds 9101–9132, four maps and both slots, alternating arm order. Net paired gain >=4 plus exact one-sided discordant-pair sign test p<=0.05; map/slot net >=-1, all valid, every game >=384 fps, treatment CPU/frame <=110%, <=768 MiB candidate-process RSS. Fixed 150-minute cap, 120 seconds/game, stop after two consecutive invalid attempts; preserve every attempt, no replacement. UAlberta Zerg compatibility is a separate two-game prerequisite for future breadth. Await exact registered schedules and root launch authorization.

Stardust repaired fork `103997…` is currently strongest in this local cohort. Author Bruce Mackenzie Nielsen; its custom license restricts tournament derivatives. Do not contact or submit it without authorization.

## Dashboard, publication and backup

Latest completed publication **https://79cf0911.starcraft-ai.pages.dev/**, session 57299, approximately 07:13 UTC: 216 recorded matches and 59 experiments. Includes final v3 league, Kestrel v10/v11, fight diagnostic and McRave screening notes. Tracked snapshot replay URLs point at this immutable host.

Bot filters group all versions by canonical identity; Kestrel is explicitly Ours/Original in Matches and Replays. Root reproduced and fixed the initial alias-per-version grouping error. Both filter options verified on the live immutable site, with no desktop overflow; earlier mobile 390 and desktop 1200 checks passed. History charts show exact-build series and conditional intervals; current and historical regimes remain distinct. Credits and author/source links appear in all bot lists. Replay viewer is dgant.github.io/openbw-replay-viewer with direct downloads retained.

This checkpoint is being backed up after **8b4f316**; inspect `git log -1` for its exact commit. It includes completed experiment reports, filters and the reviewed paired runner. Use `scripts/publish_dashboard.sh`; it rewrites tracked `dashboard/data.json` to immutable replay URLs. Never commit relative replay URLs from a local build. HTML JS syntax and 43 Python checks passed. Bulk artifacts, game data and dependencies remain local and ignored.

Production https://starcraft-ai.pages.dev/. Cloudflare Pages Git settings: main, root `/`, build `scripts/build-pages.sh`, output `public`. The heartbeat can continue bounded work after this turn; inspect active workers and exact sessions before resuming.

V11 update: module `e997841c5f173d5218f7599ab60b9dc391335f8a45788f69df3fea3bc740f49c`, runs `20260920T071134-0c1c99b3cdfb` and `20260920T071137-c12df661de50`. Second Gateways current at 2904/2894, complete at 3875/3865, after threat at 3704/3590; primary local overlap one in both. Zero rejected commands, clean losses; REJECT. Patch `patches/kestrel-v7-to-v11.patch`, report under same evaluation ID. First-Gateway timing is a possible next hypothesis, pending evidence review.
