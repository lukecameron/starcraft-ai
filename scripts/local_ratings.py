"""Exact-build local Bradley–Terry estimates; no upstream rating inheritance.

Small dense Newton solve and Laplace covariance use only the Python standard
library so a clean Pages build does not need a numerical runtime. This is an
explicitly approximate, prior-dependent model, not a tournament rating.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path

ELO_PER_LOGIT = 400 / math.log(10)
Z95 = 1.959963984540054


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def cholesky(matrix):
    n = len(matrix)
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            value = matrix[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            lower[i][j] = math.sqrt(value) if i == j else value / lower[j][j]
    return lower


def solve(lower, rhs):
    n = len(rhs)
    y = [0.0] * n
    x = [0.0] * n
    for i in range(n):
        y[i] = (rhs[i] - sum(lower[i][j] * y[j] for j in range(i))) / lower[i][i]
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(lower[j][i] * x[j] for j in range(i + 1, n))) / lower[i][i]
    return x


def fit_bt(node_ids, games, prior_sd_elo=400):
    """Return log-strength MAP and full covariance in the supplied node order.

    Each game is a (winner ID, loser ID) tuple. Independent N(0, sd²)
    log-strength priors make the Hessian positive definite even after sweeps.
    """
    if prior_sd_elo <= 0 or not math.isfinite(prior_sd_elo):
        raise ValueError("prior SD must be positive and finite")
    n = len(node_ids)
    if not n:
        return [], []
    indices = {value: index for index, value in enumerate(node_ids)}
    if len(indices) != n:
        raise ValueError("node IDs must be unique")
    pairs = Counter((indices[winner], indices[loser]) for winner, loser in games)
    if any(i == j for i, j in pairs):
        raise ValueError("self-comparisons are not rating evidence")
    precision = (ELO_PER_LOGIT / prior_sd_elo) ** 2

    def objective(theta, derivatives=False):
        loss = .5 * precision * sum(x * x for x in theta)
        gradient = [precision * x for x in theta]
        hessian = [[precision if i == j else 0.0 for j in range(n)] for i in range(n)]
        for (i, j), count in pairs.items():
            difference = theta[i] - theta[j]
            loss += count * (max(0.0, -difference) + math.log1p(math.exp(-abs(difference))))
            if derivatives:
                p = 1 / (1 + math.exp(-difference)) if difference >= 0 else math.exp(difference) / (1 + math.exp(difference))
                g = count * (p - 1)
                v = count * p * (1 - p)
                gradient[i] += g
                gradient[j] -= g
                hessian[i][i] += v
                hessian[j][j] += v
                hessian[i][j] -= v
                hessian[j][i] -= v
        return loss, gradient, hessian

    theta = [0.0] * n
    for _ in range(80):
        loss, gradient, hessian = objective(theta, True)
        if max(abs(x) for x in gradient) < 1e-9:
            break
        step = solve(cholesky(hessian), gradient)
        scale = 1.0
        directional = sum(g * s for g, s in zip(gradient, step))
        while scale >= 2 ** -30:
            candidate = [t - scale * s for t, s in zip(theta, step)]
            if objective(candidate)[0] <= loss - 1e-4 * scale * directional:
                theta = candidate
                break
            scale /= 2
        else:
            raise ArithmeticError("rating fit line search did not converge")
    else:
        raise ArithmeticError("rating fit did not converge")
    lower = cholesky(objective(theta, True)[2])
    columns = [solve(lower, [float(i == j) for i in range(n)]) for j in range(n)]
    covariance = [list(row) for row in zip(*columns)]
    return theta, covariance


def contrast(theta, covariance, index, reference):
    value = 1000 + ELO_PER_LOGIT * (theta[index] - theta[reference])
    variance = max(0.0, covariance[index][index] + covariance[reference][reference] - 2 * covariance[index][reference])
    radius = Z95 * ELO_PER_LOGIT * math.sqrt(variance)
    return {"rating": round(value, 1), "low": round(value - radius, 1), "high": round(value + radius, 1)}


def connected_components(games):
    adjacent = defaultdict(set)
    for game in games:
        a, b = game["nodes"]
        adjacent[a].add(b)
        adjacent[b].add(a)
    remaining = set(adjacent)
    result = []
    while remaining:
        found, queue = set(), [min(remaining)]
        while queue:
            node = queue.pop()
            if node in found:
                continue
            found.add(node)
            queue.extend(adjacent[node] - found)
        result.append(sorted(found))
        remaining -= found
    return result


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def extract_game(manifest, public, manifest_path):
    """Fail closed on incomplete identity or invalid results; return public-safe input."""
    if manifest.get("status") != "completed" or not manifest.get("outcome_verified"):
        raise ValueError("unverified outcome: " + str(manifest.get("termination_reason") or manifest.get("status")))
    players = sorted(manifest.get("players", []), key=lambda p: p.get("player", 0))
    results = [p.get("result_metadata") or {} for p in players]
    if (len(players) != 2 or [p.get("player") for p in players] != [1, 2]
            or any(p.get("return_code") != 0 for p in players)
            or any(r.get("ended") is not True or type(r.get("winner")) is not bool for r in results)
            or {r["winner"] for r in results} != {True, False}):
        raise ValueError("non-clean or inconsistent terminal result")
    for player in players:
        stderr = Path(player.get("stderr", {}).get("path", ""))
        if not stderr.is_file():
            raise ValueError("missing engine diagnostic log")
        if "insync_hash_mismatch" in stderr.read_text(errors="replace"):
            raise ValueError("engine hash mismatch")
    replay_players = set()
    for replay in manifest.get("replays", []):
        if file_hash(replay["path"]) != replay.get("sha256"):
            raise ValueError("replay hash mismatch")
        replay_players.add(replay.get("player"))
    if replay_players != {1, 2}:
        raise ValueError("missing player replay")
    inputs = manifest.get("inputs", {})
    source_players = sorted(inputs.get("players", []), key=lambda p: p.get("player", 0))
    if len(source_players) != 2:
        raise ValueError("missing frozen player identities")
    nodes, node_data = [], {}
    for player in source_players:
        module = player.get("bot_module", {})
        if not module.get("sha256") or not player.get("race"):
            raise ValueError("missing build SHA or race")
        if module.get("build_provenance", {}).get("diagnostic_only"):
            raise ValueError("diagnostic bot binary")
        configs = sorted((Path(x.get("path", "")).name, x.get("sha256")) for x in player.get("ai_files", []))
        if any(not sha for _, sha in configs):
            raise ValueError("missing config identity")
        node_id = digest({"module": module["sha256"], "race": player["race"], "ai_files": configs})
        identity = next((p for p in public.get("players", []) if p.get("player") == player["player"]), {})
        node_data[node_id] = {key: identity.get(key) for key in ("ownership", "origin", "author", "author_url", "source_url")}
        node_data[node_id].update(id=node_id, name=identity.get("bot") or player.get("name") or "Unknown bot", module_sha256=module["sha256"], race=player["race"], config_sha256=digest(configs))
        nodes.append(node_id)
    if len(set(nodes)) != 2:
        raise ValueError("same exact build/configuration on both sides")
    learning = manifest.get("reproducibility", {}).get("learning_state")
    if learning != "empty isolated read/write directories for each player":
        raise ValueError("unsupported learning-state regime")
    latency = [r.get("latency_frames") for r in results]
    if latency != [3, 3]:
        raise ValueError("missing or incompatible latency observations")
    engine = {"launcher": inputs.get("launcher", {}).get("sha256"),
              "libraries": sorted((Path(x.get("path", "")).name, x.get("sha256")) for x in inputs.get("engine_libraries", [])),
              "game_data": sorted(x.get("sha256", "") for x in inputs.get("game_data", [])),
              "platform": manifest.get("platform"), "latency_frames": 3,
              "learning_state": learning, "rules": manifest.get("rules")}
    if not engine["launcher"] or not engine["libraries"] or not engine["game_data"]:
        raise ValueError("incomplete engine identity")
    regime = digest(engine)
    map_sha = inputs.get("map", {}).get("sha256")
    scenario_seed = manifest.get("reproducibility", {}).get("random_seed")
    if not map_sha or type(scenario_seed) is not int:
        raise ValueError("missing map identity or scenario seed")
    scenario = digest({"regime": regime, "nodes": nodes, "map": map_sha, "seed": scenario_seed,
                       "bot_seeds": [p.get("bot_seed") for p in source_players]})
    winner = nodes[next(i for i, r in enumerate(results) if r["winner"])]
    return {"run_id": manifest["run_id"], "experiment_id": manifest.get("experiment_id"), "date": manifest.get("finished_at"),
            "nodes": nodes, "winner": winner, "loser": next(n for n in nodes if n != winner), "regime_id": regime,
            "scenario_id": scenario, "map_sha256": map_sha, "map": inputs["map"].get("configured_path")}, node_data


def build_league(root, public_runs, fallback=None):
    root = Path(root)
    config_path = root / "config/local-ratings.json"
    if not config_path.is_file():
        return fallback or {}
    config = json.loads(config_path.read_text())
    cohort_configs = config.get("cohorts") or [{
        "id": "configured",
        "label": "Configured local league",
        "experiment_ids": config.get("experiments", []),
        "expected_nodes": config.get("expected_nodes"),
        "expected_games": config.get("expected_games"),
    }]
    cohorts = []
    experiment_cohort = {}
    for index, cohort in enumerate(cohort_configs):
        cohort_id = str(cohort.get("id") or f"cohort-{index + 1}")
        experiment_ids = cohort.get("experiment_ids", cohort.get("experiments", []))
        cohort = {**cohort, "id": cohort_id, "label": cohort.get("label") or cohort_id,
                  "experiment_ids": list(experiment_ids)}
        cohorts.append(cohort)
        for experiment_id in cohort["experiment_ids"]:
            if experiment_id in experiment_cohort:
                raise ValueError(f"experiment assigned to multiple rating cohorts: {experiment_id}")
            experiment_cohort[experiment_id] = cohort_id
    allowed = set(experiment_cohort)
    reviewed = config.get("reviewed_runs", {})
    public_by_run = {run["run_id"]: run for run in public_runs if run.get("run_id")}
    paths = sorted((root / "artifacts/runs").glob("*/game-*/manifest.json")) or sorted((root / "artifacts/runs").glob("*/manifest.json"))
    if not paths:
        return fallback or {}
    all_games, node_data, excluded = [], {}, []
    seen = set()
    for path in paths:
        try:
            manifest = json.loads(path.read_text())
        except (ValueError, OSError):
            excluded.append({"run_id": path.parent.parent.name if path.parent.name.startswith("game-") else path.parent.name,
                             "reason": "unreadable run manifest; cannot establish rating eligibility"})
            continue
        if not isinstance(manifest, dict) or manifest.get("experiment_id") not in allowed:
            continue
        try:
            game, identities = extract_game(manifest, public_by_run.get(manifest.get("run_id"), {}), path)
            game["cohort_id"] = experiment_cohort.get(game["experiment_id"], "configured")
            if reviewed.get(game["run_id"]) != file_hash(path):
                raise ValueError("pending replay and manifest review")
            if game["scenario_id"] in seen:
                raise ValueError("duplicate exact scenario; no extra rating evidence")
            seen.add(game["scenario_id"])
            node_data.update(identities)
            all_games.append(game)
        except (ValueError, OSError, KeyError, TypeError) as error:
            excluded.append({"run_id": manifest.get("run_id"), "reason": str(error) if isinstance(error, ValueError) else "missing or unreadable evidence"})
    all_games.sort(key=lambda g: (g["date"] or "", g["run_id"]))
    prior_sd = config.get("prior_sd_elo", 400)
    components = []
    cohort_by_id = {cohort["id"]: cohort for cohort in cohorts}
    for regime in sorted({g["regime_id"] for g in all_games}):
        regime_games = [g for g in all_games if g["regime_id"] == regime]
        for nodes in connected_components(regime_games):
            games = [g for g in regime_games if g["nodes"][0] in nodes]
            component_cohort_ids = sorted({g["cohort_id"] for g in games})
            reference = next((n for n in nodes if node_data[n]["module_sha256"] == config.get("reference_module_sha256")), nodes[0])
            ri = nodes.index(reference)
            pairs = [(g["winner"], g["loser"]) for g in games]
            theta, covariance = fit_bt(nodes, pairs, prior_sd)
            sensitivity = {sd: fit_bt(nodes, pairs, sd)[0] for sd in (200, 800)}
            component_id = digest({"regime": regime, "reference": reference})
            rows = []
            for i, node in enumerate(nodes):
                own_games = [g for g in games if node in g["nodes"]]
                wins = sum(g["winner"] == node for g in own_games)
                rows.append({**node_data[node], **contrast(theta, covariance, i, ri), "is_reference": node == reference,
                             "games": len(own_games), "wins": wins, "losses": len(own_games) - wins,
                             "opponent_count": len({n for g in own_games for n in g["nodes"] if n != node}),
                             "map_count": len({g["map_sha256"] for g in own_games}),
                             "prior_sensitivity": {str(sd): round(1000 + ELO_PER_LOGIT * (t[i] - t[ri]), 1) for sd, t in sensitivity.items()}, "history": []})
            # A history point is cumulative evidence for this exact build and
            # reference. Do not display disconnected prior-only contrasts.
            for end in range(1, len(games) + 1):
                prefix = games[:end]
                connected = next((c for c in connected_components(prefix) if reference in c), [])
                if not connected:
                    continue
                t, cov = fit_bt(nodes, [(g["winner"], g["loser"]) for g in prefix], prior_sd)
                for i, row in enumerate(rows):
                    if row["id"] in connected:
                        row["history"].append({"date": prefix[-1]["date"], **contrast(t, cov, i, ri),
                                               "games": sum(row["id"] in g["nodes"] for g in prefix), "experiment_id": prefix[-1]["experiment_id"]})
            matchups = []
            for a, b in sorted({tuple(sorted(g["nodes"])) for g in games}):
                pair_games = [g for g in games if set(g["nodes"]) == {a, b}]
                matchups.append({"a": a, "b": b, "a_wins": sum(g["winner"] == a for g in pair_games), "b_wins": sum(g["winner"] == b for g in pair_games), "games": len(pair_games)})
            components.append({"id": component_id, "cohort_ids": component_cohort_ids,
                               "cohort_labels": [cohort_by_id[c]["label"] for c in component_cohort_ids],
                               "current": any(cohort_by_id[c].get("current") is True for c in component_cohort_ids),
                               "regime_id": regime, "reference_id": reference, "reference_name": node_data[reference]["name"],
                               "note": "1000 is an arbitrary reference coordinate, not a BASIL rating. Intervals are approximate and conditional on the model; map and matchup effects are not fitted.",
                               "games": len(games), "map_count": len({g["map_sha256"] for g in games}), "rows": sorted(rows, key=lambda r: (-r["rating"], r["id"])),
                               "matchups": matchups, "run_ids": [g["run_id"] for g in games]})
    cohort_summaries = []
    for cohort in cohorts:
        cohort_games = [g for g in all_games if g["cohort_id"] == cohort["id"]]
        cohort_summaries.append({"id": cohort["id"], "label": cohort["label"], "current": cohort.get("current") is True,
                                 "expected_nodes": cohort.get("expected_nodes"),
                                 "expected_games": cohort.get("expected_games"),
                                 "reviewed_games": len(cohort_games),
                                 "reviewed_nodes": len({n for g in cohort_games for n in g["nodes"]}),
                                 "component_ids": [c["id"] for c in components if cohort["id"] in c["cohort_ids"]]})
    expected_nodes = config.get("expected_nodes") if len(cohorts) == 1 else None
    expected_games = config.get("expected_games") if len(cohorts) == 1 else None
    return {"schema_version": 1, "method": "Gaussian-prior Bradley–Terry, Laplace uncertainty", "prior_sd_elo": prior_sd,
            "status": "uncalibrated_local", "interval_note": "Approximate 95% intervals for strength relative to the displayed reference. Sparse sweeps depend strongly on the prior. Repeated map/slot pairs may be correlated; intervals do not measure generalization to new maps or tournaments.",
            "cohorts": cohort_summaries, "components": components, "excluded": excluded, "eligible_experiments": sorted(allowed),
            "expected_nodes": expected_nodes, "expected_games": expected_games, "reviewed_games": len(all_games)}
