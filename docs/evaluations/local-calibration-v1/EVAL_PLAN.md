# Initial local league calibration

Registered before any trial on 20 September 2026. User requests more accurate Elo. Existing all-win batches against weak opponents do not establish an absolute rating.

## Hypothesis and decision

The five frozen build/race configurations in the three linked schedules complete a connected local comparison graph on two previously unused maps. Falsification: failures leave any expected node disconnected, an engine hash divergence appears, or provenance/replay validation fails. This is an evidence-collection and rating-estimator adoption check, not a candidate promotion.

Control/treatment: no code treatment; twelve scheduled head-to-head comparisons, six matchup/map/seed pairs with swapped protocol slots. Participants: McRave04521 Zerg, Stardust103997 Protoss, ZZZKce796 Zerg, UAlberta75ac Terran and Protoss. Engine27ea with its frozen launcher/libraries. New maps Heartbreak Ridge and Circuit Breaker come from the pinned Stardust map checkout; run manifests hash exact bytes. Neither map has been used in earlier project matches.

## Metrics and adoption threshold

Primary metric: number of verified scored games / 12, derived from terminal manifests, opposing Boolean winner callbacks, both process exits0, no insync_hash_mismatch log event, and both preserved replays hash-checked and screp-parsed. ADOPT initial local-estimator display only if 12/12 valid, all five exact build/race/config nodes form one connected graph, and rating implementation validation passes. REJECT the clean-graph hypothesis if any game is invalid; preserve a clearly partial display with all exclusions. Interrupted/unparseable collection is INCONCLUSIVE. No Elo threshold or bot promotion.

Rating formula: P(i wins j)=1/(1+10^((r_j-r_i)/400)). Independent zero-centered Gaussian priors on log strengths with400 Elo SD; MAP plus approximate95% Laplace intervals for contrasts. Display exact ZZZK reference at1000 as an arbitrary coordinate, including its posterior uncertainty in every other contrast. Display200/800 Elo prior sensitivity. Group exact engine/libs/game-data/platform/latency/learning/timeout regimes; no upstream ratings used. Deduplicate identical ordered scenario inputs; draws/failures are unscored and visible. Historical diagnostics and handpicked probes are excluded via an explicit experiment allowlist. Distinct module hashes or race/configuration never inherit predecessor evidence.

## Size, stopping, environment

Exactly12 games in three four-game schedules; no optional stopping on wins, retries, replacements or seed changes.180 seconds wall cap per game; no adjudicated timeout wins. Run each schedule with concurrency2; existing two-consecutive-infrastructure-failure rule applies. Normal build work may overlap, so performance is descriptive only and cannot satisfy an engineering promotion gate. Record per-game and aggregate durablefps regardless. Every game has isolated empty learning directories; McRave seeds explicit, other bots retain documented defaults. Non-deterministic bot execution and correlated map/slot pairs limit effective information. Two maps are not broad validation.

## Uncertainty and output

Report counts, graph, pairwise records, approximate conditional intervals, prior sensitivity, failures, maps, replay links and provenance. Scalar ratings assume transitive strength; matchup cycles and map/style effects may violate this. No accuracy guarantee, BASIL rating, tournament validation or precise absolute estimate. Additional comparisons must answer observed uncertainty and receive a new registration.
