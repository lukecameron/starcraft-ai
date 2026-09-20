# Kestrel bot

Kestrel is this project's independently written Protoss bot. It uses only the standard public BWAPI interface and makes decisions from the bot player's units, resources, explored map tiles, public starting locations, and currently visible/detected enemy units. It does not read OpenBW internals or hidden opponent state.

## Initial policy

Version 0 is a bounded two-gateway pressure policy intended to establish a complete, inspectable baseline:

- keep probe production active to 28 probes and return idle probes to mineral or gas gathering;
- build pylons before the remaining supply margin closes;
- open with two gateways, one assimilator, and a cybernetics core, then grow to four gateways;
- produce zealots before the core and dragoons afterward when resources permit;
- assign one probe to visit unexplored public start locations in stable coordinate order;
- send a four-unit army toward unexplored starts and attack visible, detected ground enemies;
- issue work only on a cadence no faster than command latency and traverse owned units by stable public unit ID.

The implementation is deliberately single-threaded and performs no terrain search, combat simulation, hidden-state inference, or learning. Its first likely weaknesses are fragile building placement, no expansion, no detector or anti-air plan, no retreat logic, and simplistic target selection. These are evidence targets rather than claims that the baseline is competitive.

## Build and identity

Build both the native OpenBW module and the official BWAPI 4.4 header compatibility object with:

```sh
scripts/build_kestrel.sh
```

The script pins the shared OpenBW BWAPI checkout at `48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2`, rejects tracked changes to it, uses `/usr/bin/clang++`, Release mode, C++14, Ninja, and at most four compile jobs. The module exports `gameInit` and `newAIModule` and writes tournament-directory telemetry to `bwapi-data/write/diagnostic.json`.

The current v5 frozen module is `artifacts/builds/eec8734a731d3184b002f069dd1356e995bc9a9422762bd5a8bd488f51655f89/kestrel-v5/Kestrel.dylib`. Its SHA-256 is `eec8734a731d3184b002f069dd1356e995bc9a9422762bd5a8bd488f51655f89`; the combined source identity recorded by its sidecar is `3e8167c8d2bbbb4c200faf923fa4205593c83eca19a0eee1a36f754e64be9272`. The frozen directory also contains the exact source, CMake file, MIT license, and provenance sidecar. V2 remains the first lifecycle-verified build; v1 and v3 were frozen but canceled before execution.

Native OpenBW and official BWAPI 4.4 headers compile successfully with Apple Clang 21.0.0. Official-game runtime behavior remains unverified until the module is built as the required Windows DLL and run under StarCraft 1.16.1/BWAPI.

### Reconstructing historical source

The current tracked source is v5. Three reverse patches reconstruct the source used by the durable historical evidence without relying on ignored build artifacts:

| Version | Apply independently to v5 | Expected combined source SHA-256 | Historical binary SHA-256 |
| --- | --- | --- | --- |
| v0 bug reproduction | `patches/kestrel-v5-to-v0.patch` | `359d466d1c62fb6373101c76bcac3139288246d06560f0d34bffc2f8d1f29cd2` | `a1cb8aa85489fdf57e046447be5af57c5132fd8d39f3b802547430b3e4d1f974` |
| v2 first lifecycle pass | `patches/kestrel-v5-to-v2.patch` | `8ad1044064ab9b8f8bf2511ed5e7f5c97bd63f8c595cfab35559c0263ac68a92` | `144d01bc11e64dfdb37113f0e8f79d397846c09373331244ca6563ca8e6d4495` |
| v4 two-opponent probe | `patches/kestrel-v5-to-v4.patch` | `482e8c3f66f2be0256fbe8cfba379475f2bc6bfa6969f27e553b37d53f9ee5d8` | `e93b84a0392d67a6fcf48f4349bc13c701ae38a68d34823a137ae9afd8ff3865` |

Apply one patch in a separate checkout at the commit containing v5, then use the normal build command:

```sh
git apply patches/kestrel-v5-to-v2.patch
scripts/build_kestrel.sh
```

Each reverse patch changes only `bots/kestrel/Kestrel.cpp`; CMake and the license are shared. Each patch was checked with `git apply --check`, then applied to a temporary v5 copy and compared byte-for-byte with the corresponding frozen source. The resulting combined source hashes matched the table. Revert or discard that separate checkout before applying a different historical patch.

## Evaluation status

The [initial native smoke](evaluations/kestrel-smoke-v0/RESULT.md) completed cleanly but failed its behavior gate: WorkerRush eliminated Kestrel before it produced a combat unit, and the replay exposed repeated pending building commands. The [v2 probe](evaluations/kestrel-build-reservation-v2/RESULT.md) completed a full economy-to-combat lifecycle and passed compatibility, but missed its strict construction-command threshold. V4's [two-opponent probe](evaluations/kestrel-benchmark-probe-v4/RESULT.md) completed plausible games against ZZZK and UAlbertaBot and met the throughput floor, but lost both and retained excessive rejected attack commands in the Terran game. V5 tracks the bot's own requested targets; its [matched-input command probe](evaluations/kestrel-command-state-v5/EVAL_PLAN.md) is registered but unrun. Kestrel remains a development candidate and must not be listed as a strength anchor.
