**Project brief: build the strongest practical competitive BWAPI bot**

Prepared 20 September 2026. This document is a standalone assignment for an autonomous development agent. It includes the engineer’s constraints, delegated decision authority, and working practices. Implementation choices and the research sequence remain yours.

**Your mission is to maximize credible competitive playing strength.**

Build and improve a StarCraft: Brood War bot with the highest achievable Elo under the constraints below. Optimize for strength that transfers to the BASIL opponent population and official BWAPI execution. Use headless OpenBW as the primary development, training and evaluation environment.

This is an ongoing empirical optimization project, not a request to guarantee a world record or deliver a predetermined architecture. Produce a working baseline quickly, identify its largest weaknesses from evidence, and keep improving the strongest validated version. Favor measurable playing strength per unit of engineering effort and compute. Infrastructure should make that loop faster or more trustworthy.

Choose the race, language, starting codebase, engine fork, architecture, algorithms, training methods and tools. A single-race bot is acceptable. There is no requirement to build from scratch, use machine learning, use WASM, support every race, provide a GUI, or introduce a distributed service. Native OpenBW on ARM64 is entirely acceptable and may be preferable to WASM. Decide from evidence.

**You have broad authority to act within these constraints.**

Make reasonable implementation decisions without asking the engineer to choose between routine options. Research, inspect dependencies, create branches, implement, refactor, build, profile, run bounded experiments and revert unsuccessful changes autonomously. Record consequential decisions and their rationale in the repository. Prefer reversible choices and isolate experiments from the current best build.

Ask the engineer when unavailable essential resource, paid service, external permission or substantial quota shortage needs their decision. Prepare concrete options and finish all independent useful work first. Preparing a tournament submission is in scope; contacting people or publicly submitting a bot requires existing authorization or a separate engineer decision. Do not stop merely because a minor implementation detail is unspecified.

The engineer will be away from their computer, so consider that asking a blocking question will potentially waste a day or more. This is a huge waste. Consider if a question is truly blocking based on rules above, make a decision with listed assumptions (log it somewhere), and proceed.

**The following constraints govern every design decision.**

| Constraint | Required outcome |
| --- | --- |
| Competitive deployment | A build complying with current BASIL/SSCAIT submission and runtime rules must remain achievable. The actual tournament build need not work continuously, but restoring it must remain a credible few days of development, not a rewrite. |
| Primary runtime | The bot runs complete matches under OpenBW. Routine development and evaluation use this environment. |
| Headless operation | Matches can be launched, advanced, scored and archived unattended without a window, renderer, audio device or human input. |
| Primary machine | An M5 Max MacBook Pro with 128 GB memory. Verify the actual local environment and available tools when work starts. |
| Portability | Preserve a realistic ARM64 development path and official-game Windows/BWAPI deployment path. Avoid making gameplay depend on a proprietary accelerator or host-specific service. |
| Deployment resources | Bot execution must fit the competition’s single-core and approximately 1 GB total environment envelope, including its applicable overhead. Leave headroom; do not treat all memory as available to the policy. |
| Machine learning | Allowed for training, evaluation and deployed decisions. The deployed policy must satisfy the same CPU, memory, package-size and timing limits as other code. |
| Simulation throughput | Keep representative headless evaluation capable of at least 16× realtime on the primary development machine. Establish compute budgets before adding expensive features. |
| Fast feedback | Aim for roughly five-minute hypothesis-to-feedback iterations. Maintain an approximately ten-game quick evaluation using a BASIL-derived opponent gradient. |
| Evidence retention | Preserve every generated replay and enough provenance to build a replay database later. Preserve failed-game records even when no valid replay can be produced. |
| Agent orchestration | Delegate liberally according to the model allocation and quota policy below. |

Development can use the Mac’s available cores and memory for independent matches, compilation, analysis and offline training. These resources must not quietly become requirements of the deployed bot. Accelerated offline training is allowed; accelerated inference is not a prerequisite for the competition build.

**Recheck the live competition rules at the beginning and before packaging.**

