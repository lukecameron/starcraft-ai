import unittest

from scripts import score_kestrel_hillclimb as scorer


class KestrelV44ScorerTest(unittest.TestCase):
    @staticmethod
    def zerg_metadata():
        return {
            "known_zerg": True,
            "accepted_probe_train_frames": [120],
            "probe_reserve_block_frames": [20],
            "probe_reserve_block_minerals": [200],
            "opening_probe_reserve": 250,
            "max_opening_probe_reserve": 250,
            "first_probe_reserve_window_frame": 10,
            "probe_reserve_window_end_frame": 150,
            "probe_reserve_block_count": 1,
            "first_pylon_accepted_frame": 10,
            "second_gateway_current_frame": 150,
            "zerg_five_probe_policy_active_frames": 5,
            "zerg_five_probe_pylon_accepted": True,
            "zerg_five_probe_pylon_accepted_frame": 10,
            "accepted_zealot_trains": 2,
            "second_zealot_train_frame": 160,
            "zerg_second_zealot_probe_reserve_active_frames": 10,
            "zerg_second_zealot_probe_reserve_block_frames": [155],
            "zerg_second_zealot_probe_reserve_block_minerals": [100],
            "zerg_second_zealot_probe_reserve_block_pre_accept_flags": [1],
            "zerg_second_zealot_probe_reserve_block_count": 1,
            "zerg_second_zealot_probe_reserve": 100,
            "zerg_sixth_probe_restoration_active_frames": 5,
            "zerg_sixth_probe_accepted_frame": 120,
            "zerg_sixth_probe_accepted_count": 1,
            "zerg_post_pylon_pre_second_gateway_probe_train_count": 1,
        }

    def test_v44_generation_and_all_retained_treatments_pass(self):
        metadata = self.zerg_metadata()
        self.assertEqual(scorer._candidate_generation("Kestrel-v44-sixth-probe-restoration"), "v44")
        self.assertEqual(scorer._diagnostic_generation(metadata), "v44")
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v44")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertEqual(summary["v44_treatment"]["accepted_frame"], 120)
        self.assertEqual(summary["v44_treatment"]["pre_second_gateway_probe_train_count"], 1)
        self.assertEqual(summary["v42_treatment"]["quantitative_grade"]["grade"], "pass")
        self.assertEqual(summary["v43_treatment"]["quantitative_grade"]["grade"], "pass")

    def test_v44_requires_retained_fields_and_rejects_a_seventh_probe(self):
        metadata = self.zerg_metadata()
        del metadata["zerg_five_probe_pylon_accepted_frame"]
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v44")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("v44:retained_v42:zerg_five_probe_pylon_accepted_frame_missing", summary["review_flags"])

        metadata = self.zerg_metadata()
        del metadata["zerg_second_zealot_probe_reserve_block_count"]
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v44")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("v44:retained_v43:zerg_second_zealot_probe_reserve_block_count_missing", summary["review_flags"])

        metadata = self.zerg_metadata()
        metadata["zerg_post_pylon_pre_second_gateway_probe_train_count"] = 2
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v44")
        self.assertIn("v44:zerg_pre_second_gateway_probe_train_count_not_one", summary["review_flags"])

    def test_v44_non_zerg_restoration_is_inactive(self):
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
            "zerg_five_probe_policy_active_frames": 0,
            "zerg_five_probe_pylon_accepted": False,
            "zerg_five_probe_pylon_accepted_frame": -1,
            "accepted_zealot_trains": 0,
            "second_zealot_train_frame": -1,
            "zerg_second_zealot_probe_reserve_active_frames": 0,
            "zerg_second_zealot_probe_reserve_block_frames": [],
            "zerg_second_zealot_probe_reserve_block_minerals": [],
            "zerg_second_zealot_probe_reserve_block_pre_accept_flags": [],
            "zerg_second_zealot_probe_reserve_block_count": 0,
            "zerg_sixth_probe_restoration_active_frames": 0,
            "zerg_sixth_probe_accepted_frame": -1,
            "zerg_sixth_probe_accepted_count": 0,
            "zerg_post_pylon_pre_second_gateway_probe_train_count": 0,
        })
        summary = scorer._probe_reserve_summary(metadata, "Terran", "v44")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertTrue(summary["v44_treatment"]["checks"]["non_zerg_inactive"])

        metadata["zerg_sixth_probe_restoration_active_frames"] = 1
        summary = scorer._probe_reserve_summary(metadata, "Terran", "v44")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertFalse(summary["v44_treatment"]["checks"]["non_zerg_inactive"])

    def test_same_callback_block_is_provisional_and_excluded_from_post_acceptance_gate(self):
        metadata = self.zerg_metadata()
        metadata["zerg_second_zealot_probe_reserve_block_frames"] = [160]
        metadata["zerg_second_zealot_probe_reserve_block_minerals"] = [100]
        metadata["zerg_second_zealot_probe_reserve_block_pre_accept_flags"] = [0]
        summary = scorer._v43_treatment_summary(metadata, "Zerg", require_ordering=True)
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")

        metadata["zerg_second_zealot_probe_reserve_block_pre_accept_flags"] = [1]
        summary = scorer._v43_treatment_summary(metadata, "Zerg", require_ordering=True)
        self.assertIn("reserve_block_after_second_zealot", summary["review_flags"])

    def test_probe_train_strictly_between_gateway_and_second_zealot_is_rejected(self):
        metadata = self.zerg_metadata()
        metadata["accepted_probe_train_frames"] = [120, 155]
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v44")
        self.assertIn(
            "probe_train_strictly_between_second_gateway_and_second_zealot",
            summary["review_flags"],
        )
        self.assertFalse(summary["checks"]["probe_train_absence"])

        metadata["accepted_probe_train_frames"] = [120, 150, 160]
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v44")
        self.assertNotIn(
            "probe_train_strictly_between_second_gateway_and_second_zealot",
            summary["review_flags"],
        )
        self.assertTrue(summary["checks"]["probe_train_absence"])


if __name__ == "__main__":
    unittest.main()
