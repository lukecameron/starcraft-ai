# Kestrel v16 early-Pylon plan — NOT RUN

- Registered: `2026-09-20T08:09:44.724066+00:00`, before compilation or gameplay.
- Status: source-only checkpoint. No V16 module was compiled and no game was launched.
- Question: when V15's two-Gateway opening faces a known Zerg opponent, does prioritizing the first Pylon at six completed Probes move the full production sequence early enough for two completed local Zealots to overlap before the first local Zealot dies?
- Evidence: V15 requested its first Pylon at frames `990` and `1224`, completed its second Gateway at `3433` and `3506`, completed its first Zealot at `3275` and `3509`, and lost the first local Zealot at `3859` and `3987`. The second Gateway therefore existed but could not finish a second defender in time. V12's rejected first-Pylon reservation remains rejected; V16 tests the complementary combination with V15 and does not reclassify either result.

## Frozen source arms

- Control: byte-identical copy of frozen V15 candidate source, SHA-256 `0dd08d52e816e4a28fdb979b9cb35093301d54b54eacaa38279fa07e79bc5101`.
- Candidate: control plus [the V16 patch](../../../patches/kestrel-v16-first-pylon.patch), source SHA-256 `e6965f441748a3d1cd9c181e0ef9ecfa128819c774390dadeae1e66ddc2362e0`; patch SHA-256 `64a9059ad4a3445b1c301c005daf585423079e519fbcd5d688174b6633ed8f6d`.
- Candidate change: against known Zerg only, once six Probes are completed and until the first Pylon is observed current, Nexus training leaves 100 minerals available and `constructOpening()` requests the first Pylon when 100 minerals are available. `constructionPending()` remains the first construction guard. The persistent first-Pylon-current milestone makes the priority once-only. V15's first-Gateway, second-Gateway, first-Zealot, gas-delay, supply, scouting, and combat behavior is otherwise unchanged.
- Both arms retain V15's shared Pylon/Gateway/Zealot timing, local-overlap, production, economy, command, and lifecycle telemetry.

## Fixed execution and decision rule

If execution is later authorized, compile both arms natively and against official BWAPI 4.4 headers, freeze their binaries and sidecars, then run four fresh serial games against frozen ZZZK with empty learning state, LF3, the adopted engine, 120-second caps, and no retries:

1. V15 control, Benzene, engine seed `6203`.
2. V16 candidate, Benzene, engine seed `6203`.
3. V16 candidate, Heartbreak Ridge, engine seed `6204`.
4. V15 control, Heartbreak Ridge, engine seed `6204`.

Primary gate: each candidate game records at least two simultaneously completed Zealots within 12 tiles of home before the first local Zealot loss, and is no worse than its matched control. A no-loss game measures through game end.

Each candidate must also record at least four accepted Zealot trains, at least ten Probes, two Gateways current, two completed Zealots, and at least one accepted structure request after the first accepted Zealot train. Report first-Pylon accepted/current/completed frames descriptively. Integrity requires reciprocal results, clean launcher exits, no hash mismatch, all eight replay copies parsed, LF3, no wrong-race production, no missing Zealot-loss position, zero gas-worker construction attempts, zero build `Unit_Busy`, command rejection below 5%, and at least 384 durable logical frames/s in every game.

`PASS` advances the combined V16 stack to a separate held-out comparison against accepted V13. It does not adopt V15/V16 or establish strength. A missed gameplay or integrity gate is `REJECT`; invalid infrastructure is `INCONCLUSIVE`. Outcomes are descriptive.

## Resume instructions

Do not edit canonical Kestrel. Build directly from `third_party/kestrel-opening-v16-control/` and `third_party/kestrel-opening-v16-candidate/` using their copied `CMakeLists.txt`, with no more than four compile jobs. Record compiler, official-header result, source and binary hashes in sidecars before creating the four-game schedule. Review this preregistration once, then execute exactly the fixed order above only after an exclusive game window is granted.
