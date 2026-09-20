import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "third_party/kestrel-opening-v43-candidate/Kestrel.cpp"
V42_SOURCE = ROOT / "third_party/kestrel-opening-v42-candidate/Kestrel.cpp"
PATCH = ROOT / "patches/kestrel-v42-to-v43-second-zealot-reserve.patch"


class KestrelV43CandidateTest(unittest.TestCase):
    def setUp(self):
        self.source = SOURCE.read_text()
        self.v42 = V42_SOURCE.read_text()

    def test_candidate_is_v42_plus_second_zealot_probe_reserve(self):
        self.assertNotEqual(self.source, self.v42)
        self.assertIn("else if (acceptedZealotTrains_ < 2) openingReserve = 100;", self.source)
        self.assertNotIn("else if (!firstZealotQueued_) openingReserve = 100;", self.source)
        self.assertIn("knownZerg_ && secondGatewayCurrentFrame_ >= 0 && acceptedZealotTrains_ < 2", self.source)
        self.assertIn("second_zealot_train_frame", self.source)
        self.assertIn("zerg_second_zealot_probe_reserve_block_frames", self.source)
        self.assertIn("zerg_second_zealot_probe_reserve_block_minerals", self.source)
        self.assertIn("zerg_second_zealot_probe_reserve_block_count", self.source)
        self.assertIn("acceptedZealotTrains_ == 2", self.source)

    def test_reserve_is_public_zerg_self_state_and_non_zerg_gated(self):
        train_units = self.source[self.source.index("    void trainUnits()") : self.source.index("    void constructOpening()")]
        self.assertIn("knownZerg_ && secondGatewayCurrentFrame_ >= 0", train_units)
        self.assertIn("minerals >= 50 && minerals < 150", train_units)
        self.assertNotIn("getAllUnits()", train_units)

    def test_v42_to_v43_patch_is_present_and_single_policy_change_is_named(self):
        patch = PATCH.read_text()
        self.assertIn("acceptedZealotTrains_ < 2", patch)
        self.assertIn("second_zealot_train_frame", patch)
        self.assertIn("zerg_second_zealot_probe_reserve_block_count", patch)


if __name__ == "__main__":
    unittest.main()
