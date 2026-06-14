#!/usr/bin/env python3
"""Number-guessing game — command-line entry point."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from games.number_guess import (
    pick_secret,
    evaluate_guess,
    result_message,
    CORRECT,
    DEFAULT_LOW,
    DEFAULT_HIGH,
)
from games.utils import get_int_in_range


def main():
    """Run the number-guessing game loop."""
    print("Welcome to Number Guess")
    secret = pick_secret()

    while True:
        guess = get_int_in_range(
            f"Please input a number between {DEFAULT_LOW} and {DEFAULT_HIGH}: ",
            DEFAULT_LOW,
            DEFAULT_HIGH,
        )
        result = evaluate_guess(guess, secret)
        print(result_message(result))
        if result == CORRECT:
            break

    print("Thank You for Playing Number Guess. See You Again")


if __name__ == "__main__":
    main()
