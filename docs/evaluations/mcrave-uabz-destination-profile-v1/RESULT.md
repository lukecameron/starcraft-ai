# McRave versus UAlbertaBot Zerg late-game CPU profile result

**INCONCLUSIVE.** The only registered attempt failed before game initialization because the LOCAL socket was unavailable under the default sandbox execution. No gameplay, telemetry, live McRave PID, replay, or sample existed, so this result contains no outcome or performance evidence and was not retried.

Run `20260920T072243-b14c5982eca5` ended after 0.189 seconds. Both launcher processes returned 0 and both stdout logs contain `Error: connect: No such file or directory`; neither emitted result metadata. The durable manifest SHA-256 is `02025a99a4a2e8f51ff472d5865d59920122d80c158d09ac470afbb625532c4f` and the player-1 stdout SHA-256 is `1661e40660285eebbf8be536989727cb2f57b43c36a9aedc4dcbc7bf5b16d39d` (player 2 is byte-identical).

This operational failure revealed that the OpenBW LOCAL socket launch must use escalated local command execution. It does not select an outcome or change the registered metric or decision bar.
