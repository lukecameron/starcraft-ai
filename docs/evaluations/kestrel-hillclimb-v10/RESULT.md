# Kestrel v31 early-Zerg squad-staging result

## Decision: INCONCLUSIVE — TRANSPORT NEVER STARTED

All five preregistered attempts were launched concurrently and preserved, but no game began. Both launchers in every lane exited normally after reporting `Error: connect: No such file or directory`; no terminal metadata or replay was produced and every manifest has a null logical frame count. The attempted runner environment restricted the Unix-domain transport under `/tmp`, so the batch cannot test policy, strength, speed or Elo.

No retry or replacement belongs to this experiment. A separately registered recovery may reuse the same frozen build, matrix and seeds because these attempts executed zero logical game frames. All five failed manifests and ten launcher logs remain under the local artifact store.

- Batch manifest SHA-256: `2629339b7bfe023fd38a2977f6a72aa174f17f1a07eed8d358862052ef109ed5`.
- Frozen schedule SHA-256: `8d4bc24fc2cfe421ce6f01f41fb0181692d935ab7f1ddc1e946541991bb05d38`.
- Candidate binary SHA-256: `5ff164dc9dfd5c555837f110002f3907838891c6fdc95a8960cc48f12e47e107`.
