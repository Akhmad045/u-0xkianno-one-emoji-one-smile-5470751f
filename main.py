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

Choice reconsidered on second pass against the obvious alternatives:
  - U+1F60A 😊 smiling face with smiling eyes: the warmest plain smiley,
    but it is the default pick and loses on "chosen rather than default".
  - U+1F917 🤗 hugging face: warm and playful, but a hug from a stranger
    can read as too intimate (criterion 5).
  - U+1F970 🥰 smiling face with hearts: warm, but the hearts risk
    reading as flirtation from someone unknown.
  🫶 keeps the warmth while staying clearly chosen and stranger-safe, and
  as a single code point it cannot be mistaken for a multi-character
  sequence. It is also unlikely to duplicate one of the house's fixed
  anchor texts, which tend to be plain smileys.

Standard library only, no network, deterministic.
"""

import os
import unicodedata

EMOJI = "\U0001faf6"  # 🫶 HEART HANDS
OUTPUT_PATH = "/output/entry.txt"

# Unicode blocks that hold emoji presentation characters (single code
# points). U+1FAF6 sits in Symbols and Pictographs Extended-A.
EMOJI_RANGES = (
    (0x00A9, 0x00AE),      # © ®
    (0x203C, 0x203C),      # ‼
    (0x2049, 0x2049),      # ⁉
    (0x2122, 0x2122),      # ™
    (0x2139, 0x2139),      # ℹ
    (0x2194, 0x2199),      # ↔ ↕ ↖ ↗ ↘ ↙
    (0x21A9, 0x21AA),      # ↩ ↪
    (0x231A, 0x231B),      # ⌚ ⌛
    (0x2328, 0x2328),      # ⌨
    (0x2388, 0x2388),      # ⎈
    (0x23CF, 0x23CF),      # ⏏
    (0x23E9, 0x23F3),      # ⏩ ⏪ ⏫ ⏬ ⏭ ⏮ ⏯ ⏰ ⏱ ⏲ ⏳
    (0x23F8, 0x23FA),      # ⏸ ⏹ ⏺
    (0x24C2, 0x24C2),      # Ⓜ
    (0x25AA, 0x25AB),      # ▪ ▫
    (0x25B6, 0x25B6),      # ▶
    (0x25C0, 0x25C0),      # ◀
    (0x25FB, 0x25FE),      # ◻ ◼ ◽ ◾
    (0x2600, 0x26FF),      # ☀ … ⛿ Misc Symbols
    (0x2700, 0x27BF),      # ✀ … ➿ Dingbats
    (0x2934, 0x2935),      # ⤴ ⤵
    (0x2B05, 0x2B07),      # ⬅ ⬆ ⬇
    (0x2B1B, 0x2B1C),      # ⬛ ⬜
    (0x2B50, 0x2B50),      # ⭐
    (0x2B55, 0x2B55),      # ⭕
    (0x3030, 0x3030),      # 〰
    (0x303D, 0x303D),      # 〽
    (0x3297, 0x3297),      # ㊗
    (0x3299, 0x3299),      # ㊙
    (0x1F000, 0x1FAFF),    # Mahjong … Symbols and Pictographs Extended-A
)

# Characters that would turn one code point into a multi-code-point
# grapheme (ZWJ sequences, keycaps, skin tones, variation selectors).
GRAPHEME_JOINERS = frozenset(
    ["\u200d", "\ufe0e", "\ufe0f", "\u20e3"]
    + [chr(c) for c in range(0x1F3FB, 0x1F400)]
)


def is_emoji(char: str) -> bool:
    """True when a single character is an emoji presentation character."""
    if len(char) != 1:
        return False
    code = ord(char)
    if not any(lo <= code <= hi for lo, hi in EMOJI_RANGES):
        return False
    # Emoji presentation characters are symbols, not letters or marks.
    return unicodedata.category(char) in ("So", "Sk")


def gate_check(text: str) -> None:
    """Enforce the competition gate on the entry text."""
    # Must be UTF-8 text.
    encoded = text.encode("utf-8")
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
    # Single grapheme: no joiner, variation selector, keycap or skin tone.
    assert not any(c in GRAPHEME_JOINERS for c in text), (
        "entry must be a single emoji code point, not a sequence"
    )
    assert is_emoji(non_space[0]), (
        f"entry character {non_space[0]!r} is not an emoji"
    )
    # The entry file is the emoji plus one trailing newline: 5 bytes.
    assert encoded == (EMOJI + "\n").encode("utf-8"), (
        "entry file must be exactly the chosen emoji plus a newline"
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
