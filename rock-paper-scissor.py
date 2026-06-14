from random import randint

# Mapping from a choice to the choice it beats.
# rock (r) blunts scissors, paper (p) covers rock, scissors (s) cut paper
BEATS = {"r": "s", "p": "r", "s": "p"}
NAMES = {"r": "rock", "p": "paper", "s": "scissors"}
VALID = ("r", "p", "s")


def computer_choice():
    """Return a random valid choice for the computer."""
    return VALID[randint(0, len(VALID) - 1)]


def normalize(choice):
    """Normalize raw player input: strip surrounding spaces and lowercase it."""
    if not isinstance(choice, str):
        return choice
    return choice.strip().lower()


def decide_winner(player, computer):
    """Return 'draw', 'player' or 'computer' for two valid choices."""
    if player == computer:
        return "draw"
    if BEATS[player] == computer:
        return "player"
    return "computer"


def main():
    try:
        player = normalize(input("rock (r), paper (p) or scissors (s)? "))
    except EOFError:
        print("Invalid input")
        return

    if player not in VALID:
        print("Invalid input")
        return

    computer = computer_choice()
    print(NAMES[player], "vs", NAMES[computer])

    result = decide_winner(player, computer)
    if result == "draw":
        print("DRAW!")
    elif result == "player":
        print("Player Wins!")
    else:
        print("Computer Wins!")


if __name__ == "__main__":
    main()
