"""Builds calculations/Solar_PV_Design_Calculations.xlsx

Every number is either (a) a blue input on the Assumptions sheet (or the two
monthly input tables) or (b) a live formula.  Change an input -> everything
recalculates.  Run:  python scripts/build_excel.py
"""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = Path(__file__).resolve().parent.parent / "calculations" / "Solar_PV_Design_Calculations.xlsx"

# ---------------------------------------------------------------- styles
F = "Arial"
f_norm = Font(name=F, size=10)
f_bold = Font(name=F, size=10, bold=True)
f_in = Font(name=F, size=10, color="0000FF")          # inputs
f_link = Font(name=F, size=10, color="008000")        # cross-sheet links
f_hdr = Font(name=F, size=10, bold=True, color="FFFFFF")
f_title = Font(name=F, size=14, bold=True, color="1F3864")
f_note = Font(name=F, size=9, italic=True, color="595959")
fill_hdr = PatternFill("solid", fgColor="1F3864")
fill_sec = PatternFill("solid", fgColor="D9E2F3")
fill_in = PatternFill("solid", fgColor="FFF2CC")
fill_ok = PatternFill("solid", fgColor="C6EFCE")
fill_bad = PatternFill("solid", fgColor="FFC7CE")
thin = Side(style="thin", color="BFBFBF")
box = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
center = Alignment(horizontal="center", vertical="center", wrap_text=True)

wb = Workbook()
ws_sum = wb.active
ws_sum.title = "Summary"
ws_a = wb.create_sheet("Assumptions")
ws_l = wb.create_sheet("Load_Sizing")
ws_s = wb.create_sheet("Stringing")
ws_c = wb.create_sheet("Cables")
ws_p = wb.create_sheet("Protection")
ws_g = wb.create_sheet("Generation")
ws_b = wb.create_sheet("BOM_Cost")
ws_pb = wb.create_sheet("Payback")


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = f_title
    if sub:
        ws["A2"] = sub
        ws["A2"].font = f_note
    ws.sheet_view.showGridLines = False


def header(ws, row, labels, col=1):
    for i, t in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=t)
        c.font, c.fill, c.alignment, c.border = f_hdr, fill_hdr, center, box


def put(ws, ref, value, font=f_norm, fmt=None, fill=None, align=None, border=True):
    c = ws[ref]
    c.value = value
    c.font = font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if align:
        c.alignment = align
    if border:
        c.border = box
    return c


def widths(ws, ws_widths):
    for i, w in enumerate(ws_widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def status_cf(ws, rng):
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"OK"'], fill=fill_ok))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"CHECK"'], fill=fill_bad))


# ================================================================ ASSUMPTIONS
title(ws_a, "Assumptions & Design Inputs",
      "Blue text on yellow = input you can change.  All other sheets calculate from these cells.")
widths(ws_a, [44, 16, 12, 78])
header(ws_a, 4, ["Parameter", "Value", "Unit", "Source / note"])
R = {}          # key -> absolute reference on Assumptions sheet
_row = [5]


def sec(text):
    r = _row[0]
    ws_a.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    c = ws_a.cell(row=r, column=1, value=text)
    c.font, c.fill = f_bold, fill_sec
    _row[0] += 1


def inp(key, label, value, unit, note, fmt=None):
    r = _row[0]
    put(ws_a, f"A{r}", label)
    put(ws_a, f"B{r}", value, f_in, fmt, fill_in)
    put(ws_a, f"C{r}", unit)
    put(ws_a, f"D{r}", note, f_note, align=wrap)
    R[key] = f"Assumptions!$B${r}"
    _row[0] += 1


sec("1. Site & design conditions")
inp("site", "Site (illustrative)", "Kolkata, West Bengal", "-", "Illustrative residential rooftop; not a real client site.")
inp("lat", "Latitude", 22.57, "deg N", "Approx. latitude of Kolkata.", "0.00")
inp("tilt", "Module tilt (fixed)", 22, "deg", "About equal to latitude; facing true south.", "0")
inp("tmin", "Design minimum ambient temperature", 5, "deg C", "Assumed (conservative) - gives the highest string Voc.", "0")
inp("tcell", "Maximum cell temperature", 70, "deg C", "Assumed - gives the lowest string Vmp.", "0")
inp("tavg", "Average operating cell temperature", 53, "deg C", "Assumed annual daytime average - used for the temperature loss.", "0")
inp("decl", "Solar declination - winter solstice", -23.45, "deg", "Design day for row spacing (21 Dec).", "0.00")
inp("hang", "Hour angle for no-shade check", 45, "deg", "45 deg = 09:00 solar time (no shade 09:00-15:00).", "0")
inp("vac", "AC supply voltage (1-phase)", 230, "V", "Single-phase, 50 Hz. Confirm sanctioned connection type with the DISCOM.", "0")

sec("2. PV module  (representative values - replace with the datasheet of the module you select)")
inp("n_mod", "Number of modules", 10, "nos", "Design choice - checked against the load-based requirement on Load_Sizing.", "0")
inp("mod_wp", "Module power (STC)", 540, "Wp", "Typical 540 Wp mono PERC, 144 half-cut cells.", "0")
inp("voc", "Open-circuit voltage Voc", 49.5, "V", "Typical datasheet value for this class.", "0.00")
inp("vmp", "Voltage at max power Vmp", 41.6, "V", "Typical datasheet value for this class.", "0.00")
inp("isc", "Short-circuit current Isc", 13.85, "A", "Typical datasheet value for this class.", "0.00")
inp("imp", "Current at max power Imp", 12.99, "A", "Typical datasheet value for this class.", "0.00")
inp("a_voc", "Temperature coefficient of Voc", -0.0027, "per deg C", "Typical: -0.27 %/deg C.", "0.00%")
inp("g_pmax", "Temperature coefficient of Pmax (also used for Vmp)", -0.0035, "per deg C", "Typical: -0.35 %/deg C. Using it for Vmp is a common approximation.", "0.00%")
inp("mod_fuse", "Max series fuse rating of module", 25, "A", "Typical datasheet value.", "0")
inp("mod_L", "Module length", 2.279, "m", "Typical for this class.", "0.000")
inp("mod_W", "Module width", 1.134, "m", "Typical for this class.", "0.000")

sec("3. Inverter  (representative single-phase 5 kW, 2-MPPT string inverter)")
inp("inv_kw", "Rated AC power", 5, "kW", "", "0.0")
inp("n_mppt", "Number of MPPT inputs", 2, "nos", "", "0")
inp("vdc_max", "Max DC input voltage", 600, "V", "", "0")
inp("mppt_min", "MPPT range - minimum", 90, "V", "", "0")
inp("mppt_max", "MPPT range - maximum", 550, "V", "", "0")
inp("imax_mppt", "Max operating current per MPPT", 16, "A", "", "0")
inp("isc_mppt", "Max short-circuit current per MPPT", 20, "A", "", "0")
inp("iac_max", "Max AC output current", 22.7, "A", "5 kVA class at 230 V.", "0.0")
inp("eff", "Weighted average efficiency", 0.965, "-", "Assumed (typical string inverter, 96-97%).", "0.0%")

