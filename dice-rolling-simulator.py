#!/usr/bin/env python3
"""Dice-rolling simulator — command-line entry point."""

import sys
import os

# Ensure the project root is on sys.path so `games` is importable when
# this script is run directly (e.g. `python dice-rolling-simulator.py`).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from games.dice import roll_die, DEFAULT_MIN, DEFAULT_MAX


def main():
    """Run an interactive dice-rolling loop."""
    print("Welcome to the Dice Rolling Simulator!")
    print(f"Rolling a standard die ({DEFAULT_MIN}–{DEFAULT_MAX}).\n")

    while True:
        value = roll_die()
        print("Rolling The Dices...")
        print(f"The Value is: {value}")

        again = input("Roll again? (y/n): ").strip().lower()
        if again != "y":
            break

    print("Thanks for playing!")


if __name__ == "__main__":
    main()
