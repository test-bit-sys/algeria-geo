import algeria_geo as dz
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import csv
from pathlib import Path
import shutil

out_dir = Path("exports")
out_dir.mkdir(exist_ok=True)

wilayas = dz.get_wilayas()
w_map = {w.code: w for w in wilayas}
dairas = dz.get_all_dairas()
d_map = {d.code: d for d in dairas}

# Sort communes logically by wilaya_code (01 to 69) and then commune code
communes = sorted(
    dz.get_all_communes(),
    key=lambda c: (int(c.wilaya_code), int(c.code) if c.code.isdigit() else c.code)
)

header_fill_blue = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
header_fill_green = PatternFill(start_color="15803D", end_color="15803D", fill_type="solid")
header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
cell_font = Font(name="Segoe UI", size=10)
thin_border = Border(
    left=Side(style='thin', color='D1D5DB'),
    right=Side(style='thin', color='D1D5DB'),
    top=Side(style='thin', color='D1D5DB'),
    bottom=Side(style='thin', color='D1D5DB')
)

def style_ws(ws, is_rtl=True, header_fill=header_fill_blue):
    ws.views.sheetView[0].rightToLeft = is_rtl
    for col_idx, col in enumerate(ws.columns, 1):
        header_cell = ws.cell(row=1, column=col_idx)
        header_cell.fill = header_fill
        header_cell.font = header_font
        header_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.row_dimensions[1].height = 28
        
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = max(max_len + 5, 14)
        
        for row_idx in range(2, ws.max_row + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = cell_font
            cell.border = thin_border
            # Center postal codes and numeric columns
            if isinstance(cell.value, (int, float)) or (isinstance(cell.value, str) and cell.value.isdigit()):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(vertical="center")

# =========================================================================
# 1. Custom Simplified Workbook: exactly as requested by the user's client
# Columns: البلدية | Commune | الرمز البريدي | الولاية | رقم الولاية
# =========================================================================
wb_simple = openpyxl.Workbook()
ws_simple = wb_simple.active
ws_simple.title = "بلديات الجزائر - 69 ولاية"

headers_simple = [
    "البلدية",
    "Commune",
    "الرمز البريدي",
    "الولاية",
    "رقم الولاية"
]
ws_simple.append(headers_simple)

simple_rows = []
for c in communes:
    w = w_map.get(c.wilaya_code)
    w_name_ar = w.name_ar if w else ""
    row = [
        f"بلدية {c.name_ar}",
        c.name_fr,
        c.post_code or "",
        f"ولاية {w_name_ar}",
        c.wilaya_code
    ]
    ws_simple.append(row)
    simple_rows.append(row)

style_ws(ws_simple, is_rtl=True, header_fill=header_fill_green)

simple_xlsx_path = out_dir / "algeria_communes_69_simple.xlsx"
wb_simple.save(simple_xlsx_path)

simple_csv_path = out_dir / "algeria_communes_69_simple.csv"
with open(simple_csv_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers_simple)
    writer.writerows(simple_rows)

print(f"Saved simple files: {simple_xlsx_path} and {simple_csv_path}")

# =========================================================================
# 2. Update Comprehensive Workbook (sorted strictly 01 to 69)
# =========================================================================
wb_comp = openpyxl.Workbook()
wb_comp.remove(wb_comp.active)

# Sheet 1: All in one
ws_all = wb_comp.create_sheet(title="قائمة شاملة - All")
all_headers = [
    "رقم الولاية\nN° Wilaya",
    "اسم الولاية (عربي)\nNom Wilaya (Ar)",
    "اسم الولاية (فرنسي)\nNom Wilaya (Fr)",
    "رمز الدائرة\nCode Daïra",
    "اسم الدائرة (عربي)\nNom Daïra (Ar)",
    "اسم الدائرة (فرنسي)\nNom Daïra (Fr)",
    "رمز البلدية\nCode Commune",
    "اسم البلدية (عربي)\nNom Commune (Ar)",
    "اسم البلدية (فرنسي)\nNom Commune (Fr)",
    "الرمز البريدي\nCode Postal",
    "خط العرض\nLatitude",
    "خط الطول\nLongitude"
]
ws_all.append(all_headers)

all_rows_for_csv = []
for c in communes:
    w = w_map.get(c.wilaya_code)
    d = d_map.get(c.daira_code)
    row = [
        c.wilaya_code,
        w.name_ar if w else "",
        w.name_fr if w else "",
        c.daira_code or "",
        d.name_ar if d else "",
        d.name_fr if d else "",
        c.code,
        c.name_ar,
        c.name_fr,
        c.post_code or "",
        c.latitude if c.latitude is not None else "",
        c.longitude if c.longitude is not None else ""
    ]
    ws_all.append(row)
    all_rows_for_csv.append(row)

style_ws(ws_all, is_rtl=True, header_fill=header_fill_blue)

# Sheet 2: Wilayas (1 to 69)
ws_w = wb_comp.create_sheet(title="الولايات - Wilayas")
w_headers = [
    "رقم الولاية\nCode",
    "اسم الولاية (عربي)\nNom (Ar)",
    "اسم الولاية (فرنسي)\nNom (Fr)",
    "اسم الولاية (إنجليزي)\nNom (En)",
    "رمز الهاتف\nCode Tél",
    "عدد الدوائر\nNb Daïras",
    "عدد البلديات\nNb Communes",
    "ولاية جديدة (2026)\nNouvelle Wilaya"
]
ws_w.append(w_headers)
for w in sorted(wilayas, key=lambda x: int(x.code)):
    ws_w.append([
        w.code,
        w.name_ar,
        w.name_fr,
        w.name_en,
        w.phone_code,
        w.dairas_count,
        w.communes_count,
        "نعم" if w.is_new_wilaya else "لا"
    ])
style_ws(ws_w, is_rtl=True, header_fill=header_fill_blue)

# Sheet 3: Dairas (sorted by wilaya then daira)
ws_d = wb_comp.create_sheet(title="الدوائر - Dairas")
d_headers = [
    "رمز الدائرة\nCode Daïra",
    "رقم الولاية\nCode Wilaya",
    "اسم الدائرة (عربي)\nNom Daïra (Ar)",
    "اسم الدائرة (فرنسي)\nNom Daïra (Fr)",
    "اسم الولاية (عربي)\nNom Wilaya (Ar)",
    "اسم الولاية (فرنسي)\nNom Wilaya (Fr)"
]
ws_d.append(d_headers)
for d in sorted(dairas, key=lambda x: (int(x.wilaya_code), int(x.code) if x.code.isdigit() else x.code)):
    w = w_map.get(d.wilaya_code)
    ws_d.append([
        d.code,
        d.wilaya_code,
        d.name_ar,
        d.name_fr,
        w.name_ar if w else "",
        w.name_fr if w else ""
    ])
style_ws(ws_d, is_rtl=True, header_fill=header_fill_blue)

# Sheet 4: Communes
ws_c = wb_comp.create_sheet(title="البلديات - Communes")
c_headers = [
    "رمز البلدية\nCode Commune",
    "اسم البلدية (عربي)\nNom Commune (Ar)",
    "اسم البلدية (فرنسي)\nNom Commune (Fr)",
    "رمز الدائرة\nCode Daïra",
    "رقم الولاية\nCode Wilaya",
    "الرمز البريدي\nCode Postal",
    "خط العرض\nLatitude",
    "خط الطول\nLongitude"
]
ws_c.append(c_headers)
for c in communes:
    ws_c.append([
        c.code,
        c.name_ar,
        c.name_fr,
        c.daira_code or "",
        c.wilaya_code,
        c.post_code or "",
        c.latitude if c.latitude is not None else "",
        c.longitude if c.longitude is not None else ""
    ])
style_ws(ws_c, is_rtl=True, header_fill=header_fill_blue)

comp_xlsx_path = out_dir / "algeria_geo_69_wilayas.xlsx"
wb_comp.save(comp_xlsx_path)

comp_csv_path = out_dir / "algeria_complete.csv"
with open(comp_csv_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    clean_headers = [h.replace("\n", " / ") for h in all_headers]
    writer.writerow(clean_headers)
    writer.writerows(all_rows_for_csv)

print(f"Updated comprehensive files: {comp_xlsx_path} and {comp_csv_path}")

# Copy to user desktop for convenience
desktop = Path(r"C:\Users\safou\Desktop")
if desktop.exists():
    shutil.copy(simple_xlsx_path, desktop / "algeria_communes_69_simple.xlsx")
    shutil.copy(simple_csv_path, desktop / "algeria_communes_69_simple.csv")
    shutil.copy(comp_xlsx_path, desktop / "algeria_geo_69_wilayas.xlsx")
    shutil.copy(comp_csv_path, desktop / "algeria_complete.csv")
    print("Copied all files to Desktop!")
