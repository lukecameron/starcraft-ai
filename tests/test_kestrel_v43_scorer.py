import unittest

from scripts import score_kestrel_hillclimb as scorer


class KestrelV43ScorerTest(unittest.TestCase):
    @staticmethod
    def metadata(known_zerg=True):
        return {
            "known_zerg": known_zerg,
            "accepted_zealot_trains": 2 if known_zerg else 0,
            "second_gateway_current_frame": 100 if known_zerg else -1,
            "second_zealot_train_frame": 160 if known_zerg else -1,
            "zerg_second_zealot_probe_reserve_active_frames": 10 if known_zerg else 0,
            "zerg_second_zealot_probe_reserve_block_frames": [120, 130] if known_zerg else [],
            "zerg_second_zealot_probe_reserve_block_minerals": [100, 140] if known_zerg else [],
            "zerg_second_zealot_probe_reserve_block_count": 2 if known_zerg else 0,
            "zerg_second_zealot_probe_reserve": 100,
        }

    def test_v43_generation_and_reserve_mechanism_pass(self):
        metadata = self.metadata()
        self.assertEqual(scorer._candidate_generation("Kestrel-v43-second-zealot-reserve"), "v43")
        self.assertEqual(scorer._diagnostic_generation(metadata), "v43")
        summary = scorer._v43_treatment_summary(metadata, "Zerg")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertEqual(summary["second_zealot_train_frame"], 160)
        self.assertEqual(summary["reserve_block_count"], 2)

    def test_v43_rejects_misaligned_or_malformed_reserve_evidence(self):
        metadata = self.metadata()
        metadata["zerg_second_zealot_probe_reserve_block_minerals"] = [100]
        summary = scorer._v43_treatment_summary(metadata, "Zerg")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("reserve_trace_length_mismatch", summary["review_flags"])

        metadata = self.metadata()
        metadata["zerg_second_zealot_probe_reserve_active_frames"] = 0
        summary = scorer._v43_treatment_summary(metadata, "Zerg")
        self.assertIn("zerg_second_zealot_probe_reserve_active_frames_not_positive", summary["review_flags"])

    def test_v43_non_zerg_reserve_is_inactive(self):
        summary = scorer._v43_treatment_summary(self.metadata(False), "Terran")
        self.assertEqual(summary["quantitative_grade"]["grade"], "pass")
        self.assertTrue(summary["checks"]["non_zerg_inactive"])

    def test_v43_requires_retained_v42_treatment(self):
        metadata = self.metadata()
        metadata.update({
            "accepted_probe_train_frames": [],
            "probe_reserve_block_frames": [],
            "probe_reserve_block_minerals": [],
            "opening_probe_reserve": 0,
            "max_opening_probe_reserve": 250,
            "first_probe_reserve_window_frame": 10,
            "probe_reserve_window_end_frame": 100,
            "probe_reserve_block_count": 0,
            "zerg_five_probe_policy_active_frames": 5,
            "zerg_five_probe_pylon_accepted": True,
            "zerg_five_probe_pylon_accepted_frame": 10,
            "first_pylon_accepted_frame": 10,
        })
        del metadata["zerg_five_probe_pylon_accepted_frame"]
        summary = scorer._probe_reserve_summary(metadata, "Zerg", "v43")
        self.assertEqual(summary["quantitative_grade"]["grade"], "review")
        self.assertIn("v43:retained_v42:zerg_five_probe_pylon_accepted_frame_missing", summary["review_flags"])

        metadata = self.metadata()
        metadata["second_zealot_train_frame"] = 90
        self.assertIn(
            "second_zealot_train_before_second_gateway",
            scorer._v43_treatment_summary(metadata, "Zerg")["review_flags"],
        )


if __name__ == "__main__":
    unittest.main()
