#!/usr/bin/env python3
"""Mad-libs story generator — command-line entry point."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from games.madlibs import collect_words, build_story
from games.utils import print_separator


def main():
    """Collect words from the user and print the generated story."""
    print("Welcome to Mad Libs! Enter the requested words:\n")
    words = collect_words()
    print_separator()
    print(build_story(words))


if __name__ == "__main__":
    main()
