# Kestrel Modular v1 second-Gateway safety — PASS TO FIVE-GAME SCREEN

The preregistered row ran once on 21 September 2026. Run
`20260921T045411-569a7d0daa5f` was a valid loss to ZZZKBot on Heartbreak
Ridge at seed `12409`; both processes exited zero and the reciprocal terminal
callbacks named ZZZKBot the winner. The candidate reached frame 5397 and the
opponent reached frame 5428. This outcome is diagnostic-only and does not
enter local Elo.

The candidate-specific mechanism passed. Kestrel accepted three Zealot trains,
observed the second completed Zealot at frame 3537, reached
`max_zealots = 3`, and released the lone-Zealot hold at the same frame. It did
not accept or observe a second Gateway before the game ended
(`second_gateway_accepted_frame = -1`, `second_gateway_current_frame = -1`).
That is the preregistered censored case: it proves there was no premature
acceptance during this row, but does not claim the bot would never request a
later Gateway.

Commandability and retained defenses also passed. All 43 issued commands were
accepted: three build, three train, 20 gather, 12 attack and five scout
commands, with no `Unit_Busy` error. The 96/48-pixel return hysteresis recorded
four entries, 111 active samples, five accepted return moves, 106 coalesced
moves and three releases. The 160-pixel close-threat rule recorded 29 eligible
samples and five accepted attacks, all originating inside the 96-pixel leash.

The generic, recovery, hold, hysteresis and second-Gateway scorecards all
passed with no issues. The replay audit also passed. Every accepted
close-threat event matched exactly one candidate-owned `Attack1` command two
replay frames later, with matching target coordinates; no hold-active
`AttackMove` appeared, and all five held-unit return commands targeted the
public base-center anchor.

Both source and archived replay copies parsed fully with the expected Zerg and
Protoss identities. Player 1's 66,168-byte replay has SHA-256
`1b6d21323e520cdad7a9d347d4be6dc8b3fda92ea6ddebc34a2000c183bda37f`
and header frame 5427, matching callback frame 5428. Player 2's 65,932-byte
replay has SHA-256
`51fba496779ad11085c5b3e57100d89067b3439864d0647b8f39ab8a7cf8f8cc`
and header frame 5396, matching callback frame 5397. The only terminal kill
events were the two registered terminal-drain events.

## Decision

**PASS TO FIVE-GAME SCREEN.** Every frozen integrity, retained-system,
commandability, two-Zealot overlap, release, second-Gateway ordering,
close-threat and replay gate passed. The loss does not change this mechanism
decision. A separately preregistered five-game mixed-opponent screen is the
next strength measurement; only its valid exact-build rows may enter the
corresponding local rating cohort.

## Durable evidence

- Experiment manifest SHA-256:
  `d45cd74cdf590af2d651c476fcc0100a1b78b2870b322a7f4710a506e1f8606c`.
- Match manifest SHA-256:
  `12174fb073fcf6ef4a6b185626637398e6e12ac2dbfb6f1c0f05cc06720d7a42`.
- Candidate diagnostic SHA-256:
  `bbc6a60c73a49eabfcc527d4fddbce8f80ec8e118f96ea6a44a30145abad4db9`.
- Generic scorecard SHA-256:
  `e65efc08cfa029fdfa8cfd2213405bc3a11f0473751299c2e345c2183d1b8fbd`.
- Recovery scorecard SHA-256:
  `3ba8dc94b71b5cf5eeb6b0235767d8a9b528fcf9381f2c702e290212c19e0c86`.
- Hold scorecard SHA-256:
  `0af80b36842ab069005ba9a89ed2e66d0d14b9a408d69670e78eaa4b6dcf20f2`.
- Hysteresis scorecard SHA-256:
  `2d21ce812422be33d19953a6810734fe9018ed215cea7a0767b313c4a2656d9c`.
- Second-Gateway scorecard SHA-256:
  `8e1f49e0c2e336d98dfcde785a4d9112af4c8156bd8c5267c2a6db1000181797`.
- Replay audit SHA-256:
  `208c04bfa59dfdcb0b6f8177aadc9cd32d0347a758fb5274f84dbc3eb0e24aca`.
