<div align="center">

# 🇩🇿 algeria-geo

**Algeria's 69 wilayas, 538 dairas and 1,541 communes, with Arabic/French search and historical boundaries for Python and TypeScript.**

[![PyPI](https://img.shields.io/pypi/v/algeria-geo?logo=pypi)](https://pypi.org/project/algeria-geo/)
[![npm](https://img.shields.io/npm/v/algeria-geo?logo=npm)](https://www.npmjs.com/package/algeria-geo)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![TypeScript](https://img.shields.io/badge/types-included-3178c6)
![Dependencies](https://img.shields.io/badge/runtime%20deps-0-brightgreen)

[English](#english) · [العربية](#العربية)

</div>

---

## English

### Data status

| Layer | Status |
|---|---|
| 69 wilayas (AR / FR / EN, era flags) | ✅ included; codes 59–69 follow Presidential Decree 26-206 |
| Dairas and communes | ✅ 538 dairas and 1,541 communes, including the 2026 reorganization and 48/58/69-era wilaya lineage |
| Postal codes and GPS | ⚠️ fields and API are ready, but these records are not included in the cited official-text dataset |

### Quickstart

**Node.js**
```bash
npm i algeria-geo
```
```js
import { getWilaya, search } from "algeria-geo";
console.log(getWilaya(69)?.name_fr, search("Warqla").wilayas[0]?.item.name_ar);
```

**Python**
```bash
pip install algeria-geo
```
```python
import algeria_geo as geo
print(geo.get_wilaya(69).name_fr, geo.search("Warqla").wilayas[0].item.name_ar)
```

### API (identical in both languages)

| Python | TypeScript | Notes |
|---|---|---|
| `get_wilaya(id, era=69)` | `getWilaya(id, era = 69)` | code (`16`, `"16"`) or name in ar/fr/en, transliteration-tolerant |
| `get_wilayas(era=69)` | `getWilayas(era)` | |
| `get_dairas(code, era=69)` | `getDairas(code, era)` | |
| `get_communes(code, era=69)` | `getCommunes(code, era)` | `era` selects the territorial definition |
| `search(query, lang="any")` | `search(query, lang)` | scored fuzzy match across Arabic and Latin scripts |
| `get_postal_code(name)` | `getPostalCode(name)` | Returns a code only when postal-code data is populated |
| `to_dropdown_options(lang="ar")` | `toDropdownOptions(lang)` | `[{value, label}]` |

Search combines accent and diacritic folding, Arabic letter unification, a drop of the `ال` prefix and a shared phonetic key, so `Ouargla`, `Warqla` and `ورقلة` resolve to the same wilaya.

### Comparison

| | **algeria-geo** | `othmanus/algeria-cities` |
|---|---|---|
| Wilayas | **69** (+ 58 / 48 era views) | 48 (frozen) |
| PyPI / npm packages | ✅ / ✅ | ❌ |
| Postal code and GPS fields | ⚠️ schema is ready; values are not in the current dataset | ❌ |
| Integrity validation (orphans, formats, GPS bounds) | ✅ | ❌ |
| SQL (PostgreSQL / MySQL / SQLite), CSV, JSON, tree | ✅ | partial |
| Types | frozen dataclasses, strict `.d.ts` | none |

### Build from source
```bash
python scripts/build.py --check     # validate canonical data
python scripts/build.py             # dist/, SQL, CSV, package data
python scripts/build.py --strict    # also require dairas, communes, postal codes and GPS
```
Outputs: `dist/wilayas.min.json`, `communes.min.json`, `dairas.min.json`, `tree.min.json`, `dist/csv/*.csv`, `dist/algeria_geo.sql` (PostgreSQL and SQLite), `dist/algeria_geo.mysql.sql`.

Refresh the administrative dataset with `python scripts/import_source.py`, then rebuild. The importer pins [djazairdev/wilayas](https://github.com/djazairdev/wilayas) to a source revision based on the Journal officiel (data license: CC0 1.0). Commune codes remain the ONS codes; 60 communes have no daira in the cited texts, so their `daira_code` is `null`. Postal codes and coordinates remain `null` until a verifiable source is added.

### Migrating from 58 to 69 wilayas

1. **Nothing is removed.** Codes `01`–`58` are unchanged; `59`–`69` are new (`is_new_wilaya: true`).
2. **Pin the old view** with `era=58` (or `48`) to keep legacy behaviour: `get_communes("17", era=58)` still returns every commune Djelfa had before the split.
3. **Communes moved.** In era 69, communes of new wilayas leave their parent. Each record keeps `wilaya_code_58` and `wilaya_code_48`, so you can migrate stored data by mapping the old code to the new `wilaya_code`.
4. **Aggregations change.** Counts per wilaya (`communes_count`) differ in era 69 for the parents: Laghouat, Batna, Biskra, Tébessa, Tlemcen, Tiaret, Djelfa, Médéa, M'Sila, El Bayadh. Verify the exact parents against the decree.
5. **UI selects:** `to_dropdown_options()` now returns 69 entries.
6. **Vehicle plates and external codes** for 59–69 apply from 1 January 2027. Don't assume they match your own legacy systems.

| Code | Wilaya |
|---|---|
| 59 | Aflou (آفلو) |
| 60 | Barika (بريكة) |
| 61 | El Kantara (القنطرة) |
| 62 | Bir El Ater (بئر العاتر) |
| 63 | El Aricha (العريشة) |
| 64 | Ksar Chellala (قصر الشلالة) |
| 65 | Aïn Oussera (عين وسارة) |
| 66 | Messaad (مسعد) |
| 67 | Ksar El Boukhari (قصر البخاري) |
| 68 | Bou Saâda (بوسعادة) |
| 69 | El Abiodh Sidi Cheikh (الأبيض سيدي الشيخ) |

Codes 64–66 are inferred; sources disagree on the numbering. Edit `data/wilayas.json` if the official decree differs.

### License
MIT.

---

## العربية

<div dir="rtl">

### حالة البيانات

| الطبقة | الحالة |
|---|---|
| الولايات الـ 69 (عربي / فرنسي / إنجليزي مع علامات الحقبة) | ✅ متوفرة، وأرقام 59–69 بانتظار التحقق النهائي من الجريدة الرسمية |
| الدوائر والبلديات | ✅ 538 دائرة و1541 بلدية، مع تحديث 2026 وعلاقات الولايات في الحقب 48 و58 و69 |
| الرموز البريدية والإحداثيات | ⚠️ الحقول والواجهة جاهزة، لكن المصدر الرسمي المستورد لا يتضمن هذه البيانات |

لتحديث بيانات التقسيم الإداري شغّل `python scripts/import_source.py` ثم أعد البناء. يعتمد المستورد على [djazairdev/wilayas](https://github.com/djazairdev/wilayas)، المثبت على نسخة موثقة من نصوص الجريدة الرسمية (البيانات بترخيص CC0 1.0). تحتفظ البلديات برموز ONS، و60 بلدية لا تتبع دائرة في المصدر؛ لذلك تكون قيمة `daira_code` لها `null`.

### البدء السريع

**Node.js**
```bash
npm i algeria-geo
```
```js
import { getWilaya, search } from "algeria-geo";
console.log(getWilaya(69)?.name_ar, search("Warqla").wilayas[0]?.item.name_ar);
```

**Python**
```bash
pip install algeria-geo
```
```python
import algeria_geo as geo
print(geo.get_wilaya(69).name_ar, geo.search("Warqla").wilayas[0].item.name_ar)
```

### الواجهة البرمجية

الدوال متطابقة في اللغتين: `get_wilaya` و`get_communes` و`search` و`get_postal_code` و`to_dropdown_options` (وفي TypeScript: `getWilaya` وغيرها). يقبل البحث الأحرف العربية واللاتينية ويتسامح مع اختلافات النقل الحرفي، فـ `Ouargla` و`Warqla` و`ورقلة` تُرجع الولاية نفسها.

### الانتقال من 58 إلى 69 ولاية

1. **لا يُحذف شيء:** الرموز `01`–`58` كما هي، و`59`–`69` جديدة (`is_new_wilaya: true`).
2. **للإبقاء على السلوك القديم** استخدم `era=58` (أو `48`).
3. **انتقال البلديات:** في حقبة 69 تخرج بلديات الولايات الجديدة من ولاياتها الأم؛ يحتفظ كل سجل بالحقلين `wilaya_code_58` و`wilaya_code_48` لتسهيل ترحيل بياناتك المخزنة.
4. **تتغيّر الإحصاءات** للولايات الأم (الأغواط، باتنة، بسكرة، تبسة، تلمسان، تيارت، الجلفة، المدية، المسيلة، البيض). تحقق من الولايات الأم بدقة من المرسوم.
5. **القوائم المنسدلة:** تُرجع `to_dropdown_options()` الآن 69 عنصراً.
6. **ترقيم المركبات** للولايات 59–69 يسري اعتباراً من 1 جانفي 2027.

</div>
