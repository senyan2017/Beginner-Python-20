import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


core = load_module(ROOT / 'team_chooser_core.py', 'team_chooser_core')


class TeamChooserCoreTests(unittest.TestCase):
    def test_split_even_players(self):
        team_a, team_b = core.split_into_teams(['a', 'b', 'c', 'd'])
        self.assertEqual(len(team_a), 2)
        self.assertEqual(len(team_b), 2)
        self.assertEqual(sorted(team_a + team_b), ['a', 'b', 'c', 'd'])

    def test_split_odd_players(self):
        players = ['a', 'b', 'c', 'd', 'e']
        team_a, team_b = core.split_into_teams(players)
        self.assertEqual(len(team_a), 3)
        self.assertEqual(len(team_b), 2)
        self.assertEqual(sorted(team_a + team_b), sorted(players))

    def test_split_does_not_mutate_input(self):
        players = ['a', 'b', 'c']
        core.split_into_teams(players)
        self.assertEqual(players, ['a', 'b', 'c'])

    def test_load_lines_ignores_blank_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / 'players.txt'
            file_path.write_text('Sam\n\nJohn\n  \nMark\n', encoding='utf-8')
            self.assertEqual(core.load_lines(file_path), ['Sam', 'John', 'Mark'])


class TeamChooserScriptsTests(unittest.TestCase):
    def run_script(self, script_path, cwd=None):
        return subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30,
        )

    def test_team_chooser_script_runs(self):
        result = self.run_script(ROOT / 'team-chooser.py')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Team A', result.stdout)
        self.assertIn('Team B', result.stdout)

    def test_file_based_script_runs_from_any_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_script(ROOT / 'team-chooser-using-files' / 'main.py', cwd=tmp)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Team A', result.stdout)
        self.assertIn('Team B', result.stdout)
        self.assertIn('Sam', result.stdout)


if __name__ == '__main__':
    unittest.main()
