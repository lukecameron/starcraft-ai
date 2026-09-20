# Working instructions

Read `bwapi-autonomous-project-brief.md` and `docs/resume.md` first. The brief is the project assignment; the resume identifies the current validated build and running work.

- Prioritize credible competitive strength with short, explicit experiments. Do not promote from one lucky batch.
- Use native headless OpenBW for development; keep the official BWAPI 4.4.0 Win32 path credible and separately verified.
- Only public legal BWAPI observations enter gameplay. Evaluator/replay access may be privileged but must remain separate.
- Preserve every real match's replay, logs and manifest, including failures. Bulk artifacts/dependencies/game data stay local and ignored by Git.
- Label our bots as Ours and identify Original, Port or Fork in every dashboard list. Keep original author and source links with ports/forks. Upstream BASIL observations belong to upstream builds, never automatically to our ports. Maintain `config/bot-identities.json` as builds are added.
- Follow the model policy below for the lead and every delegated worker; the lead integrates and verifies.
- Reproduce bugs through the actual CLI/game path before fixing them. Lifecycle tests supplement real-engine checks.
- Record uncertainty and measurement scope. Diagnostic fixtures are not ladder anchors; Apple Silicon measurements are not tournament validation.
- Keep changes backed up on `main` in the authorized `lukecameron/starcraft-ai` repository. Do not contact people or submit a bot without authorization.
- Prefer simple direct workflows; add infrastructure only for an observed need. Track exact process/session IDs and checkpoint long work.

## Model policy

- Use **Sol (`gpt-5.6-sol`)** for the lead task.
- Use **Luna (`gpt-5.6-luna`)** for delegated workers unless the user changes this policy or explicitly authorizes an exception.
- When continuing work started by another model, preserve its exact processes, artifacts and experiment gates. Transfer the checkpoint to the current lead rather than rerunning active experiments.
- Model choice does not relax source review, preregistration, replay retention, provenance or validation requirements.
