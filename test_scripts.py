"""
Regression tests for all project scripts.
Covers: syntax validity, rock-paper-scissor logic, input validation,
        file-based path resolution, and dice-rolling loop behavior.
"""
import ast
import os
import subprocess
import sys
import unittest

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable


class TestSyntaxValidity(unittest.TestCase):
    """All scripts must parse without syntax errors."""

    SCRIPTS = [
        'dice-rolling-simulator.py',
        'number-guess.py',
        'rock-paper-scissor.py',
        'team-chooser.py',
        'team-chooser-using-files/main.py',
        'madlibs-generator.py',
    ]

    def test_all_scripts_parse(self):
        for script in self.SCRIPTS:
            path = os.path.join(PROJECT_DIR, script)
            with self.subTest(script=script):
                with open(path, 'r') as f:
                    source = f.read()
                # ast.parse raises SyntaxError on invalid syntax
                ast.parse(source)


class TestRockPaperScissor(unittest.TestCase):
    """Verify all 9 outcome combinations are handled correctly."""

    def _run(self, player_input):
        result = subprocess.run(
            [PYTHON, os.path.join(PROJECT_DIR, 'rock-paper-scissor.py')],
            input=player_input + '\n',
            capture_output=True, text=True, timeout=5,
        )
        return result.stdout + result.stderr

    def test_rock_vs_scissors_player_wins(self):
        # computer randomly picks, but we can at least verify no crash
        out = self._run('r')
        self.assertIn('vs', out)

    def test_valid_inputs_no_crash(self):
        for inp in ('r', 'p', 's', 'R', 'P', 'S', ' r ', ' p '):
            with self.subTest(input=inp):
                out = self._run(inp)
                # should never traceback
                self.assertNotIn('Traceback', out)
                self.assertIn('vs', out)

    def test_invalid_input_handled(self):
        for inp in ('', 'x', 'rock', '123', 'q'):
            with self.subTest(input=inp):
                out = self._run(inp)
                self.assertNotIn('Traceback', out)
                self.assertIn('Invalid input', out)

    def test_all_nine_combinations_covered(self):
        """Verify source code covers all 9 game outcomes."""
        path = os.path.join(PROJECT_DIR, 'rock-paper-scissor.py')
        with open(path, 'r') as f:
            source = f.read()
        # Check the six distinct win/lose branches exist
        expected_pairs = [
            ("'r'", "'s'"),  # rock beats scissors
            ("'r'", "'p'"),  # rock loses to paper
            ("'p'", "'r'"),  # paper beats rock
            ("'p'", "'s'"),  # paper loses to scissors
            ("'s'", "'r'"),  # scissors loses to rock
            ("'s'", "'p'"),  # scissors beats paper
        ]
        for p, c in expected_pairs:
            with self.subTest(player=p, computer=c):
                self.assertIn(f'player == {p} and computer == {c}', source)
        # Draw is handled by player == computer (covers r-r, p-p, s-s)
        self.assertIn('player == computer', source)


class TestNumberGuess(unittest.TestCase):
    """Verify input validation and basic game flow."""

    def _run(self, inputs):
        # append 0..100 so the game always finds the answer and exits cleanly
        all_inputs = list(inputs) + list(range(101))
        input_str = '\n'.join(str(i) for i in all_inputs) + '\n'
        result = subprocess.run(
            [PYTHON, os.path.join(PROJECT_DIR, 'number-guess.py')],
            input=input_str,
            capture_output=True, text=True, timeout=10,
        )
        return result.stdout + result.stderr

    def test_empty_input_no_crash(self):
        out = self._run([''])
        self.assertNotIn('Traceback', out)
        self.assertIn('Invalid input', out)

    def test_letter_input_no_crash(self):
        out = self._run(['abc'])
        self.assertNotIn('Traceback', out)
        self.assertIn('Invalid input', out)

    def test_out_of_range_input(self):
        out = self._run(['-1', '101'])
        self.assertNotIn('Traceback', out)
        self.assertIn('Out of range', out)

    def test_correct_guess_ends_game(self):
        out = self._run([])
        self.assertNotIn('Traceback', out)
        self.assertIn('Bravo, You Got It!', out)


