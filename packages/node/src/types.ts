export type Era = 48 | 58 | 69;
export type Lang = "ar" | "fr" | "en";
export type SearchLang = Lang | "any";

export interface Wilaya {
  readonly code: string;
  readonly name_ar: string;
  readonly name_fr: string;
  readonly name_en: string;
  readonly dairas_count: number;
  readonly communes_count: number;
  readonly phone_code: string | null;
  readonly is_new_wilaya: boolean;
  readonly era: Era;
}

export interface Daira {
  readonly code: string;
  readonly wilaya_code: string;
  readonly name_ar: string;
  readonly name_fr: string;
  readonly name_en: string;
  readonly wilaya_code_58: string;
  readonly wilaya_code_48: string;
}

export interface Commune {
  readonly code: string;
  readonly daira_code: string | null;
  readonly wilaya_code: string;
  readonly name_ar: string;
  readonly name_fr: string;
  readonly name_en: string;
  readonly post_code: string | null;
  readonly latitude: number | null;
  readonly longitude: number | null;
  readonly wilaya_code_58: string;
  readonly wilaya_code_48: string;
}

export interface Match<T> {
  readonly item: T;
  readonly score: number;
  readonly field: Lang;
}

export interface SearchResult {
  readonly query: string;
  readonly wilayas: readonly Match<Wilaya>[];
  readonly dairas: readonly Match<Daira>[];
  readonly communes: readonly Match<Commune>[];
}

export interface DropdownOption {
  readonly value: string;
  readonly label: string;
}

/** [code, name_ar, name_fr, name_en, phone_code, era] */
export type WilayaRow = readonly [string, string, string, string, string | null, Era];
/** [code, wilaya_code, name_ar, name_fr, name_en, wilaya_code_58, wilaya_code_48] */
export type DairaRow = readonly [string, string, string, string, string, string, string];
/** [code, daira_code, wilaya_code, name_ar, name_fr, name_en, post_code, latitude, longitude, wilaya_code_58, wilaya_code_48] */
export type CommuneRow = readonly [
  string, string | null, string, string, string, string,
  string | null, number | null, number | null, string, string,
];
