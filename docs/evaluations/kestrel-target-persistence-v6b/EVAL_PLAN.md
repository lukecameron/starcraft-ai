# Kestrel v6b target-persistence probe plan

- Registered: `2026-09-20T06:28:58Z`, after the telemetry-complete build and before any game using it.
- Observed problem: v5's cooldown rejected 43.5% of commands against ZZZK and 42.4% against UAlbertaBot because nearest-target changes bypassed same-target suppression.
- Change: retain each owned attacker's previously requested target while that public unit is alive, visible, detected, ground-based, and enemy. Reselect immediately when invalid; retry an unchanged target after 96 frames. Command logic is otherwise v5. Telemetry now attributes attempts and rejections to build/train/gather/attack and records immediate public BWAPI error IDs; it does not alter decisions.
- Candidate: frozen Kestrel v6b SHA-256 `3b38bb8736d529a1d17dae27ce67e6fcb86dd881a7d9f1b36fb57764a3395f7a`; combined source identity `66660d92c4f0980077dfc8b728e04b052f7d8c12d969fe55f22327eed70b9569`.
- Fixed serial schedule: one attempt each on the v4/v5 comparison engine—ZZZK Zerg on Benzene seed `6103`, then UAlbertaBot Terran on Destination seed `6104`; Kestrel Protoss player 1, LF3, empty learning state, 120 seconds, no retries.
- Reproducibility limit: engine inputs and slots are controlled; opponent RNG and address/order effects are not. Compare rates and lifecycle, not exact streams.
- Infrastructure/lifecycle guard: zero launcher exits, opposing callbacks, no state-hash mismatch, two parsed replays, at least 384 frames/s, at least eight probes, one pylon, one gateway, a zealot or dragoon, scouting and combat, and no wrong-race production in every game.
- Primary gate: rejected-command fraction is below 20% in each game and below corresponding v5 values (43.5%, 42.4%). Accepted `Attack1` density must not increase after normalizing from first Kestrel combat-unit train to terminal frame. Report command categories and error counts; zero attack attempts or absent post-production combat fails lifecycle rather than passing by inactivity.
- Responsiveness guard: inspect early target transitions. After target death/disappearance, another visible legal target must be commanded within 96 frames when replay evidence supports that observation; ambiguity is explicit.
- Strength interpretation: outcomes are descriptive; no Elo or promotion follows from two games.
- Decision: all gates passing establishes the first command-clean baseline and permits a separate opening-defense experiment. Failure returns to diagnosis without a wider batch.
