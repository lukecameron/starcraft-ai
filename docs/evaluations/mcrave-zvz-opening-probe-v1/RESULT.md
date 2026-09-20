# McRave ZvZ opening-selection and execution probe result

**Result: ADEQUATE OBSERVATIONAL EVIDENCE.** All four preregistered games completed with opposing terminal results, no process failure, no reported sync-hash mismatch, and durable telemetry through the first Pool and Zergling. The selected tuple was stable across maps for each seed and differed between seeds: seed 1001 selected `PoolLair / 9Pool / 1HatchMuta`; seed 6301 selected `PoolLair / Gaspool / 1HatchMuta`.

The roughly 600-frame delay previously associated with the seed-6301 Heartbreak Ridge loss follows opener selection. On Heartbreak Ridge, Gaspool requested the Pool 505 frames later, started it 560 frames later, and first observed a Zergling 559 frames later than 9Pool. Within a fixed seed/opener, changing maps moved first-Zergling timing by only 51 frames for 9Pool and 62 frames for Gaspool in these observations. This identifies seed-associated opener selection as the main source of the earlier timing difference; it does not establish that either opener is stronger.

## Registered cells and evidence

| Cell | Seed | Map | Initial and final tuple | Pool requested | Pool started | Zergling pump requested | First Zergling | Result |
|---|---:|---|---|---:|---:|---:|---:|---|
| 1 | 1001 | Benzene | PoolLair / 9Pool / 1HatchMuta | 967 | 1508 | 2436 | 3178 | win, frame 16154 |
| 2 | 1001 | Heartbreak Ridge | PoolLair / 9Pool / 1HatchMuta | 983 | 1574 | 2460 | 3229 | win, frame 16061 |
| 3 | 6301 | Heartbreak Ridge | PoolLair / Gaspool / 1HatchMuta | 1488 | 2134 | 2624 | 3788 | loss, frame 6079 |
| 4 | 6301 | Benzene | PoolLair / Gaspool / 1HatchMuta | 1455 | 2074 | 2617 | 3726 | loss, frame 7257 |

For 9Pool, Heartbreak Ridge minus Benzene was +16 frames at Pool request, +66 at Pool start, and +51 at first Zergling. Its request-to-start interval was 541 frames on Benzene and 591 on Heartbreak Ridge; Pool-start-to-first-Zergling was 1670 and 1655 frames respectively. For Gaspool, the same comparison was +33, +60, and +62 frames; request-to-start was 619 and 646 frames, while Pool-start-to-first-Zergling was 1652 and 1654 frames. The near-identical final interval within each opener gives no evidence of a material map-specific post-Pool production delay in these four cells.

All manifests report `status: completed`, `outcome_verified: true`, `termination_reason: children_exited`, exit-clean launchers, and two archived replays. All eight replay copies still match their manifest SHA-256 and parse structurally with screp 1.13.4. Each header reports two Zerg players on the expected map, and its final frame is one less than its owning callback frame. This is header evidence, not playback validation. The retained details are in `replay-validation.json`. No stderr contained `insync_hash_mismatch`, a kill-source diagnostic, or an exception.

- Cell 1: `artifacts/runs/20260920T063857-4d53d8292099/game-0001/manifest.json`
- Cell 2: `artifacts/runs/20260920T063934-d495601949d7/game-0001/manifest.json`
- Cell 3: `artifacts/runs/20260920T064006-320cd0c4815e/game-0001/manifest.json`
- Cell 4: `artifacts/runs/20260920T064021-77d0cb29d7ec/game-0001/manifest.json`

## Source interpretation

With an empty learning file, ZvZ defaults to `PoolLair / 9Pool / 1HatchMuta`, but learning still scores candidates with a `rand() % randomness` term (`Source/McRave/Builds/All/Learning.cpp`, lines 99-103 and 122-170). The ZvZ candidate set explicitly permits the three PoolLair openers 9Pool, Overpool, and Gaspool (lines 364-371). The selected opener then dispatches to distinct build-order functions (`Source/McRave/Builds/Zerg/ZvZ/ZvZ_PoolLair.cpp`, lines 58-66). In particular, 9Pool requests the Pool at supply 18, whereas Gaspool first requests a second Overlord and Extractor and only requests the Pool once an Extractor is visible (lines 29-55). The observed request order and timing match those source contracts.

## Limits and next test

Each map/opener cell has one observation against one opponent, and engine seed changed with bot seed as preregistered. The evidence isolates the selected tuple within these controlled cells; it does not estimate win rate, generalize a map effect, or justify forcing an opener. The next strategy evaluation should hold engine/map starts fixed and compare 9Pool and Gaspool through a diagnostic-only forced-selection mechanism or shadow decision, then preregister enough independent games to measure survival and win outcomes. No learning policy or production command changed in this probe.
