"""In-memory index: O(1) lookups by code, O(N) fuzzy search."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from typing import Any, Dict, Generic, List, Optional, Sequence, Tuple, TypeVar, Union

from ._text import normalize, phonetic_key, similarity
from .models import Commune, Daira, Match, SearchResult, Wilaya

ERAS = (48, 58, 69)
MIN_SCORE = 0.6
_LANGS = ("ar", "fr", "en")
T = TypeVar("T", Wilaya, Daira, Commune)
Identifier = Union[str, int]


@dataclass(frozen=True)
class _Entry(Generic[T]):
    item: T
    names: Tuple[Tuple[str, str, str], ...]  # (lang, normalized, phonetic)


def _entry(item: T) -> "_Entry[T]":
    return _Entry(item, tuple((lang, normalize(getattr(item, f"name_{lang}")),
                               phonetic_key(getattr(item, f"name_{lang}"))) for lang in _LANGS))


def _score(qn: str, qp: str, norm: str, phon: str) -> float:
    if norm == qn:
        return 1.0
    if norm.startswith(qn):
        return 0.92
    if qn in norm:
        return 0.85
    if len(qp) >= 2 and phon == qp:
        return 0.8
    return max(similarity(norm, qn), similarity(phon, qp) * 0.9) * 0.75


def _rank(entries: Sequence["_Entry[T]"], qn: str, qp: str, langs: Sequence[str],
          limit: int) -> Tuple[Match[T], ...]:
    out: List[Match[T]] = []
    for e in entries:
        best, field = 0.0, "ar"
        for lang, norm, phon in e.names:
            if lang in langs:
                s = _score(qn, qp, norm, phon)
                if s > best:
                    best, field = s, lang
        if best >= MIN_SCORE:
            out.append(Match(e.item, round(best, 4), field))
    out.sort(key=lambda m: (-m.score, m.item.code))
    return tuple(out[:limit])


def to_code(identifier: Any) -> Optional[str]:
    if isinstance(identifier, bool):
        return None
    s = str(identifier).strip()
    return s.zfill(2) if re.fullmatch(r"\d{1,2}", s) else None


def check_era(era: int) -> None:
    if era not in ERAS:
        raise ValueError(f"era must be one of {ERAS}, got {era!r}")


class GeoIndex:
    def __init__(self, wilayas: Sequence[Wilaya], dairas: Sequence[Daira],
                 communes: Sequence[Commune]) -> None:
        self.wilayas: Tuple[Wilaya, ...] = tuple(sorted(wilayas, key=lambda w: w.code))
        self.wilaya_by_code: Dict[str, Wilaya] = {w.code: w for w in self.wilayas}
        self.daira_by_code: Dict[str, Daira] = {d.code: d for d in dairas}
        self.commune_by_code: Dict[str, Commune] = {c.code: c for c in communes}

        d_acc: Dict[Tuple[int, str], List[Daira]] = {}
        c_acc: Dict[Tuple[int, str], List[Commune]] = {}
        for d in sorted(dairas, key=lambda x: x.code):
            for era, w in ((69, d.wilaya_code), (58, d.wilaya_code_58), (48, d.wilaya_code_48)):
                d_acc.setdefault((era, w), []).append(d)
        for c in sorted(communes, key=lambda x: x.code):
            for era, w in ((69, c.wilaya_code), (58, c.wilaya_code_58), (48, c.wilaya_code_48)):
                c_acc.setdefault((era, w), []).append(c)
        self.dairas_by_era: Dict[Tuple[int, str], Tuple[Daira, ...]] = {k: tuple(v) for k, v in d_acc.items()}
        self.communes_by_era: Dict[Tuple[int, str], Tuple[Commune, ...]] = {k: tuple(v) for k, v in c_acc.items()}

        self.wilaya_by_name: Dict[str, Wilaya] = {}
        self.wilaya_by_phon: Dict[str, List[Wilaya]] = {}
        for w in self.wilayas:
            for lang in _LANGS:
                raw = getattr(w, f"name_{lang}")
                self.wilaya_by_name.setdefault(normalize(raw), w)
                bucket = self.wilaya_by_phon.setdefault(phonetic_key(raw), [])
                if w not in bucket:
                    bucket.append(w)

        self.commune_by_name: Dict[str, List[Commune]] = {}
        for c in sorted(communes, key=lambda x: x.code):
            for lang in _LANGS:
                bucket = self.commune_by_name.setdefault(normalize(getattr(c, f"name_{lang}")), [])
                if c not in bucket:
                    bucket.append(c)

        self._w_entries = tuple(_entry(w) for w in self.wilayas)
        self._d_entries = tuple(_entry(d) for d in sorted(dairas, key=lambda x: x.code))
        self._c_entries = tuple(_entry(c) for c in sorted(communes, key=lambda x: x.code))

    @classmethod
    def load(cls) -> "GeoIndex":
        base = resources.files("algeria_geo") / "data"

        def read(name: str) -> List[Dict[str, Any]]:
            return json.loads((base / name).read_text(encoding="utf-8"))

        return cls([Wilaya(**r) for r in read("wilayas.json")],
                   [Daira(**r) for r in read("dairas.json")],
                   [Commune(**r) for r in read("communes.json")])

    # ------------------------------------------------------------ queries

    def get_wilaya(self, identifier: Identifier, era: int = 69) -> Optional[Wilaya]:
        check_era(era)
        code = to_code(identifier)
        found: Optional[Wilaya]
        if code is not None:
            found = self.wilaya_by_code.get(code)
        else:
            key = normalize(str(identifier))
            found = self.wilaya_by_name.get(key)
            if found is None:
                hits = self.wilaya_by_phon.get(phonetic_key(str(identifier)), [])
                found = hits[0] if len(hits) == 1 else None
        return found if found is not None and int(found.code) <= era else None

    def get_wilayas(self, era: int = 69) -> List[Wilaya]:
        check_era(era)
        return [w for w in self.wilayas if int(w.code) <= era]

    def get_dairas(self, wilaya_code: Identifier, era: int = 69) -> List[Daira]:
        check_era(era)
        code = to_code(wilaya_code)
        return list(self.dairas_by_era.get((era, code), ())) if code and int(code) <= era else []

    def get_communes(self, wilaya_code: Identifier, era: int = 69) -> List[Commune]:
        check_era(era)
        code = to_code(wilaya_code)
        return list(self.communes_by_era.get((era, code), ())) if code and int(code) <= era else []

    def search(self, query: str, lang: str = "any", limit: int = 20) -> SearchResult:
        if lang != "any" and lang not in _LANGS:
            raise ValueError("lang must be 'any', 'ar', 'fr' or 'en'")
        qn = normalize(query)
        if not qn:
            return SearchResult(query, (), (), ())
        qp = phonetic_key(query)
        langs = _LANGS if lang == "any" else (lang,)
        return SearchResult(query,
                            _rank(self._w_entries, qn, qp, langs, limit),
                            _rank(self._d_entries, qn, qp, langs, limit),
                            _rank(self._c_entries, qn, qp, langs, limit))

    def get_postal_code(self, commune_name: str, wilaya_code: Optional[Identifier] = None) -> Optional[str]:
        code = to_code(wilaya_code) if wilaya_code is not None else None
        for c in self.commune_by_name.get(normalize(commune_name), ()):
            if c.post_code and (code is None or c.wilaya_code == code):
                return c.post_code
        return None

    def to_dropdown_options(self, lang: str = "ar", era: int = 69) -> List[Dict[str, str]]:
        return [{"value": w.code, "label": w.name(lang)} for w in self.get_wilayas(era)]


@lru_cache(maxsize=1)
def default_index() -> GeoIndex:
    return GeoIndex.load()
