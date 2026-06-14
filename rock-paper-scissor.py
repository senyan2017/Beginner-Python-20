import random
from random import randint  # kept for backwards compatibility / standalone feel


def play_rock_paper_scissors(input_fn=input, print_fn=print, rng=random):
    """Play one round of rock-paper-scissors and return an outcome string.

    Defaults reproduce the original standalone behaviour; the parameters make it
    drivable by the launcher and the tests.
    """
    player = input_fn('rock (r), paper (p) or scissors (s)?')
    chosen = rng.randint(1, 3)

    if chosen == 1:
        computer = 'r'
    elif chosen == 2:
        computer = 'p'
    else:
        computer = 's'
    print_fn(player, 'vs', computer)

    # rock blunts scissors, paper covers rock, scissors cut paper
    player_wins = {('r', 's'), ('s', 'p'), ('p', 'r')}
    computer_wins = {('s', 'r'), ('p', 's'), ('r', 'p')}

    if player not in ('r', 'p', 's'):
        print_fn('Invalid input')
        return "Invalid input (you: {})".format(player)

    if player == computer:
        print_fn('DRAW!')
        result = "Draw"
    elif (player, computer) in player_wins:
        print_fn('Player Wins!')
        result = "Player Wins"
    elif (player, computer) in computer_wins:
        print_fn('Computer Wins!')
        result = "Computer Wins"
    else:  # pragma: no cover - all valid combinations are covered above
        print_fn('Invalid input')
        result = "Invalid input"

    return "{} (you: {}, cpu: {})".format(result, player, computer)


if __name__ == "__main__":
    play_rock_paper_scissors()
