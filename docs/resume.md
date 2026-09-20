# Resume

Checkpoint: 20 September 2026, 06:18 UTC. The user personally redeemed a usage reset and authorized another 24 hours: more accurate Elo, a from-scratch bot, fork improvements and the dashboard. Continue through **21 September 05:52 UTC** unless redirected or resources require a decision.

## Authorization and resources

Weekly quota was 100% available at 05:52 UTC; two unused reset credits remain. Do not consume another without per-credit authorization. Recheck around 06:22 UTC and every 30–60 minutes thereafter. Main backups and Pages publishing are authorized; contact, tournament submission, purchases and implicit reset redemption are not.

Thread heartbeat `starcraft-development-while-away` runs every 30 minutes for 48 runs, with a deadline in its prompt. Inspect exact agents/processes before launching anything; do not duplicate work. Checkpoint and stop the follow-up at the deadline. Coordinate game windows, especially performance tests. Preserve all attempts/replays, including invalids.

## Active work and next windows

- Lead: engine repair build session **59040 completed**. Four-game target batch **session5369 active**, using `config/openbw-terminal-drain-targets-v1.json`; ledger under the matching experiment ID. First two were clean Stardust wins at the last check. Two controls still need to run: `config/openbw-terminal-drain-control-mcrave-v1.json` and `config/openbw-terminal-drain-control-stardust-v1.json`. Exactly six total, 180s cap, concurrency2, no replacements. No adoption yet.
- After engine suite, grant **engine_sol** its registered Kestrel v5 two-game probe, then **harness_sol** its registered ten-game Support JPS production gate. Both are frozen and waiting. Read messages before dispatch.
- **opponents_luna** completed engine source review and awaits acknowledgement to add exact-build local Elo history charts in dashboard/index.html. First publication is complete, so it can proceed independently now.
- Local dashboard server: session85590, PID1285, `127.0.0.1:8787`, serving `public`. Chrome devtools CLI works headlessly despite the locked Mac; current preview is the immutable Pages site with390px mobile emulation. Do not bypass the lock.

## Kestrel: original Protoss bot

Our independently written MIT bot lives in `bots/kestrel/`, author Luke Cameron; registry labels Ours / Original. Public standard BWAPI only. Native and official4.4 header checks pass, not Win32 runtime. `scripts/build_kestrel.sh` and `docs/kestrel-bot.md` cover builds and exact history. Reverse patches from current v5 reconstruct v0/v2/v4 byte-for-byte; canceled v1/v3 stages remain documented.

- v0 `a1cb8aa8…`: run `20260920T060144-b9ed2a9e5aad`, clean loss to WorkerRush, repeated building commands and no army. Lifecycle failed.
- **First working lifecycle reference v2:** `144d01bc11e64dfdb37113f0e8f79d397846c09373331244ca6563ca8e6d4495`, package `<sha>/kestrel-v2`. Run `20260920T060713-1258ac57a72c` beat WorkerRush and produced workers, buildings, zealots and dragoons. Lifecycle passed;16 build commands exceeded12, so overall REJECT. Fixture is not a rating anchor.
- v4 `e93b84a0392d67a6fcf48f4349bc13c701ae38a68d34823a137ae9afd8ff3865`: clean losses vs ZZZK (`20260920T061023-430740c71f57`) and UABT (`20260920T061035-54dd2cefee96`). Both above384fps, but71% rejected commands in UAB game failed command quality. See `docs/evaluations/kestrel-benchmark-probe-v4/RESULT.md`.
- **Pending v5:** `eec8734a731d3184b002f069dd1356e995bc9a9422762bd5a8bd488f51655f89`, package `<sha>/kestrel-v5`. Per-unit request state: immediate target-change response,96f successful refresh,24f failed retry, clear disappeared target. Native/official pass. Two matched input games await grant; primary UAB rejection<25% plus per-row/lifecycle criteria. Preserve registered bar.

## Local ratings and calibration

`config/local-ratings.json`, `scripts/local_ratings.py`, `docs/local-ratings.md`. Gaussian-prior Bradley–Terry MAP,400 Elo SD, approximate95% Laplace contrast intervals,200/800 sensitivity. Exact module+race+AI-config nodes; exact engine/game-data/platform/rules regimes stay separate. Connected components never share a ranking. ZZZK1000 is a display coordinate, not BASIL. Reviewed manifest hashes gate inclusion after replay parsing; duplicates and invalids stay unscored.41 Python tests passed, including independent grid/curvature and identity/deduplication checks.

Initial `local-calibration-v1`: all12 attempted on previously unused Heartbreak Ridge/Circuit Breaker; **9 clean /3 conflicting winners**, so clean-cohort gate REJECT. All24 replays hash-checked, parsed, owner-frame/race checked. Nine accepted games connect five nodes in old engine27ea's partial league. Local estimates: Stardust1083[312,1854], ZZZK1000 reference, UAB Protoss769[34,1504], McRave579[−76,1233], UAB Terran449[−262,1161]. Broad overlapping intervals, no promotion. Full report: `docs/evaluations/local-calibration-v1/RESULT.md`.

