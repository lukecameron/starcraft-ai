# Kestrel Modular v1 tight close-threat defense result

Date: 2026-09-21
Decision: **REJECT**

The one fixed Heartbreak Ridge row completed validly. The 160-pixel threat
radius reached the main tactical target: the second Zealot completed at frame
3537 while the first was still alive, `max_zealots` reached two, and the hold
released at that same frame. Three return entries produced 73 active return
samples, three accepted anchor moves, 70 coalesced return requests, three
return releases, and zero rejected commands. The candidate nevertheless fails
two frozen gates. Two accepted Gateway construction lifecycles were incomplete
when the bot lost, so all four registered scorecards reject it. The frozen
replay auditor also reports nine missing `Attack1` commands because it searches
only before the first hold release even though all nine accepted close-threat
events happened during later one-Zealot hold epochs. Direct `screp` inspection
shows all nine commands at the expected event-frame-plus-two offset with the
expected target coordinates, but the preregistered auditor itself did not pass
and cannot be changed after seeing the outcome. The row is therefore
**REJECT**, does not enter local Elo, and does not advance to the five-game
screen.

## Frozen identity and valid row

- Candidate binary SHA-256:
  `396f6c66088fc1dadb3ecb1dee7850712bad49dbf683ce14d54c73e7b70bf33b`
- Candidate source-manifest SHA-256:
  `428dce70e38365a390801bf30a3bc7a6594548509ee69bf00b091b56cbb3edce`
- Candidate build-sidecar SHA-256:
  `a450cdc64ff071b91afa82d023ea604e893afd54141bb43fdef22b5d9db60fba`
- Candidate source commit: `a63a7d5f03e8ba3d922161fc66a3c3933fe4485e`
- Preregistration commit: `2f7f980`
- Plan SHA-256:
  `6852fefb32f132a1f3c6eddd9dfd0f3053a4bd9ed3a5a08f5bff7eba70ffec17`
- Source and persisted schedule SHA-256:
  `a781873c84425944c0a1ca9c2a02c2f2e47cd38465d675d179e905cf2f12fa3d`
- Run ID: `20260921T042715-19076dbafd78`
- Match/root manifest SHA-256:
  `407c386245c0d4623f343f64ae6b58e3a4d4debb96b4265bd93c56c419f660d3`
- Experiment manifest SHA-256:
  `8bdf4dd177819f2f294c1166aaa3c8257275e57f28193493bacd332f2933edc7`
- Candidate diagnostic SHA-256:
  `36ff59335499e79878bb003cc08f03c679bf0aa2b7f19916c69567bb29309e07`
- Durable replay audit SHA-256:
  `554fd87dcfe784a9c24eb78aa4a89d5deb325a14d1f7ccd740a7f581aee26de2`
- Generic, recovery, hold, and hysteresis scorecard SHA-256 values:
  `9e5f5ca1df179fd87dc63c00aa2fd0b2601b9cbf1f70a0bce9020d82a998ee61`,
  `ae4f53ce652b5064b578de9eefe9931b8c31a32b600cc6ed2639d15b7dda9efa`,
  `2d834abd6ba07f94963364e39c55ef569219b061708bf0cfadef21cba5f30579`,
  and `7f07d251639dff1322b94e914f06ae7edd7fd980f2bdc7fae6a3ff05505c72c5`
  respectively.

Kestrel Modular v1 is **Ours / Original**, author Luke Cameron. ZZZKBot is
**Ours / Port**, original author Chris Coxe, with source at
<https://github.com/chriscoxe/ZZZKBot>. The row used ZZZKBot as player 1 and the
candidate as player 2, Heartbreak Ridge, fresh seed 12408, LF3, and empty
isolated learning state. Both children exited zero. ZZZK reported a win at
callback frame 5521; Kestrel reported a loss at frame 5490. The registered
terminal-drain kill event was the only terminal event.

Both source and archived replay copies passed full `screp` parsing with Zerg
player 1 and Protoss player 2 and no parse-error commands. Player 1's 66,490
byte replay has SHA-256
`44c31e39bb8c13c5847f10e85e41abe4a2861aefad3fe02d688609566791e23f`
and header frame 5520. Player 2's 66,191 byte replay has SHA-256
`5cd947133d3ebaa0e525550452206380c530079872f4069731bf129aaa4132ee`
and header frame 5489. Both satisfy the owning callback-frame relation.

## Mechanism and retained-system evidence

The candidate emitted 47 commands with no rejection or `Unit_Busy` error:
five builds, three trains, 18 gathers, 18 attacks, and three scout commands.
The Pylon was accepted at frame 378 after four completed Probes, both mineral
reserves were active, and the second Zealot was trained at frame 2931 and
completed at frame 3537. One accepted Gateway completed, while later Gateway
attempts accepted at frames 2172 and 2871 remained incomplete at game end.
That violates the scorecards' registered construction-completion invariant.

The tight defense counters reconcile in aggregate and per held unit. Unit 160
was held from frames 2931–3534 and returned to the anchor successfully before
the second completion released the hold. Later one-Zealot epochs held units
166 and 174, producing nine accepted close-threat attacks and three total
accepted return moves. All recorded attack origins remained within the
96-pixel leash, and the close-threat samples obeyed the 160-pixel target
radius.

The durable replay audit failed because its frozen implementation filters the
candidate `Attack1` rows to frames before the first release and then attempts
to match later accepted events against that filtered set. The replay itself
contains matching `Attack1` orders at frames 3758, 3764, 3788, 3815, 3836,
4478, 4487, 4508, and 4556. Each is exactly two frames after its diagnostic
event and carries the same target coordinates. This explains the audit
failure but does not waive the registered pass requirement. A future plan
must model distinct hold epochs and freeze the repaired auditor before play.

The row ran at 1,388.65 logical frames per wall second. Candidate process peak
RSS was 43,565,056 bytes and maximum callback wall time was 2.83229 ms. These
are Apple Silicon OpenBW diagnostic measurements, not original-game tournament
validation.

The next evaluation should repair the evaluator's hold-epoch handling and
separate strategically optional late construction from the opening lifecycle
invariant before registering a fresh scenario. The 160-pixel behavior is a
promising tactical result, but the current experiment cannot establish a
promotion.