class TestDiceRolling(unittest.TestCase):
    """Verify dice script rolls and exits on 'n'."""

    def _run(self, inputs):
        input_str = '\n'.join(str(i) for i in inputs) + '\n'
        result = subprocess.run(
            [PYTHON, os.path.join(PROJECT_DIR, 'dice-rolling-simulator.py')],
            input=input_str,
            capture_output=True, text=True, timeout=5,
        )
        return result.stdout + result.stderr

    def test_single_roll_then_quit(self):
        out = self._run(['n'])
        self.assertNotIn('Traceback', out)
        self.assertIn('Rolling The Dices', out)
        self.assertIn('Thanks for playing', out)

    def test_multiple_rolls_then_quit(self):
        out = self._run(['y', 'y', 'n'])
        self.assertNotIn('Traceback', out)
        # "Rolling The Dices" should appear at least 3 times
        self.assertGreaterEqual(out.count('Rolling The Dices'), 3)

    def test_empty_input_stops(self):
        """Empty response (not 'y') should stop the loop."""
        out = self._run([''])
        self.assertNotIn('Traceback', out)
        self.assertIn('Thanks for playing', out)


class TestTeamChooser(unittest.TestCase):
    """Verify team-chooser.py runs without syntax errors."""

    def test_runs_cleanly(self):
        result = subprocess.run(
            [PYTHON, os.path.join(PROJECT_DIR, 'team-chooser.py')],
            capture_output=True, text=True, timeout=5,
        )
        output = result.stdout + result.stderr
        self.assertNotIn('Traceback', output)
        self.assertIn('Team A', output)
        self.assertIn('Team B', output)
        self.assertEqual(result.returncode, 0)


class TestTeamChooserUsingFiles(unittest.TestCase):
    """Verify file-based team chooser reads from script-relative paths."""

    def test_runs_from_project_dir(self):
        result = subprocess.run(
            [PYTHON, os.path.join(PROJECT_DIR, 'team-chooser-using-files', 'main.py')],
            capture_output=True, text=True, timeout=5,
            cwd=PROJECT_DIR,
        )
        output = result.stdout + result.stderr
        self.assertNotIn('Traceback', output)
        self.assertIn('Team A', output)
        self.assertEqual(result.returncode, 0)

    def test_runs_from_different_directory(self):
        """Must work when launched from a completely different directory."""
        result = subprocess.run(
            [PYTHON, os.path.join(PROJECT_DIR, 'team-chooser-using-files', 'main.py')],
            capture_output=True, text=True, timeout=5,
            cwd='/tmp',
        )
        output = result.stdout + result.stderr
        self.assertNotIn('Traceback', output)
        self.assertNotIn('FileNotFoundError', output)
        self.assertIn('Team A', output)
        # verify it actually read the player names from files
        self.assertIn('Sam', output)
        self.assertEqual(result.returncode, 0)

    def test_all_players_assigned(self):
        """Every player from players.txt should appear in Team A or Team B."""
        result = subprocess.run(
            [PYTHON, os.path.join(PROJECT_DIR, 'team-chooser-using-files', 'main.py')],
            capture_output=True, text=True, timeout=5,
            cwd='/tmp',
        )
        output = result.stdout
        # Read expected players from the file
        players_path = os.path.join(PROJECT_DIR, 'team-chooser-using-files', 'players.txt')
        with open(players_path) as f:
            expected_players = [line.strip() for line in f if line.strip()]
        for player in expected_players:
            with self.subTest(player=player):
                self.assertIn(player, output)


class TestMadlibs(unittest.TestCase):
    """Verify madlibs generator handles inputs including empty strings."""

    def test_normal_inputs(self):
        inputs = 'Alice\nGoogle\nPython\nBob\nJava\n'
        result = subprocess.run(
            [PYTHON, os.path.join(PROJECT_DIR, 'madlibs-generator.py')],
            input=inputs,
            capture_output=True, text=True, timeout=5,
        )
        output = result.stdout + result.stderr
        self.assertNotIn('Traceback', output)
        self.assertIn('Alice', output)
        self.assertEqual(result.returncode, 0)

    def test_empty_inputs_no_crash(self):
        inputs = '\n\n\n\n\n'
        result = subprocess.run(
            [PYTHON, os.path.join(PROJECT_DIR, 'madlibs-generator.py')],
            input=inputs,
            capture_output=True, text=True, timeout=5,
        )
        output = result.stdout + result.stderr
        self.assertNotIn('Traceback', output)
        self.assertEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
