from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from team_chooser_core import load_lines, split_into_teams

BASE_DIR = Path(__file__).resolve().parent


def main():
    players = load_lines(BASE_DIR / 'players.txt')
    teams = load_lines(BASE_DIR / 'teams.txt')

    print('\nPlayers: ', players)
    print('Teams: ', teams)

    team_a, team_b = split_into_teams(players)

    print('\nTeam A: ', team_a)
    print('Team B: ', team_b)


if __name__ == '__main__':
    main()
