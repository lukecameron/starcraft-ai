# Kestrel v33 two-Probe emergency Zerg bridge hill-climb

Drafted 2026-09-21 before candidate compilation or gameplay. This screen starts from the exact frozen Kestrel v32 policy and tests one bounded addition: a short emergency bridge using at most two eligible Probes while a real local Zerg combat threat exists before the stable combat reserve reaches two completed units. The v32 screen and its result remain the governing prior evidence; this preregistration assumes no gameplay improvement from v33.

## Candidate and hypothesis

The candidate is exact v32 (`kestrel-hillclimb-v11`) plus the two-Probe emergency bridge described below. The v32 stable three-unit Zerg reserve, its 96-frame per-unit home-move retry rule, surplus offense from army size four, production and economy policy, sixth-Pylon limit, build-commandability guards, and all other target-selection behavior remain unchanged. All non-Zerg behavior remains byte-for-byte policy-equivalent in intent and must not observe or activate the new bridge.

Against a publicly identified Zerg opponent, the bridge is eligible only when all of the following are true:

1. BWAPI currently exposes a visible and detected enemy Zerg unit that is non-worker and attack-capable.
2. That unit is inside the existing v32 local home-threat radius.
3. Fewer than two completed Kestrel combat units (Zealots or Dragoons) exist globally.

While the qualifying threat persists and the completed combat army remains below two, assign at most the two nearest eligible completed Probes to the existing public-BWAPI attack handling. Eligible selection excludes the builder, scout, current emergency defenders, and any Probe unavailable to accept a command. The economy and construction selectors exclude current emergency defenders for the entire assignment interval, so gathering or building cannot replace their defense orders. No more than two simultaneous emergency defenders may exist.

Release every surviving emergency defender when the qualifying threat clears or the completed combat army reaches two. Release returns the Probe to normal economy/build selection on the same or a later policy pass; it does not alter the v32 stable reserve. A defender death removes only that identity and cannot cause the cap to be exceeded. No hidden state, evaluator state, replay state, worker scout contact, or cross-frame enemy cache may trigger the bridge.

The hypothesis is that a two-Probe, threat-qualified bridge covers the interval before the first two combat units complete, while its narrow trigger and explicit economy exclusion avoid v9's six-Probe cost and preserve v32's stable reserve. A qualifying ZZZK-like threat must produce an assignment and an accepted attack order for the mechanism to count as exercised. A later gather or build assignment after release is evidence of recovery only when the replay and telemetry show an actual release opportunity.

Telemetry records the first bridge trigger and the count of threat-qualified trigger episodes; ordered assignment frames, batch sizes, and assigned Probe IDs; current and peak defenders; accepted emergency attack orders; ordered release frames, sizes, and army-two-versus-threat-clear flags; cause-specific release summaries; defender deaths; build/economy selection exclusions; and accepted post-release gather/build orders. Assignment batch sizes partition the ordered ID list, including a repeated ID if a later trigger reassigns the same Probe. It retains all v32 reserve telemetry: reserve recruit/death events, current and peak reserve size, first-three frame, home-move attempts/accepts/cooldowns/repeat interval, remote-target suppressions, local-defense attacks, first visible non-worker Zerg home threat, global/local combat and reserve counts at that frame, surplus release frame/army, and maximum offensive surplus. It also records command rejections, gas-worker build attempts, build `Unit_Busy` rejections, Pylon milestones, callback timing, CPU time, and peak RSS.

## Frozen five-game screen

Run exactly five fresh candidate attempts concurrently, with no retry, reseeding, or replacement:

| Game | Opponent | Map | Kestrel slot | Engine seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 9921 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 9922 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 9923 |
| 4 | McRave-9Pool-treatment | Circuit Breaker | P2 | 9924 |
| 5 | Stardust-repaired | Benzene | P1 | 9925 |

Use a 300-second wall cap per game and a 900-second cohort cap. Omit unsupported `MATCH_BOT_SEED` flags. Preserve every manifest, runner log, diagnostic, replay, hash, and parse result, including failures. Stop after two consecutive infrastructure-invalid attempts or the cohort cap; do not replace an invalid attempt. Fresh seeds make outcomes and frame differences descriptive, not matched causal evidence against v32.

## Integrity, regression, and mechanism gates

Integrity passes only if all five attempts have completed manifests, both child return codes zero, reciprocal Boolean terminal results, no timeout, launcher, state-hash, or wrong-race failure, exactly two archived replay copies per game, matching recorded and measured replay hashes, full `screp` parsing without parse-error commands, and expected races. For each replay copy require `replay_header_frames + 1 == owning_callback_frame`; the replay terminal frame is one below its owner's terminal callback frame. Normal nonempty OpenBW diagnostic stderr is not by itself a launcher failure; lifecycle records and child exit status control this gate.

