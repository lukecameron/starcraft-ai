# Kestrel v12 pending-first-Pylon reservation plan

## Decision

- Registered: `2026-09-20T07:18:59.327194+00:00`, before compilation or any v12 game.
- Hypothesis: retaining 100 minerals after the first accepted Pylon order until that Pylon becomes current will prevent the stale/retry sequence observed in v7, without stopping Probe production when both costs are affordable.
- Falsification: either valid game accepts more than one build request before the first Pylon becomes current, takes more than 120 frames from first accepted request to current Pylon, or fails a clean-game or production guard.
- Decision: `ADOPT` means retain only the reservation mechanism for broader validation. It does not replace canonical v7 or establish strength. A failed bar is `REJECT`; an infrastructure-invalid attempt with no permitted retry is `INCONCLUSIVE`.

## Change and control

- Control evidence: canonical v7 diagnostic run `20260920T070255-f110c96947fd`. Its first Pylon was accepted at bot frame 942, a Probe was accepted at 972, the same Pylon tile was requested again with another Probe at 1,428, and the Pylon became current only after the retry. The retained 120-frame samples show an affordable 106-mineral checkpoint while the first worker remained stale, but they do not establish every intermediate balance or a unique engine cause.
- Treatment: isolated v12 based on v7. Only while the first Pylon is the accepted pending build and no Pylon is current, Nexus Probe training requires at least 150 minerals rather than 50. This leaves 100 minerals available for the Pylon. Probe training proceeds normally at 150 or more and immediately returns to v7's 50-mineral rule once the Pylon is current. Existing pending-build timing/retry logic, supply thresholds, Gateway/gas/Core order, scouting, targeting, and combat are unchanged.
- Telemetry only: first Pylon accepted/current/completed frames, accepted first-Pylon build-request count, first Gateway current/completed frames, first Zealot train/completed frames, first visible/detected ground attacker capable of attacking within 12 tiles of home, its public unit-type ID, and accepted home-defense attack-command timing/count.
- Source identity: combined source SHA-256 `006bc89ce5d7df71a374492ad86fcf3d519ff9d4d85dc752e1c4ec2b1e0436b6`; v7-to-v12 patch SHA-256 `99d4e059558abd0ec51181f9145fb9adf2c266a0cd0d24ac17db586fa8e5a913`. Prelaunch review added the explicit `firstPylonCurrentFrame < 0` historical guard so the reservation cannot reactivate after a later Pylon loss; this occurred before either trial and changed the frozen source and patch identities above, without changing the registered mechanism or gates.
- Build identity recorded at `2026-09-20T07:21:24Z`, before launch: native module SHA-256 `cb91e9217c99099e2683603ab4220e1b2154d162df3ff8b62cb61a78deac3b8b`; official BWAPI 4.4 header compile passed with Apple Clang 21.0.0. The frozen package is `artifacts/builds/cb91e9217c99099e2683603ab4220e1b2154d162df3ff8b62cb61a78deac3b8b/kestrel-v12-pylon-reservation/`.

## Fixed execution

- Exactly two games, serial and once each: v12 Protoss as player 1 versus frozen ZZZK Zerg on Benzene seed `6103`, then Heartbreak Ridge seed `6104`.
- Adopted engine `eee406…`, LF3, empty isolated learning state, 120-second cap, no bot seeds, retries, replacement games, or adaptive changes.
- Minimum sample size and stop: both games. Preserve every attempt; stop after an infrastructure-invalid attempt because retries are not registered.
- Invalid only for nonzero launcher exit, timeout, missing/inconsistent callbacks, state-hash mismatch, missing required telemetry, or unreadable replay. Gameplay losses and failed policy bars remain valid.

## Metrics and gates

- Primary mechanism metric per game: `first_pylon_current_frame - first_pylon_accepted_frame`, in logical frames from bot telemetry. Both values must exist, `first_pylon_build_requests` must equal `1`, and the difference must be between `0` and `120` inclusive in both games. The experiment passes only if both games pass.
- Clean-game guard: zero launcher exits, reciprocal callbacks, no state-hash mismatch, two fully parsed replays, and at least 384 durable logical frames/s in each game. Throughput only validates package operation and is not a performance claim.
- Production guard: each game continues Probe production after the reservation, reaches a completed Pylon, current and completed Gateway, accepted and completed Zealot, scouting and combat/home-defense command evidence, fewer than 5% rejected commands, and no wrong-race production. Report exact timing even when the guard fails.
- Descriptive fields: first Gateway and Zealot timing, first home attacker and home-defense commands, outcome, terminal frame, worker/army maxima, and replay production sequence. No win, survival change, or two-game outcome can promote strength or override the mechanism decision.
