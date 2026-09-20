# Kestrel v12 pending-first-Pylon reservation result

## Decision: REJECT

The registered mechanism failed on Benzene and the production guard failed on Heartbreak Ridge. Kestrel v12 remains an isolated rejected candidate; canonical v7 is unchanged. The two losses are descriptive and are not a strength decision.

The experiment ran exactly the two registered games once each in batch session `60898`:

| Run | Map / seed | Result | Pylon accepted → current | Accepted first-Pylon requests | Commands rejected | FPS |
|---|---|---:|---:|---:|---:|---:|
| `20260920T072208-a970044c0407` | Benzene / 6103 | loss, 6,079 Kestrel frames | 996 → 1,285 (**289 frames; fail**) | 1 | 0/56 (0%; pass) | 2,967.3 |
| `20260920T072210-f1bde9483beb` | Heartbreak Ridge / 6104 | loss, 5,924 Kestrel frames | 1,200 → 1,315 (**115 frames; pass**) | 1 | 11/68 (16.2%; fail) | 3,466.5 |

The primary gate required one accepted request and a 0–120 frame accepted-to-current interval in **both** games. Heartbreak Ridge met it; Benzene exceeded it by 169 frames. This falsifies the claim that reserving 100 minerals from Probe training is sufficient to make the existing first-Pylon lifecycle prompt on both fixed inputs. Heartbreak Ridge's 11 rejected build requests were all `unit_busy`, so it also failed the registered under-5% command-rejection guard. The candidate is rejected even though every other recorded request category was accepted.

## Production and terminal checks

Both games produced Probes after the reservation, completed the first Pylon and Gateway, trained and completed Zealots, observed a Zergling near home, and issued accepted home-defense attacks. No wrong-race production was observed.

| Map | Pylon current / complete | Gateway current / complete | first Zealot train / complete | first home attacker / attack command | maxima (Probe/Pylon/Gateway/Zealot) |
|---|---:|---:|---:|---:|---:|
| Benzene | 1,285 / 1,806 | 2,127 / 3,098 | 3,102 / 3,707 | 3,727 / 3,786 | 16 / 2 / 2 / 2 |
| Heartbreak Ridge | 1,315 / 1,836 | 2,127 / 3,098 | 3,102 / 3,707 | 3,574 / 3,708 | 15 / 2 / 1 / 2 |

Both launchers returned zero, callbacks were reciprocal (Kestrel loss, ZZZK win), LF3 was reported, and neither stderr pair contained `insync_hash_mismatch`. All four replay copies parsed fully with `screp`; player-1 replay SHA-256 values are `9d0b259e5cee2bf116eb02d83500fc2ef9e8ff6d07df9d340ba22c077dfd9b01` and `815392bc0dd24de491ae779e27563a267daa74ece373edd2fa293ed07d3cca0f`. The terminal diagnostic streams contain the expected natural terminal controller transition and peer transport cleanup, with no hash mismatch. Each game exceeded the 384 logical frames/s package-operation floor.

## Identity and limits

The preregistration was written at `2026-09-20T07:18:59.327194+00:00`. Prelaunch review added the explicit once-only `firstPylonCurrentFrame < 0` guard before either trial; the final build was recorded at `2026-09-20T07:21:24+00:00` and the first game began at `2026-09-20T07:22:08.038799+00:00`.

- Module SHA-256: `cb91e9217c99099e2683603ab4220e1b2154d162df3ff8b62cb61a78deac3b8b`
- Combined source SHA-256: `006bc89ce5d7df71a374492ad86fcf3d519ff9d4d85dc752e1c4ec2b1e0436b6`
- V7-to-V12 patch SHA-256: `99d4e059558abd0ec51181f9145fb9adf2c266a0cd0d24ac17db586fa8e5a913`
- Frozen package: `artifacts/builds/cb91e9217c99099e2683603ab4220e1b2154d162df3ff8b62cb61a78deac3b8b/kestrel-v12-pylon-reservation/`
- Batch manifest: `artifacts/experiments/kestrel-pylon-reservation-v12/manifest.json`

This two-game screen isolates only the Probe-training reservation. It does not identify the remaining Benzene delay cause, estimate playing strength, or support changing canonical v7.
