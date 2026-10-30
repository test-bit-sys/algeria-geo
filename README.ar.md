<a id="top"></a>

<p align="right">
  <a href="./README.md">English</a> &nbsp;|&nbsp;
  <strong>العربية</strong> &nbsp;|&nbsp;
  <a href="./README.fr.md">Français</a>
</p>

<div align="center">

  <a href="https://github.com/test-bit-sys/algeria-geo">
    <img src="assets/logo.png" alt="شعار algeria-geo" width="720" style="border-radius: 16px; max-width: 100%; box-shadow: 0 10px 30px rgba(0,0,0,0.3);" />
  </a>

  <br/><br/>

  # 🇩🇿 algeria-geo

  **المكتبة المعيارية الشاملة للتقسيم الإداري والجغرافي للجمهورية الجزائرية بدون أي اعتماديات تشغيل خارجية.**<br/>
  *69 ولاية، 538 دائرة، و1,541 بلدية مع دعم الحقب الإدارية التاريخية (48، 58، 69) والبحث الذكي متعدد اللغات.*

  <br/>

  [![CI](https://github.com/test-bit-sys/algeria-geo/actions/workflows/ci.yml/badge.svg)](https://github.com/test-bit-sys/algeria-geo/actions/workflows/ci.yml)
  [![PyPI](https://img.shields.io/pypi/v/algeria-geo?logo=pypi&color=blue)](https://pypi.org/project/algeria-geo/)
  [![npm](https://img.shields.io/npm/v/algeria-geo?logo=npm&color=red)](https://www.npmjs.com/package/algeria-geo/)
  [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://pypi.org/project/algeria-geo/)
  [![TypeScript](https://img.shields.io/badge/typescript-ready-3178C6?logo=typescript&logoColor=white)](https://www.npmjs.com/package/algeria-geo/)
  [![Runtime Dependencies](https://img.shields.io/badge/runtime%20deps-0-brightgreen.svg)](#المميزات-الرئيسية)

</div>

---

<div dir="rtl">

## جدول المحتويات

- [المميزات الرئيسية](#المميزات-الرئيسية)
- [التغطية الإدارية الرسمية](#التغطية-الإدارية-الرسمية)
- [التثبيت](#التثبيت)
- [أمثلة الاستخدام السريع](#أمثلة-الاستخدام-السريع)
  - [TypeScript / JavaScript](#typescript--javascript)
  - [Python](#python)
- [جدول الواجهة البرمجية (API)](#جدول-الواجهة-البرمجية-api)
- [الحقب الإدارية التاريخية (48، 58، 69)](#الحقب-الإدارية-التاريخية-48-58-69)
- [توزيعات البيانات الجاهزة (SQL, CSV, JSON)](#توزيعات-البيانات-الجاهزة)
- [مصدر البيانات والتراخيص](#مصدر-البيانات-والتراخيص)
- [البناء من المصدر](#البناء-من-المصدر)
- [المساهمة في المشروع](#المساهمة)
- [الترخيص](#الترخيص)

---

## المميزات الرئيسية

- 🇩🇿 **تغطية إدارية شاملة وموثقة**: كافة **الولايات الـ 69** (بما في ذلك التقسيم الإداري لعام 2026: الولايات 59 إلى 69)، **538 دائرة**، و**1,541 بلدية**.
- ⏳ **دعم الحقب الإدارية التاريخية**: استخراج حدود وبلديات الولايات كما كانت في حقبة **48 ولاية** (1984)، **58 ولاية** (2019)، والتقسيم الحالي **69 ولاية** (2026).
- 🔍 **بحث تقريبي ذكي عابر للغات**: معالجة متقدمة لعلامات التشكيل والتنوين، الهمزات، الحركات الصوتية اللاتينية، والنقل الحرفي الصوتي (مثل: `Warqla` = `Ouargla` = `ورقلة`).
- ⚡ **أداء فائق بدون أي اعتماديات خارجية**: تطبيق مبني بالكامل على المكتبات القياسية مع استعلامات فورية في الذاكرة بتعقيد زمني $O(1)$.
- 📦 **تطابق تام بين اللغتين**: توافق كامل للوظائف والنماذج والأداء بين بيئتي **TypeScript** (ESM + CommonJS) و**Python** (مع كامل التلميحات النوعية Typed).
- 🗄️ **توزيعات جاهزة متعددة الصيغ**: ملفات SQL جاهزة للاستيراد المباشر (PostgreSQL، SQLite، MySQL / MariaDB)، ملفات JSON مصغرة، شجرة هيكلية كاملة، وملفات CSV بترميز UTF-8 مع BOM.

---

## التغطية الإدارية الرسمية

| المستوى الإداري | العدد | المعرفات | اللغات المتوفرة |
|---|:---:|---|---|
| **الولايات** | **69** | `01` – `69` (رمز ONS المكون من خانتين) | العربية، الفرنسية، والنقل اللاتيني ASCII |
| **الدوائر** | **538** | `0101` – `6912` (رمز من 4 خانات) | العربية، الفرنسية، والنقل اللاتيني ASCII |
| **البلديات** | **1,541** | `0101` – `6912` (رمز ONS الرباعي) | العربية، الفرنسية، والنقل اللاتيني ASCII |

> [!NOTE]
> الأسماء متوفرة باللغتين العربية (`name_ar`) والفرنسية (`name_fr`). يمثل الحقل `name_en` صيغة بحروف ASCII لاتينية مشتقة من التهجئة الرسمية لتسهيل البحث. الرموز البريدية الرسمية (`post_code`) المكونة من 5 أرقام والإحداثيات الجغرافية (`latitude` و `longitude`) متوفرة ومحققة لكافة البلديات الـ 1,541، مع توفير مؤشرات الهاتف الثابت (`phone_code`) لكافة الولايات الـ 69.

---

## التثبيت

### في بيئة Node.js / TypeScript

```bash
# npm
npm install algeria-geo

# pnpm
pnpm add algeria-geo

# yarn
yarn add algeria-geo

# bun
bun add algeria-geo
```

### في بيئة Python

```bash
# pip
pip install algeria-geo

# uv
uv add algeria-geo

# poetry
poetry add algeria-geo
```

---

## أمثلة الاستخدام السريع

### TypeScript / JavaScript

تعمل المكتبة بسلاسة في Node.js، Bun، Deno، Next.js، Nuxt، Vite، والمتصفحات:

```ts
import {
  getWilaya,
  getDaira,
  getCommune,
  getCommunes,
  getWilayaByPhoneCode,
  getWilayaByCommune,
  search,
  toDropdownOptions,
} from "algeria-geo";

// 1. الاستعلام المباشر عن ولاية برمزها أو اسمها
const alger = getWilaya(16); // يقبل الرقم 16 أو "16" أو "Alger" أو "الجزائر"
console.log(alger?.name_ar); // "الجزائر"
console.log(alger?.communes_count); // 57

// 2. الاستعلام عن الدوائر والبلديات
const daira = getDaira("0301");
console.log(daira?.name_ar); // "الأغواط"

const commune = getCommune("0319");
console.log(commune?.name_ar); // "أفلو"
console.log(commune?.wilaya_code); // "59" (ولاية جديدة ضمن تقسيم 2026)

// 3. الاستعلام العكسي (معرفة الولاية التابعة لها بلدية عبر الحقب التاريخية)
console.log(getWilayaByCommune("0319", 69)?.name_ar); // "أفلو" (في تقسيم 69 ولاية)
console.log(getWilayaByCommune("0319", 58)?.name_ar); // "الأغواط" (في تقسيم 58 ولاية)

// 4. الاستعلام بواسطة رمز الهاتف الثابت
console.log(getWilayaByPhoneCode("021")?.name_ar); // "الجزائر"

// 5. البحث التقريبي الذكي عابر اللغات
const results = search("Warqla", { limit: 5 });
console.log(results.wilayas[0]?.item.name_ar); // "ورقلة"
console.log(results.wilayas[0]?.score); // 0.85

// 6. تجهيز خيارات قوائم الاختيار في واجهات الويب (Dropdown Select)
const options = toDropdownOptions("ar");
// [{ value: "01", label: "أدرار" }, { value: "02", label: "الشلف" }, ...]
```

### Python

```python
import algeria_geo as geo

# 1. الاستعلام المباشر بالرقم أو الاسم
alger = geo.get_wilaya(16)  # يقبل int أو str: "16", "Alger", "الجزائر"
print(alger.name_ar)         # "الجزائر"
print(alger.communes_count)  # 57

# 2. الاستعلام عن دائرة وبلدية
daira = geo.get_daira("0301")
print(daira.name_ar)  # "الأغواط"

commune = geo.get_commune("0319")
print(commune.name_ar)       # "أفلو"
print(commune.wilaya_code)   # "59" (أفلو ولاية في تقسيم 69)

# 3. الاستعلام العكسي للولاية التابعة لها بلدية عبر الحقب
print(geo.get_wilaya_by_commune("0319", era=69).name_ar)  # "أفلو"
print(geo.get_wilaya_by_commune("0319", era=58).name_ar)  # "الأغواط"

# 4. الاستعلام بواسطة رمز الهاتف الثابت
print(geo.get_wilaya_by_phone_code("021").name_ar)  # "الجزائر"

# 5. البحث التقريبي الذكي متعدد اللغات
res = geo.search("Ouargla")
print(res.wilayas[0].item.name_ar)  # "ورقلة"
print(res.best.score)               # 1.0

# 6. التحويل إلى قاموس (Dict / JSON) لتطبيقات الويب (FastAPI / Django)
import json
print(json.dumps(commune.to_dict(), ensure_ascii=False))

# 7. تجهيز خيارات القوائم المنسدلة
dropdown = geo.to_dropdown_options(lang="ar")
# [{"value": "01", "label": "أدرار"}, {"value": "02", "label": "الشلف"}, ...]
```

---

## جدول الواجهة البرمجية (API)

| دالة Python | دالة TypeScript | الغرض والوظيفة |
|---|---|---|
| `get_wilaya(id, era=69)` | `getWilaya(id, era = 69)` | جلب ولاية بالرمز الرقمي (`16`، `"16"`) أو بالاسم (عربي / فرنسي / لاتيني) |
| `get_wilayas(era=69)` | `getWilayas(era = 69)` | عرض قائمة الولايات التابعة لحقبة إدارية معينة |
| `get_daira(code)` | `getDaira(code)` | جلب دائرة برمزها الرباعي |
| `get_dairas(wilaya_code, era=69)` | `getDairas(wilayaCode, era = 69)` | جلب جميع الدوائر التابعة لولاية محددة |
| `get_all_dairas(era=69)` | `getAllDairas(era = 69)` | عرض جميع دوائر القطر الجزائري في حقبة معينة |
| `get_commune(code)` | `getCommune(code)` | جلب بلدية برمز ONS الرباعي |
| `get_communes(wilaya_code, era=69)`| `getCommunes(wilayaCode, era = 69)`| جلب جميع بلديات ولاية محددة |
| `get_all_communes(era=69)` | `getAllCommunes(era = 69)` | عرض جميع بلديات القطر الجزائري في حقبة معينة |
| `get_communes_by_daira(daira_code)`| `getCommunesByDaira(dairaCode)` | جلب البلديات التابعة لدائرة معينة |
| `get_wilaya_by_commune(code, era=69)`| `getWilayaByCommune(code, era = 69)`| معرفة الولاية التي تنتمي إليها بلدية معينة |
| `get_wilaya_by_phone_code(phone)` | `getWilayaByPhoneCode(phone)` | جلب الولاية انطلاقاً من رمز الهاتف الثابت (مثل `"021"`) |
| `search(query, lang, limit)` | `search(query, langOrOptions, limit)` | بحث تقريبي ذكي عابر للغات في الولايات والدوائر والبلديات |
| `get_postal_code(name, wilaya)` | `getPostalCode(name, wilaya)` | جلب الرمز البريدي عند توفر بياناته |
| `to_dropdown_options(lang, era)` | `toDropdownOptions(lang, era)` | تجهيز مصفوفة خيارات لقوائم الاختيار في واجهات الويب |

---

## الحقب الإدارية التاريخية (48، 58، 69)

مر التقسيم الإداري للجمهورية الجزائرية بثلاث محطات تشريعية كبرى:

```mermaid
flowchart LR
    A["تقسيم 1984 (قانون 84-09)<br/><b>48 ولاية</b>"] --> B["تقسيم 2019 (قانون 19-12)<br/><b>58 ولاية</b>"]
    B --> C["تقسيم 2026<br/><b>69 ولاية</b>"]
```

تحتفظ `algeria-geo` بالنسب الإداري التاريخي كاملاً، بحيث يمكنك عبر تمرير `era=48` أو `era=58` استخراج البيانات بدقة تاريخية:

```python
# في نظام 58 ولاية، كانت بلدية أفلو تابعة لولاية الأغواط (03)
communes_58 = geo.get_communes("03", era=58)

# في النظام الحالي (69 ولاية)، أصبحت أفلو ولاية قائمة بذاتها (59)
communes_69 = geo.get_communes("59", era=69)
```

---

## توزيعات البيانات الجاهزة

تتوفر جميع ملفات التوزيع في مجلد [`dist/`](dist/):

| الملف | الصيغة | الوصف |
|---|:---:|---|
| [`dist/wilayas.min.json`](dist/wilayas.min.json) | JSON | مصفوفة مصغرة للولايات الـ 69 مع عدد الدوائر والبلديات |
| [`dist/dairas.min.json`](dist/dairas.min.json) | JSON | مصفوفة مصغرة للدوائر الـ 538 مع الرموز التاريخية |
| [`dist/communes.min.json`](dist/communes.min.json) | JSON | مصفوفة مصغرة للبلديات الـ 1,541 مع شجرة النسب الإداري |
| [`dist/tree.min.json`](dist/tree.min.json) | JSON | شجرة هرمية متداخلة: ولايات ➔ دوائر ➔ بلديات |
| [`dist/csv/*.csv`](dist/csv/) | CSV | ملفات CSV مهيأة بترميز UTF-8 مع BOM لبرنامج Excel |
| [`dist/algeria_geo.sql`](dist/algeria_geo.sql) | SQL | سكربت DDL وINSERT جاهز لقواعد بيانات PostgreSQL وSQLite |
| [`dist/algeria_geo.mysql.sql`](dist/algeria_geo.mysql.sql) | SQL | سكربت مخصص لقواعد بيانات MySQL 8 وMariaDB (`utf8mb4`) |

---

## مصدر البيانات والتراخيص

البيانات الأساسية مستندة إلى المستودع [djazairdev/wilayas](https://github.com/djazairdev/wilayas/tree/0b3b6ab2ac1b1569469285d8fe5e7df18666fcdf)، وهي مجموعة بيانات مفتوحة منقولة وموثقة مباشرة عن المراسيم والنصوص المنشورة في الجريدة الرسمية للجمهورية الجزائرية الديمقراطية الشعبية.

- توجد 60 بلدية لا تتبع أي دائرة في السجلات الرسمية المعتمدة؛ لذلك تكون قيمة `daira_code` لديها `null`.
- كود المكتبة البرمجي منشور تحت ترخيص **MIT**.
- مجموعة البيانات الإدارية تقع ضمن الملك العام تحت رخصة المشاع الإبداعي **CC0 1.0 Universal**.

---

## البناء من المصدر

```bash
# 1. التحقق من سلامة البيانات
python scripts/build.py --check

# 2. بناء التوزيعات وحزم الكود
python scripts/build.py

# 3. إعادة استيراد أحدث بيانات من المصدر
python scripts/import_source.py
python scripts/build.py
```

---

## المساهمة

المساهمات مرحب بها دائماً! يرجى مراجعة ملف [CONTRIBUTING.md](CONTRIBUTING.md) للتعرف على شروط توثيق البيانات من الجريدة الرسمية ومعايير الكود.

---

## الترخيص

الكود البرمجي مرخص بموجب [رخصة MIT](LICENSE).  
البيانات الإدارية تقع ضمن الملك العام بموجب [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).

</div>

---

<p align="right"><a href="#top">الرجوع لأعلى الصفحة ↑</a></p>
