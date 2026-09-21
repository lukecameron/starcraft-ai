import unittest

from scripts import score_kestrel_hillclimb as scorer


class KestrelV45ScorerTest(unittest.TestCase):
    @staticmethod
    def zerg_metadata():
        return {
            "known_zerg": True,
            "latency_frames": 6,
            "accepted_probe_train_frames": [220],
            "probe_reserve_block_frames": [155],
            "probe_reserve_block_minerals": [200],
            "opening_probe_reserve": 100,
            "max_opening_probe_reserve": 250,
            "first_probe_reserve_window_frame": 10,
            "probe_reserve_window_end_frame": 150,
            "probe_reserve_block_count": 1,
            "first_pylon_accepted_frame": 10,
            "second_gateway_current_frame": 150,
            "zerg_four_probe_policy_active_frames": 5,
            "zerg_four_probe_pylon_accepted": True,
            "zerg_four_probe_pylon_accepted_frame": 10,
            "zerg_four_probe_pylon_probe_count": 4,
            "accepted_zealot_trains": 2,
            "second_zealot_train_frame": 160,
            "second_zealot_completed_frame": 210,
            "zerg_second_zealot_probe_reserve_active_frames": 10,
            "zerg_second_zealot_probe_reserve_block_frames": [155],
            "zerg_second_zealot_probe_reserve_block_minerals": [100],
            "zerg_second_zealot_probe_reserve_block_pre_accept_flags": [1],
            "zerg_second_zealot_probe_reserve_block_count": 1,
            "zerg_second_zealot_probe_reserve": 100,
        }

    def test_v45_generation_and_all_opening_gates_pass(self):
        metadata = self.zerg_metadata()
        self.assertEqual(scorer._candidate_generation("Kestrel-v45-four-probe-pylon"), "v45")
        self.assertEqual(scorer._diagnostic_generation(metadata, "Kestrel-v45-four-probe-pylon"), "v45")
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v45")
        self.assertEqual(summary["generation"], "v45")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertEqual(summary["v45_treatment"]["pylon_probe_count"], 4)
        self.assertEqual(summary["v45_treatment"]["second_zealot_completed_frame"], 210)
        self.assertTrue(summary["checks"]["probe_train_absence"])

    def test_v45_rejects_pre_pylon_probe_and_non_four_pylon_acceptance(self):
        metadata = self.zerg_metadata()
        metadata["accepted_probe_train_frames"] = [9, 220]
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v45")
        self.assertIn("v45:zerg_pre_pylon_probe_train_accepted", summary["review_flags"])

        metadata = self.zerg_metadata()
        metadata["accepted_probe_train_frames"] = [10]
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v45")
        self.assertIn("v45:zerg_pre_pylon_probe_train_accepted", summary["review_flags"])

        metadata = self.zerg_metadata()
        metadata["zerg_four_probe_pylon_probe_count"] = 5
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v45")
        self.assertIn("v45:zerg_four_probe_pylon_probe_count_not_four", summary["review_flags"])

    def test_v45_rejects_strict_interval_probe_and_bad_completion_order(self):
        metadata = self.zerg_metadata()
        metadata["accepted_probe_train_frames"] = [155]
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v45")
        self.assertIn(
            "v45:zerg_probe_train_strictly_between_second_gateway_and_second_zealot",
            summary["review_flags"],
        )

        metadata = self.zerg_metadata()
        metadata["second_zealot_completed_frame"] = 159
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v45")
        self.assertIn("v45:zerg_second_zealot_completed_before_train", summary["review_flags"])

        metadata = self.zerg_metadata()
        metadata["second_zealot_completed_frame"] = 160
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v45")
        self.assertIn("v45:zerg_second_zealot_completed_before_train", summary["review_flags"])

    def test_v45_carries_v44_same_callback_flags_without_sixth_probe(self):
        metadata = self.zerg_metadata()
        metadata["zerg_second_zealot_probe_reserve_block_pre_accept_flags"] = [0]
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v45")
        self.assertIn("v45:retained_v43:reserve_block_provisional_frame_mismatch", summary["review_flags"])

        metadata = self.zerg_metadata()
        self.assertNotIn("zerg_sixth_probe_restoration_active_frames", metadata)
        self.assertIsNone(summary["v44_treatment"])

    def test_v45_non_zerg_treatment_is_inactive(self):
        metadata = self.zerg_metadata()
        metadata.update({
            "known_zerg": False,
            "accepted_probe_train_frames": [],
            "probe_reserve_block_frames": [],
            "probe_reserve_block_minerals": [],
            "opening_probe_reserve": 0,
            "max_opening_probe_reserve": 0,
            "first_probe_reserve_window_frame": -1,
            "probe_reserve_window_end_frame": -1,
            "probe_reserve_block_count": 0,
            "first_pylon_accepted_frame": -1,
            "second_gateway_current_frame": -1,
            "zerg_four_probe_policy_active_frames": 0,
            "zerg_four_probe_pylon_accepted": False,
            "zerg_four_probe_pylon_accepted_frame": -1,
            "zerg_four_probe_pylon_probe_count": -1,
            "accepted_zealot_trains": 0,
            "second_zealot_train_frame": -1,
            "second_zealot_completed_frame": -1,
            "zerg_second_zealot_probe_reserve_active_frames": 0,
            "zerg_second_zealot_probe_reserve_block_frames": [],
            "zerg_second_zealot_probe_reserve_block_minerals": [],
            "zerg_second_zealot_probe_reserve_block_pre_accept_flags": [],
            "zerg_second_zealot_probe_reserve_block_count": 0,
            "zerg_second_zealot_probe_reserve": 100,
        })
        summary = scorer._probe_reserve_summary(metadata, "Terran", "v45")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertTrue(summary["v45_treatment"]["checks"]["non_zerg_inactive"])

        metadata["zerg_four_probe_policy_active_frames"] = 1
        summary = scorer._probe_reserve_summary(metadata, "Terran", "v45")
        self.assertIn("v45:non_zerg_four_probe_policy_active_frames_nonzero", summary["review_flags"])


if __name__ == "__main__":
    unittest.main()
