# Paired confirmation runner

`scripts/run_paired_confirmation.py` exists because the current quick-evaluation runner accepts one fixed candidate module for an entire schedule. It cannot alternate two frozen McRave modules within each matched pair or safely resume the unlaunched remainder of this fixed pair order. This experiment-specific driver calls the existing `scripts/run_match.py` CLI directly; it adds only schedule validation, serial ordering, pair checkpoints, the registered stop rules, and retained replay/terminal inspection. It is not a general match-control service.

Validate without launching:

```sh
python3 scripts/run_paired_confirmation.py \
  --schedule docs/evaluations/mcrave-zvz-9pool-confirmation-v1/schedule.json \
  --validate-only
```

The operational confirmation command, only after explicit authorization, is the same command without `--validate-only`. The compatibility preflight uses `docs/evaluations/mcrave-ualberta-zerg-compat-v1/schedule.json`.
