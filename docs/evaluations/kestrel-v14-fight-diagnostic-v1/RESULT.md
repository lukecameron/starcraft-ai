# Kestrel v14 first-fight diagnostic result

## Finding

The registered hypothesis is supported in this one trajectory: the first two completed Zealots stayed at home and fought locally while heavily outnumbered. They did not leave toward the scout's distant targets, and the accepted-attack history does not show harmful rapid target switching.

The single registered run was `20260920T075933-6d07d8618ace`. It completed as a Kestrel loss with reciprocal callbacks, both launchers returning zero, LF3, no state-hash mismatch, and both replay copies parsing fully through 6,016/6,047 frames. The trace contains 40 bounded snapshots, seven accepted attacks, and the first-completed-Zealot event.

## First defender

Zealot 144 completed at frame 3,389 at `(3576,704)`, near the starting base. It remained idle there through frame 3,660. At frame 3,702 it accepted an attack on Zergling 141 at `(3451,965)`, which was within roughly 580 pixels of home; three visible Zerglings were already in that local approach at frame 3,720. At frame 3,780 the Zealot was fighting six visible Zerglings, had lost all but one shield and 14 HP, and its target had only 4 HP. Its sole target change, at frame 3,792 from unit 141 to unit 119, followed that nearly dead target. Zealot 144 was gone by the frame-3,840 snapshot.

This is local defense against at least six attackers, not a chase toward the scout-visible units that appeared roughly 3,000 pixels from home around frame 3,000. One justified target change after a nearly killed target is not repeated attack thrashing.

## Second defender

Zealot 155 was still warping while the first defender fought and died. It completed shortly before frame 4,176, then accepted an attack on Zergling 28 at the home base. From frames 4,176 through 4,368 it retained the same target; the three accepted requests are the policy's 96-frame retry cadence, not target switching. Snapshots show seven or more visible Zerglings within about 300 pixels of home as it entered combat. It fell from full shields at frame 4,260 to 41 shields at 4,320 and 50 HP/2 shields at 4,380, and was gone by frame 4,440. A third Zealot remained incomplete through frame 5,000.

The observed failure is sequential local engagement: each Zealot completes after the attack has arrived and fights the Zergling group alone. The trace does not support changing target persistence or preventing outward movement. It narrows the next design question to whether the opening can create overlapping completed defenders or otherwise survive until they overlap; it does not itself select a policy.

## Preserved identity

- Diagnostic module: `f2bd52def8c0afc837ead106a5e16b821b8023d50b4cf82363562dba84bc2d3c`
- Source: `ff6bf76b2291b945739555f84e4b287262705aebfdcd8a43652662e3cdb174e1`
- Patch: `791ab8db8e7e19a4d54422e81ff4dc8f310c35f21dbf67adc6c4be21127e3e31`
- Player-1 replay: `1749bdaef3e080fc5b05184400d9e669930e4a0d1f6fa23cedd84c1b865085be`
- Player-2 replay: `1e0bfecdf2bb483479631fa3835f9a4242788891cc31ec77e17b6a886cee042b`
- Raw trace: `artifacts/runs/20260920T075933-6d07d8618ace/game-0001/player-1/bwapi-data/write/kestrel-v14-fight.jsonl`

Instrumentation uses only public observations and does not change gameplay commands. This one diagnostic supports a source diagnosis, not strength or adoption.
