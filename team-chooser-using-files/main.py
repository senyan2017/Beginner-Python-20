from pathlib import Path
from random import choice

# Resolve data files relative to THIS script, not the current working directory,
# so the example works no matter where it is launched from.
BASE_DIR = Path(__file__).resolve().parent


def load_lines(filename):
    """Read non-empty, stripped lines from a file located next to this script."""
    path = BASE_DIR / filename
    with open(path, "r") as f:
        return [line.strip() for line in f.read().splitlines() if line.strip()]


def split_teams(players):
    """Split players into two teams by alternating random picks.

    Returns a (teamA, teamB) tuple. The input list is left unmodified.
    """
    pool = list(players)
    teamA = []
    teamB = []

    while pool:
        pick = choice(pool)
        teamA.append(pick)
        pool.remove(pick)

        if not pool:
            break

        pick = choice(pool)
        teamB.append(pick)
        pool.remove(pick)

    return teamA, teamB


def main():
    players = load_lines("players.txt")
    teams = load_lines("teams.txt")

    print("\nPlayers: ", players)
    print("Teams: ", teams)

    teamA, teamB = split_teams(players)

    print("\nTeam A: ", teamA)
    print("Team B: ", teamB)


if __name__ == "__main__":
    main()
