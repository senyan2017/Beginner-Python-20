"""Tests for games.number_guess module."""

import unittest
from games.number_guess import (
    evaluate_guess,
    result_message,
    pick_secret,
    TOO_LOW,
    TOO_HIGH,
    CORRECT,
    DEFAULT_LOW,
    DEFAULT_HIGH,
)


class TestEvaluateGuess(unittest.TestCase):
    def test_guess_too_low(self):
        self.assertEqual(evaluate_guess(3, 50), TOO_LOW)

    def test_guess_too_high(self):
        self.assertEqual(evaluate_guess(80, 50), TOO_HIGH)

    def test_guess_correct(self):
        self.assertEqual(evaluate_guess(50, 50), CORRECT)

    def test_boundary_low(self):
        self.assertEqual(evaluate_guess(0, 1), TOO_LOW)

    def test_boundary_high(self):
        self.assertEqual(evaluate_guess(100, 99), TOO_HIGH)


class TestResultMessage(unittest.TestCase):
    def test_messages_exist(self):
        for result in (TOO_LOW, TOO_HIGH, CORRECT):
            msg = result_message(result)
            self.assertIsInstance(msg, str)
            self.assertTrue(len(msg) > 0)


class TestPickSecret(unittest.TestCase):
    def test_in_default_range(self):
        for _ in range(100):
            s = pick_secret()
            self.assertGreaterEqual(s, DEFAULT_LOW)
            self.assertLessEqual(s, DEFAULT_HIGH)

    def test_custom_range(self):
        for _ in range(100):
            s = pick_secret(10, 15)
            self.assertGreaterEqual(s, 10)
            self.assertLessEqual(s, 15)


if __name__ == "__main__":
    unittest.main()
