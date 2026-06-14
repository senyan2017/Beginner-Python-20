"""Tests for games.rps module."""

import unittest
from games.rps import (
    judge,
    outcome_message,
    computer_move,
    ROCK,
    PAPER,
    SCISSORS,
    WIN,
    LOSE,
    DRAW,
    VALID_MOVES,
)


class TestJudge(unittest.TestCase):
    def test_rock_beats_scissors(self):
        self.assertEqual(judge(ROCK, SCISSORS), WIN)

    def test_scissors_loses_to_rock(self):
        self.assertEqual(judge(SCISSORS, ROCK), LOSE)

    def test_paper_beats_rock(self):
        self.assertEqual(judge(PAPER, ROCK), WIN)

    def test_rock_loses_to_paper(self):
        self.assertEqual(judge(ROCK, PAPER), LOSE)

    def test_scissors_beats_paper(self):
        self.assertEqual(judge(SCISSORS, PAPER), WIN)

    def test_paper_loses_to_scissors(self):
        self.assertEqual(judge(PAPER, SCISSORS), LOSE)

    def test_same_move_is_draw(self):
        for move in VALID_MOVES:
            self.assertEqual(judge(move, move), DRAW)

    def test_invalid_move_raises(self):
        with self.assertRaises(ValueError):
            judge("x", ROCK)
        with self.assertRaises(ValueError):
            judge(ROCK, "z")

    def test_all_six_combinations_covered(self):
        """Ensure every distinct (player, computer) pair resolves to WIN or LOSE."""
        outcomes = set()
        for p in VALID_MOVES:
            for c in VALID_MOVES:
                if p != c:
                    outcomes.add(judge(p, c))
        self.assertEqual(outcomes, {WIN, LOSE})


class TestComputerMove(unittest.TestCase):
    def test_returns_valid_move(self):
        for _ in range(50):
            self.assertIn(computer_move(), VALID_MOVES)


class TestOutcomeMessage(unittest.TestCase):
    def test_messages_exist(self):
        for result in (WIN, LOSE, DRAW):
            msg = outcome_message(result)
            self.assertIsInstance(msg, str)
            self.assertTrue(len(msg) > 0)


if __name__ == "__main__":
    unittest.main()
