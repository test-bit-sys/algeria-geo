"""algeria-geo: Algerian administrative divisions (69 wilayas), communes and postal codes."""
from __future__ import annotations

from typing import Dict, List, Optional, Union

from .index import GeoIndex, default_index
from .models import Commune, Daira, Match, SearchResult, Wilaya

__version__ = "1.0.0"
__all__ = [
    "Commune", "Daira", "GeoIndex", "Match", "SearchResult", "Wilaya",
    "get_commune", "get_communes", "get_dairas", "get_postal_code", "get_wilaya",
    "get_wilayas", "search", "to_dropdown_options",
]

Identifier = Union[str, int]


def get_wilaya(identifier: Identifier, era: int = 69) -> Optional[Wilaya]:
    """Look up by code (16, "16"), or by exact/transliterated name in ar/fr/en."""
    return default_index().get_wilaya(identifier, era)


def get_wilayas(era: int = 69) -> List[Wilaya]:
    return default_index().get_wilayas(era)


def get_dairas(wilaya_code: Identifier, era: int = 69) -> List[Daira]:
    return default_index().get_dairas(wilaya_code, era)


def get_communes(wilaya_code: Identifier, era: int = 69) -> List[Commune]:
    """Communes of a wilaya as it was defined in `era` (48, 58 or 69)."""
    return default_index().get_communes(wilaya_code, era)


def get_commune(code: str) -> Optional[Commune]:
    return default_index().commune_by_code.get(code)


def search(query: str, lang: str = "any") -> SearchResult:
    return default_index().search(query, lang)


def get_postal_code(commune_name: str) -> Optional[str]:
    return default_index().get_postal_code(commune_name)


def to_dropdown_options(lang: str = "ar") -> List[Dict[str, str]]:
    return default_index().to_dropdown_options(lang)
