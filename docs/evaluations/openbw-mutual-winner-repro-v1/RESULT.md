# OpenBW reciprocal winner investigation

## Preserved failure

Batch game 10, run `20260920T035743-5518317f90cd`, completed both launcher processes with return code 0 and empty stderr, but both bot callbacks recorded `winner: true`. The harness correctly marked `outcome_verified: false` and the run `incomplete`; it must not be scored.

The two client-local replays disagree about the winner:

| Local replay | SHA-256 | Frames | Terminal command | Parsed winner |
| --- | --- | ---: | --- | --- |
| UAlbertaBot player 1 | `5326c82cae042b5989153d0f27deeb31f81e12e9c7c3877c421473287d6b963d` | 18,664 | McRave/player ID 0 leaves as `Dropped` at frame 18,633 | Team 2, UAlbertaBot |
| McRave player 2 | `b836331b03e13b3e8b7b796460fd5c2e9fa5d2a36d9607e5e79d3bc865e94e9a` | 18,633 | UAlbertaBot/player ID 1 leaves as `Dropped` at frame 18,631 | Team 1, McRave |

The decoded command sequences match through list index 239,011. The first difference is the McRave-local replay's frame-18,631 `Leave Game` command from UAlbertaBot; the UAlbertaBot-local replay instead continues with the previously synchronized commands and later records McRave leaving. This is a client-local terminal disagreement, not evidence that both players won one authoritative result.

## Exact reproduction

The preregistered one-attempt reproduction used the same map, slots, names, frozen modules, corrected engine package, scenario seed 3003, McRave bot seed 3003, and 120-second cap. It is preserved as run `20260920T040129-096a092f98d9`.

The attempt followed a different permitted trajectory and did not reproduce the reciprocal result. UAlbertaBot recorded `winner: false` at frame 19,874 and McRave recorded `winner: true` at frame 19,905; both processes returned 0 with empty stderr, and the harness verified the opposing callbacks. The McRave-local replay records UAlbertaBot leaving after defeat. No retry or seed sweep was performed.

## Source hypotheses

`BWAPILauncher/Source/Main.cpp` exits its frame loop as soon as the local `Game::gameOver()` observes that local player's victory or defeat. It then calls `GameImpl::update()`, which creates `MatchEnd(win)` from that client's local `PlayerVictory`, calls `onGameEnd()`, and unconditionally calls `bwgame.leaveGame()`.

For a started OpenBW game, `sync.h::send_leave_game()` emits reason byte 0, while `kill_client(client, false)` synthesizes reason byte 6 (`Dropped`). Both preserved failure replays contain byte 6, so their decisive terminal events did not come from delivery of the launcher's explicit reason-0 leave action. Reason 6 does not uniquely prove socket teardown: the same function is called for transport loss, an in-sync hash mismatch, a timeout, and a remote action processed after that player's controller ceased being occupied.

OpenBW's ordinary frame synchronization permits a client to lead another by the configured latency, three frames here. Teardown before a peer settles remains one plausible cause, but the preserved replay alone does not distinguish it from the other `kill_client(false)` paths.

Melee terminal triggers add a separate 31-frame ordering constraint. Trigger conditions read the pre-pass game state, while victory and defeat actions write a temporary `ets.victory_state` committed only after all triggers execute. Defeating and removing one player can therefore happen in one trigger pass; the survivor's victory condition observes that removal only when triggers run again 31 frames later. A losing client must remain a synchronization participant during that interval. This explains why a finished-acknowledgement-only repair would be incomplete, but it does not identify which kill path caused the preserved reciprocal result.

## Minimal repair direction

Before a semantic repair, an isolated diagnostic build must identify every `kill_client(false)` source, frame, peer slot, controller/victory state, and, for in-sync rejection, both hash values and the ring index. It must also log launcher terminal-loop entry and cleanup. One ordinary natural-completion fixture and one attempt at the original competitive scenario are sufficient; failures and non-reproduction remain evidence. No engine change was made in this investigation.
