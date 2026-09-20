# McRave memoized A* late-game CPU profile

Registered 2026-09-20T05:01:21Z, before launch or sampling.

## Frozen trial

Run exactly one serial match: production memo candidate `04521befa41bb3873783b215493abf3a071414d2a5315cdea68fc7a67f4415ec` as player 1 Zerg against frozen UAlbertaBot Terran on Destination, engine seed 3001, McRave bot seed 3001, and frozen diagnostic engine `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb`. The wall cap is 120 seconds. No concurrent build, game, replay playback, or profiler is planned.

After player 1's durable progress metadata first reports `frame_count >= 15000`, resolve and record the exact player-1 launcher PID from the runner's process tree and working directory. Invoke `/usr/bin/sample <pid> 10 1` exactly once, requesting ten seconds at one-millisecond intervals and writing the complete raw report under `artifacts/experiments/mcrave-memo-late-profile-v1/raw`. Do not retry if the match ends first, PID resolution is ambiguous, sample setup fails, or the sample is incomplete. Preserve the run and every partial artifact.

## Question and analysis rule

Which cohesive subsystem accounts for at least 20% of sampled main-thread stacks at this later state, and how much remains in BWEB `generateAS`, Grids, and other Combat work?

Use the sample report's main-thread sample count as denominator. Count an observed sample once in each reported inclusive category, but construct the primary subsystem partition from mutually exclusive outermost branch roots so its shares can be summed without double counting. Within a primary branch, report inclusive nested hotspots such as `BWEB::Path::generateAS` as drill-down shares and state that they overlap their parent. Keep unresolved/symbol-poor samples explicit. Do not add sibling and descendant counts together. Cite exact symbols and raw counts.

The result is descriptive for this one process, scenario, machine and late-game window. It neither changes strategy nor measures full-match production throughput. PASS means a complete sample after frame 15,000 identifies at least one cohesive source subsystem at or above 20% with enough symbols to recommend a specific next source investigation. Early match completion, ambiguous PID, fewer than the requested sample duration, insufficient symbols, or no qualifying subsystem is INCONCLUSIVE. No retry and no code change follow automatically.
