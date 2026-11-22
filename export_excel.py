import algeria_geo as dz
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import csv
from pathlib import Path

out_dir = Path("exports")
out_dir.mkdir(exist_ok=True)

# Build lookup maps for fast parent lookup
wilayas = dz.get_wilayas()
w_map = {w.code: w for w in wilayas}

dairas = dz.get_all_dairas()
d_map = {d.code: d for d in dairas}

communes = dz.get_all_communes()

wb = openpyxl.Workbook()
wb.remove(wb.active)  # Remove default sheet

# Styling definitions
header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Dark blue
header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
cell_font = Font(name="Segoe UI", size=10)
thin_border = Border(
    left=Side(style='thin', color='D1D5DB'),
    right=Side(style='thin', color='D1D5DB'),
    top=Side(style='thin', color='D1D5DB'),
    bottom=Side(style='thin', color='D1D5DB')
)

def style_sheet(ws, is_rtl=False):
    ws.views.sheetView[0].rightToLeft = is_rtl
    for col_idx, col in enumerate(ws.columns, 1):
        # Header style
        header_cell = ws.cell(row=1, column=col_idx)
        header_cell.fill = header_fill
        header_cell.font = header_font
        header_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.row_dimensions[1].height = 28
        
        # Determine column width
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)
        
        # Cells style
        for row_idx in range(2, ws.max_row + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = cell_font
            cell.border = thin_border
            if col_idx in [1, 4, 7, 10]:  # Codes
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(vertical="center")

# -------------------------------------------------------------
# Sheet 1: Comprehensive flat table (Wilaya + Daira + Commune)
# -------------------------------------------------------------
ws_all = wb.create_sheet(title="قائمة شاملة - All")
all_headers = [
    "رمز الولاية\nCode Wilaya",
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

style_sheet(ws_all, is_rtl=True)

# -------------------------------------------------------------
# Sheet 2: Wilayas
# -------------------------------------------------------------
ws_w = wb.create_sheet(title="الولايات - Wilayas")
w_headers = [
    "رمز الولاية\nCode",
    "اسم الولاية (عربي)\nNom (Ar)",
    "اسم الولاية (فرنسي)\nNom (Fr)",
    "اسم الولاية (إنجليزي)\nNom (En)",
    "رمز الهاتف\nCode Tél",
    "عدد الدوائر\nNb Daïras",
    "عدد البلديات\nNb Communes",
    "ولاية جديدة 2026\nNouvelle Wilaya"
]
ws_w.append(w_headers)
for w in wilayas:
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
style_sheet(ws_w, is_rtl=True)

# -------------------------------------------------------------
# Sheet 3: Dairas
# -------------------------------------------------------------
ws_d = wb.create_sheet(title="الدوائر - Dairas")
d_headers = [
    "رمز الدائرة\nCode Daïra",
    "رمز الولاية\nCode Wilaya",
    "اسم الدائرة (عربي)\nNom Daïra (Ar)",
    "اسم الدائرة (فرنسي)\nNom Daïra (Fr)",
    "اسم الولاية (عربي)\nNom Wilaya (Ar)",
    "اسم الولاية (فرنسي)\nNom Wilaya (Fr)"
]
ws_d.append(d_headers)
for d in dairas:
    w = w_map.get(d.wilaya_code)
    ws_d.append([
        d.code,
        d.wilaya_code,
        d.name_ar,
        d.name_fr,
        w.name_ar if w else "",
        w.name_fr if w else ""
    ])
style_sheet(ws_d, is_rtl=True)

# -------------------------------------------------------------
# Sheet 4: Communes
# -------------------------------------------------------------
ws_c = wb.create_sheet(title="البلديات - Communes")
c_headers = [
    "رمز البلدية\nCode Commune",
    "اسم البلدية (عربي)\nNom Commune (Ar)",
    "اسم البلدية (فرنسي)\nNom Commune (Fr)",
    "رمز الدائرة\nCode Daïra",
    "رمز الولاية\nCode Wilaya",
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
style_sheet(ws_c, is_rtl=True)

excel_path = out_dir / "algeria_geo_69_wilayas.xlsx"
wb.save(excel_path)
print(f"Saved Excel file to: {excel_path.resolve()}")

# Also export clean CSVs with utf-8-sig (Excel friendly)
csv_complete_path = out_dir / "algeria_complete.csv"
with open(csv_complete_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    clean_headers = [h.replace("\n", " / ") for h in all_headers]
    writer.writerow(clean_headers)
    writer.writerows(all_rows_for_csv)

print(f"Saved CSV file to: {csv_complete_path.resolve()}")