sec("4. String configuration")
inp("n_ser", "Modules in series per string", 5, "nos", "Checked on Stringing sheet.", "0")
inp("n_str", "Number of strings", 2, "nos", "One string per MPPT input.", "0")

sec("5. Cables")
inp("rho", "Copper resistivity at operating temp", 0.021, "ohm.mm2/m", "Approx. value for Cu at about 70 deg C.", "0.0000")
inp("lim_dc", "Voltage-drop limit - DC side", 0.015, "-", "Design target (not a code value).", "0.0%")
inp("lim_ac", "Voltage-drop limit - AC side", 0.02, "-", "Design target (not a code value).", "0.0%")
inp("dc_size", "DC cable size (Cu, PV cable)", 4, "mm2", "Solar cable, e.g. EN 50618 type.", "0")
inp("dc_base", "DC cable base current rating", 44, "A", "Indicative surface-clipped rating - verify with the cable datasheet.", "0")
inp("dc_der", "DC cable derating factor", 0.70, "-", "Indicative: hot rooftop temperature + grouping.", "0.00")
inp("ac_size", "AC cable size (Cu, 3-core)", 10, "mm2", "", "0")
inp("ac_base", "AC cable base current rating", 52, "A", "Indicative conservative value (PVC/XLPE, clipped) - verify with datasheet.", "0")
inp("ac_der", "AC cable derating factor", 0.79, "-", "Ambient 45 deg C for PVC, IEC 60364-5-52 type table - verify.", "0.00")
inp("L_s1", "Length - String 1 to DCDB (one way)", 10, "m", "Route measured on roof layout E-04 (~6.4 m) + rises, slack and margin.", "0")
inp("L_s2", "Length - String 2 to DCDB (one way)", 7, "m", "Route measured on roof layout E-04 (~2.9 m) + rises, slack and margin.", "0")
inp("L_dd", "Length - DCDB to inverter (one way)", 3, "m", "DCDB mounted beside the inverter.", "0")
inp("L_ia", "Length - inverter to ACDB", 5, "m", "", "0")
inp("L_am", "Length - ACDB to meter / main DB", 15, "m", "", "0")

sec("6. Protection, earthing & lightning")
inp("dc_f", "DC protective device factor (x Isc)", 1.25, "-", "In >= 1.25 x Isc.", "0.00")
inp("ac_f", "AC protective device factor (x max Iac)", 1.25, "-", "In >= 1.25 x Iac,max.", "0.00")
inp("dc_dev_v", "DC MCB / isolator rated voltage", 600, "V DC", "Must be >= string Voc at Tmin.", "0")
inp("dc_spd_uc", "DC SPD (Type 2) Uc", 600, "V DC", "Must be >= string Voc at Tmin.", "0")
inp("ac_spd_uc", "AC SPD (Type 2) Uc", 275, "V AC", "Must be >= 1.1 x supply voltage.", "0")
inp("rcd_ma", "RCCB sensitivity", 30, "mA", "Type A (use Type B only if the inverter maker requires it).", "0")
inp("n_pits", "Earth pits", 4, "nos", "EP-1 equipment, EP-2 AC/neutral, EP-3 & EP-4 lightning.", "0")
inp("r_earth", "Earth resistance target (each pit)", 5, "ohm", "Design target - to be proven by site measurement.", "0")
inp("r_sph", "Rolling-sphere radius (assumed LPL III)", 45, "m", "IEC 62305 style; a site risk assessment decides the real level.", "0")
inp("rod_h", "Air-terminal height above roof", 3.0, "m", "", "0.0")
inp("struct_low", "Module lower-edge height above roof", 0.5, "m", "Structure leg height at the front.", "0.0")
inp("rod_off", "Air terminal offset from array edge", 1.0, "m", "One rod each side of the array, at mid-depth.", "0.0")
inp("bldg_h", "Building height (roof to ground)", 10, "m", "Illustrative G+2 building.", "0")
inp("strip_roof", "Roof conductor length (GI strip)", 12, "m", "", "0")
inp("strip_gnd", "Ground interconnection strip", 30, "m", "Links the four pits.", "0")

sec("7. Performance losses")
inp("l_soil", "Soiling", 0.04, "-", "Assumed (dusty, monsoon-washed site).", "0.0%")
inp("l_mis", "Module mismatch", 0.02, "-", "Assumed.", "0.0%")
inp("l_shade", "Shading", 0.02, "-", "Assumed (row spacing designed for no shade 09:00-15:00).", "0.0%")
inp("l_avail", "Availability / downtime", 0.01, "-", "Assumed.", "0.0%")
inp("l_lid", "Light-induced degradation & other", 0.02, "-", "Assumed.", "0.0%")
inp("offset", "Target energy offset", 1.0, "-", "Size the system to cover this share of annual consumption.", "0%")

sec("8. Financial  (illustrative - replace with real quotes and tariff)")
inp("tariff", "Grid tariff", 7.0, "INR/kWh", "Assumed domestic energy rate; check the current DISCOM tariff order.", "0.00")
inp("esc", "Annual tariff escalation", 0.03, "-", "Assumed.", "0.0%")
inp("deg", "Annual module degradation", 0.005, "-", "Typical 0.4-0.7 %/yr.", "0.0%")
inp("method", "Savings method (1 = monthly offset, 2 = annual banking)", 1, "-", "1 is conservative: surplus in a month is not credited.", "0")
inp("subsidy", "Capital subsidy (CFA)", 78000, "INR", "Assumed from the PM Surya Ghar scheme - VERIFY current rules/eligibility; set 0 to ignore.", "#,##0")
inp("om", "Annual O&M (cleaning, checks)", 3000, "INR/yr", "Assumed.", "#,##0")
inp("inv_year", "Inverter replacement year", 12, "year", "Assumed.", "0")
inp("inv_cost", "Inverter replacement cost", 40000, "INR", "Assumed.", "#,##0")
inp("ef", "Grid emission factor", 0.7, "tCO2/MWh", "Assumed round figure - check the latest CEA value.", "0.00")
ws_a.freeze_panes = "A5"

# ================================================================ STRINGING
title(ws_s, "Array Configuration, String Sizing & Row Spacing",
      "Voltage/current checks against the inverter window, plus roof-layout geometry.")
widths(ws_s, [46, 44, 14, 9, 14, 10])
header(ws_s, 4, ["Parameter", "Basis", "Value", "Unit", "Limit", "Status"])
S = {}


def srow(r, key, label, basis, formula, unit, fmt="0.00", limit=None, status=None, limit_fmt=None):
    put(ws_s, f"A{r}", label)
    put(ws_s, f"B{r}", basis, f_note, align=wrap)
    put(ws_s, f"C{r}", formula, f_norm, fmt)
    put(ws_s, f"D{r}", unit)
    put(ws_s, f"E{r}", limit if limit is not None else "", f_norm, limit_fmt or fmt)
    put(ws_s, f"F{r}", status if status else "", f_bold, align=center)
    S[key] = f"Stringing!$C${r}"


