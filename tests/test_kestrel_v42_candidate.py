import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "third_party/kestrel-opening-v42-candidate/Kestrel.cpp"
V41_SOURCE = ROOT / "third_party/kestrel-opening-v41-candidate/Kestrel.cpp"
PATCH = ROOT / "patches/kestrel-v41-to-v42-five-probe-pylon.patch"


class KestrelV42CandidateTest(unittest.TestCase):
    def setUp(self):
        self.source = SOURCE.read_text()
        self.v41 = V41_SOURCE.read_text()

    def test_candidate_is_v41_plus_the_five_probe_opening_policy(self):
        self.assertNotEqual(self.source, self.v41)
        patch = PATCH.read_text()
        self.assertIn("completedProbes >= 5", self.source)
        self.assertIn("zergFiveProbePolicyActive", self.source)
        self.assertIn("zerg_five_probe_policy_active_frames", self.source)
        self.assertIn("zerg_five_probe_pylon_accepted_frame", self.source)
        self.assertIn("zerg_five_probe_pylon_accepted", self.source)
        self.assertIn("zerg_five_probe_policy_active_frames", patch)
        self.assertNotIn("completedProbes >= 4", patch)

    def test_training_and_first_pylon_use_the_same_public_five_probe_condition(self):
        train_units = self.source[self.source.index("    void trainUnits()") : self.source.index("    void constructOpening()")]
        construct = self.source[self.source.index("    void constructOpening()") : self.source.index("    void assignEconomy()")]
        self.assertRegex(
            train_units,
            re.compile(
                r"const bool zergFiveProbePolicyActive =\s*"
                r"knownZerg_ && completedProbes >= 5 && firstPylonCurrentFrame_ < 0;"
            ),
        )
        self.assertIn("if (zergFiveProbePolicyActive) {", train_units)
        self.assertIn("openingReserve = kZergTwoGatewayProbeReserve;", train_units)
        self.assertIn(
            "if (knownZerg_ && completedProbes >= 5 && firstPylonCurrentFrame_ < 0 && spendableMinerals() >= 100)",
            construct,
        )

    def test_v41_reserve_telemetry_remains_and_pylon_acceptance_is_public_self_state(self):
        self.assertIn("zerg_pre_pylon_probe_reserve_frames", self.source)
        self.assertIn("if (zergPrePylonProbeReserve) ++zergPrePylonProbeReserveFrames_;", self.source)
        self.assertIn(
            "if (knownZerg_ && count(BWAPI::UnitTypes::Protoss_Probe, true) >= 5 && firstPylonCurrentFrame_ < 0)",
            self.source,
        )
        self.assertIn("zergFiveProbePylonAcceptedFrame_ = frame;", self.source)
        self.assertNotIn("getAllUnits()", self.source[self.source.index("void trainUnits()") : self.source.index("void constructOpening()")])


if __name__ == "__main__":
    unittest.main()
