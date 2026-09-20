#!/usr/bin/env python3
"""Export an allowlisted static progress dashboard from local manifests."""
from __future__ import annotations
import argparse, json, math, shutil
from datetime import datetime, timezone
from pathlib import Path

try:
    from .local_ratings import build_league
except ImportError:
    from local_ratings import build_league

BOT_NAMES={"WorkerRush.dylib":"WorkerRush","Idle.dylib":"Idle","McRave.dylib":"McRave","ZZZKBot.dylib":"ZZZKBot","UAlbertaBot.dylib":"UAlbertaBot"}
EXPERIMENT_DECISIONS={"ADOPT","REJECT","INCONCLUSIVE"}

def load_json(path, fallback):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError): return fallback

def bot_identity(player):
    env=player.get("environment",{}); raw=env.get("BWAPI_CONFIG_AI__AI") if isinstance(env,dict) else None
    name=Path(str(raw)).name if raw else "Unknown bot"
    return BOT_NAMES.get(name,Path(name).stem or "Unknown bot")

def identity_for(module_name, identities, module_sha=None):
    family=identities.get(Path(str(module_name or "")).name,{}) if isinstance(identities,dict) else {}
    value=family
    overrides=family.get("sha256_overrides",{}) if isinstance(family,dict) else {}
    if module_sha and isinstance(overrides,dict) and isinstance(overrides.get(module_sha),dict):
        # Variant records may change local ownership/origin only; family-level
        # upstream attribution must remain intact for every binary.
        value={**family,**{k:v for k,v in overrides[module_sha].items() if k in {"ownership","origin"}}}
    if not isinstance(value,dict): value={}
    return {"ownership":value.get("ownership","unknown"),"origin":value.get("origin","unknown"),"upstream_name":value.get("upstream_name"),"author":value.get("author"),"author_url":value.get("author_url"),"source_url":value.get("source_url"),"provenance_verified":bool(value)}

def public_manifest(path, identities=None):
    source=load_json(path,{})
    if not isinstance(source,dict): return {}
    inputs=source.get("inputs",{}) if isinstance(source.get("inputs"),dict) else {}
    input_players={x.get("player"):x for x in inputs.get("players",[]) if isinstance(x,dict)}
    players=[]
    runtime_players={p.get("player"):p for p in source.get("players",[]) if isinstance(p,dict)}
    player_ids=sorted(set(input_players)|set(runtime_players))
    for player_id in player_ids:
        player=runtime_players.get(player_id,{"player":player_id})
        if not isinstance(player,dict): continue
        env=player.get("environment",{}); result=player.get("result_metadata"); inp=input_players.get(player.get("player"),{})
        module=inp.get("bot_module",{}) if isinstance(inp,dict) else {}; provenance=module.get("build_provenance",{}) if isinstance(module,dict) else {}
        usage=player.get("resource_usage",{}) if isinstance(player.get("resource_usage"),dict) else {}
        build_name=Path(str(module.get("path",""))).name or Path(str(env.get("BWAPI_CONFIG_AI__AI",""))).name or None
        identity=identity_for(build_name,identities or {},module.get("sha256"))
        players.append({"player":player.get("player"),"name":inp.get("name"),"bot":identity.get("upstream_name") or bot_identity(player),"race":inp.get("race") or (env.get("BWAPI_CONFIG_AUTO_MENU__RACE") if isinstance(env,dict) else None),"build_name":build_name,"module_sha256":module.get("sha256"),**identity,"source_url":identity.get("source_url") or provenance.get("source_repository") or inp.get("source_url"),"source_revision":provenance.get("source_revision"),"return_code":player.get("return_code"),"peak_rss_raw":usage.get("peak_rss_raw"),"user_cpu_seconds":usage.get("user_cpu_seconds"),"result":{k:result.get(k) for k in ("ended","winner","frame_count","latency_frames","command_count","rejected_commands")} if isinstance(result,dict) else None})
    replays=[]
    for index,replay in enumerate(source.get("replays",[]),1):
        if isinstance(replay,dict):
            replay_player=next((x for x in players if x.get("player")==replay.get("player")),{})
            replays.append({"player":replay.get("player"),"bot":replay_player.get("bot"),"ownership":replay_player.get("ownership"),"origin":replay_player.get("origin"),"upstream_name":replay_player.get("upstream_name"),"author":replay_player.get("author"),"author_url":replay_player.get("author_url"),"source_url":replay_player.get("source_url"),"size_bytes":replay.get("size_bytes"),"sha256":replay.get("sha256"),"source_run":source.get("run_id"),"ordinal":index,"source_path":replay.get("path") or replay.get("replay_path")})
    map_input=inputs.get("map",{}) if isinstance(inputs.get("map"),dict) else {}
    return {"run_id":source.get("run_id"),"game_id":source.get("game_id"),"experiment_id":source.get("experiment_id"),"purpose":source.get("purpose"),"status":source.get("status"),"started_at":source.get("started_at"),"finished_at":source.get("finished_at"),"termination_reason":source.get("termination_reason"),"map":map_input.get("configured_path"),"map_sha256":map_input.get("sha256"),"logical_frame_count":source.get("logical_frame_count"),"throughput":source.get("logical_frames_per_wall_second"),"durable_throughput":source.get("durable_logical_frames_per_wall_second"),"elapsed_seconds":source.get("elapsed_seconds"),"durable_completion_seconds":source.get("durable_completion_seconds"),"outcome_verified":source.get("outcome_verified"),"players":players,"replays":replays}

