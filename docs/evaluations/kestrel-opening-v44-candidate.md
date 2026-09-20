# Kestrel v44 candidate: sixth-Probe restoration

Status: built diagnostic candidate only. No match was launched, and this
candidate is not an evaluation result, ladder anchor, promotion, or Elo
evidence.

## Mechanism

The rejected v23 screen showed that v43 fixed the second-Zealot spending
conflict but left the primary rows one opening cycle too late. V44 isolates the
top v23 shortlist item:

- Against a known Zerg, after the early first Pylon is accepted, permit exactly
  one additional Probe while fewer than six Probes exist and the second Gateway
  is not current.
- After that acceptance, retain the existing 250-mineral Probe reserve until
  the second Gateway is current, then retain v43's 100-mineral reserve until
  the second Zealot train command is accepted.
- Once the sixth Probe restoration has been accepted, block every further Probe
  command in the pre-second-Gateway window.
- Keep non-Zerg behavior unchanged.

The candidate records the sixth-Probe acceptance frame and count, restoration
active cadence frames, and the total number of accepted Probes between first
Pylon acceptance and second-Gateway current. The latter must be exactly one,
which proves no seventh pre-second-Gateway Probe command was accepted. All
retained v42/v43 telemetry remains present and scored. Each v43 reserve block
also records a pre-acceptance flag: `1` means the callback ended with the
second Zealot still pending, while `0` marks a provisional block sample from
the same callback that accepted the second Zealot. This removes dependence on
whether unit iteration reached the Nexus or Gateway first.

## Identity and validation

Parent: `Kestrel-v43-second-zealot-reserve`.

Candidate binary:

`artifacts/builds/324074602725432e2b2ac20a1d9a5e2eda124663b97c221a4c9c1897cba296c5/kestrel-opening-v44-sixth-probe-restoration/Kestrel.dylib`

- Binary SHA-256: `324074602725432e2b2ac20a1d9a5e2eda124663b97c221a4c9c1897cba296c5`
- `Kestrel.cpp` SHA-256: `ace7789619d06370ba57ac7dc88582358bc7dd3a16410a4f5bc52a06d71b43a9`
- Source-combination SHA-256: `c83ab18e3179360023ded37f5ff804e6fa72a65561f18f8865f022b8e97f8c97`
- Patch: `patches/kestrel-v43-to-v44-sixth-probe-restoration.patch`
- Patch SHA-256: `b3b88268f3c550b0e15941d0d2f47be26117f4af455f3d60aa5ad0b7edc679d4`

Native OpenBW and official BWAPI-header builds passed with C++14, warnings as
errors, and Release configuration. Official BWAPI runtime remains unverified.
No matches were run by this candidate build.
