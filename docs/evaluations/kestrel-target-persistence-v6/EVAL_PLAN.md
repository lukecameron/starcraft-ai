# Kestrel v6 target-persistence probe plan

**Canceled before execution at `2026-09-20T06:28:58Z`.** Before launch, review required command-category and BWAPI error attribution so reduced command counts could not mask inactivity. The frozen `1042321b…` module remains an unrun pre-telemetry artifact. The replacement v6b plan preserves this schedule and decision gate with the telemetry-complete source identity.

- Registered: `2026-09-20T06:23:25Z`, before any Kestrel v6 game was launched.
- Observed problem: v5's per-target cooldown still rejected 43.5% of commands against ZZZK and 42.4% against UAlbertaBot. The nearest-enemy selector could change among adjacent enemies every cadence, bypassing that cooldown.
- Change: each owned attacker retains its previously requested target while that public BWAPI unit remains alive, visible, detected, ground-based, and enemy. It selects a new nearest target immediately once any condition fails. Same-target retries use 96 frames regardless of prior acceptance. Opening, production, construction, scouting, and the legal observation boundary are unchanged.
- Candidate: frozen Kestrel v6 SHA-256 `1042321b2ac97269f6f548a29e636035c09199e406f7338b63062ff139c817ac`; combined source identity `6c1960336af3c94f21f361757f250ddc0a1af4852a33485a964755d8b697ca26`.
- Fixed serial schedule: one attempt each on the same matched inputs as v4/v5—ZZZK Zerg on Benzene seed `6103`, then UAlbertaBot Terran on Destination seed `6104`, with Kestrel Protoss as player 1, LF3, empty learning state, 120 seconds, no retries.
- Reproducibility limit: engine inputs and slots are controlled; opponent RNG and address/order effects are not. Compare robust rates and lifecycle outcomes, not exact global command streams.
- Infrastructure/lifecycle guard: zero launcher exits, opposing callbacks, no state-hash mismatch, two parsed replays, at least 384 durable frames/s, at least eight probes, one pylon, one gateway, a zealot or dragoon, scouting and combat, and no wrong-race production in every game.
- Primary gate: rejected-command fraction is below 20% in each game and lower than the corresponding v5 values of 43.5% and 42.4%. Replay accepted `Attack1` density must not increase relative to v5 after normalizing by frames from the first Kestrel combat-unit train through terminal frame.
- Responsiveness guard: inspect the first target transitions in each replay. A target death/disappearance must be followed by a command to another visible legal target within 96 frames when one exists; ambiguous replay visibility is reported rather than silently passed.
- Strength interpretation: outcomes are descriptive only. No Elo or promotion follows from two games.
- Decision: passing establishes v6 as the first command-clean Kestrel baseline and permits a separate opening-defense experiment. Failure returns to source diagnosis without a wider batch.
