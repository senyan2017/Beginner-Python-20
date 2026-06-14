# importing module for random number generation
import random

# range of the values of a single die
MIN_VAL = 1
MAX_VAL = 6
DICE_COUNT = 2  # "Rolling The Dice" -> roll two dice each round


def roll_die():
    """Return a single random die value between MIN_VAL and MAX_VAL (inclusive)."""
    return random.randint(MIN_VAL, MAX_VAL)


def roll_dice(count=DICE_COUNT):
    """Roll `count` dice and return the list of rolled values."""
    return [roll_die() for _ in range(count)]


def ask_roll_again():
    """Ask whether to roll again. Returns True only for an explicit yes."""
    try:
        answer = input("Roll again? (y/n): ").strip().lower()
    except EOFError:
        return False
    return answer in ("y", "yes")


def main():
    print("Welcome to the Dice Rolling Simulator")
    while True:
        print("\nRolling The Dice...")
        values = roll_dice()
        print("The Values are:", values)
        print("Total:", sum(values))
        if not ask_roll_again():
            break
    print("Thanks for rolling. See You Again")


if __name__ == "__main__":
    main()
