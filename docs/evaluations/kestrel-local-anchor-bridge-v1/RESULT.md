# Kestrel v13 local-anchor bridge v1 result — ADOPT FOR LOCAL RATING EVIDENCE ONLY

The fixed eight-row cohort ran once on 21 September 2026. Seven rows were
valid. One Kestrel edge row reached the 120-second wall limit with no terminal
result or replay and remains preserved as infrastructure-invalid. It was not
retried, replaced, or included in the likelihood.

## Direct result

UAlbertaBot Protoss scored 3-0 against Kestrel v13 across Benzene,
Heartbreak Ridge, and Circuit Breaker, with valid games in both player slots.
It scored 1-3 against ZZZKBot across all four registered maps and both slots.
The cohort therefore meets the registered adoption threshold: seven valid
rows, at least three valid rows on each edge, both slots on each edge, and at
least three distinct maps on each edge.

The invalid Destination row, seed 14005, timed out after 120 seconds. Both
children exited by termination signal, no winner or terminal callback was
recorded, and no replay exists. Its logs contain repeated UAlberta BOSS
assertions. This row is excluded from rating evidence.

## Independent integrity review

All seven valid final manifests match the frozen module, configuration,
engine, launcher, game-data, map, seed, race, and slot identities. Both replay
copies from every valid game exist and match their recorded source and archive
hashes. All 14 copies parse with `screp`, report the expected races and no
command parse error, and satisfy `header frames + 1 == owning callback frame`.
Every terminal kill event is one of the two preregistered terminal-drain
events. No engine sync mismatch or unregistered kill source was found.

| Row | Opponent | UAB slot | Result | Final manifest SHA-256 |
| ---: | --- | ---: | --- | --- |
| 1 | Kestrel v13 | P1 | Win | `af0efde2c7ef0bb84741dd99e2ebb98492b0ebd0e1893f90d930b41dab0ebff7` |
| 2 | ZZZKBot | P2 | Loss | `1e4606ecdecdea7ebcb1750fd5b0940e3d8c5c17c938eac521d79466ab75ccc1` |
| 3 | Kestrel v13 | P2 | Win | `67bdbc380607bafe8c5eb6eaccf336c5fc156d5a854bfa8f0ce2ed6b6ddc6ad2` |
| 4 | ZZZKBot | P1 | Loss | `adf02525e2ca3292691c8661328e8f28aff55a02c2b45903d39337d9395ca878` |
| 5 | Kestrel v13 | P1 | Invalid timeout | `40c310c125469d4289c51ef1cf1d9ddbb0dd98aedd430dfb98a2f1600c3b5a92` |
| 6 | ZZZKBot | P2 | Win | `bf3c000984cb599f3c0ab7e4c870341ebd845a76c56f9508ce0c8cf73035b2cd` |
| 7 | Kestrel v13 | P2 | Win | `2b3d873f9986f6a3dc4ac2d568c475ad03e4d339591e7ba694d5509855f0997d` |
| 8 | ZZZKBot | P1 | Loss | `798facd61361909ef3902e626bb70f67bc119db9c5e81281108c413f74b5b85a` |

## Updated exact-build component

The unchanged Gaussian-prior Bradley-Terry model now contains 35 reviewed
games in the Kestrel component. Relative to the arbitrary ZZZKBot coordinate
of 1000, the 400-Elo-prior estimates are:

| Exact node | Record | Rating | Approximate 95% interval | Prior SD 200 / 800 |
| --- | ---: | ---: | ---: | ---: |
| ZZZKBot Zerg | 17-1 | 1000.0 | reference | 1000.0 / 1000.0 |
| UAlbertaBot Protoss | 4-3 | 817.4 | [472.2, 1162.5] | 839.9 / 810.5 |
| UAlbertaBot Terran | 11-3 | 575.3 | [95.4, 1055.2] | 752.7 / 383.1 |
| Kestrel v13 Protoss | 3-28 | 340.8 | [-101.6, 783.1] | 518.9 / 153.3 |

Kestrel's conditional interval narrowed from 978.3 to 884.7 Elo, while its
point estimate moved from 373.5 to 340.8. The result remains highly
prior-dependent. The scalar model omits map, slot, matchup, and repeated-game
dependence. These values describe this frozen Apple Silicon OpenBW regime;
they are not BASIL, ladder, Win32 tournament, or submission evidence.

## Frozen evidence

- Plan SHA-256: `bdc150f65b65b125460f133c8717d8c1b6875182fd34fa9f809b4fa35dddd2ef`
- Registered schedule SHA-256: `baf8cc1322ebb975f0c264143a53c803cdce997d1e7be5928528e8ebb535490c`
- Executed schedule SHA-256: `20b6cf4f77884b30710f03eaf2cd5f4499c60e1416f8d9821460548a724df53b`
- Batch manifest SHA-256: `231ef5c2bfc7971580f27f5d32b9f9c51e970312ba246a592b4ba921e977e8d7`

Decision: **ADOPT for local rating evidence only**. The seven valid final
manifest hashes are pinned in `config/local-ratings.json`; the invalid timeout
is preserved and excluded.
