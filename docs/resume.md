# Resume

Checkpoint: 20 September 2026, 07:47 UTC. Continue the user's autonomous development request through **21 September 05:52 UTC** unless redirected or resources require a decision. User redeemed a reset personally; do not consume another. Their status question about the original bot was answered: Kestrel works end-to-end, but has not beaten a benchmark bot. V13 is now the accepted construction-correctness baseline; opening strength still needs improvement.

## Authorization and ongoing work

- Direct `main` backups and Cloudflare Pages publication are authorized. No contact, tournament submission, purchases or additional reset redemption.
- Quota checked about 07:39 UTC: **22% remaining** (78% used). Conservative mode: finish and checkpoint the current eight-game performance screen, reduce speculative work and long lead turns, and recheck around 08:10. Do not redeem a reset. Notify the user if below about 15% or essential work exceeds remaining quota. Two credits exist but are not authorized for redemption.
- Active heartbeat `starcraft-development-while-away`: every 30 minutes, 48 scheduled runs, deadline in saved prompt. Inspect exact agents/sessions before launching anything. Stop follow-up at the deadline. Preserve all failed attempts and replays.
- **engine_sol finished:** v13 session12179 completed and passed its registered correctness checks. Lead adopted canonical v13 after source review and independent final-manifest calculations. No active Kestrel build/game. Do not duplicate the completed probe.
- **harness_sol active screen:** exact session **66424**, runner PID **88241**, candidate `da737a4e6435d42f21378a0a84b56f480062026d119d3e2de11126bd041f79d2`. Registered four-pair/eight-game performance screen under `docs/evaluations/mcrave-grids-bounds-performance-v1/`; plan SHA `261fae8eacae2476e40aabe9183f51b66f54d4376adf526f88ad3898b85958fd`, schedule SHA `7635521a28f9bf963409fea5eb31c62b71aca4ee8855005923a0b2116befae8c`. Lead released publication and authorized launch. Twenty-minute cap, immediate stop on any invalid attempt, no concurrent game/build/profiler. Control fd174, UABZ75ac, current engine; Benzene9201/P1, Destination9202/P2, Benzene9203/P2, Destination9204/P1, alternating arm order. Aggregate CPU/frame<=95% control, no pair>110%, RSS<=105%, no additional candidate losses, all eight clean. Advance-to-validation only; report the 384-fps floor separately. First four attempts completed valid; inspect the exact session and durable paired ledger for newer results. Finish current screen and checkpoint; no further variants/confirmation without next review. **64-game strategy confirmation remains unlaunched.**
- **opponents_luna idle:** bounded timing analysis agreed the first Gateway-to-Zealot pipeline is now the earliest target. No edits/builds/games. Engine agent will check resource feasibility before another policy change.
- Root owns `config/experiments.json`, `docs/kestrel-bot.md`, this resume and publication. Avoid overlapping edits without handoff.
- Local HTTP server session 85590, PID 1285, serves `public` at 127.0.0.1:8787. Chrome CLI works while Mac is locked; do not bypass the lock. Current browser is immutable 4d385b42, desktop 1200. Prior mobile 390 and desktop layout checks passed.

## Current engine

**Adopted:** engine `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`, launcher `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`. Exact paths in `config/engine.json`; rebuild route `docs/engine-terminal-drain.md`. Frozen flat package under `artifacts/builds/<engine-sha>/openbw-terminal-drain/`. Patch `patches/openbw-terminal-drain.patch`, SHA `787c642705c8181ac814ce68d44709e07a20116a5f02a0ad0950998e4ec5f2a8`.

The repair discards ordinary queued commands from defeated players before execution/replay recording and retains their transport until explicit leave or normal cleanup. It fixes the reproduced old-engine reciprocal-winner failure. Hash/control/error handling remains. Six registered targets/controls passed; all 12 replays parsed and 1,380,602 common commands matched. Subsequent 36 calibration games and 16 strategy screening games completed cleanly. This is not proof of all engine paths or Windows runtime.

Old f1/27ea packages, invalid results and schedules remain preserved. `scripts/engine-build.sh` builds the historical foundation; the current engine document gives the direct rebuild route.

## Kestrel, our original bot

