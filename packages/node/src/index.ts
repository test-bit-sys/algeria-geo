import { COMMUNES, DAIRAS, WILAYAS } from "./data.js";
import { normalize, phoneticKey, similarity } from "./text.js";
import type {
  Commune, Daira, DropdownOption, Era, Lang, Match, SearchLang, SearchResult, Wilaya,
} from "./types.js";

export type {
  Commune, Daira, DropdownOption, Era, Lang, Match, SearchLang, SearchResult, Wilaya,
} from "./types.js";

export const ERAS: readonly Era[] = [48, 58, 69];
const LANGS: readonly Lang[] = ["ar", "fr", "en"];
const MIN_SCORE = 0.6;

interface Name { readonly lang: Lang; readonly norm: string; readonly phon: string }
interface Entry<T> { readonly item: T; readonly names: readonly Name[] }
interface Named { readonly name_ar: string; readonly name_fr: string; readonly name_en: string }

interface Index {
  readonly wilayas: readonly Wilaya[];
  readonly wilayaByCode: Map<string, Wilaya>;
  readonly communeByCode: Map<string, Commune>;
  readonly dairasByEra: Map<string, readonly Daira[]>;
  readonly communesByEra: Map<string, readonly Commune[]>;
  readonly wilayaByName: Map<string, Wilaya>;
  readonly wilayaByPhon: Map<string, Wilaya[]>;
  readonly communeByName: Map<string, Commune[]>;
  readonly wEntries: readonly Entry<Wilaya>[];
  readonly dEntries: readonly Entry<Daira>[];
  readonly cEntries: readonly Entry<Commune>[];
}

let cache: Index | undefined;

function entry<T extends Named>(item: T): Entry<T> {
  const raw: ReadonlyArray<readonly [Lang, string]> = [
    ["ar", item.name_ar], ["fr", item.name_fr], ["en", item.name_en],
  ];
  return { item, names: raw.map(([lang, s]) => ({ lang, norm: normalize(s), phon: phoneticKey(s) })) };
}

function push<K, V>(map: Map<K, V[]>, key: K, value: V): void {
  const bucket = map.get(key);
  if (bucket) {
    if (!bucket.includes(value)) bucket.push(value);
  } else {
    map.set(key, [value]);
  }
}

function build(): Index {
  const dc = new Map<string, number>();
  const cc = new Map<string, number>();
  const dairas: Daira[] = DAIRAS.map((r) => Object.freeze({
    code: r[0], wilaya_code: r[1], name_ar: r[2], name_fr: r[3], name_en: r[4],
    wilaya_code_58: r[5], wilaya_code_48: r[6],
  })).sort((a, b) => (a.code < b.code ? -1 : 1));
  const communes: Commune[] = COMMUNES.map((r) => Object.freeze({
    code: r[0], daira_code: r[1], wilaya_code: r[2], name_ar: r[3], name_fr: r[4], name_en: r[5],
    post_code: r[6], latitude: r[7], longitude: r[8], wilaya_code_58: r[9], wilaya_code_48: r[10],
  })).sort((a, b) => (a.code < b.code ? -1 : 1));
  for (const d of dairas) dc.set(d.wilaya_code, (dc.get(d.wilaya_code) ?? 0) + 1);
  for (const c of communes) cc.set(c.wilaya_code, (cc.get(c.wilaya_code) ?? 0) + 1);

  const wilayas: Wilaya[] = WILAYAS.map((r) => Object.freeze({
    code: r[0], name_ar: r[1], name_fr: r[2], name_en: r[3],
    dairas_count: dc.get(r[0]) ?? 0, communes_count: cc.get(r[0]) ?? 0,
    phone_code: r[4], is_new_wilaya: Number(r[0]) > 58, era: r[5],
  })).sort((a, b) => (a.code < b.code ? -1 : 1));

  const dairasByEra = new Map<string, Daira[]>();
  for (const d of dairas) {
    push(dairasByEra, `69:${d.wilaya_code}`, d);
    push(dairasByEra, `58:${d.wilaya_code_58}`, d);
    push(dairasByEra, `48:${d.wilaya_code_48}`, d);
  }
  const communesByEra = new Map<string, Commune[]>();
  for (const c of communes) {
    push(communesByEra, `69:${c.wilaya_code}`, c);
    push(communesByEra, `58:${c.wilaya_code_58}`, c);
    push(communesByEra, `48:${c.wilaya_code_48}`, c);
  }

  const wilayaByName = new Map<string, Wilaya>();
  const wilayaByPhon = new Map<string, Wilaya[]>();
  for (const w of wilayas) {
    for (const raw of [w.name_ar, w.name_fr, w.name_en]) {
      const key = normalize(raw);
      if (!wilayaByName.has(key)) wilayaByName.set(key, w);
      push(wilayaByPhon, phoneticKey(raw), w);
    }
  }
  const communeByName = new Map<string, Commune[]>();
  for (const c of communes) {
    for (const raw of [c.name_ar, c.name_fr, c.name_en]) push(communeByName, normalize(raw), c);
  }

  return {
    wilayas,
    wilayaByCode: new Map(wilayas.map((w) => [w.code, w])),
    communeByCode: new Map(communes.map((c) => [c.code, c])),
    dairasByEra, communesByEra, wilayaByName, wilayaByPhon, communeByName,
    wEntries: wilayas.map(entry), dEntries: dairas.map(entry), cEntries: communes.map(entry),
  };
}

