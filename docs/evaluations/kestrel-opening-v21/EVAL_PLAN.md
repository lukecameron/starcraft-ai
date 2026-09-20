# Kestrel v21 two-train reserve plan

Registered as a source-only preregistration after v20 review. No v21 source has been compiled and no v21 game has been launched.

## Hypothesis

V19's lone-Zealot hold produced two local defenders before first loss on both maps, but its Heartbreak arm accepted only three Zealot trains and no post-first-train structure. V20 kept the reserve until four accepted trains and did not repair that miss. The narrower policy tested here keeps the mineral reserve only until the second Zealot train is accepted, then releases it early enough for ordinary construction and later production.

## Frozen arms and exact change

- Control: byte-identical v19 candidate source SHA-256 `8994f313e679125395c360657b41c8559659db260f47a854c0c4ac98dfb87230`; frozen binary SHA-256 `f02db8b97e01482f897a0f481c11a92f0cd5bc21f4629abea1f5a6d113b44b9a`.
- Candidate: v19 control plus `patches/kestrel-v21-two-train-reserve.patch`; candidate source and binary SHA-256 are recorded in build sidecars before the schedule is created. The preregistered patch SHA-256 is `d10162173e7868b062eee73e259ecfd0d9b384611c018d08e75dfa7bcc4b2470`.
- Candidate behavior: in `trainUnits()`, after the existing v19 first-Pylon, Gateway and first-Zealot reserve branches, reserve 100 minerals while `acceptedZealotTrains_ < 2` and `probes >= 10`. This is the only candidate change. The v19 home hold, construction, combat targeting, scouting, gas-worker guard, telemetry and all non-Zerg behavior remain unchanged.
- Build convention: copy the frozen v19 control and candidate source trees, apply only this patch to the candidate, build each with its copied `CMakeLists.txt` using at most four jobs, compile native and all official BWAPI 4.4 translation units, and freeze hashes and sidecars before launch. Do not edit canonical Kestrel.

## Fixed schedule

Run exactly four serial games against frozen ZZZKBot `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`, with adopted engine `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`, empty learning state, LF3, 120-second per-game caps, and no retries or replacements:

| Attempt | Arm | Map | Engine/McRave seed | Kestrel slot |
|---:|---|---|---:|---:|
| 1 | v19 control | `sscai/(2)Benzene.scx` | 6213 | P1 |
| 2 | v21 candidate | `sscai/(2)Benzene.scx` | 6213 | P1 |
| 3 | v21 candidate | `sscai/(2)Heartbreak Ridge.scx` | 6214 | P2 |
| 4 | v19 control | `sscai/(2)Heartbreak Ridge.scx` | 6214 | P2 |

The opponent occupies the other slot in every game. Persist and hash this schedule before the first launch.

## Integrity, performance and gameplay gates

Every game must have zero launcher exits, opposing Boolean terminal callbacks, no timeout, crash, state-hash mismatch, unexpected kill path, missing telemetry position, gas-worker build attempt, build `Unit_Busy`, or wrong-race production. Both replay copies must match manifest hashes and parse fully with `.tools/screp/screp`, including owner frame and race checks. Every game must reach at least 384 durable logical frames per wall second; command rejection must remain below 5%.

Each candidate game must record at least two simultaneously completed local Zealots within 12 tiles of home before the first local Zealot loss, at least four accepted Zealot trains, at least ten Probes, two Gateways current, two completed Zealots, and at least one accepted structure request after the first accepted Zealot train. The candidate must be no worse than its matched control on the local-overlap metric and must satisfy all production gates on both maps.

`PASS` advances only this v21 policy to a separately registered held-out comparison against accepted canonical v13. It does not adopt v21, update the canonical bot, or establish tournament strength. A complete valid cohort missing any gameplay, production, integrity or throughput gate is `REJECT`; any infrastructure-invalid attempt is `INCONCLUSIVE` and is preserved without retry.

## Scope and uncertainty

This is a two-map, two-seed mechanism screen against one frozen ZZZKBot build. Outcomes and terminal frames are descriptive. It cannot establish Elo, BASIL transfer, or a universal opening policy. The v19 overlap signal and v20 production failure remain part of the rationale and are not pooled as independent strength evidence.
