#!/usr/bin/env python3
"""Import Algeria's administrative divisions from a pinned, cited source."""
from __future__ import annotations

import csv
import json
import io
import unicodedata
from pathlib import Path
from urllib.request import urlopen
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REVISION = "0b3b6ab2ac1b1569469285d8fe5e7df18666fcdf"
BASE_URL = f"https://raw.githubusercontent.com/djazairdev/wilayas/{REVISION}/data"


def read_csv(name: str) -> list[dict[str, str]]:
    with urlopen(f"{BASE_URL}/{name}.csv", timeout=30) as response:
        text = response.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def ascii_fold(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.replace("’", "'"))
    plain = "".join(char for char in normalized if not unicodedata.combining(char))
    return "".join(char for char in plain if 32 <= ord(char) < 127).strip()


def pad(code: str) -> str:
    return code.strip().zfill(2)


def ancestor(code: str, parents: dict[str, str], era: int) -> str:
    while int(code) > era:
        code = parents[code]
    return code


def main() -> int:
    wilaya_source = read_csv("wilayas")
    daira_source = read_csv("dairas")
    commune_source = read_csv("communes")
    parent_by_code = {
        pad(row["code"]): pad(row["parent"])
        for row in wilaya_source if row["parent"]
    }

    wilaya_path = ROOT / "data" / "wilayas.json"
    existing_wilayas: list[dict[str, Any]] = []
    if wilaya_path.exists():
        existing_wilayas = json.loads(wilaya_path.read_text(encoding="utf-8"))
    phone_codes = {row["code"]: row.get("phone_code") for row in existing_wilayas}

    commune_path = ROOT / "data" / "communes.json"
    existing_communes: list[dict[str, Any]] = []
    if commune_path.exists():
        existing_communes = json.loads(commune_path.read_text(encoding="utf-8"))
    commune_attrs = {
        row["code"]: (row.get("post_code"), row.get("latitude"), row.get("longitude"), row.get("daira_code"))
        for row in existing_communes
    }

    wilayas = []
    for row in wilaya_source:
        code = pad(row["code"])
        number = int(code)
        name_ar = row["name_ar"]
        if code == "33":
            name_ar = "إليزي"
        wilayas.append({
            "code": code,
            "name_ar": name_ar,
            "name_fr": row["name_fr"],
            "name_en": ascii_fold(row["name_fr"]),
            "phone_code": phone_codes.get(code),
            "era": 48 if number <= 48 else 58 if number <= 58 else 69,
        })

    dairas = []
    for row in daira_source:
        code = row["code"].strip()
        wilaya = pad(row["wilaya"])
        old_wilaya = pad(code[:2])
        dairas.append({
            "code": code,
            "wilaya_code": wilaya,
            "name_ar": row["name_ar"],
            "name_fr": row["name_fr"],
            "name_en": ascii_fold(row["name_fr"]),
            "wilaya_code_58": old_wilaya,
            "wilaya_code_48": ancestor(old_wilaya, parent_by_code, 48),
        })

    communes = []
    for row in commune_source:
        code = row["code"].strip()
        wilaya = pad(row["wilaya"])
        old_wilaya = pad(row["wilaya_before"] or wilaya)
        prev_post, prev_lat, prev_lon, prev_daira = commune_attrs.get(code, (None, None, None, None))
        daira_code = prev_daira if prev_daira else (row["daira"].strip() or None)
        communes.append({
            "code": code,
            "daira_code": daira_code,
            "wilaya_code": wilaya,
            "name_ar": row["name_ar"],
            "name_fr": row["name_fr"],
            "name_en": ascii_fold(row["name_fr"]),
            "post_code": prev_post,
            "latitude": prev_lat,
            "longitude": prev_lon,
            "wilaya_code_58": old_wilaya,
            "wilaya_code_48": ancestor(old_wilaya, parent_by_code, 48),
        })

    for name, records in (("wilayas", wilayas), ("dairas", dairas), ("communes", communes)):
        path = ROOT / "data" / f"{name}.json"
        path.write_text(json.dumps(records, ensure_ascii=False, separators=(",", ":")) + "\n",
                        encoding="utf-8")
    print(f"Imported {len(wilayas)} wilayas, {len(dairas)} dairas and {len(communes)} communes from {REVISION}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
