"""Tests for games.dice module."""

import unittest
from games.dice import roll_die, roll_dice, DEFAULT_MIN, DEFAULT_MAX


class TestRollDie(unittest.TestCase):
    def test_result_in_range(self):
        for _ in range(100):
            value = roll_die()
            self.assertGreaterEqual(value, DEFAULT_MIN)
            self.assertLessEqual(value, DEFAULT_MAX)

    def test_custom_range(self):
        for _ in range(100):
            value = roll_die(10, 20)
            self.assertGreaterEqual(value, 10)
            self.assertLessEqual(value, 20)


class TestRollDice(unittest.TestCase):
    def test_correct_count(self):
        results = roll_dice(count=5)
        self.assertEqual(len(results), 5)

    def test_default_count_is_one(self):
        results = roll_dice()
        self.assertEqual(len(results), 1)

    def test_all_in_range(self):
        results = roll_dice(count=50)
        for v in results:
            self.assertGreaterEqual(v, DEFAULT_MIN)
            self.assertLessEqual(v, DEFAULT_MAX)


if __name__ == "__main__":
    unittest.main()
