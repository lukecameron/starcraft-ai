# McRave post-cache profile v1

## Registration

- Experiment: `mcrave-post-cache-profile-v1`
- Registered: `2026-09-20T04:00:22.187548Z`
- Status: preregistered; no trial launched

## Question and hypothesis

Which source subsystem now dominates McRave's main thread after the goal-distance cache and Station-coordinate correction?

The hypothesis is that the old repeated goal-distance search is no longer the dominant stack and that one remaining cohesive McRave, BWAPI, or OpenBW subsystem accounts for at least 20% of main-thread samples. The result falsifies that hypothesis if no cohesive subsystem reaches 20%; it will then be reported as dispersed work. Visual-only work is measured explicitly from stacks containing `Visuals::drawInformation`, its drawing/formatting callees, or BWAPI draw calls reached from it. It is material only if it reaches the same 20% threshold.

This is a diagnostic characterization. It does not control adoption and cannot support a speed or strength claim.

## Frozen trial

One trial reproduces the slowest successful completed game in `quick-mcrave-coordinate-cache-v1`:

- Source run: `20260920T035642-481cbf8ab37d`, batch game 8
- Map: `sscai/(2)Destination.scx`
- Player 1: McRave Zerg, slot 1, frozen module SHA-256 `98df26327cba498ac6ea1759d00b748f63870c655b34ecad6e24eb0e6851f1df`
- Player 2: UAlbertaBot Terran, slot 2, frozen module SHA-256 `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`
- Engine/library package: SHA-256 identity `f1a32e5a3dc64b8c62a17788488d36594dd95b13ef124637795b5aca4c846c42`
- Scenario seed: `3001`
- McRave bot seed: `3001`; no player-2 bot seed
- Wall cap: 120 seconds

The scenario inputs match, but the game can follow a different global trajectory because OpenBW/BWAPI object traversal is not globally deterministic. The trial is still useful for locating CPU work in the state it reaches; it is not a paired performance comparison.

## Measurement protocol

Launch the normal match runner once, with no source, policy, or configuration changes. Track the exact player-1 launcher PID from that run's live manifest. Poll player 1's diagnostic frame counter. At the first observation at or above frame 10,000, sample that exact PID with macOS `sample` for 10 seconds at a 1 millisecond interval. No compilation or other planned game runs may overlap the sample.

If the process exits or the match ends before sampling starts or completes, preserve the trial and report insufficient sampling. Do not retry and do not sweep another seed.

Record:

- full sample output and SHA-256;
- main-thread sample count and inclusive counts grouped by cohesive source subsystem;
- any single symbol or cohesive main-thread subsystem at or above 20% of main-thread samples;
- inclusive visual-only count and fraction;
- player-level user/system CPU and peak RSS from the match manifest;
- frame count, elapsed/durable time, exit status, diagnostics, replay, and all runner logs.

Sampling and polling add overhead. FPS, wall time, and CPU are descriptive only. Inclusive stack categories can overlap and therefore are not summed as exclusive shares.

## Stopping and interpretation

The minimum and maximum sample size are one registered trial. Stop after it, whatever the outcome. Report a major hotspot only when a single symbol or cohesive main-thread subsystem appears in at least 20% of sampled main-thread stacks. Otherwise report dispersed work. A run without a completed 10-second sample after frame 10,000 is `INCONCLUSIVE` for the primary metric.
