import os
from random import choice

# resolve file paths relative to this script's directory, not the working directory
script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, 'players.txt'), 'r') as f:
    players = [line.strip() for line in f if line.strip()]

with open(os.path.join(script_dir, 'teams.txt'), 'r') as f:
    teams = [line.strip() for line in f if line.strip()]

print('\nPlayers: ', players)
print('Teams: ', teams)

teamA = []
teamB = []

while len(players) > 0:
	playerA = choice(players)
	teamA.append(playerA)
	players.remove(playerA)

	if players == []:
		break

	playerB = choice(players)
	teamB.append(playerB)
	players.remove(playerB)

print('\nTeam A: ', teamA)
print('Team B: ', teamB)