McRave lost both Heartbreak Ridge games to ZZZK and one clean Circuit Breaker game to Stardust. Earlier10/10 on Benzene/Destination did not generalize. `mcrave-loss-analysis.md` observes pool/lings about600 frames later than one Benzene win, but seeds6301 vs1001, slots and maps confound cause. Next opening probe should instrument selected opener/timing before a strategy change.

## McRave and Stardust forks

Retain McRave reference `c49ee3c4b20a2772f1bfca03249c182d32a7238f9453a7a568990a188a1c4c65` in `config/baseline.json`. Canonical checkout still unadopted98df; later work isolated. No robust competitive incumbent yet.

Production04521 (`patches/mcrave-as-memo-candidate.patch`) won10/10 old quick games but failed384fps per-game in four (aggregate413.1,min269.5): REJECT. Bounds ddc0415 also rejected. Do not infer causal speedup across different trajectories. Late profile remains INCONCLUSIVE: only9.110s target lifetime after sample timestamp versus required10s.

Subsequent path diagnostic passed: run `20260920T060444-344951b48e0f`,103.791s, clean. Support generated24,676 paths,23,795 unreachable (96.43%). See `docs/evaluations/mcrave-path-regeneration-v1/RESULT.md`.

**JPS shadow PASS:** run `20260920T061222-aea159a208bb`, session39543 completed62.656s.16,773 comparisons, zero reachability/bit-distance/ordered-path mismatches.211,081,633 raw callbacks vs72,506,005 memo evaluations (−65.65%).16,220 failures actually searched; only26 cheap rejects. Timers4.409s vs2.011s are biased diagnostic evidence, not production speed.

**Pending Support-only production candidate:** `436cfa74fa34c267f7404777a3170be0202485bdc7224d15fb30b85f02c5644e`, package `<sha>/mcrave-support-jps-memo-candidate`. Full patchSHA5d4c99a7…, incremental44a0ebae…. Fresh cache per opted-in search, allocated after cheap rejection. Existing endpoint/bounds/JPS semantics retained; no cross-frame caching; other callers off.114 source TUs, no diagnostic/untracked compiled files; native/official pass. `docs/evaluations/mcrave-support-jps-memo-quick-v1/EVAL_PLAN.md` uses old engine27ea and established10 scenarios; every game and aggregate >=384 durablefps. Waiting after engine/Kestrel windows.

Repaired Stardust `1039975842c6edea71043e0da091ff21ad5311fd3ddbeb568cf89b364f7d28aa` remains a provisional opponent, original author Bruce Mackenzie Nielsen. Earlier four compatibility games passed at2059 aggregatefps. Its license requires written permission for derivative public tournament submission; no contact authorized. No upstream BASIL rating transfer.

## Engine repair under test

Three calibration failures: `20260920T055717-7842246af878`, `20260920T055717-5eafb5ffe760`, `20260920T060312-129fdb979771`. Winner-side engine closes an already defeated peer on Select(action9); the peer one frame behind receives EOF before its own defeat and also wins. No hash mismatch/crash. Earlier clean games closed on LeaveGame(action87) after defeat was observed.

Candidate full patch `patches/openbw-terminal-drain.patch`, SHA `787c642705c8181ac814ce68d44709e07a20116a5f02a0ad0950998e4ec5f2a8`. It discards an already defeated player's ordinary queued commands before execution/replay recording, retains remote transport and consumes the queue, and preserves explicit LeaveGame/control/error handling. Local terminal clearing remains. Luna reviewed queue safety; compare common replay action prefixes and hashes. This is not an acknowledgement-only game-over barrier.

Candidate engine **`eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`**, launcher `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`. Sources `third_party/{openbw,bwapi}-terminal-drain`; build logs/sidecars in `artifacts/experiments/openbw-terminal-drain-v1/`; frozen package `<sha>/openbw-terminal-drain/`. Canonical f1a32e5a and diagnostic27ea unchanged. Acceptance:6/6 clean, deferred branch exercised, both controls pass, all replays parse. New engine means a new rating regime; old invalid games stay unscored.

## Dashboard and backups

Latest **https://82334421.starcraft-ai.pages.dev/** (publication session62685 complete):131 runs,37 experiments,228 replay files. Partial league, exact hashes, ownership/origin/author links, intervals, prior sensitivity, cumulative history and390px mobile cards verified. A small wording fix after publication remains local. Exact-build history chart is next with Luna.

Production https://starcraft-ai.pages.dev/. Pages main/root `/`, build `scripts/build-pages.sh`, output `public`. Use authorized `scripts/publish_dashboard.sh`; it rewrites immutable replay URLs in tracked dashboard/data.json. **Never commit relative replay URLs.** Viewer is https://dgant.github.io/openbw-replay-viewer/ with direct-download fallback; playback verified earlier.

Main was3b72ec9 before this turn. New source/docs/config/tests are awaiting backup. Do not stage ignored game data, builds, raw artifacts or replays. All raw failures/successes remain local. Official-header builds do not prove Win32 DLL or original-game runtime; preserve the documented restoration path.
