"""Regression tests for the beginner Python example scripts.

Run with:  python3 -m unittest discover -s tests -p "test_*.py"
       or:  python3 -m pytest tests/

These tests intentionally cover the non-happy paths that used to break:
illegal/empty input, boundary values, file reading from any directory, and
loop termination (subprocess calls use a timeout so a reintroduced infinite
loop fails the test instead of hanging).
"""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_module(filename, modname):
    """Import a script by file path (handles hyphenated, non-importable names)."""
    spec = importlib.util.spec_from_file_location(modname, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script(relpath, stdin_text="", cwd=None):
    """Run a script in a subprocess with the given stdin; 30s timeout guards loops."""
    return subprocess.run(
        [sys.executable, str(ROOT / relpath)],
        input=stdin_text,
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=30,
    )


# Load the importable logic once.
rps = load_module("rock-paper-scissor.py", "rps_mod")
guess = load_module("number-guess.py", "guess_mod")
dice = load_module("dice-rolling-simulator.py", "dice_mod")
teamfiles = load_module("team-chooser-using-files/main.py", "teamfiles_mod")


class RockPaperScissorLogic(unittest.TestCase):
    def test_draws(self):
        for c in ("r", "p", "s"):
            self.assertEqual(rps.decide_winner(c, c), "draw")

    def test_player_wins(self):
        # rock>scissors, paper>rock, scissors>paper
        for player, computer in (("r", "s"), ("p", "r"), ("s", "p")):
            self.assertEqual(rps.decide_winner(player, computer), "player")

    def test_computer_wins(self):
        # the previously-broken scissors cases are included here
        for player, computer in (("s", "r"), ("r", "p"), ("p", "s")):
            self.assertEqual(rps.decide_winner(player, computer), "computer")

    def test_full_truth_table_is_consistent(self):
        # Every one of the 9 combinations must resolve to exactly one result.
        for a in ("r", "p", "s"):
            for b in ("r", "p", "s"):
                self.assertIn(rps.decide_winner(a, b), ("draw", "player", "computer"))

    def test_normalize_case_and_spaces(self):
        self.assertEqual(rps.normalize("R "), "r")
        self.assertEqual(rps.normalize("  P"), "p")
        self.assertEqual(rps.normalize("S"), "s")
        self.assertEqual(rps.normalize("ROCK"), "rock")


class RockPaperScissorEndToEnd(unittest.TestCase):
    def test_valid_lowercase(self):
        r = run_script("rock-paper-scissor.py", "r\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("vs", r.stdout)

    def test_uppercase_is_accepted(self):
        r = run_script("rock-paper-scissor.py", "R\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("vs", r.stdout)
        self.assertNotIn("Invalid input", r.stdout)

    def test_invalid_input(self):
        r = run_script("rock-paper-scissor.py", "banana\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Invalid input", r.stdout)

    def test_empty_eof_does_not_crash(self):
        r = run_script("rock-paper-scissor.py", "")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Invalid input", r.stdout)


class NumberGuessLogic(unittest.TestCase):
    def test_parse_rejects_non_numbers(self):
        for bad in ("abc", "", "   ", "1.5", "12x"):
            self.assertIsNone(guess.parse_guess(bad))

    def test_parse_accepts_numbers(self):
        self.assertEqual(guess.parse_guess("5"), 5)
        self.assertEqual(guess.parse_guess(" 42 "), 42)
        self.assertEqual(guess.parse_guess("0"), 0)
        self.assertEqual(guess.parse_guess("100"), 100)
        self.assertEqual(guess.parse_guess("-3"), -3)

    def test_compare_boundaries(self):
        self.assertEqual(guess.compare(0, 0), "correct")
        self.assertEqual(guess.compare(100, 100), "correct")
        self.assertEqual(guess.compare(0, 100), "low")
        self.assertEqual(guess.compare(100, 0), "high")
        self.assertEqual(guess.compare(7, 7), "correct")


class NumberGuessEndToEnd(unittest.TestCase):
    def test_bad_input_then_sweep_terminates(self):
        # "abc" and "" exercise the illegal-input path; sweeping 0..100 guarantees
        # a correct guess regardless of the random target, so the loop must end.
        stdin = "abc\n\n" + "".join(f"{i}\n" for i in range(101))
        r = run_script("number-guess.py", stdin)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("That is not a whole number", r.stdout)
        self.assertIn("Bravo, You Got It!", r.stdout)

    def test_eof_does_not_crash(self):
        r = run_script("number-guess.py", "")
        self.assertEqual(r.returncode, 0, r.stderr)


class DiceLogic(unittest.TestCase):
    def test_single_die_in_range(self):
        for _ in range(200):
            self.assertIn(dice.roll_die(), range(1, 7))

    def test_roll_dice_count_and_range(self):
        values = dice.roll_dice()
        self.assertEqual(len(values), 2)
        for v in values:
            self.assertIn(v, range(1, 7))
        self.assertEqual(len(dice.roll_dice(5)), 5)


class DiceEndToEnd(unittest.TestCase):
    def test_rolls_again_then_stops(self):
        r = run_script("dice-rolling-simulator.py", "y\nn\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertGreaterEqual(r.stdout.count("Rolling The Dice"), 2)
        self.assertIn("The Values are:", r.stdout)

    def test_garbage_answer_stops_without_crash(self):
        r = run_script("dice-rolling-simulator.py", "maybe\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("The Values are:", r.stdout)

    def test_eof_stops(self):
        r = run_script("dice-rolling-simulator.py", "")
        self.assertEqual(r.returncode, 0, r.stderr)


class TeamChooserFiles(unittest.TestCase):
    def test_load_lines_reads_data(self):
        players = teamfiles.load_lines("players.txt")
        teams = teamfiles.load_lines("teams.txt")
        self.assertIn("Sam", players)
        self.assertIn("Python", teams)
        self.assertTrue(all(line.strip() for line in players))  # no blank entries

    def test_split_even(self):
        a, b = teamfiles.split_teams(["a", "b", "c", "d"])
        self.assertEqual(len(a), 2)
        self.assertEqual(len(b), 2)

    def test_split_odd_keeps_everyone_once(self):
        people = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        a, b = teamfiles.split_teams(people)
        self.assertEqual(len(a), 5)
        self.assertEqual(len(b), 4)
        self.assertEqual(sorted(a + b), sorted(people))  # everyone placed, no dupes

    def test_split_edge_cases(self):
        self.assertEqual(teamfiles.split_teams([]), ([], []))
        self.assertEqual(teamfiles.split_teams(["solo"]), (["solo"], []))

    def test_split_does_not_mutate_input(self):
        people = ["a", "b", "c"]
        teamfiles.split_teams(people)
        self.assertEqual(people, ["a", "b", "c"])

    def test_runs_from_any_directory(self):
        # The whole point of this example: launch from an unrelated CWD.
        with tempfile.TemporaryDirectory() as tmp:
            r = run_script("team-chooser-using-files/main.py", cwd=tmp)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Team A", r.stdout)
        self.assertIn("Sam", r.stdout)


class TeamChooserInline(unittest.TestCase):
    def test_runs_without_syntax_error(self):
        r = run_script("team-chooser.py")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Team A", r.stdout)
        self.assertIn("Team B", r.stdout)


if __name__ == "__main__":
    unittest.main()