function index(): Index {
  return (cache ??= build());
}

function checkEra(era: number): asserts era is Era {
  if (!ERAS.includes(era as Era)) throw new RangeError(`era must be one of ${ERAS.join(", ")}, got ${era}`);
}

function toCode(id: string | number): string | null {
  const s = String(id).trim();
  return /^\d{1,2}$/.test(s) ? s.padStart(2, "0") : null;
}

function scoreName(qn: string, qp: string, n: Name): number {
  if (n.norm === qn) return 1;
  if (n.norm.startsWith(qn)) return 0.92;
  if (n.norm.includes(qn)) return 0.85;
  if (qp.length >= 2 && n.phon === qp) return 0.8;
  return Math.max(similarity(n.norm, qn), similarity(n.phon, qp) * 0.9) * 0.75;
}

function rank<T extends { readonly code: string }>(
  entries: readonly Entry<T>[], qn: string, qp: string, langs: readonly Lang[], limit: number,
): Match<T>[] {
  const out: Match<T>[] = [];
  for (const e of entries) {
    let best = 0;
    let field: Lang = "ar";
    for (const n of e.names) {
      if (!langs.includes(n.lang)) continue;
      const s = scoreName(qn, qp, n);
      if (s > best) { best = s; field = n.lang; }
    }
    if (best >= MIN_SCORE) out.push({ item: e.item, score: Math.round(best * 10000) / 10000, field });
  }
  out.sort((a, b) => b.score - a.score || (a.item.code < b.item.code ? -1 : a.item.code > b.item.code ? 1 : 0));
  return out.slice(0, limit);
}

/** Look up by code (16, "16") or by exact/transliterated name in Arabic, French or English. */
export function getWilaya(identifier: string | number, era: Era = 69): Wilaya | null {
  checkEra(era);
  const idx = index();
  const code = toCode(identifier);
  let found: Wilaya | undefined;
  if (code !== null) {
    found = idx.wilayaByCode.get(code);
  } else {
    found = idx.wilayaByName.get(normalize(String(identifier)));
    if (!found) {
      const hits = idx.wilayaByPhon.get(phoneticKey(String(identifier)));
      if (hits && hits.length === 1) found = hits[0];
    }
  }
  return found && Number(found.code) <= era ? found : null;
}

export function getWilayas(era: Era = 69): Wilaya[] {
  checkEra(era);
  return index().wilayas.filter((w) => Number(w.code) <= era);
}

export function getDairas(wilayaCode: string | number, era: Era = 69): Daira[] {
  checkEra(era);
  const code = toCode(wilayaCode);
  return code !== null && Number(code) <= era ? [...(index().dairasByEra.get(`${era}:${code}`) ?? [])] : [];
}

/** Communes of a wilaya as it was defined in `era` (48, 58 or 69). */
export function getCommunes(wilayaCode: string | number, era: Era = 69): Commune[] {
  checkEra(era);
  const code = toCode(wilayaCode);
  return code !== null && Number(code) <= era ? [...(index().communesByEra.get(`${era}:${code}`) ?? [])] : [];
}

export function getCommune(code: string): Commune | null {
  return index().communeByCode.get(code) ?? null;
}

export function search(query: string, lang: SearchLang = "any", limit = 20): SearchResult {
  if (lang !== "any" && !LANGS.includes(lang)) throw new RangeError("lang must be 'any', 'ar', 'fr' or 'en'");
  const qn = normalize(query);
  if (qn === "") return { query, wilayas: [], dairas: [], communes: [] };
  const qp = phoneticKey(query);
  const langs: readonly Lang[] = lang === "any" ? LANGS : [lang];
  const idx = index();
  return {
    query,
    wilayas: rank(idx.wEntries, qn, qp, langs, limit),
    dairas: rank(idx.dEntries, qn, qp, langs, limit),
    communes: rank(idx.cEntries, qn, qp, langs, limit),
  };
}

export function getPostalCode(communeName: string, wilayaCode?: string | number): string | null {
  const code = wilayaCode === undefined ? null : toCode(wilayaCode);
  for (const c of index().communeByName.get(normalize(communeName)) ?? []) {
    if (c.post_code && (code === null || c.wilaya_code === code)) return c.post_code;
  }
  return null;
}

export function toDropdownOptions(lang: Lang = "ar", era: Era = 69): DropdownOption[] {
  if (!LANGS.includes(lang)) throw new RangeError("lang must be 'ar', 'fr' or 'en'");
  const key = `name_${lang}` as const;
  return getWilayas(era).map((w) => ({ value: w.code, label: w[key] }));
}
