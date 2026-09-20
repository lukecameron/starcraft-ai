# Kestrel early-spending analysis against ZZZK

This source and replay inspection compares accepted Kestrel production commands in the v7 matched Benzene loss and the two rejected v8 games. It asks whether early technology spending competes with a usable Zealot defense. Replay build commands show accepted requests; an accepted request can still be replaced before construction starts, so repeated build commands are not treated as proof that minerals were debited twice.

## Accepted command sequence

| Event | v7 Benzene 6103 | v8 Benzene 6103 | v8 Heartbreak 6105 |
| --- | ---: | ---: | ---: |
| Probe train requests before first Zealot | 10 through frame 3,296 | 6 through frame 1,796 | 5 through frame 1,304 |
| Pylon request(s) before first Zealot | 998, 1,238 | 968 | 1,202, 1,442 |
| Gateway request(s) before first Zealot | 1,988; 2,228; 3,068 | 1,916 | 2,024 |
| Assimilator request | 2,528 | 3,026 | 3,146 |
| First Zealot train | 3,416 | 3,020 | 3,140 |
| Second Gateway after first Zealot | already requested by 3,068 | 3,332 | 3,452 |
| Second Zealot train | 4,082 | 3,626 | 3,746 |
| Third Zealot train | 4,226 | 4,232 | 4,352 |
| Maximum completed/current Zealots reported | 3 | 2 | 2 |
| Maximum Dragoons reported | 0 | 0 | 0 |

V7 accepted an Assimilator command 888 frames before its first Zealot train. Its repeated early Gateway commands reflect travel/pending-construction behavior and the eventual two-Gateway opening; the v7 source cannot request gateways three and four until a completed Cybernetics Core exists. V8's first-unit reservation deferred both gas and the second Gateway until immediately after its first Zealot request. That advanced the first request but failed its lifecycle and survival gates, so it is not a policy to reuse.

All three games committed to gas before having two completed Zealots. None accepted a Cybernetics Core build command, none trained a Dragoon, and telemetry reports zero Dragoons. The gas investment therefore provided no combat unit before each loss. The current source starts an Assimilator whenever any Gateway exists, before considering a Core; it assigns up to three workers to gas while gas is below 250. Against this ZZZK trajectory, this consumes 100 minerals plus worker mining time without producing the intended tech unit.

ZZZK's replay command stream repeatedly directs its selected units to `(3808,464)` on Benzene and `(3808,1840)` on Heartbreak Ridge. Those points are adjacent to Kestrel's opening mineral targets around `(4000,496)` and `(4000,1904)`. Multiple selected Zerg unit tags receive the home-destination order by frame 2,545, before Kestrel's first Zealot request in every row. This is direct pressure toward the mineral line, although `screp` does not label a right-clicking selected unit's type and the command time is not an arrival timestamp.

## Supported policy hypothesis

A coherent next candidate can retain v7's probe, supply, scouting, targeting, and two-Gateway behavior while changing only its Zerg defense production phase:

- when the known opponent race is Zerg and fewer than four Zealots are current or queued, allow the first two Gateways and continue normal Probe and Pylon production;
- do not request an Assimilator or Cybernetics Core during that phase, and train Zealots from each completed Gateway whenever the existing legal checks permit;
- once four Zealots are current or queued, resume v7's normal gas, Core, and later Gateway/Dragoon path.

This differs from rejected v8: it does not pause Probe production or reserve everything until the first army unit. It removes technology spending that produced no realized combat benefit and gives a two-Gateway Zealot phase an explicit completion condition. It also differs from rejected v9 by making no worker-pull or micro change.

The evidence supports testing this mechanism, not assuming a win. A registered evaluation should require gas to occur only after the fourth accepted Zealot train, preserve v7 lifecycle/command-quality gates, measure first through fourth Zealot request and completion timing, and compare survival on the fixed matched row plus a held-out map. Wider strength promotion would still require a larger preregistered cohort.
