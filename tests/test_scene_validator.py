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

    def test_v2_fixture_covers_naming_assets_and_measured_budgets(self):
        report = validate_snapshot(load_snapshot(FIXTURES / "asset_validation_v2.json"))
        codes = {finding["code"] for finding in report["findings"]}
        self.assertTrue({
            "GENERIC_NAME", "NAMING_SYSTEM_UNKNOWN", "MISSING_REFERENCE",
            "TEXTURE_COLORSPACE_MISMATCH", "TEXTURE_MAX_SIZE_EXCEEDED",
            "LIGHTMAP_UV_MISSING", "MESH_TRIANGLE_BUDGET_EXCEEDED",
            "PERFORMANCE_BUDGET_EXCEEDED",
        }.issubset(codes))
        self.assertNotIn("INVALID_SCHEMA", codes)

    def test_v2_schema_rejects_negative_measured_values(self):
        report = validate_snapshot({
            "schema_version": 2,
            "metadata": {}, "settings": {}, "assets": {}, "objects": [],
            "performance": {"gpu_ms": -1},
        })
        self.assertIn("INVALID_SCHEMA", {finding["code"] for finding in report["findings"]})

    def test_unknown_schema_version_is_reported(self):
        report = validate_snapshot({"schema_version": 99, "metadata": {}, "settings": {}, "assets": {}, "objects": []})
        self.assertIn("UNSUPPORTED_SCHEMA_VERSION", {finding["code"] for finding in report["findings"]})

    def test_declared_naming_convention_is_enforced(self):
        report = validate_snapshot({
            "schema_version": 2, "metadata": {},
            "settings": {"naming_mode": "production", "naming_convention": "lowercase-kebab-case"},
            "assets": {}, "objects": [{"name": "Bad_Name", "type": "GameObject"}],
        })
        codes = {finding["code"] for finding in report["findings"]}
        self.assertIn("NAMING_CONVENTION_MISMATCH", codes)
        self.assertNotIn("NAMING_SYSTEM_UNKNOWN", codes)


if __name__ == "__main__":
    unittest.main()
