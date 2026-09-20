# Frame-3 command divergence

The paired seed controls reproduce McRave's opening choice, but they do not make its unit traversal deterministic across different binaries. The first gameplay divergence has a direct source explanation.

In the seed-4101 baseline replay, the four initial harvest commands select drones in tag order `3593, 3594, 3595, 3596`. The candidate selects them as `3594, 3593, 3596, 3595`. The first three assigned mineral positions happen to match. The fourth baseline drone targets `(896,112)`, while the fourth candidate drone targets `(896,432)`. This occurs at replay frame 3, before the optimized late-game goal assignment is relevant.

`Workers.cpp` iterates `Units::getUnits(PlayerState::Self)` when it assigns resources. `Units.cpp` stores those units as `std::set<std::shared_ptr<UnitInfo>>` with the default comparator. That comparator provides an ownership-based strict weak order; it does not order units by StarCraft identity. A different binary layout and allocation sequence can therefore change traversal order even with identical engine and bot RNG seeds. The observed drone-tag order changes exactly as this predicts.

The same assignment walks `Resources::getMyMinerals()`, another default `std::set<std::shared_ptr<ResourceInfo>>`. Before four minutes, each candidate mineral is scored by its distance to the resource depot. Equal-distance minerals are resolved by strict `<`, so the first equal candidate in this pointer-ordered set wins. This explains why changing worker traversal and resource traversal can change the final initial mineral target. Neither set comparator uses `BWAPI::Unit::getID()`.

A minimal evaluation-only stabilization would sort snapshots at the two affected traversal sites:

1. Sort the self-worker snapshot by `unit->unit()->getID()` before `Workers::updateResource` assigns initial resources.
2. Sort the mineral snapshot by `resource->unit()->getID()` before the strict-distance selection loop.

BWAPI unit IDs are public observations already available to the bot. Sorting by them does not reveal hidden state or grant a gameplay privilege. Applying the same deterministic traversal patch to both seed-only baseline and cache candidate would preserve a controlled comparison, although it deliberately replaces upstream's unspecified pointer tie-breaking with stable ID tie-breaking.

This two-site change was tested in the follow-up `mcrave-stable-traversal-v1` evaluation and failed its same-variant repeat gate at frame 3. OpenBW BWAPI unit IDs are assigned in first-access order while iterating a pointer-hashed `Unitset`, so `getID()` is public but not stable across these processes. The proposed change therefore does not provide a deterministic comparison path. No broader stabilization was attempted.
