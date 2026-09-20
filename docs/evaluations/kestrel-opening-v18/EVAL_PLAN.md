# Kestrel v18 explicit-second-Pylon plan — NOT RUN

- Registered: `2026-09-20T08:46:56Z`, before compilation or gameplay.
- Status: source-only checkpoint. No v18 module has been compiled and no game has been launched.
- Question: does explicitly requesting a second Pylon once the first Gateway is current repair the missing supply structure in v16/v17 and create two local Zealots before the first local loss?
- Evidence: v16 and v17 candidates both built only one Pylon, accepted no structure after the first Zealot, and reached only one local completed Zealot before first loss. V18 control is the frozen v17 candidate. The candidate adds one public-state branch that requests a second Pylon before the known-Zerg second-Gateway branch when fewer than two Pylons exist and 100 minerals are available.

## Frozen source arms

- Control: byte-identical copy of the rejected v17 candidate source, SHA-256 `7d0033408a9931a98b7130fd0fde086b57a0ac3b0060ace87663a1d33af8c769`.
- Candidate: control plus [the v18 patch](../../../patches/kestrel-v18-explicit-second-pylon.patch), source SHA-256 `4c9e71f2c3a62f1e1d5fc5a6676fa445e7744e133d89cb9029c1004ed54105e3`; patch SHA-256 `b3a19b3fd9eb8bd1868a3d08ba31e2ac82f2c9926a0b771bb454b8815d85cff7`.
- Candidate change: after the first Gateway is observed current, and before the second Gateway branch, request a second Pylon whenever fewer than two Pylons are present and 100 minerals are available. V17's first-Pylon reservation, six-supply margin, first/second Gateway, gas delay, combat micro, scouting, telemetry and all non-Pylon behavior remain unchanged.

## Fixed execution and decision rule

Compile both arms natively and against official BWAPI 4.4 headers, freeze binaries and sidecars, then run four fresh serial games against frozen ZZZK with empty learning state, LF3, the adopted engine, 120-second caps and no retries:

1. v18 control, Benzene, engine seed `6207`.
2. v18 candidate, Benzene, engine seed `6207`.
3. v18 candidate, Heartbreak Ridge, engine seed `6208`.
4. v18 control, Heartbreak Ridge, engine seed `6208`.

Primary gate: each candidate game records at least two simultaneously completed Zealots within 12 tiles of home before the first local Zealot loss, and is no worse than its matched control. A no-loss game measures through game end.

Each candidate must also record at least four accepted Zealot trains, at least ten Probes, two Gateways current, two completed Zealots, at least two Pylons, and at least one accepted structure request after the first accepted Zealot train. Report Pylon and Gateway timing descriptively. Integrity requires reciprocal results, clean launcher exits, no hash mismatch, all eight replay copies parsed, LF3, no wrong-race production, no missing Zealot-loss position, zero gas-worker construction attempts, zero build `Unit_Busy`, command rejection below 5%, and at least 384 durable logical frames/s in every game.

`PASS` advances only the explicit-second-Pylon policy to a separate held-out comparison against accepted v13. A missed gameplay or integrity gate is `REJECT`; invalid infrastructure is `INCONCLUSIVE`. Outcomes are descriptive and do not establish a tournament rating.

## Resume instructions

Do not edit canonical Kestrel. Build directly from `third_party/kestrel-opening-v18-control/` and `third_party/kestrel-opening-v18-candidate/` using their copied `CMakeLists.txt`, with no more than four compile jobs. Record compiler, official-header result, source and binary hashes in sidecars before creating the four-game schedule. Execute exactly the fixed order above, preserving every outcome and replay.
