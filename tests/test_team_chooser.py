"""Tests for games.team_chooser module."""

import os
import tempfile
import unittest
from games.team_chooser import split_into_teams, load_lines


class TestSplitIntoTeams(unittest.TestCase):
    def test_all_players_assigned(self):
        players = ["A", "B", "C", "D", "E", "F"]
        teams = split_into_teams(players)
        assigned = [p for team in teams for p in team]
        self.assertEqual(sorted(assigned), sorted(players))

    def test_default_two_teams(self):
        players = ["A", "B", "C", "D"]
        teams = split_into_teams(players)
        self.assertEqual(len(teams), 2)

    def test_custom_num_teams(self):
        players = ["A", "B", "C", "D", "E", "F"]
        teams = split_into_teams(players, num_teams=3)
        self.assertEqual(len(teams), 3)

    def test_no_player_lost(self):
        players = ["Alice", "Bob", "Charlie"]
        teams = split_into_teams(players)
        assigned = [p for team in teams for p in team]
        self.assertEqual(sorted(assigned), sorted(players))

    def test_empty_players(self):
        teams = split_into_teams([])
        self.assertEqual(teams, [[], []])

    def test_single_player(self):
        teams = split_into_teams(["Solo"])
        assigned = [p for team in teams for p in team]
        self.assertEqual(assigned, ["Solo"])

    def test_original_list_not_mutated(self):
        original = ["A", "B", "C", "D"]
        copy = list(original)
        split_into_teams(original)
        self.assertEqual(original, copy)

    def test_teams_are_balanced(self):
        """With even count, both teams should have equal size."""
        players = ["A", "B", "C", "D", "E", "F"]
        teams = split_into_teams(players)
        sizes = [len(t) for t in teams]
        self.assertEqual(max(sizes) - min(sizes), 0)

    def test_odd_count_teams_off_by_one(self):
        """With odd count, team sizes should differ by at most 1."""
        players = ["A", "B", "C", "D", "E"]
        teams = split_into_teams(players)
        sizes = [len(t) for t in teams]
        self.assertLessEqual(max(sizes) - min(sizes), 1)


class TestLoadLines(unittest.TestCase):
    def test_load_non_empty_lines(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write("Alice\nBob\n\nCharlie\n\n")
            tmp_path = tmp.name
        try:
            lines = load_lines(tmp_path)
            self.assertEqual(lines, ["Alice", "Bob", "Charlie"])
        finally:
            os.unlink(tmp_path)

    def test_load_empty_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write("\n\n")
            tmp_path = tmp.name
        try:
            lines = load_lines(tmp_path)
            self.assertEqual(lines, [])
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
