"""Team chooser with a built-in (hardcoded) roster.

Run directly with ``python team-chooser.py``. The actual team-splitting rule
lives in ``team_chooser_core`` so it stays in sync with the file-based version.
"""

from team_chooser_core import split_into_teams

players = ['Sam', 'John', 'Mark', 'Elon', 'Joy', 'Tim', 'Rony', 'Chan']
teams = ['Python', 'Java', 'Ruby', 'Javascript', 'Hadoop', 'Kotlin']

print('\nPlayers: ', players)
print('Teams: ', teams)

team_a, team_b = split_into_teams(players)

print('\nTeam A: ', team_a)
print('Team B: ', team_b)
