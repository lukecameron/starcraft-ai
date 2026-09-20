# Kestrel v14 first-fight diagnostic plan

- Registered: `2026-09-20T07:58:43.533312+00:00`, before compilation or execution.
- Question: after V14's earlier first Zealot, do the first two Zealots leave home for scout-visible distant targets, fight locally while outnumbered, or lose effectiveness through repeated target switching?
- Hypothesis: the Zealots remain near home and engage locally while outnumbered; accepted attack requests and public order/target histories will falsify that if they instead leave home or repeatedly switch targets.
- Policy: exact frozen corrected V14 candidate `d9e3445e…`, plus passive logging only. No command condition, target choice, production decision, or state used by gameplay changes.
- Trace: every 60 frames from 2,600 through 5,000 inclusive, record minerals/gas/supply; all Zealots and home-near Probes; every visible/detected enemy ground unit; public positions, HP, shields, completion, orders, order targets/positions, and ground-weapon cooldowns. Separately record the first completed Zealot and every accepted attack request with actor, target, and position. This bounds snapshots to at most 41 plus accepted-attack events.
- Frozen source SHA-256: `ff6bf76b2291b945739555f84e4b287262705aebfdcd8a43652662e3cdb174e1`; incremental diagnostic patch SHA-256: `791ab8db8e7e19a4d54422e81ff4dc8f310c35f21dbf67adc6c4be21127e3e31`.
- Execution: exactly one Kestrel diagnostic Protoss versus frozen ZZZK Zerg game on Benzene seed `6103`, player 1, adopted current engine, LF3, empty state, 120-second cap, no retry or replacement.
- Adequacy: reciprocal callbacks, zero launcher exits, no state-hash mismatch, both archived replays parse fully, trace covers the registered frame window through terminal state and contains first completion plus accepted attacks. Preserve every outcome.
- Interpretation: descriptive source diagnosis only. No playing-strength, policy-adoption, timing, or throughput decision follows from this instrumented game.
