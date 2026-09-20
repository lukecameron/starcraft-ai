# Kestrel v19 lone-Zealot hold plan — NOT RUN

- Registered: `2026-09-20T08:52:19Z`, before compilation or gameplay.
- Status: source-only checkpoint. No v19 module has been compiled and no game has been launched.
- Question: when a known Zerg opponent appears before the second defender is complete, does keeping a lone first Zealot at home until a second Zealot exists prevent the sequential local losses seen in v14–v18?
- Evidence: the v14 fight trace showed the first Zealot fighting six visible Zerglings alone and dying before the second arrived. V16–v18 repeatedly recorded one local completed Zealot before first loss despite faster Gateway/Pylon variants. V19 control is the frozen v16 candidate; the candidate changes only the pre-two-Zealot combat order.

## Frozen source arms

- Control: byte-identical copy of the rejected v16 candidate source, SHA-256 `e6965f441748a3d1cd9c181e0ef9ecfa128819c774390dadeae1e66ddc2362e0`.
- Candidate: control plus [the v19 patch](../../../patches/kestrel-v19-lone-zealot-hold.patch), source SHA-256 `8994f313e679125395c360657b41c8559659db260f47a854c0c4ac98dfb87230`; patch SHA-256 `16ecf951bbcccb41786e72ae050f5c0c011cd53242c6804c4f0b2dac8ef85b83`.
- Candidate change: against known Zerg, a completed Zealot does not issue a target attack while fewer than two completed Zealots exist; if it is more than four tiles from home it receives a home move. The existing public target selection, Gateway/Pylon priorities, gas delay, scouting and all non-Zealot behavior remain unchanged.

## Fixed execution and decision rule

Compile both arms natively and against official BWAPI 4.4 headers, freeze binaries and sidecars, then run four fresh serial games against frozen ZZZK with empty learning state, LF3, the adopted engine, 120-second caps and no retries:

1. v19 control, Benzene, engine seed `6209`.
2. v19 candidate, Benzene, engine seed `6209`.
3. v19 candidate, Heartbreak Ridge, engine seed `6210`.
4. v19 control, Heartbreak Ridge, engine seed `6210`.

Primary gate: each candidate game records at least two simultaneously completed Zealots within 12 tiles of home before the first local Zealot loss, and is no worse than its matched control. A no-loss game measures through game end.

Each candidate must also record at least four accepted Zealot trains, at least ten Probes, two Gateways current, two completed Zealots, and at least one accepted structure request after the first accepted Zealot train. Report first attack and loss timing descriptively. Integrity requires reciprocal results, clean launcher exits, no hash mismatch, all eight replay copies parsed, LF3, no wrong-race production, no missing Zealot-loss position, zero gas-worker construction attempts, zero build `Unit_Busy`, command rejection below 5%, and at least 384 durable logical frames/s in every game.

`PASS` advances only the hold policy to a separate held-out comparison against accepted v13. A missed gameplay or integrity gate is `REJECT`; invalid infrastructure is `INCONCLUSIVE`. Outcomes are descriptive and do not establish a tournament rating.

## Resume instructions

Do not edit canonical Kestrel. Build directly from `third_party/kestrel-opening-v19-control/` and `third_party/kestrel-opening-v19-candidate/` using their copied `CMakeLists.txt`, with no more than four compile jobs. Record compiler, official-header result, source and binary hashes in sidecars before creating the four-game schedule. Execute exactly the fixed order above, preserving every outcome and replay.
