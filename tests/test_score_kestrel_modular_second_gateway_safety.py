import unittest

from scripts.score_kestrel_modular_second_gateway_safety import (
    validate_second_gateway_safety_evidence,
)


class SecondGatewaySafetyEvidenceTests(unittest.TestCase):
    def base(self):
        return {
            "known_zerg": True,
            "accepted_zealot_trains": 2,
            "second_zealot_completed_frame": 1600,
            "max_zealots": 2,
            "second_gateway_accepted_frame": -1,
            "lone_zealot_hold_release_frame": 1600,
        }

    def test_absent_second_gateway_is_censored_and_passes(self):
        issues, mechanism_issues = validate_second_gateway_safety_evidence(self.base())
        self.assertEqual(issues, [])
        self.assertEqual(mechanism_issues, [])

    def test_second_gateway_after_completion_passes(self):
        record = self.base()
        record["second_gateway_accepted_frame"] = 1600
        issues, mechanism_issues = validate_second_gateway_safety_evidence(record)
        self.assertEqual(issues, [])
        self.assertEqual(mechanism_issues, [])

    def test_second_gateway_before_completion_fails(self):
        record = self.base()
        record["second_gateway_accepted_frame"] = 1599
        issues, mechanism_issues = validate_second_gateway_safety_evidence(record)
        self.assertEqual(issues, [])
        self.assertIn(
            "second Gateway was accepted before the second Zealot completion",
            mechanism_issues,
        )

    def test_missing_completion_is_structural(self):
        record = self.base()
        record["second_zealot_completed_frame"] = None
        record["second_gateway_accepted_frame"] = 1700
        issues, mechanism_issues = validate_second_gateway_safety_evidence(record)
        self.assertIn("second_zealot_completed_frame is not an integer", issues)
        self.assertIn(
            "second Gateway acceptance is present without a valid completion frame",
            issues,
        )

    def test_overlap_is_required(self):
        record = self.base()
        record["max_zealots"] = 1
        issues, mechanism_issues = validate_second_gateway_safety_evidence(record)
        self.assertEqual(issues, [])
        self.assertIn("two completed Zealots did not overlap", mechanism_issues)


if __name__ == "__main__":
    unittest.main()
