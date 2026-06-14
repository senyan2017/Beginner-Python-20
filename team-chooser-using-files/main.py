#!/usr/bin/env python3
"""Team chooser (file-based) — command-line entry point.

Reads players and team names from players.txt and teams.txt located in
the same directory as this script.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from games.team_chooser import split_into_teams, load_lines


def main():
    """Load players/teams from files and display the random split."""
    here = os.path.dirname(os.path.abspath(__file__))

    players = load_lines(os.path.join(here, "players.txt"))
    teams = load_lines(os.path.join(here, "teams.txt"))

    print("\nPlayers: ", players)
    print("Teams:   ", teams)

    result = split_into_teams(players)
    print("\nTeam A: ", result[0])
    print("Team B: ", result[1])


if __name__ == "__main__":
    main()
