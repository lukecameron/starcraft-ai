# McRave native OpenBW port

McRave is vendored at upstream commit `7d1719a22d8b896f957abae50e2ea5efff974fe2` under its MIT license. `scripts/build_mcrave.sh` builds the full upstream gameplay source as an ARM64 native `build/mcrave/McRave.dylib` linked to this repository's OpenBW BWAPI 4.2 library. It does not disable gameplay subsystems.

The port makes the Windows DLL entry point conditional while exporting the same `gameInit` and `newAIModule` ABI on macOS. It disables only BWEM's Windows performance-counter helper, makes the visual focus check portable, fixes two Windows path separators, and makes MSVC-accepted C++ constructs conforming without changing their intended values. The CMake port uses Clang's delayed template parsing because upstream relies on MSVC template lookup behavior. Windows code remains under `_WIN32`, so the original Visual Studio source path is retained.

Build with:

```sh
scripts/build_mcrave.sh
```

The command uses the repository-local CMake and Ninja, limits compilation to four jobs, and writes `build/mcrave/McRave.dylib.build.json`. It applies `patches/mcrave.patch` when the checkout is clean and accepts an exact already-applied patch, so repeated builds are idempotent. The sidecar records the source and BWAPI revisions, SHA-256 of the source patch and dylib, compiler, language mode, and port flags. A successful local build exports both required module symbols.

The port also repairs compiler-observed undefined behavior: missing count returns, a self-referential static initializer, a reference to a temporary empty set, and a shadowed text-color value. Remaining warnings are the upstream `M_PI` redefinition and BWAPI template-definition diagnostics; there are no remaining missing-return or dangling-reference diagnostics. The complete source compiles against the OpenBW fork's BWAPI 4.2 headers. The `McRaveOfficialHeaders` object target also compiles all 114 translation units as native ARM64 objects against official BWAPI 4.4.0 headers at revision `7687da8abc4726f8366401f11ab648d421385793`. This checks public source compatibility without linking the official core into the OpenBW runtime module. Windows x86 compilation, linking, and original-game execution remain unverified.

The native end-to-end run `20260920T020358-c05c1bb639cc` completed on Benzene against the WorkerRush diagnostic module in 12.089 seconds of measured wall time. McRave won at frame 8,900 with runtime latency 3, nine drones, three hatchery-tier buildings, one spawning pool, and 18 zerglings. Both launchers exited zero, both result records reported `ended: true` with opposing winners, and both players produced nonempty native replays. The durable evidence is in `artifacts/runs/20260920T020358-c05c1bb639cc/game-0001/manifest.json`; this is a gameplay smoke test, not evidence of strength equivalence to the historical upstream or BASIL bot.

The upstream MIT license is preserved verbatim at `ports/mcrave/LICENSE` for redistribution of the patch and port build files.

## Destination crash repair

The original frozen build later completed `onEnd` on Destination but exited with `SIGSEGV` while BWAPI unloaded the module (`20260920T021708-85baf6eb5040`). AddressSanitizer separately found a concrete lifetime error in combat clustering: the code retained a reference to `queue.front()`, popped that element, and then dereferenced the invalid reference. The port now copies the queued pointer before `pop()`.

Optimized LLDB runs also showed BWEB map roots containing coordinate-like values during initialization. The attempted hardware watchpoint did not resolve the anonymous static variable, so this was stack and state evidence rather than direct proof of the writing instruction. Inspection found that `BWEB::Blocks::addToBlockGrid` wrote station-derived coordinates into a fixed `256 x 256` array without checking the current map bounds. The port now skips coordinates outside the active map. Temporary cache-lifetime and compiler global-merging experiments did not fix the release failure and are not part of the final patch.

The final frozen module is `artifacts/builds/c49ee3c4b20a2772f1bfca03249c182d32a7238f9453a7a568990a188a1c4c65/McRave.dylib`. The AddressSanitizer verification `20260920T023651-fb11b5825657` completed with both processes exiting zero and no sanitizer output; its result metadata was inconsistent, so it is not scored. The release verification `20260920T023737-795afabea26a` completed on Destination in 12.551 seconds with both processes exiting zero, opposing verified results, LF3, empty stderr, and two nonempty hashed replays. These repairs address memory safety and lifecycle reliability; they are not a strategic gameplay change.

## Station defense coordinates

`BWEB::Station::defenses` contains absolute map-tile positions. Its other producers add the station base location, while Planning, Buildings, Wall, and Block consume each entry directly as a map tile. The upstream Zerg secondary-location path validated `base->Location() + defense` but inserted the raw relative offset. The native port now inserts the validated absolute tile.

The registered diagnostic in `docs/evaluations/mcrave-station-coordinates-v1` exercised this code on Destination. At the first Creep Colony request, the unchanged path exposed `(0,-3)` in the defense set for base `(64,118)`. The one-line candidate exposed `(64,115)` instead; all station defense entries were in bounds and near the base, and the replay recorded an accepted Creep Colony build at the corrected tile on frame 3,542. The unchanged run also found other legal positions and issued a colony command. The differing game outcomes therefore do not show a strength improvement or prove that this defect caused the earlier loss. The evidence establishes the coordinate contract and an actual game-path correction.
