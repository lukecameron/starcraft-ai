# Kestrel v5 command-state probe result

**Decision: reject v5's command-state policy. Infrastructure and lifecycle guards passed, but both registered command gates failed.**

Both fixed games completed with zero launcher exits, opposing terminal callbacks, no state-hash mismatch, two copied and `screp`-readable replays, and throughput above 384 logical frames per wall second. Kestrel produced a legal Protoss economy and army in both games and lost both. These two losses are descriptive rather than an Elo estimate.

| Opponent | Run | Frames | Durable frames/s | Unit maxima: probes / pylons / gateways / zealots / dragoons | Rejected commands | v4 reference |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| ZZZKBot | `20260920T062152-c192464ca3eb` | 6,513 | 3,037.0 | 15 / 2 / 2 / 3 / 0 | 54 / 124 (43.5%) | 14 / 77 (18.2%) |
| UAlbertaBot Terran | `20260920T062203-44a429a08fed` | 16,402 | 2,773.2 | 28 / 5 / 4 / 3 / 7 | 357 / 841 (42.4%) | 621 / 876 (70.9%) |

The UAlbertaBot rejection fraction improved relative to v4 but missed the registered below-25% gate. The ZZZK fraction regressed, so the required per-row improvement also failed. Full trajectories differed despite matched inputs: the UAlbertaBot game ran 16,402 frames versus v4's 11,969 and contained 349 accepted Kestrel `Attack1` orders versus 135. This makes raw accepted-order comparison noncausal, but it does not change the rejection-fraction failures.

Source and replay evidence indicate that retry timing alone is insufficient. The nearest visible target can change among nearby enemy units every policy cadence, bypassing the same-target cooldown and causing immediate replacement orders. A safer next change is target persistence: retain the bot-owned target while that unit remains legally visible, detected, attackable, and alive; choose a new nearest target only when the prior target becomes invalid. Rejected requests should use the same long cooldown because a 24-frame retry did not provide useful acceptance behavior.

Construction commands totaled five pylon-plus-gateway builds against ZZZK and 12 against UAlbertaBot, both below their v4 values of six and 16. Kestrel callback CPU/p99/max were 0.013587 seconds / 0.004709 ms / 1.79304 ms against ZZZK and 0.043153 seconds / 0.008583 ms / 2.2845 ms against UAlbertaBot.

Replay SHA-256 values are `c335041863d0aff0bd0a3afeb7ec89e35a47861897f3d6e1f172be7870dc4305` and `2b946845f396bed239f32273a407dc57dd48c63075719f03d05235f85e982e73` for ZZZK, and `80ed9baf60bd165f93b24b32cf38f3dbe8b71d7da7107a6a03e5d7403dc5b1d6` and `f2723a2d56efa3cdf725705783baace54ca47668b17634b4e4d8f7de592881a7` for UAlbertaBot. The manifests under the run IDs above are authoritative.
