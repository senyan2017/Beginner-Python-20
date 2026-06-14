#!/usr/bin/env python3
"""Team chooser (hardcoded names) — command-line entry point."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from games.team_chooser import split_into_teams

# Default rosters used when no file is supplied
DEFAULT_PLAYERS = ["Sam", "John", "Mark", "Elon", "Joy", "Tim", "Rony", "Chan"]
DEFAULT_TEAMS = ["Python", "Java", "Ruby", "Javascript", "Hadoop", "Kotlin"]


def main():
    """Split the default player list into two random teams."""
    print("\nPlayers: ", DEFAULT_PLAYERS)
    print("Teams:   ", DEFAULT_TEAMS)

    teams = split_into_teams(DEFAULT_PLAYERS)
    print("\nTeam A: ", teams[0])
    print("Team B: ", teams[1])


if __name__ == "__main__":
    main()
