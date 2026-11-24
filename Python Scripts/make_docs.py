"""Writes README.md and docs/DESIGN_NOTES.md using the numbers in the Excel workbook."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import design_data

ROOT = Path(__file__).resolve().parent.parent
D = design_data.load()


def f(x, d=1):
    return f"{x:,.{d}f}"


def p(x, d=2):
    return f"{x * 100:.{d}f}"


bom_rows = "\n".join(f"| {n} | {item} | {spec} | {unit} | {qty:,.0f} |" for n, item, spec, unit, qty in D["bom"])
mon = "\n".join(f"| {m} | {g:,.0f} | {l:,.0f} |" for m, g, l in D["months"])
earth_wire = next(b for b in D["bom"] if b[1] == "Earth wire")[4]

README = f"""# {f(D['kwp'], 1)} kWp Rooftop On-Grid Solar PV System - Electrical Design

A complete, self-study electrical design of a **single-phase, net-metered rooftop solar PV system**:
an 8-sheet drawing set (single line diagrams, roof layout, earthing & lightning protection, panel wiring,
equipment mounting, schedules) and a formula-driven Excel calculation workbook.
Drawings and calculations are linked, so every rating and quantity on a drawing matches the workbook.

> **Status: portfolio study for an illustrative site - not for construction.**
> Module and inverter data are representative values, and irradiation, load, rates and subsidy are stated assumptions
> (see [Assumptions & limitations](#assumptions--limitations)).

![DC side single line diagram](images/E-02.png)

## At a glance

| Item | Value |
|---|---|
| Site (illustrative) | {D['site']} |
| Array | {D['n_mod']:.0f} x {D['mod_wp']:.0f} Wp = **{f(D['kwp'], 2)} kWp**, {D['n_str']:.0f} strings x {D['n_ser']:.0f} modules |
| Inverter | {f(D['inv_kw'], 0)} kW, single-phase, 2 MPPT (DC/AC ratio {f(D['dcac'], 2)}) |
| String Voc at {D['tmin']:.0f} deg C | {f(D['v_str_oc'], 1)} V (inverter limit {D['vdc_max']:.0f} V) |
| String Vmp window | {f(D['v_str_h'], 0)} - {f(D['v_str_c'], 0)} V (MPPT range {D['mppt_min']:.0f} - {D['mppt_max']:.0f} V) |
| Tilt / orientation | {D['tilt']:.0f} deg / south, row pitch {f(D['pitch'], 2)} m (no shade 09:00-15:00 on 21 Dec) |
| Protection | DC MCB {D['dc_mcb']:.0f} A per string, AC MCB {D['ac_mcb']:.0f} A, RCCB {D['rccb']:.0f} A / {D['rcd_ma']:.0f} mA, Type 2 SPDs on DC and AC |
| Voltage drop | DC {p(D['vd_dc'])} % (limit 1.5 %), AC {p(D['vd_ac'])} % (limit 2 %) |
| Earthing & LPS | {D['n_pits']:.0f} earth pits bonded by a GI ring, 2 air terminals, rolling-sphere check done |
| Estimated generation | {f(D['gen'], 0)} kWh/year ({f(D['yield'], 0)} kWh/kWp, PR {p(D['pr'], 1)} %) |
| Budgetary cost (illustrative) | INR {f(D['capex'], 0)} (INR {f(D['perwp'], 1)}/Wp) |
| Simple payback (illustrative) | {f(D['payback'], 1)} years with the assumed subsidy |

## What this project covers

- PV system sizing from electricity consumption
- String design against inverter voltage / current limits (cold Voc, hot Vmp, Isc)
- Row-spacing and roof-layout geometry from sun position
- DC and AC cable sizing: ampacity, derating, voltage drop
- Protection selection and coordination (MCB, RCCB, SPD, isolators)
- Earthing, equipotential bonding and a lightning-protection check
- Single line diagrams, wiring schematics, schedules and BOM in a consistent drawing set
- Calculations linked to drawings so numbers never contradict each other

## Drawing gallery

| | |
|---|---|
| ![E-03](images/E-03.png) | ![E-04](images/E-04.png) |
| ![E-05](images/E-05.png) | ![E-06](images/E-06.png) |

## Repository structure

```
solar-pv-design/
├── README.md
├── calculations/
│   └── Solar_PV_Design_Calculations.xlsx   <- 9 sheets, live formulas
├── drawings/
│   ├── Solar_PV_Drawing_Set.pdf            <- all 8 sheets in one PDF
│   ├── dxf/   E-01.dxf ... E-08.dxf        <- open in AutoCAD / AutoCAD Electrical
│   └── pdf/   E-01.pdf ... E-08.pdf
├── images/    E-01.png ... E-08.png        <- previews
├── docs/
│   └── DESIGN_NOTES.md                     <- step-by-step design calculations
└── scripts/                                <- rebuilds the workbook, drawings and docs
```

## Drawing set (A3)

| Sheet | Title | Preview |
|---|---|---|
| E-01 | Cover sheet, drawing index, design data, general notes, symbols | [PNG](images/E-01.png) |
| E-02 | DC side single line diagram | [PNG](images/E-02.png) |
| E-03 | AC side single line diagram | [PNG](images/E-03.png) |
| E-04 | Roof plan - array layout, string routing, row-spacing section | [PNG](images/E-04.png) |
| E-05 | Earthing & lightning protection layout | [PNG](images/E-05.png) |
| E-06 | DCDB & ACDB internal wiring schematic | [PNG](images/E-06.png) |
| E-07 | Equipment mounting elevation & building cable/earth routes | [PNG](images/E-07.png) |
| E-08 | Cable schedule & bill of materials | [PNG](images/E-08.png) |

## Excel workbook

| Sheet | What it does |
|---|---|
| Summary | Key results (all live links) and a pass / fail count of design checks |
| Assumptions | Every input in one place (blue on yellow) with a source / note |
| Load_Sizing | Monthly consumption to required array size |
| Stringing | Voc / Vmp / Isc checks against the inverter window, row-spacing geometry |
| Cables | Cable size, ampacity (Ib <= In <= Iz) and voltage drop |
| Protection | MCB / RCCB / SPD selection, earthing summary, rolling-sphere check |
| Generation | Loss tree, performance ratio, monthly generation vs consumption, chart |
| BOM_Cost | Quantities linked to the design, illustrative rates and cost |
| Payback | 25-year cash flow, payback, IRR, CO2 avoided |

Colour code: **blue = input, black = formula, green = link from another sheet**.
Change an input (for example the module count or cable length) and the whole workbook recalculates.

## Design flow

1. **Load and size.** Annual consumption of {f(D['load'], 0)} kWh (illustrative profile) divided by the specific yield gives about {f(D['load'] / D['yield'], 2)} kWp; rounded up to {D['n_mod']:.0f} modules of {D['mod_wp']:.0f} Wp.
2. **String design.** Cold-weather Voc and hot-weather Vmp are checked against the inverter limits; {D['n_ser']:.0f} modules per string is inside the allowed {D['n_min']:.0f} - {D['n_max']:.0f}.
3. **Roof layout.** Row pitch from sun position at 09:00 on 21 December; minimum roof footprint {f(D['roof_min'], 0)} m2.
4. **Cables.** 4 sq.mm Cu PV cable on DC and 10 sq.mm Cu armoured cable on AC; each run checked for ampacity and voltage drop.
5. **Protection.** Devices sized from Isc and the inverter's maximum AC current, then checked against cable ampacity.
6. **Earthing & lightning.** Four bonded earth pits and two air terminals; rolling-sphere check (protected radius {f(D['rp'], 2)} m against {f(D['rp_need'], 2)} m needed).
7. **Yield & economics.** Loss tree gives PR {p(D['pr'], 1)} %; monthly offset, cost and payback follow.

Full working is in [docs/DESIGN_NOTES.md](docs/DESIGN_NOTES.md).

## Bill of materials (from the workbook)

| # | Item | Specification | Unit | Qty |
|---|---|---|---|---|
{bom_rows}

## How to use

- **Look at the design:** open `drawings/Solar_PV_Drawing_Set.pdf` or the PNGs in `images/`.
- **Edit in CAD:** open any file in `drawings/dxf/` with AutoCAD (or any DXF-compatible CAD) and refine or re-draft.
- **Change the design:** edit the blue cells on the `Assumptions` sheet of the workbook.
- **Rebuild everything** (Python 3.10+):

```bash
pip install -r requirements.txt
python scripts/build_excel.py          # writes the workbook
# recalculate once in Excel/LibreOffice so values are cached, then:
python scripts/make_drawings.py        # DXF + PDF + PNG, read from the workbook
python scripts/make_docs.py            # README + design notes
```

## Assumptions & limitations

- **Illustrative site.** Not a real client project; there is no site survey, roof structural check or shading analysis.
- **Representative equipment.** Module and inverter values are typical for the class (540 Wp, 5 kW 2-MPPT). Replace them with a real datasheet before relying on any number.
- **Irradiation is approximate.** Monthly peak-sun-hours are approximate climatological values for Kolkata; use PVGIS, NASA POWER or PVsyst for real work.
- **Load is illustrative.** The monthly consumption profile is assumed; use real electricity bills.
- **Costs are budgetary.** Rates (INR, taxes included), tariff, escalation and the capital subsidy are assumptions. Verify the subsidy scheme rules and the DISCOM tariff before quoting any payback.
- **Cable ampacities are indicative.** Base ratings and derating factors must be checked against the actual cable datasheet and the applicable code.
- **Lightning protection is indicative.** A site risk assessment (IEC 62305-2) decides the real protection level.
- **Single-phase 230 V** is assumed; the sanctioned load and phase type must be confirmed with the DISCOM.
- **Standards** are listed as the design basis only; compliance has not been audited.

## Tools & method

- **Microsoft Excel / LibreOffice:** calculation workbook (openpyxl used to build it, LibreOffice to recalculate and verify: 0 formula errors).
- **Python + ezdxf + matplotlib:** the DXF drawings are generated by script from the workbook values, so drawings and calculations cannot drift apart. PDF and PNG previews are rendered from the same DXF files.
- **AutoCAD / AutoCAD Electrical:** the DXF files open directly in AutoCAD and can be used as a base for re-drafting with AutoCAD Electrical symbols and project tools.

## Standards used as design basis

IEC 62548 (PV array design), IEC 60364-7-712 (PV supply systems), IEC 60364-5-52 (current ratings),
IEC 62305 (lightning protection), IS 3043 (earthing), IEC 61643-31 / 61643-11 (SPDs), EN 50618 (solar cables),
IEC 62109-1 (inverter safety).

## Author

Suvadeep Mallik - B.Tech Electrical Engineering, aspiring AutoCAD Electrical designer.
"""

NOTES = f"""# Design Notes - {f(D['kwp'], 1)} kWp Rooftop On-Grid Solar PV

Working for every number used in the drawings. All values come from
`calculations/Solar_PV_Design_Calculations.xlsx`; the sheet name is given in brackets.

## 1. Design inputs  [Assumptions]

| Item | Value |
|---|---|
| Location | {D['site']}, latitude {D['lat']:.2f} N |
| Design temperatures | minimum ambient {D['tmin']:.0f} deg C, maximum cell {D['tcell']:.0f} deg C |
| Module (representative) | {D['mod_wp']:.0f} Wp; Voc {D['voc']} V; Vmp {D['vmp']} V; Isc {D['isc']} A; Imp {D['imp']} A; {D['mod_L'] * 1000:.0f} x {D['mod_W'] * 1000:.0f} mm |
| Temperature coefficients | Voc -0.27 %/deg C; Pmax (and Vmp) -0.35 %/deg C |
| Inverter (representative) | {f(D['inv_kw'], 0)} kW, 1-phase {D['vac']:.0f} V, 2 MPPT, {D['mppt_min']:.0f}-{D['mppt_max']:.0f} V MPPT, {D['vdc_max']:.0f} V max, {D['iac_max']} A max AC |

## 2. System sizing  [Load_Sizing]

- Annual consumption (illustrative profile): **{f(D['load'], 0)} kWh**
- Specific yield: **{f(D['yield'], 0)} kWh/kWp/year**
- Required size = {f(D['load'], 0)} / {f(D['yield'], 0)} = **{f(D['load'] / D['yield'], 2)} kWp**
- Modules required = ROUNDUP({f(D['load'] / D['yield'], 2)} x 1000 / {D['mod_wp']:.0f}) = **{D['n_mod']:.0f}**
- Installed size = {D['n_mod']:.0f} x {D['mod_wp']:.0f} Wp = **{f(D['kwp'], 2)} kWp**; DC/AC ratio = {f(D['kwp'], 2)} / {f(D['inv_kw'], 0)} = {f(D['dcac'], 2)}

## 3. String design  [Stringing]

| Quantity | Formula | Result |
|---|---|---|
| Module Voc at {D['tmin']:.0f} deg C | Voc x (1 + a_Voc x (Tmin - 25)) | {f(D['voc_c'], 2)} V |
| Module Vmp at {D['tcell']:.0f} deg C | Vmp x (1 + g_Pmax x (Tcell - 25)) | {f(D['vmp_h'], 2)} V |
| Module Vmp at {D['tmin']:.0f} deg C | Vmp x (1 + g_Pmax x (Tmin - 25)) | {f(D['vmp_c'], 2)} V |
| Max modules per string | ROUNDDOWN({D['vdc_max']:.0f} / {f(D['voc_c'], 2)}) | {D['n_max']:.0f} |
| Min modules per string | ROUNDUP({D['mppt_min']:.0f} / {f(D['vmp_h'], 2)}) | {D['n_min']:.0f} |
| Selected | {D['n_ser']:.0f} in series x {D['n_str']:.0f} strings | OK |
| String Voc (cold) | {D['n_ser']:.0f} x {f(D['voc_c'], 2)} | {f(D['v_str_oc'], 1)} V (limit {D['vdc_max']:.0f} V) |
| String Vmp (hot) | {D['n_ser']:.0f} x {f(D['vmp_h'], 2)} | {f(D['v_str_h'], 1)} V (min {D['mppt_min']:.0f} V) |
| String Vmp (cold) | {D['n_ser']:.0f} x {f(D['vmp_c'], 2)} | {f(D['v_str_c'], 1)} V (max {D['mppt_max']:.0f} V) |

One string per MPPT input, so each MPPT carries {D['imp']} A (limit 16 A) and Isc {D['isc']} A (limit 20 A).

## 4. Row spacing  [Stringing]

Design day: 21 December, 09:00 solar time, latitude {D['lat']:.2f} N.

- Solar altitude = {f(D['alt'], 1)} deg, azimuth from south = {f(D['azi'], 1)} deg
- Module rise = {D['mod_L']} x sin({D['tilt']:.0f} deg) = {f(D['rise'], 3)} m; horizontal projection = {f(D['proj'], 3)} m
- Clear gap = rise x cos(azimuth) / tan(altitude) = **{f(D['gap'], 2)} m**; row pitch = **{f(D['pitch'], 2)} m**
- Array footprint {f(D['width'], 2)} x {f(D['depth'], 2)} m; with 1 m clearance, minimum roof = **{f(D['roof_min'], 1)} m2**

## 5. Cables  [Cables]

Rule: **Ib <= In <= Iz** and voltage drop within the design limit.

| Tag | Run | Cable | Length | Ib | Device | Iz | VD |
|---|---|---|---|---|---|---|---|
| DC-1 | String 1 to DCDB | 2 x {D['dc_size']:.0f} sq.mm Cu | {D['L_s1']:.0f} m | {f(D['ib_dc'], 1)} A | {D['dc_mcb']:.0f} A | {f(D['iz_dc'], 1)} A | {p(D['vd_s1'])} % |
| DC-2 | String 2 to DCDB | 2 x {D['dc_size']:.0f} sq.mm Cu | {D['L_s2']:.0f} m | {f(D['ib_dc'], 1)} A | {D['dc_mcb']:.0f} A | {f(D['iz_dc'], 1)} A | {p(D['vd_s2'])} % |
| DC-3 | DCDB to inverter | 2 x {D['dc_size']:.0f} sq.mm Cu | {D['L_dd']:.0f} m | {f(D['ib_dc'], 1)} A | {D['dc_mcb']:.0f} A | {f(D['iz_dc'], 1)} A | {p(D['vd_dd'])} % |
| AC-1 | Inverter to ACDB | 3C x {D['ac_size']:.0f} sq.mm Cu | {D['L_ia']:.0f} m | {D['iac_max']} A | {D['ac_mcb']:.0f} A | {f(D['iz_ac'], 1)} A | {p(D['vd_ia'])} % |
| AC-2 | ACDB to meter / main DB | 3C x {D['ac_size']:.0f} sq.mm Cu | {D['L_am']:.0f} m | {D['iac_max']} A | {D['ac_mcb']:.0f} A | {f(D['iz_ac'], 1)} A | {p(D['vd_am'])} % |

- DC design current Ib = 1.25 x Isc = 1.25 x {D['isc']} = {f(D['ib_dc'], 1)} A; voltage drop uses Imp = {D['imp']} A.
- DC voltage drop = 2 x L x I x rho / A, with rho = 0.021 ohm.mm2/m (Cu, about 70 deg C). Worst string total = **{p(D['vd_dc'])} %** (limit 1.5 %).
- AC voltage drop total = **{p(D['vd_ac'])} %** (limit 2 %).
- Iz = base rating x derating; the base ratings used are indicative and must be checked against the real cable datasheet.

## 6. Protection  [Protection]

| Device | Rule | Result |
|---|---|---|
| DC MCB 2P (per string) | In >= 1.25 x Isc = {f(1.25 * D['isc'], 1)} A; In <= Iz and <= module max fuse (25 A) | **{D['dc_mcb']:.0f} A**, {D['dc_dev_v']:.0f} V DC |
| DC SPD Type 2 | Uc >= string Voc cold ({f(D['v_str_oc'], 1)} V) | Uc {D['dc_spd_uc']:.0f} V DC |
| AC MCB 2P, C-curve | In >= 1.25 x {D['iac_max']} A = {f(1.25 * D['iac_max'], 1)} A; In <= Iz | **{D['ac_mcb']:.0f} A** |
| RCCB 2P Type A | one size above the MCB | **{D['rccb']:.0f} A / {D['rcd_ma']:.0f} mA** |
| AC SPD Type 2 | Uc >= 1.1 x {D['vac']:.0f} V = {f(1.1 * D['vac'], 0)} V | Uc {D['ac_spd_uc']:.0f} V AC |
| AC isolator 2P | In >= MCB rating, lockable | **{D['ac_iso']:.0f} A** |

Because each string has its own MPPT input, no string fuses are required: the maximum reverse current is below the module's series-fuse rating.

## 7. Earthing and lightning protection  [Protection]

- Four earth pits: EP-1 equipment (frames, DCDB, inverter), EP-2 AC / neutral, EP-3 and EP-4 lightning; all bonded by a 25 x 3 mm GI strip ring. Target <= {D['r_earth']:.0f} ohm each, to be proven by measurement.
- Two air terminals, {D['rod_h']:.1f} m above the roof, {D['rod_off']:.1f} m outside the array at mid-depth.
- Rolling-sphere check (R = {D['r_sph']:.0f} m): protected radius at array top = sqrt(h(2R-h)) - sqrt(hx(2R-hx)) = **{f(D['rp'], 2)} m**; farthest array point from the nearest rod = **{f(D['rp_need'], 2)} m** -> covered.
- This is an indicative layout only. The real protection level comes from a risk assessment (IEC 62305-2).

## 8. Energy yield  [Generation]

Performance ratio = product of (1 - loss) for soiling, temperature, mismatch, shading, DC cable, inverter, AC cable, availability and LID/other = **{p(D['pr'], 1)} %**.

Annual generation = {f(D['kwp'], 2)} kWp x {f(D['psh'], 2)} kWh/m2/day x 365 x PR = **{f(D['gen'], 0)} kWh** (CUF {p(D['cuf'], 1)} %).

| Month | Generation (kWh) | Consumption (kWh) |
|---|---|---|
{mon}

Peak-sun-hours are approximate assumptions for Kolkata and should be replaced with PVGIS / NASA POWER / PVsyst values.

## 9. Cost and payback  [BOM_Cost, Payback]

- Budgetary project cost (illustrative rates, taxes included): **INR {f(D['capex'], 0)}** = INR {f(D['perwp'], 1)}/Wp.
- Assumed capital subsidy: INR {f(D['subsidy'], 0)} (verify the scheme rules); net investment INR {f(D['net'], 0)}.
- Energy credited to the bill in year 1 (monthly offset, conservative): {f(D['credited'], 0)} kWh x INR {D['tariff']}/kWh = INR {f(D['sav1'], 0)}.
- Simple payback **{f(D['payback'], 1)} years**; 25-year IRR {p(D['irr'], 1)} %; about {f(D['co2'], 0)} t CO2 avoided over 25 years.
- Escalation, degradation, O&M and an inverter replacement in year 12 are included in the 25-year cash flow.

## 10. What a real project would add

Site survey and roof structural check, shading study, real module / inverter datasheets, DISCOM application and
net-metering approval, short-circuit / fault-level check, earth resistance test results, commissioning checklist,
and a formal design review.
"""

(ROOT / "README.md").write_text(README, encoding="utf-8")
(ROOT / "docs").mkdir(exist_ok=True)
(ROOT / "docs" / "DESIGN_NOTES.md").write_text(NOTES, encoding="utf-8")
(ROOT / "requirements.txt").write_text("ezdxf>=1.3\nmatplotlib>=3.8\nopenpyxl>=3.1\npypdf>=4.0\n", encoding="utf-8")
(ROOT / ".gitignore").write_text("__pycache__/\n*.pyc\n", encoding="utf-8")
print("docs written")