def public_experiment(path, identities=None):
    source=load_json(path,{})
    if not isinstance(source,dict) or not source.get("experiment_id"): return {}
    result={"id":source["experiment_id"]}
    for key in ("title","status","hypothesis","summary","started_at","finished_at","runner_notes"):
        if source.get(key) is not None and source.get(key) != "": result[key]=source[key]
    decision=source.get("decision")
    if isinstance(decision,str) and decision in EXPERIMENT_DECISIONS:
        result["decision"]=decision
    elif decision not in (None,""):
        # Older runners put generic follow-up advice in this field. It is not
        # an evaluation verdict and must not replace the reviewed conclusion.
        result.setdefault("runner_notes",decision)
    if source.get("started_at"):
        result["date"]=str(source["started_at"])[:10]
    if source.get("conclusion") not in (None,""):
        result["conclusion"]=source["conclusion"]
    games=[]
    for game in source.get("games",[]):
        if not isinstance(game,dict): continue
        m=game.get("measurements",{}) if isinstance(game.get("measurements"),dict) else {}
        games.append({"index":game.get("index"),"opponent":game.get("opponent"),"map":game.get("map"),"candidate_player":game.get("candidate_player"),"status":game.get("status"),"classification":game.get("classification"),"measurements":{k:m.get(k) for k in ("elapsed_seconds","durable_completion_seconds","logical_frame_count","logical_frames_per_wall_second")}})
    candidate=source.get("candidate",{}) if isinstance(source.get("candidate"),dict) else {}
    opponents={}
    for name,value in (source.get("opponents",{}) if isinstance(source.get("opponents"),dict) else {}).items():
        if isinstance(value,dict): opponents[name]={"race":value.get("race"),**identity_for(value.get("path"),identities or {},value.get("sha256"))}
    if candidate:
        result["candidate"]={"sha256":candidate.get("sha256"),**identity_for(candidate.get("path"),identities or {},candidate.get("sha256"))}
    if opponents: result["opponents"]=opponents
    if games: result["games"]=games
    scorecard=load_json(path.parent/"hillclimb-scorecard.json",{})
    if isinstance(scorecard,dict) and isinstance(scorecard.get("aggregate"),dict):
        public_games=[]
        for game in scorecard.get("games",[]):
            if not isinstance(game,dict): continue
            replay=game.get("replay",{}) if isinstance(game.get("replay"),dict) else {}
            public_games.append({"index":game.get("index"),"run_id":game.get("run_id"),"candidate_outcome":game.get("candidate_outcome"),"terminal_frames":game.get("terminal_frames"),"elapsed_seconds":game.get("elapsed_seconds"),"durable_fps":game.get("durable_fps"),"short_game":game.get("short_game"),"heuristic_grade":replay.get("heuristic_grade"),"heuristic_score":replay.get("heuristic_score"),"signals":replay.get("signals"),"first_frames":replay.get("first_frames"),"attack_orders":replay.get("attack_orders"),"harvest_orders":replay.get("harvest_orders"),"build_units":replay.get("build_units"),"production_units":replay.get("production_units")})
        result["scorecard"]={"schema_version":scorecard.get("schema_version"),"candidate_name":scorecard.get("candidate_name"),"measurement_scope":scorecard.get("measurement_scope"),"decision_note":scorecard.get("decision_note"),"aggregate":scorecard["aggregate"],"games":public_games}
    return result

