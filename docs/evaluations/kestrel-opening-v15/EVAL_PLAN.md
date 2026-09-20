# Kestrel v15 two-Gateway overlap plan

- Registered: `2026-09-20T08:02:28.855495+00:00`, before compilation or gameplay.
- Question: with V14's earlier first Gateway, can a persistent two-Gateway, gas-delayed opening produce at least two simultaneously completed local Zealots before the first local Zealot dies?
- Evidence: V14's diagnostic showed Zealot 144 fighting at least six local Zerglings alone and dying before Zealot 155 completed; the second then fought at least seven alone. V11's second Gateway completed after home pressure because both Gateways started late. V14 materially advances the first Gateway, creating a new opportunity to overlap production.

## Arms

- Fresh control: evaluated V14 policy plus passive shared overlap telemetry. It records accepted Zealot trains, second-Gateway current/completed frames, first visible detected ground threat within 12 tiles of home, first own Zealot destroyed within that radius after threat, and the maximum simultaneously completed Zealots within the same radius before that loss. Source SHA-256 `9370cc157c0e5ada5663ae476275b87ce07f9f6ba3bdfb8c66d24e7e4ff8f30f`; telemetry patch SHA-256 `3d13b06b73461ed3cddc9c6289ec5f640d4bfa6a9f35d2221bd8c00a8b4744cd`.
- Candidate: identical telemetry and micro. Against known Zerg, once the first Gateway is observed current, Probe training leaves 150 minerals for the second Gateway until that Gateway is observed current. Normal Zealot training remains ahead of construction in each callback. Existing supply-Pylon handling remains ahead of the special second-Gateway request. Assimilator and Core are deferred until a persistent counter reaches four accepted Zealot trains. The milestones are once-only accepted/current facts and cannot reactivate after army deaths. Source SHA-256 `15c4963a13ff6c89b55d021e8b76b44761ba2c3f40275457ceba1788c6b64284`; policy patch SHA-256 `adfcdb7440028b39a38e4b7b8154b59c1411db895063e7841970f12ec955cafa`.
- Unchanged: V13 gas-worker guard, V14 first-Gateway priority, Pylon thresholds/cap, scouting, target selection, combat micro, expansion behavior, and non-Zerg behavior.

## Execution and fixed gates

Four fresh serial games versus frozen ZZZK: control then candidate on Benzene seed `6201`, candidate then control on Heartbreak Ridge seed `6202`. Use the current adopted engine, LF3, empty state, 120-second cap, no retries or replacements.

- Primary: candidate `max_local_completed_zealots_before_loss >= 2` in both games and no lower than its matched fresh control. If no local Zealot loss occurs, measure through game end.
- Mechanism/production: each candidate observes two Gateways current, records at least four accepted Zealot trains, completes at least two Zealots, resumes ordinary Probe training to at least ten Probes, records at least one accepted structure request after `firstZealotTrainFrame`. Report gas resumption separately; lack of time after the fourth train is not silently treated as proof.
- Integrity: reciprocal callbacks, zero launcher exits, no state-hash mismatch, eight fully parsed archived replay copies, LF3, no wrong-race production, `zealot_loss_position_missing == 0`, zero gas-worker build attempts, zero build `Unit_Busy`, fewer than 5% rejected commands, and at least 384 durable logical frames/s in all games.
- Decision: `PASS` advances V15 to broader strength validation only. A missed gameplay/production/integrity gate is `REJECT`; invalid infrastructure is `INCONCLUSIVE`. Outcomes and terminal frames are descriptive.

## Frozen build identities before gameplay

- Control module: `348dd9de12e71b49b1cdca10950746221393b535cce642e296d409246c446c74`; native and official-header compile passed.
- Candidate module: `440316ebaf2359d196b4d636e0c518852a4fe7b0cf4f333a4ec372708940aed0`; native and official-header compile passed.

- Prelaunch review amendment `2026-09-20T08:04:56.402661+00:00`: after the second Gateway becomes current, preserve V14's 100-mineral first-Zealot reserve until the persistent accepted-first-Zealot flag is set. Both arms now count accepted structure requests after the first Zealot train. The loss metric uses last-observed valid own-Zealot positions; any missing position invalidates the game. The unrun modules `348dd9de…` and `440316eb…` remain preserved. Thresholds otherwise remain unchanged.

- Corrected control module before gameplay: `67413847356807ce6c9a8c69dd02d888ead1284a71ed94237c98c81d1c819dd5`.
- Corrected candidate module before gameplay: `42f3ea9c3218a2873803962d5437d4f5e313e4883eef6f89ca4a63d6a30713a2`.
