"""SVG map generation and vector paths for Algerian wilayas."""
from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from typing import Dict, Optional, Union

Identifier = Union[str, int]


@lru_cache(maxsize=1)
def load_svg_paths() -> Dict[str, str]:
    """Return dictionary of official 2-digit wilaya codes mapped to SVG path strings."""
    base = resources.files("algeria_geo") / "data"
    raw = (base / "map_paths.json").read_text(encoding="utf-8")
    return json.loads(raw)


def get_wilaya_svg_path(code: Identifier) -> Optional[str]:
    """Return the SVG path geometry (d attribute) for a given wilaya code."""
    s = str(code).strip()
    c = s.zfill(2) if s.isdigit() and len(s) <= 2 else None
    return load_svg_paths().get(c) if c else None


def get_map_svg(
    era: int = 69,
    width: Union[str, int] = "100%",
    height: Union[str, int] = "100%",
    svg_id: str = "algeria-map",
    class_name: str = "wilaya",
    include_styles: bool = True,
) -> str:
    """Generate a complete standalone SVG map of Algeria for the given boundary era (48, 58, 69)."""
    from .index import check_era, default_index
    check_era(era)
    idx = default_index()
    wilayas = idx.get_wilayas(era=era)
    paths_dict = load_svg_paths()

    styles = (
        "  <defs>\n"
        "    <style>\n"
        f"      .{class_name} {{ fill: #cbd5e1; stroke: #ffffff; stroke-width: 1.5; stroke-linejoin: round; vector-effect: non-scaling-stroke; transition: fill 0.2s ease; }}\n"
        f"      .{class_name}:hover {{ fill: #10b981; cursor: pointer; }}\n"
        "    </style>\n"
        "  </defs>\n"
        if include_styles
        else ""
    )

    path_lines = []
    for w in wilayas:
        d = paths_dict.get(w.code, "")
        phone = w.phone_code or ""
        path_lines.append(
            f'    <path id="wilaya-{w.code}" class="{class_name}" data-code="{w.code}" '
            f'data-name-ar="{w.name_ar}" data-name-fr="{w.name_fr}" data-name-en="{w.name_en}" '
            f'data-phone-code="{phone}" data-era="{w.era}" data-dairas="{w.dairas_count}" '
            f'data-communes="{w.communes_count}" d="{d}" />'
        )

    paths_str = "\n".join(path_lines)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg id="{svg_id}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10000 9999" '
        f'data-bbox="-8.6689,18.9681,11.9973,37.0883" width="{width}" height="{height}">\n'
        '  <!-- algeria-geo: 69 Wilayas SVG Map (Web Mercator projection). Boundaries © OpenStreetMap contributors under ODbL 1.0. -->\n'
        f'{styles}'
        '  <g id="wilayas">\n'
        f'{paths_str}\n'
        '  </g>\n'
        '</svg>\n'
    )
