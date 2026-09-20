# McRave same-state goal-cache shadow plan

This evaluation compares the original repeated-distance selection, the proposed invocation-local cache, and the actual original gameplay selection inside each real non-flyer goal-assignment call. All three receive the same ordered units, positions, eligibility, target, type, and requested count before gameplay mutation.

Both shadows use `DBL_MAX`, strict `<`, and original iteration order. Locally selected units become ineligible in subsequent shadow steps. `setGoal` and `setGoalType` affect only the selected unit's goal fields, so they cannot change another unit's eligibility. The actual gameplay path remains the upstream repeated `getClosestUnitGround` helper loop; the shadows issue no command and retain no cross-call state.

The validator aggregates all calls, choices, distance-call counts, and separate timings. It retains the first call, first call with at least 20 eligible units and requested count at least 10, maximum-coverage call, and the complete first divergence. Summaries flush periodically. The 180-second Destination game uses engine and bot seed 4301, McRave Zerg versus UAlbertaBot Terran at LF3.

Pass requires zero divergence between both shadows and actual gameplay plus at least one qualifying large-state invocation. Instrumentation timing is evidence about distance-call work only and is not production throughput. No result establishes strength or promotes a binary.
