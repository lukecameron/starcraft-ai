# Kestrel hill-climb v22 result

Date: 2026-09-21
Decision: **REJECT**

The fixed five-game screen of `Kestrel-v42-five-probe-pylon` ran once with
five concurrent launchers and no retry, reseed, replacement, or rerun. Four
games completed as losses and the UAlbertaBot-Terran row reached its registered
120-second wall timeout. V42 executed its five-Probe Pylon policy in all four
Zerg rows, but one row missed the registered Pylon-advance threshold, both
primary P2 ZZZK lanes still had only one completed local defender at first
pressure, and the previously passing Benzene sentinel regressed to one defender
and a loss. These independent failures require `REJECT`. V42 does not advance,
and canonical Kestrel v13 and local Elo remain unchanged.

## Frozen identity and evidence

The registered plan SHA-256 is
`2cfcbf9c7f1870c5e90579a452b0dbd4e74639c2554485a24897133e115ff3a0`.
The committed source schedule SHA-256 is
`4ac796e5ae2da62c8bcab418717858dea081b73cb3999bdf9417b37bfeae56a4`;
the runner-persisted canonical schedule SHA-256 is
`d399b2123d72516e59eb0fc4520819f0100e7364c5425fe45ebda71b83a55c78`.
The experiment manifest SHA-256 is
`1c7c845177aca82b286b960abc692b03da8c5412623cf19ac51e4d850f14de2b`,
the scorecard SHA-256 is
`07cb2478cd9a88476302f16d088c0ab7c623dad2afae85c23bc422f3bea04107`,
and the independent integrity audit SHA-256 is
`91c5dc9853e3d4b7e8d0bc4b72388c7f260155a002d4ee0d5d85512e2e9e233b`.

