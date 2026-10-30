<a id="top"></a>

<p align="right"><a href="#english">English</a> | <a href="#arabic">العربية</a></p>

<div align="center">

# 🇩🇿 algeria-geo

**Algeria's 69 wilayas, 538 dairas and 1,541 communes, with Arabic/French search and historical boundaries for Python and TypeScript.**

[![PyPI](https://img.shields.io/pypi/v/algeria-geo?logo=pypi)](https://pypi.org/project/algeria-geo/)
[![npm](https://img.shields.io/npm/v/algeria-geo?logo=npm)](https://www.npmjs.com/package/algeria-geo/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![TypeScript](https://img.shields.io/badge/types-included-3178c6)
![Dependencies](https://img.shields.io/badge/runtime%20deps-0-brightgreen)

</div>

<a id="english"></a>

## English

### Overview

`algeria-geo` is a zero-runtime-dependency library for looking up and searching Algeria's administrative divisions. Python and TypeScript expose matching APIs, typed records, Arabic/French names, and historical views of the 48-, 58-, and 69-wilaya boundaries.

| Data | Coverage |
|---|---:|
| Wilayas | 69 |
| Dairas | 538 |
| Communes | 1,541 |

Names are provided in Arabic and French. The `name_en` field is an ASCII-friendly form derived from the French name, not an English translation. Postal-code and coordinate fields are part of the schema but currently `null` because the pinned administrative source does not provide those records.

### Install

**Node.js**

```bash
npm install algeria-geo
```

**Python**

```bash
pip install algeria-geo
```

### Quick start

**TypeScript / JavaScript**

```ts
import { getCommune, getCommunes, search } from "algeria-geo";

console.log(getCommune("0319")?.name_ar); // أفلو
console.log(getCommune("0319")?.wilaya_code); // 59
console.log(getCommunes("03", 58).length); // communes in the 58-wilaya view
console.log(search("Warqla").wilayas[0]?.item.name_ar); // ورقلة
```

**Python**

```python
import algeria_geo as geo

print(geo.get_commune("0319").name_ar)  # أفلو
print(geo.get_commune("0319").wilaya_code)  # 59
print(len(geo.get_communes("03", era=58)))
print(geo.search("Warqla").wilayas[0].item.name_ar)  # ورقلة
```

### API

| Python | TypeScript | Purpose |
|---|---|---|
| `get_wilaya(id, era=69)` | `getWilaya(id, era = 69)` | Look up a wilaya by code or Arabic/French name |
| `get_wilayas(era=69)` | `getWilayas(era)` | List wilayas in a boundary era |
| `get_dairas(code, era=69)` | `getDairas(code, era)` | List a wilaya's dairas |
| `get_communes(code, era=69)` | `getCommunes(code, era)` | List a wilaya's communes |
| `get_commune(code)` | `getCommune(code)` | Look up a commune by ONS code |
| `search(query, lang="any")` | `search(query, lang)` | Fuzzy search across wilayas, dairas and communes |
| `get_postal_code(name)` | `getPostalCode(name)` | Look up a postal code when postal data is populated |
| `to_dropdown_options(lang="ar")` | `toDropdownOptions(lang)` | Create wilaya select options |

`era` can be `48`, `58`, or `69`. Search folds accents and Arabic diacritics, unifies common Arabic letter variants, and tolerates transliteration differences. For example, `Ouargla`, `Warqla`, and `ورقلة` find the same wilaya.

### Data and boundaries

The canonical data is pinned to [djazairdev/wilayas](https://github.com/djazairdev/wilayas/tree/0b3b6ab2ac1b1569469285d8fe5e7df18666fcdf), a CC0 dataset transcribed from cited texts in Algeria's Journal officiel. The 2026 reorganization is represented in the current 69-wilaya view; `wilaya_code_58` and `wilaya_code_48` preserve the earlier assignments for migration and historical queries.

Sixty communes have no daira assignment in the cited records, so their `daira_code` is `null`. Postal codes and latitude/longitude are not included in this source and remain `null`; `get_postal_code` therefore returns no result until a verified postal dataset is added.

### Build from source

```bash
python scripts/build.py --check
python scripts/build.py
```

To refresh the administrative source and rebuild:

```bash
python scripts/import_source.py
python scripts/build.py
```

`--strict` also requires postal codes and coordinates to be populated. Build outputs include minified JSON, CSV, a nested tree, and SQL for PostgreSQL, SQLite, and MySQL.

### License

Library code is MIT. The imported administrative dataset is CC0 1.0; see the linked source for its citations and data terms.

<p align="right"><a href="#arabic">العربية</a> · <a href="#top">Back to top</a></p>

<a id="arabic"></a>

## العربية

<div dir="rtl">

### نبذة

`algeria-geo` مكتبة بلا اعتماديات وقت التشغيل للبحث والاستعلام عن التقسيم الإداري في الجزائر. توفر واجهتين متقاربتين لـPython وTypeScript، وسجلات مكتوبة الأنواع، وأسماء بالعربية والفرنسية، وإمكانية الاستعلام وفق حدود الولايات في الحقب 48 و58 و69.

| البيانات | العدد |
|---|---:|
| الولايات | 69 |
| الدوائر | 538 |
| البلديات | 1541 |

الأسماء متوفرة بالعربية والفرنسية. الحقل `name_en` صيغة لاتينية ASCII مشتقة من الاسم الفرنسي، وليس ترجمة إنجليزية. حقول الرمز البريدي والإحداثيات موجودة في المخطط، لكن قيمها `null` حالياً لأن مصدر التقسيم المثبت لا يتضمنها.

### التثبيت

**Node.js**

```bash
npm install algeria-geo
```

**Python**

```bash
pip install algeria-geo
```

### بدء سريع

**TypeScript / JavaScript**

```ts
import { getCommune, getCommunes, search } from "algeria-geo";

console.log(getCommune("0319")?.name_ar); // أفلو
console.log(getCommune("0319")?.wilaya_code); // 59
console.log(getCommunes("03", 58).length); // البلديات ضمن تقسيم 58 ولاية
console.log(search("Warqla").wilayas[0]?.item.name_ar); // ورقلة
```

**Python**

```python
import algeria_geo as geo

print(geo.get_commune("0319").name_ar)  # أفلو
print(geo.get_commune("0319").wilaya_code)  # 59
print(len(geo.get_communes("03", era=58)))
print(geo.search("Warqla").wilayas[0].item.name_ar)  # ورقلة
```

### الواجهة البرمجية

| Python | TypeScript | الوظيفة |
|---|---|---|
| `get_wilaya(id, era=69)` | `getWilaya(id, era = 69)` | جلب ولاية بالرمز أو بالاسم العربي/الفرنسي |
| `get_wilayas(era=69)` | `getWilayas(era)` | عرض الولايات وفق حقبة التقسيم |
| `get_dairas(code, era=69)` | `getDairas(code, era)` | عرض دوائر الولاية |
| `get_communes(code, era=69)` | `getCommunes(code, era)` | عرض بلديات الولاية |
| `get_commune(code)` | `getCommune(code)` | جلب بلدية برمز ONS |
| `search(query, lang="any")` | `search(query, lang)` | بحث تقريبي في الولايات والدوائر والبلديات |
| `get_postal_code(name)` | `getPostalCode(name)` | جلب الرمز البريدي عند توفر بياناته |
| `to_dropdown_options(lang="ar")` | `toDropdownOptions(lang)` | تجهيز خيارات قائمة الولايات |

تقبل `era` القيم `48` أو `58` أو `69`. يطوي البحث اختلافات التشكيل واللكنات، ويوحّد بعض أشكال الحروف العربية، ويتسامح مع اختلافات النقل الحرفي. لذلك تؤدي `Ouargla` و`Warqla` و`ورقلة` إلى الولاية نفسها.

### البيانات والحقب

البيانات الأساسية مثبتة على [djazairdev/wilayas](https://github.com/djazairdev/wilayas/tree/0b3b6ab2ac1b1569469285d8fe5e7df18666fcdf)، وهي مجموعة بترخيص CC0 منقولة عن نصوص موثقة في الجريدة الرسمية الجزائرية. يتضمن العرض الحالي إعادة التنظيم الإداري لعام 2026؛ ويحفظ الحقلان `wilaya_code_58` و`wilaya_code_48` الولايات السابقة لتسهيل الترحيل والاستعلام التاريخي.

ستون بلدية لا تتبع دائرة في السجلات المعتمدة، لذلك تكون قيمة `daira_code` لديها `null`. لا يتضمن هذا المصدر الرموز البريدية أو الإحداثيات، وتبقى قيمها `null` إلى حين إضافة مصدر موثوق؛ لذلك لن يعيد `get_postal_code` نتيجة حالياً.

### البناء من المصدر

```bash
python scripts/build.py --check
python scripts/build.py
```

لتحديث بيانات التقسيم ثم إعادة البناء:

```bash
python scripts/import_source.py
python scripts/build.py
```

يتطلب الخيار `--strict` أيضاً توفر الرموز البريدية والإحداثيات. تشمل مخرجات البناء JSON مصغراً وCSV وشجرة متداخلة وملفات SQL لـPostgreSQL وSQLite وMySQL.

### الترخيص

كود المكتبة بترخيص MIT. مجموعة البيانات المستوردة بترخيص CC0 1.0؛ راجع المصدر المرتبط للاطلاع على المراجع وشروط البيانات.

</div>

<p align="right"><a href="#english">English</a> · <a href="#top">أعلى الصفحة</a></p>