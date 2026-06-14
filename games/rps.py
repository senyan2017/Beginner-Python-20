"""Rock-Paper-Scissors core logic."""

import random

ROCK = "r"
PAPER = "p"
SCISSORS = "s"
VALID_MOVES = (ROCK, PAPER, SCISSORS)

WIN = "win"
LOSE = "lose"
DRAW = "draw"

_OUTCOMES = {
    (ROCK, SCISSORS): WIN,
    (ROCK, PAPER): LOSE,
    (PAPER, ROCK): WIN,
    (PAPER, SCISSORS): LOSE,
    (SCISSORS, PAPER): WIN,
    (SCISSORS, ROCK): LOSE,
}

MOVE_NAMES = {ROCK: "Rock", PAPER: "Paper", SCISSORS: "Scissors"}


def computer_move():
    """Return a random move for the computer."""
    return random.choice(VALID_MOVES)


def judge(player, computer):
    """Return the outcome (WIN / LOSE / DRAW) for the player."""
    if player not in VALID_MOVES or computer not in VALID_MOVES:
        raise ValueError(f"Invalid move: player={player!r}, computer={computer!r}")
    if player == computer:
        return DRAW
    return _OUTCOMES[(player, computer)]


def outcome_message(result):
    """Return a human-readable message for an outcome."""
    messages = {WIN: "Player Wins!", LOSE: "Computer Wins!", DRAW: "DRAW!"}
    return messages[result]
