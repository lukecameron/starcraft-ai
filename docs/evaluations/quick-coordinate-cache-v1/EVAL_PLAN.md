# Coordinate repair and goal-cache quick check

Registered 2026-09-20T03:52:41.817318+00:00, before launch. The schedule is `config/quick-coordinate-cache-schedule.json`. It freezes candidate `98df26327cba498ac6ea1759d00b748f63870c655b34ecad6e24eb0e6851f1df`, the corrected f1a32e5a engine package, ten opponent/map/start scenarios, and explicit candidate bot seeds. The native and official-header builds passed. No learning state is reused.

Do not launch unless the separate live-state goal-cache shadow check first meets its zero-divergence and large-state coverage requirements. Run at concurrency two, with 120 seconds per game and the existing stop after two consecutive infrastructure failures. Keep every attempt; do not replace failures or choose new seeds after seeing results.

Engineering acceptance requires ten clean verified completions, no candidate crashes or timeouts, at least 384 durable frames/s for each match and for sum(frames)/sum(durable seconds). Report initialization and both processes' CPU/RSS alongside the slow tail. A failure identifies the next bottleneck; it does not justify relaxing the bar. The earlier batch used a different engine and no controlled bot seed, so this is a fresh engineering check, not a paired causal speed comparison.

Report wins, losses and failures by opponent, Wilson intervals, and uncalibrated relative Elo where finite. Ten games cannot prove a strength improvement or justify a calibrated BASIL rating. Passing may establish an engineering baseline; strategic promotion still needs a separate comparison and broader validation.