srow(5, "voc_c", "Module Voc at minimum temperature", "Voc x (1 + a_Voc x (Tmin - 25))", f"={R['voc']}*(1+{R['a_voc']}*({R['tmin']}-25))", "V")
srow(6, "vmp_h", "Module Vmp at maximum cell temperature", "Vmp x (1 + g_Pmax x (Tcell - 25))", f"={R['vmp']}*(1+{R['g_pmax']}*({R['tcell']}-25))", "V")
srow(7, "vmp_c", "Module Vmp at minimum temperature", "Vmp x (1 + g_Pmax x (Tmin - 25))", f"={R['vmp']}*(1+{R['g_pmax']}*({R['tmin']}-25))", "V")
srow(8, "n_max", "Maximum modules per string", "ROUNDDOWN(Vdc,max / module Voc cold)", f"=ROUNDDOWN({R['vdc_max']}/C5,0)", "nos", "0")
srow(9, "n_min", "Minimum modules per string", "ROUNDUP(MPPT,min / module Vmp hot)", f"=ROUNDUP({R['mppt_min']}/C6,0)", "nos", "0")
srow(10, "n_ser", "Selected modules per string", "From Assumptions", f"={R['n_ser']}", "nos", "0", None,
     '=IF(AND(C10<=C8,C10>=C9),"OK","CHECK")')
srow(11, "n_str", "Number of strings", "From Assumptions", f"={R['n_str']}", "nos", "0")
srow(12, "n_tot", "Total modules (series x strings)", "Must equal the module count", "=C10*C11", "nos", "0", f"={R['n_mod']}",
     '=IF(C12=E12,"OK","CHECK")')
srow(13, "v_str_oc", "String Voc at minimum temperature", "Must not exceed the inverter max DC voltage", "=C5*C10", "V", "0.0", f"={R['vdc_max']}",
     '=IF(C13<=E13,"OK","CHECK")')
srow(14, "v_str_h", "String Vmp at maximum cell temperature", "Must stay above the MPPT minimum", "=C6*C10", "V", "0.0", f"={R['mppt_min']}",
     '=IF(C14>=E14,"OK","CHECK")')
srow(15, "v_str_c", "String Vmp at minimum temperature", "Must stay below the MPPT maximum", "=C7*C10", "V", "0.0", f"={R['mppt_max']}",
     '=IF(C15<=E15,"OK","CHECK")')
srow(16, "v_str_n", "String Vmp at STC (nominal)", "Used for the DC voltage-drop %", f"={R['vmp']}*C10", "V", "0.0")
srow(17, "str_mppt", "Strings per MPPT input", "Strings / MPPT inputs", f"=C11/{R['n_mppt']}", "nos", "0.0", None,
     '=IF(C17=INT(C17),"OK","CHECK")')
srow(18, "i_mppt", "Operating current per MPPT (Imp x strings)", "Must not exceed the inverter MPPT current", f"={R['imp']}*C17", "A", "0.00", f"={R['imax_mppt']}",
     '=IF(C18<=E18,"OK","CHECK")')
srow(19, "isc_mppt", "Short-circuit current per MPPT (Isc x strings)", "Must not exceed the inverter MPPT Isc", f"={R['isc']}*C17", "A", "0.00", f"={R['isc_mppt']}",
     '=IF(C19<=E19,"OK","CHECK")')
srow(20, "kwp", "Array size (STC)", "Modules x Wp / 1000", f"=C12*{R['mod_wp']}/1000", "kWp", "0.00")
srow(21, "dcac", "DC / AC ratio", "kWp / inverter kW (typical 1.0 - 1.3)", f"=C20/{R['inv_kw']}", "-", "0.00", "1.0 - 1.3",
     '=IF(AND(C21>=1,C21<=1.3),"OK","CHECK")')

put(ws_s, "A23", "Roof layout geometry (row spacing for no shading, winter solstice 09:00-15:00)", f_bold, border=False)
srow(24, "rise", "Vertical rise of module (L x sin tilt)", "Module in portrait, length along slope", f"={R['mod_L']}*SIN(RADIANS({R['tilt']}))", "m", "0.000")
srow(25, "proj", "Horizontal projection (L x cos tilt)", "", f"={R['mod_L']}*COS(RADIANS({R['tilt']}))", "m", "0.000")
srow(26, "alt", "Solar altitude at 09:00, 21 Dec", "sin a = sin(lat) sin(decl) + cos(lat) cos(decl) cos(h)",
     f"=DEGREES(ASIN(SIN(RADIANS({R['lat']}))*SIN(RADIANS({R['decl']}))+COS(RADIANS({R['lat']}))*COS(RADIANS({R['decl']}))*COS(RADIANS({R['hang']}))))", "deg", "0.0")
srow(27, "azi", "Solar azimuth from south at 09:00", "sin g = cos(decl) sin(h) / cos(a)",
     f"=DEGREES(ASIN(COS(RADIANS({R['decl']}))*SIN(RADIANS({R['hang']}))/COS(RADIANS(C26))))", "deg", "0.0")
srow(28, "gap", "Minimum clear gap between rows", "rise x cos(azimuth) / tan(altitude)", "=C24*COS(RADIANS(C27))/TAN(RADIANS(C26))", "m", "0.00")
srow(29, "pitch", "Row pitch (front edge to front edge)", "projection + gap", "=C25+C28", "m", "0.00")
srow(30, "rows", "Number of rows", "One string per row", f"={R['n_str']}", "nos", "0")
srow(31, "width", "Array width (modules side by side)", "modules per string x module width", f"={R['n_ser']}*{R['mod_W']}", "m", "0.00")
srow(32, "depth", "Array depth (all rows)", "(rows - 1) x pitch + projection", "=(C30-1)*C29+C25", "m", "0.00")
srow(33, "area", "Total module area", "modules x L x W", f"={R['n_mod']}*{R['mod_L']}*{R['mod_W']}", "m2", "0.0")
srow(34, "roof", "Minimum roof footprint (1 m clearance all round)", "(width + 2) x (depth + 2)", "=(C31+2)*(C32+2)", "m2", "0.0")
srow(35, "top_h", "Highest point of array above roof", "lower-edge height + rise", f"={R['struct_low']}+C24", "m", "0.00")
status_cf(ws_s, "F5:F40")

# ================================================================ GENERATION (built before Load_Sizing refs it)
title(ws_g, "Generation Estimate & Performance Ratio",
      "Monthly peak-sun-hours (blue) are APPROXIMATE climatological values for Kolkata - replace with PVGIS / NASA POWER / PVsyst data.")
