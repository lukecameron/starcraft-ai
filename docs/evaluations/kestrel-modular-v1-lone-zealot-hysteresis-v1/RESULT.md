# Kestrel Modular v1 lone-Zealot leash hysteresis result

Date: 2026-09-21
Decision: **REJECT**

The one fixed Heartbreak Ridge row completed validly. The 96/48-pixel
hysteresis mechanism exercised cleanly: three return entries produced 117
active return samples, five actually issued and accepted anchor moves, 112
coalesced return requests, two return releases, and zero rejected commands.
Four accepted close-threat attacks all originated within the leash and matched
the candidate replay at the registered LF3 offset. The candidate still did not
observe two completed Zealots simultaneously, and the hold never released.
The registered overlap and release gates therefore fail. This valid loss is
**REJECT**, not infrastructure-inconclusive; it does not enter local Elo or
advance to the five-game screen.

## Frozen identity and valid row

- Candidate binary SHA-256:
  `c1b45a4d70bfb8d52c0fe981e849bbbad63b3fb1f9db649f25fb928f03d2a2fd`
- Candidate source-manifest SHA-256:
  `f42c18ca88cd4b1ffac83b5977ceb0e8605c4f6030e1770aa96e094eb36e67da`
- Candidate build-sidecar SHA-256:
  `1672f749ba1bbcd9b8ddcb2e010de563ad96e4f6555eab6563040daf1483249e`
- Candidate source commit: `6babb1fa9cc36b3e2091efb68403c63443eec0fe`
- Preregistration commit: `40f7cd223e7fb0a60349c1f9a836d641fd396562`
- Plan SHA-256:
  `1afc0d0258e21af63ad035a9d7cc69f39b9f0aa1931bd5056ba1453ac99b97e4`
- Source and persisted schedule SHA-256:
  `a6f009c7147b9e57d5754d207e4996a5d2df63b0bdc7654dd7c17d543822a5da`
- Run ID: `20260921T041428-775197f3f051`
- Match/root manifest SHA-256:
  `0c28854a32630be193b91192196895706c7de6a9d3aad9851cf84ca8bd2830dc`
- Experiment manifest SHA-256:
  `e73ac2002691fe84f89abb850637d17f730900c1f15c427ae9bdbaa3c8720d36`
- Candidate diagnostic SHA-256:
  `514df4d8c9508c35a39f369489fb1c527137542abab3ffe511b787a417a193dc`
- Durable replay audit SHA-256:
  `a2d96988a32e0c68ed65fa6a15df0a65ae24c1a9093bcc4bcfc4cde82d6b696f`

Kestrel Modular v1 is **Ours / Original**, author Luke Cameron. ZZZKBot is
**Ours / Port**, original author Chris Coxe, with source at
<https://github.com/chriscoxe/ZZZKBot>. The row used ZZZKBot as player 1 and the
candidate as player 2, Heartbreak Ridge, fresh seed 12407, LF3, and empty
isolated learning state. Both children exited zero. ZZZK reported a win at
callback frame 5304; Kestrel reported a loss at frame 5273. The two registered
terminal-drain events were the only kill events.

Both source and archived replay copies passed full `screp` parsing with Zerg
player 1 and Protoss player 2 and no parse-error commands. Player 1's 65,399
byte replay has SHA-256
`c3b82cb19b2082440e5a021db415f95b03e4468d0a6148a3f7ef8ad2b61b16f4`
and header frame 5303. Player 2's 65,213 byte replay has SHA-256
`ea1fd184666a8b0dab12d9f99ae8a9fb4ae53216bd82e7b2b32623063d2c9403`
and header frame 5272. Both satisfy the owning callback-frame relation.

## Mechanism and retained-system evidence

The candidate emitted 34 commands with no rejection or `Unit_Busy` error:
three builds, four trains, 18 gathers, four attacks, and five moves. The Pylon
was accepted at frame 378 after four completed Probes, both mineral reserves
were active, construction lifecycles reconciled, the second Gateway became
current at frame 2199, and the second Zealot train was accepted at frame 3237.
The generic, recovery, hold, and hysteresis scorecards were structurally
complete. Each failed only its registered second-completion/release mechanism
requirements.

The hysteresis counters reconcile in aggregate and per held unit. Unit 165 was
held from frames 3318–3780, entered return state twice, released once, issued
three accepted anchor moves, and made one accepted close-threat attack. Unit
169 was held from frames 3843–4059, entered and released once, issued two
accepted anchor moves, and made three accepted attacks. Their lifecycles are
still disjoint by 63 frames, so there is no verified two-defender overlap.
This is descriptively closer than the prior close-threat row's 123-frame gap,
but different fresh seeds mean the change does not establish a causal gain.

The replay auditor passed with no issues. Candidate-owned replay commands have
five `Move` orders, all to the base-center anchor `(3808,1840)`, no
`AttackMove`, and four `Attack1` orders at frames 3629, 3983, 4031, and 4043.
Those exactly equal the accepted telemetry event frames plus two and have the
same target coordinates. Replay `UnitTag` values cannot be mapped reliably to
BWAPI telemetry unit IDs, so the identity subcheck remains explicitly
unsupported; ownership, frame, order, and coordinates pass.

The row ran at 2,374.78 logical frames per wall second. Candidate process peak
RSS was 43,991,040 bytes and maximum callback wall time was 2.19075 ms. These
are Apple Silicon OpenBW diagnostic measurements, not original-game tournament
validation.

The next experiment should retain the working hysteresis and reduce how far
from the anchor a lone held Zealot may select a threat. That isolates the
remaining exposure while keeping the opening and economic systems unchanged.
