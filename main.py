"""One Word, One Username, One Reward.

Writes the entrant's own make.fun username -- sunny-stork-42 -- and
nothing else to <MAKEFUN_OUTPUT_DIR>/entry.txt (default
/output/entry.txt). One word, at most 30 characters, no trailing
newline.

The entry:

    sunny-stork-42

Why this word (reasoning, kept here and in the README; the entry
itself is just the username, as the brief requires):

* It is the account's own make.fun username, exactly as the brief
  demands: one word, no explanation, no links, no pitch.
* "sunny-stork" is an odd, memorable pairing -- a cheerful bird that
  delivers babies, wearing sunshine -- where most usernames are a
  name plus a number. The incongruity is the whole joke, and it
  survives being read cold: sunny + stork is funny before you know
  anything about the account.
* The "-42" is the answer to everything, which gives the judge a
  second smile on the re-read: the bird is sunny, and the number is
  the universe's punchline.

Standard library only. Deterministic: no randomness, no network, no
clock.
"""

import hashlib
import os

TEXT = "sunny-stork-42"

MAX_CHARS = 30

# sha256 of the exact bytes main.py must write to entry.txt, measured
# from a verified run. The read-back step asserts the file's digest
# equals this value, so any drift in the written bytes fails loudly.
EXPECTED_SHA256 = (
    "8e53f702937e427cbbabbd022423fbeb8b872711d364f11487395b83bfd47f83"
)


def validate_text(value) -> str:
    """Guard: value must be a single non-blank word of 1..30 chars.

    Accepts either the text string or the raw bytes read back from the
    entry file, so the same check covers the pre-write guard and the
    post-write read-back verification. Returns the text as a str, or
    raises AssertionError with a clear message.
    """
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    assert 1 <= len(value) <= MAX_CHARS, (
        f"entry.txt must be 1..{MAX_CHARS} characters, got {len(value)}"
    )
    assert value.strip(), "entry.txt must not be only whitespace"
    assert len(value.split()) == 1, "entry.txt must be exactly one word"
    assert "\n" not in value and "\r" not in value, (
        "entry.txt must be a single line"
    )
    return value


def main() -> None:
    # Pre-write guard: refuse to write anything outside the gate.
    validate_text(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(TEXT)
    # Read-back validation: the gate is 1..30 characters, so the file
    # must hold exactly the text we intended to write.
    with open(path, "rb") as f:
        data = f.read()
    assert validate_text(data) == TEXT
    # Digest verification: the written bytes must hash to the digest
    # measured from the verified run, proving no drift or stray bytes.
    digest = hashlib.sha256(data).hexdigest()
    assert digest == EXPECTED_SHA256, (
        f"entry.txt sha256 mismatch: got {digest}, "
        f"expected {EXPECTED_SHA256}"
    )
    print(TEXT)
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
