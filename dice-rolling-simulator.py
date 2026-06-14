# importing module for random number generation
import random

# range of the values of a dice
min_val = 1
max_val = 6


def play_dice(input_fn=input, print_fn=print, rng=random):
    """Roll a die repeatedly until the player declines, return an outcome string.

    Defaults reproduce the original standalone "roll again" loop. ``input_fn`` /
    ``print_fn`` / ``rng`` are injectable so the launcher and tests can drive it.
    """
    rolls = []
    # loop
    while True:
        print_fn("Rolling The Dices...")
        print_fn("The Values are :")

        # generating and printing random integer from 1 to 6
        dice = rng.randint(min_val, max_val)
        print_fn(dice)
        rolls.append(dice)

        try:
            roll_again = input_fn("Roll again? (y/n): ").strip().lower()
        except EOFError:
            # No more input (e.g. piped run): stop gracefully instead of crashing.
            roll_again = 'n'
        if roll_again != 'y':
            print_fn("Thanks for playing!")
            break

    return "Rolled " + ", ".join(str(r) for r in rolls)


if __name__ == "__main__":
    play_dice()
