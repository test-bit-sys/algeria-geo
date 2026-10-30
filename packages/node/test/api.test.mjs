import assert from "node:assert/strict";
import { test } from "node:test";
import { getCommune, getCommunes, getDairas, getWilaya, getWilayas, search, toDropdownOptions } from "../dist/esm/index.js";

test("lookup by code and name", () => {
  assert.equal(getWilaya(16)?.name_fr, "Alger");
  assert.equal(getWilaya("Warqla")?.code, "30");
  assert.equal(getWilaya("تيارت")?.code, "14");
});

test("eras", () => {
  assert.equal(getWilaya(59)?.is_new_wilaya, true);
  assert.equal(getWilaya(59, 58), null);
  assert.equal(getWilayas(58).length, 58);
  assert.throws(() => getWilaya(1, 50));
});

test("official commune and daira coverage", () => {
  assert.equal(getCommunes("16").length, 57);
  assert.equal(getDairas("16").length, 0);
  assert.equal(getCommune("1601")?.daira_code, null);
  assert.equal(getCommunes("59").length, 12);
  assert.equal(getCommune("0319")?.name_fr, "Aflou");
  assert.equal(getCommune("0319")?.wilaya_code_58, "03");
  assert.equal(getWilayas().flatMap((w) => getCommunes(w.code)).length, 1541);
});

test("cross-script search", () => {
  assert.equal(search("Tiaret").wilayas[0]?.item.code, "14");
  assert.equal(search("تيارت").wilayas[0]?.item.code, "14");
  assert.equal(search("Ouargla").wilayas[0]?.item.code, "30");
});

test("dropdown", () => {
  assert.deepEqual(toDropdownOptions("fr")[0], { value: "01", label: "Adrar" });
  assert.equal(toDropdownOptions().length, 69);
});
