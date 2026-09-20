# Kestrel v7 train-legality probe result

**Decision: pass. V7 is the first command-clean Kestrel baseline. End command-cleanup work and move to early Zerg defense.**

Both registered games passed infrastructure and lifecycle guards: zero launcher exits, opposing terminal callbacks, no state-hash mismatch, two copied and `screp`-readable replays, legal Protoss economy and combat, and throughput above 384 logical frames per wall second. Kestrel lost both games; these outcomes are descriptive and do not estimate Elo.

| Opponent | Run | Frames | Durable frames/s | Unit maxima: probes / pylons / gateways / zealots / dragoons | Total rejected | Train rejected | Attack rejected |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: |
| ZZZKBot | `20260920T063735-568f09f7d3a0` | 6,358 | 2,943.6 | 15 / 2 / 2 / 3 / 0 | 0 / 58 (0%) | 0 / 17 | 0 / 11 |
| UAlbertaBot Terran | `20260920T063750-d32c98d8cbcc` | 27,221 | 1,464.5 | 28 / 5 / 4 / 5 / 10 | 48 / 1,189 (4.0%) | 0 / 107 | 0 / 901 |

The primary gate passed. Neither game recorded a rejected train command, `Unit_Busy` or `Insufficient_Supply` train error, and both remained below 5% total rejection. Every train request appears as an accepted replay command: ZZZK has 14 probes and three zealots; UAlbertaBot has 38 probes, nine zealots, and 60 dragoons. This confirms that `canTrain(type)` removed avoidable requests without suppressing production.

The target-persistence guard also passed its observable requirement: both games had nonzero combat attempts and zero rejected attack commands. The replay command streams contain post-production combat. As in v6b, replay visibility alone cannot prove every target-transition deadline, so no broader responsiveness claim is made.

The 48 UAlbertaBot rejections were all gather commands reported as `Unit_Busy`; build, train, and attack commands had zero rejection. At 4.0% overall this remains within the registered gate and is lower priority than strategy. Kestrel callback CPU/p99/max were 0.014163 seconds / 0.003958 ms / 1.65029 ms against ZZZK and 0.071072 seconds / 0.013208 ms / 2.42433 ms against UAlbertaBot.

The accepted baseline still has two important strategy constraints. It lost to ZZZK after producing only three zealots, so early worker and building defense is the next strength hypothesis. Separately, `constructOpening` caps pylons at five, imposing a 49-supply ceiling including Nexus supply; the longer Terran game reached five pylons and continued for 27,221 frames. Future macro work must remove that ceiling, but it should not be mixed into the early-defense experiment.

Replay SHA-256 values are `0f663faa4203895f862470c352bec8c4f84810268d374d4fbaa5e7ea3e841f63` and `6069abdc68bd7a8a53748514a9e78d6b27585e6db908b5c0f23d9e42f2b99557` for ZZZK, and `b24a2dba895d35d01c8f5b7559e8fb8748981d15970854f988d2962a210f38dd` and `f450ed5acac4efa838a8a9101d0497cf158508aef50b1ad500b82926ebacf344` for UAlbertaBot. Match manifests under the run IDs above are authoritative.
