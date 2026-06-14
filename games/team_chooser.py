"""Team-chooser core logic -- unified for both hardcoded and file-based usage."""

import random


def split_into_teams(players, num_teams=2):
    """Randomly distribute *players* across *num_teams* teams.

    Players are drawn without replacement, round-robin style, until none
    remain.  Returns a list of lists (one per team).

    A *copy* of the input list is used so the caller's list is not mutated.
    """
    remaining = list(players)
    teams = [[] for _ in range(num_teams)]
    team_idx = 0

    while remaining:
        player = random.choice(remaining)
        remaining.remove(player)
        teams[team_idx].append(player)
        team_idx = (team_idx + 1) % num_teams

    return teams


def load_lines(filepath):
    """Read non-empty lines from a text file, using a context manager."""
    with open(filepath, "r", encoding="utf-8") as fh:
        return [line for line in fh.read().splitlines() if line.strip()]
