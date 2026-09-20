# Kestrel build-worker diagnostic v1 plan

- Registered: `2026-09-20T07:26:55+00:00`, before compilation or execution.
- Question: in the fixed Heartbreak Ridge v12 trajectory, are rejected build requests caused by `assignEconomy()` successfully issuing gather to the same Probe earlier in the same policy cadence, or by another public BWAPI worker/order state?
- Treatment: an isolated diagnostic-only build from frozen v12. Gameplay statements and ordering are unchanged. It records every build attempt before and immediately after `worker->build`: frame, building type, worker ID/position/order, target tile/distance, minerals, whether that worker accepted gather in the same cadence, acceptance, immediate BWAPI error, and post-call order. For each accepted build, it also records the builder's position/order/minerals on policy cadences until the building becomes current or the existing bounded retry interval expires.
- Scope: this test targets the 11 aggregate `Unit_Busy` build rejections observed on Heartbreak Ridge. The successful first-Pylon trace is descriptive. It cannot diagnose Benzene travel unless the same relevant behavior happens incidentally, and no Benzene game is registered.
- Execution: exactly one game, Kestrel diagnostic Protoss as player 1 versus frozen ZZZK Zerg on `sscai/(2)Heartbreak Ridge.scx`, scenario seed `6104`, adopted current engine, LF3, empty learning state, 120-second cap, no retry or replacement.
- Adequacy: the game must finish with zero launcher exits, reciprocal callbacks, no state-hash mismatch, a fully parsed archived replay, a complete build-attempt JSONL file, and at least one rejected build attempt. If no rejection reproduces, the result is `INCONCLUSIVE` for rejection cause.
- Interpretation: `CONFIRMED` same-cadence conflict requires a rejected attempt whose worker ID has a successful gather at that same bot frame and whose immediate error is `Unit_Busy`. Otherwise report the recorded order/state and the narrowest supported cause. No policy fix or adoption follows from this diagnostic alone.
- Stop: preserve the single attempt regardless of outcome. No retry, policy modification, strength claim, or performance comparison.

## Frozen source before build

- Combined source SHA-256: `b54d1cb5632ad86bc48b8c19102224f2f8be24052b697757fcd0aaaeb7b99665`
- Incremental v12 diagnostic patch SHA-256: `331b19cf48b5a53a3e74516abcdabfa4b273a4e1867bad12a5908e9f71a62e0c`
- Native module SHA-256: `a91296e864dc712e51440127280f07cf944ae28f23b28906f8949eb01933e78a`; native and official-header targets passed at `2026-09-20T07:27:47+00:00`.
