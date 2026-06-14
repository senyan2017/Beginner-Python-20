"""Dice-rolling core logic."""

import random

# Default die faces
DEFAULT_MIN = 1
DEFAULT_MAX = 6


def roll_die(min_val=DEFAULT_MIN, max_val=DEFAULT_MAX):
    """Return a single random die roll in [min_val, max_val]."""
    return random.randint(min_val, max_val)


def roll_dice(count=1, min_val=DEFAULT_MIN, max_val=DEFAULT_MAX):
    """Return a list of *count* random die rolls."""
    return [roll_die(min_val, max_val) for _ in range(count)]
