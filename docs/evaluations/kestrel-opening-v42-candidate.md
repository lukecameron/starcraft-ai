# Kestrel v42 candidate: five-Probe Pylon opening

Status: built diagnostic candidate only. No match was launched, and this
candidate is not an evaluation result, ladder anchor, promotion, or Elo
evidence.

## Mechanism

The v21 diagnostic showed that v41's six-Probe policy became active after the
Probe queue decisions it was intended to change. Each Zerg run had already
queued two Probes before the first Pylon, and the v41 treatment usually only
changed a later reserve value. The registered next change is therefore one
coherent five-Probe opening policy:

- Against a known Zerg, when at least five Probes are complete and the first
  Pylon is not current, use the existing 250-mineral opening reserve.
- Use the special first-Pylon construction branch at five completed Probes
  under the same public condition, so the reserve cannot wait forever for a
  sixth Probe.
- Keep v41's reserve amount, Gateway timing, builder selection, combat policy,
  and all non-Zerg behavior unchanged.

The existing v41 telemetry remains present. The new
`zerg_five_probe_policy_active_frames` counter counts only cadence passes where
all three treatment conditions hold. `zerg_five_probe_pylon_accepted_frame`
records the accepted first Pylon when that condition held, and
`zerg_five_probe_pylon_accepted` is its bounded boolean summary. These fields
use public self-state and are never read by gameplay.

## Identity and validation

Parent: `Kestrel-v41-zerg-two-gateway-bank`.

Candidate binary:

`artifacts/builds/a212db989667f9abc5ed88c82ea474af03a9a0e353924422e131feacaec139f7/kestrel-opening-v42-five-probe-pylon/Kestrel.dylib`

- Binary SHA-256: `a212db989667f9abc5ed88c82ea474af03a9a0e353924422e131feacaec139f7`
- `Kestrel.cpp` SHA-256: `33bfc50879539f84ed886ed3430f813ad0fbc7d9ad7c12b380ed308ffea8a950`
- Source-combination SHA-256: `114de3d7522e9936fa30f918f1ba368dcd4e4799f958c4bd66bfc1ac0560356a`
- Patch: `patches/kestrel-v41-to-v42-five-probe-pylon.patch`
- Patch SHA-256: `0f50c3c1106a00ed5cf9852ac34e227ff15d4e4ac7925db072442710c4df11ec`

Native OpenBW and official BWAPI header builds passed with C++14, warnings as
errors, and Release configuration. Focused candidate and scorer tests passed,
and the complete Python suite passed: 109 tests. Official BWAPI runtime remains
unverified.

The main risk is that five workers may delay mineral income if Pylon placement
or the second Gateway cannot start promptly. The new acceptance frame makes
that outcome measurable without relying on privileged evaluator state.
