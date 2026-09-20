# Kestrel v13 local-anchor plan — NOT RUN

- Registered: `2026-09-20T09:07:00Z`, before any match launch.
- Status: schedule-only checkpoint. No game has been launched.
- Question: where does the accepted Kestrel v13 development baseline sit in the existing current-engine local rating graph relative to the frozen UAlbertaBot Terran and ZZZKBot nodes?
- Purpose: add exact-build, current-engine local Elo evidence for Kestrel with uncertainty. This is a descriptive calibration cohort, not a promotion or tournament claim.

## Frozen regime and identities

- Engine: adopted terminal-drain package `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`, LF3, current game-data runtime, empty isolated learning state, 120-second cap.
- Candidate: accepted Kestrel v13, module SHA-256 `622bca47b47f78f3e9d1971d1e340f991b54ced7f3bfdfd932d3062e125cbd98`, Protoss, Ours / Original.
- UAlbertaBot Terran: module SHA-256 `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`, project Port, David Churchill attribution retained.
- ZZZKBot: module SHA-256 `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`, project Port, Chris Coxe attribution retained.

## Fixed schedule

Run exactly once, serially, with no retries, replacements or outcome-adaptive seeds. Each edge uses three maps and both player slots: UAlberta Terran on Benzene, Heartbreak Ridge and Destination with seeds `9701`–`9703`; ZZZKBot on the same maps with seeds `9704`–`9706`. The exact schedule is frozen in `schedule.json`.

All 12 attempts must have reciprocal terminal callbacks, zero launcher exits, no state-hash mismatch, two archived replay copies with matching hashes, full `screp` parsing, expected races, owner-frame matches, LF3 and exact engine/build identities. Any invalid attempt makes the cohort INCONCLUSIVE; preserve every outcome and do not replace it.

## Rating rule

If all 12 attempts validate, add this experiment as a current-engine cohort to `config/local-ratings.json` and include all reviewed final manifest hashes. Recompute the unchanged Gaussian-prior Bradley–Terry MAP with 400 Elo prior SD, approximate 95% Laplace contrast intervals and 200/800 sensitivity. Report Kestrel's conditional estimate relative to the arbitrary ZZZK 1000 coordinate and direct win records against each opponent. The result remains conditional on this small map/slot sample and does not transfer to BASIL or tournament play.
