# Kestrel hill-climb v23 result

Date: 2026-09-21
Decision: **REJECT**

The fixed five-game `Kestrel-v43-second-zealot-reserve` screen ran once with
five concurrent launchers and no retry, reseed, replacement, or rerun. All five
games completed cleanly: Kestrel won the Benzene ZZZK row and lost the two
primary P2 ZZZK rows, the McRave row, and the Stardust sentinel. The reserve
moved the second Zealot command earlier and restored two defenders plus a win
on Benzene. It still left only one completed defender at first pressure on both
primary rows, so the registered gameplay gate fails and v43 is `REJECT`.
Canonical Kestrel v13 and local Elo remain unchanged.

## Frozen identity and evidence

The registered plan SHA-256 is
`95249c1b444ca20ef50f56063cd3fc51f943779732472df542c5c5b2be54ef91`.
The committed source schedule SHA-256 is
`cb81a0916a19fc0aa383ea1c2da460e8ff040d176afc54247c095bfd60a46784`;
the runner-persisted canonical schedule SHA-256 is
`bec5be688a47d893d05d51c009820af33c143081b373303c33d10396bffe874c`.
The experiment manifest SHA-256 is
`faa831af17a52f4180b62f0af00e84da9e1f812b1b99e3056f00a0aca5524cc5`,
the scorecard SHA-256 is
`26c2a209333564a66e237295398648dd9b4299feccc843ed2ef935e970321dfc`,
and the independent integrity audit SHA-256 is
`7d448d26715bb27204e77f592179a1144ffb4bbe25918e8edc6a0c9110cd67d1`.

The candidate binary SHA-256 is
`234dcc4b0dc57ce386c19d19f249546c62986b1806396fb3d2fcb615b5f62287`,
source SHA-256
`1d0783bac7b559bae28616a7d19d00dd77d70c94c43c3091a69171cf09a636cf`,
combined source SHA-256
`6259f12081942c6368bd9bfa33a800bd0c5e966a8c9d6922227234502ff90daa`,
and patch SHA-256
`40f36042d9f1390274b8f04afff45b59d8011f9e1f60f9e7e405c833232242ce`.
Kestrel is **Ours / Original**, author Luke Cameron. The schedule identifies
ZZZKBot as **Ours / Port**, author Chris Coxe; McRave as **Ours / Fork**,
author Christian McCrave; and Stardust as **Ours / Fork**, author Bruce
Mackenzie Nielsen, with original source URLs and frozen identities retained.

## Run-by-run result

| Game | Run ID | Opponent | Map | Slot | Result | Candidate frame | Durable fps |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: |
| 1 | `20260920T215006-dc13ce0caf72` | ZZZKBot | Destination | P2 | Loss | 5,428 | 2,567.7 |
| 2 | `20260920T215006-a8d0da4f9a13` | ZZZKBot | Heartbreak Ridge | P2 | Loss | 5,273 | 2,590.1 |
| 3 | `20260920T215006-4c23fcecced6` | ZZZKBot | Benzene | P1 | **Win** | 12,310 | 3,265.1 |
| 4 | `20260920T215006-38cb5aa358d2` | McRave-9Pool-treatment | Circuit Breaker | P1 | Loss | 15,658 | 551.9 |
| 5 | `20260920T215006-fe12f40698f9` | Stardust-repaired | Benzene | P2 | Loss | 10,388 | 1,376.1 |

All five rows have reciprocal terminal results, zero child exits, and ten
archived replay copies. Independent review recomputed every replay hash and
size, parsed every copy completely with `screp`, confirmed the registered race
pair, and verified `replay_header_frames + 1 == owning_callback_frame`. No
state-hash mismatch or unregistered kill event was observed. Every row exceeded
the descriptive 384 fps floor. Candidate commands had zero rejections in all
five games, with zero gas-worker build attempts and zero build-specific
`Unit_Busy` rejections. All retained construction, Gateway-builder, emergency,
staging, shared-target, scaling, cap, commandability, and public-information
checks passed where observed.

## Treatment and production timing

The retained five-Probe treatment passed on all four Zerg rows and stayed
inactive against Stardust. First-Pylon acceptance was frame 696 on Destination,
618 on Heartbreak Ridge, 648 on Benzene, and 666 on Circuit Breaker. V43's
second-Zealot reserve was active for 161, 161, 163, and 163 callback cadences,
and recorded 102, 113, 108, and 99 blocked Probe opportunities respectively.
The Stardust sentinel reported zero Zerg treatment activity and zero blocks.

