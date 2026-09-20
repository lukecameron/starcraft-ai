# Kestrel v4 benchmark-opponent probe result

**Decision: infrastructure and behavior gates passed; the command gate failed in the Terran game. Keep v2 as the first verified lifecycle reference and diagnose attack-target state before any broader evaluation.**

Both fixed games completed with zero launcher exits, opposing terminal callbacks, no `insync_hash_mismatch`, two copied replays each, and successful `screp` parsing. Both exceeded the 384 frames-per-second engineering floor. Kestrel lost both games; this 0-2 descriptive result is not an Elo estimate.

| Opponent | Run | Result | Frames | Durable seconds | Frames/s | Max probes / pylons / gateways / zealots / dragoons | Commands rejected |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: |
| ZZZKBot Zerg | `20260920T061023-430740c71f57` | Loss | 6,296 | 2.4627 | 2,556.6 | 16 / 2 / 2 / 1 / 0 | 14 / 77 (18.2%) |
| UAlbertaBot Terran | `20260920T061035-54dd2cefee96` | Loss | 11,969 | 3.6412 | 3,287.1 | 28 / 4 / 4 / 5 / 6 | 621 / 876 (70.9%) |

The behavior gate passed in both games. The ZZZK replay contains 15 probe trains, three pylon and three gateway build commands, two zealot trains, scouting, and combat. The UAlbertaBot replay contains 30 probe trains, nine pylon and seven gateway build commands, eight zealot and 14 dragoon trains, scouting, and combat. Both contain only Protoss production for Kestrel.

The command gate passed against ZZZK but failed against UAlbertaBot because 70.9% exceeds v2's registered 49.7% reference. Kestrel's UAlbertaBot replay contains 135 accepted `Attack1` orders, while telemetry shows hundreds more attempted orders were rejected before entering the replay stream. Direct unit targeting therefore did not make `getOrderTarget()` a reliable deduplication state for this path, especially while choosing among a larger moving Terran army. A local record of each owned unit's last requested target and command frame is the next bounded fix; it must still permit retargeting when the target disappears or after a bounded retry.

Construction did not worsen in the longer Terran trajectory relative to v2: pylon plus gateway commands totaled 16, equal to v2, and totaled six in the shorter ZZZK game. The initial pylon still required a 240-frame retry in both games, so the actual-order extension did not eliminate that case.

Kestrel callback CPU was 0.014666 seconds with 0.0045 ms p99 and 1.95179 ms maximum against ZZZK, and 0.045184 seconds with 0.008 ms p99 and 2.31275 ms maximum against UAlbertaBot. These are trajectory descriptions, not representative late-game or tournament-host measurements.

Replay SHA-256 values are `1852ac0b1ce4e9e852bc9f3031c08a7faf2901afb52f919040566f1788eadf38` and `8ff5e3c12c5b1dd6a35c5a769e0953ca6c219d8184e31f8dfda1c2794874854` for the ZZZK game, and `2d77662e503c5aeef90ebbe4cdd14f1f8c0c3d45e8ab74c52191a0ad03374bbc` and `58535c3c4f71c5f154ffd6c609e8d74c81c8060d2c4d2d19d3581cf4b1927baf` for the UAlbertaBot game. The match manifests under the run IDs above are authoritative.
