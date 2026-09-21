import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "third_party/kestrel-opening-v45-candidate/Kestrel.cpp"
V43_SOURCE = ROOT / "third_party/kestrel-opening-v43-candidate/Kestrel.cpp"
PATCH = ROOT / "patches/kestrel-v43-to-v45-four-probe-pylon.patch"


class KestrelV45CandidateTest(unittest.TestCase):
    def setUp(self):
        self.source = SOURCE.read_text()
        self.v43 = V43_SOURCE.read_text()

    def test_candidate_is_v43_plus_four_probe_opening_and_completion_telemetry(self):
        self.assertNotEqual(self.source, self.v43)
        self.assertIn("completedProbes >= 4", self.source)
        self.assertNotIn("completedProbes >= 5", self.source)
        self.assertIn("zergFourProbePolicyActive", self.source)
        self.assertIn("zerg_four_probe_policy_active_frames", self.source)
        self.assertIn("zerg_four_probe_pylon_accepted_frame", self.source)
        self.assertIn("zerg_four_probe_pylon_accepted", self.source)
        self.assertIn("zerg_four_probe_pylon_probe_count", self.source)
        self.assertIn("secondZealotCompletedFrame_", self.source)
        self.assertIn("second_zealot_completed_frame", self.source)
        self.assertIn("zerg_second_zealot_probe_reserve_block_pre_accept_flags", self.source)
        self.assertNotIn("zergSixthProbeRestorationActive", self.source)

    def test_zerg_probe_training_is_suppressed_until_first_pylon_acceptance(self):
        train_units = self.source[self.source.index("    void trainUnits()") : self.source.index("    void constructOpening()")]
        construct = self.source[self.source.index("    void constructOpening()") : self.source.index("    void assignEconomy()")]
        self.assertRegex(
            train_units,
            re.compile(
                r"const bool zergFourProbePolicyActive =\s*"
                r"knownZerg_ && completedProbes >= 4 && firstPylonCurrentFrame_ < 0;"
            ),
        )
        self.assertIn(
            "canTrainProbe &&\n                    (!knownZerg_ || firstPylonAcceptedFrame_ >= 0)",
            train_units,
        )
        self.assertIn(
            "if (knownZerg_ && completedProbes >= 4 && firstPylonCurrentFrame_ < 0 && spendableMinerals() >= 100)",
            construct,
        )
        self.assertNotIn("getAllUnits()", train_units)

    def test_v43_reserves_and_second_zealot_completion_are_retained(self):
        train_units = self.source[self.source.index("    void trainUnits()") : self.source.index("    void constructOpening()")]
        self.assertIn("if (firstGatewayCurrentFrame_ < 0) openingReserve = 250;", train_units)
        self.assertIn("else if (secondGatewayCurrentFrame_ < 0) openingReserve = 250;", train_units)
        self.assertIn("else if (acceptedZealotTrains_ < 2) openingReserve = 100;", train_units)
        self.assertIn("acceptedZealotTrains_ == 2", train_units)
        play = self.source[self.source.index("    void play()") : self.source.index("public:")]
        self.assertIn(
            "if (count(BWAPI::UnitTypes::Protoss_Zealot, true) >= 2 && secondZealotCompletedFrame_ < 0)",
            play,
        )

    def test_treatment_is_zerg_gated_and_patch_is_present(self):
        treatment = self.source[self.source.index("void trainUnits()") : self.source.index("void constructOpening()")]
        self.assertIn("knownZerg_ && completedProbes >= 4", treatment)
        self.assertIn("knownZerg_ && firstPylonAcceptedFrame_ >= 0", treatment)
        self.assertIn("zergFourProbePylonAcceptedFrame_ = frame", self.source)
        patch = PATCH.read_text()
        self.assertIn("completedProbes >= 4", patch)
        self.assertIn("secondZealotCompletedFrame_", patch)
        self.assertIn("zerg_four_probe_policy_active_frames", patch)
        self.assertIn("zerg_second_zealot_probe_reserve_block_pre_accept_flags", patch)


if __name__ == "__main__":
    unittest.main()
