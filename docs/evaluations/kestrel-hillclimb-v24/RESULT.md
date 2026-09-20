# Kestrel hill-climb v24 result

Date: 2026-09-21
Decision: **REJECT**

The fixed five-game `Kestrel-v44-sixth-probe-restoration` screen ran once
with five concurrent launchers and no retry, reseed, replacement, or rerun.
Kestrel won the Benzene ZZZK row and lost the two primary P2 ZZZK rows, the
McRave row, and the Stardust sentinel. All five rows are clean terminal games
with ten independently verified replay copies.

V44 restored exactly one sixth Probe on every Zerg row and blocked a seventh
before the second Gateway, but it delayed the first Gateway on all four
same-map/slot comparisons with v23. Both primary rows still had one completed
local defender at pressure, so the registered primary metric is
`M = min(1, 1) = 1`, below the required `M >= 2`. Every Zerg row also
accepted at least one Probe strictly between second-Gateway current and second-Zealot
acceptance, failing the registered retained-policy gate. V44 is `REJECT`;
canonical Kestrel v13 and local Elo remain unchanged.

## Frozen identity and evidence

The registered plan SHA-256 is
`9b1fa692795501b069ff790eacf2b0b008a4b7b01c1ae69b09a2a2ec236d1b7e`.
The committed source schedule SHA-256 is
`958ca475544962dfed2f741c14b3dd50c23e1962f16a782a8310701f067b67a2`.
The runner-persisted canonical schedule SHA-256 is
`b2d2edff4ef3a58f207bd79c9f978a1e88bb4b984392791e3e8f413be0be7aac`.
The experiment manifest SHA-256 is
`521b2f3c6645cf7f2e97430d2f72d405175934b24334fc99997d8dcca4c6537d`,
the scorecard SHA-256 is
`d86080d4020582196dfe069830dc1f9a8b65d7a5ed0258e8b7405cd50622bd90`,
and the independent integrity audit SHA-256 is
`cf4d6fc286c980522f169e14b25dc9966ed956e0fbf56325d2034be294c20970`.

The candidate binary SHA-256 is
`324074602725432e2b2ac20a1d9a5e2eda124663b97c221a4c9c1897cba296c5`,
source SHA-256
`ace7789619d06370ba57ac7dc88582358bc7dd3a16410a4f5bc52a06d71b43a9`,
combined source SHA-256
`c83ab18e3179360023ded37f5ff804e6fa72a65561f18f8865f022b8e97f8c97`,
and patch SHA-256
`b3b88268f3c550b0e15941d0d2f47be26117f4af455f3d60aa5ad0b7edc679d4`.
Kestrel is **Ours / Original**, author Luke Cameron. The frozen schedule
identifies ZZZKBot as **Ours / Port**, author Chris Coxe; McRave as
**Ours / Fork**, author Christian McCrave; and Stardust as **Ours / Fork**,
author Bruce Mackenzie Nielsen, with original source URLs retained.

## Run-by-run result

| Game | Run ID | Opponent | Map | Slot | Result | Candidate frame | Durable fps |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: |
| 1 | `20260920T234446-aa54b29e566f` | ZZZKBot | Destination | P2 | Loss | 5,893 | 2,462.8 |
| 2 | `20260920T234446-9cb8a424ab0d` | ZZZKBot | Heartbreak Ridge | P2 | Loss | 5,676 | 2,512.8 |
| 3 | `20260920T234446-0e7e59395da5` | ZZZKBot | Benzene | P1 | **Win** | 12,341 | 3,132.0 |
| 4 | `20260920T234446-dbc658de3260` | McRave-9Pool-treatment | Circuit Breaker | P1 | Loss | 15,813 | 425.9 |
| 5 | `20260920T234446-35248d13924d` | Stardust-repaired | Benzene | P2 | Loss | 10,295 | 1,314.0 |

Every row has reciprocal terminal results, zero child exits, and two archived
replay copies. Independent review recomputed every replay hash, parsed every
copy completely with `screp`, confirmed the registered race pair, and
verified `replay_header_frames + 1 == owning_callback_frame`. All registered
launcher, candidate, opponent, script, map, game-data, sidecar, and provenance
hashes matched. No state-hash mismatch or unregistered kill event was
observed. Candidate commands had zero rejections in all five games, including
zero gas-worker build attempts and zero build-specific `Unit_Busy`
rejections.

The scorecard labels four Zerg rows `review` because the registered Probe
interval mechanism failed. That is a gameplay/measurement gate, not an
infrastructure defect: all five terminals and replay copies are exact and
usable evidence. Throughput and duration are descriptive under v24; there is
no fixed speed requirement.

