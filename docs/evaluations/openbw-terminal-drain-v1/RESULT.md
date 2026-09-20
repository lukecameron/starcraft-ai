# Terminal synchronization repair — ADOPT

All six preregistered games completed cleanly, with opposing terminal results and zero child errors, timeouts or state-hash mismatches. Each of the four target games exercised the deferred-disconnect branch. Both ordinary controls passed. Adopt the frozen engine for new development experiments; keep historical engine regimes and all invalid games separate.

The observed failure was an early transport close after natural defeat. One process had marked the opponent defeated and handled its queued Select command while the opponent process was one frame behind. Closing that peer caused it to drop the still-active opponent before observing its own defeat. This differs from normal cleanup after an explicit LeaveGame command.

The repair discards ordinary commands from an already defeated player before executing or recording them, consumes remote queued commands while keeping its transport alive, and preserves explicit LeaveGame and existing error cleanup. It does not wait for both players to announce game over. Source review moved the discard before execution to avoid stale alliance/shared-vision commands mutating the survivor state.

## Registered results

| Scenario | Run | Result | Durable fps | Deferred branch |
|---|---|---|---:|---:|
| Stardust–McRave, Heartbreak P1 | `20260920T061624-ba5464b864bb` | Clean opposing results | 419.5 | 1 |
| Stardust–McRave, Heartbreak P2 | `20260920T061624-e26a9a2af1dc` | Clean opposing results | 420.4 | 1 |
| Stardust–McRave, Circuit P1 | `20260920T061703-19c325d3ac49` | Clean opposing results | 459.3 | 1 |
| Stardust–McRave, Circuit P2 | `20260920T061707-9c7d0c281740` | Clean opposing results | 504.9 | 1 |
| McRave–ZZZK control | `20260920T062025-0d5aa3b26f11` | Clean opposing results | 592.0 | 0 |
| Stardust–UAlberta Terran control | `20260920T062029-aa953d404b20` | Clean opposing results | 2048.8 | 0 |

All-attempt aggregate: 99,311 logical frames / 190.488 durable seconds = 521.3fps. These are the registered correctness scenarios, not representative late-game validation or a causal performance comparison. The previously failed games retain their original invalid classifications; these changed-engine attempts are separate evidence.

## Replay consistency and limits

All twelve replay hashes match the archive and all parse with screp1.13.4. Header frame+1 matches the owner's terminal callback. For every match, both replay command streams match exactly through the shorter replay's final frame after excluding terminal LeaveGame commands and parser-derived inefficiency annotations: 1,380,602 compared commands. This supplements the clean synchronization hashes and checks the source-review concern about mismatched post-defeat action handling. Terminal replay suffixes may differ because loser and survivor finish on different trigger frames.

This six-game check does not prove correctness for every action, multiplayer mode or engine path. The ordinary controls preserve the earlier LeaveGame behavior; no broad protocol redesign is claimed. All frozen module/library hashes and raw event/parser evidence remain in the local experiment directory. Future rating data use a new engine regime and do not absorb old invalid outcomes.

## Frozen build

- Engine library: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`
- Launcher: `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`
- Full OpenBW patch: `patches/openbw-terminal-drain.patch`, SHA256`787c642705c8181ac814ce68d44709e07a20116a5f02a0ad0950998e4ec5f2a8`
- Launcher patch: `patches/bwapi-terminal-diagnostics.patch`, unchanged
- Frozen package: `artifacts/builds/<engine-sha>/openbw-terminal-drain/`
- Pinned OpenBW`4b046d5f65302b10cb0a745f0fecd37ec85b20a8`, BWAPI`48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2`
- Raw review ledger: `artifacts/experiments/openbw-terminal-drain-v1/review.json`, SHA256`e0d96c6aeff361dc4ac7fcd7f98486827181d5600ef571aee73b52779e1a0165`

See `docs/engine-terminal-drain.md` for the direct rebuild route. Canonical older checkouts remain unchanged for historical reproduction.
