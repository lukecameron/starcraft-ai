# Kestrel Modular v1 second-Gateway safety — five-game screen result

The preregistered screen ran its five rows once, concurrently, on 21 September
2026. Four rows produced verified terminal outcomes and one row was
infrastructure-invalid. Kestrel Modular v1 finished **1–3 in valid games**:

| Opponent | Map | Result | Candidate frames | Commands / rejected |
| --- | --- | --- | ---: | ---: |
| ZZZKBot (Zerg) | Benzene | **Win** | 16,092 | 1,157 / 0 |
| UAlbertaBot (Terran) | Destination | Invalid | 99,840 | 2,345 / 0 |
| UAlbertaBot (Protoss) | Heartbreak Ridge | Loss | 36,893 | 2,457 / 0 |
| McRave memo fork (Zerg) | Circuit Breaker | Loss | 18,386 | 484 / 0 |
| Stardust repaired fork (Protoss) | Benzene | Loss | 11,721 | 534 / 0 |

The valid-game descriptive win rate is 25%, with a nominal Wilson 95% interval
of 4.6–69.9%. This interval is deliberately wide and is not a pooled Elo
claim. Every valid game had reciprocal terminal callbacks, zero child exit
codes, source/archive replay hash equality, complete `screp` parsing with the
expected races, and callback/header-frame alignment. All 4,632 candidate
commands in valid games were accepted, with no `Unit_Busy` error.

The UAlbertaBot-Terran row is excluded. Both children exited zero after a
transport callback at game frame 100,002, but neither recorded an ended
terminal result; Kestrel's winner remained null and no replay was produced.
The row is right-censored infrastructure evidence, not a win or loss, and the
registered no-retry rule was respected.

The clean ZZZK win is the strongest result. Kestrel observed the second
completed Zealot at frame 3411 and accepted the delayed second Gateway at
frame 7104. It reached 16 Zealots and issued 1,085 accepted attack commands.
The McRave loss also preserved the ordering gate: second Zealot completion at
3480 preceded second-Gateway acceptance at 8130. Neither known-Zerg row
exercised a 160-pixel close-threat attack, so that mechanism remains censored
in this screen rather than failed.

Two measurement limitations prevent these four outcomes from entering local
Elo. First, this exact candidate diagnostic did not record `latency_frames`,
which the rating extractor requires from both players before admitting a row.
Second, the generic hold replay auditor applies known-Zerg hold semantics to
non-Zerg games, producing policy findings on the otherwise replay-valid
UAlberta-Protoss and Stardust rows. The ZZZK and McRave replay audits passed;
the two Protoss rows passed all raw replay integrity checks but need the audit
scope repaired before later rating use. No rating configuration was changed.

The screen also exposed an enemy-race observation anomaly: Kestrel's final
diagnostic says `known_zerg = true` against the Stardust Protoss replay. That
row followed the Zerg opening even though both parsed replay headers identify
Stardust as Protoss. This is measurement/gameplay evidence for a focused race
classification investigation; it is not grounds to reinterpret the outcome.

## Decision

The candidate achieved the registered clean-win target and retained zero
command rejections, but the screen is **descriptive only** because one row was
invalid and the exact build lacks rating-required latency telemetry. Keep the
gameplay change and the first verified ZZZK win as evidence. The immediate
next build adds latency telemetry without changing gameplay, then requires a
fresh preregistered exact-build screen before any local Elo update.

## Durable evidence

- Batch manifest SHA-256:
  `9296dfc62aed898c0442279851285c498bc2f5d1a28bff55703292d4704b2ac1`.
- Valid match-manifest SHA-256 values: ZZZK
  `2c2170d9ba652e82273904d3ac99ce65b369bc474c404b947bc9bf9edba9bde7`,
  UAlberta-Protoss
  `dd7d4f1ab1d5c0d0ff0975241c07abdf5bbd606023dff56ac0dadcf57b9061ad`,
  McRave `19c0669055690666ddc08fb9f0befd386f26af9e1622819337534ba26ba06740`,
  and Stardust
  `013460322cd191617dc5c834c68b09d5651fe60825b3d827a1888af4581ca996`.
- Invalid UAlberta-Terran match-manifest SHA-256:
  `b6004bd674e8737bf4d4315cf09b40c3cfcfe35b9ade88e09e5bbb4376d62712`.
- Replay-audit SHA-256 values by row:
  `7dff7fbca44a91ea026d3bfacd204761a0164fdba895177b65888f9edb5d423d`,
  `2f01c772b67a3e61178d1a37e789fdd76416f9d33a9e5d1f5348ba491f1d4ece`,
  `1e57d4b20a2edd2ebf1b0e757343706b3fa008f1bb0f09417c4b655f3d72265a`,
  `2031cdc568d939e17a6add23475a27cec7553680767507b4a385d4917c79f0b3`,
  and `58cd54cb9a35f11d2cc5cd832a9272e0ddf7f9236f7e8dae6314747650fe902b`.
