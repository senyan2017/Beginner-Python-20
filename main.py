#!/usr/bin/env python3
"""
Unified Game Hub - Command-line entry point for all mini-games.
Supports: Number Guess, Rock-Paper-Scissors, Dice Rolling, Team Chooser
Features: Game history logging, statistics view, error handling
"""

import random
import json
import os
from datetime import datetime

HISTORY_FILE = 'game_history.json'

# ============================================================================
# History Management
# ============================================================================

def load_history():
    """Load game history from JSON file. Returns empty list if file doesn't exist."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load history file ({e}). Starting fresh.")
        return []

def save_history(history):
    """Save game history to JSON file with error handling."""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Warning: Could not save history ({e}). Game result not recorded.")

def log_game_result(game_name, result):
    """Log a game result with timestamp to history."""
    history = load_history()
    entry = {
        'game': game_name,
        'result': result,
        'timestamp': datetime.now().isoformat()
    }
    history.append(entry)
    save_history(history)

def show_statistics():
    """Display game statistics and recent history."""
    history = load_history()

    if not history:
        print("\n=== Game Statistics ===")
        print("No games played yet. Start playing to see statistics!")
        return

    # Calculate statistics per game
    stats = {}
    for entry in history:
        game = entry['game']
        if game not in stats:
            stats[game] = {'count': 0, 'last_result': None, 'last_played': None}
        stats[game]['count'] += 1
        stats[game]['last_result'] = entry['result']
        stats[game]['last_played'] = entry['timestamp']

    print("\n=== Game Statistics ===")
    print(f"Total games played: {len(history)}\n")

    for game, data in sorted(stats.items()):
        print(f"{game}:")
        print(f"  Times played: {data['count']}")
        print(f"  Last result: {data['last_result']}")
        last_played = datetime.fromisoformat(data['last_played'])
        print(f"  Last played: {last_played.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    # Show recent games (last 5)
    print("=== Recent Games ===")
    recent = history[-5:] if len(history) >= 5 else history
    for entry in reversed(recent):
        timestamp = datetime.fromisoformat(entry['timestamp'])
        print(f"{timestamp.strftime('%m-%d %H:%M')} - {entry['game']}: {entry['result']}")
    print()

# ============================================================================
# Game: Number Guess
# ============================================================================

def play_number_guess():
    """Number guessing game - guess a number between 0 and 100."""
    print("\n=== Number Guess ===")
    print("Welcome to Number Guess!")
    print("I'm thinking of a number between 0 and 100.\n")

    rand_num = random.randint(0, 100)
    attempts = 0
    max_attempts = 20

    while attempts < max_attempts:
        try:
            user_input = input(f"Attempt {attempts + 1}/{max_attempts} - Please input a number between 0 and 100: ")
            user_num = int(user_input)

            if user_num < 0 or user_num > 100:
                print("Please enter a number between 0 and 100.")
                continue

            attempts += 1

            if user_num < rand_num:
                print("It's lower than the actual number. Try again.")
            elif user_num > rand_num:
                print("It's higher than the actual number. Try again.")
            else:
                result = f"Won in {attempts} attempts"
                print(f"Bravo, You Got It! The number was {rand_num}.")
                print(f"You won in {attempts} attempt(s)!")
                log_game_result("Number Guess", result)
                return result

        except ValueError:
            print("Invalid input! Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nGame cancelled.")
            return "Cancelled"

    result = f"Lost (number was {rand_num})"
    print(f"\nGame Over! You've used all {max_attempts} attempts.")
    print(f"The number was {rand_num}.")
    log_game_result("Number Guess", result)
    return result

# ============================================================================
# Game: Rock Paper Scissors
# ============================================================================

def play_rock_paper_scissors():
    """Rock-Paper-Scissors game."""
    print("\n=== Rock Paper Scissors ===")
    print("Choose your move:")
    print("  r - Rock")
    print("  p - Paper")
    print("  s - Scissors\n")

    valid_moves = {'r': 'Rock', 'p': 'Paper', 's': 'Scissors'}

    try:
        player = input("Your choice (r/p/s): ").strip().lower()

        if player not in valid_moves:
            print("Invalid input! Please use r, p, or s.")
            return "Invalid input"

        # Computer's random choice
        computer = random.choice(['r', 'p', 's'])

        print(f"\nYou chose: {valid_moves[player]}")
        print(f"Computer chose: {valid_moves[computer]}")
        print(f"{valid_moves[player]} vs {valid_moves[computer]}")

        # Determine winner
        if player == computer:
            result = "Draw"
            print("It's a DRAW!")
        elif (player == 'r' and computer == 's') or \
             (player == 'p' and computer == 'r') or \
             (player == 's' and computer == 'p'):
            result = "Win"
            print("You Win!")
        else:
            result = "Loss"
            print("Computer Wins!")

        log_game_result("Rock Paper Scissors", result)
        return result

    except KeyboardInterrupt:
        print("\nGame cancelled.")
        return "Cancelled"

# ============================================================================
# Game: Dice Rolling
# ============================================================================

def play_dice_rolling():
    """Dice rolling simulator."""
    print("\n=== Dice Rolling ===")
    print("Rolling the dice...\n")

    min_val = 1
    max_val = 6

    try:
        while True:
            dice = random.randint(min_val, max_val)
            print(f"You rolled: {dice}")

            roll_again = input("Roll again? (y/n): ").strip().lower()
            if roll_again != 'y':
                result = f"Last roll: {dice}"
                print("Thanks for playing!")
                log_game_result("Dice Rolling", result)
                return result

    except KeyboardInterrupt:
        print("\nGame cancelled.")
        return "Cancelled"

# ============================================================================
# Game: Team Chooser
# ============================================================================

def play_team_chooser():
    """Team chooser with default or custom player list."""
    print("\n=== Team Chooser ===")
    print("How would you like to choose teams?")
    print("  1. Use default player list")
    print("  2. Enter custom player names")
    print("  3. Load from file (players.txt)")

    try:
        choice = input("\nYour choice (1/2/3): ").strip()

        if choice == '1':
            players = ['Sam', 'John', 'Mark', 'Elon', 'Joy', 'Tim', 'Rony', 'Chan']
            print(f"\nUsing default players: {players}")

        elif choice == '2':
            print("\nEnter player names (comma-separated, e.g., Alice,Bob,Charlie):")
            user_input = input("Players: ").strip()
            if not user_input:
                print("No players entered. Using default list.")
                players = ['Sam', 'John', 'Mark', 'Elon', 'Joy', 'Tim', 'Rony', 'Chan']
            else:
                players = [p.strip() for p in user_input.split(',') if p.strip()]
                if len(players) < 2:
                    print("Need at least 2 players. Using default list.")
                    players = ['Sam', 'John', 'Mark', 'Elon', 'Joy', 'Tim', 'Rony', 'Chan']
                else:
                    print(f"\nUsing custom players: {players}")

        elif choice == '3':
            # Try to load from team-chooser-using-files directory
            file_path = 'team-chooser-using-files/players.txt'
            if not os.path.exists(file_path):
                file_path = 'players.txt'

            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        players = [line.strip() for line in f if line.strip()]
                    print(f"\nLoaded from file: {players}")
                except IOError as e:
                    print(f"Error reading file: {e}. Using default list.")
                    players = ['Sam', 'John', 'Mark', 'Elon', 'Joy', 'Tim', 'Rony', 'Chan']
            else:
                print("players.txt not found. Using default list.")
                players = ['Sam', 'John', 'Mark', 'Elon', 'Joy', 'Tim', 'Rony', 'Chan']

        else:
            print("Invalid choice. Using default list.")
            players = ['Sam', 'John', 'Mark', 'Elon', 'Joy', 'Tim', 'Rony', 'Chan']

        # Shuffle and divide into teams
        random.shuffle(players)
        team_a = players[::2]  # Even indices
        team_b = players[1::2]  # Odd indices

        print(f"\n{'='*30}")
        print(f"Team A ({len(team_a)} players):")
        for player in team_a:
            print(f"  - {player}")
        print(f"\nTeam B ({len(team_b)} players):")
        for player in team_b:
            print(f"  - {player}")
        print(f"{'='*30}")

        result = f"Team A: {len(team_a)}, Team B: {len(team_b)}"
        log_game_result("Team Chooser", result)
        return result

    except KeyboardInterrupt:
        print("\nGame cancelled.")
        return "Cancelled"

# ============================================================================
# Main Menu
# ============================================================================

def show_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("         Unified Game Hub")
    print("="*50)
    print("1. Number Guess")
    print("2. Rock Paper Scissors")
    print("3. Dice Rolling")
    print("4. Team Chooser")
    print("5. View Statistics")
    print("6. Exit")
    print("="*50)

def main():
    """Main entry point - runs the unified game hub."""
    print("Welcome to the Unified Game Hub!")

    while True:
        show_menu()

        try:
            choice = input("\nEnter your choice (1-6): ").strip()

            if choice == '1':
                play_number_guess()
            elif choice == '2':
                play_rock_paper_scissors()
            elif choice == '3':
                play_dice_rolling()
            elif choice == '4':
                play_team_chooser()
            elif choice == '5':
                show_statistics()
            elif choice == '6':
                print("\nThanks for playing! Goodbye!")
                break
            else:
                print("\nInvalid choice! Please enter a number between 1 and 6.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Please try again.")

if __name__ == '__main__':
    main()