Independent MIT Protoss policy, author Luke Cameron, `bots/kestrel/`, registry Ours/Original. Only public BWAPI observations. Native and official BWAPI 4.4 header compilation pass; official Win32 runtime remains unverified. Build and reconstruction instructions: `docs/kestrel-bot.md`, `scripts/build_kestrel.sh`.

**Canonical accepted v13 development baseline:** module `622bca47b47f78f3e9d1971d1e340f991b54ced7f3bfdfd932d3062e125cbd98`, package `<sha>/kestrel-v13-gas-worker-guard/`, source `12cecdb5039569711c318bab5bb6781b4f1e86e22c87e453f9d85c295fa13df0`. Canonical source matches the evaluated package byte-for-byte; config/kestrel-baseline.json points to it. Two games exercised gas-worker exclusion1/7 times, with no gas-worker build attempts or build Unit_Busy, total rejection3.57%/3.41%, clean parsed replay pairs and2953/1633fps. Both lost; adoption is construction correctness, not strength. Runs `20260920T073627-856dcb721664` and `20260920T073629-a6ad5ae88993` (the earlier d64 token in a message was erroneous and has no run). Reverse patch `patches/kestrel-v13-to-v7.patch` restores v7 before applying older history patches.

Historical v7 remains frozen as module `2facbf970d4a4fd131564d3d02cd3966bcadc50e13e08256a1a92d3886013d3e`, source `34f43843f762ed32c7052eda64e324db8fe6b4204dd48f94692d84df5d2b18f1`. Rejected candidates and diagnostic source remain isolated and reconstructible.

V7 passed command checks: zero train or attack rejections in two full losses. ZZZK run `20260920T063735-568f09f7d3a0`: 2,944 fps, max 3 Zealots. UAlberta Terran `20260920T063750-d32c98d8cbcc`: 1,465 fps, max 28 Probes, 4 Gateways, 5 Zealots and 10 Dragoons; 4% gather-only command rejection. V2 beat the WorkerRush diagnostic, but no Kestrel version has yet beaten ZZZK or UAlberta. Do not call Kestrel a rating anchor or a competitive success.

Recent rejected candidates:

- V8 `fd799d9e…`: first Zealot train 396 frames earlier, but both games failed lifecycle/survival bars. Current-count reservation could reactivate after army loss; recorded deviation, unadopted.
- V9 tested `cf3e8409…`: six-Probe worker defense executed legally, but both games lost earlier with less army. Unrun `7518…` was corrected before launch for builder/defender role conflict. Keep both identities.
- V10 `2c029177…`: delay gas/Core until four queued/current Zealots against known Zerg. Both games had zero rejected commands, but third train advanced only 132 frames against the registered 200-frame bar; no fourth Zealot queued, max two completed. REJECT. Forward patch `patches/kestrel-v7-to-v10.patch`.

**Latest diagnostic:** isolated instrumentation-only v7 `084160cc9afcee500a54a851f434388c462ab00d81aa60536f47ab217f68d1ef`, run `20260920T070255-f110c96947fd`. Clean loss, two parsed replay copies. At frame 3,720 there were 166 minerals, an unfinished first Zealot and five local Zerglings. First Zealot attacked at 3,740 and died at 3,823. Second Gateway only requested at 3,672; second Zealot attacked at 4,580 and died at 4,725 against at least eight lings. The units engaged locally but separately. Gas was already built/staffed; no Core or Dragoon realized. This supports an earlier-capacity experiment, not a general causal or strength claim. Full evidence `docs/evaluations/kestrel-fight-diagnostic-v1/RESULT.md`, patch `patches/kestrel-v7-fight-diagnostic.patch`, public trace SHA `e3f7e880f12155ddc0006b745169a268e27994fb58bc7e793f2e4773ca8e41f4`.

Earlier replay analyses distinguish scout contact/death from home exposure. Attack destinations alone do not prove arrival. V11 tested completed-defender overlap and failed. A separate later macro defect is the five-Pylon cap (49 supply); do not mix it into opening experiments.

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

