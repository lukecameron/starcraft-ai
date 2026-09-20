# Decisions

## 2026-09-20: start with a native headless OpenBW spike

The repository initially contained only the assignment. The actual machine supports the brief's native ARM64 path. Start with upstream OpenBW and its BWAPI fork, UI disabled, before introducing WASM, ML, distributed scheduling, or terrain libraries. First acceptance: two bot modules finish a game unattended and produce a parsable replay with durable provenance.

OpenBW's BWAPI fork identifies itself as 4.2.0 and does not run on the original game. The official lane therefore needs a separate build using official BWAPI; shared gameplay code must stay on the common public API surface. Do not claim binary compatibility.

The engine spike and initial source discovery run in parallel: Sol owns the engine build; Luna owns bounded technique and opponent research. Lead handles rules, environment, integration and source backup. An initial researcher was interrupted before work because the model had been inherited instead of explicitly selected; the replacement crawl used the requested Luna model.

## Initial experiment: establish the runtime, not playing strength

- Problem: no engine, policy, match command or measured baseline exists.
- Proposed change: pinned native engine, minimal bot modules and replay capture.
- Expected effect: a reproducible complete match, or a concrete dependency blocker.
- Test: compile Release without UI; launch a bounded headless match after required assets exist; parse its replay.
- Stop: checkpoint after 15 minutes of build work; do not launch matches repeatedly if essential game data is absent.
- Status: in progress. No best validated bot, local rating, strength gain or throughput result yet.
