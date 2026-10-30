#!/usr/bin/env python3
"""algeria-geo build pipeline: validate canonical data, emit every distribution."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LAT_RANGE = (18.9, 37.2)
LON_RANGE = (-8.7, 12.0)

Row = dict[str, Any]

W_FIELDS = ("code", "name_ar", "name_fr", "name_en", "dairas_count", "communes_count",
            "phone_code", "is_new_wilaya", "era")
D_FIELDS = ("code", "wilaya_code", "name_ar", "name_fr", "name_en",
            "wilaya_code_58", "wilaya_code_48")
C_FIELDS = ("code", "daira_code", "wilaya_code", "name_ar", "name_fr", "name_en",
            "post_code", "latitude", "longitude", "wilaya_code_58", "wilaya_code_48")

CODE2 = re.compile(r"\d{2}")
CODE4 = re.compile(r"\d{4}")
POST = re.compile(r"\d{5}")
PHONE = re.compile(r"0\d{2}")
ASCII = re.compile(r"[\x20-\x7E]+")


def era_of(code: int) -> int:
    return 48 if code <= 48 else 58 if code <= 58 else 69


def load(path: Path) -> list[Row]:
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise SystemExit(f"{path}: expected a JSON array")
    return data


def validate(wilayas: list[Row], dairas: list[Row], communes: list[Row],
             strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    def names(kind: str, row: Row) -> None:
        for f in ("name_ar", "name_fr", "name_en"):
            if not isinstance(row.get(f), str) or not row[f].strip():
                errors.append(f"{kind} {row.get('code')}: empty {f}")
        if isinstance(row.get("name_en"), str) and not ASCII.fullmatch(row["name_en"]):
            errors.append(f"{kind} {row.get('code')}: name_en must be printable ASCII")

    def lineage(kind: str, row: Row, wset: set[str]) -> None:
        code = row.get("code")
        w, w58, w48 = row.get("wilaya_code"), row.get("wilaya_code_58"), row.get("wilaya_code_48")
        for label, v in (("wilaya_code", w), ("wilaya_code_58", w58), ("wilaya_code_48", w48)):
            if v not in wset:
                errors.append(f"{kind} {code}: {label}={v!r} is not a known wilaya")
                return
        if int(w58) > 58:
            errors.append(f"{kind} {code}: wilaya_code_58 must be <= 58")
        if int(w48) > 48:
            errors.append(f"{kind} {code}: wilaya_code_48 must be <= 48")
        if int(w) <= 58 and w58 != w:
            errors.append(f"{kind} {code}: wilaya_code_58 must equal wilaya_code for pre-59 wilayas")
        if int(w) <= 48 and w48 != w:
            errors.append(f"{kind} {code}: wilaya_code_48 must equal wilaya_code for pre-49 wilayas")

    expected = [f"{i:02d}" for i in range(1, 70)]
    if [w.get("code") for w in wilayas] != expected:
        errors.append("wilayas: codes must be exactly '01'..'69', in order, without duplicates")
    wset = {w.get("code") for w in wilayas}
    for w in wilayas:
        c = w.get("code")
        if not (isinstance(c, str) and CODE2.fullmatch(c)):
            continue
        names("wilaya", w)
        if w.get("era") != era_of(int(c)):
            errors.append(f"wilaya {c}: era must be {era_of(int(c))}")
        pc = w.get("phone_code")
        if pc is not None and not (isinstance(pc, str) and PHONE.fullmatch(pc)):
            errors.append(f"wilaya {c}: phone_code must be null or like '021'")

    dmap: dict[str, Row] = {}
    for d in dairas:
        c = d.get("code")
        if not (isinstance(c, str) and CODE4.fullmatch(c)):
            errors.append(f"daira {c!r}: code must be 4 digits")
            continue
        if c in dmap:
            errors.append(f"daira {c}: duplicate code")
        dmap[c] = d
        names("daira", d)
        lineage("daira", d, wset)

    seen: set[str] = set()
    per_daira: Counter[str] = Counter()
    missing_geo = missing_post = 0
    for c in communes:
        code = c.get("code")
        if not (isinstance(code, str) and CODE4.fullmatch(code)):
            errors.append(f"commune {code!r}: code must be 4 digits")
            continue
        if code in seen:
            errors.append(f"commune {code}: duplicate code")
        seen.add(code)
        names("commune", c)
        lineage("commune", c, wset)
        parent = dmap.get(c.get("daira_code")) if c.get("daira_code") is not None else None
        if c.get("daira_code") is not None and parent is None:
            errors.append(f"commune {code}: orphan, unknown daira_code {c.get('daira_code')!r}")
        elif parent is not None:
            per_daira[parent["code"]] += 1
            for f in ("wilaya_code", "wilaya_code_58", "wilaya_code_48"):
                if c.get(f) != parent.get(f):
                    errors.append(f"commune {code}: {f} differs from its daira {parent['code']}")
        pc = c.get("post_code")
        if pc is None:
            missing_post += 1
        elif not (isinstance(pc, str) and POST.fullmatch(pc)):
            errors.append(f"commune {code}: post_code {pc!r} is not a 5-digit string")
        lat, lon = c.get("latitude"), c.get("longitude")
        if lat is None and lon is None:
            missing_geo += 1
        elif not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (lat, lon)):
            errors.append(f"commune {code}: latitude/longitude must both be numbers or both null")
        elif not (LAT_RANGE[0] <= lat <= LAT_RANGE[1] and LON_RANGE[0] <= lon <= LON_RANGE[1]):
            errors.append(f"commune {code}: GPS ({lat}, {lon}) is outside Algeria's bounding box")

    problems = warnings if not strict else errors
    for d in dmap:
        if per_daira[d] == 0:
            problems.append(f"daira {d}: has no communes")
    with_daira = {d.get("wilaya_code") for d in dairas}
    empty = [w.get("code") for w in wilayas if w.get("code") not in with_daira]
    if empty:
        problems.append(f"{len(empty)} wilaya(s) without dairas: {', '.join(empty)}")
    if missing_post:
        problems.append(f"{missing_post} commune(s) without post_code")
    if missing_geo:
        problems.append(f"{missing_geo} commune(s) without coordinates")
    return errors, warnings


def enrich(wilayas: list[Row], dairas: list[Row], communes: list[Row]) -> list[Row]:
    dc = Counter(d["wilaya_code"] for d in dairas)
    cc = Counter(c["wilaya_code"] for c in communes)
    return [{
        "code": w["code"], "name_ar": w["name_ar"], "name_fr": w["name_fr"], "name_en": w["name_en"],
        "dairas_count": dc[w["code"]], "communes_count": cc[w["code"]],
        "phone_code": w.get("phone_code"), "is_new_wilaya": int(w["code"]) > 58, "era": w["era"],
    } for w in wilayas]


def project(rows: list[Row], fields: tuple[str, ...]) -> list[Row]:
    return [{f: r.get(f) for f in fields} for r in sorted(rows, key=lambda r: r["code"])]


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def write_csv(path: Path, fields: tuple[str, ...], rows: list[Row]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(fields)
        for r in rows:
            wr.writerow(["" if r[f] is None else str(r[f]).lower() if isinstance(r[f], bool) else r[f]
                         for f in fields])


def build_tree(wil: list[Row], dai: list[Row], com: list[Row]) -> dict[str, Any]:
    by_daira: dict[str, list[Row]] = {}
    unassigned: dict[str, list[Row]] = {}
    for c in com:
        if c["daira_code"] is None:
            unassigned.setdefault(c["wilaya_code"], []).append(c)
        else:
            by_daira.setdefault(c["daira_code"], []).append(c)
    by_wilaya: dict[str, list[Row]] = {}
    for d in dai:
        by_wilaya.setdefault(d["wilaya_code"], []).append({**d, "communes": by_daira.get(d["code"], [])})
    return {"wilayas": [{**w, "dairas": by_wilaya.get(w["code"], []),
                         "unassigned_communes": unassigned.get(w["code"], [])} for w in wil]}


# ---------------------------------------------------------------- SQL

SQL_COLS = {"wilayas": W_FIELDS, "dairas": D_FIELDS, "communes": C_FIELDS}


def literal(v: Any, mysql: bool) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float)):
        return repr(v)
    s = str(v)
    if mysql:
        s = s.replace("\\", "\\\\")
    return "'" + s.replace("'", "''") + "'"


def ddl(mysql: bool) -> str:
    tail = " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci" if mysql else ""
    return f"""DROP TABLE IF EXISTS communes;
