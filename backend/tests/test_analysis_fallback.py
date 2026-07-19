import unittest
from unittest.mock import patch

from app.main import normalize_analysis


class AnalysisFallbackTests(unittest.TestCase):
    def test_normalize_analysis_uses_demo_defaults_when_raw_is_none(self):
        analysis = normalize_analysis(None, "cut on arm")

        self.assertEqual(analysis["severity"], "Moderate")
        self.assertTrue(analysis["demo_mode"])
        self.assertIn("first_aid", analysis)
        self.assertIn("red_flags", analysis)


if __name__ == "__main__":
    unittest.main()
