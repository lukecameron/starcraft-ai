# McRave station-coordinate diagnostic plan

Registered at 2026-09-20T03:37:43Z, before either diagnostic module was built or launched.

## Question

Does the frozen seeded McRave baseline expose a relative `BWEB::Station::defenses` entry on the actual Destination game path, and does changing only that insertion to an absolute base-relative map tile restore the collection invariant and affect the first Creep Colony placement decision?

## Fixed controls

- Destination, McRave Zerg as launcher player 1 versus ZZZKBot Zerg as player 2.
- OpenBW scenario seed 1002, player IDs 1 and 2, and McRave `MATCH_BOT_SEED=1002`.
- Corrected frozen engine package with `libOpenBWData.dylib` SHA-256 `f1a32e5a3dc64b8c62a17788488d36594dd95b13ef124637795b5aca4c846c42`.
- Frozen seeded McRave baseline source patch `patches/mcrave-seeded-baseline.patch`, whose existing module SHA-256 is `7b089ca77fa9b2a057320b88d8fd4cf3d6b984bca0715e2fe3aca517b7a1f998`.
- Frozen ZZZKBot module SHA-256 `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`.
- LF3 and a 120-second wall timeout.

ZZZKBot has no declared bot RNG control, so the pair is not claimed to be fully deterministic. Both runs and every emitted replay remain evidence regardless of outcome.

## Variants and measurements

Build two modules in isolated source directories. Both add the same observation-only diagnostic at the first Creep Colony request. It records each owned station's base and pocket tile, every station-defense tile in iteration order, map bounds, displacement from the base, and the placement predicates: validity, larva/egg overlap, pathability, existing plan, used or unbuildable footprint, nearby blocking enemy identity and distance, builder availability, and creep readiness.

The baseline retains the upstream `defenses.insert(defense)`. The candidate changes only that policy line to `defenses.insert(base->Location() + defense)`. Instrumentation, compiler, and build flags are otherwise identical.

## Interpretation fixed in advance

The baseline reproduces the coordinate defect if the actual first-colony path contains a defense entry equal to a small relative offset and far from its owning base, including an out-of-map negative entry. The candidate repairs the invariant if every emitted station defense is in map bounds and near its owning base and the intended absolute defense replaces the relative entry.

An accepted Creep Colony build command, if exercised, must be confirmed from the replay rather than inferred from McRave logs. A changed result or win is not strength evidence and is not required to establish the coordinate contract. If the run never requests a colony, the initialization evidence may establish the collection defect but placement behavior remains unexercised. No canonical source or baseline changes follow automatically from this diagnostic.
