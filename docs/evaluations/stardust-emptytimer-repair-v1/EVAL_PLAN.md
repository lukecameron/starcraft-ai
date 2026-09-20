# Stardust empty-timer repair plan

Registered `2026-09-20T04:42:12.651398+00:00`, before compilation or launch.

When excluding zero exhausts the predicted pre-cycle timer set, the candidate restores the complete conservative nonzero domain `{1..8}`. The existing cycle then produces `{0..7}`. Nonempty paths and multiplicities remain unchanged. A defensive consumer check logs an unexpected empty derived set, marks only that forecast fully saturated, and returns from the constructor before later forecast logic runs. The change uses only the existing standard BWAPI observations and leaves the mining optimizer enabled.

Run exactly one Stardust Protoss player-1 versus ZZZKBot Zerg game on Benzene with engine seed 5202 and a 120-second cap. Do not retry or sweep seeds. Acceptance requires at least one `producer_recovered` event, no `consumer_fail_closed` event, two zero launcher return codes, verified opposing winner callbacks, no `insync_hash_mismatch`, and a complete replay containing Protoss worker, building, and combat production. This is a correctness probe, not a throughput, rating, or strength evaluation.
