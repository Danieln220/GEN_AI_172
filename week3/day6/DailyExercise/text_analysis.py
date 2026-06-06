# ============================================================
#  Text Analysis — OOP, Modules, File Handling
# ============================================================
import string
import re
from collections import Counter


# ── Part I & II: Text Class ─────────────────────────────────
class Text:
    """Analyse a piece of text — from a string or a file."""

    # ── Step 1: Constructor ──────────────────────────────────
    def __init__(self, text):
        self.text = text

    # ── Step 2: word_frequency ───────────────────────────────
    def word_frequency(self, word):
        """Return how many times `word` appears in the text.
        Case-insensitive. Returns None if the word isn't found."""
        words = self.text.lower().split()
        count = words.count(word.lower())
        return count if count > 0 else None

    # ── Step 3: most_common_word ─────────────────────────────
    def most_common_word(self):
        """Return the single most-frequent word in the text."""
        words = self.text.lower().split()
        if not words:
            return None
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1          # build frequency dict
        return max(freq, key=freq.get)             # word with highest count

    # ── Step 4: unique_words ─────────────────────────────────
    def unique_words(self):
        """Return a sorted list of every distinct word in the text."""
        words = self.text.lower().split()
        return sorted(set(words))                  # set removes duplicates

    # ── Step 5: from_file class method ───────────────────────
    @classmethod
    def from_file(cls, file_path):
        """Create a Text instance from the contents of a file."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return cls(content)                        # same as Text(content)

    def __repr__(self):
        preview = self.text[:60].replace("\n", " ")
        return f'Text("{preview}{"..." if len(self.text) > 60 else ""}")'


# ── Bonus: TextModification Class ───────────────────────────
class TextModification(Text):
    """Extends Text with cleaning / normalisation methods."""

    # ── Step 7: remove_punctuation ───────────────────────────
    def remove_punctuation(self):
        """Strip all punctuation characters from the text."""
        # string.punctuation = !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        table = str.maketrans("", "", string.punctuation)
        return self.text.translate(table)

    # ── Step 8: remove_stop_words ────────────────────────────
    def remove_stop_words(self):
        """Remove common English stop words from the text."""
        stop_words = {
            "a", "an", "the", "and", "or", "but", "if", "in", "on",
            "at", "to", "for", "of", "with", "by", "from", "is", "was",
            "are", "were", "be", "been", "being", "have", "has", "had",
            "do", "does", "did", "will", "would", "could", "should",
            "may", "might", "shall", "can", "not", "no", "nor", "so",
            "yet", "both", "either", "neither", "as", "than", "that",
            "this", "these", "those", "it", "its", "i", "me", "my",
            "we", "our", "you", "your", "he", "she", "they", "them",
            "his", "her", "their", "what", "which", "who", "whom",
            "when", "where", "why", "how", "all", "each", "every",
            "any", "such", "into", "through", "during", "about", "up",
        }
        words = self.text.split()
        filtered = [w for w in words if w.lower() not in stop_words]
        return " ".join(filtered)

    # ── Step 9: remove_special_characters ────────────────────
    def remove_special_characters(self):
        """Keep only letters, digits, and whitespace."""
        return re.sub(r"[^a-zA-Z0-9\s]", "", self.text)


# ── Demo / test ──────────────────────────────────────────────
if __name__ == "__main__":

    sample = (
        "To be or not to be, that is the question. "
        "Whether 'tis nobler in the mind to suffer "
        "the slings and arrows of outrageous fortune, "
        "or to take arms against a sea of troubles."
    )

    print("=" * 55)
    print("  Part I — Analysing a string")
    print("=" * 55)

    t = Text(sample)

    print(f"\nText preview : {sample[:60]}...")
    print(f"word_frequency('to')  : {t.word_frequency('to')}")
    print(f"word_frequency('xyz') : {t.word_frequency('xyz')}")
    print(f"most_common_word()    : {t.most_common_word()!r}")
    print(f"unique_words()        : {t.unique_words()[:8]} ...")

    print("\n" + "=" * 55)
    print("  Part II — from_file()")
    print("=" * 55)

    # Write a tiny sample file so from_file() has something to read
    sample_file = "/tmp/sample_text.txt"
    with open(sample_file, "w") as f:
        f.write("Python is great. Python is fun. Learning Python is rewarding!")

    t2 = Text.from_file(sample_file)
    print(f"\nLoaded from file : {t2!r}")
    print(f"most_common_word(): {t2.most_common_word()!r}")
    print(f"unique_words()    : {t2.unique_words()}")

    print("\n" + "=" * 55)
    print("  Bonus — TextModification")
    print("=" * 55)

    dirty = "Hello, World!!! This is a test... #special @characters & more?"
    tm = TextModification(dirty)

    print(f"\nOriginal             : {dirty}")
    print(f"remove_punctuation() : {tm.remove_punctuation()}")
    print(f"remove_stop_words()  : {tm.remove_stop_words()}")
    print(f"remove_special()     : {tm.remove_special_characters()}")

    print("\n--- Combined pipeline (punctuation → stop words → special chars) ---")
    step1 = TextModification(dirty).remove_punctuation()
    step2 = TextModification(step1).remove_stop_words()
    step3 = TextModification(step2).remove_special_characters()
    print(f"Result: {step3!r}")
