# Kestrel v20 four-Zealot reserve plan — NOT RUN

- Registered: `2026-09-20T08:57:37Z`, before compilation or gameplay.
- Status: source-only checkpoint. No v20 module has been compiled and no game has been launched.
- Question: after v19's overlap improvement, does reserving 100 minerals once ten Probes exist until four Zealot trains are accepted preserve the hold while repairing Heartbreak's production miss?
- Evidence: v19 candidate reached two local completed Zealots before first loss on both maps, but Heartbreak accepted only three Zealot trains and no post-first-train structure. V20 control is the frozen v19 candidate. The candidate changes only Nexus Probe mineral reservation after ten Probes and before four accepted Zealot trains.

## Frozen source arms

- Control: byte-identical copy of the rejected v19 candidate source, SHA-256 `8994f313e679125395c360657b41c8559659db260f47a854c0c4ac98dfb87230`.
- Candidate: control plus [the v20 patch](../../../patches/kestrel-v20-four-zealot-reserve.patch), source SHA-256 `52fac23540e49f704f3899bb56361d56afc5c458aa596020aaa09dc69b675290`; patch SHA-256 `1e702ecc361f1f5011b0e600aa33e7396cf569c7c432fcdc81459219eeb61614`.
- Candidate change: after the existing first-Pylon, Gateway and first-Zealot reserves, Nexus Probe training leaves 100 minerals available while fewer than four Zealot trains have been accepted and at least ten Probes exist. Combat hold, construction, target selection, scouting and all other behavior remain unchanged.

## Fixed execution and decision rule

Compile both arms natively and against official BWAPI 4.4 headers, freeze binaries and sidecars, then run four fresh serial games against frozen ZZZK with empty learning state, LF3, the adopted engine, 120-second caps and no retries:

1. v20 control, Benzene, engine seed `6211`.
2. v20 candidate, Benzene, engine seed `6211`.
3. v20 candidate, Heartbreak Ridge, engine seed `6212`.
4. v20 control, Heartbreak Ridge, engine seed `6212`.

Primary gate: each candidate game records at least two simultaneously completed Zealots within 12 tiles of home before the first local Zealot loss, and is no worse than its matched control. A no-loss game measures through game end.

Each candidate must also record at least four accepted Zealot trains, at least ten Probes, two Gateways current, two completed Zealots, and at least one accepted structure request after the first accepted Zealot train. Report Probe and Zealot timing descriptively. Integrity requires reciprocal results, clean launcher exits, no hash mismatch, all eight replay copies parsed, LF3, no wrong-race production, no missing Zealot-loss position, zero gas-worker construction attempts, zero build `Unit_Busy`, command rejection below 5%, and at least 384 durable logical frames/s in every game.

`PASS` advances only the hold-plus-reserve policy to a separate held-out comparison against accepted v13. A missed gameplay or integrity gate is `REJECT`; invalid infrastructure is `INCONCLUSIVE`. Outcomes are descriptive and do not establish a tournament rating.

## Resume instructions

Do not edit canonical Kestrel. Build directly from `third_party/kestrel-opening-v20-control/` and `third_party/kestrel-opening-v20-candidate/` using their copied `CMakeLists.txt`, with no more than four compile jobs. Record compiler, official-header result, source and binary hashes in sidecars before creating the four-game schedule. Execute exactly the fixed order above, preserving every outcome and replay.
