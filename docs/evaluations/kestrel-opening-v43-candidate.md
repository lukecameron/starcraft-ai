# Kestrel v43 candidate: second-Zealot Probe reserve

Status: built diagnostic candidate only. No match was launched, and this
candidate is not an evaluation result, ladder anchor, promotion, or Elo
evidence.

## Mechanism

V22's rejected five-game screen showed Probe train commands after the second
Gateway became current and before the second Zealot was accepted. V43 changes
one Zerg-only production gate carried from v42:

- When the second Gateway is current, reserve 100 minerals from Probe training
  while `acceptedZealotTrains_ < 2`.
- End the reserve in the same cadence pass that accepts the second Zealot train
  command.
- Keep all non-Zerg production and the earlier five-Probe Pylon policy intact.

The candidate records `second_zealot_train_frame`, reserve-active cadence
frames, and Probe reserve block frames/minerals using public self state. These
fields are telemetry only and are not read by gameplay.

## Identity and validation

Parent: `Kestrel-v42-five-probe-pylon`.

Candidate binary:

`artifacts/builds/234dcc4b0dc57ce386c19d19f249546c62986b1806396fb3d2fcb615b5f62287/kestrel-opening-v43-second-zealot-reserve/Kestrel.dylib`

- Binary SHA-256: `234dcc4b0dc57ce386c19d19f249546c62986b1806396fb3d2fcb615b5f62287`
- `Kestrel.cpp` SHA-256: `1d0783bac7b559bae28616a7d19d00dd77d70c94c43c3091a69171cf09a636cf`
- Source-combination SHA-256: `6259f12081942c6368bd9bfa33a800bd0c5e966a8c9d6922227234502ff90daa`
- Patch: `patches/kestrel-v42-to-v43-second-zealot-reserve.patch`
- Patch SHA-256: `40f36042d9f1390274b8f04afff45b59d8011f9e1f60f9e7e405c833232242ce`

Native OpenBW and official BWAPI-header builds passed with C++14, warnings as
errors, and Release configuration. Official BWAPI runtime remains unverified.
No matches were run by this candidate build.
