"""algeria-geo: Algerian administrative divisions (69 wilayas), dairas and communes."""
from __future__ import annotations

from typing import Dict, List, Optional, Union

from .index import GeoIndex, default_index
from .models import Commune, Daira, Match, SearchResult, Wilaya

__version__ = "1.1.0"
__all__ = [
    "Commune",
    "Daira",
    "GeoIndex",
    "Match",
    "SearchResult",
    "Wilaya",
    "default_index",
    "get_all_communes",
    "get_all_dairas",
    "get_commune",
    "get_communes",
    "get_communes_by_daira",
    "get_daira",
    "get_dairas",
    "get_postal_code",
    "get_wilaya",
    "get_wilaya_by_commune",
    "get_wilaya_by_phone_code",
    "get_wilayas",
    "search",
    "to_dropdown_options",
]

Identifier = Union[str, int]


def get_wilaya(identifier: Identifier, era: int = 69) -> Optional[Wilaya]:
    """Look up a wilaya by code (16, '16'), or by exact/transliterated name in Arabic/French/English."""
    return default_index().get_wilaya(identifier, era)


def get_wilayas(era: int = 69) -> List[Wilaya]:
    """List all wilayas defined in a given boundary era (48, 58, or 69)."""
    return default_index().get_wilayas(era)


def get_daira(code: Identifier) -> Optional[Daira]:
    """Look up a daira by its 4-digit code (e.g. '1601', 1601)."""
    return default_index().get_daira(code)


def get_dairas(wilaya_code: Identifier, era: int = 69) -> List[Daira]:
    """List all dairas of a wilaya in a given era."""
    return default_index().get_dairas(wilaya_code, era)


def get_all_dairas(era: int = 69) -> List[Daira]:
    """List all dairas across all wilayas for a given boundary era."""
    return default_index().get_all_dairas(era)


def get_commune(code: Identifier) -> Optional[Commune]:
    """Look up a commune by its 4-digit ONS code."""
    return default_index().get_commune(code)


def get_communes(wilaya_code: Identifier, era: int = 69) -> List[Commune]:
    """Communes of a wilaya as it was defined in `era` (48, 58 or 69)."""
    return default_index().get_communes(wilaya_code, era)


def get_all_communes(era: int = 69) -> List[Commune]:
    """List all communes across all wilayas for a given boundary era."""
    return default_index().get_all_communes(era)


def get_communes_by_daira(daira_code: Identifier) -> List[Commune]:
    """List all communes belonging to a specific daira."""
    return default_index().get_communes_by_daira(daira_code)


def get_wilaya_by_phone_code(phone_code: Union[str, int]) -> Optional[Wilaya]:
    """Look up a wilaya by its telephone area code (e.g. '021' or '21')."""
    return default_index().get_wilaya_by_phone_code(phone_code)


def get_wilaya_by_commune(commune_code: Identifier, era: int = 69) -> Optional[Wilaya]:
    """Find the wilaya that a commune belongs to in a given era."""
    return default_index().get_wilaya_by_commune(commune_code, era)


def search(query: str, lang: str = "any", limit: int = 20) -> SearchResult:
    """Fuzzy search across wilayas, dairas and communes."""
    return default_index().search(query, lang, limit)


def get_postal_code(commune_name: str, wilaya_code: Optional[Identifier] = None) -> Optional[str]:
    """Look up a postal code for a commune (optional wilaya constraint)."""
    return default_index().get_postal_code(commune_name, wilaya_code)


def to_dropdown_options(lang: str = "ar", era: int = 69) -> List[Dict[str, str]]:
    """Format wilayas for select dropdowns: [{'value': '01', 'label': 'Adrar'}, ...]."""
    return default_index().to_dropdown_options(lang, era)
