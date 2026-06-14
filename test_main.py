#!/usr/bin/env python3
"""
Tests for the Unified Game Hub.
Covers: main menu, history logging/loading, team chooser, statistics, error handling.
"""

import unittest
import json
import os
import sys
from unittest.mock import patch
from io import StringIO

# Ensure the project root is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import main


class TestHistoryManagement(unittest.TestCase):
    """Test history loading, saving, and logging."""

    TEST_HISTORY_FILE = 'test_game_history.json'

    def setUp(self):
        """Use a test-specific history file."""
        main.HISTORY_FILE = self.TEST_HISTORY_FILE
        if os.path.exists(self.TEST_HISTORY_FILE):
            os.remove(self.TEST_HISTORY_FILE)

    def tearDown(self):
        """Clean up test history file."""
        if os.path.exists(self.TEST_HISTORY_FILE):
            os.remove(self.TEST_HISTORY_FILE)

    def test_load_history_no_file(self):
        """load_history returns empty list when file doesn't exist."""
        result = main.load_history()
        self.assertEqual(result, [])

    def test_save_and_load_history(self):
        """save_history writes data that load_history can read back."""
        test_data = [{'game': 'Test', 'result': 'Win', 'timestamp': '2026-01-01T00:00:00'}]
        main.save_history(test_data)
        result = main.load_history()
        self.assertEqual(result, test_data)

    def test_load_history_corrupted_file(self):
        """load_history returns empty list for corrupted JSON."""
        with open(self.TEST_HISTORY_FILE, 'w') as f:
            f.write("{corrupted json")
        result = main.load_history()
        self.assertEqual(result, [])

    def test_log_game_result(self):
        """log_game_result appends a properly structured entry."""
        main.log_game_result("TestGame", "Win")
        history = main.load_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['game'], 'TestGame')
        self.assertEqual(history[0]['result'], 'Win')
        self.assertIn('timestamp', history[0])

    def test_log_multiple_results(self):
        """Multiple log_game_result calls accumulate correctly."""
        main.log_game_result("Game1", "Win")
        main.log_game_result("Game2", "Loss")
        main.log_game_result("Game1", "Draw")
        history = main.load_history()
        self.assertEqual(len(history), 3)

    def test_save_history_io_error(self):
        """save_history handles IOError gracefully (no crash)."""
        main.HISTORY_FILE = '/nonexistent_dir/history.json'
        # Should not raise
        main.save_history([{'game': 'Test', 'result': 'Win', 'timestamp': '2026-01-01'}])
        main.HISTORY_FILE = self.TEST_HISTORY_FILE


class TestShowStatistics(unittest.TestCase):
    """Test statistics display."""

    TEST_HISTORY_FILE = 'test_stats_history.json'

    def setUp(self):
        main.HISTORY_FILE = self.TEST_HISTORY_FILE
        if os.path.exists(self.TEST_HISTORY_FILE):
            os.remove(self.TEST_HISTORY_FILE)

    def tearDown(self):
        if os.path.exists(self.TEST_HISTORY_FILE):
            os.remove(self.TEST_HISTORY_FILE)

    def test_statistics_empty(self):
        """show_statistics handles empty history gracefully."""
        captured = StringIO()
        sys.stdout = captured
        main.show_statistics()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("No games played yet", output)

    def test_statistics_with_data(self):
        """show_statistics displays game counts and recent games."""
        history = [
            {'game': 'Number Guess', 'result': 'Won in 5 attempts', 'timestamp': '2026-06-14T10:00:00'},
            {'game': 'Rock Paper Scissors', 'result': 'Win', 'timestamp': '2026-06-14T10:05:00'},
            {'game': 'Number Guess', 'result': 'Lost (number was 42)', 'timestamp': '2026-06-14T10:10:00'},
        ]
        main.save_history(history)

        captured = StringIO()
        sys.stdout = captured
        main.show_statistics()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()

        self.assertIn("Total games played: 3", output)
        self.assertIn("Number Guess", output)
        self.assertIn("Times played: 2", output)
        self.assertIn("Rock Paper Scissors", output)
        self.assertIn("Recent Games", output)


class TestMainMenu(unittest.TestCase):
    """Test main menu navigation."""

    def setUp(self):
        main.HISTORY_FILE = 'test_menu_history.json'
        if os.path.exists(main.HISTORY_FILE):
            os.remove(main.HISTORY_FILE)

    def tearDown(self):
        if os.path.exists(main.HISTORY_FILE):
            os.remove(main.HISTORY_FILE)

    @patch('builtins.input', side_effect=['6'])
    def test_exit_immediately(self, mock_input):
        """Selecting option 6 exits the main loop."""
        captured = StringIO()
        sys.stdout = captured
        main.main()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("Goodbye", output)

    @patch('builtins.input', side_effect=['7', '6'])
    def test_invalid_choice_then_exit(self, mock_input):
        """Invalid choice shows error, then exit works."""
        captured = StringIO()
        sys.stdout = captured
        main.main()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("Invalid choice", output)

    @patch('builtins.input', side_effect=['5', '6'])
    def test_view_statistics_then_exit(self, mock_input):
        """Statistics option works from menu."""
        captured = StringIO()
        sys.stdout = captured
        main.main()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("Statistics", output)


