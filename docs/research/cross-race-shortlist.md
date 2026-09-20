# Cross-race native opponent shortlist

Research date: 2026-09-20. The recommendation is **Stardust** at commit `22d93d7a55d0a0494384474a456fd7ee26baee97` as the first cross-race native build spike. The archived BASIL snapshot records Stardust as enabled, `PROTOSS`, rating 3459, rank S, 49,456 games, 220 cumulative crashes, map pool `SSCAIT`, and `lastUpdated` 2026-08-22. It is strategically distinct from the McRave, ZZZKBot and UAlbertaBot leads: the repository describes a tournament-optimized Protoss bot using BWEM terrain analysis and modified FAP combat simulation.

Stardust is unusually suitable for the current ARM64/OpenBW lane because its primary `CMakeLists.txt` has an explicit non-MSVC path: C++20, macOS deployment target 13.0, `OPENBW_DIR=3rdparty/openbw/openbw`, and `add_subdirectory(3rdparty/openbw/bwapi)`. It then builds vendored `BWEM`, `FAP`, `nlohmann`, `bitsery`, `cppcrc`, `zstd`, and `zstdstream` before `src`. The repository also has a native `test` target that links Stardust and several opponent libraries. This is a concrete native CMake route, not an inference from the bot’s language.

The immediate blockers are dependency completeness and API alignment: the pinned checkout must contain or fetch the expected `3rdparty` trees, and its bundled OpenBW/BWAPI fork may differ from this project’s pinned engine. The CMake file’s non-MSVC branch also builds its own OpenBW/BWAPI rather than consuming `third_party/bwapi` automatically. First test should therefore be a clean configure/build of Stardust’s own target on the Mac, followed by an adapter smoke match against the existing WorkerRush fixture on Benzene. Capture compiler, CMake, dependency and engine hashes before treating a successful build as an opponent result. Do not run the broad opponent test suite until the smallest target and one complete native match work.

The license is MIT with an additional condition: forks may not be submitted to StarCraft AI competitions without written author consent. The author says Protoss forks receive stricter review. Benchmarking the unmodified pinned bot is a separate question from submitting a derivative; no permission is needed for this local diagnostic use, but any future derivative submission remains blocked pending consent and current SSCAIT’s recent-copy author-contact rule.

Ecgberht is a useful lower-rated Terran research lead but a worse first native candidate. Its current head is `4e6f84469f8f83333ae68a868b8f6be167632e46`, BASIL snapshot rating 2514, race TERRAN, rank E, 1,101 games, and last update 2020-01-25. The primary README requires a 32-bit JDK8, Gradle `fatjar`, Java BWAPI4J, and 32-bit `java.exe`; the repository is GPL-3.0. That route is oriented toward the official Windows/JAR environment, while native OpenBW on this Mac would add JVM and BWAPI4J bridge uncertainty. Keep Ecgberht as a later Terran diversity probe if Stardust’s CMake dependencies fail.

## Sources

- [Stardust README](https://github.com/bmnielsen/Stardust/blob/main/README.md)
- [Stardust CMakeLists.txt](https://github.com/bmnielsen/Stardust/blob/main/CMakeLists.txt)
- [Stardust LICENSE](https://github.com/bmnielsen/Stardust/blob/main/LICENSE)
- [Ecgberht README](https://github.com/Jabbo16/Ecgberht/blob/master/README.md)
- [Ecgberht LICENSE](https://github.com/Jabbo16/Ecgberht/blob/master/LICENSE)
- `artifacts/sources/basil-ranking-2026-09-20.json` (SHA-256 `56d749eac93df8aba889d09f5abed9f271b62a2dc02976525c8130f441c6e802`)