| Lane | v22 second Zealot replay command | v23 command | Advance | v23 second Gateway completed |
| --- | ---: | ---: | ---: | ---: |
| Destination P2 / ZZZK | 3,218 | 3,080 | 138 | 3,085 |
| Heartbreak P2 / ZZZK | 3,206 | 3,116 | 90 | 3,123 |
| Benzene P1 / ZZZK | 3,140 | 2,960 | 180 | 2,956 |
| Circuit Breaker P1 / McRave | 3,122 | 3,110 | 12 | 3,105 |

No Probe train was accepted strictly between second-Gateway current and the
second Zealot on any Zerg row. Heartbreak accepted a Probe and the second
Zealot in the same frame, 3,114 in callback telemetry and 3,116 in the replay;
the Nexus iteration left the registered 100 minerals for the later Gateway
iteration. This violates the plan's stricter inclusive protected-interval
wording even though it did not delay that Zealot command.

The generic scorer also marked Destination, Benzene, and Circuit Breaker for a
reserve block at the exact second-Zealot frame. Source order shows the Nexus
block observation occurs earlier in `trainUnits()` than the Gateway acceptance
on that cadence, so this is an ambiguity in frame-only telemetry rather than a
post-acceptance gameplay read. The registered inclusive trace gate remains
failed; the evidence is not silently regraded after results.

## Defense and replay analysis

Destination's first Gateway completed at frame 2,378, its first Zealot trained
at 2,472 and completed at 3,077, and its second Zealot trained immediately at
3,078. Qualifying pressure arrived at 3,522 with only one global and local
combat unit; that Zealot died at 3,665. The second unit could not complete
before pressure.

Heartbreak Ridge followed the same sequence: first Gateway completion 2,415,
first Zealot train/completion 2,508/3,113, immediate second train at 3,114,
then pressure at 3,539 with one global/local defender and the first loss at
3,677. The Probe accepted on the same frame did not consume the reserved 100
minerals, but the first Gateway cycle itself was already too late.

Benzene completed the second Gateway at 2,956 and accepted the second Zealot at
2,958 callback time. It had two global/local completed defenders when pressure
arrived at 3,648 and won at frame 12,310. This restores the v21 sentinel state
that v22 had lost. Circuit Breaker likewise had two defenders at its qualifying
army pressure at 4,373, survived its first home combat loss until 11,743, and
then lost at 15,658; its remaining problem is later than the opening reserve.

Replay command streams agree with the diagnostics: the primary rows no longer
spend on Probes before the second Zealot, but their second Zealot commands still
occur 161 and 180 frames too late to complete by the observed pressure frames.
The immediate bottleneck is now first-Gateway/first-Zealot cadence and early
mineral income, rather than post-Gateway Probe spending.

## Next changes

The evidence supports this ranked shortlist:

1. Restore exactly the sixth Probe immediately after the early Pylon is
   accepted, then freeze additional Probe production until the second Gateway
   is current. This keeps v42's early Pylon while testing whether one extra
   miner advances the Gateway and Zealot cycles needed by the primary rows.
2. If the sixth worker does not advance the first Gateway enough, isolate an
   earlier first-Gateway construction rule; the primary second defenders need
   roughly 160-180 more frames to complete before pressure.
3. Record reserve-block ordering explicitly within a callback, or suppress the
   block event when the same cadence accepts the second Zealot, so the scorer
   can distinguish pre-command blocking from post-command activity.
4. Keep Circuit Breaker composition and engagement work separate because its
   opening produced two defenders and failed much later.
5. Keep the Stardust non-Zerg loss separate from the Zerg opening hill climb;
   its treatment sentinel passed and its PvP weakness is a different policy.

The next experiment should isolate item 1 and retain the v42/v43 evidence.
V43's Benzene win is a useful positive signal, but the two failed primary lanes
and registered trace violation prevent advancement or Elo inclusion.

## Limits

This is a five-game local Apple Silicon OpenBW diagnostic. Same-map comparisons
with v22 use different seeds and are descriptive. Replay commands do not prove
hidden state or command acceptance. The official BWAPI header build passed,
but official Win32 runtime transfer remains unverified. No v23 game enters the
local rating graph or establishes tournament strength.
