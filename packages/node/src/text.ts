const AR_STRIP = /[\u064B-\u065F\u0670\u06D6-\u06ED\u0640]/g;
// Match definite article with bare Alef, Alef Wasla or Alef with Hamza above, but not Alef with Hamza below (إ).
// Also protect "اليزي" so its leading letters are not mistakenly treated as the definite article.
const AL_PREFIX = /(^| )[\u0627\u0671\u0623]\u0644(?!يزي(?:\b|\s))(?=\S{2,})/g;

const AR_ROMAN: Readonly<Record<string, string>> = {
  ا: "a", ب: "b", ت: "t", ث: "th", ج: "j", ح: "h", خ: "kh",
  د: "d", ذ: "dh", ر: "r", ز: "z", س: "s", ش: "sh", ص: "s",
  ض: "d", ط: "t", ظ: "z", ع: "", غ: "gh", ف: "f", ق: "q",
  ك: "k", ل: "l", م: "m", ن: "n", ه: "h", و: "w", ي: "y",
  ء: "", ڤ: "g", ڨ: "g", گ: "g", پ: "b",
};

const ARABIZI_MAP: ReadonlyArray<readonly [string, string]> = [
  ["3", ""],
  ["7", "h"],
  ["9", "q"],
  ["5", "kh"],
  ["2", ""],
];

const DIGRAPHS: ReadonlyArray<readonly [string, string]> = [
  ["ou", "w"], ["ch", "s"], ["sh", "s"], ["kh", "h"], ["gh", "k"],
  ["dj", "j"], ["ph", "f"], ["th", "t"], ["dh", "d"],
];
const FOLD_FROM = "qcgzpvx";
const FOLD_TO = "kkksbfk";

/** Lowercase, strip accents/diacritics, unify Arabic letter variants, drop the "ال" prefix. */
export function normalize(input: string): string {
  let s = input.normalize("NFKC").replace(AR_STRIP, "");
  // Strip definite article before folding hamzas to preserve root words starting with "إلـ"
  s = s.replace(AL_PREFIX, "$1");
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
  return s;
}

/** Consonant skeleton shared by Arabic and Latin spellings ("Ouargla" = "Warqla" = "ورقلة"). */
export function phoneticKey(input: string): string {
  let s = input.toLowerCase();
  for (const [digit, repl] of ARABIZI_MAP) {
    s = s.split(digit).join(repl);
  }
  let roman = "";
  for (const ch of normalize(s)) roman += AR_ROMAN[ch] ?? ch;
  roman = roman.replace(/ /g, "");
  for (const [a, b] of DIGRAPHS) roman = roman.split(a).join(b);
  roman = roman.replace(/[qcgzpvx]/g, (ch) => FOLD_TO.charAt(FOLD_FROM.indexOf(ch)));
  roman = roman.replace(/[aeiouy]/g, "").replace(/(.)\1+/g, "$1");
  if (roman.length > 2 && roman.endsWith("h")) roman = roman.slice(0, -1);
  return roman;
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
