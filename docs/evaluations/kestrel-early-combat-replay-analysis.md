# Kestrel early-combat replay analysis

This source and replay inspection asks whether Kestrel's first zealot was drawn away from its base by an enemy exposed by the scout. It covers the matched v7 and v8 Benzene games and v8's Heartbreak Ridge game. It does not change policy or establish a general behavior across seeds.

`scoutAndFight()` sends each completed zealot or dragoon to the nearest currently visible, detected ground enemy regardless of army size. The `army >= 4` condition applies only to attacking an unexplored public start position when no enemy is visible. A scout can therefore expose a global target that a new zealot is legally allowed to choose. `first_enemy_contact_frame` records any visible enemy anywhere and cannot be interpreted as base exposure.

The preserved command streams do not show that failure mode in these games:

| Version / run | Scout contact | First combat-unit attack | Home-location evidence | Interpretation |
| --- | --- | --- | --- | --- |
| v7 Benzene `20260920T063735-568f09f7d3a0` | Scout tag 3622 attacks at frame 2,642 near `(693,2842)` | Zealot tag 3598 attacks at frame 4,022 near `(3771,400)` | Opening worker harvest targets are near `(4000,496)` | Scout contact is distant; first zealot fights at home. |
| v8 Benzene `20260920T064202-95acc7e7959a` | Scout tag 3624 attacks at frame 2,648 near `(580,2855)` | Zealot tag 3606 attacks at frame 3,704 near `(3453,952)` | Opening worker harvest targets are near `(4000,496)` and `(4000,592)` | First zealot moves toward an approaching local threat, not the scout contact. |
| v8 Heartbreak Ridge `20260920T064215-e798f5386b3a` | Scout tag 3604 attacks at frame 2,414 near `(464,1248)` | Zealot tag 3577 attacks at frame 3,746 near `(3584,1625)` | Opening worker harvest targets are near `(4000,1904)` and `(4000,1968)` | First zealot fights near the right-side home. |

The selected zealot tags had not previously received harvest commands, while the scout tags had. Each later combat order in the inspected early sequence remains near the home-side engagements. The replay parser reported no command parse errors.

The source permits distant pursuit under another visibility trajectory, so a future policy may still need a rally or local-defense rule. These three losses do not support that as their observed cause. A new diagnostic is unnecessary for the bounded question because the existing replay records identify the selected unit tag, target position, and home resource positions. The next candidate should start from accepted v7 and target a separately observed cause rather than combining rejected v8 mineral reservation or v9 worker pulling.
