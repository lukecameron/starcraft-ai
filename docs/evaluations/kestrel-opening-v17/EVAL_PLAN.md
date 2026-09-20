# Kestrel v17 supply-buffer plan — NOT RUN

- Registered: `2026-09-20T08:40:09Z`, before compilation or gameplay.
- Status: source-only checkpoint. No v17 module has been compiled and no game has been launched.
- Question: after v16 moved the first Pylon earlier but never requested a second supply Pylon before pressure, does asking for the next supply Pylon at a six-supply margin preserve the faster opening while allowing two local Zealots to overlap?
- Evidence: v16 candidate had one Pylon in both games, no accepted structure after its first Zealot, and only one local completed Zealot before first loss on both maps. Its matched controls reached two local defenders. The v17 control is the frozen v16 candidate; the candidate changes only the ordinary supply-Pylon trigger from a four-supply margin to six.

## Frozen source arms

- Control: byte-identical copy of the rejected v16 candidate source, SHA-256 `e6965f441748a3d1cd9c181e0ef9ecfa128819c774390dadeae1e66ddc2362e0`.
- Candidate: control plus [the v17 patch](../../../patches/kestrel-v17-supply-buffer.patch), source SHA-256 `7d0033408a9931a98b7130fd0fde086b57a0ac3b0060ace87663a1d33af8c769`; patch SHA-256 `03510ab3c5525b1e37bedc4fe764ebf237089af69717a73ac7ce6caabd43a091`.
- Candidate change: `constructOpening()` requests an ordinary supply Pylon when the remaining margin is at most six supply instead of at most four. First-Pylon reservation, Gateway priorities, gas delay, combat micro, scouting, telemetry and all non-supply behavior remain unchanged.

## Fixed execution and decision rule

If execution is authorized by this project scope, compile both arms natively and against official BWAPI 4.4 headers, freeze binaries and sidecars, then run four fresh serial games against frozen ZZZK with empty learning state, LF3, the adopted engine, 120-second caps and no retries:

1. v17 control, Benzene, engine seed `6205`.
2. v17 candidate, Benzene, engine seed `6205`.
3. v17 candidate, Heartbreak Ridge, engine seed `6206`.
4. v17 control, Heartbreak Ridge, engine seed `6206`.

Primary gate: each candidate game records at least two simultaneously completed Zealots within 12 tiles of home before the first local Zealot loss, and is no worse than its matched control. A no-loss game measures through game end.

Each candidate must also record at least four accepted Zealot trains, at least ten Probes, two Gateways current, two completed Zealots, and at least one accepted structure request after the first accepted Zealot train. Report first and subsequent Pylon timing descriptively. Integrity requires reciprocal results, clean launcher exits, no hash mismatch, all eight replay copies parsed, LF3, no wrong-race production, no missing Zealot-loss position, zero gas-worker construction attempts, zero build `Unit_Busy`, command rejection below 5%, and at least 384 durable logical frames/s in every game.

`PASS` advances only the supply-buffer policy to a separate held-out comparison against accepted v13. A missed gameplay or integrity gate is `REJECT`; invalid infrastructure is `INCONCLUSIVE`. Outcomes are descriptive and do not establish a tournament rating.

## Resume instructions

Do not edit canonical Kestrel. Build directly from `third_party/kestrel-opening-v17-control/` and `third_party/kestrel-opening-v17-candidate/` using their copied `CMakeLists.txt`, with no more than four compile jobs. Record compiler, official-header result, source and binary hashes in sidecars before creating the four-game schedule. Execute exactly the fixed order above, preserving every outcome and replay.
