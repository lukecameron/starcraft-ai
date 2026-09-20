# McRave ground-path regeneration diagnosis

Registered 2026-09-20T05:57:52Z, before compilation or execution.

## Question and frozen trial

Which existing gates cause Combat march, Combat retreat, and Support JPS paths to regenerate in the late-game Destination scenario, and is there a sufficiently frequent case for a semantics-preserving shadow candidate?

Build an isolated diagnostic from frozen production candidate `04521befa41bb3873783b215493abf3a071414d2a5315cdea68fc7a67f4415ec`. Run it exactly once as player 1 Zerg against frozen UAlbertaBot Terran on Destination, with engine seed 3001, McRave bot seed 3001, frozen engine `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb`, and a 120-second wall cap. Do not retry.

The production path remains authoritative. Instrumentation only observes each existing decision and resulting `BWEB::Path`: requested source and target tiles, prior source and target, exact reuse, source-only/target-only/both endpoint changes, destination validity, policy eligibility, BWEM area permission, empty/reachable prior path, endpoint validity/walkability/occupancy, generated reachability, tile count, and unique unit count. It writes an atomic aggregate every 240 frames and on end. It does not issue commands or select paths.

## Decision rule

The diagnostic is adequate if its last durable summary is internally consistent, covers at least 1,000 attempts and 100 generated paths across the profiled families, and records both Combat march and retreat. Lack of Support generation is reported as missing Support coverage rather than inferred behavior. A completed match must also have opposing terminal metadata, zero launcher crashes, and no `insync_hash_mismatch`.

A next shadow candidate is justified only for a directly observed reason representing at least 20% and at least 100 generated paths. It must preserve the current endpoint, path ordering, walkability policy, and dynamic obstruction behavior. Source-tile-only changes can justify investigating safe prefix trimming and validating the remaining path again; they do not justify blind cross-frame reuse. Target changes, unreachable paths, area rejection, occupied endpoints, and invalid endpoints remain separate and cannot be combined into a reuse claim.

Missing coverage, corrupt accounting, instrumentation effects, timeout without adequate durable coverage, or terminal-integrity failure is INCONCLUSIVE. Any observed opportunity only selects a same-input shadow comparison; it does not establish correctness, speed, strength, or adoption.
