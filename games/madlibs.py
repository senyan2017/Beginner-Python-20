"""Mad-libs story generation core logic."""

STORY_TEMPLATE = (
    "{programmer} went to attend an interview at {company} for the first time.\n"
    "He knows well to code in {language1}.\n"
    "{recruiter}, the HR says that \"we need a {language2} developer, so You can go home\"."
)

PROMPTS = [
    ("programmer", "Someone's Name"),
    ("company", "A Company Name"),
    ("language1", "A Programming Language"),
    ("recruiter", "Someone Else's Name"),
    ("language2", "Another Programming Language"),
]


def collect_words(prompts=None):
    """Collect user input for each prompt; returns a dict of key -> value."""
    prompts = prompts or PROMPTS
    words = {}
    for key, label in prompts:
        words[key] = input(f"{label}: ")
    return words


def build_story(words, template=None):
    """Fill *template* with *words* dict and return the resulting string."""
    template = template or STORY_TEMPLATE
    return template.format(**words)
