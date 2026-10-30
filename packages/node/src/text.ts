const AR_STRIP = /[\u064B-\u065F\u0670\u06D6-\u06ED\u0640]/g;
const AL_PREFIX = /(^| )ال(?=\S{2,})/g;

const AR_ROMAN: Readonly<Record<string, string>> = {
  ا: "a", ب: "b", ت: "t", ث: "th", ج: "j", ح: "h", خ: "kh",
  د: "d", ذ: "dh", ر: "r", ز: "z", س: "s", ش: "sh", ص: "s",
  ض: "d", ط: "t", ظ: "z", ع: "", غ: "gh", ف: "f", ق: "q",
  ك: "k", ل: "l", م: "m", ن: "n", ه: "h", و: "w", ي: "y",
  ء: "", ڤ: "g", ڨ: "g", گ: "g", پ: "b",
};

const DIGRAPHS: ReadonlyArray<readonly [string, string]> = [
  ["ou", "w"], ["ch", "s"], ["sh", "s"], ["kh", "h"], ["gh", "k"],
  ["dj", "j"], ["ph", "f"], ["th", "t"], ["dh", "d"],
];
const FOLD_FROM = "qcgzpvx";
const FOLD_TO = "kkksbfk";

/** Lowercase, strip accents/diacritics, unify Arabic letter variants, drop the "ال" prefix. */
export function normalize(input: string): string {
  let s = input.normalize("NFKC").replace(AR_STRIP, "");
  s = s
    .replace(/[ٱأإآ]/g, "ا")
    .replace(/ى/g, "ي")
    .replace(/ئ/g, "ي")
    .replace(/ؤ/g, "و")
    .replace(/ة/g, "ه")
    .toLowerCase()
    .normalize("NFKD")
    .replace(/\p{M}/gu, "")
    .replace(/[^\p{L}\p{N}]+/gu, " ")
    .trim();
  return s.replace(AL_PREFIX, "$1");
}

/** Consonant skeleton shared by Arabic and Latin spellings ("Ouargla" = "Warqla" = "ورقلة"). */
export function phoneticKey(input: string): string {
  let s = "";
  for (const ch of normalize(input)) s += AR_ROMAN[ch] ?? ch;
  s = s.replace(/ /g, "");
  for (const [a, b] of DIGRAPHS) s = s.split(a).join(b);
  s = s.replace(/[qcgzpvx]/g, (ch) => FOLD_TO.charAt(FOLD_FROM.indexOf(ch)));
  s = s.replace(/[aeiouy]/g, "").replace(/(.)\1+/g, "$1");
  if (s.length > 2 && s.endsWith("h")) s = s.slice(0, -1);
  return s;
}

/** 1 - normalized Levenshtein distance. */
export function similarity(a: string, b: string): number {
  if (a.length === 0 || b.length === 0) return 0;
  if (a === b) return 1;
  let prev: number[] = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    const cur: number[] = [i];
    for (let j = 1; j <= b.length; j++) {
      const sub = (prev[j - 1] as number) + (a.charCodeAt(i - 1) === b.charCodeAt(j - 1) ? 0 : 1);
      cur.push(Math.min((prev[j] as number) + 1, (cur[j - 1] as number) + 1, sub));
    }
    prev = cur;
  }
  return 1 - (prev[b.length] as number) / Math.max(a.length, b.length);
}
