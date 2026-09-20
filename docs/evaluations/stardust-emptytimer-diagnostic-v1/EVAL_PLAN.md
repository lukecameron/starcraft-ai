# Stardust empty-timer diagnostic plan

Registered `2026-09-20T04:34:26.147264+00:00`, before compilation or launch.

The question was whether the frozen seed-5202 Stardust-versus-ZZZK crash scenario exhausts `possibleOrderProcessTimerValues` before `PatchOccupiedForecast` dereferences `rbegin()`. The isolated build made no recovery or policy change. It logged the producer's prior set size and public worker/order state and aborted explicitly if excluding zero emptied the set; an independent consumer guard logged and aborted before `rbegin()` if it received an empty set.

Run exactly one Stardust Protoss player-1 versus ZZZKBot Zerg game on Benzene with engine seed 5202 and a 120-second cap. Preserve every outcome and do not retry or sweep seeds. The hypothesis is confirmed only if stderr records `producer_exhausted` or `consumer_empty` before termination. Otherwise the suspected cause remains unconfirmed.