Latest completed publication **https://4d385b42.starcraft-ai.pages.dev/**, session 80994, approximately 07:41 UTC: 226 recorded matches, 66 experiments and 418 replay files. Includes Kestrel v13 adoption, rejected v12, worker-state diagnostic, UAlberta Zerg compatibility limits, both profile attempts and bounds-shadow evidence. Tracked replay URLs point at this immutable host. Chrome verified data HTTP 200, the ADOPT conclusion, both v13 runs with Ours/Original provenance, and replay download HTTP 200. A prior Python urllib fetch returned 403; the normal browser succeeded.

Bot filters group all versions by canonical identity; Kestrel is explicitly Ours/Original in Matches and Replays. Root reproduced and fixed the initial alias-per-version grouping error. Both filter options verified on the live immutable site, with no desktop overflow; earlier mobile 390 and desktop 1200 checks passed. History charts show exact-build series and conditional intervals; current and historical regimes remain distinct. Credits and author/source links appear in all bot lists. Replay viewer is dgant.github.io/openbw-replay-viewer with direct downloads retained.

Previous pushed main is **7d90074**; the next checkpoint contains the v13 baseline, reconstruction patches, all completed reports above, the performance plan/schedule and published snapshot. Inspect `git log` and status for the exact backup commit and any later agent-written result. Use `scripts/publish_dashboard.sh`; it rewrites tracked `dashboard/data.json` to immutable replay URLs. Never commit relative replay URLs from a local build. HTML JS syntax and 43 Python checks passed before this checkpoint; v13 also passed native/official-header compilation and its two real-engine checks. Bulk artifacts, game data and dependencies remain local and ignored.

Production https://starcraft-ai.pages.dev/. Cloudflare Pages Git settings: main, root `/`, build `scripts/build-pages.sh`, output `public`. The heartbeat can continue bounded work after this turn; inspect active workers and exact sessions before resuming.

V11 update: module `e997841c5f173d5218f7599ab60b9dc391335f8a45788f69df3fea3bc740f49c`, runs `20260920T071134-0c1c99b3cdfb` and `20260920T071137-c12df661de50`. Second Gateways current at 2904/2894, complete at 3875/3865, after threat at 3704/3590; primary local overlap one in both. Zero rejected commands, clean losses; REJECT. Patch `patches/kestrel-v7-to-v11.patch`, report under same evaluation ID. First-Gateway timing is a possible next hypothesis, pending evidence review.

Latest opening evidence: first Pylon accepted 942 (replay 944), Probe trained 972, original builder remains PlaceBuilding through frame 1200 despite 106 minerals. Probe 1278; retry 1428 (replay 1430) uses a different Probe at the same tile (111,15), then construction starts. Accepted build orders do not reserve minerals. Resource starvation/stale order is a testable hypothesis; 120-frame snapshots do not prove no affordable intermediate instant. See `docs/evaluations/kestrel-opening-resource-analysis.md`. V12 tests that mechanism before another Gateway threshold.

V12 final module `cb91e9217c99099e2683603ab4220e1b2154d162df3ff8b62cb61a78deac3b8b`, final source `006bc89ce5d7df71a374492ad86fcf3d519ff9d4d85dc752e1c4ec2b1e0436b6`, patch `99d4e059558abd0ec51181f9145fb9adf2c266a0cd0d24ac17db586fa8e5a913`. Runs `20260920T072208-a970044c0407` / `20260920T072210-f1bde9483beb`; all clean and four replays parsed. Preserve fixed-bar REJECT despite only one accepted Pylon order in each game; 289-frame delay may include travel and should not be attributed uniquely without evidence.

Profile trigger correction: archived capture.json and trigger-diagnostic.json record frame18,720; a prior live observation was reported as15,120. Use the archived value for reproducible evidence. Both exceed the registered15,000 trigger; full ten-second live sampling evidence is unchanged.

Worker diagnostic confirmed gas-state conflict: build requests at3738/3744 reused worker137 during HarvestGas and returned Unit_Busy; no same-cadence gather occurred. The same worker could build during ReturnGas at3750. V13 excludes public isGatheringGas() in both retained-builder reuse and availableProbe, including refinery travel/return phases; this is based on v7, not rejectedv12. Build-specific error telemetry was added before trials to avoid confusing gather errors with build errors.