## Treatment and production timing

The retained v42 five-Probe Pylon treatment passed on all four Zerg rows. V44
then accepted exactly one sixth Probe, at callback frames 852, 888, 810, and
876, with 39, 42, 43, and 45 restoration-active cadence frames. Every row
reported one post-Pylon/pre-second-Gateway Probe acceptance and no seventh
acceptance in that interval. The Stardust sentinel reported zero v42/v43/v44
Zerg treatment activity.

The extra Probe did not advance early production. Replay commands show:

| Lane | v23 first Gateway | v24 first Gateway | Delta | v23 second Zealot | v24 second Zealot | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Destination P2 / ZZZK | 1,340 | 1,508 | +168 | 3,080 | 3,242 | +162 |
| Heartbreak P2 / ZZZK | 1,358 | 1,496 | +138 | 3,116 | 3,164 | +48 |
| Benzene P1 / ZZZK | 1,280 | 1,430 | +150 | 2,960 | 3,122 | +162 |
| Circuit Breaker P1 / McRave | 1,418 | 1,478 | +60 | 3,110 | 3,104 | -6 |

The same-map/slot comparison uses fresh seeds and is descriptive, but the
direction is consistent for the first Gateway: the sixth Probe's 50-mineral
cost was not repaid early enough to improve the production opening.

V44's order-aware reserve trace was aligned and valid on all rows. It removed
v23's same-callback ambiguity. Separately, Destination, Heartbreak Ridge, and
Circuit Breaker accepted a Probe at callback frames 2,604, 3,030, and 2,922;
Benzene accepted two at frames 2,514 and 3,012. Every command was strictly
after second-Gateway current and before the second Zealot. The existing
100-mineral reserve allowed these commands whenever at least 150 minerals were
available. This behavior is faithful to the implementation but fails v24's
frozen no-Probe interval gate.

## Defense and replay analysis

Destination accepted its first Gateway at frame 1,506, completed it at 2,634,
and accepted the second Zealot at 3,240. Qualifying pressure arrived at 3,694
with one global/local defender; that first Zealot died at 3,849. Heartbreak
Ridge accepted its first Gateway at 1,494, completed it at 2,555, and accepted
the second Zealot at 3,162. Pressure arrived at 3,588 with one global/local
defender and the first Zealot died at 3,724. Thus
`M = min(1, 1) = 1`.

Benzene remained a win, but it regressed from v23's two defenders at pressure
to one. Its first Zealot completed at 3,119, the second was accepted at 3,120,
and pressure arrived at 3,700; the next Zealot would complete just after that
window. Circuit Breaker improved from two to three global/local defenders at
its frame-4,434 pressure and did not lose its first home Zealot until 12,501,
so its eventual frame-15,813 loss remains a later combat/scaling problem.

Replay streams agree with the diagnostics. The sixth Probe appears once after
the Pylon in each Zerg opening. A later Probe also appears inside every
registered second-Gateway-to-second-Zealot interval. Production was not idle
once a Gateway could train: the primary bottleneck remained the delayed first
Gateway and first Zealot cycle.

## Next changes

The evidence supports this ranked shortlist:

1. Revert the sixth-Probe restoration. It delayed every first-Gateway replay
   command by 60-168 frames and failed both primary rows.
2. Test a four-Probe Pylon opening that skips the frame-0 Probe, then preserves
   the v43 second-Gateway and second-Zealot reserves. This directly tests
   whether spending 50 fewer minerals before the Pylon advances the first
   Gateway enough to complete a second defender.
3. Keep the stricter post-second-Gateway Probe freeze as a separate change.
   V24 proved the 100-mineral reserve still accepts Probes in that interval,
   although those commands retained enough minerals for a Zealot and were not
   the main first-cycle bottleneck.
4. Record the second Zealot completion frame directly rather than inferring it
   from the train frame and stable build time.
5. Keep Circuit Breaker later combat and Stardust PvP work separate from the
   Zerg opening hill climb.

The next gameplay experiment should isolate item 2 on the rejected v43 parent,
with item 4 as instrumentation. Item 3 should not be combined with it because
that would change a second gameplay variable.

## Limits

This is a five-game local Apple Silicon OpenBW diagnostic. Same-map
comparisons with v23 use different seeds and are descriptive. Replay commands
do not prove hidden state or command acceptance. The official BWAPI header
build passed, but official Win32 runtime transfer remains unverified. No v24
game enters the local rating graph or establishes tournament strength.