widths(ws_g, [30, 10, 12, 16, 14, 14, 14, 14, 14, 14])
header(ws_g, 4, ["Loss item", "Loss", "Basis"])
ws_g.merge_cells("C4:E4")
losses = [
    (5, "Soiling", f"={R['l_soil']}", "Assumption"),
    (6, "Temperature", f"=ABS({R['g_pmax']})*({R['tavg']}-25)", "|g_Pmax| x (avg cell temp - 25)"),
    (7, "Module mismatch", f"={R['l_mis']}", "Assumption"),
    (8, "Shading", f"={R['l_shade']}", "Assumption"),
    (9, "DC cable", "=Cables!$I$9", "From Cables sheet (average string)"),
    (10, "Inverter", f"=1-{R['eff']}", "1 - efficiency"),
    (11, "AC cable", "=Cables!$I$14", "From Cables sheet"),
    (12, "Availability", f"={R['l_avail']}", "Assumption"),
    (13, "LID & other", f"={R['l_lid']}", "Assumption"),
]
for r, name, fml, basis in losses:
    put(ws_g, f"A{r}", name)
    put(ws_g, f"B{r}", fml, f_link if "!" in fml and "Assumptions" not in fml else f_norm, "0.00%")
    ws_g.merge_cells(f"C{r}:E{r}")
    put(ws_g, f"C{r}", basis, f_note)
put(ws_g, "A14", "Performance ratio (PR)", f_bold)
put(ws_g, "B14", "=(1-B5)*(1-B6)*(1-B7)*(1-B8)*(1-B9)*(1-B10)*(1-B11)*(1-B12)*(1-B13)", f_bold, "0.0%")
ws_g.merge_cells("C14:E14")
put(ws_g, "C14", "Product of (1 - loss)", f_note)

header(ws_g, 17, ["Month", "Days", "Peak sun hours (kWh/m2/day, tilted plane)", "Irradiation (kWh/m2/month)",
                  "Generation (kWh)", "Yield (kWh/kWp)", "Consumption (kWh)", "Offset (kWh)", "Surplus (kWh)", "Grid import (kWh)"])
ws_g.row_dimensions[17].height = 54
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
psh = [4.9, 5.5, 5.9, 5.9, 5.6, 4.5, 4.0, 4.1, 4.2, 4.7, 4.8, 4.7]
load = [420, 400, 480, 620, 720, 700, 680, 680, 660, 560, 440, 400]
for i, m in enumerate(months):
    r = 18 + i
    put(ws_g, f"A{r}", m)
    put(ws_g, f"B{r}", days[i], f_norm, "0")
    put(ws_g, f"C{r}", psh[i], f_in, "0.0", fill_in)
    put(ws_g, f"D{r}", f"=B{r}*C{r}", f_norm, "0.0")
    put(ws_g, f"E{r}", f"={S['kwp']}*D{r}*$B$14", f_norm, "#,##0")
    put(ws_g, f"F{r}", f"=D{r}*$B$14", f_norm, "0.0")
    put(ws_g, f"G{r}", f"=Load_Sizing!C{5 + i}", f_link, "#,##0")
    put(ws_g, f"H{r}", f"=MIN(E{r},G{r})", f_norm, "#,##0")
    put(ws_g, f"I{r}", f"=MAX(E{r}-G{r},0)", f_norm, "#,##0")
    put(ws_g, f"J{r}", f"=MAX(G{r}-E{r},0)", f_norm, "#,##0")
put(ws_g, "A30", "Total / annual", f_bold)
put(ws_g, "B30", "=SUM(B18:B29)", f_bold, "0")
put(ws_g, "C30", "=D30/B30", f_bold, "0.00")
for col, fmt in zip("DEFGHIJ", ["0", "#,##0", "0", "#,##0", "#,##0", "#,##0", "#,##0"]):
    put(ws_g, f"{col}30", f"=SUM({col}18:{col}29)", f_bold, fmt)
put(ws_g, "A32", "Average peak sun hours (kWh/m2/day)")
put(ws_g, "D32", "=C30", f_norm, "0.00")
put(ws_g, "A33", "Specific yield (kWh/kWp/year)")
put(ws_g, "D33", "=F30", f_norm, "#,##0")
put(ws_g, "A34", "Capacity utilisation factor (CUF)")
put(ws_g, "D34", f"=E30/({S['kwp']}*8760)", f_norm, "0.0%")
put(ws_g, "A35", "Energy credited to bill (kWh/yr)")
put(ws_g, "D35", f"=IF({R['method']}=1,H30,MIN(E30,G30))", f_bold, "#,##0")
put(ws_g, "E35", "method 1 = sum of monthly offsets; 2 = annual banking", f_note, border=False)
ws_g.merge_cells("A32:C32"); ws_g.merge_cells("A33:C33"); ws_g.merge_cells("A34:C34"); ws_g.merge_cells("A35:C35")

ch = BarChart()
ch.type = "col"
ch.title = "Monthly generation vs consumption (kWh)"
ch.roundedCorners = False
ch.add_data(Reference(ws_g, min_col=5, min_row=17, max_row=29), titles_from_data=True)
ch.add_data(Reference(ws_g, min_col=7, min_row=17, max_row=29), titles_from_data=True)
ch.set_categories(Reference(ws_g, min_col=1, min_row=18, max_row=29))
ch.legend.position = "b"
ch.legend.overlay = False
ch.title.overlay = False
ch.x_axis.delete = False
ch.y_axis.delete = False
ch.y_axis.title = "kWh"
ch.y_axis.title.overlay = False
ch.height, ch.width = 8.5, 17
ws_g.add_chart(ch, "L4")

# ================================================================ LOAD SIZING
title(ws_l, "Load Calculation & System Sizing",
      "Monthly units (blue) are an ILLUSTRATIVE household profile - replace with the real electricity bills.")
widths(ws_l, [14, 8, 18, 4, 44, 16, 12, 10])
header(ws_l, 4, ["Month", "Days", "Consumption (kWh)"])
for i, m in enumerate(months):
    r = 5 + i
    put(ws_l, f"A{r}", m)
    put(ws_l, f"B{r}", days[i], f_norm, "0")
    put(ws_l, f"C{r}", load[i], f_in, "#,##0", fill_in)
put(ws_l, "A17", "Annual", f_bold)
put(ws_l, "B17", "=SUM(B5:B16)", f_bold, "0")
put(ws_l, "C17", "=SUM(C5:C16)", f_bold, "#,##0")
put(ws_l, "A18", "Monthly avg", f_bold)
put(ws_l, "C18", "=AVERAGE(C5:C16)", f_bold, "#,##0")
put(ws_l, "A19", "Daily avg", f_bold)
put(ws_l, "C19", "=C17/B17", f_bold, "0.0")

header(ws_l, 4, ["Sizing step", "Value", "Unit"], col=5)
L = {}
rows = [
    ("annual", "Annual consumption", "=C17", "kWh", "#,##0"),
    ("target", "Target offset", f"={R['offset']}", "-", "0%"),
    ("e_req", "Energy to be generated", "=F5*F6", "kWh", "#,##0"),
    ("yield", "Specific yield (from Generation)", "=Generation!D33", "kWh/kWp/yr", "#,##0"),
    ("kwp_req", "Required array size", "=F7/F8", "kWp", "0.00"),
    ("wp", "Module rating", f"={R['mod_wp']}", "Wp", "0"),
    ("n_req", "Required modules (rounded up)", "=ROUNDUP(F9*1000/F10,0)", "nos", "0"),
    ("n_sel", "Selected modules", f"={R['n_mod']}", "nos", "0"),
    ("kwp_in", "Installed array size", f"={S['kwp']}", "kWp", "0.00"),
    ("gen", "Estimated annual generation", "=Generation!E30", "kWh", "#,##0"),
    ("cover", "Generation / consumption", "=F14/F5", "%", "0%"),
]
for i, (k, lab, fml, unit, fmt) in enumerate(rows):
    r = 5 + i
    put(ws_l, f"E{r}", lab)
    put(ws_l, f"F{r}", fml, f_link if "!" in fml else f_norm, fmt)
    put(ws_l, f"G{r}", unit)
    L[k] = f"Load_Sizing!$F${r}"
