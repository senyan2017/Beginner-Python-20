import random  # for random number generation

# game_records is optional for standalone use; the function works without it.


def play_number_guess(input_fn=input, print_fn=print, rng=random):
    """Run one round of Number Guess and return a short outcome string.

    The default arguments reproduce the original standalone behaviour exactly
    (same prompts, same random range). ``input_fn`` / ``print_fn`` / ``rng`` are
    injectable so the launcher and the tests can drive it deterministically.
    """
    rand_num = rng.randrange(0, 100)  # random number (0..99) to be guessed
    guessCheck = "wrong"  # for controlling the loop
    attempts = 0

    print_fn("Welcome to Number Guess")

    # loop
    while guessCheck == "wrong":
        raw = input_fn("Please input a number between 0 and 100:")
        # Guard against non-numeric input instead of crashing the whole program.
        try:
            user_input = int(raw)
        except (ValueError, TypeError):
            print_fn("That's not a whole number. Try Again.")
            continue

        attempts += 1

        # checks for the correctness of guess
        if user_input < rand_num:
            print_fn("Its Lower than actual number. Try Again.")
        elif user_input > rand_num:
            print_fn("Its Higher than actual number. Try Again.")
        else:
            print_fn("Bravo, You Got It!")
            guessCheck = "correct"  # terminate loop

    print_fn("Thank You for Playing Number Guess. See You Again")
    return "Won in {} tries (answer was {})".format(attempts, rand_num)


if __name__ == "__main__":
    play_number_guess()
