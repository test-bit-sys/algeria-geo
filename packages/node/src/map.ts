import { WILAYA_SVG_PATHS } from "./map-data.js";
import { getWilayas } from "./index.js";
import type { Era } from "./types.js";

export interface MapSvgOptions {
  /** Boundary era: 48 (1984), 58 (2019), or 69 (2026). Defaults to 69. */
  readonly era?: Era;
  /** Width attribute of root svg. Defaults to "100%". */
  readonly width?: number | string;
  /** Height attribute of root svg. Defaults to "100%". */
  readonly height?: number | string;
  /** CSS class assigned to each <path>. Defaults to "wilaya". */
  readonly className?: string;
  /** HTML id of root svg element. Defaults to "algeria-map". */
  readonly id?: string;
  /** Whether to embed default hover and stroke styles in <defs>. Defaults to true. */
  readonly includeStyles?: boolean;
}

export { WILAYA_SVG_PATHS };

/** Return the SVG path geometry (d attribute) for a given wilaya code (e.g. 16, "16"). */
export function getWilayaSvgPath(code: string | number): string | null {
  const s = String(code).trim();
  const c = /^\d{1,2}$/.test(s) ? s.padStart(2, "0") : null;
  return c ? (WILAYA_SVG_PATHS[c] ?? null) : null;
}

/** Generate a complete standalone SVG map string of Algeria. */
export function getMapSvg(options: MapSvgOptions = {}): string {
  const {
    era = 69,
    width = "100%",
    height = "100%",
    className = "wilaya",
    id = "algeria-map",
    includeStyles = true,
  } = options;

  const wilayas = getWilayas(era);
  const styles = includeStyles
    ? "  <defs>\n" +
      "    <style>\n" +
      `      .${className} { fill: #cbd5e1; stroke: #ffffff; stroke-width: 1.5; stroke-linejoin: round; vector-effect: non-scaling-stroke; transition: fill 0.2s ease; }\n` +
      `      .${className}:hover { fill: #10b981; cursor: pointer; }\n` +
      "    </style>\n" +
      "  </defs>\n"
    : "";

  const paths = wilayas
    .map((w) => {
      const d = WILAYA_SVG_PATHS[w.code] ?? "";
      const phone = w.phone_code ?? "";
      return (
        `    <path id="wilaya-${w.code}" class="${className}" data-code="${w.code}" ` +
        `data-name-ar="${w.name_ar}" data-name-fr="${w.name_fr}" data-name-en="${w.name_en}" ` +
        `data-phone-code="${phone}" data-era="${w.era}" data-dairas="${w.dairas_count}" ` +
        `data-communes="${w.communes_count}" d="${d}" />`
      );
    })
    .join("\n");

  return (
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<svg id="${id}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10000 9999" ` +
    `data-bbox="-8.6689,18.9681,11.9973,37.0883" width="${width}" height="${height}">\n` +
    `  <!-- algeria-geo: 69 Wilayas SVG Map (Web Mercator projection). Boundaries © OpenStreetMap contributors under ODbL 1.0. -->\n` +
    styles +
    `  <g id="wilayas">\n` +
    paths +
    `\n  </g>\n` +
    `</svg>\n`
  );
}
