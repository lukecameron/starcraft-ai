# Development environment

Verified 2026-09-20 on the primary machine.

| Item | Observed |
| --- | --- |
| Host | Apple M5 Max MacBook Pro, native ARM64 |
| CPU / memory | 18 cores (6 super + 12 performance), 128 GB |
| OS | macOS 26.6.2, Darwin 25.6.0 |
| Compiler | Apple clang 21.0.0, Command Line Tools |
| Python | 3.14.7 |
| Storage | Approximately 1.6 TiB available at initialization |
| Build tools | CMake/Ninja absent from initial PATH; install project-local tools |
| Official runtime | No original-game Windows installation verified |
| Game data | No MPQs found by Spotlight or targeted Applications/Downloads/Games/Blizzard search |

`quota-axi --provider codex --json` works, but its initial fetch failed and its 97% remaining report was explicitly stale. The Codex usage tool supplied a fresh **95% remaining** weekly window, resetting **2026-09-26 10:56:45 UTC**. No reset credits consumed. Recheck after substantial work or 30–60 minutes, not every operation.

Use project-local dependencies and native compilation. Initial allowance: at most four concurrent compile jobs and two match workers until measurements justify more. Long-running processes must retain an exact session/process ID and write logs under `artifacts/`.

Full-match speed target is 384 logical frames per wall second (16 × 24). No performance claim exists until complete matches, initialization, both bots and replay persistence have been measured. Apple Silicon timings cannot establish compliance on the competition's x86 host.
