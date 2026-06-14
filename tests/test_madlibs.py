"""Tests for games.madlibs module."""

import unittest
from games.madlibs import build_story, STORY_TEMPLATE


class TestBuildStory(unittest.TestCase):
    def test_all_placeholders_filled(self):
        words = {
            "programmer": "Alice",
            "company": "Acme",
            "language1": "Python",
            "recruiter": "Bob",
            "language2": "Java",
        }
        story = build_story(words)
        self.assertIn("Alice", story)
        self.assertIn("Acme", story)
        self.assertIn("Python", story)
        self.assertIn("Bob", story)
        self.assertIn("Java", story)

    def test_no_unfilled_braces(self):
        words = {
            "programmer": "X",
            "company": "Y",
            "language1": "Z",
            "recruiter": "W",
            "language2": "Q",
        }
        story = build_story(words)
        # After formatting, no {placeholder} should remain
        import re
        self.assertFalse(re.search(r"\{[a-z]+\}", story))

    def test_custom_template(self):
        template = "{a} met {b}."
        words = {"a": "Foo", "b": "Bar"}
        self.assertEqual(build_story(words, template), "Foo met Bar.")


if __name__ == "__main__":
    unittest.main()
