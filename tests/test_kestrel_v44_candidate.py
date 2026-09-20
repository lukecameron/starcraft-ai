import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "third_party/kestrel-opening-v44-candidate/Kestrel.cpp"
V43_SOURCE = ROOT / "third_party/kestrel-opening-v43-candidate/Kestrel.cpp"
PATCH = ROOT / "patches/kestrel-v43-to-v44-sixth-probe-restoration.patch"


class KestrelV44CandidateTest(unittest.TestCase):
    def setUp(self):
        self.source = SOURCE.read_text()
        self.v43 = V43_SOURCE.read_text()

    def test_candidate_is_v43_plus_one_sixth_probe_restoration(self):
        self.assertNotEqual(self.source, self.v43)
        self.assertIn(
            "knownZerg_ && firstPylonAcceptedFrame_ >= 0 && secondGatewayCurrentFrame_ < 0 && probes < 6",
            self.source,
        )
        self.assertIn("openingReserve = 0;", self.source)
        self.assertIn("zergSixthProbeAcceptedCount_ == 0", self.source)
        self.assertIn("zerg_sixth_probe_accepted_frame", self.source)
        self.assertIn("zerg_sixth_probe_accepted_count", self.source)
        self.assertIn("zerg_post_pylon_pre_second_gateway_probe_train_count", self.source)
        self.assertIn("zerg_second_zealot_probe_reserve_block_pre_accept_flags", self.source)

    def test_restoration_is_zerg_gated_and_stops_before_second_gateway(self):
        train_units = self.source[self.source.index("    void trainUnits()") : self.source.index("    void constructOpening()")]
        self.assertIn("knownZerg_ && firstPylonAcceptedFrame_ >= 0", train_units)
        self.assertIn("secondGatewayCurrentFrame_ < 0", train_units)
        self.assertIn("zergPostPylonPreSecondGatewayProbeWindow", train_units)
        self.assertIn(
            "(!zergPostPylonPreSecondGatewayProbeWindow ||\n                     (zergSixthProbeRestorationActive && zergSixthProbeAcceptedCount_ == 0))",
            train_units,
        )
        self.assertIn("if (zergSixthProbeRestorationActive) ++zergSixthProbeRestorationActiveFrames_;", train_units)
        self.assertNotIn("getAllUnits()", train_units)

    def test_same_callback_second_zealot_marks_provisional_block(self):
        self.assertIn(
            "if (zergSecondZealotProbeReserveBlockFrames_[index] == secondZealotTrainFrame_)\n"
            "                                    zergSecondZealotProbeReserveBlockPreAcceptFlags_[index] = 0;",
            self.source,
        )

    def test_v43_to_v44_patch_is_present(self):
        patch = PATCH.read_text()
        self.assertIn("zergSixthProbeRestorationActive", patch)
        self.assertIn("zerg_sixth_probe_accepted_frame", patch)
        self.assertIn("zerg_post_pylon_pre_second_gateway_probe_train_count", patch)


if __name__ == "__main__":
    unittest.main()
