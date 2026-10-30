import { readdirSync, readFileSync } from "node:fs";
import { gzipSync } from "node:zlib";

let raw = 0;
let gz = 0;
for (const f of readdirSync("dist/esm").filter((n) => n.endsWith(".js"))) {
  const buf = readFileSync(`dist/esm/${f}`);
  raw += buf.length;
  gz += gzipSync(buf, { level: 9 }).length;
}
console.log(`ESM total: ${(raw / 1024).toFixed(1)} KB raw, ${(gz / 1024).toFixed(1)} KB gzip`);
if (gz > 75 * 1024) {
  console.error("over the 75 KB gzip budget");
  process.exit(1);
}
