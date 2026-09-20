# Kestrel v41 candidate: Zerg two-Gateway mineral bank

Status: built diagnostic candidate only. No match was launched, and this
candidate is not an evaluation result, ladder anchor, promotion, or Elo
evidence.

## Mechanism

v20 showed that the failing P2 lanes accepted the second Gateway around frame
2004, made it current around frame 2084, and completed it around frame 3055.
The first qualifying Zerg threat arrived at frames 3560 and 3551, before the
second Gateway could finish a Zealot. v41 keeps the v40 nearest eligible
Gateway-Probe policy and changes one opening resource decision:

- Once the public self-state has at least six completed Probes and the first
  Pylon is not current, a known-Zerg game uses a 250-mineral Probe reserve.
- The existing known-Zerg reserve remains 250 until the second Gateway is
  current. The reserve then returns to the existing v40 policy.
- The Nexus Probe condition is `minerals >= 50 + openingReserve`; therefore
  the higher pre-Pylon reserve defers a 50-mineral Probe that v40 could queue
  while retaining enough minerals to place the Pylon. That saved mineral then
  enters the existing v40 bank for the first and second Gateways.
- Gateway construction, Gateway training, combat, emergency defense, gas
  handling, range research, and all non-Zerg branches are unchanged.

The policy reads only public BWAPI self state and the public enemy race already
used by v40. `zerg_pre_pylon_probe_reserve_frames` records only cadence passes
where all three treatment conditions are true: known Zerg, at least six
completed Probes, and the first Pylon is not current. It is diagnostic output
and is not read by gameplay.

## Identity and validation

Parent: `Kestrel-v40-nearest-gateway-probe`.

Candidate binary:

`artifacts/builds/2e39f690e1ec598dd03d0bbfe35de75f282ab626d7b6b0c135a6fb9947ed984d/kestrel-opening-v41-zerg-two-gateway-bank/Kestrel.dylib`

- Binary SHA-256: `2e39f690e1ec598dd03d0bbfe35de75f282ab626d7b6b0c135a6fb9947ed984d`
- `Kestrel.cpp` SHA-256: `fec0f4f6c1a1a37924827be427fabe9ce695cad84ef17f5bde23e77d754218ad`
- Source-combination SHA-256: `a6d9a19debf32131aabb16b57f6726e09c9312917be83e25362e2aeafa340d3a`
- Patch: `patches/kestrel-v40-to-v41-zerg-two-gateway-bank.patch`
- Patch SHA-256: `446a560f4aab5c4bb167118ee82bd2fe7bb41702ef7b7c415a853eb25466ae07`

Native OpenBW and official BWAPI header builds passed with C++14, warnings as
errors, and Release configuration. The focused candidate lifecycle tests and
the complete Python suite passed: 97 tests. Official BWAPI runtime remains
unverified, as it does for v40.

The expected benefit is earlier first- and second-Gateway acceptance, with the
second Gateway gaining up to the time needed to accumulate the deferred Probe
cost. The exact frame shift depends on map, slot, worker travel, and resource
timing; only a fresh bounded diagnostic can measure it. The main risk is
reduced early worker count if the second Gateway does not start promptly, so
the candidate should remain experimental until the Gateway timing and
two-local-defender gates are checked.
