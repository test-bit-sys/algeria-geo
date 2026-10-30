"""Script-aware normalization and phonetic keys (Arabic + Latin)."""
from __future__ import annotations

import re
import unicodedata

_AR_STRIP = re.compile("[\u064B-\u065F\u0670\u06D6-\u06ED\u0640]")
_AR_FOLD = str.maketrans({
    "ٱ": "ا", "أ": "ا", "إ": "ا", "آ": "ا",
    "ى": "ي", "ئ": "ي", "ؤ": "و", "ة": "ه",
})
_AL_PREFIX = re.compile(r"(^| )ال(?=\S{2,})")

_AR_ROMAN = {
    "ا": "a", "ب": "b", "ت": "t", "ث": "th", "ج": "j", "ح": "h", "خ": "kh",
    "د": "d", "ذ": "dh", "ر": "r", "ز": "z", "س": "s", "ش": "sh", "ص": "s",
    "ض": "d", "ط": "t", "ظ": "z", "ع": "", "غ": "gh", "ف": "f", "ق": "q",
    "ك": "k", "ل": "l", "م": "m", "ن": "n", "ه": "h", "و": "w", "ي": "y",
    "ء": "", "ڤ": "g", "ڨ": "g", "گ": "g", "پ": "b",
}
_DIGRAPHS = (("ou", "w"), ("ch", "s"), ("sh", "s"), ("kh", "h"), ("gh", "k"),
             ("dj", "j"), ("ph", "f"), ("th", "t"), ("dh", "d"))
_FOLD = str.maketrans("qcgzpvx", "kkksbfk")
_VOWELS = re.compile(r"[aeiouy]")
_REPEATS = re.compile(r"(.)\1+")


def normalize(text: str) -> str:
    """Lowercase, strip accents/diacritics, unify Arabic letter variants, drop the 'ال' prefix."""
    s = unicodedata.normalize("NFKC", text)
    s = _AR_STRIP.sub("", s).translate(_AR_FOLD).lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c if c.isalnum() else " " for c in s if not unicodedata.category(c).startswith("M"))
    s = " ".join(s.split())
    return _AL_PREFIX.sub(r"\1", s)


def phonetic_key(text: str) -> str:
    """Consonant skeleton shared by Arabic and Latin spellings ('Ouargla' == 'Warqla' == 'ورقلة')."""
    s = "".join(_AR_ROMAN.get(c, c) for c in normalize(text)).replace(" ", "")
    for a, b in _DIGRAPHS:
        s = s.replace(a, b)
    s = s.translate(_FOLD)
    s = _VOWELS.sub("", s)
    s = _REPEATS.sub(r"\1", s)
    if len(s) > 2 and s.endswith("h"):
        s = s[:-1]
    return s


def similarity(a: str, b: str) -> float:
    """1 - normalized Levenshtein distance."""
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return 1.0 - prev[-1] / max(len(a), len(b))
