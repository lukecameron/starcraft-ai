# Kestrel v7 first-home-fight diagnostic result

**Finding: the fixed loss is primarily a production-capacity and timing failure that creates sequential, ineffective local engagements. The Zealots are at the home fight, but each arrives alone against a much larger Zergling group. Available minerals are not the immediate constraint at first contact.**

The single registered run, `20260920T070255-f110c96947fd`, completed with opposing callbacks, both launchers returning zero, no state-hash mismatch, and two `screp`-parseable replays. Kestrel lost at local frame 6,141. The diagnostic module is instrumentation-only; its 2,879.7 durable frames/s is not comparable production-performance evidence.

## First engagement

- Kestrel accepted its first Gateway at frame 2,058, Assimilator at 2,484, and first Zealot train at 3,132.
- At frame 3,120 it had 186 minerals, zero gas, no current Zealot, and one completed Gateway beginning the first train twelve frames later.
- At frame 3,672 it accepted the second Gateway. At the frame-3,720 checkpoint it still had 166 minerals, 24 gas, one unfinished Zealot at `(3616,656)`, and five visible full-HP Zerglings between `(3455,868)` and `(3573,720)` near home.
- The first Zealot completed locally and received attack commands at replay frames 3,740 and 3,806. It died at bot frame 3,823 at `(3568,703)`, only 83 frames after its first attack order. The next checkpoint shows no Zealot and the local Zerglings still at full displayed HP.
- Kestrel accepted the second Zealot train at frame 3,972. By then the first Zealot was dead and Zerglings were killing Probes at the mineral line. At frame 4,560 the second Zealot remained unfinished while nine visible Zerglings occupied the home area and only one completed Probe remained.
- The second Zealot attacked locally at replay frames 4,580 and 4,670. At frame 4,680 it was at `(3540,618)`, `AttackUnit`, with 70 HP against eight nearby visible Zerglings. It died at bot frame 4,725 at the same local fight. By frame 4,800 only one Zergling showed substantial damage, at 5 HP; the rest shown were full HP.

This rules out positional isolation from the fight: both Zealots spawn and engage next to the home Gateway/mineral area. They are isolated in time. Only one combat unit exists for each engagement, first against five visible Zerglings and then against at least eight. The result therefore includes ineffective engagement, but the source of that engagement is insufficient concurrent production rather than a missing attack order.

## Economy and production state

The first local pressure is not explained by a lack of banked minerals. Kestrel has 166 minerals at frame 3,720 while its only Zealot is unfinished. The limiting state is one operational Gateway and no completed army. The second Gateway is requested only 48 frames before that checkpoint and cannot contribute to the first fight.

Meanwhile, v7 has already spent on an Assimilator, moves workers to gas by frame 3,480, continues Probe trains at 3,522 and 3,828, and has 24–40 gas during the first engagement. It realizes no Core or Dragoon. These observations agree with the earlier replay spending analysis but add the missing live-state evidence: extra minerals exist when the Zerglings arrive, while production capacity and build time prevent those minerals from becoming simultaneous defenders.

The first own Probe death at frame 2,848 occurs at `(583,2414)`, far from the home mineral line, confirming the scout loss. Mineral-line Probe deaths begin at frame 3,957 and then occur rapidly through frame 4,616. Thus the global contact/scout death is distinct from the home collapse.

## Narrowest supported next change

The smallest policy change supported by this trace is a known-Zerg build-order change that makes the second Gateway the next production structure after the first Gateway starts, before the Assimilator, while leaving Probe, Pylon, targeting, and combat behavior unchanged. Gas/Core can resume after two Gateways are current. This targets the observed constraint directly: the existing second Gateway request at frame 3,672 is too late to create a partner for the first Zealot.

This is narrower than another mineral reservation, worker pull, or micro change. It does not claim that two earlier Gateways will beat ZZZK; it identifies the next falsifiable mechanism: the second Gateway should begin early enough that two Zealots can overlap at the first home fight. Any candidate requires a new preregistration and should measure Gateway start/completion, simultaneous completed army at first home threat, and the first two engagement group sizes.

## Reproduction and artifacts

Apply `patches/kestrel-v7-fight-diagnostic.patch` to the accepted v7 source, then configure the copied source with the same `BWAPI_ROOT`, `BWAPI_BUILD`, `BWAPI_OFFICIAL_ROOT`, `/usr/bin/clang++`, Release, and Ninja arguments used by `scripts/build_kestrel.sh`. Build `KestrelOfficialHeaders` and `Kestrel` with at most four jobs. The combined source SHA-256 is `0f212fb66b01b810301c7e1e523161f45d9ac1ef6d85026c7db08f593d70c7e0`, patch SHA-256 is `3d284207a778004856ef0ee73920b1380259c21b903c455fdb2ca1365262ca3d`, and frozen diagnostic binary SHA-256 is `084160cc9afcee500a54a851f434388c462ab00d81aa60536f47ab217f68d1ef`.

The checkpointed JSONL is preserved in the run write state with SHA-256 `e3f7e880f12155ddc0006b745169a268e27994fb58bc7e793f2e4773ca8e41f4`. Replay SHA-256 values are `0a514976830a627f8d8f2ad8e34857afc17e0c0b0448b1a2de84b894ed5fbf29` and `dc062cb57842bfe443c98d8f700c13250f8ed722317266b919547c9ff89bbf0b`.
