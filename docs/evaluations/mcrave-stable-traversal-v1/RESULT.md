# McRave stable-traversal result

The repeatability gate failed, so no candidate game or throughput comparison was run.

Both repeats used evaluation-only baseline binary `879c0f1785bac559090a87cf77e8f2d905fc6227642b6b15154e9e131cd3078f`, engine and bot seed 4201, the same player names, and the corrected engine. Run `20260920T032943-b3600552589a` completed at frame 23,253 in 103.317 durable seconds. Run `20260920T033151-e6f376be4df7` completed at frame 19,564 in 50.565 durable seconds. Both selected `HatchPool11Hatch2HatchMuta`, exited cleanly, and produced parseable replays.

Raw commands differed at the first frame-2 `Select`: tag 3598 versus 3599. After applying the preregistered normalization, the first difference was still at frame 3, command index 7. One run targeted mineral position `(864,208)` and the other `(864,304)`. The ordered command counts through frame 1,000 were 654 and 690.

Sorting by `BWAPI::Unit::getID()` did not establish a stable order because OpenBW BWAPI assigns that ID by first access. `GameImpl::extractUnitData` iterates `aliveUnits`; `aliveUnits` is a `Unitset`, implemented as an unordered container hashed by pointer. When a unit has ID `-1`, `Server::getUnitID` appends it to `unitVector` and returns that position. Pointer-hash traversal can therefore assign different public BWAPI IDs to the same starting units in separate processes.

The evaluation stopped at the preregistered first-repeat mismatch. The isolated candidate binary `3e922a4aa2dd3a786061f43e63a5eb1612abab715c77afc5c51c44a681c11fbe` was built and preserved but never launched. Canonical source and production binaries were unchanged. There is no performance, strength, or promotion conclusion.