put(ws_l, "E16", "Check: selected modules >= required", f_bold)
put(ws_l, "F16", '=IF(F12>=F11,"OK","CHECK")', f_bold, align=center)
put(ws_l, "E17", "Check: array at least as large as required", f_bold)
put(ws_l, "F17", '=IF(F13>=F9,"OK","CHECK")', f_bold, align=center)
status_cf(ws_l, "F16:F17")

# ================================================================ CABLES
title(ws_c, "Cable Sizing & Voltage Drop",
      "DC: Ib = 1.25 x Isc, VD at Imp.  AC (1-phase): VD = 2 x L x I x rho / A.  Ampacity values are indicative - verify with the cable datasheet.")
widths(ws_c, [8, 30, 22, 9, 9, 11, 11, 9, 9, 10, 10, 11, 11, 11])
header(ws_c, 4, ["Tag", "Run", "Cable", "Size (mm2)", "Length (m)", "Design Ib (A)", "VD current (A)",
                 "VD (V)", "VD (%)", "Limit (%)", "Iz (A)", "Device In (A)", "Ampacity check", "VD check"])
ws_c.row_dimensions[4].height = 40
dcIz = f"{R['dc_base']}*{R['dc_der']}"
acIz = f"{R['ac_base']}*{R['ac_der']}"
dc_runs = [(5, "DC-1", "String 1 to DCDB", "L_s1"), (6, "DC-2", "String 2 to DCDB", "L_s2"), (7, "DC-3", "DCDB to inverter (per string)", "L_dd")]
for r, tag, run, lk in dc_runs:
    put(ws_c, f"A{r}", tag, f_bold)
    put(ws_c, f"B{r}", run)
    put(ws_c, f"C{r}", "1C Cu solar cable x 2")
    put(ws_c, f"D{r}", f"={R['dc_size']}", f_link, "0")
    put(ws_c, f"E{r}", f"={R[lk]}", f_link, "0")
    put(ws_c, f"F{r}", f"={R['dc_f']}*{R['isc']}", f_norm, "0.0")
    put(ws_c, f"G{r}", f"={R['imp']}", f_link, "0.00")
    put(ws_c, f"H{r}", f"=2*E{r}*G{r}*{R['rho']}/D{r}", f_norm, "0.00")
    put(ws_c, f"I{r}", f"=H{r}/{S['v_str_n']}", f_norm, "0.00%")
    put(ws_c, f"J{r}", f"={R['lim_dc']}", f_link, "0.0%")
    put(ws_c, f"K{r}", f"={dcIz}", f_norm, "0.0")
    put(ws_c, f"L{r}", "=Protection!$E$6", f_link, "0")
    put(ws_c, f"M{r}", f'=IF(AND(F{r}<=L{r},L{r}<=K{r}),"OK","CHECK")', f_bold, align=center)
    put(ws_c, f"N{r}", f'=IF(I{r}<=J{r},"OK","CHECK")', f_bold, align=center)
put(ws_c, "A8", "DC", f_bold)
put(ws_c, "B8", "Worst-case string total (DC-1 or DC-2, plus DC-3)", f_bold)
ws_c.merge_cells("B8:H8")
put(ws_c, "I8", "=MAX(I5,I6)+I7", f_bold, "0.00%")
put(ws_c, "J8", f"={R['lim_dc']}", f_link, "0.0%")
put(ws_c, "N8", '=IF(I8<=J8,"OK","CHECK")', f_bold, align=center)
put(ws_c, "B9", "Average DC loss used in the PR (avg strings + DC-3)", f_note, border=False)
put(ws_c, "I9", "=AVERAGE(I5,I6)+I7", f_norm, "0.00%")

ac_runs = [(11, "AC-1", "Inverter to ACDB", "L_ia"), (12, "AC-2", "ACDB to meter / main DB", "L_am")]
for r, tag, run, lk in ac_runs:
    put(ws_c, f"A{r}", tag, f_bold)
    put(ws_c, f"B{r}", run)
    put(ws_c, f"C{r}", "3C Cu armoured (L,N,PE)")
    put(ws_c, f"D{r}", f"={R['ac_size']}", f_link, "0")
    put(ws_c, f"E{r}", f"={R[lk]}", f_link, "0")
    put(ws_c, f"F{r}", f"={R['iac_max']}", f_link, "0.0")
    put(ws_c, f"G{r}", f"={R['iac_max']}", f_link, "0.0")
    put(ws_c, f"H{r}", f"=2*E{r}*G{r}*{R['rho']}/D{r}", f_norm, "0.00")
    put(ws_c, f"I{r}", f"=H{r}/{R['vac']}", f_norm, "0.00%")
    put(ws_c, f"J{r}", f"={R['lim_ac']}", f_link, "0.0%")
    put(ws_c, f"K{r}", f"={acIz}", f_norm, "0.0")
    put(ws_c, f"L{r}", "=Protection!$E$8", f_link, "0")
    put(ws_c, f"M{r}", f'=IF(AND(F{r}<=L{r},L{r}<=K{r}),"OK","CHECK")', f_bold, align=center)
    put(ws_c, f"N{r}", f'=IF(I{r}<=J{r},"OK","CHECK")', f_bold, align=center)
put(ws_c, "A13", "AC", f_bold)
put(ws_c, "B13", "Total AC run (AC-1 + AC-2)", f_bold)
ws_c.merge_cells("B13:H13")
put(ws_c, "I13", "=I11+I12", f_bold, "0.00%")
put(ws_c, "J13", f"={R['lim_ac']}", f_link, "0.0%")
put(ws_c, "N13", '=IF(I13<=J13,"OK","CHECK")', f_bold, align=center)
put(ws_c, "B14", "AC loss used in the PR", f_note, border=False)
put(ws_c, "I14", "=I13", f_norm, "0.00%")
put(ws_c, "A16", "Rule checked:  Ib <= In <= Iz.   Iz = base rating x derating factor (Assumptions sheet).", f_note, border=False)
status_cf(ws_c, "M5:N14")

# ================================================================ PROTECTION
title(ws_p, "Protection, Earthing & Lightning Protection",
      "Device sizes are the next standard rating at or above the calculated minimum.")
widths(ws_p, [34, 22, 36, 14, 13, 14, 10, 4, 12])
header(ws_p, 4, ["Device", "Location", "Sizing rule", "Required min", "Selected", "Unit / rating", "Result"])
header(ws_p, 4, ["Std ratings (A)"], col=9)
for i, v in enumerate([6, 10, 16, 20, 25, 32, 40, 50, 63]):
    put(ws_p, f"I{5 + i}", v, f_in, "0", fill_in)
