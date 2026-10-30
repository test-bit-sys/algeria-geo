import assert from "node:assert/strict";
import { test } from "node:test";
import {
  getAllCommunes,
  getAllDairas,
  getCommune,
  getCommunes,
  getCommunesByDaira,
  getDaira,
  getDairas,
  getPostalCode,
  getWilaya,
  getWilayaByCommune,
  getWilayaByPhoneCode,
  getWilayasByPhoneCode,
  getWilayas,
  search,
  toDropdownOptions,
} from "../dist/esm/index.js";

test("lookup by code and name", () => {
  assert.equal(getWilaya(16)?.name_fr, "Alger");
  assert.equal(getWilaya("16")?.name_ar, "الجزائر");
  assert.equal(getWilaya("Warqla")?.code, "30");
  assert.equal(getWilaya("تيارت")?.code, "14");
  assert.equal(getWilaya("invalid"), null);
});

test("eras", () => {
  assert.equal(getWilaya(59)?.is_new_wilaya, true);
  assert.equal(getWilaya(59, 58), null);
  assert.equal(getWilayas(58).length, 58);
  assert.equal(getWilayas(48).length, 48);
  assert.equal(getWilayas(69).length, 69);
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

test("daira lookup and relations", () => {
  const daira = getDaira("0301");
  assert.ok(daira);
  assert.equal(daira.wilaya_code, "03");
  assert.equal(daira.name_ar, "الأغواط");

  const communes = getCommunesByDaira("0301");
  assert.ok(communes.length > 0);
  assert.equal(communes[0]?.daira_code, "0301");

  assert.equal(getAllDairas().length, 538);
  assert.equal(getAllCommunes().length, 1541);
});

test("phone code and commune parent lookups", () => {
  const alger = getWilayaByPhoneCode("021");
  assert.equal(alger?.code, "16");
  const algerShort = getWilayaByPhoneCode("21");
  assert.equal(algerShort?.code, "16");

  const blidaArea = getWilayasByPhoneCode("025");
  assert.ok(blidaArea.some((w) => w.code === "09"));
  assert.ok(blidaArea.some((w) => w.code === "26"));

  // Commune to wilaya reverse lookup
  const aflouWilaya69 = getWilayaByCommune("0319", 69);
  assert.equal(aflouWilaya69?.code, "59"); // Aflou is now wilaya 59

  const aflouWilaya58 = getWilayaByCommune("0319", 58);
  assert.equal(aflouWilaya58?.code, "03"); // Historically in Laghouat (03)

  // Verify formerly orphan communes have assigned dairas
  assert.equal(getCommune("0919")?.daira_code, "0926");
  assert.equal(getCommune("3532")?.daira_code, "3502");
  assert.equal(getCommune("3533")?.daira_code, "3502");
});

test("cross-script search and options", () => {
  assert.equal(search("Tiaret").wilayas[0]?.item.code, "14");
  assert.equal(search("تيارت").wilayas[0]?.item.code, "14");
  assert.equal(search("Ouargla").wilayas[0]?.item.code, "30");
  assert.equal(search("Warqla", { limit: 1 }).wilayas.length, 1);
  assert.equal(search("").wilayas.length, 0);

  // Illizi with hamza and Arabizi search
  assert.equal(getWilaya("إليزي")?.code, "33");
  assert.equal(search("إليزي").wilayas[0]?.item.code, "33");
  assert.equal(search("3in defla").wilayas[0]?.item.code, "44");
  assert.equal(search("war9la").wilayas[0]?.item.code, "30");
  assert.equal(search("5nchela").wilayas[0]?.item.code, "40");
});

test("dropdown", () => {
  assert.deepEqual(toDropdownOptions("fr")[0], { value: "01", label: "Adrar" });
  assert.equal(toDropdownOptions().length, 69);
  assert.equal(toDropdownOptions("ar", 58).length, 58);
});

test("postal codes and coordinates", () => {
  assert.equal(getPostalCode("Alger Centre"), "16000");
  assert.equal(getPostalCode("وهران"), "31000");
  const c = getCommune("1601");
  assert.equal(c?.post_code, "16000");
  assert.ok(typeof c?.latitude === "number" && c.latitude > 35);
  assert.ok(typeof c?.longitude === "number" && c.longitude > 2);
});
