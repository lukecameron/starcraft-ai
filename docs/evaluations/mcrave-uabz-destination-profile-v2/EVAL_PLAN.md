# McRave versus UAlbertaBot Zerg late-game CPU profile v2

Registered 2026-09-20T07:23:44Z, before launch or sampling.

Version 1 failed before game initialization because its OpenBW LOCAL socket launch ran under the default sandbox. It produced no gameplay, telemetry, PID, replay, sample, or outcome evidence. This independently registered evaluation keeps the same frozen inputs, diagnostic question, metrics, and bars, while explicitly requiring escalated local command execution so the LOCAL socket can be created. It does not replace or revise the v1 record.

## Frozen trial

Run exactly one serial match on `sscai/(2)Destination.scx` with frozen McRave 9Pool candidate `fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa` as player 2 Zerg and frozen UAlbertaBot `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9` as player 1 Zerg. Use frozen engine `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`, engine seed 9202, McRave bot seed 9202, empty per-player learning state, and a 120-second wall cap. Launch the command with escalated local execution. No concurrent game, build, replay playback, or profiler is allowed.

After player 2's durable `diagnostic.json` first reports `frame_count >= 15000`, record the exact player-2 PID from the runner's live manifest and invoke `/usr/bin/sample <pid> 10 1` exactly once. Record the detected frame, PID, command start and end timestamps, exit status, and hashes of the raw report and capture metadata under `artifacts/experiments/mcrave-uabz-destination-profile-v2/raw`. Do not retry if the match ends early, PID resolution is ambiguous, sampling setup fails, or the requested live duration is incomplete. Preserve the full game artifacts in every case.

This sampled run is diagnostic only. Exclude its outcome, elapsed time, FPS, CPU, and memory from throughput and strength evidence.

## Hypothesis and decision rule

The working hypothesis is that one cohesive McRave main-thread subsystem, expected most plausibly to be Combat navigation/pathing or Grids, accounts for at least 20% of samples after frame 15,000. The purpose is to identify the narrowest source hotspot that warrants a later semantics-preserving diagnostic; this plan authorizes no implementation.

Use all sampled main-thread stacks as the denominator. Build a mutually exclusive partition from outermost source subsystem branches so primary shares sum without double counting. Report inclusive descendants such as BWEB path generation separately as overlapping drill-down evidence. Keep unresolved or symbol-poor stacks explicit.

PASS requires all of the following: the trigger is reached before termination; the exact McRave-side PID is sampled live for the full requested ten seconds; the report contains at least 1,000 main-thread samples; and one nonoverlapping cohesive subsystem accounts for at least 20% of the main-thread denominator with symbols specific enough to recommend a narrow source investigation. Otherwise the result is INCONCLUSIVE. Match completion, terminal integrity, crashes, hash mismatches, and profiler perturbation are reported separately and do not convert this run into throughput or strength evidence. No retry is permitted.
