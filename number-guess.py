import random  # for random number generation

LOW = 0
HIGH = 100


def parse_guess(raw):
    """Parse user input into an int. Return None if it is not a valid whole number."""
    try:
        return int(raw.strip())
    except (ValueError, AttributeError):
        return None


def compare(guess, target):
    """Return 'low', 'high' or 'correct' comparing guess to target."""
    if guess < target:
        return "low"
    if guess > target:
        return "high"
    return "correct"


def main():
    target = random.randint(LOW, HIGH)  # random number within range LOW..HIGH (inclusive)
    print("Welcome to Number Guess")

    while True:
        try:
            raw = input("Please input a number between {} and {}: ".format(LOW, HIGH))
        except EOFError:
            print("\nNo more input received. Goodbye!")
            return

        guess = parse_guess(raw)
        if guess is None:
            print("That is not a whole number. Please try again.")
            continue

        result = compare(guess, target)
        if result == "low":
            print("Its Lower than actual number. Try Again.")
        elif result == "high":
            print("Its Higher than actual number. Try Again.")
        else:
            print("Bravo, You Got It!")
            break

    print("Thank You for Playing Number Guess. See You Again")


if __name__ == "__main__":
    main()
