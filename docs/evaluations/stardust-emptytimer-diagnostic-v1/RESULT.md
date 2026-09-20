# Stardust empty-timer diagnostic result

## Outcome: confirmed

The single preregistered seed-5202 Stardust-versus-ZZZK attempt confirmed the suspected producer invariant violation. The diagnostic module explicitly aborted at frame 765 immediately after `MyWorkerImpl::update` excluded the sole timer hypothesis:

```json
{"event":"producer_exhausted","frame":765,"worker_id":45,"prior_size":1,"prior_was_single_zero":true,"order_id":87,"order_timer":0,"previous_order_id":87,"last_started_mining":681,"last_transitioned_to_mining":680}
```

The independent consumer guard was not reached. This proves that `possibleOrderProcessTimerValues` can become empty at the producer. `OrderProcessTimer::atStartOfNextFrame` and `atStartOfFrameAtDelta` can preserve that empty set, after which `PatchOccupiedForecast` dereferences `rbegin()` without checking it. The confirmed producer violation provides a concrete route to the original faulting `rbegin()` instruction. The original crash did not record its timer set, and this diagnostic aborted earlier without reaching the consumer, so it does not directly prove the historical invocation had an empty set.

The attempt is run `20260920T044040-2281fd96a9f4`. It failed as designed with Stardust return code -6 and no result; the peer observed transport loss. It was not retried.

## Frozen evidence

- Diagnostic module SHA-256: `c1afd9a5292621220e6484e115e5c016616a50deadafc88a92cc5f8df1469d9b`
- Full native-port plus diagnostic patch SHA-256: `4a2ec3536944642ff3c927d6213ad62123dece0c71b4b886c58202f625de8a17`
- Explicit-abort crash report SHA-256: `30a1484d131a544df7c0196853dc8ddd7bb582378089bed579e8facf0ac023f2`
- Frozen package: `artifacts/builds/c1afd9a5292621220e6484e115e5c016616a50deadafc88a92cc5f8df1469d9b/stardust-emptytimer-diagnostic/`
- Raw preregistration, patch, result, build logs, and crash report: `artifacts/experiments/stardust-emptytimer-diagnostic-v1/`

No semantic repair was included. The proposed repair is to restore the conservative complete nonzero pre-cycle domain `{1..8}` when exclusion of zero exhausts the model, allowing the existing cycle to produce `{0..7}`. A defensive consumer check should log and treat only an unexpectedly empty patch forecast as fully saturated before returning from the constructor, avoiding unsafe takeover without disabling the optimizer.
