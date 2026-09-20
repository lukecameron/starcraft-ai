# Preserve terminal synchronization before disconnecting defeated peers

Registered 20 September 2026 before candidate compilation or trials.

## Reproduction and hypothesis

The real calibration path produced three conflicting-winner games: runs 20260920T055717-7842246af878, 20260920T055717-5eafb5ffe760 and20260920T060312-129fdb979771. In every case one client processes an ordinary Select command (action 9) from a peer whose controller is already 10 and victory_state 2; it immediately closes that peer. The other client is one engine frame behind, sees transport EOF while its opponent is still active, drops that opponent and announces victory instead of reaching its own defeat. Both processes exit 0 and no hash mismatch is logged.

Source: `sync.h::process_messages` closes a non-occupied peer after any action, although `actions.h` action 9 only selects units. `bwgame.h` marks a defeated occupied player as user_left before the survivor's victory trigger 31 frames later. Prior clean controls closed after action 87 (LeaveGame), after the loser had already observed defeat.

Hypothesis: keeping the connection for ordinary pending commands after natural defeat lets the lagging peer reach the same defeat state. Preserve explicit LeaveGame, timeout, hash-mismatch and transport-error cleanup. This is not an end-of-game acknowledgement barrier: the defeated bot may terminate before the survivor reaches victory.

## Treatment and controls

Create an isolated engine from the full frozen 27ea diagnostic source patch plus one change: when a remote client is already non-occupied with committed defeat state2 after an ordinary game action other than 87, retain it and continue draining its queued actions. Log the first such deferral. Preserve the local client's existing terminal action clearing and explicit 87 cleanup. Do not change gameplay, command latency, outcome callbacks or scoring.

Frozen bot inputs: McRave04521 Zerg, Stardust103997 Protoss, ZZZKce796 Zerg and UAlberta75ac Terran. Six games: Stardust vs McRave on Heartbreak Ridge seed6101 both slots, same pair on Circuit Breaker seed6302 both slots, McRave vs ZZZK on Benzene seed1001, Stardust vs UAlberta Terran on Destination seed5301. Explicit McRave RNG seed equals scenario seed. Existing failed calibration replays are historical reproductions, not extra candidate observations or retries of that cohort. New experiment identity and changed engine are mandatory.

## Metrics, bar and stopping

Primary metric: clean opposing terminal results / 6, from both process exits 0, opposing Boolean ended callbacks, no hash mismatch, and both preserved replays parsing with owner frames. ADOPT as a correctness repair only if 6/6 pass, at least one target game logs the deferred disconnect branch, and both ordinary control matchups pass. Reject if any inconsistent outcome, crash or deadlock/timeout occurs. If all games pass but no target exercises the branch, INCONCLUSIVE. No strength promotion or BASIL claim.

Exactly six attempts, no replacement seeds or adaptive retries.180-second wall cap, concurrency2. Existing batch stop after two consecutive infrastructure failures applies. Observe full durable throughput and resource use but no performance-causality claim; other games/profiling must not overlap. Compile and freeze all engine binaries/patches/sidecars before launch. If the repair passes, future ratings start a distinct engine regime; old invalid games stay unscored.

## Source-review amendment before compilation or trials

Luna identified that executing all queued post-defeat actions could apply stale shared-vision/alliance mutations. The final candidate discards ordinary commands from an already defeated player **before** execution or replay recording. This check applies identically to local and remote player state; the local queue is cleared as before, while remote actions are consumed without closing the connection. Explicit LeaveGame and synchronization/control messages retain existing handling. The numerical acceptance bar and six scenarios are unchanged.