def append_unique(existing, additions, fields):
    result=[x for x in existing if isinstance(x,dict)]; keys={tuple(x.get(f) for f in fields) for x in result}
    for item in additions:
        key=tuple(item.get(f) for f in fields)
        if key not in keys: result.append(item); keys.add(key)
    return result

def local_history(experiments):
    points=[]
    for experiment in experiments:
        summary=experiment.get("summary",{}) if isinstance(experiment,dict) else {}
        for opponent,result in (summary.get("by_opponent",{}) if isinstance(summary,dict) else {}).items():
            rating=result.get("relative_elo_advantage") if isinstance(result,dict) else None
            if isinstance(rating,(int,float)) and math.isfinite(rating): points.append({"id":f"{experiment.get('id')}:{opponent}","name":opponent,"date":experiment.get("finished_at") or experiment.get("date"),"rating":rating,"source":"local_relative_elo"})
    return points

def absolutize_replays(path, base_url):
    snapshot=load_json(path,{})
    if not isinstance(snapshot,dict): raise ValueError(f"invalid dashboard snapshot: {path}")
    base=base_url.rstrip("/")
    for run in snapshot.get("runs",[]):
        for replay in run.get("replays",[]) if isinstance(run,dict) else []:
            value=replay.get("replay_path") if isinstance(replay,dict) else None
            if isinstance(value,str) and value and "://" not in value: replay["replay_path"]=base+"/"+value.lstrip("/")
    path.write_text(json.dumps(snapshot,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return snapshot

def export(root, output):
    output.mkdir(parents=True,exist_ok=True); fallback=load_json(root/"dashboard/data.json",{})
    identity_config=load_json(root/"config/bot-identities.json",{"bots":{}}); identities=identity_config.get("bots",{}) if isinstance(identity_config,dict) else {}
    run_paths=sorted((root/"artifacts/runs").glob("*/game-*/manifest.json")) or sorted((root/"artifacts/runs").glob("*/manifest.json"))
    runs=[x for path in run_paths if (x:=public_manifest(path,identities))]; has_raw_artifacts=bool(runs)
    if not runs and isinstance(fallback,dict): runs=fallback.get("runs",[])
    configured=load_json(root/"config/experiments.json",{"experiments":[]}); configured_experiments=configured.get("experiments",[]) if isinstance(configured,dict) else []
    artifact_experiments=[x for path in sorted((root/"artifacts/experiments").glob("*/manifest.json")) if (x:=public_experiment(path,identities))]
    by_id={}
    for experiment in fallback.get("experiments",[]) if isinstance(fallback,dict) else []:
        if isinstance(experiment,dict) and experiment.get("id"): by_id[experiment["id"]]={**by_id.get(experiment["id"],{}),**experiment}
    for experiment in configured_experiments:
        if isinstance(experiment,dict) and experiment.get("id"): by_id[experiment["id"]]={**by_id.get(experiment["id"],{}),**experiment}
    for experiment in artifact_experiments:
        merged={**by_id.get(experiment["id"],{}),**experiment}
        if not merged.get("conclusion") and merged.get("runner_notes"):
            merged["conclusion"]=merged["runner_notes"]
        by_id[experiment["id"]]=merged
    experiments=list(by_id.values())
    for experiment in experiments:
        if experiment.get("decision") not in ("ADOPT","REJECT","INCONCLUSIVE"):
            experiment.pop("decision",None)
    opponents=load_json(root/"config/opponents.json",{"opponents":[],"provisional_buckets":[]}); ratings=[]
    for item in opponents.get("opponents",[]) if isinstance(opponents,dict) else []:
        if isinstance(item,dict):
            r=item.get("ratings",{}); obs=item.get("basil_observation",{}); ratings.append({"id":item.get("id"),"name":item.get("display_name"),"race":(item.get("races") or [None])[0],"rating":r.get("basil_elo"),"observed":r.get("basil_observed"),"observed_timestamp":obs.get("lastUpdated"),"source_url":item.get("source_url"),"author":item.get("author"),"author_url":item.get("author_url"),"ownership":"upstream","origin":"upstream","license":item.get("license"),"version":item.get("version",{}),"status":item.get("openbw_status"),"played":obs.get("played"),"won":obs.get("won"),"lost":obs.get("lost"),"crashed":obs.get("crashed")})
    replay_dir=output/"replays"
    for run in runs:
        for replay in run.get("replays",[]) if isinstance(run,dict) else []:
            source_path=replay.pop("source_path",None)
            if source_path and Path(source_path).is_file():
                replay_dir.mkdir(parents=True,exist_ok=True); target=f"{run.get('run_id','run')}-{replay.get('player','unknown')}-{replay.get('ordinal','1')}.rep"
                shutil.copyfile(source_path,replay_dir/target); replay["replay_path"]="replays/"+target
    current_basil=[{"id":x.get("id"),"name":x.get("name"),"date":x.get("observed"),"rating":x.get("rating"),"source_url":x.get("source_url")} for x in ratings if x.get("rating") is not None]
    snapshot={"schema_version":1,"generated_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),"runs":runs,"experiments":experiments,"ratings":ratings or (fallback.get("ratings",[]) if isinstance(fallback,dict) else []),"rating_buckets":opponents.get("provisional_buckets",[]) if isinstance(opponents,dict) else (fallback.get("rating_buckets",[]) if isinstance(fallback,dict) else []),"basil_history":append_unique(fallback.get("basil_history",[]) if isinstance(fallback,dict) else [],current_basil,("id","date","rating")),"local_elo_history":append_unique(fallback.get("local_elo_history",[]) if isinstance(fallback,dict) else [],local_history(artifact_experiments),("id","date","rating"))}
    snapshot["local_league"]=build_league(root,runs,fallback.get("local_league",{}) if isinstance(fallback,dict) else {})
    serialized=json.dumps(snapshot,indent=2,sort_keys=True)+"\n"; (output/"data.json").write_text(serialized,encoding="utf-8")
    if has_raw_artifacts: (root/"dashboard/data.json").write_text(serialized,encoding="utf-8")
    shutil.copyfile(root/"dashboard/index.html",output/"index.html"); return snapshot

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument("--output",type=Path); parser.add_argument("--rewrite-replay-base")
    args=parser.parse_args()
    if args.rewrite_replay_base:
        absolutize_replays(args.root/"dashboard/data.json",args.rewrite_replay_base)
        public=args.root/"public/data.json"
        if public.is_file(): absolutize_replays(public,args.rewrite_replay_base)
        print(f"rewrote replay URLs to {args.rewrite_replay_base}"); return
    output=args.output or args.root/"dashboard/dist"; snapshot=export(args.root,output); print(f"exported {len(snapshot['runs'])} runs and {len(snapshot['experiments'])} experiments to {output}")

if __name__=="__main__": main()
