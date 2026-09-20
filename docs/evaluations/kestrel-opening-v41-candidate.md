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
used by v40. `zerg_two_gateway_reserve_frames` records how many cadence passes
used the new reserve; it is diagnostic output and is not read by gameplay.

## Identity and validation

Parent: `Kestrel-v40-nearest-gateway-probe`.

Candidate binary:

`artifacts/builds/d7f147ba269ac9dfd3387a003a2ade531cf11eaa2fe4770f4b2b647ca1ab3fd8/kestrel-opening-v41-zerg-two-gateway-bank/Kestrel.dylib`

- Binary SHA-256: `d7f147ba269ac9dfd3387a003a2ade531cf11eaa2fe4770f4b2b647ca1ab3fd8`
- `Kestrel.cpp` SHA-256: `570cc241c98cd6c91d20dc1f409907dcb8553dcd1716cde3b42a1501f858fc6d`
- Source-combination SHA-256: `621cba159541c6eda92fd2f24474968e32527968820a2c6527a89516a256cc4a`
- Patch: `patches/kestrel-v40-to-v41-zerg-two-gateway-bank.patch`
- Patch SHA-256: `c26739ec47881f13fec624d85046fb6c0fbb1fc18c8c9507aade94fdda2c27fa`

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
