"""Shared team-chooser logic.

This is the single source of truth for how players are split into teams and
how player/team rosters are loaded from files. Both entry points
(``team-chooser.py`` and ``team-chooser-using-files/main.py``) import from
here so the rules only ever need to change in one place.
"""

from random import choice


def split_into_teams(players, num_teams=2):
    """Randomly distribute ``players`` across ``num_teams`` teams.

    Players are drawn at random without replacement and handed out
    round-robin (team 0, team 1, ... team 0, ...) until none remain. With the
    default of two teams this reproduces the original "pick for A, pick for B"
    behaviour, including giving the first team the extra player when the number
    of players is odd.

    The caller's list is never mutated; a copy is used internally.

    Returns a list of ``num_teams`` lists (one per team).
    """
    remaining = list(players)
    teams = [[] for _ in range(num_teams)]
    index = 0

    while remaining:
        player = choice(remaining)
        remaining.remove(player)
        teams[index].append(player)
        index = (index + 1) % num_teams

    return teams


def load_lines(filepath):
    """Read non-empty, whitespace-stripped lines from a text file.

    Uses a context manager so the file handle is always closed, and skips
    blank lines so trailing/extra newlines never turn into empty entries.
    """
    with open(filepath, "r", encoding="utf-8") as handle:
        return [line for line in handle.read().splitlines() if line.strip()]