At preparation time, BASIL publishes BW 1.16.1, normal latency setting LF3, one Ryzen 7 1700X core, 1 GB RAM minus OS usage, and 100 MB total across `ai`, `read` and `write`. Network access is generally prohibited. It specifies a 30-minute wall timeout and a 60-minute game limit with score adjudication, and says it does not enforce a per-frame timeout. Treat these as a dated rules snapshot; source the exact semantics again rather than inferring them from game-clock labels. [BASIL rules](https://www.basil-ladder.net/rules.html).

SSCAIT’s submission rules additionally cover supported official BWAPI binaries, source and executable delivery, filesystem access, slow-frame losses, information restrictions and derivative-bot eligibility. Its rules page contains legacy platform and tournament text. The homepage now says SSCAIT no longer runs matches and submissions feed BASIL. Resolve the applicable current requirements using the live venue documentation; retain uncertainty explicitly. Do not silently apply AIIDE/CoG rules to this project. [SSCAIT rules](https://sscaitournament.com/index.php?action=rules), [current status](https://sscaitournament.com/).

Create a small compliance matrix with the requirement, source URL, verification date, local enforcement method, current status and remaining work. Include command latency, information visibility, accepted API version, file persistence, crashes, timeout adjudication, forbidden exploits and source/licensing obligations. Rule interpretation should be traceable.

Reuse is encouraged when it improves the outcome, but benchmark-opponent availability and permission to submit a derivative are different questions. Check both licenses and venue restrictions before committing to a base bot. For example, Stardust explicitly places conditions on competition submissions of forks. Prefer a viable alternative when permission would block progress. [Stardust](https://github.com/bmnielsen/Stardust).

**Make the tournament pathway concrete without maintaining it continuously.**

Keep gameplay decisions behind an interface that can be supplied by both OpenBW and official BWAPI. The exact architecture is your decision. Do not let simulator-only facilities become essential information or capabilities of the deployed policy.

Early in the project, perform a bounded compatibility spike: identify the target official BWAPI release, executable/module format, toolchain, dependencies and packaging route; compile a minimal representative slice if the environment permits. Capture actual obstacles. If original-game execution is unavailable, distinguish “compiled,” “statically reviewed,” and “runtime verified.”

Maintain a compatibility-debt list with affected components, restoration steps, evidence and an effort estimate. Interpret “a few days” as approximately two to three focused engineering days. Temporary build breakage is acceptable. An unknown port, unavailable inference runtime, dependency on privileged engine state, or wholesale policy rewrite is not an acceptable pathway.

Review this list after architectural changes and at meaningful milestones, especially when adding libraries or ML runtimes. Restore the official-game lane before its debt exceeds the allowance. Continuous Windows CI is optional. A credible documented path is mandatory; a statement that portability should be easy is insufficient.

Engine evaluation access and policy access must be separated. It is acceptable for an evaluator to inspect complete state to determine outcomes or diagnose a failure. The bot may use only legally available observations and its own history. Hypothetical rollouts may use inferred hidden state, never privileged live enemy state. Keep such distinctions testable.

**Define 16× realtime numerically and measure the complete cost.**

Use 24 logical simulation frames per reference second as this project’s explicit convention, independently of the renderer, host polling rate or game-clock display. Under that convention, 16× means at least 384 logical frames per wall second, or approximately 2.60 ms of wall time per simulated frame. Preserve competition command latency while running the simulation faster; do not skip engine updates or discard required bot work to inflate throughput.

Maintain two separate budgets:

- The candidate bot’s deployed cost: CPU time, callback tails, peak memory, startup cost, persistent data and binary/model size.
- The local match’s end-to-end cost: initialization, engine, both bots, adapter, harness, result capture and replay persistence, measured from launch to durable completion.

Start with the following engineering defaults, then profile and adjust the internal allocation while preserving the hard constraints:

| Measurement | Initial budget or reporting requirement |
| --- | --- |
| Full-match throughput | At least 16× on a fixed representative headless suite on the primary Mac. Report each match, aggregate throughput and the slow tail; opening-only benchmarks do not qualify. |
| Candidate decision work | Aim initially for no more than 0.5 ms CPU per frame amortized on the primary Mac, with p99 callbacks around 1.5 ms or less. These are design budgets, not quoted tournament limits. |
| Planning spikes | Bound work and make it interruptible or deferrable where practical. Report maximum callback time and rolling cost across short and longer frame windows; averages must not conceal stalls. |
| Bot memory | Start with a target below 512 MiB attributable to bot code, state and inference, then validate whole-environment headroom under the actual deployment cap. |
| Threads and accelerators | Default deployed computation to one CPU thread; constrain library thread pools. Any alternate mechanism must still be measured within one core’s total budget and accepted rules. |
| Local parallelism | Run independent matches concurrently only while each worker’s throughput, memory and thermal behavior remain healthy. Report per-match speed as well as total throughput. |

Initialization and terrain preprocessing are measured separately as well as in end-to-end totals. In an in-process build, whole-process RSS includes the engine and potentially both bots: report the scope honestly rather than pretending it is the candidate’s isolated footprint.

Use realistic late-game armies, difficult maps and expensive decision situations in performance checks. A fast opening with a tiny army is not sufficient evidence. Identify when an opponent is the bottleneck; do not silently weaken it or remove its cost from the reported end-to-end rate. Improve scheduling, porting or cohort selection transparently.

Passing on the M5 Max does not prove tournament performance on older x86 hardware. Obtain a representative x86 measurement when practical. Until then, use a conservative, explicitly uncertain estimate and maintain headroom. Before claiming tournament readiness, verify the packaged bot on the intended original-game runtime under the applicable resource limits. CPU throttling and a single microbenchmark are not proof of equivalence.

**Build an opponent gradient grounded in BASIL, then validate it locally.**

Use the [BASIL ranking](https://www.basil-ladder.net/ranking.html), [crosstable](https://www.basil-ladder.net/crosstable.html), bot repositories and available competition archives to assemble a reproducible opponent cohort. Select across the available rating range, with coverage of races and strategically distinct styles. Avoid a cohort dominated by related forks or a single rush strategy.

Derive bucket boundaries from the observed rating distribution rather than inventing current bot ratings. Begin with enough runnable opponents to get a gradient, then expand where coverage is weak. Prioritize reliable, relatively inexpensive OpenBW ports. Use stronger opponents as the candidate improves, while retaining cheap diagnostic anchors.

For each opponent record:

- Identity, race, strategic style where known, source URL, license and immutable version/hash.
- BASIL rating and its exact displayed meaning/scale, observation date, available match count and uncertainty about matching the downloaded version.
- OpenBW/API versions, native/WASM build route, required patches and headless test status.
- Learning-state initialization, random seeds, command latency and any other behavior-affecting settings.
- Runtime cost, replay support, known gaps and a clear compatibility status.

Treat names such as ZZZKBot, McRave, Steamhammer/UAlbertaBot, Stardust and PurpleWave as research leads, not a guaranteed compatible or legally reusable roster. Existing ZZZKBot/McRave WASM work is useful evidence, but neither it nor a bot’s language establishes compatibility with your chosen native runner. [OpenBW bot port notes](https://github.com/heiner/openbw/blob/master/web/bot/README.md), [additional web ports](https://github.com/danglade/openbw).

A bot must actually complete representative games with plausible behavior before it becomes a rating anchor. Check missing API features, race visibility, startup behavior, disabled file learning and scheduling changes. Correct compatibility errors before estimating strength. Do not label a crippled port with its original BASIL rating.

Run a small anchor-versus-anchor calibration initially and after relevant engine/port changes. Grow it only when it resolves uncertainty. Record the difference between a ladder rating and an inferred local rating; do not force local results to reproduce the ladder’s ordering.

If current rating data, exact versions or sufficient compatible bots are unavailable, keep building the harness with provisional opponents and report the limitation. Use dated evidence where available. Never fabricate Elo buckets or claim a complete calibrated gradient prematurely.

**Provide quick approximate Elo without promising precision that ten games cannot supply.**

The required fast mode should normally use about ten complete games to provide a coarse strength bracket, regression signal and actionable failure examples. Ten games cannot guarantee accurate absolute Elo; report an estimate or bracket with uncertainty and its provenance. Distinguish “BASIL rating,” “BASIL-calibrated local estimate,” and “uncalibrated local league estimate.”

The agent may choose the rating model and scheduler. Useful properties are:

- Opponent selection focused near the candidate’s current estimated strength, with some easy/hard anchors and rotating race/style coverage.
- Balanced maps and starting locations over successive batches, with a recorded schedule and selection policy.
- Reuse of previous evidence for the exact same candidate version/configuration and evaluation regime, without counting cached games as new observations.
- Conservative handling of evidence from predecessor builds; an old posterior must not masquerade as measurements of changed code.
- Calibration uncertainty, crash/timeout outcomes and nontransitive matchups visible alongside a scalar score.

Use a frozen schedule or matched scenarios when comparing a change with the incumbent. Cached incumbent results are acceptable where the engine, inputs and learning-state regime match; otherwise rerun what is necessary. Repeating an identical deterministic outcome does not create independent evidence.

Maintain three levels of evaluation:

| Level | Purpose | Typical use |
| --- | --- | --- |
| Targeted probe | Reproduce a failure, profile a hotspot or test a local decision | One scenario or a few short checks; these are not full-game Elo results. |
| Quick match batch | Detect large gains, regressions and the next weakness | Roughly ten games, mostly against informative nearby opponents. |
| Promotion/validation batch | Decide whether an apparent gain generalizes | A larger sequential test sized to the remaining uncertainty; use held-out opponents/maps and stop once the decision is clear. |

Do not automatically run hundreds of games after every patch. Escalate only when the expected value of more evidence justifies the time. Avoid winner’s-curse promotion from repeatedly selecting lucky ten-game batches. Preserve a best validated build and a separate current experiment.

Reserve some opponent/map combinations for periodic validation instead of tuning on every available result. As practical, cross-check milestone builds on the original game and eventually against real BASIL results. Do not merge records from different engines or rulesets as if they were identical trials.

Every quick report should include build identity, opponents, maps, score, uncertainty, crashes/timeouts, performance, worst regressions and replay links. A useful output ends with a concrete recommendation: promote, reject, investigate a particular failure, or collect a specific additional comparison.

**Keep iterations around five minutes and make every simulation answer a question.**

Before an experiment, state the observed problem, proposed change, expected effect, chosen test and stop condition. Choose the smallest test capable of changing the next decision. Inspect existing replays and metrics before launching another broad run.

A normal loop is: inspect one high-impact failure; make one coherent change; run the relevant probe and compact match batch; compare with the incumbent; preserve or revert the change; record the result and next hypothesis. Include compilation and analysis in the iteration budget.

Ten full games do not necessarily fit into five minutes serially. Ten games each lasting twenty reference minutes consume about 12.5 worker-minutes at 16×, before startup and analysis. Use appropriate local concurrency, cached matched baselines and targeted probes. Measure actual elapsed time instead of assuming acceleration guarantees the desired loop.

Do not truncate games and silently score unfinished matches as wins or losses. Apply the selected adjudication rules explicitly. Early-terminated diagnostic runs are labeled incomplete. Every launched game still produces an archival record.

Ambitious work is welcome when split into short measurable checkpoints. Longer runs need a written expected payoff, resource allowance and stopping rule; they need not trigger an engineer interruption when already within authorized resources. Stop low-information simulations, duplicate searches and training that no longer changes the decision.

**Research broadly at the start, then implement the highest-value findings.**

Start with a bounded crawl of [the StarCraft AI wiki](https://www.starcraftai.com/wiki/Main_Page). Delegate discovery to Luna. Follow relevant links and capture a compact index of useful techniques, primary sources, implementation availability and likely relevance. Keep a frontier for later research instead of attempting an unlimited crawl.

Give particular attention to terrain/topology analysis, choke points, expansion placement, combat evaluation and SparCraft, build-order search, opponent modeling, and replay analysis/data extraction. Use the wiki as an idea index: it contains old API versions and stale links. Verify dependencies and claims against current primary repositories before investing in them.

Useful starting points include [BWEM](https://bwem.sourceforge.net/), [SparCraft](https://github.com/davechurchill/ualbertabot/tree/master/SparCraft), [replay/data-mining references](https://www.starcraftai.com/wiki/StarCraft_Brood_War_Data_Mining), and the [competition resource directory](https://davechurchill.ca/starcraft/resources/). Combat simulators are approximate decision tools; validate important conclusions in the actual game engine.

Run independent research tracks where useful: engine and portability; opponents and calibration; strategic/tactical techniques; replay tooling; and selective ML opportunities. Each track should return an actionable recommendation, evidence, uncertainty, expected implementation cost and a small next experiment. Close tracks that do not justify further effort.

Do not front-load a long literature review before obtaining a working match loop. Terrain analysis and richer replay features are candidates to evaluate, not mandated subsystems to build regardless of need.

**Machine learning is optional and must earn its runtime and development cost.**

Use ML where it plausibly provides more strength per unit of effort than a simpler alternative. Possibilities include opening selection, opponent prediction, combat evaluation, scouting decisions, building placement, parameter tuning or compact distilled policies. You may pursue a more ambitious approach when evidence supports it.

Offline training may use multiple cores, available accelerators and substantial memory on the development machine. The deployed artifact must be self-contained, run within the competition CPU/memory envelope, and fit the package and persistent-data limits. It cannot depend on network inference or live engineer/agent decisions.

Estimate feature extraction, inference latency, model size and runtime-library overhead before committing to a model family. Measure on the CPU path intended for deployment. Training throughput and GPU inference speed are not substitutes for that measurement.

Retain a reproducible training recipe, data versions, seeds, model artifact hashes, training cost and evaluation results. Split replay-derived training and validation data so near-duplicate games or shared trajectories do not leak across the split. Keep privileged replay labels separate from features legally available during play.

Compare learned components with an inexpensive baseline and use an ablation when it answers a concrete attribution question. Adopt distillation, quantization, caching or other optimization only when justified. A learned component must improve the constrained deployed policy, not just an unconstrained research configuration.

**Use Astra, Sol and Luna deliberately.**

Assume Astra is available for lead orchestration. Assign big-picture strategy, architecture decisions, ambiguous synthesis, difficult debugging and ML design/diagnosis to Astra where its knowledge materially helps. Delegate the majority of ordinary work to Sol and Luna.

| Model | Default assignments |
| --- | --- |
| Sol | Well-defined implementation, dependency/build fixes, bounded refactors, harness features, targeted tests, profiling tasks and execution of specified experiments. |
| Luna | Cheap exploratory research, the initial wiki crawl, candidate discovery, documentation triage, small reproductions and first-pass log/replay cataloging. |
| Astra | Prioritization, resolving conflicting evidence, hard debugging, complex algorithm design, ML reasoning and high-impact integration decisions. |

Give each sub-agent a narrow question or deliverable, acceptance condition, relevant context, time/compute allowance and ownership of files or branches. Require concrete evidence rather than long activity reports. Run independent tasks in parallel; serialize conflicting edits or use isolated worktrees. The lead integrates and verifies the result.

Do not escalate every uncertainty to Astra. Ask a cheaper agent for a bounded attempt, then escalate with its evidence when the task needs deeper reasoning. Conversely, do not waste repeated cheap attempts on a demonstrated hard blocker. Model assignment can change with task difficulty and quota.

Use the actual model-selection controls provided by the harness. If a named model is unavailable, choose the nearest reasonable available option and disclose that briefly. Never claim a task ran on a model that the tool did not select.

**Monitor quota occasionally with `quota-axi`.**

The engineer expects the CLI `quota-axi` to be installed in the working environment. At startup, discover its supported invocation using local help; do not invent flags. Inspect remaining Codex quota and reset windows. Recheck occasionally, for example after a substantial batch of agent work or roughly every 30–60 minutes, rather than before every task.

Use the most constrained active quota window to guide spending. As remaining quota falls, narrow parallelism, prefer well-defined Sol/Luna tasks, reduce speculative research and checkpoint sooner. Reserve Astra for decisions where it is likely to change the outcome. Suggested adjustable bands are normal operation above 30%, conservative operation around 15–30%, and explicit engineer notification below roughly 15% or whenever estimated remaining work exceeds the available quota.

The engineer may have Codex quota resets available. When quota is becoming a real bottleneck, report the observed remaining amount, relevant reset time, completed evidence, next valuable work and why extra quota would help. Ask whether they want to use a reset; do not consume one yourself or create a reset loop. Continue inexpensive useful work while possible.

If `quota-axi` is unavailable, report that once and continue conservatively using any reliable available quota signal. Do not repeatedly probe, silently substitute a different similarly named tool, or spend significant effort installing it without need. Local simulation/training budgets and model quota are separate resources; monitor both.

**Preserve replays as a future database, starting with the first match.**

Choose a simple directory convention and a machine-readable index. Keep storage local and portable initially; no database server is required. Paths and serialization formats are your decision, but replay identities and references must remain stable.

A reasonable default is:

- `artifacts/runs/<run-id>/` for the run manifest, schedule, aggregate results and experiment notes.
- `artifacts/replays/<YYYY>/<MM>/<DD>/<run-id>/<game-id>.rep` for each replay.
- A sidecar per game for result, provenance, metrics and relative artifact paths.
- Separate versioned stores for opponents, maps, models and learning-state snapshots, referenced by hash.

Preserve replays from wins, losses, calibration, self-play, training matches and failed or interrupted games whenever the engine can emit them. Do not keep only highlights or losses. If output is missing or corrupt, preserve the metadata/logs and the reason. Verify replay generation and playback/parsing early; a custom command log must not be mislabeled as a valid `.rep`.

The record for each game must be sufficient to identify and, where supported, reproduce it:

- Unique run/game IDs, schema version, timestamps and experiment purpose.
- Candidate and opponent source/binary/configuration hashes, race and model identity.
- Engine and API revisions, build options, execution backend and target platform.
- Map identity/hash, starting positions, seeds, latency, rules and adjudication settings.
- Initial learning-state references and subsequent state/output references where relevant.
- Result, termination reason, logical frame count, wall time, throughput, CPU timings and peak memory with measurement scope.
- Replay/log paths and hashes, archival status, and references to known nondeterminism.

Write records incrementally and finalize them safely so a harness failure cannot erase an entire batch. Support retrieval by build, opponent, map, result and experiment without parsing every replay. Retain raw data alongside derived features; version extraction code and schemas. Hash-based deduplication and lossless compression are allowed if all game records remain represented and replay bytes remain recoverable.

Keep replay archives outside the tournament bot’s restricted persistent directories and memory budget. The local harness owns archival I/O; the deployed bot writes only permitted bounded data. Exclude bulk artifacts from normal source commits and monitor disk growth. If retention becomes costly, report it and propose storage changes; do not silently delete old games.

**Deliver useful milestones and maintain a recoverable state.**

Sequence these according to evidence, overlapping independent work where helpful:

1. A bounded research/source inventory, live rule snapshot, measured environment and decision on an initial engine/bot route.
2. A complete unattended headless match on the primary Mac, valid replay output, resource measurements and a documented tournament compatibility pathway.
3. A versioned OpenBW-compatible opponent gradient, compact evaluation command and honest approximate-strength report.
4. A first measured improvement over the chosen baseline, backed by replay evidence and a larger check when the effect is uncertain.
5. Continued strength improvements, held-out validation and periodic portability/resource checks; a tournament-ready package when that milestone is selected.

Keep the following easy to find: setup/build/run instructions; current best build and reproducing command; experiment ledger with accepted and rejected hypotheses; opponent/rating manifest; performance report; compliance/compatibility debt; known engine gaps; and the next few highest-value tasks. Keep documentation proportional to its use.

Before a long run, quota exhaustion or context handoff, checkpoint source changes and write a short resume note describing what is running, where results will appear, what has been learned and the next decision. Never leave the next agent to infer the current best build from a directory of artifacts.

Progress reports should lead with strength changes and confidence, then runtime cost, important failures and the next experiment. Do not claim tournament readiness from OpenBW-only testing, statistical improvement from one lucky batch, or a precise BASIL Elo from uncalibrated local games.

Work autonomously toward the strongest validated bot until the engineer redirects you, a genuine external blocker remains, or the resource budget requires a decision. Keep the project in a runnable, inspectable state throughout.


**Project management and github**

You may create lukecameron/starcraft-ai. Don't create other repositories. This repo should be public. Don't commit secrets.

Use `main` as the trunk. You may use branches and pull requests if desired, but keep in mind that you are the sole developer. You can use PR as a way of having subagents review each other's work, but there are no human team members, and if PRs get raised it is your responsibility to get them merged.

Commit and push your commits whenever meaningful progress has been made. You don't have to overdo it, just to keep the code for the bot and research materials backed up.

Data that is derived from publically fetched data, or the binary replay data we accumulate can stay on local disk - I as the engineer will arrange its backup at a later date, just keep it well-organised to make that job easier for me.
