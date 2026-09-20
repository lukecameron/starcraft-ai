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

The tracked source and `scripts/build_kestrel.sh` build the accepted v7 development baseline. Its frozen module is `artifacts/builds/2facbf970d4a4fd131564d3d02cd3966bcadc50e13e08256a1a92d3886013d3e/kestrel-v7/Kestrel.dylib`; its binary SHA-256 is `2facbf970d4a4fd131564d3d02cd3966bcadc50e13e08256a1a92d3886013d3e` and its combined source identity is `34f43843f762ed32c7052eda64e324db8fe6b4204dd48f94692d84df5d2b18f1`. `config/kestrel-baseline.json` records the same immutable reference.

Rejected v8, v9, v10 and v11 remain frozen under their binary hashes. The default source stays on v7; none of these failed experiments replaces it.

Native OpenBW and official BWAPI 4.4 headers compile successfully with Apple Clang 21.0.0. Official-game runtime behavior remains unverified until the module is built as the required Windows DLL and run under StarCraft 1.16.1/BWAPI.

### Reconstructing historical source

The current tracked source is v7. Apply `patches/kestrel-v7-to-v6b.patch`, then `patches/kestrel-v6-to-v5.patch` to recover v5 (expected combined source SHA-256 `3e8167c8d2bbbb4c200faf923fa4205593c83eca19a0eee1a36f754e64be9272`). The forward patch `patches/kestrel-v7-to-v8.patch` reconstructs rejected v8, while `patches/kestrel-v7-to-v9.patch` reconstructs the isolated worker-defense candidate. Three further reverse patches reconstruct the source used by earlier durable evidence without relying on ignored build artifacts:

| Version | Apply independently to v5 | Expected combined source SHA-256 | Historical binary SHA-256 |
| --- | --- | --- | --- |
| v0 bug reproduction | `patches/kestrel-v5-to-v0.patch` | `359d466d1c62fb6373101c76bcac3139288246d06560f0d34bffc2f8d1f29cd2` | `a1cb8aa85489fdf57e046447be5af57c5132fd8d39f3b802547430b3e4d1f974` |
| v2 first lifecycle pass | `patches/kestrel-v5-to-v2.patch` | `8ad1044064ab9b8f8bf2511ed5e7f5c97bd63f8c595cfab35559c0263ac68a92` | `144d01bc11e64dfdb37113f0e8f79d397846c09373331244ca6563ca8e6d4495` |
| v4 two-opponent probe | `patches/kestrel-v5-to-v4.patch` | `482e8c3f66f2be0256fbe8cfba379475f2bc6bfa6969f27e553b37d53f9ee5d8` | `e93b84a0392d67a6fcf48f4349bc13c701ae38a68d34823a137ae9afd8ff3865` |

Apply the v7-to-v6b and v6-to-v5 patches, then one historical patch in a separate checkout and use the normal build command:

```sh
git apply patches/kestrel-v7-to-v6b.patch
git apply patches/kestrel-v6-to-v5.patch
git apply patches/kestrel-v5-to-v2.patch
scripts/build_kestrel.sh
```

Each reverse patch changes only `bots/kestrel/Kestrel.cpp`; CMake and the license are shared. The historical patches were checked and applied to a temporary v5 copy, then compared byte-for-byte with the corresponding frozen source. The resulting combined source hashes matched the table. Revert or discard that separate checkout before applying a different historical patch.

## Evaluation status

The [initial native smoke](evaluations/kestrel-smoke-v0/RESULT.md) completed cleanly but failed its behavior gate. V4 and V5 exposed excessive command rejection. Telemetry-complete v6b reduced attack-request rejection but found busy and supply-invalid training attempts. V7's [fixed probe](evaluations/kestrel-train-legality-v7/RESULT.md) passed: all train and attack requests were accepted, both full opponent games retained production and combat, and total rejection remained below 5%. V8's [first-zealot experiment](evaluations/kestrel-first-zealot-v8/RESULT.md) advanced the first train by 396 frames but failed lifecycle and survival gates. V9's [worker-defense experiment](evaluations/kestrel-worker-defense-v9/RESULT.md) executed a legal six-probe response but ended earlier than the matched v7 row and reduced combat production. V10's [Zerg-defense production experiment](evaluations/kestrel-zerg-zealot-v10/RESULT.md) advanced three Zealot trains without gas spending, but failed its third-train threshold and never queued a fourth unit. V7 remains the command-clean baseline and is not a strength anchor.

The [first-home-fight diagnostic](evaluations/kestrel-fight-diagnostic-v1/RESULT.md) observed v7’s first two Zealots engaging locally but separately against larger Zergling groups. The second Gateway started too late to support the first fight despite banked minerals. This supports testing earlier production capacity; one instrumented loss does not prove a general cause. Apply `patches/kestrel-v7-fight-diagnostic.patch` to reconstruct the diagnostic source.

The [earlier-second-Gateway screen](evaluations/kestrel-early-second-gateway-v11/RESULT.md) also failed. Both second Gateways completed after home pressure arrived, and both games had at most one completed Zealot in the home-fight window. V11 remains isolated and reconstructible through `patches/kestrel-v7-to-v11.patch`; canonical v7 is unchanged.
