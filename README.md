 5.4 kWp Rooftop Solar PV: Electrical Design

I'm an electrical engineer learning AutoCAD Electrical, and I wanted one project that shows how a rooftop solar system is actually designed from start to finish. This is that project: a 5.4 kWp, single-phase, grid-connected system for an imaginary house in Kolkata, with a calculation workbook and a set of 8 drawings.

It's a practice design, not meant for construction.

What the system looks like

- **Panels:** 10 modules of 540 Wp, arranged as 2 strings of 5, tilted 22° facing south
- **Inverter:** 5 kW single-phase with 2 MPPT inputs
- **Cables:** 4 sq.mm copper on the DC side, 3C x 10 sq.mm copper on the AC side
- **Voltage drop:** about 0.85 % on DC and 0.83 % on AC, both under 1 %
- **Protection:** DC MCB 20 A per string, AC MCB 32 A, RCCB 40 A / 30 mA, and surge protection on both sides
- **Earthing and lightning:** 4 bonded earth pits and 2 air terminals
- **Expected output:** around 7,400 kWh a year

What's in this repo

- **`calculations/`** has the Excel workbook. It covers string sizing, row spacing, cable sizing, protection ratings, earthing, generation, BOM and payback. Blue cells are inputs, everything else is a formula.
- **`drawings/`** has 8 A3 sheets in DXF (for AutoCAD) and PDF:
  - E-01 Cover, index and design data
  - E-02 DC single line diagram
  - E-03 AC single line diagram
  - E-04 Roof plan and row spacing
  - E-05 Earthing and lightning protection
  - E-06 DCDB / ACDB wiring
  - E-07 Equipment mounting and routing
  - E-08 Cable schedule and BOM

Why I used Python

In a solar design the same numbers show up everywhere: module count, string length, cable size, breaker rating. If you change one and forget to update a drawing, the paperwork stops matching. I used Python so that can't happen.

- **openpyxl** builds the workbook with real formulas, so Excel is the one place the numbers come from.
- **ezdxf** reads those values and draws the DXF sheets.
- **matplotlib** turns the same drawings into PDFs.

Change an input once and the calculation, drawings and BOM all follow. The drawings are script-generated, and I checked all 8 DXF files for errors (none found).

Things to keep in mind

- Module and inverter data are typical values, not from a specific datasheet.
- Sunshine hours, household load, tariff and subsidy are my own assumptions, so check them before trusting the cost and payback figures.
- Cable ratings are indicative, and a real project would need a proper lightning risk assessment.
- Standards such as IEC 62548, IEC 60364-7-712 and IEC 62305 were used as design reference only, not as a compliance claim.

Suvadeep Mallik, B.Tech Electrical Engineering
