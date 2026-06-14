from pathlib import Path
from random import choice


def load_lines(path):
    with Path(path).open('r', encoding='utf-8') as handle:
        return [line.strip() for line in handle if line.strip()]


def split_into_teams(players):
    pool = list(players)
    team_a = []
    team_b = []

    while pool:
        player_a = choice(pool)
        team_a.append(player_a)
        pool.remove(player_a)

        if not pool:
            break

        player_b = choice(pool)
        team_b.append(player_b)
        pool.remove(player_b)

    return team_a, team_b
