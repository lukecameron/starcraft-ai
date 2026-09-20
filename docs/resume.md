# Resume

Checkpoint: 20 September 2026, 06:40 UTC. Continue the user's 24-hour autonomous development request through **21 September 05:52 UTC** unless redirected or resources require a decision. User personally redeemed the reset; do not consume another. Their latest status question about the original bot was answered: Kestrel works but has not beaten a real benchmark bot; now moving from command reliability to early-army strategy.

## Authorization, resources and processes

- Main backups and Cloudflare Pages publication are authorized. No contact, tournament submission, purchases or additional reset redemption.
- Quota last checked06:45 UTC:59% remaining (41% used). Recheck around07:15, then every30–60 minutes. Two credits remain, requiring explicit per-credit approval.
- Heartbeat `starcraft-development-while-away`: every30 minutes,48 runs, deadline in prompt. Inspect exact agents/sessions before starting anything. Stop follow-up at the deadline. Preserve all failed attempts/replays.
- **harness_sol active:** four serial McRave opening diagnostic cells. Final cell session **35070** (seed6301, Benzene) just launched. Earlier runs `20260920T063857-4d53d8292099`, `20260920T063934-d495601949d7`, `20260920T064006-320cd0c4815e`, all rc0. No other games until this window releases. Diagnostic module3314c66d…; plan `docs/evaluations/mcrave-zvz-opening-probe-v1/EVAL_PLAN.md`. Root handles publication/identity.
- **engine_sol active:** Kestrel v7 passed. Next source/build task is first-Zealot priority vs ZZZK, with matched v7 controls and held-out seed/map criteria; awaiting its preregistered frozen candidate. Hold games until grant. Supply-cap change is a separate later hypothesis.
- **opponents_luna completed:** local rating cohort metadata and chart. Root integrated/refined. Available for bounded discovery.
- Lead: fresh24-game calibration fully reviewed; preparing next12 missing-edge comparisons (not yet registered/launched). Next compare Stardust–ZZZK, McRave–UAlbertaP and McRave–UAlbertaT on current engine. Do not pool old-engine results.
- Local server session85590/PID1285 at127.0.0.1:8787 serves public. Chrome CLI works while Mac locked; do not bypass lock. Current browser preview immutable250463df, desktop1200; mobile390 and desktop tested. CUA native cannot unlock.

## Validated engine

**ADOPT for new development:** engine `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`, launcher `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`. Paths in `config/engine.json`; full build route `docs/engine-terminal-drain.md`. Full patch `patches/openbw-terminal-drain.patch`, SHA787c642705c8181ac814ce68d44709e07a20116a5f02a0ad0950998e4ec5f2a8. Sources third_party/{openbw,bwapi}-terminal-drain; frozen flat package artifacts/builds/<engine-sha>/openbw-terminal-drain with verified sidecar.

Fixed a reproduced early peer-disconnect race after natural defeat. Ordinary queued commands from a defeated player are discarded before execution/replay recording; remote transport survives until explicit leave/normal cleanup. Existing hash/control/error handling remains. Old27ea could report two winners when winner closes after Select while loser is one frame behind.

Six registered regressions/controls passed; four targets exercised the branch. All12 replays parsed and1,380,602 commands matched through shared final frame (excluding LeaveGame and parser annotations). `docs/evaluations/openbw-terminal-drain-v1/RESULT.md`. New24-game rating cohort also completed cleanly. This is not proof of all engine paths or Win32 runtime. Oldf1/27ea packages and frozen schedules remain preserved. scripts/engine-build.sh still builds the historical foundation; current doc gives direct rebuild.

## Original bot Kestrel

Independent MIT Protoss policy, `bots/kestrel/`, author Luke Cameron. Registry Ours/Original. Native and official BWAPI4.4 header compilation pass; no Win32 runtime. Public BWAPI observations only. Build/history/reconstruction instructions: `docs/kestrel-bot.md`, `scripts/build_kestrel.sh`, tracked reverse patches. Keep canceled unrunv1/v3/v6 artifacts documented.

**Current command/lifecycle baseline v7:** `2facbf970d4a4fd131564d3d02cd3966bcadc50e13e08256a1a92d3886013d3e`, frozen package `<sha>/kestrel-v7`. Public canTrain legality check removed all rejected train commands. ZZZK run `20260920T063735-568f09f7d3a0`: clean loss,2944fps,3 zealots,zero rejected commands. UABT `20260920T063750-d32c98d8cbcc`: clean loss,1465fps,max28 probes/5 pylons/4 gateways/5 zealots/10 dragoons,4% rejected (gather Unit_Busy only); zero attack/train rejection. Both replay pairs parsed. Registered gates PASS, no strength promotion. Result `docs/evaluations/kestrel-train-legality-v7/RESULT.md`.

Earlier v0 failed production. v2 `144d01bc…` beat WorkerRush and completed lifecycle but16 construction commands failed the12-command bar. v4/v5/v6b all lost real benchmark games and failed command gates; retain results. v6b stable targets improved attack acceptance but training busy/supply errors dominated; responsiveness timing remained inconclusive. v7 fixes training legality only.

