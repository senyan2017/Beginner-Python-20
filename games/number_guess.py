"""Number-guessing game core logic."""

import random

DEFAULT_LOW = 0
DEFAULT_HIGH = 100

# Result constants returned by evaluate_guess()
TOO_LOW = "too_low"
TOO_HIGH = "too_high"
CORRECT = "correct"


def pick_secret(low=DEFAULT_LOW, high=DEFAULT_HIGH):
    """Return a random secret number in [low, high]."""
    return random.randint(low, high)


def evaluate_guess(guess, secret):
    """Compare *guess* to *secret* and return a result constant.

    Returns one of TOO_LOW, TOO_HIGH, or CORRECT.
    """
    if guess < secret:
        return TOO_LOW
    if guess > secret:
        return TOO_HIGH
    return CORRECT


def result_message(result):
    """Return a human-readable message for a guess result."""
    messages = {
        TOO_LOW: "It's lower than the actual number. Try Again.",
        TOO_HIGH: "It's higher than the actual number. Try Again.",
        CORRECT: "Bravo, You Got It!",
    }
    return messages[result]
