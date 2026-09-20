# Resume

Checkpoint: 2026-09-20 05:09 UTC. The latest replay-viewer request is complete and live. The broader bot project remains ongoing; a quota decision is pending.

## Resource decision

Weekly usage has **10% remaining** as of 05:08 UTC. Three reset credits are unused. An async question is pending asking permission to use **one credit expiring 21 September at 10:21 am Sydney time** when remaining usage reaches 10%. The tool threshold is now met, but the user has not answered that explicit approval question. Do not redeem without the answer. Heavy usage is authorized, but the reset tool requires per-credit confirmation. The normal weekly reset is 26 September at 20:56 Sydney. Finish this source/publish checkpoint, then avoid starting another substantial agent run until the resource decision.

## Current builds and conclusions

- Retain reference McRave Zerg `c49ee3c4b20a2772f1bfca03249c182d32a7238f9453a7a568990a188a1c4c65` (`config/baseline.json`). No robust competitive strength incumbent or calibrated local Elo has been adopted.
- Canonical McRave checkout remains the unadopted coordinate/goal-cache source corresponding to `98df2632…`. Later experiments are isolated and frozen.
- Latest experimental production McRave is **04521befa41bb3873783b215493abf3a071414d2a5315cdea68fc7a67f4415ec**, at `artifacts/builds/<sha>/mcrave-as-memo-candidate/McRave.dylib`. Full source patch: `patches/mcrave-as-memo-candidate.patch`, SHA2d7b64f1…. It adds per-search pure-callback memoization on top of bounds candidate ddc0415. Native and all114 official-header translation units compile. Its shadow matched13,611 valid paths and two invalid probes with91.02% fewer callback evaluations.
- **quick-mcrave-as-memo-v1 REJECT:** ten clean wins, no crashes/timeouts/hash mismatches/conflicting outcomes, and20 hash-checked, parsed replays. Aggregate413.1fps passed, but games6–9 missed the384 per-game bar; minimum269.5fps. Exact completed runner session3299. No retry or replacement. Preserve raw ledger; source schedule retains a documented copied descriptive title/count error, while operational inputs and the separate preregistration are correct.
- Prior bounds candidate ddc0415 also REJECT: ten clean wins,373.9 aggregatefps, six below384. Prior coordinate/cache98df batch INCONCLUSIVE:9/10 clean and one conflicting-winner game. The c49 first batch was INCONCLUSIVE:7/10 clean, engine crash and two timeouts. These trajectories differ, so do not infer causal speedups or strategic improvement.
- **Stardust provisional local opponent:** our repaired fork **1039975842c6edea71043e0da091ff21ad5311fd3ddbeb568cf89b364f7d28aa**, frozen under `artifacts/builds/<sha>/stardust-emptytimer-repair/`. Full source patch `patches/stardust-emptytimer-repair.patch`, SHAcd3a3555…. Original port b6097c9a crashed its first cohort game and remains rejected. Diagnostic c1afd9a5 confirmed producer timer-set exhaustion. The conservative fallback fork passed its one repair probe and all four registered compatibility games, aggregate2059.4fps, with no hash mismatch or consumer fallback and plausible replay production. Config/opponents.json points to the repaired artifact. It does not inherit upstream BASIL Elo. Original author Bruce Mackenzie Nielsen is credited; derivative tournament submission still needs written permission.

## Latest profile and next work

One registered late-game profile used production04521, diagnostic engine27ea, Destination/UAlbertaBot Terran, engine and McRave seed3001, candidateP1. Run `20260920T050142-3662b2986e1a`, runner session75876, exact candidatePID95545. Match completed normally in57.718s at19998frames with opposing outcomes and two replays.

The sample followed frame15120 and contains7165 main-thread observations. Combat1706(23.81%), Grids1351(18.86%), Support842(11.75%); all observed generateAS398(5.55%). Combat ground march/retreat contexts566(7.90%) and Support enter JPS. Parent/child categories overlap and must not be summed.

**Formal profile decision is INCONCLUSIVE:** raw header05:02:31.475 versus target completion05:02:40.585 leaves only9.110s, so the required10s of live sampling is unproved. A successful sample exit and complete-looking report are insufficient. Preserve counts as partial evidence and do not retry this registered experiment. `harness_sol` corrected the derived analysis/report; raw sample SHA849538f82dbccb9ea295d48bc6bd2d912e010e2765381469a4ca7a17462ea657 remains unchanged. No further build/game is running.

The next bounded investigation should count why Combat ground march/retreat and Support paths regenerate (changed endpoints, validity tests, map state), then choose a semantics-preserving optimization from that evidence. Do not introduce cross-frame caches speculatively or optimize more A* merely because it was the previous hotspot. Source also contains shadowed Navigation locals, but that is a separate untested policy issue.

## Engine, dashboard and operational state

- Canonical repaired enginef1a32e5a remains unchanged. Experiments use logging-only engine27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb at `artifacts/builds/<sha>/openbw-kill-path-diagnostic/` (flat files). Historical reciprocal winners remain unclassified/unscored. Do not implement a speculative acknowledgement-only shutdown barrier.
- Pages: https://starcraft-ai.pages.dev/, main, build`scripts/build-pages.sh`, output`public`, root`/`. Wrangler is authenticated and publishing authorized. Replay links use **https://dgant.github.io/openbw-replay-viewer/?url=<encoded-public-replay-url>**, with direct downloads. Actual browser playback was verified. Our originals/ports/forks carry author/source links throughout the dashboard.
- Generic runner advice is now `runner_notes`, so it cannot erase reviewed verdicts/conclusions.31 Python tests passed; local and live browser regression checks passed. Completion hooks publish batches; reviewed conclusions are published after analysis. Immutable replay URLs in tracked dashboard/data.json preserve access through clean Git builds.
- Last pushed source commit before final checkpoint: **ac33c2a**. Final manual publication: **29b42bb1.starcraft-ai.pages.dev**, completed session68035, with111 runs and28 experiments. The corrected INCONCLUSIVE profile is browser-verified. This checkpoint is backed up by the next main commit.
- No agent game/build remains active. Local dashboard HTTP server session85590 serves127.0.0.1:8787 and is idle; no replay playback tab is active. Temporary browser test tabs were closed. Game data, frozen binaries, samples and replays remain local/ignored and preserved.
- Official-header compile checks pass for McRave114, UAlberta115, Stardust147+16 translation units. This is not Win32 DLL or original-game runtime proof. Keep portability work within the brief's credible restoration path.
- Main backups and Pages publishing are authorized. No contact, tournament submission, paid services, or reset redemption is authorized implicitly by this checkpoint.
