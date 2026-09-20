# Progress dashboard

The dashboard is a static export of local run manifests, the dated BASIL snapshot in `config/opponents.json`, and the experiment ledger in `config/experiments.json`. It does not run a server, read raw logs in the browser, expose environment variables or local paths, or claim a local Elo before calibration.

Generate the local preview with:

```sh
python3 scripts/export_dashboard.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory dashboard/dist
```

The batch runner calls the configured publication hook after every terminal experiment outcome, including failed/interrupted outcomes. Publication failure is recorded separately and never changes match scoring. `--no-publish` skips the hook explicitly. The match runner's `--experiment-id` links future games; historical experiments use `evidence_run_ids`.

Cloudflare Pages publication is separate:

```sh
scripts/publish_dashboard.sh
```

It regenerates `public/` first and invokes `npx wrangler pages deploy public --project-name starcraft-ai --branch main`. A lock prevents overlapping publication. Local exports copy replays under `public/replays/`; after deployment the committed snapshot uses immutable deployment URLs, so clean Git builds retain working replay links without putting binary artifacts in Git.

The Pages project uses build command `scripts/build-pages.sh`, output directory `public`, repository root `/`, and production branch `main`. Source-only CI preserves the allowlisted snapshot and rating histories. The website checks for updated data every minute while visible.

`config/bot-identities.json` records ownership separately from origin. Our native adaptations are **Ours / Port**, strategic derivatives should be **Ours / Fork**, and project-written fixtures are **Ours / Original**. Unrecognized modules remain unverified. Original author and source links accompany bot names in matches, experiments and replay cards. BASIL observations are labeled **Upstream** and do not establish ratings for local builds.

Replay links use `https://dgant.github.io/openbw-replay-viewer/?url=<encoded-public-replay-url>` with a direct download alongside them. Representative playback was observed in the browser with map, units and advancing controls. The previous official host was inaccessible. No game assets or raw local environment/log data are published.