Regression passes only with zero gas-worker build attempts, zero build `Unit_Busy` rejections, below 5% rejected commands in every attempt and across the cohort, no game above six Pylons, and ordered accepted/current/completed frames for every observed sixth Pylon. If a retained build-commandability guard blocks, a later construction must be accepted after its first block. Report unexercised retained mechanisms as untested rather than passing them by inference.

The emergency-bridge mechanism passes only if both Zerg attempts are valid, neither records more than two simultaneous emergency defenders, every assignment batch has size one or two while a threat-qualified trigger is active, and every release row has a cause flag showing either completed army two or threat clear. Assignment counters, ordered frames/sizes, and the Probe-ID list must agree; release counters, ordered frames/sizes/cause flags, and cause-specific summaries must agree. A qualifying ZZZK-like local non-worker attack-capable threat must record at least one emergency assignment and at least one accepted emergency attack order. Across the two Zerg lanes, report each assignment batch and release, whether defenders were actually excluded from economy/build selection when those selectors encountered them, and whether a surviving released defender later received an accepted gather or build order when such an opportunity occurred. An exclusion selector or post-release economy path that never has an opportunity is untested rather than failed. Emergency-defender counters and arrays must remain empty or zero, and frame/army/local milestones must retain their documented `-1` sentinel, in all three non-Zerg lanes.

All v32 stable-reserve gates remain mandatory: reserve remote attack orders remain zero; accepted home moves do not exceed attempts; when accepted repeat moves exist, the minimum accepted repeat interval is at least 96 frames; each Zerg attempt reaching three completed combat units records reserve peak three and a nonnegative first-three frame; and if a first non-worker Zerg home threat observes `g >= 2` completed combat units globally, reserve size and reserved-local count at that exact frame are each at least `min(3, g)`. Across the Zerg lanes, at least one must record a reserve remote-target suppression, at least one an accepted reserve local-defense attack, and at least one both a three-unit reserve and an accepted non-reserve remote attack with a nonnegative surplus-release frame and release army of at least four. New reserve telemetry remains zero or `-1` in non-Zerg lanes. An unobserved reserve, suppression, local defense, surplus release, or qualifying threat is untested and does not satisfy its gate.

Report durable logical frames per second, callback p99/max time, callback CPU time, and peak RSS for every game. No fixed 384-fps gate applies; the 300-second game cap, 900-second cohort cap, lifecycle, integrity, regression, and mechanism gates control validity. A shorter verified win is favorable; a faster loss is not improvement.

## Decision and scope

Adopt v33 for a separately registered held-out confirmation only if every integrity, regression, emergency-bridge, and retained v32 stable-reserve gate passes and the candidate records at least one verified win. A complete valid cohort missing any gameplay or mechanism gate, or with zero wins, is `REJECT`. An infrastructure-invalid attempt or cohort is `INCONCLUSIVE`, is preserved without retry, and does not count as a failed gameplay result. This exploratory screen cannot update Elo, replace canonical Kestrel v13, or establish tournament strength.

## Registered source identity

- Base policy experiment: `kestrel-hillclimb-v11` (exact Kestrel v32).
- Candidate source SHA-256: `d3c09bc2cd94eaccabefffe0fe76ed542f0e063a2a400a1428fc4b51d79d887a`.
- Combined source SHA-256: `562dc539d1171c5958ce80cbaebef4e53b336c908dc51e7385e75cb0d656cb66` over the registered source files in the build sidecar.
- Candidate binary SHA-256: `1d77b4483ea0fa21db1df9d8b45e15364986b793a2745b2c570f0db2fb55b632`.
- Candidate binary path: `artifacts/builds/1d77b4483ea0fa21db1df9d8b45e15364986b793a2745b2c570f0db2fb55b632/kestrel-opening-v33-candidate/Kestrel.dylib`.
- Reconstruction patch: `patches/kestrel-v32-to-v33-two-probe-emergency-zerg-bridge.patch`, SHA-256 `e1765155cff50b27e306b16f6b9c6d562ea9d1aae5746ed1d74854228b3d7276`.
- The final schedule records the evaluation plan SHA-256 before launch.

The candidate must compile natively against OpenBW and against the official BWAPI 4.4 headers before launch. The build sidecar must preserve exact v32 base identity, candidate source and patch bytes, compiler, binary, and runtime identities. The schedule freezes opponent provenance and Ours/Original/Port/Fork labels; upstream observations remain attached to upstream builds and are not transferred to this Kestrel candidate.

## Frozen runtime identities

- Engine library SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Engine launcher: `artifacts/builds/eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b/openbw-terminal-drain/BWAPILauncher`.
- Game data: `third_party/game-data/runtime`.
- The opponent identities and hashes are frozen in `schedule.json`; preserve their source provenance in the build sidecars.
