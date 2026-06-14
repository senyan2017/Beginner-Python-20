import os
import random
from random import choice  # kept for the original standalone feel

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_PLAYERS_FILE = os.path.join(_BASE_DIR, "team-chooser-using-files", "players.txt")
_TEAMS_FILE = os.path.join(_BASE_DIR, "team-chooser-using-files", "teams.txt")

# Fallback roster used when no custom list is given and the data files are missing.
DEFAULT_PLAYERS = ['Sam', 'John', 'Mark', 'Elon', 'Joy', 'Tim', 'Rony', 'Chan']
DEFAULT_TEAMS = ['Python', 'Java', 'Ruby', 'Javascript', 'Hadoop', 'Kotlin']


def _read_lines(path):
    """Return non-empty stripped lines from a file, or [] if it can't be read."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh.read().splitlines() if line.strip()]
    except OSError:
        return []


def default_players():
    """Default roster: prefer players.txt (file version), else the built-in list."""
    return _read_lines(_PLAYERS_FILE) or list(DEFAULT_PLAYERS)


def default_teams():
    """Default team labels: prefer teams.txt, else the built-in list."""
    return _read_lines(_TEAMS_FILE) or list(DEFAULT_TEAMS)


def choose_teams(players=None, teams=None, print_fn=print, rng=random):
    """Split ``players`` randomly into Team A and Team B; return an outcome string.

    ``players``/``teams`` default to the shared roster (file-backed, with a
    built-in fallback), which unifies the old file and non-file variants into a
    single entry point. The caller's list is never mutated.
    """
    if not players:
        players = default_players()
    if not teams:
        teams = default_teams()

    print_fn('\nPlayers: ', players)
    print_fn('Teams: ', teams)

    teamA = []
    teamB = []
    pool = list(players)  # copy so we don't mutate the caller's list

    while len(pool) > 0:
        playerA = rng.choice(pool)
        teamA.append(playerA)
        pool.remove(playerA)

        if not pool:
            break

        playerB = rng.choice(pool)
        teamB.append(playerB)
        pool.remove(playerB)

    print_fn('\nTeam A: ', teamA)
    print_fn('Team B: ', teamB)

    return "Team A: {} vs Team B: {}".format(teamA, teamB)


if __name__ == "__main__":
    choose_teams()
