"""Shared utilities for input validation and display."""


def get_int_in_range(prompt, low, high):
    """Prompt the user until they enter an integer within [low, high]."""
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
        except ValueError:
            print(f"Please enter a valid integer.")
            continue
        if low <= value <= high:
            return value
        print(f"Please enter a number between {low} and {high}.")


def get_choice(prompt, valid_options):
    """Prompt the user until they enter one of *valid_options*."""
    while True:
        raw = input(prompt).strip()
        if raw in valid_options:
            return raw
        print(f"Invalid input. Choose from: {', '.join(valid_options)}")


def print_separator(char="-", width=60):
    """Print a horizontal separator line."""
    print(char * width)
