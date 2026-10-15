import unittest

from matcher import analyze_match


class MatcherTests(unittest.TestCase):
    def test_counts_coverage_and_missing_skills(self):
        result = analyze_match("Python and JavaScript", "Need Python, JavaScript, and SQL")
        self.assertEqual(result["matched"], ["javascript", "python"])
        self.assertEqual(result["missing"], ["sql"])
        self.assertEqual(result["score"], 66.7)

    def test_alias_is_normalized(self):
        result = analyze_match("I build with JS", "JavaScript experience required")
        self.assertIn("javascript", result["matched"])

    def test_whole_word_does_not_match_substrings(self):
        result = analyze_match("My skill is C++", "C is required")
        self.assertEqual(result["matched"], [])

    def test_no_known_skills_has_no_score(self):
        result = analyze_match("some text", "communication and curiosity")
        self.assertIsNone(result["score"])
        self.assertEqual(result["job_skills"], [])


if __name__ == "__main__":
    unittest.main()
