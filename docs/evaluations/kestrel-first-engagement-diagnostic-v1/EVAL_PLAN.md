# Kestrel v30 first-engagement diagnostic plan

Registered 2026-09-20 after the v29 five-lane screen produced five verified losses. v29 separately verified the build-commandability recovery and sixth-Pylon mechanisms, but its outcomes span early home-pressure losses and later mixed-army losses. This diagnostic asks which observed failure mode should determine the next single policy change. It is not a strength comparison, adoption screen or Elo input.

The candidate starts from the exact v29 policy: source SHA-256 `0dbb8404b62197e52020655d098c888abdb25aaeca79b60358d44b4a806b4fe3`, combined source SHA-256 `956c5882e2948d54fce8d5dbf4e8fa963121e2998a09a6179a136d3e6b4f924d`, and binary SHA-256 `c7196ea991f5755b6e34c9c9ebff87faf3884d221de9492a7952ce20cc57d56c`. v30 may add observations only. It must not change build order, economy, production, targeting, movement, cadence, thresholds or any other gameplay decision.

Append a durable JSONL diagnostic at start, every 120 frames, at first detected home threat, first local engagement, accepted build/train/attack commands, each newly completed Zealot or Dragoon, own Probe/Zealot/Dragoon deaths, and game end. Each snapshot uses public BWAPI observations only and records:

- frame, trigger, minerals, gas and supply;
- current and completed Probe, Gateway, Zealot and Dragoon counts;
- each own Zealot and Dragoon's identity, completion, public position, hit points, shields, order, order target and distance from the starting-base center;
- each Nexus and Gateway's completion, training state, remaining train time and public training queue;
- visible, detected, ground enemy units within 16 tiles of home, including type, position, hit points, shields, attack capability and distance from home.

The home center is exactly the v29 calculation: the starting tile converted to pixels with offsets `(64, 48)`. A local unit is a completed Zealot or Dragoon less than 12 tiles from that point. The first local engagement is the first frame where a completed own combat unit and a visible, detected, non-flying enemy attacker are at most six tiles apart while both are within 12 tiles of home. The event records both identities, positions and local/global army counts. Visible enemy superiority means that visible enemy attackers within the 12-tile classification radius outnumber local completed combat units at the same event or snapshot; the 16-tile snapshot radius remains context only.

Accepted command events identify the actor, produced unit or building and public position. Accepted attack events also identify the target, both positions, distance and whether the target changed. Completion events provide cumulative first, second and third unique combat-unit completion frames. Death events use the last public position observed by the bot when available and record distance from home and local status. Scalar terminal telemetry adds `first_home_combat_loss_frame` across Zealots and Dragoons and the maximum simultaneous completed combat-unit count. The file is opened in append mode and flushed per event so interruption retains evidence. Remove any old diagnostic file on start. Instrumented source and binary identities will be recorded after compilation as a schedule amendment; the hashes above identify the v29 base at registration.

Run exactly five attempts concurrently against the same frozen opponent/map/slot matrix with fresh engine seeds. Do not retry or replace attempts:

| Game | Opponent | Map | Kestrel slot | Engine seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 9891 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 9892 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 9893 |
| 4 | McRave-9Pool-treatment | Circuit Breaker | P2 | 9894 |
| 5 | Stardust-repaired | Benzene | P1 | 9895 |

Use a 300-second wall cap for each game and a 900-second cohort cap. Omit unsupported `MATCH_BOT_SEED` flags. Preserve every manifest, runner log, result file, replay, hash, diagnostic JSONL and full replay parse, including invalid attempts.

The diagnostic is valid only if all five attempts have completed manifests, both child return codes zero, verified reciprocal terminal results, no timeout, launcher, state-hash or wrong-race failure, exactly two replay copies with recorded hashes matching bytes, expected races, full parsing with no replay parse errors, and replay terminal frame equal to the corresponding callback frame plus one. Each retained JSONL must exist, parse line by line, end with a final `ended` event, have monotonically nondecreasing frames and no event after the terminal frame. Event frames and counts must agree with scalar telemetry; completion milestones must be ordered; local counts cannot exceed global counts; accepted attack-event count cannot exceed accepted attack commands; and counts/distances must be nonnegative or explicitly `-1`. Stop after two consecutive infrastructure-invalid attempts or the cohort cap. Do not replace an invalid attempt.

Record throughput, command rejection and the retained v29 construction fields, but do not use the 384-fps hill-climb gate to invalidate this instrumentation-only diagnostic. Detailed JSONL logging can change throughput, and v29's McRave lane was already below that floor.

Classify each valid lane from public evidence without forcing a single label:

- **production timing:** the cumulative second unique completed Zealot/Dragoon milestone occurs after first home threat or never occurs, with accepted production and remaining-train-time evidence explaining when reinforcements can arrive;
- **positional dispersion:** the second combat unit was already complete by first home threat, but fewer than two completed combat units were within 12 tiles of home, supported by positions and orders;
- **local combat conversion:** at least two completed units were local, a direct public first-local-engagement event occurred, and a combat loss followed before a win;
- **late conversion:** no own Zealot or Dragoon loss occurs within 2,400 frames after first home threat, the maximum simultaneous completed combat-unit count reaches at least ten, and the game still ends as a loss.

Apply these labels in the order shown when one primary label is needed, and report every supported secondary label. Report resource state, production queues, local/total army, visible threat composition and replay command evidence around first threat, first engagement and first local combat loss for every lane. Fresh seeds are descriptive observations and cannot be compared causally with v29's seeds. These heuristics do not establish causes or hidden state. The result may recommend one bounded v31 gameplay change only if the same concrete failure is supported in at least two valid lanes. Otherwise stop with separate diagnoses and no policy candidate. Regardless of outcomes, v30 cannot update Elo, replace canonical Kestrel v13 or advance a prior candidate.
