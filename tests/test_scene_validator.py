import unittest
from pathlib import Path

from tools.scene_validator import load_snapshot, validate_snapshot


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "fixtures"


class SceneValidatorTests(unittest.TestCase):
    def test_problematic_fixture_reports_expected_risks(self):
        report = validate_snapshot(load_snapshot(FIXTURES / "scene_problematic.json"))
        codes = {finding["code"] for finding in report["findings"]}

        self.assertEqual(report["status"], "fail")
        self.assertTrue(
            {
                "MISSING_REFERENCE",
                "GPU_INSTANCING_RECOMMENDED",
                "SRP_BATCHER_INCOMPATIBLE",
                "PARTICLE_OVERDRAW_RISK",
                "UNEXPECTED_SCENE_PAYLOAD",
            }.issubset(codes)
        )

    def test_clean_fixture_has_no_warnings_or_errors(self):
        report = validate_snapshot(load_snapshot(FIXTURES / "scene_clean.json"))

        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["summary"]["errors"], 0)
        self.assertEqual(report["summary"]["warnings"], 0)

    def test_report_contains_actionable_fields(self):
        report = validate_snapshot(load_snapshot(FIXTURES / "scene_problematic.json"))

        for finding in report["findings"]:
            self.assertTrue(finding["location"])
            self.assertTrue(finding["evidence"])
            self.assertTrue(finding["recommendation"])


if __name__ == "__main__":
    unittest.main()
