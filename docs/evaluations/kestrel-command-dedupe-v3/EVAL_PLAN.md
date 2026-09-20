# Kestrel v3 command-deduplication probe plan

**Canceled before execution at `2026-09-20T06:09:24Z`.** Replay/source review identified two construction-side causes that could be corrected in the same command-priority checkpoint: a blind retry while the builder still held `PlaceBuilding`, and supply planning that ignored an incomplete pylon. V3 remains frozen and unrun; v4 incorporates those changes and retains the direct unit-target attack change.

- Registered: `2026-09-20T06:08:22Z`, before any Kestrel v3 game was launched.
- Observed problem: v2 completed its lifecycle but attempted 636 commands, of which 316 were rejected. Replay inspection showed repeated position-targeted attack orders as visible enemy workers moved.
- Change: retain the nearest-visible-enemy selection, but issue `attack(BWAPI::Unit)` and suppress it while the unit's public order target remains that enemy. Unexplored-start attack-move behavior is unchanged. Economy, build order, production, and construction reservation are unchanged.
- Candidate: frozen Kestrel v3 SHA-256 `3f08e8f06ebb7c44c07c2f82727f6238a9959fc4c4a62bbe9d4cc3400fc98a7d`; combined source identity `5b240e5a280a3ca21b0c079fc698d776bca57f7be748463a9095747bb88c3af4`.
- Scenario: exact matched repeat of v2—Kestrel Protoss player 1 versus WorkerRush Zerg player 2, Benzene, engine seed `6101`, LF3, empty learning state, 120-second wall cap.
- Execution: one attempt after an exclusive game-window grant. Preserve every result and do not retry or change the seed.
- Compatibility/lifecycle guard: both launchers exit zero, callbacks are opposing, no state-hash mismatch occurs, both replays parse, and telemetry records at least one gateway and one zealot or dragoon.
- Primary gate: rejected command count is below v2's 316 and rejected-command fraction is below v2's `316 / 636 = 49.7%`. Replay visible-enemy attack commands must decrease from v2 without removing scouting or post-production combat commands. Any increase fails the change.
- Construction guard: report pylon plus gateway build commands against v2's 16; this change is not allowed to worsen them.
- Interpretation: this matched deterministic fixture tests command behavior on one trajectory. It does not establish strength or representative performance. Report callback and whole-match measurements descriptively only.