Next: earlier first combat unit against ZZZK. Luna observed v5 Pool845/first enemy lings2087 vs Kestrel Gateway2006/first Zealot train3404. Agent must inspect actual v7 timing before registering new controls. Later separate macro defect: hard5-pylon cap creates49 supply ceiling. Do not mix both changes or treat timing improvement as demonstrated win-rate improvement. Agent has source/build authorization, games await registered plan/window.

## Local ratings

Gaussian-prior Bradley–Terry MAP,400 Elo SD, approximate95% Laplace contrast intervals and200/800 sensitivity. ZZZK1000 is arbitrary, not BASIL. Exact module/race/AI-config nodes and engine/game-data/platform/latency/learning/timeout regimes. Invalid, unreviewed, duplicate and diagnostic games excluded. Final manifest hashes in `config/local-ratings.json` gate inclusion after replay review.

**Current v2: ADOPT display cohort**,24/24 clean across4 maps, all48 replay hashes/parses/owner-frame/race checks pass. Full report `docs/evaluations/local-calibration-v2/RESULT.md`; local review JSON under same artifact experiment. Fixed modules: Stardust103997,McRave04521,ZZZKce796,UAB75ac P/T. Current estimates (conditional intervals): Stardust1278.8[737.3,1820.3],ZZZK1000 reference,McRave747.8[368.0,1127.6],UABP640.4[136.6,1144.1],UABT616.7[166.7,1066.7]. Stardust12–0; ZZZK7–1; McRave1–11; both UAB variants2–6. UABT–UABP split2–2 across maps. No direct Stardust–ZZZK edge or McRave–UAB edges yet; fill these next. Aggregate726.5fps,min351.1, descriptive only with build overlap.

Historical v1:9 clean/3 reciprocal-winner invalid,12-attempt gate REJECT. Remains separate old27ea component. Old and new ratings are not a before/after strength comparison. Cohorts are coverage metadata only: later cohorts with same exact regime pool cumulative evidence; different regimes separate. Explicit current flag drives UI, not label text.43 Python tests pass, including same/different-regime cohort handling.

## Fork work

McRave reference remains c49ee3c4… in config/baseline.json; no robust strategic incumbent promotion. Canonical checkout98df is unadopted. Full frozen04521 A* memo fork used for ratings. Preserve full patches and source identities.

Support JPS work: diagnostic shadow5860af09… run061222-aea159a208bb had16,773 comparisons,zero path/distance/reachability mismatches,65.65% fewer callback evaluations. Only diagnostic equivalence supported; production candidate436cfa74… then **REJECTED** engineering gate. Nine clean wins/one old-engine two-winner invalid; four valid games<384fps,all-attempt377.5/clean366.7fps. Result docs/evaluations/mcrave-support-jps-memo-quick-v1/RESULT.md. Secondary comparable rows showed4–12% CPU/frame reductions, not sufficient for adoption. Full candidatepatch patches/mcrave-support-jps-memo-candidate.patch.

Current diagnostic3314c66d7f88fc5e04f5ad5d1dadd38e88ba852830cc9b3731b7977e8defdbc3 derives experimental436c. Four cells cross seeds1001/6301 with Benzene/Heartbreak, fixed McRaveP1 vs ZZZK. Full patch SHA125e859d…; sidecar5965f321…; native/114official TUs passed. Telemetry will distinguish opening selection from map-dependent execution delay; no strategy treatment yet. Registered adequacy includes clean cells and same-seed opening invariance; do not silently relax if it fails.

Stardust103997 repaired fork is currently the strongest local opponent, with custom tournament-derivative permission constraints. Do not contact or submit. Author Bruce Mackenzie Nielsen. Repaired empty upgrade-timer producer passed earlier compatibility tests. No upstream BASIL rating transfer.

## Dashboard and backups

Latest verified immutable publication **https://250463df.starcraft-ai.pages.dev/**, publish session40769 complete:175 runs,48 experiments,320 replay files. Exact-build local history charts with conditional intervals, current/historical cohort counts, full provenance and responsive390/1200 layout. Current cohort defaults in selector. Ownership/origin/author credits remain on all bot lists. Replay viewer dgant.github.io/openbw-replay-viewer, direct downloads retained.

Main latest pushed was **e61153e** before this checkpoint; subsequent changes await next commit. User has authorized directmain backups and Pages. Use scripts/publish_dashboard.sh; it rewrites tracked dashboard/data.json replay links to immutable URL. Never commit relative replay URLs after a local build. Current snapshot from completed publish is absolute. Current HTML JS syntax and43Python checks pass. All raw artifacts,dependencies,game data remain ignored/local.

Production https://starcraft-ai.pages.dev/, main/root `/`, scripts/build-pages.sh outputpublic. Recent Kestrelv7 final notes and final McRave diagnostic notes may postdate latest publication; add reviewed config/experiments records and publish after those results. README now points at current engine/current24-game cohort; docs preserve historical outcomes.