class TestNumberGuess(unittest.TestCase):
    """Test number guessing game."""

    def setUp(self):
        main.HISTORY_FILE = 'test_guess_history.json'
        if os.path.exists(main.HISTORY_FILE):
            os.remove(main.HISTORY_FILE)

    def tearDown(self):
        if os.path.exists(main.HISTORY_FILE):
            os.remove(main.HISTORY_FILE)

    @patch('builtins.input', side_effect=['50', '25', '42'])
    @patch('random.randint', return_value=42)
    def test_guess_game_flow(self, mock_randint, mock_input):
        """Number guess handles lower/higher hints and correct guess."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_number_guess()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        # 50 > 42 -> "higher", 25 < 42 -> "lower", 42 == 42 -> correct
        self.assertIn("higher", output.lower())
        self.assertIn("lower", output.lower())
        self.assertIn("bravo", output.lower())
        self.assertIn("Won in 3 attempts", result)

    @patch('builtins.input', side_effect=['abc'])
    def test_guess_invalid_input(self, mock_input):
        """Number guess handles non-integer input gracefully."""
        captured = StringIO()
        sys.stdout = captured
        # Should not crash, but will ask again. Patch to give one bad input then quit
        with patch('builtins.input', side_effect=['abc', KeyboardInterrupt]):
            try:
                main.play_number_guess()
            except StopIteration:
                pass
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("Invalid input", output)

    @patch('builtins.input', side_effect=['42'])
    @patch('random.randint', return_value=42)
    def test_guess_correct(self, mock_randint, mock_input):
        """Correct guess logs win result."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_number_guess()
        sys.stdout = sys.__stdout__
        self.assertIn("Won in 1 attempts", result)

        history = main.load_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['game'], 'Number Guess')


class TestRockPaperScissors(unittest.TestCase):
    """Test rock-paper-scissors game."""

    def setUp(self):
        main.HISTORY_FILE = 'test_rps_history.json'
        if os.path.exists(main.HISTORY_FILE):
            os.remove(main.HISTORY_FILE)

    def tearDown(self):
        if os.path.exists(main.HISTORY_FILE):
            os.remove(main.HISTORY_FILE)

    @patch('builtins.input', return_value='r')
    @patch('random.choice', return_value='s')
    def test_player_wins(self, mock_choice, mock_input):
        """Player rock beats computer scissors."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_rock_paper_scissors()
        sys.stdout = sys.__stdout__
        self.assertEqual(result, "Win")

    @patch('builtins.input', return_value='r')
    @patch('random.choice', return_value='r')
    def test_draw(self, mock_choice, mock_input):
        """Same move results in draw."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_rock_paper_scissors()
        sys.stdout = sys.__stdout__
        self.assertEqual(result, "Draw")

    @patch('builtins.input', return_value='x')
    def test_invalid_input(self, mock_input):
        """Invalid move returns 'Invalid input'."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_rock_paper_scissors()
        sys.stdout = sys.__stdout__
        self.assertEqual(result, "Invalid input")


class TestTeamChooser(unittest.TestCase):
    """Test team chooser with all input modes."""

    def setUp(self):
        main.HISTORY_FILE = 'test_team_history.json'
        if os.path.exists(main.HISTORY_FILE):
            os.remove(main.HISTORY_FILE)

    def tearDown(self):
        if os.path.exists(main.HISTORY_FILE):
            os.remove(main.HISTORY_FILE)

    @patch('builtins.input', side_effect=['1'])
    def test_default_players(self, mock_input):
        """Option 1 uses default player list and divides into two teams."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_team_chooser()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()

        self.assertIn("Team A", output)
        self.assertIn("Team B", output)
        self.assertIn("default", output.lower())
        self.assertIn("Team A:", result)

        history = main.load_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['game'], 'Team Chooser')

    @patch('builtins.input', side_effect=['2', 'Alice,Bob,Charlie,Dave,Eve,Frank'])
    def test_custom_players(self, mock_input):
        """Option 2 with comma-separated names creates custom teams."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_team_chooser()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()

        self.assertIn("Team A", output)
        self.assertIn("Team B", output)

    @patch('builtins.input', side_effect=['2', ''])
    def test_custom_players_empty_fallback(self, mock_input):
        """Empty custom input falls back to default list."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_team_chooser()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()

        self.assertIn("default", output.lower())

    @patch('builtins.input', side_effect=['2', 'Alice'])
    def test_custom_players_too_few(self, mock_input):
        """Single player input falls back to default list."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_team_chooser()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()

        self.assertIn("default", output.lower())

    @patch('builtins.input', side_effect=['9'])
    def test_invalid_choice_fallback(self, mock_input):
        """Invalid menu choice in team chooser falls back to default."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_team_chooser()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()

        self.assertIn("Team A", output)


class TestDiceRolling(unittest.TestCase):
    """Test dice rolling game."""

    def setUp(self):
        main.HISTORY_FILE = 'test_dice_history.json'
        if os.path.exists(main.HISTORY_FILE):
            os.remove(main.HISTORY_FILE)

    def tearDown(self):
        if os.path.exists(main.HISTORY_FILE):
            os.remove(main.HISTORY_FILE)

    @patch('builtins.input', side_effect=['n'])
    @patch('random.randint', return_value=4)
    def test_single_roll_then_quit(self, mock_randint, mock_input):
        """One roll then 'n' exits and logs result."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_dice_rolling()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()

        self.assertIn("4", output)
        self.assertIn("Last roll: 4", result)

        history = main.load_history()
        self.assertEqual(len(history), 1)

    @patch('builtins.input', side_effect=['y', 'y', 'n'])
    def test_multiple_rolls(self, mock_input):
        """Multiple rolls work until user says 'n'."""
        captured = StringIO()
        sys.stdout = captured
        result = main.play_dice_rolling()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()

        # Should have rolled 3 times
        self.assertEqual(output.count("You rolled"), 3)


if __name__ == '__main__':
    unittest.main()