STD = "$I$5:$I$13"


def nxt(cell):
    return f"=IF(INDEX({STD},MATCH({cell},{STD},1))={cell},{cell},INDEX({STD},MATCH({cell},{STD},1)+1))"


put(ws_p, "A5", "DC string breaker / isolator voltage", f_norm)
put(ws_p, "B5", "DCDB")
put(ws_p, "C5", "Rated voltage >= string Voc at Tmin", f_note)
put(ws_p, "D5", f"={S['v_str_oc']}", f_link, "0.0")
put(ws_p, "E5", f"={R['dc_dev_v']}", f_link, "0")
put(ws_p, "F5", "V DC")
put(ws_p, "G5", '=IF(E5>=D5,"OK","CHECK")', f_bold, align=center)
put(ws_p, "A6", "DC MCB / isolator, 2P (per string)", f_norm)
put(ws_p, "B6", "DCDB")
put(ws_p, "C6", "In >= 1.25 x Isc;  In <= Iz and <= module max fuse", f_note)
put(ws_p, "D6", f"={R['dc_f']}*{R['isc']}", f_norm, "0.0")
put(ws_p, "E6", nxt("D6"), f_bold, "0")
put(ws_p, "F6", "A")
put(ws_p, "G6", f'=IF(AND(E6<=Cables!$K$5,E6<={R["mod_fuse"]}),"OK","CHECK")', f_bold, align=center)
put(ws_p, "A7", "DC SPD Type 2 (one per MPPT)", f_norm)
put(ws_p, "B7", "DCDB")
put(ws_p, "C7", "Uc >= string Voc at Tmin", f_note)
put(ws_p, "D7", f"={S['v_str_oc']}", f_link, "0.0")
put(ws_p, "E7", f"={R['dc_spd_uc']}", f_link, "0")
put(ws_p, "F7", "V DC (Uc)")
put(ws_p, "G7", '=IF(E7>=D7,"OK","CHECK")', f_bold, align=center)
put(ws_p, "A8", "AC MCB, 2P, C-curve", f_norm)
put(ws_p, "B8", "ACDB")
put(ws_p, "C8", "In >= 1.25 x Iac,max;  In <= Iz", f_note)
put(ws_p, "D8", f"={R['ac_f']}*{R['iac_max']}", f_norm, "0.0")
put(ws_p, "E8", nxt("D8"), f_bold, "0")
put(ws_p, "F8", "A")
put(ws_p, "G8", f'=IF(AND(E8>={R["iac_max"]},E8<=Cables!$K$11),"OK","CHECK")', f_bold, align=center)
put(ws_p, "A9", "RCCB, 2P, Type A", f_norm)
put(ws_p, "B9", "ACDB")
put(ws_p, "C9", "In >= 1.25 x upstream MCB (one size above)", f_note)
put(ws_p, "D9", "=1.25*E8", f_norm, "0.0")
put(ws_p, "E9", nxt("D9"), f_bold, "0")
put(ws_p, "F9", f'=TEXT({R["rcd_ma"]},"0")&" mA"')
put(ws_p, "G9", '=IF(E9>=E8,"OK","CHECK")', f_bold, align=center)
put(ws_p, "A10", "AC SPD Type 2", f_norm)
put(ws_p, "B10", "ACDB")
put(ws_p, "C10", "Uc >= 1.1 x supply voltage", f_note)
put(ws_p, "D10", f"=1.1*{R['vac']}", f_norm, "0")
put(ws_p, "E10", f"={R['ac_spd_uc']}", f_link, "0")
put(ws_p, "F10", "V AC (Uc)")
put(ws_p, "G10", '=IF(E10>=D10,"OK","CHECK")', f_bold, align=center)
put(ws_p, "A11", "AC isolator, 2P, lockable", f_norm)
put(ws_p, "B11", "After ACDB (DISCOM accessible)")
put(ws_p, "C11", "In >= MCB rating", f_note)
put(ws_p, "D11", "=E8", f_norm, "0")
put(ws_p, "E11", nxt("D11"), f_bold, "0")
put(ws_p, "F11", "A")
put(ws_p, "G11", '=IF(E11>=D11,"OK","CHECK")', f_bold, align=center)

put(ws_p, "A14", "Lightning protection - rolling sphere check (indicative)", f_bold, border=False)
header(ws_p, 15, ["Item", "Basis", "", "Value", "", "Unit", "Result"])
lp = [
    (16, "Rolling-sphere radius R", "Assumption", f"={R['r_sph']}", "m", "0.0"),
    (17, "Air-terminal height h above roof", "Assumption", f"={R['rod_h']}", "m", "0.0"),
    (18, "Highest array point hx", "From Stringing", f"={S['top_h']}", "m", "0.00"),
    (19, "Protected radius at array top", "sqrt(h(2R-h)) - sqrt(hx(2R-hx))", "=SQRT(D17*(2*D16-D17))-SQRT(D18*(2*D16-D18))", "m", "0.00"),
    (20, "Farthest array point from nearest rod", "sqrt((W/2 + offset)^2 + (D/2)^2)", f"=SQRT(({'Stringing!$C$31'}/2+{R['rod_off']})^2+({'Stringing!$C$32'}/2)^2)", "m", "0.00"),
]
for r, a, b, fml, u, fmt in lp:
    put(ws_p, f"A{r}", a)
    put(ws_p, f"B{r}", b, f_note, align=wrap)
    ws_p.merge_cells(f"B{r}:C{r}")
    put(ws_p, f"D{r}", fml, f_link if "!" in fml and "Assumptions" in fml else f_norm, fmt)
    put(ws_p, f"F{r}", u)
put(ws_p, "A21", "Array covered by the two air terminals?", f_bold)
put(ws_p, "G21", '=IF(D19>=D20,"OK","CHECK")', f_bold, align=center)
put(ws_p, "A22", "Note: the real protection level and air-terminal layout must come from a site risk assessment (IEC 62305-2).", f_note, border=False)

put(ws_p, "A24", "Earthing summary", f_bold, border=False)
header(ws_p, 25, ["Pit", "Serves", "Conductor", "Target (ohm)"])
earth = [
    ("EP-1", "Array frames, DCDB, inverter (equipment earth)", "6 mm2 Cu (G/Y)"),
    ("EP-2", "ACDB earth bar & AC neutral / supply earth", "10 mm2 Cu (G/Y)"),
    ("EP-3", "Lightning down conductor 1 (west)", "25x3 mm GI strip"),
    ("EP-4", "Lightning down conductor 2 (east)", "25x3 mm GI strip"),
]
for i, (a, b, c) in enumerate(earth):
    r = 26 + i
    put(ws_p, f"A{r}", a, f_bold)
    put(ws_p, f"B{r}", b, align=wrap)
    ws_p.merge_cells(f"B{r}:B{r}")
    put(ws_p, f"C{r}", c)
    put(ws_p, f"D{r}", f"={R['r_earth']}", f_link, "0")
put(ws_p, "A30", "All pits are bonded together with 25x3 mm GI strip (equipotential bonding).", f_note, border=False)
status_cf(ws_p, "G5:G21")

