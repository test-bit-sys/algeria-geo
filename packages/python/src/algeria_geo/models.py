"""Immutable data models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Literal, Optional, Tuple, TypeVar

Lang = Literal["ar", "fr", "en"]
Era = Literal[48, 58, 69]
T = TypeVar("T")


class _Named:
    __slots__ = ()
    name_ar: str
    name_fr: str
    name_en: str

    def name(self, lang: str = "ar") -> str:
        if lang not in ("ar", "fr", "en"):
            raise ValueError(f"lang must be 'ar', 'fr' or 'en', got {lang!r}")
        return getattr(self, f"name_{lang}")


@dataclass(frozen=True, slots=True)
class Wilaya(_Named):
    code: str
    name_ar: str
    name_fr: str
    name_en: str
    dairas_count: int
    communes_count: int
    phone_code: Optional[str]
    is_new_wilaya: bool
    era: int


@dataclass(frozen=True, slots=True)
class Daira(_Named):
    code: str
    wilaya_code: str
    name_ar: str
    name_fr: str
    name_en: str
    wilaya_code_58: str
    wilaya_code_48: str


@dataclass(frozen=True, slots=True)
class Commune(_Named):
    code: str
    daira_code: Optional[str]
    wilaya_code: str
    name_ar: str
    name_fr: str
    name_en: str
    post_code: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    wilaya_code_58: str
    wilaya_code_48: str


@dataclass(frozen=True)
class Match(Generic[T]):
    item: T
    score: float
    field: str


@dataclass(frozen=True)
class SearchResult:
    query: str
    wilayas: Tuple[Match[Wilaya], ...]
    dairas: Tuple[Match[Daira], ...]
    communes: Tuple[Match[Commune], ...]

    def __len__(self) -> int:
        return len(self.wilayas) + len(self.dairas) + len(self.communes)

    @property
    def best(self) -> Optional[Match]:
        every = (*self.wilayas, *self.dairas, *self.communes)
        return max(every, key=lambda m: m.score, default=None)
