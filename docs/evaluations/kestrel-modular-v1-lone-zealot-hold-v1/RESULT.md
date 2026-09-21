# Kestrel Modular v1 lone-Zealot hold result

Date: 2026-09-21  
Decision: **REJECT**

The one registered Heartbreak Ridge row ran exactly once on fresh seed 12403.
The hold mechanism exercised cleanly: it suppressed lone-Zealot attacks in 188
public-state samples, affected two distinct completed Zealots, accepted both
home moves, and issued no attack command. It still never observed two
completed Zealots at once, so the frozen overlap and release gates fail. The
row is not retried and does not advance to the five-game screen or local Elo.

## Frozen identity and run

- Candidate binary SHA-256:
  `b387872d7ec3e9cd5a96041992699699e5606c0c0f9be67ad85cfdfcb769e81a`
- Candidate source-manifest SHA-256:
  `bf88a5ca1dd21f93635fd2258bc0ac02e54f7ca61099c0ad25b9b65d0b4edd9e`
- Candidate build-sidecar SHA-256:
  `ec080508fbcb1d79d2729684879fc7e66fc8780f51bbbfdc2d61b55eb5b8c3b7`
- Plan SHA-256:
  `b8600900ada0d45bd5bb2f28cda4de5dd3b31150df6b7f6a0335af674840f3a3`
- Schedule SHA-256:
  `1602c15a3404c7c2f5866e1b36469f4c4cce06f923b871f18e7ad3a6788ae2a7`
- Run ID: `20260921T022121-822fa892eafd`
- Run/final manifest SHA-256:
  `61615ed4ac2698e1459356a8bceea500350b66c39c67aa3e7ad0882a20518d21`
- Experiment manifest SHA-256:
  `4a4951debb4262409d29c6e0b14b32e1d2e50f3c0fe07c50ee3985039cfe0e96`
- Candidate diagnostic SHA-256:
  `bf99a79a0e50af77587281ca979a48502ad405d68f0d237a9e98a6a767918a1b`

Kestrel Modular v1 is **Ours / Original**, author Luke Cameron. ZZZKBot is
**Ours / Port**, original author Chris Coxe, with source at
<https://github.com/chriscoxe/ZZZKBot>. Kestrel lost at callback frame 5,242;
ZZZKBot won at callback frame 5,273. Both children exited zero. The game
completed durably in 1.97 seconds at about 2,670 logical frames per wall
second. Candidate and opponent peak RSS were approximately 43.4 and 44.2 MB.

## Independent integrity review

The plan, schedule, candidate, opponent, launcher, engine, map, game data,
sidecars, source manifests, slot, race and seed match their frozen identities.
The two source replay files and archived copies are byte-identical:

| Owner | Bytes | Replay SHA-256 | Header frame | Callback frame |
| --- | ---: | --- | ---: | ---: |
| ZZZKBot / P1 | 65,452 | `6377273435c8caae2db2a4349847fa8258303e963137403573f98b0e33890af5` | 5,272 | 5,273 |
| Kestrel Modular v1 / P2 | 65,294 | `719795f7cea0f87bf8d10bb0c317ef8ad209bc3500f160f57ac1348d076a3197` | 5,241 | 5,242 |

All four source/archive parses exit zero with `screp`, report Zerg and
Protoss in the expected slots, contain no command parse errors, and satisfy
`header frame + 1 == owning callback frame`. The logs contain only the two
registered terminal-drain kill events, `transport_callback/-1` and
`controller_not_occupied_after_action/87`, with no sync mismatch. The
owner-filtered command stream identifies Kestrel as player ID 1 and contains
two ordinary home `Move` orders at replay frames 3,365 and 3,884, with no
candidate `Attack1` or `AttackMove` order. This is full parser validation,
not replay playback validation.

## Mechanism evidence

The candidate issued 27 commands with zero rejection: build 3/0 rejected,
train 4/0, gather 18/0, attack 0/0 and scout 2/0. `Unit_Busy` remained zero.
Gather accounting reconciles at 18 accepted assignments, with nine public
preflight skips. Builder selection recorded two cargo deferrals. Each accepted
build maps to an ordered current and completed construction event.

The four-Probe Pylon was accepted at frame 387 and completed at 998. The two
Gateways were accepted at frames 1,260 and 2,163 and completed at 2,324 and
3,275. The second Zealot train was accepted at frame 3,276, but the public
self-state never contained two completed Zealots simultaneously. The hold
therefore remained active through the loss and recorded release frame `-1`.
All three registered scorers are structurally complete; the base and recovery
scorers fail the second-completed-Zealot gate, while the hold scorer also fails
the required release equality.

The two distinct held-unit identities show that the first completed Zealot was
no longer present before another completed Zealot entered the hold. The
preserved command stream does not prove the exact disappearance or death frame.
This valid rejection narrows the next work: passive home staging alone does not
create defender overlap against this early pressure. The next candidate should
isolate a safer defensive staging position, earlier combat production, or an
explicit local engagement policy, with unit-lifecycle telemetry to distinguish
survival from production timing.

This is diagnostic Apple Silicon OpenBW evidence from one short loss. It does
not measure playing strength, establish local Elo, validate replay playback,
or verify the official Win32 BWAPI runtime.