# ================================================================ BOM & COST
title(ws_b, "Bill of Materials & Budgetary Cost",
      "Quantities are formulas linked to the design.  Rates (blue) are ILLUSTRATIVE budgetary figures in INR incl. taxes - replace with real quotations.")
widths(ws_b, [5, 38, 54, 8, 10, 12, 14])
header(ws_b, 4, ["#", "Item", "Specification", "Unit", "Qty", "Rate (INR)", "Amount (INR)"])
bom = [
    ("PV module", "540 Wp mono PERC, 144 half-cut cells (representative)", "nos", f"={R['n_mod']}", 13000),
    ("String inverter", "5 kW, 1-phase, 2 MPPT, grid-tied, IP65, with WiFi monitoring", "nos", "=1", 48000),
    ("Mounting structure", "Hot-dip GI, fixed tilt 22 deg, south facing, per module", "nos", f"={R['n_mod']}", 2200),
    ("DC cable", "1C Cu solar cable 4 mm2, red + black (10% wastage)", "m",
     f"=ROUNDUP((2*({R['L_s1']}+{R['L_s2']})+2*{R['n_str']}*{R['L_dd']})*1.1,0)", 75),
    ("MC4 connectors", "Pair, 1000 V DC rated", "pair", f"={R['n_str']}*4", 150),
    ("DC distribution box (DCDB)", "IP65; 2 x DC MCB 2P 20 A 600 V; 2 x DC SPD Type 2; PE bar", "set", "=1", 7500),
    ("AC distribution box (ACDB)", "IP65; MCB 2P 32 A C; RCCB 2P 40 A 30 mA; AC SPD Type 2; N & PE bars", "set", "=1", 6500),
    ("AC cable", "3C Cu armoured 10 mm2 (10% wastage)", "m", f"=ROUNDUP(({R['L_ia']}+{R['L_am']})*1.1,0)", 350),
    ("Earth pit", "Maintenance-free (chemical) earth electrode with inspection chamber", "nos", f"={R['n_pits']}", 3500),
    ("GI strip", "25 x 3 mm hot-dip GI (roof, down conductors, pit interconnection)", "m",
     f"={R['strip_roof']}+2*{R['bldg_h']}+{R['strip_gnd']}", 150),
    ("Earth wire", "Cu 6 mm2 green-yellow (frame bonding + run to pit)", "m", f"=ROUNDUP({R['n_str']}*Stringing!$C$31+25,0)", 55),
    ("Air terminal", "3 m GI/Cu air terminal with base plate", "nos", "=2", 3750),
    ("Net meter", "Bi-directional (import/export) meter, as per DISCOM", "nos", "=1", 6000),
    ("Conduit, tray & accessories", "HDPE/GI conduit, cable tray, glands, lugs, markers", "lot", "=1", 8000),
    ("Installation & commissioning", "Erection, testing, commissioning, net-metering paperwork", "lot", "=1", 25000),
]
for i, (item, spec, unit, qty, rate) in enumerate(bom):
    r = 5 + i
    put(ws_b, f"A{r}", i + 1, f_norm, "0")
    put(ws_b, f"B{r}", item)
    put(ws_b, f"C{r}", spec, f_note, align=wrap)
    put(ws_b, f"D{r}", unit)
    put(ws_b, f"E{r}", qty, f_link if "Assumptions" in qty else f_norm, "#,##0")
    put(ws_b, f"F{r}", rate, f_in, "#,##0", fill_in)
    put(ws_b, f"G{r}", f"=E{r}*F{r}", f_norm, "#,##0")
last = 4 + len(bom)
tr = last + 1
put(ws_b, f"B{tr}", "Total project cost", f_bold)
put(ws_b, f"G{tr}", f"=SUM(G5:G{last})", f_bold, "#,##0")
put(ws_b, f"B{tr + 1}", "Cost per Wp (INR/Wp)")
put(ws_b, f"G{tr + 1}", f"=G{tr}/({S['kwp']}*1000)", f_norm, "0.0")
put(ws_b, f"B{tr + 2}", "Capital subsidy (assumed)")
put(ws_b, f"G{tr + 2}", f"={R['subsidy']}", f_link, "#,##0")
put(ws_b, f"B{tr + 3}", "Net investment after subsidy", f_bold)
put(ws_b, f"G{tr + 3}", f"=G{tr}-G{tr + 2}", f_bold, "#,##0")
BOM_TOTAL = f"BOM_Cost!$G${tr}"
BOM_PERWP = f"BOM_Cost!$G${tr + 1}"
BOM_NET = f"BOM_Cost!$G${tr + 3}"
BOM_LAST = last

# ================================================================ PAYBACK
title(ws_pb, "Savings, Payback & 25-Year Cash Flow",
      "Energy credited, tariff escalation and degradation come from Assumptions / Generation.")
widths(ws_pb, [8, 16, 12, 14, 12, 14, 14, 16, 12])
put(ws_pb, "A4", "Total project cost (INR)", f_bold); ws_pb.merge_cells("A4:C4")
put(ws_pb, "D4", f"={BOM_TOTAL}", f_link, "#,##0")
put(ws_pb, "A5", "Net investment after subsidy (INR)", f_bold); ws_pb.merge_cells("A5:C5")
put(ws_pb, "D5", f"={BOM_NET}", f_link, "#,##0")
put(ws_pb, "A6", "Year-1 savings (INR)", f_bold); ws_pb.merge_cells("A6:C6")
put(ws_pb, "D6", "=D12", f_norm, "#,##0")
put(ws_pb, "A7", "Simple payback - with subsidy (years)", f_bold); ws_pb.merge_cells("A7:C7")
put(ws_pb, "D7", '=IF(SUM(I12:I36)=0,"> 25",SUM(I12:I36))', f_bold, "0.0")
put(ws_pb, "A8", "Simple payback - without subsidy, yr-1 savings (years)", f_bold); ws_pb.merge_cells("A8:C8")
put(ws_pb, "D8", "=D4/D6", f_norm, "0.0")
put(ws_pb, "F4", "25-year net benefit (INR)", f_bold); ws_pb.merge_cells("F4:G4")
put(ws_pb, "H4", "=H36", f_norm, "#,##0")
put(ws_pb, "F5", "Project IRR (25 yr, with subsidy)", f_bold); ws_pb.merge_cells("F5:G5")
put(ws_pb, "H5", "=IRR(G11:G36)", f_norm, "0.0%")
put(ws_pb, "F6", "Lifetime energy credited (kWh)", f_bold); ws_pb.merge_cells("F6:G6")
put(ws_pb, "H6", "=SUM(B12:B36)", f_norm, "#,##0")
put(ws_pb, "F7", "CO2 avoided (tonnes)", f_bold); ws_pb.merge_cells("F7:G7")
put(ws_pb, "H7", f"=H6*{R['ef']}/1000", f_norm, "#,##0")
header(ws_pb, 10, ["Year", "Energy credited (kWh)", "Tariff (INR/kWh)", "Savings (INR)", "O&M (INR)",
                   "Inverter repl. (INR)", "Net cash flow (INR)", "Cumulative (INR)", "Payback helper"])
