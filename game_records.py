"""Local persistence + simple stats for the mini game hub.

Records are stored as a JSON list of entries::

    {"game": "Number Guess", "outcome": "Won in 4 tries", "time": "2026-06-14T10:00:00"}

Every file operation is defensive: a missing or corrupt history file never
crashes the caller, it simply behaves like an empty history.
"""

import json
import os
from datetime import datetime

# Anchor the history file next to this module so it is found no matter what the
# current working directory is when the hub (or a standalone script) runs.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(_BASE_DIR, ".game_history.json")


def load_records(path=DEFAULT_PATH):
    """Return the list of recorded games. Never raises.

    A missing file yields an empty list; a corrupt/unreadable file also yields
    an empty list (so a single bad write can't permanently break the menu).
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError, ValueError):
        # Corrupt or unreadable history: degrade to "no history" rather than crash.
        return []
    # Be tolerant of an unexpected shape on disk.
    if not isinstance(data, list):
        return []
    return [entry for entry in data if isinstance(entry, dict)]


def record_game(game, outcome, path=DEFAULT_PATH):
    """Append one play result to the history file.

    Returns the entry that was stored. Failures to write are swallowed (the
    return value still reflects what we tried to store) so a read-only disk
    doesn't take the whole program down mid-demo.
    """
    entry = {
        "game": str(game),
        "outcome": str(outcome),
        "time": datetime.now().isoformat(timespec="seconds"),
    }
    records = load_records(path)
    records.append(entry)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(records, fh, ensure_ascii=False, indent=2)
    except OSError:
        # Couldn't persist (e.g. read-only fs). Don't crash the caller.
        pass
    return entry


def _format_time(iso_string):
    """Render a stored ISO timestamp as 'YYYY-MM-DD HH:MM'. Falls back to raw."""
    try:
        return datetime.fromisoformat(iso_string).strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return str(iso_string)


def format_recent(limit=5, path=DEFAULT_PATH):
    """Return a human-readable block of the most recent plays (newest first)."""
    records = load_records(path)
    if not records:
        return "No games played yet."
    recent = records[-limit:][::-1]
    lines = []
    for entry in recent:
        when = _format_time(entry.get("time", ""))
        game = entry.get("game", "?")
        outcome = entry.get("outcome", "")
        lines.append("  [{}] {} - {}".format(when, game, outcome))
    return "\n".join(lines)


def last_summary(path=DEFAULT_PATH):
    """One-liner describing the most recent play, for the menu header."""
    records = load_records(path)
    if not records:
        return "No games played yet."
    last = records[-1]
    return "{} - {} ({})".format(
        last.get("game", "?"),
        last.get("outcome", ""),
        _format_time(last.get("time", "")),
    )


def format_stats(path=DEFAULT_PATH):
    """Return per-game counts plus each game's most recent outcome."""
    records = load_records(path)
    if not records:
        return "No games played yet."

    counts = {}
    last_outcome = {}
    for entry in records:
        game = entry.get("game", "?")
        counts[game] = counts.get(game, 0) + 1
        last_outcome[game] = entry.get("outcome", "")

    lines = ["Total games played: {}".format(len(records)), ""]
    for game in sorted(counts):
        lines.append(
            "  {}: {} time(s) | last: {}".format(
                game, counts[game], last_outcome[game]
            )
        )
    return "\n".join(lines)
