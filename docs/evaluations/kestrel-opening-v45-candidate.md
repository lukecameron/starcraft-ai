# Kestrel v45 candidate: four-Probe Pylon opening

Status: built diagnostic candidate only. No match was launched, and this
candidate is not an evaluation result, ladder anchor, promotion, or Elo
evidence.

## Mechanism

V44 was rejected because restoring a sixth Probe delayed the first Gateway on
all four Zerg rows and still left the primary rows with one defender. V45
returns to the rejected v43 parent and changes one opening variable:

- Against a known Zerg, do not accept any Probe train before the first Pylon
  request is accepted.
- Request the first Pylon as soon as four completed starting Probes and 100
  spendable minerals are publicly available.
- After the first Pylon is accepted, retain v43's 250-mineral Probe reserve
  until the second Gateway is current, then retain its 100-mineral reserve
  until the second Zealot train command is accepted.
- Keep non-Zerg production and construction behavior outside this treatment.

The candidate records the four-Probe policy's active cadence frames, its exact
accepted first-Pylon frame and boolean acceptance, the completed-Probe count
at that acceptance, and the second Zealot's direct public completion frame.
It also carries v44's measurement-only reserve pre-acceptance flags, so a
same-callback reserve sample is distinguished from a block observed after the
second Zealot was accepted. Probe acceptance remains recorded as an ordered
public self-state trace; no evaluator or replay state enters the policy.

## Identity and validation

Parent: `Kestrel-v43-second-zealot-reserve`.

Candidate source:

`third_party/kestrel-opening-v45-candidate/Kestrel.cpp`

Candidate binary:

`artifacts/builds/0c4ab506d192f1ea5902ab0a91bab2fb64ccceb04bd359eea46c250a829b2a72/kestrel-opening-v45-four-probe-pylon/Kestrel.dylib`

- Binary SHA-256: `0c4ab506d192f1ea5902ab0a91bab2fb64ccceb04bd359eea46c250a829b2a72`
- `Kestrel.cpp` SHA-256: `2f21540b80ae36c9c852382e5d4d99aebfdf3e0918390702f56aeb33cdd12f3d`
- Source-combination SHA-256: `9999b3271a37f95e73d7afbc3c25d9ca9b9531f933fe1a20e05cf734e55fbc4f`
- Patch: `patches/kestrel-v43-to-v45-four-probe-pylon.patch`
- Patch SHA-256: `842d6d5e1bb4942267fa1d6349e1b2485956f7e58ed88d995cd66aa77754b0d1`

The native OpenBW BWAPI lane and the official BWAPI 4.4.0 header lane were
both compiled with C++14, warnings as errors, and Release configuration.
Official BWAPI runtime execution remains unverified. No matches were run by
this candidate build. The scorer recognizes `Kestrel-v45-four-probe-pylon`
and checks zero pre-Pylon accepted Probes, exact four-Probe Pylon acceptance,
the retained v43 reserve ordering, no strict second-Gateway-to-second-Zealot
Probe acceptance, and direct second-Zealot completion ordering.

## Scope and limitations

The four-Probe opening is a Zerg-only treatment selected from the public enemy
race reported at `onStart`. The acceptance and completion fields are public
self state and are telemetry only. The candidate does not prove that the
Pylon request is accepted in every map/layout or that four Probes dominate
the rejected five-Probe policy; both require a separately registered match
screen. The binary is an isolated candidate and does not alter the protected
experiment registry, dashboard snapshot, resume checkpoint, or v24 evidence.
