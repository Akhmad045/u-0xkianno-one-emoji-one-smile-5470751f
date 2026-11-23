#!/usr/bin/env python3
"""One Emoji, One Smile — make.fun entry.

Writes exactly one emoji to /output/entry.txt: the one most likely to make
a stranger smile.

Chosen emoji: 🫶 (U+1FAF6 HEART HANDS)
  - Warm at first glance: two hands forming a heart, a small gesture of
    kindness sent with no words needed.
  - Universal: a heart is read the same way by a stranger of any age or
    background, with no irony, in-joke or language barrier.
  - Chosen, not default: not the first smiley that comes to mind, yet
    instantly readable on a phone screen.
  - Right for a stranger: affectionate without intimacy, sarcasm or
    flirtation — a friendly gesture, not a hug or a wink.

Standard library only, no network, deterministic.
"""

import os
import unicodedata

EMOJI = "\U0001faf6"  # 🫶 HEART HANDS
OUTPUT_PATH = "/output/entry.txt"


def is_emoji(char: str) -> bool:
    """True when a single character is an emoji presentation character."""
    if len(char) != 1:
        return False
    # 🫶 is category So (Symbol, other); emoji presentation characters
    # live in So (and a few in Sk). Require a symbol, not a letter/mark.
    return unicodedata.category(char) in ("So", "Sk")


def gate_check(text: str) -> None:
    """Enforce the competition gate on the entry text."""
    # Must be UTF-8 text.
    text.encode("utf-8")
    # Gate: 1 to 8 characters, not only whitespace.
    assert 1 <= len(text) <= 8, f"entry must be 1-8 chars, got {len(text)}"
    assert text.strip(), "entry must not be only whitespace"
    # Exactly one emoji: a single non-whitespace character, and it must
    # be an emoji character.
    non_space = [c for c in text if not c.isspace()]
    assert len(non_space) == 1, (
        f"entry must contain exactly one emoji, got {len(non_space)} "
        "non-whitespace characters"
    )
    assert is_emoji(non_space[0]), (
        f"entry character {non_space[0]!r} is not an emoji"
    )


def main() -> None:
    text = EMOJI + "\n"
    gate_check(text)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Verify the round trip: read back exactly what was written.
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        written = f.read()
    assert written == text, "round-trip mismatch"
    gate_check(written)
    print(f"Wrote {OUTPUT_PATH}: {EMOJI!r} ({len(EMOJI)} character)")


if __name__ == "__main__":
    main()
