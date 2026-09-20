# McRave Grids walk-bounds same-input shadow result

**PASS.** The shadow compared 1,757,500,992 real `Grids::addToGrids` walk-circle inputs and found zero disagreements between BWAPI's authoritative `WalkPosition::isValid()` result and the direct predicate using dimensions initialized by `Grids::onStart`. All eight boundary and invalid-sentinel comparisons also agreed.

## Build and source evidence

The isolated module SHA-256 is `55961f04637d731038584b0cb22e04ec4372e48f51579c0b5e9726b61ad32692`. It compiled natively and compiled all 114 translation units against official BWAPI 4.4 headers. The frozen full-source patch SHA-256 is `925ffbc005d45f2ca4d8bc67f2d915cbabf2deed33319d83dec191e3f6fb7af4`; the incremental instrumentation patch SHA-256 is `644161cf760e0f43c319e64d2778868937f44315657a3cbd187374637a44a5d7`. Its binary-matched sidecar records the frozen `fd174fa…` base and declares the module diagnostic-only.

The comparison runs immediately after the existing authoritative call on the same `WalkPosition`. Only the authoritative result controls `continue`; the direct result affects counters and diagnostic output only. `initializeLogTable()` caches `mapWidth() * 4` and `mapHeight() * 4` before the eight sentinel checks. The sentinel set covers negative x/y, origin, the final valid corner, each one-past edge, one-past both dimensions, and BWAPI's invalid sentinel.

## Game evidence

Runner session `31487`, run `20260920T073257-1a4397fbfe6b`, completed in 87.944 seconds. The terminal shadow summary reports frame 28,833, map walk dimensions 384 by 512, 1,757,500,992 gameplay checks, zero gameplay mismatches, eight sentinel checks, and zero sentinel mismatches. Its SHA-256 is `85a4188dc48643a97e623f7758d37bba60e558f9f45b69854cf7a1399c1438c7`.

Both launchers returned 0, terminal metadata was opposing, `outcome_verified` was true, and both replay copies were archived. The only kill diagnostics were the reviewed terminal-drain pair: loser-side `transport_callback` and winner-side `controller_not_occupied_after_action`. There was no hash mismatch, crash, timeout, or unrelated kill source. McRave won, but the outcome is not strength evidence.

The summary writes every 100,000 comparisons, so the diagnostic performed roughly 17,575 atomic writes during the game. Its elapsed time, CPU use, memory, and FPS are therefore invalid as production performance evidence. The pass establishes predicate equivalence for this exact call site and scenario only. It supports review of a production replacement that removes the shadow, counters, sentinels, and diagnostic I/O; it does not establish a speedup or show that the separate 256-by-256 visibility scan is equivalent to any proposed replacement.
