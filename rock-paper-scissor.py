#!/usr/bin/env python3
"""Rock-Paper-Scissors — command-line entry point."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from games.rps import (
    computer_move,
    judge,
    outcome_message,
    MOVE_NAMES,
    VALID_MOVES,
)
from games.utils import get_choice


def main():
    """Run a single round of Rock-Paper-Scissors."""
    prompt = "rock (r), paper (p) or scissors (s)? "
    player = get_choice(prompt, VALID_MOVES)
    computer = computer_move()

    print(f"{MOVE_NAMES[player]} vs {MOVE_NAMES[computer]}")
    result = judge(player, computer)
    print(outcome_message(result))


if __name__ == "__main__":
    main()