ws_pb.row_dimensions[10].height = 40
put(ws_pb, "A11", 0, f_norm, "0")
for col in "BCDEFI":
    put(ws_pb, f"{col}11", "")
put(ws_pb, "G11", "=-D5", f_norm, "#,##0;(#,##0);-")
put(ws_pb, "H11", "=G11", f_norm, "#,##0;(#,##0);-")
for y in range(1, 26):
    r = 11 + y
    put(ws_pb, f"A{r}", y, f_norm, "0")
    put(ws_pb, f"B{r}", f"=Generation!$D$35*(1-{R['deg']})^(A{r}-1)", f_norm, "#,##0")
    put(ws_pb, f"C{r}", f"={R['tariff']}*(1+{R['esc']})^(A{r}-1)", f_norm, "0.00")
    put(ws_pb, f"D{r}", f"=B{r}*C{r}", f_norm, "#,##0")
    put(ws_pb, f"E{r}", f"=-{R['om']}", f_norm, "#,##0;(#,##0);-")
    put(ws_pb, f"F{r}", f"=IF(A{r}={R['inv_year']},-{R['inv_cost']},0)", f_norm, "#,##0;(#,##0);-")
    put(ws_pb, f"G{r}", f"=D{r}+E{r}+F{r}", f_norm, "#,##0;(#,##0);-")
    put(ws_pb, f"H{r}", f"=H{r - 1}+G{r}", f_norm, "#,##0;(#,##0);-")
    put(ws_pb, f"I{r}", f"=IF(AND(H{r - 1}<0,H{r}>=0),(A{r}-1)+(-H{r - 1})/G{r},0)", f_note, "0.0")

# ================================================================ SUMMARY
title(ws_sum, "5.4 kWp Rooftop On-Grid Solar PV System - Design Summary",
      "Self-study portfolio design. All values below are live links to the calculation sheets. Not for construction.")
widths(ws_sum, [44, 22, 14, 4, 40])
header(ws_sum, 4, ["Item", "Value", "Unit"])
summ = [
    ("Site", f"={R['site']}", "", None),
    ("Array size (STC)", f"={S['kwp']}", "kWp", "0.00"),
    ("Modules", f'=TEXT({R["n_mod"]},"0")&" x "&TEXT({R["mod_wp"]},"0")&" Wp"', "", None),
    ("String configuration", f'=TEXT({R["n_str"]},"0")&" strings x "&TEXT({R["n_ser"]},"0")&" modules"', "", None),
    ("Inverter", f'=TEXT({R["inv_kw"]},"0.0")&" kW, 1-phase, "&TEXT({R["n_mppt"]},"0")&" MPPT"', "", None),
    ("DC / AC ratio", f"={S['dcac']}", "-", "0.00"),
    ("String Voc at minimum temperature", f"={S['v_str_oc']}", "V", "0.0"),
    ("String Vmp window (hot ... cold)", f'=TEXT({S["v_str_h"]},"0")&" ... "&TEXT({S["v_str_c"]},"0")', "V", None),
    ("Annual consumption (illustrative)", f"={L['annual']}", "kWh", "#,##0"),
    ("Estimated annual generation", f"={L['gen']}", "kWh", "#,##0"),
    ("Specific yield", "=Generation!D33", "kWh/kWp/yr", "#,##0"),
    ("Performance ratio", "=Generation!B14", "%", "0.0%"),
    ("Capacity utilisation factor", "=Generation!D34", "%", "0.0%"),
    ("Energy credited to bill (year 1)", "=Generation!D35", "kWh", "#,##0"),
    ("DC voltage drop (worst string)", "=Cables!I8", "%", "0.00%"),
    ("AC voltage drop (total)", "=Cables!I13", "%", "0.00%"),
    ("Row pitch / min. roof footprint", '=TEXT(Stringing!C29,"0.00")&" m / "&TEXT(Stringing!C34,"0")&" m2"', "", None),
    ("Total project cost (illustrative)", f"={BOM_TOTAL}", "INR", "#,##0"),
    ("Cost per Wp", f"={BOM_PERWP}", "INR/Wp", "0.0"),
    ("Net investment after assumed subsidy", f"={BOM_NET}", "INR", "#,##0"),
    ("Simple payback (with subsidy)", "=Payback!D7", "years", "0.0"),
    ("Project IRR (25 years)", "=Payback!H5", "%", "0.0%"),
    ("CO2 avoided over 25 years", "=Payback!H7", "tonnes", "#,##0"),
]
for i, (lab, fml, unit, fmt) in enumerate(summ):
    r = 5 + i
    put(ws_sum, f"A{r}", lab)
    put(ws_sum, f"B{r}", fml, f_link, fmt, align=Alignment(horizontal="right"))
    put(ws_sum, f"C{r}", unit)
r = 5 + len(summ) + 1
put(ws_sum, f"A{r}", "Design checks passed (OK)", f_bold)
oks = ('=COUNTIF(Stringing!F5:F40,"OK")+COUNTIF(Load_Sizing!F16:F17,"OK")+COUNTIF(Cables!M5:N14,"OK")'
       '+COUNTIF(Protection!G5:G21,"OK")')
put(ws_sum, f"B{r}", oks, f_bold, "0", align=Alignment(horizontal="right"))
put(ws_sum, f"A{r + 1}", "Design checks failed (CHECK)", f_bold)
bad = ('=COUNTIF(Stringing!F5:F40,"CHECK")+COUNTIF(Load_Sizing!F16:F17,"CHECK")+COUNTIF(Cables!M5:N14,"CHECK")'
       '+COUNTIF(Protection!G5:G21,"CHECK")')
put(ws_sum, f"B{r + 1}", bad, f_bold, "0", align=Alignment(horizontal="right"))
ws_sum.conditional_formatting.add(f"B{r + 1}", CellIsRule(operator="greaterThan", formula=["0"], fill=fill_bad))
ws_sum.conditional_formatting.add(f"B{r + 1}", CellIsRule(operator="equal", formula=["0"], fill=fill_ok))

put(ws_sum, "E4", "How to read this workbook", f_hdr, fill=fill_hdr, align=center)
guide = [
    "Assumptions - every input in one place (blue on yellow).",
    "Load_Sizing - consumption to array size.",
    "Stringing - voltage/current checks + row spacing.",
    "Cables - sizing, ampacity, voltage drop.",
    "Protection - MCB/RCCB/SPD, earthing, lightning check.",
    "Generation - PR, monthly kWh, chart.",
    "BOM_Cost - quantities and budgetary cost.",
    "Payback - 25-year cash flow, payback, IRR.",
    "",
    "Colour code: blue = input, black = formula,",
    "green = link from another sheet.",
    "",
    "Module/inverter values are representative.",
    "Irradiation, load, rates and subsidy are",
    "assumptions - replace with real data.",
]
for i, t in enumerate(guide):
    put(ws_sum, f"E{5 + i}", t, f_norm, border=False)

for ws in wb.worksheets:
    ws.sheet_properties.tabColor = "1F3864" if ws.title in ("Summary", "Assumptions") else "8EA9DB"

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print("saved", OUT)
