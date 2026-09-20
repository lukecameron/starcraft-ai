# Kestrel v13 local-anchor v3 result

Date: 2026-09-21  
Decision: **ADOPT for local rating evidence only**

All 16 preregistered rows completed validly with no retry, replacement, or
reseed. Kestrel v13 scored 1-7 against UAlbertaBot Terran and 0-8 against
ZZZKBot. The combined v1+v3 exact-build record is 3-25 across 28 games. Under
the unchanged Gaussian-prior Bradley-Terry model, Kestrel is **373.5
[-115.6, 862.7]** relative to the arbitrary ZZZKBot 1000 coordinate. This is
conditional Apple Silicon OpenBW calibration with wide prior-sensitive
uncertainty; it is not a BASIL, ladder, submission, or tournament rating.

The frozen plan heading remains `NOT RUN` because that file is the immutable
preregistration. Its SHA-256 is
`502c0967dd2f395db5f095e98c73e592259652d220caddae3607f51a04958bea`.
The committed source schedule SHA-256 is
`8016f315fe8f22f281b702b705d88a501c69f9a9329f7e63ebcd256b025750b8`;
the runner's canonical persisted JSON SHA-256 is
`67ba1eece29c04858b407c4c5838c8600b7e0a22361486b16e5e6865d472412d`.
The final incremental ledger SHA-256 is
`60474414641bf8f2b2930c962a2e37b87d708770f9df9dc594fc0f54a72ac540`.

## Registered decision

The cohort exceeded every fixed evidence threshold: 16 valid games versus a
minimum of 14; eight valid games per opponent versus six; eight games in each
Kestrel player slot across the cohort versus three; and all four scheduled
maps represented on both opponent edges versus three. No invalid or skipped
row entered the likelihood. The decision therefore is `ADOPT for local rating
evidence only`; it does not promote a bot or select a gameplay policy.

## Integrity review

The exact 16 rows used unique seeds 9801-9816, eight games per opponent, four
Kestrel P1 and four Kestrel P2 games per opponent, and four maps per opponent.
Candidate, opponents, launcher, engine libraries, build sidecars, provenance,
maps, three runtime MPQs, source, and reconstruction patch hashes all match
the committed schedule. The regime matches v1: LF3, 120-second game cap,
isolated empty learning state, native arm64 Darwin, and the same terminal-drain
OpenBW package. v3 ran at concurrency five while v1 was serial; the reported
combined estimate is explicitly conditional on the reviewed local regime and
does not assume broader concurrency neutrality.

Every game has reciprocal terminal results, both child return codes zero, a
verified winner, and two replay copies. Independent review verified all 32
source/archive replay hashes and sizes. All copies parse with `screp`, contain
the expected race pair, and satisfy
`replay_header_frames + 1 == owning_callback_frame`. Only the two registered
normal terminal-drain kill events appeared; there were no unrecognized kill
events or state-hash mismatches.

| Game | Run ID | Opponent | Kestrel slot | Result | Final manifest SHA-256 |
| ---: | --- | --- | ---: | --- | --- |
| 1 | `20260920T193309-63b45d5c49c0` | UAlbertaBot-Terran | P1 | Loss | `4719bb41095f592029f1f9242e74ff4779bed0030bf147018d5aa2cc6cc1aad8` |
| 2 | `20260920T193309-9be0fc272fc8` | ZZZKBot | P2 | Loss | `bba4ded2ec44e97131b8187eb3312f8bbe11dde261cbe4d5da16b945168df4ec` |
| 3 | `20260920T193309-5a21729162f4` | UAlbertaBot-Terran | P2 | Loss | `78df64dc780e82883e313bcbb816e545c36a065ebc4ed6fad99381267c827f94` |
| 4 | `20260920T193309-277c1655e5b4` | ZZZKBot | P1 | Loss | `8a74d78d0d44433ae32da1b65f505557fa9dbb7b4000c1cfb36fb3330cc2db77` |
| 5 | `20260920T193309-10ade8fd49bb` | UAlbertaBot-Terran | P1 | Loss | `d6557158d36242e5c77b556340733dc331e716617534ca121115e11892465418` |
| 6 | `20260920T193311-4bb1aab175df` | ZZZKBot | P2 | Loss | `1b6def61d54b47cea52466d2e310faa7bc5cbd2bcea81ea82fdc3c5b4f6d91c4` |
| 7 | `20260920T193311-15656dc9827e` | UAlbertaBot-Terran | P2 | Loss | `59001b1f36d376f898565520d9186d3943b9f9382a8bc9e42e574329bc64d143` |
| 8 | `20260920T193313-9194fa053231` | ZZZKBot | P1 | Loss | `c1820505e1e3e2faae819bff9a39d5c896895f3395d2b07d323d96b770a463fd` |
| 9 | `20260920T193314-36e1360c2988` | UAlbertaBot-Terran | P1 | Loss | `5f6cb802832e25cf2f048f452d57cdc9923d3435d9fc3412366a7a3e2893cb5b` |
| 10 | `20260920T193315-e27fba2acd8a` | ZZZKBot | P2 | Loss | `519ab3d8104bc016487ce0bfda155b884682f7251b764eac0c1a430f3b72f1ee` |
| 11 | `20260920T193317-cf2faf653858` | UAlbertaBot-Terran | P2 | Win | `3d0223ffa5a6dca42a4febcad7b15d2ef3a56be3a3a5c98f7b6f58dfd5447b37` |
| 12 | `20260920T193320-9cca13f84e40` | ZZZKBot | P1 | Loss | `9dd0ce1365691529f1df1006be591c9375fad68e8ea8116f1fc2ba3b1433120d` |
| 13 | `20260920T193322-e06b675801d6` | UAlbertaBot-Terran | P1 | Loss | `f2c7682bdb814779abd8911bd73960fc9f101ffe3301df3684059e5adc0ffce3` |
| 14 | `20260920T193323-57d4b513e6c4` | ZZZKBot | P2 | Loss | `463fcf6d223638196fdeefdbb4a33b11108fa691e6228e89ad442be720cc54cb` |
| 15 | `20260920T193323-eee596f37130` | UAlbertaBot-Terran | P2 | Loss | `4cb2ed31839301720ea1aeb868c513ae278eab0348e1ace4a9e9b244fc3e030d` |
| 16 | `20260920T193325-889d2802c20d` | ZZZKBot | P1 | Loss | `7c9ab8d6f1038d75f8faac48ea80165410bda27a2618ce872c1de8be36107244` |

## Rating interpretation

At the registered 400 Elo prior SD, the combined exact-build estimates are:

- ZZZKBot: 1000.0 by definition of the displayed coordinate.
- UAlbertaBot Terran: 603.7 [79.8, 1127.6].
- Kestrel v13: 373.5 [-115.6, 862.7].

Kestrel's interval width narrowed from 1048.1 Elo in v1 to 978.3 Elo after
v3. The improvement is smaller than the preregistration-time expected-value
simulation because Kestrel's 0-8 ZZZK result creates near-separation and makes
the estimate strongly prior-dependent. At prior SD 200 the displayed Kestrel
coordinate is 550.0 [261.1, 838.8]; at prior SD 800 it is 184.5 [-674.5,
1043.6]. The primary gain is 16 more clean exact-build observations and four-
map coverage, while substantial uncertainty remains.

The v2 attempts remain excluded. Hill-climb screens and experimental Kestrel
builds remain outside the rating graph. No public submission or tournament
claim follows from this result.