DROP TABLE IF EXISTS dairas;
DROP TABLE IF EXISTS wilayas;

CREATE TABLE wilayas (
  code CHAR(2) NOT NULL PRIMARY KEY,
  name_ar VARCHAR(100) NOT NULL,
  name_fr VARCHAR(100) NOT NULL,
  name_en VARCHAR(100) NOT NULL,
  dairas_count SMALLINT NOT NULL,
  communes_count SMALLINT NOT NULL,
  phone_code VARCHAR(4),
  is_new_wilaya SMALLINT NOT NULL,
  era SMALLINT NOT NULL
){tail};

CREATE TABLE dairas (
  code CHAR(4) NOT NULL PRIMARY KEY,
  wilaya_code CHAR(2) NOT NULL,
  name_ar VARCHAR(100) NOT NULL,
  name_fr VARCHAR(100) NOT NULL,
  name_en VARCHAR(100) NOT NULL,
  wilaya_code_58 CHAR(2) NOT NULL,
  wilaya_code_48 CHAR(2) NOT NULL,
  FOREIGN KEY (wilaya_code) REFERENCES wilayas (code),
  FOREIGN KEY (wilaya_code_58) REFERENCES wilayas (code),
  FOREIGN KEY (wilaya_code_48) REFERENCES wilayas (code)
){tail};
CREATE INDEX idx_dairas_wilaya ON dairas (wilaya_code);
CREATE INDEX idx_dairas_wilaya_58 ON dairas (wilaya_code_58);
CREATE INDEX idx_dairas_wilaya_48 ON dairas (wilaya_code_48);