The candidate binary SHA-256 is
`a212db989667f9abc5ed88c82ea474af03a9a0e353924422e131feacaec139f7`,
source SHA-256
`33bfc50879539f84ed886ed3430f813ad0fbc7d9ad7c12b380ed308ffea8a950`,
combined source SHA-256
`114de3d7522e9936fa30f918f1ba368dcd4e4799f958c4bd66bfc1ac0560356a`,
and patch SHA-256
`0f50c3c1106a00ed5cf9852ac34e227ff15d4e4ac7925db072442710c4df11ec`.
Kestrel is **Ours / Original**, author Luke Cameron, with source at
[lukecameron/starcraft-ai](https://github.com/lukecameron/starcraft-ai/tree/main/bots/kestrel).
The frozen schedule identifies ZZZKBot as **Ours / Port**, author Chris Coxe;
McRave as **Ours / Fork**, author Christian McCrave; and UAlbertaBot as
**Ours / Port**, author David Churchill, with each original source URL and
build identity preserved.

## Run-by-run result

| Game | Run ID | Opponent | Map | Slot | Result | Candidate frame | Durable fps |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: |
| 1 | `20260920T211709-3cac45da16f9` | ZZZKBot | Destination | P2 | Loss | 5,211 | 2,569.8 |
| 2 | `20260920T211709-32e13ddc3cfc` | ZZZKBot | Heartbreak Ridge | P2 | Loss | 5,335 | 2,699.2 |
| 3 | `20260920T211709-e3b8432d5601` | ZZZKBot | Benzene | P1 | Loss | 5,583 | 2,686.4 |
| 4 | `20260920T211709-c7ca11b9d488` | McRave-9Pool-treatment | Circuit Breaker | P1 | Loss | 18,789 | 401.1 |
| 5 | `20260920T211709-aadbbf559d96` | UAlbertaBot-Terran | Destination | P1 | Timeout | 96,240 observed | 800.3 |

The four terminal rows have reciprocal winners, zero launcher failures, and
eight archived replay copies. Every copy matches its recorded hash and size,
parses fully with `screp`, has the registered races and exact owner, and has a
header frame one below the owning callback frame. The timeout is preserved in
the fixed denominator. It has no terminal result or replay; both child
processes were terminated with `-15` at the wall cap, so it is not an
integrity-valid terminal and was not replaced.

Every row exceeded the descriptive 384 fps floor, including the timeout's
observed interval. The four valid Zerg terminals had zero rejected candidate
commands, zero gas-worker build attempts, and zero build-specific `Unit_Busy`
rejections. The timeout recorded 16 rejected commands out of 13,684 attempts
(0.117%), zero gas-worker build attempts, and zero build-specific `Unit_Busy`
rejections. All observed construction, Gateway-builder, emergency, staging,
shared-target, scaling, cap, commandability, and public-information integrity
checks passed. The timeout reported the expected inactive non-Zerg treatment
sentinels, but its missing terminal prevents it from satisfying the registered
valid-sentinel gate.

## Treatment and timing

All four Zerg rows reported positive five-Probe treatment frames, true Pylon
acceptance, and a treatment acceptance frame equal to the first Pylon frame.
Each accepted exactly one Probe train before the first Pylon, the initial
frame-0 train. Three rows met the registered 180-frame advance threshold;
Destination missed it by 54 frames.

| Lane | v21 Pylon | v22 Pylon | Advance | Registered latest | Gate |
| --- | ---: | ---: | ---: | ---: | --- |
| Destination P2 / ZZZK | 822 | 696 | 126 | 642 | Fail |
| Heartbreak P2 / ZZZK | 846 | 618 | 228 | 666 | Pass |
| Benzene P1 / ZZZK | 810 | 576 | 234 | 630 | Pass |
| Circuit Breaker P1 / McRave | 852 | 606 | 246 | 672 | Pass |

The earlier Pylon moved the first Gateway current 108, 253, 249, and 256
frames earlier than v21. It moved the second Gateway current only 80 and 147
frames earlier on the two primary lanes, 13 frames later on Benzene, and 140
frames earlier on Circuit Breaker. First Zealot completion advanced 60, 144,
222, and 252 frames respectively. These are descriptive same-map/slot
comparisons with different seeds, not paired causal estimates.

## Defense failure and replay evidence

Destination saw qualifying pressure at frame 3,524 with one completed global
and local combat unit; that unit died at 3,676. Heartbreak saw pressure at
3,539 with one global/local unit and lost it at 3,691. Both primary repair
lanes fail the registered two-defender gate. Benzene regressed from v21's win
with two global/local defenders to a loss with one defender at frame 3,643 and
the first loss at 3,794. Circuit Breaker passed the opening defense with four
global/local defenders at frame 5,481, survived until its first home combat
loss at 14,365, and later lost at frame 18,789; that failure is later than the
opening policy under test.

Replay commands expose the immediate production conflict. Destination trained
Probes at frames 2,612 and 2,918 before accepting its second Zealot at 3,218.
Heartbreak did the same at 2,624 and 2,930 before the Zealot at 3,206. Benzene
trained Probes at 2,546 and 2,852 before the Zealot at 3,140. These commands do
not by themselves prove causal strength, but they agree with the public
diagnostic timing: after the second Gateway became current, Probe production
consumed minerals while the second combat unit still missed the pressure
window.

## Next changes

The evidence supports this ranked shortlist:

1. Keep a hard 100-mineral production reserve after the second Gateway is
   current until the second Zealot train is accepted, so Nexus iteration order
   cannot spend the combat unit's minerals on a Probe.
2. Restore the sixth worker immediately after the early Pylon is accepted,
   then freeze further Probe production until the second Gateway is current;
   the five-worker bank advanced the Pylon much more than the second Gateway.
3. Investigate the Destination P2 Pylon delay separately because its frame-696
   acceptance missed the mechanism gate while the other three Zerg rows passed.
4. Keep McRave composition/engagement work separate from the opening repair;
   that row had four defenders at first pressure and failed much later.
5. Treat the long UAlbertaBot-Terran timeout as a separate bounded-runtime
   problem before relying on that sentinel for a complete cohort.

The next experiment should isolate one production/economy change and retain
the v22 treatment telemetry. V22's zero wins, invalid sentinel, failed primary
lanes, and Benzene regression are not Elo evidence and cannot promote any
build.

## Limits

This is a five-game local Apple Silicon OpenBW diagnostic. Different seeds
limit v21 timing comparisons, and one row timed out without a replay. Replay
commands are useful qualitative evidence but do not prove command acceptance,
hidden state, or general ladder strength. The scorecard validates generic v42
telemetry but does not encode the v22-specific 180-frame thresholds; root and
an independent Luna audit recomputed those gates from the frozen plan and raw
diagnostics.
