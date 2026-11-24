
Electrical Design: 5.4 kWp Rooftop On-Grid Solar PV

A single-phase, net-metered rooftop solar design worked out the way an EPC design desk would: sizing, string design, cable and protection selection, earthing, and a full drawing set. Everything is tied to one calculation workbook, so a number changed in one place changes everywhere.

> Practice project for an illustrative house in Kolkata. Not for construction.

The design in numbers

- **Array:** 10 x 540 Wp = **5.4 kWp**, 2 strings x 5 modules, 22° tilt, south
- **Inverter:** 5 kW, single-phase, 2 MPPT (DC/AC ratio 1.08)
- **String check:** Voc 260.9 V at 5 °C (limit 600 V); Vmp 175-223 V (MPPT window 90-550 V)
- **Cables:** 4 sq.mm Cu on DC, 3C x 10 sq.mm Cu on AC
- **Voltage drop:** DC 0.85 %, AC 0.83 % (both under 1 %)
- **Protection:** DC MCB 20 A per string, AC MCB 32 A, RCCB 40 A / 30 mA, Type 2 SPD on both sides
- **Earthing and LPS:** 4 bonded earth pits, 2 air terminals, rolling-sphere check passed
- **Expected output:** about 7,400 kWh/year (PR 76.6 %)

What's inside

- **`calculations/Solar_PV_Design_Calculations.xlsx`**: string sizing, row spacing, cable sizing and voltage drop, protection ratings, earthing, generation, BOM and payback. Inputs are in blue on the Assumptions sheet; everything else is a live formula.
- **`drawings/`**: 8 A3 sheets as DXF (open in AutoCAD) and PDF.
  - E-01 cover and index
  - E-02 DC single line
  - E-03 AC single line
  - E-04 roof plan and row spacing
  - E-05 earthing and lightning protection
  - E-06 DCDB/ACDB wiring
  - E-07 equipment mounting and routing
  - E-08 cable schedule and BOM

Why Python

A solar design repeats the same numbers in many places: module count, string length, cable size, breaker rating. In a normal workflow these get retyped on every drawing, and one missed edit leaves the drawings disagreeing with the calculation. I used Python to avoid that.

- **openpyxl** builds the Excel workbook with real formulas, not pasted values. The workbook is the single source of truth.
- **LibreOffice recalculation** evaluates all formulas and confirms there are no errors, so the drawings read calculated values.
- **ezdxf** reads those values and draws the DXF sheets: single lines, roof plan, earthing layout, wiring, schedules.
- **matplotlib** renders the same drawings to PDF.

Result: change the module count or a cable length once, and the calculation, drawings and BOM stay consistent. The drawings are script-generated, then audited as DXF files (0 errors on all 8 sheets).

Assumptions to know about

- Module and inverter data are typical values for the class, not a specific datasheet.
- Monthly sunshine hours, household load, rates, tariff and subsidy are my assumptions. Check them before trusting the cost or payback numbers.
- Cable ampacities are indicative, and the lightning layout needs a proper risk assessment on a real job.
- Design basis only, not a compliance claim: IEC 62548, IEC 60364-7-712, IEC 60364-5-52, IEC 62305, IS 3043.

Built by Suvadeep Mallik, B.Tech Electrical Engineering.
