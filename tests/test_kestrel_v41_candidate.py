import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "third_party/kestrel-opening-v41-candidate/Kestrel.cpp"
V40_SOURCE = ROOT / "third_party/kestrel-opening-v40-candidate/Kestrel.cpp"
PATCH = ROOT / "patches/kestrel-v40-to-v41-zerg-two-gateway-bank.patch"


class KestrelV41CandidateTest(unittest.TestCase):
    def setUp(self):
        self.source = SOURCE.read_text()
        self.v40 = V40_SOURCE.read_text()

    def test_candidate_is_distinct_and_patch_records_the_single_policy_delta(self):
        self.assertNotEqual(self.source, self.v40)
        patch = PATCH.read_text()
        self.assertIn("kZergTwoGatewayProbeReserve = 250", self.source)
        self.assertIn("openingReserve = kZergTwoGatewayProbeReserve;", self.source)
        self.assertIn("openingReserve = 100;", self.source)
        self.assertIn("zerg_pre_pylon_probe_reserve_frames", self.source)
        self.assertNotIn("zerg_two_gateway_reserve_frames", self.source)
        self.assertIn("kZergTwoGatewayProbeReserve = 250", patch)
        self.assertNotIn("kZergTwoGatewayProbeReserve = 200", patch)

    def test_reserve_is_zerg_only_and_stops_at_second_gateway_current(self):
        train_units = self.source[self.source.index("    void trainUnits()") : self.source.index("    void constructOpening()")]
        early_policy = re.search(
            r"const bool zergPrePylonProbeReserve =\s*"
            r"knownZerg_ && completedProbes >= 6 && firstPylonCurrentFrame_ < 0;\s*"
            r"if \(zergPrePylonProbeReserve\) \{\s*"
            r"openingReserve = kZergTwoGatewayProbeReserve;",
            train_units,
        )
        self.assertIsNotNone(early_policy)
        self.assertIn("else if (knownZerg_ && firstPylonAcceptedFrame_ >= 0)", train_units)
        self.assertIn("else if (secondGatewayCurrentFrame_ < 0) openingReserve = 250;", train_units)
        self.assertIn("openingProbeReserve_ = knownZerg_ ? openingReserve : 0;", train_units)
        self.assertIn("if (zergPrePylonProbeReserve) ++zergPrePylonProbeReserveFrames_;", train_units)

    def test_policy_does_not_change_gateway_training_or_non_zerg_opening(self):
        train_units = self.source[self.source.index("    void trainUnits()") : self.source.index("    void constructOpening()")]
        opening = self.source[self.source.index("    void constructOpening()") : self.source.index("    void assignEconomy()")]
        self.assertIn("unit->train(BWAPI::UnitTypes::Protoss_Zealot)", train_units)
        self.assertIn("unit->train(BWAPI::UnitTypes::Protoss_Dragoon)", train_units)
        self.assertIn("if (!knownZerg_ && supplyUsed >= 26 && gateways < 2", opening)
        self.assertIn("if ((!knownZerg_ || acceptedZealotTrains_ >= 2)", opening)


if __name__ == "__main__":
    unittest.main()
