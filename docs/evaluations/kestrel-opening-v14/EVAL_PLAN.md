# Kestrel v14 one-time opening priority plan

- Registered: `2026-09-20T07:52:47.607421+00:00`, before compilation or any v14 game.
- Question: against a publicly known Zerg opponent, does a one-time mineral priority for the first Gateway and first Zealot materially advance both accepted orders without breaking V13's lifecycle and command quality?
- Evidence: fresh V13 Benzene 6103 requested its first Pylon at replay frame 998, a second Pylon at 1,238, first Gateway at 1,994, Assimilator at 2,396, and first Zealot at 3,122. Earlier V8 moved first Zealot training earlier but broadly suppressed Probe/technology spending and failed lifecycle; V10 delayed technology but missed its production/timing gates; V11 moved only the second Gateway and completed too late; V12's first-Pylon reservation failed one map's timing bar. V14 therefore tests the earlier Gateway-to-first-Zealot segment only.

## Arms

- Control: frozen V13 policy plus passive first-Pylon, first-Gateway, and first-Zealot accepted/current/completed telemetry. Source SHA-256 `359a58670d8174e361e8b80a16f2338444b6cc9478c656f0f1d7842543a8707d`; V13-to-control telemetry patch SHA-256 `615ffcf08cac4d79d280ac2d99fbdc288d7a40aee68856ef7060bf55831ed633`.
- Candidate: the same telemetry and V13 gas-worker guard. Only against known Zerg, after the first accepted Pylon it leaves 150 minerals available for the first Gateway when deciding whether to train a Probe. Once the first Pylon is complete, it requests that Gateway before later supply/technology spending. After the Gateway request and until the first accepted Zealot train, it leaves 100 minerals available when deciding whether to train a Probe and defers the second Gateway and Assimilator. An accepted Zealot sets a persistent `firstZealotQueued` flag, so the priority cannot reactivate after deaths. Existing Pylon thresholds/cap, micro, scouting, combat, expansion behavior, and post-first-Zealot strategy are unchanged. Candidate source SHA-256 `67758a7787a2df97598b49fcc28a84d0ac2c5336fb8ab052ea5bd2ddbc5bd046`; incremental policy patch SHA-256 `b5fd51e6e50ab8eda83b12bcd550fc58e61a875ba09790598d01a99795f47a5c`.

## Fixed execution

Four serial games against frozen ZZZK, with fresh empty state, current adopted engine, LF3, 120-second cap, no retries or replacements:

1. Control, Benzene seed 6103.
2. Candidate, Benzene seed 6103.
3. Candidate, Heartbreak Ridge seed 6104.
4. Control, Heartbreak Ridge seed 6104.

This alternates arm order across the two matched map/seed pairs. Global trajectories may still diverge despite fixed scenario seeds, so the two pairs are a bounded mechanism screen rather than a strength estimate.

## Fixed gates

- Opening mechanism: in **each** matched pair, candidate first-Gateway accepted frame and first-Zealot train frame must each be at least 120 logical frames earlier than its fresh control. All four timings must exist. This is an advance-only threshold; later terminal survival cannot compensate for a miss.
- Production: every game must complete a Pylon, Gateway, and Zealot, continue Probe production to at least eight Probes, issue accepted scouting/post-production combat commands, and show no wrong-race production. Candidate must resume ordinary Probe production and later construction after `firstZealotQueued`.
- Correctness/lifecycle: reciprocal callbacks, zero launcher exits, no state-hash mismatch, eight fully parsed replay copies, LF3, fewer than 5% rejected commands, zero gas-worker build attempts, zero build `Unit_Busy`, and at least 384 durable logical frames/s in every game.
- Decision: `PASS` only if every mechanism, production, and lifecycle gate passes. Otherwise `REJECT`; infrastructure-invalid evidence is `INCONCLUSIVE`. Passing advances the policy only to broader confirmation and does not establish strength or replace canonical V13.

## Build identities recorded before gameplay

- Control module: `23a6ca0190d6cb088c64be990cc8fa6128abf63de1f99820213a5cd29c77d5dc`; native and official-header compile passed.
- Candidate module: `415832a2a633dc68f9bf625302ddcf3e6d31d66f1bcbbbf88b2854b1049eaa56`; native and official-header compile passed.

- Prelaunch review amendment `2026-09-20T07:54:40.392826000Z`: accepted construction does not spend minerals until construction begins, so the 150-mineral reserve and special Gateway retry now remain active until `firstGatewayCurrentFrame >= 0`; only then does the 100-mineral first-Zealot reserve apply. The unrun module `415832a2…` is preserved as superseded. Thresholds and gates are unchanged.
- Corrected candidate module recorded before gameplay: `d9e3445e4740cd1c7dd48d0d99a27760bb95d365e573684222d649b3ee470f25`; native and official-header compile passed.
