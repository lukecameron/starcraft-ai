#!/usr/bin/env python3
"""Check McRave source contracts and model cached selection edge cases."""
import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UTIL = (ROOT / "third_party/mcrave/Source/McRave/Main/Util.h").read_text()
GOALS = (ROOT / "third_party/mcrave/Source/McRave/Strategy/Goals/Goals.cpp").read_text()

# Keep the model tied to the actual helper/candidate contracts. These checks fail
# if either implementation gains another filter or changes its comparison rule.
ground_helper = UTIL[UTIL.index("UnitInfo *getClosestUnitGround"):UTIL.index("UnitInfo *getFurthestUnitGround")]
assert ground_helper.count("if (") == 2
assert "if (!pred(u))" in ground_helper
assert "BWEB::Map::getGroundDistance(here, u->getPosition())" in ground_helper
assert "if (dist < distBest)" in ground_helper
candidate_branch = GOALS[GOALS.index("if (count <= 0)"):GOALS.index("template <class T> //\n        void assignPercentToGoal")]
assert "if (assignable(unit))" in candidate_branch
assert "if (assignable(unit) && distance < distBest)" in candidate_branch
assert candidate_branch.count("BWEB::Map::getGroundDistance") == 1


def original(candidates, initial_eligible, count):
    eligible = list(initial_eligible)
    selected = []
    for _ in range(count):
        best = None
        best_distance = sys.float_info.max
        for index, distance in enumerate(candidates):
            if eligible[index] and distance < best_distance:
                best = index
                best_distance = distance
        if best is not None:
            selected.append(best)
            eligible[best] = False
    return selected


def cached(candidates, initial_eligible, count):
    distances = [(index, distance) for index, distance in enumerate(candidates) if initial_eligible[index]]
    eligible = list(initial_eligible)
    selected = []
    for _ in range(count):
        best = None
        best_distance = sys.float_info.max
        for index, distance in distances:
            if eligible[index] and distance < best_distance:
                best = index
                best_distance = distance
        if best is not None:
            selected.append(best)
            eligible[best] = False
    return selected


rng = random.Random(20260920)
for case in range(10000):
    distances = [rng.choice([-1.0, 0.0, 1.0, 8.0, 8.0, 32.5, 100.0,
                             sys.float_info.max, float("inf"), float("nan")])
                 for _ in range(rng.randrange(80))]
    initial_eligible = [bool(rng.randrange(2)) for _ in distances]
    count = rng.randrange(100)
    assert original(distances, initial_eligible, count) == cached(distances, initial_eligible, count), case
print("actual source contracts verified; 10000 ordered cases passed, including ties, DBL_MAX, infinity, and NaN")