CREATE TABLE communes (
  code CHAR(4) NOT NULL PRIMARY KEY,
    daira_code CHAR(4),
  wilaya_code CHAR(2) NOT NULL,
  name_ar VARCHAR(100) NOT NULL,
  name_fr VARCHAR(100) NOT NULL,
  name_en VARCHAR(100) NOT NULL,
  post_code CHAR(5),
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  wilaya_code_58 CHAR(2) NOT NULL,
  wilaya_code_48 CHAR(2) NOT NULL,
  FOREIGN KEY (daira_code) REFERENCES dairas (code),
  FOREIGN KEY (wilaya_code) REFERENCES wilayas (code),
  FOREIGN KEY (wilaya_code_58) REFERENCES wilayas (code),
  FOREIGN KEY (wilaya_code_48) REFERENCES wilayas (code)
){tail};
CREATE INDEX idx_communes_daira ON communes (daira_code);
CREATE INDEX idx_communes_wilaya ON communes (wilaya_code);
CREATE INDEX idx_communes_wilaya_58 ON communes (wilaya_code_58);
CREATE INDEX idx_communes_wilaya_48 ON communes (wilaya_code_48);
CREATE INDEX idx_communes_post_code ON communes (post_code);
"""


def inserts(table: str, rows: list[Row], mysql: bool, chunk: int = 500) -> list[str]:
    cols = SQL_COLS[table]
    out = []
    for i in range(0, len(rows), chunk):
        values = ",\n".join("  (" + ", ".join(literal(r[c], mysql) for c in cols) + ")"
                            for r in rows[i:i + chunk])
        out.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n{values};")
    return out


def build_sql(wil: list[Row], dai: list[Row], com: list[Row], mysql: bool) -> str:
    head = ("-- algeria-geo: 69 wilayas, dairas, communes (UTF-8)\n"
            + ("-- Target: MySQL / MariaDB\nSET NAMES utf8mb4;\n\n" if mysql else
               "-- Target: PostgreSQL and SQLite (MySQL 8 works if the database default is utf8mb4;\n"
               "-- otherwise use algeria_geo.mysql.sql)\n\n"))
    body = [ddl(mysql), "BEGIN;"]
    for table, rows in (("wilayas", wil), ("dairas", dai), ("communes", com)):
        body.extend(inserts(table, rows, mysql))
    body.append("COMMIT;")
    return head + "\n".join(body) + "\n"


# ---------------------------------------------------------------- package data

def emit_python(root: Path, wil: list[Row], dai: list[Row], com: list[Row]) -> None:
    base = root / "packages" / "python" / "src" / "algeria_geo" / "data"
    write_json(base / "wilayas.json", wil)
    write_json(base / "dairas.json", dai)
    write_json(base / "communes.json", com)
    readme = root / "README.md"
    if readme.exists():
        (root / "packages" / "python" / "README.md").write_text(readme.read_text(encoding="utf-8"), encoding="utf-8")


def emit_node(root: Path, wil: list[Row], dai: list[Row], com: list[Row]) -> None:
    def block(name: str, typ: str, rows: list[list[Any]]) -> str:
        lines = ",\n".join("  " + json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in rows)
        return f"export const {name}: readonly {typ}[] = [\n{lines}\n];\n" if rows \
            else f"export const {name}: readonly {typ}[] = [];\n"

    w = [[r["code"], r["name_ar"], r["name_fr"], r["name_en"], r["phone_code"], r["era"]] for r in wil]
    d = [[r["code"], r["wilaya_code"], r["name_ar"], r["name_fr"], r["name_en"],
          r["wilaya_code_58"], r["wilaya_code_48"]] for r in dai]
    c = [[r["code"], r["daira_code"], r["wilaya_code"], r["name_ar"], r["name_fr"], r["name_en"],
          r["post_code"], r["latitude"], r["longitude"], r["wilaya_code_58"], r["wilaya_code_48"]]
         for r in com]
    text = ("// AUTO-GENERATED by scripts/build.py. Do not edit.\n"
            'import type { CommuneRow, DairaRow, WilayaRow } from "./types.js";\n\n'
            + block("WILAYAS", "WilayaRow", w) + "\n"
            + block("DAIRAS", "DairaRow", d) + "\n"
            + block("COMMUNES", "CommuneRow", c))
    (root / "packages" / "node" / "src").mkdir(parents=True, exist_ok=True)
    (root / "packages" / "node" / "src" / "data.ts").write_text(text, encoding="utf-8")
    readme = root / "README.md"
    if readme.exists():
        (root / "packages" / "node" / "README.md").write_text(readme.read_text(encoding="utf-8"), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build algeria-geo distributions.")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    ap.add_argument("--strict", action="store_true",
                    help="treat missing dairas/communes/postal codes/coordinates as errors")
    ap.add_argument("--no-packages", action="store_true", help="skip writing package data files")
    args = ap.parse_args(argv)
    root: Path = args.root

    wilayas = load(root / "data" / "wilayas.json")
    dairas = load(root / "data" / "dairas.json")
    communes = load(root / "data" / "communes.json")

    errors, warnings = validate(wilayas, dairas, communes, args.strict)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if errors:
        print(f"validation failed: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"validation ok: {len(wilayas)} wilayas, {len(dairas)} dairas, {len(communes)} communes")
    if args.check:
        return 0

    wil = enrich(wilayas, dairas, communes)
    dai = project(dairas, D_FIELDS)
    com = project(communes, C_FIELDS)
    dist = root / "dist"

    write_json(dist / "wilayas.min.json", wil)
    write_json(dist / "dairas.min.json", dai)
    write_json(dist / "communes.min.json", com)
    write_json(dist / "tree.min.json", build_tree(wil, dai, com))
    write_csv(dist / "csv" / "wilayas.csv", W_FIELDS, wil)
    write_csv(dist / "csv" / "dairas.csv", D_FIELDS, dai)
    write_csv(dist / "csv" / "communes.csv", C_FIELDS, com)
    dist.mkdir(parents=True, exist_ok=True)
    (dist / "algeria_geo.sql").write_text(build_sql(wil, dai, com, mysql=False), encoding="utf-8")
    (dist / "algeria_geo.mysql.sql").write_text(build_sql(wil, dai, com, mysql=True), encoding="utf-8")

    if not args.no_packages:
        emit_python(root, wil, dai, com)
        emit_node(root, wil, dai, com)
    print(f"wrote distributions to {dist}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
