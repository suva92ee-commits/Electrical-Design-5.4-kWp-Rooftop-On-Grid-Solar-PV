"""Drawing sheets E-01 .. E-04.  All numbers come from design_data.load() (the Excel workbook)."""
import math
from cad import Sheet

TOTAL = 8


def f(x, d=1):
    return f"{x:,.{d}f}"


def pct(x, d=2):
    return f"{x * 100:.{d}f}"


INDEX = [
    ("E-01", "Cover sheet, drawing index, design data & general notes"),
    ("E-02", "DC side single line diagram"),
    ("E-03", "AC side single line diagram"),
    ("E-04", "Roof plan - array layout, string routing, row spacing"),
    ("E-05", "Earthing & lightning protection layout"),
    ("E-06", "DCDB & ACDB internal wiring / connection schematic"),
    ("E-07", "Equipment mounting, cable routing & building section"),
    ("E-08", "Cable schedule & bill of materials"),
]


# =================================================================== E-01
def e01(D):
    s = Sheet("E-01", "COVER SHEET & DRAWING INDEX", "Design data, general notes, standards, symbols", 1, TOTAL)
    s.text(14, 276, "5.4 kWp ROOFTOP ON-GRID SOLAR PV SYSTEM", 7.5)
    s.text(14, 266, "ELECTRICAL DESIGN DRAWING SET", 4.2)
    s.text(14, 259.5, f"Site: {D['site']} (illustrative)  |  Grid-connected, net-metered, single-phase 230 V", 2.6, "NOTE")

    # drawing index
    s.text(14, 250, "DRAWING INDEX", 3.2)
    rows = [["DWG NO.", "TITLE", "REV"]] + [[a, b, "0"] for a, b in INDEX]
    s.table(14, 247, [20, 128, 12], rows, row_h=5.6, h=2.5, aligns=["L", "L", "C"])

    # design data
    s.text(14, 190, "KEY DESIGN DATA", 3.2)
    dd = [["PARAMETER", "VALUE"],
          ["Array size (STC)", f"{D['n_mod']} x {D['mod_wp']:.0f} Wp = {f(D['kwp'], 2)} kWp"],
          ["Configuration", f"{D['n_str']} strings x {D['n_ser']} modules in series"],
          ["Inverter", f"{f(D['inv_kw'], 1)} kW, 1-phase, {2} MPPT   (DC/AC {f(D['dcac'], 2)})"],
          ["String Voc @ {0} deg C".format(D['tmin']), f"{f(D['v_str_oc'], 1)} V   (limit {D['vdc_max']:.0f} V)"],
          ["String Vmp window", f"{f(D['v_str_h'], 0)} - {f(D['v_str_c'], 0)} V   (MPPT {D['mppt_min']:.0f}-{D['mppt_max']:.0f} V)"],
          ["Tilt / orientation", f"{D['tilt']:.0f} deg / south"],
          ["Est. annual generation", f"{f(D['gen'], 0)} kWh   ({f(D['yield'], 0)} kWh/kWp, PR {pct(D['pr'], 1)} %)"],
          ["Voltage drop DC / AC", f"{pct(D['vd_dc'])} % / {pct(D['vd_ac'])} %"],
          ["Protection", f"DC MCB {D['dc_mcb']:.0f} A | AC MCB {D['ac_mcb']:.0f} A | RCCB {D['rccb']:.0f} A/{D['rcd_ma']:.0f} mA"],
          ["Earthing / LPS", f"{D['n_pits']:.0f} earth pits, 2 air terminals, all bonded"]]
    s.table(14, 187, [44, 116], dd, row_h=5.6, h=2.4)

    # right column: notes
    s.text(190, 250, "GENERAL NOTES", 3.2)
    notes = [
        "1. This is a self-study portfolio design for an illustrative site. NOT FOR CONSTRUCTION.",
        "2. Module and inverter data are representative values; replace with the selected product datasheets.",
        "3. All dimensions in mm unless noted. Cable lengths in metres.",
        "4. Cables: DC = 1C Cu PV cable (EN 50618 type), AC = 3C Cu armoured. Sizes per cable schedule (E-08).",
        "5. DC and AC cables to run in separate conduits / tray compartments.",
        "6. All metal parts (module frames, structure, enclosures, inverter) to be bonded to earth.",
        "7. All earth pits to be interconnected (equipotential bonding). Target <= 5 ohm each, to be measured.",
        "8. Colour code: DC+ red, DC- black/blue, AC L brown (phase), N blue, PE green-yellow.",
        "9. Install lockable AC isolator accessible to the DISCOM; warning labels on every DC / AC box.",
        "10. Net-metering arrangement and sanctioned load subject to DISCOM approval.",
        "11. Lightning protection layout is indicative - final design needs a site risk assessment.",
        "12. Verify cable ampacities with the actual cable datasheets before ordering.",
    ]
    for i, n in enumerate(notes):
        s.text(190, 245 - i * 5.0, n, 2.2)

    s.text(190, 182, "STANDARDS REFERRED TO (design basis)", 3.2)
    stds = ["IEC 62548 - PV array design requirements", "IEC 60364-7-712 - Solar PV power supply systems",
            "IEC 60364-5-52 - Selection of wiring systems (current ratings)", "IEC 62305 - Protection against lightning",
            "IS 3043 - Code of practice for earthing", "IEC 61643-31 / 61643-11 - Surge protective devices (DC / AC)",
            "EN 50618 - Solar cables", "IEC 62109-1 - Safety of power converters for PV"]
    for i, t in enumerate(stds):
        s.text(190, 177 - i * 4.6, t, 2.2)
    s.text(190, 139, "Standards are listed as the design basis only; compliance must be confirmed on a real project.", 1.9, "NOTE")

    # legend
    s.text(190, 130, "SYMBOLS", 3.2)
    y = 122
    ent = [("PV module", lambda x, yy: s.module(x, yy - 3, 11, 7)),
           ("DC / AC breaker (MCB, 2P)", lambda x, yy: s.switch(x + 6, yy, "EQUIP", 12)),
           ("Surge protective device (SPD)", lambda x, yy: s.varistor(x + 6, yy + 4, yy - 4)),
           ("Earth electrode (pit)", lambda x, yy: s.earth(x + 6, yy + 3, "PEC", 3)),
           ("Bi-directional energy meter", lambda x, yy: s.meter(x + 6, yy, 4.5, "kWh")),
           ("Inverter (DC to AC)", lambda x, yy: (s.rect(x, yy - 4, 12, 8), s.line(x, yy - 4, x + 12, yy + 4)))]
    for i, (lab, fn) in enumerate(ent):
        yy = y - i * 9.5
        fn(192, yy)
        s.text(210, yy, lab, 2.3)
    lg = [("DCP", "DC positive"), ("DCN", "DC negative"), ("ACL", "AC phase (L)"), ("ACN", "AC neutral (N)"),
          ("PE", "Earth / PE conductor"), ("LPS", "Lightning conductor")]
    for i, (ly, lab) in enumerate(lg):
        yy = y - i * 9.5
        s.line(285, yy, 305, yy, ly)
        s.text(309, yy, lab, 2.3)
    s.text(285, 62, "Drawings E-02 to E-08 are generated from the Excel calculation workbook,", 1.9, "NOTE")
    s.text(285, 58.5, "so quantities and ratings on every sheet match the calculations.", 1.9, "NOTE")
    return s


# =================================================================== E-02
def e02(D):
    s = Sheet("E-02", "DC SIDE SINGLE LINE DIAGRAM", "PV strings  >  DC distribution box (DCDB)  >  inverter DC inputs", 2, TOTAL)
    ns = int(D["n_ser"])
    s.text(14, 280, f"DC SIDE  -  {int(D['n_str'])} STRINGS x {ns} MODULES  =  {f(D['kwp'], 2)} kWp", 3.6)
    strings = [(225, 1, D["L_s1"], D["vd_s1"]), (165, 2, D["L_s2"], D["vd_s2"])]
    mw, gp, x0 = 16, 3, 25
    for y0, i, L, vd in strings:
        pos, neg = y0 + 12, y0 - 12
        for k in range(ns):
            s.module(x0 + k * (mw + gp), y0 - 6, mw, 12)
            if k < ns - 1:
                s.line(x0 + k * (mw + gp) + mw, y0, x0 + (k + 1) * (mw + gp), y0, "EQUIP")
        xl, xr = x0, x0 + (ns - 1) * (mw + gp) + mw
        s.line(xl, y0, xl, neg, "DCN")
        s.line(xr, y0, xr, pos, "DCP")
        s.line(xr, pos, 171, pos, "DCP")
        s.line(xl, neg, 171, neg, "DCN")
        s.text(x0, y0 + 10, f"STRING {i}:  {ns} x {D['mod_wp']:.0f} Wp  =  {f(ns * D['mod_wp'] / 1000, 2)} kWp", 2.4)
        s.text(x0, y0 + 14.5, f"Voc(cold) {f(D['v_str_oc'], 1)} V   Isc {f(D['isc'], 2)} A", 2.0, "NOTE")
        s.text(122, pos + 3.6, f"DC-{i}: 2 x {D['dc_size']:.0f} sq.mm Cu", 2.1)
        s.text(122, neg - 3.8, f"{D['L_s1' if i == 1 else 'L_s2']:.0f} m   VD {pct(vd)} %", 2.1)
        # PE bonding of frames
        s.line(20, y0 - 8, 121, y0 - 8, "PE")
        s.text(122, y0 - 8, "PE 6 sq.mm Cu", 1.9, "NOTE")
        # MCB 2P
        s.switch(177, pos, "DCP")
        s.switch(177, neg, "DCN")
        s.line(180.5, pos + 4.5, 180.5, neg + 4.5, "BOUND")
        s.text(186, y0 + 3.5, f"Q{i}  DC MCB 2P", 2.1)
        s.text(186, y0 - 0.5, f"{D['dc_mcb']:.0f} A, {D['dc_dev_v']:.0f} V DC", 2.1)
        # conductors out
        s.line(183, pos, 300, pos, "DCP")
        s.line(183, neg, 300, neg, "DCN")
        # SPD (3-mode: +/PE and -/PE)
        s.varistor(218, pos, y0)
        s.varistor(218, y0, neg)
        s.dot(218, pos, "DCP"); s.dot(218, neg, "DCN")
        s.line(218, y0, 228, y0, "PEC")
        s.dot(228, y0, "PEC")
        s.text(232, y0 + 3.5, f"SPD-{i}  Type 2", 2.1)
        s.text(232, y0 - 0.5, f"Uc {D['dc_spd_uc']:.0f} V DC", 2.1)
        # inverter terminals
        s.dot(300, pos, "DCP"); s.dot(300, neg, "DCN")
        s.text(303, y0 + 3, f"MPPT-{i}", 2.4)
        s.text(303, y0 - 1.5, f"{f(D['imp'], 2)} A", 2.0, "NOTE")
    # frame bond vertical + earth bus
    s.line(20, 217, 20, 112, "PEC")
    s.dot(20, 157, "PEC")
    s.line(228, 225, 228, 140, "PEC")
    # DCDB enclosure
    s.rect(160, 128, 108, 124, "BOUND")
    s.text(214, 247.5, "DC DISTRIBUTION BOX (DCDB)  IP65", 2.4, "TEXT", "C")
    s.line(176, 140, 252, 140, "EQUIP")
    s.line(176, 140.8, 252, 140.8, "EQUIP")
    s.text(176, 144, "PE BAR", 1.9)
    s.line(205, 140, 205, 112, "PEC")
    s.text(270, 201, "DC-3 (each string):", 1.9)
    s.text(270, 197, "2 x {0:.0f} sq.mm Cu, {1:.0f} m".format(D["dc_size"], D["L_dd"]), 1.9)
    s.text(270, 193, f"VD {pct(D['vd_dd'])} %", 1.9)
    # inverter
    s.rect(300, 140, 60, 110, "EQUIP")
    s.line(300, 140, 360, 250, "EQUIP")
    s.line(336, 238, 346, 238, "EQUIP"); s.line(336, 235, 346, 235, "EQUIP")  # = sign
    s.text(345, 170, "~", 7, "TEXT", "C")
    s.text(330, 255, f"{f(D['inv_kw'], 0)} kW GRID-TIE STRING INVERTER", 2.6, "TEXT", "C")
    s.text(330, 135, f"1-phase 230 V | {2} MPPT | IP65", 2.0, "NOTE", "C")
    s.text(330, 131, f"MPPT {D['mppt_min']:.0f}-{D['mppt_max']:.0f} V | max {D['vdc_max']:.0f} V DC", 2.0, "NOTE", "C")
    # AC output
    s.line(360, 200, 395, 200, "ACL"); s.line(360, 190, 395, 190, "ACN")
    s.text(363, 203, "L", 2.2); s.text(363, 187, "N", 2.2)
    s.text(363, 182, "to ACDB", 2.1); s.text(363, 178, "(see E-03)", 2.1)
    s.line(345, 140, 345, 112, "PEC")
    # earth bus
    s.line(20, 112, 345, 112, "PEC")
    s.earth(110, 112, "PEC")
    s.text(118, 108.5, "EP-1: EQUIPMENT EARTH PIT, 6 sq.mm Cu (G/Y), target <= 5 ohm", 2.1)
    s.text(60, 115.5, "EARTH BUS (PE)", 1.9, "NOTE")

    # data tables
    s.text(15, 101.5, "STRING DESIGN CHECK", 2.6)
    rows = [["PARAMETER", "VALUE", "LIMIT"],
            ["Modules in series", f"{ns}", f"{D['n_min']:.0f} - {D['n_max']:.0f}"],
            [f"String Voc @ {D['tmin']:.0f} deg C", f"{f(D['v_str_oc'], 1)} V", f"<= {D['vdc_max']:.0f} V"],
            [f"String Vmp @ {D['tcell']:.0f} deg C", f"{f(D['v_str_h'], 1)} V", f">= {D['mppt_min']:.0f} V"],
            [f"String Vmp @ {D['tmin']:.0f} deg C", f"{f(D['v_str_c'], 1)} V", f"<= {D['mppt_max']:.0f} V"],
            ["Isc per MPPT", f"{f(D['isc'], 2)} A", "<= 20 A"],
            ["DC voltage drop (worst)", f"{pct(D['vd_dc'])} %", "<= 1.5 %"]]
    s.table(15, 99, [62, 34, 30], rows, row_h=5.0, h=2.2, aligns=["L", "C", "C"])
    s.text(150, 101.5, "MODULE DATA (representative)", 2.6)
    mrows = [["ITEM", "VALUE"], ["Power (STC)", f"{D['mod_wp']:.0f} Wp"], ["Voc / Vmp", f"{D['voc']} V / {D['vmp']} V"],
             ["Isc / Imp", f"{D['isc']} A / {D['imp']} A"], ["Dimensions", f"{D['mod_L'] * 1000:.0f} x {D['mod_W'] * 1000:.0f} mm"],
             ["Cell type", "Mono PERC, 144 half-cut"], ["Quantity", f"{D['n_mod']:.0f} nos"]]
    s.table(150, 99, [30, 52], mrows, row_h=5.0, h=2.2)
    s.text(240, 101.5, "LEGEND", 2.6)
    leg = [("DCP", "DC positive (+)"), ("DCN", "DC negative (-)"), ("PE", "PE conductor (dashed)")]
    for i, (ly, lab) in enumerate(leg):
        s.line(242, 94 - i * 6, 262, 94 - i * 6, ly)
        s.text(266, 94 - i * 6, lab, 2.1)
    s.switch(252, 76, "EQUIP"); s.text(266, 76, "DC MCB / isolator 2P", 2.1)
    s.varistor(252, 74 - 0, 66); s.text(266, 70, "SPD (varistor, 3-mode)", 2.1)
    s.rect(342, 90, 16, 8, "BOUND"); s.text(362, 94, "Enclosure boundary", 2.1)
    s.module(342, 76, 12, 7); s.text(362, 79.5, "PV module", 2.1)
    s.earth(348, 72, "PEC", 3); s.text(362, 68, "Earth pit", 2.1)
    s.text(342, 62, "Strings run on separate MPPT inputs, so no", 1.9, "NOTE")
    s.text(342, 58.5, "string fuses are needed (max reverse current", 1.9, "NOTE")
    s.text(342, 55, f"{f(D['isc'], 2)} A < module fuse rating).", 1.9, "NOTE")
    return s


# =================================================================== E-03
def e03(D):
    s = Sheet("E-03", "AC SIDE SINGLE LINE DIAGRAM", "Inverter  >  ACDB  >  net meter  >  main LT DB  >  grid", 3, TOTAL)
    s.text(14, 280, f"AC SIDE  -  1-PHASE {D['vac']:.0f} V, 50 Hz,  {f(D['inv_kw'], 0)} kW  ({f(D['iac_max'], 1)} A max)", 3.6)
    yL, yN, yP = 215, 205, 195
    # inverter
    s.rect(20, 180, 50, 70, "EQUIP")
    s.line(20, 180, 70, 250, "EQUIP")
    s.text(45, 255, f"{f(D['inv_kw'], 0)} kW INVERTER", 2.6, "TEXT", "C")
    s.text(45, 175, "AC OUTPUT", 2.0, "NOTE", "C")
    s.text(32, 232, "=", 6, "TEXT", "C"); s.text(58, 195, "~", 6, "TEXT", "C")
    s.text(25, 243, "(DC in: E-02)", 1.9, "NOTE")
    # lines
    s.line(70, yL, 105, yL, "ACL"); s.line(70, yN, 105, yN, "ACN"); s.line(70, yP, 105, yP, "PE")
    s.text(72, yL + 3.6, f"AC-1: 3C x {D['ac_size']:.0f} sq.mm Cu", 2.1)
    s.text(72, yL + 7.4, "ARMOURED", 1.9, "NOTE")
    s.text(72, yP - 4, f"{D['L_ia']:.0f} m  VD {pct(D['vd_ia'])} %", 2.1)
    for lab, y in (("L", yL), ("N", yN), ("PE", yP)):
        s.text(66, y + 2.2, lab, 1.8, "NOTE", "R")
    # ACDB
    s.rect(105, 150, 140, 112, "BOUND")
    s.text(175, 257, "AC DISTRIBUTION BOX (ACDB)  IP65", 2.4, "TEXT", "C")
    s.line(105, yL, 125, yL, "ACL"); s.line(105, yN, 125, yN, "ACN"); s.line(105, yP, 245, yP, "PE")
    # MCB
    s.switch(131, yL, "ACL"); s.switch(131, yN, "ACN")
    s.line(134.5, yL + 4.5, 134.5, yN + 4.5, "BOUND")
    s.text(112, yL + 11, "Q3  MCB 2P (C)", 2.1)
    s.text(112, yL + 7.4, f"{D['ac_mcb']:.0f} A", 2.1)
    s.line(137, yL, 152, yL, "ACL"); s.line(137, yN, 152, yN, "ACN")
    # RCCB with core
    s.switch(158, yL, "ACL"); s.switch(158, yN, "ACN")
    s.circle(158, (yL + yN) / 2, 8.5, "EQUIP")
    s.line(161.5, yL + 4.5, 161.5, yN + 4.5, "BOUND")
    s.text(148, yL + 11, "F1  RCCB 2P Type A", 2.1)
    s.text(148, yL + 7.4, f"{D['rccb']:.0f} A / {D['rcd_ma']:.0f} mA", 2.1)
    s.line(164, yL, 205, yL, "ACL"); s.line(164, yN, 205, yN, "ACN")
    # SPD
    s.varistor(180, yL, yP); s.varistor(190, yN, yP)
    s.dot(180, yL, "ACL"); s.dot(190, yN, "ACN"); s.dot(180, yP, "PE"); s.dot(190, yP, "PE")
    s.text(168, 232 - 24, "", 2)
    s.text(170, 178, "F2  SPD Type 2", 2.1)
    s.text(170, 174, f"Uc {D['ac_spd_uc']:.0f} V AC", 2.1)
    # isolator
    s.switch(211, yL, "ACL"); s.switch(211, yN, "ACN")
    s.line(214.5, yL + 4.5, 214.5, yN + 4.5, "BOUND")
    s.text(201, yL + 11, "Q4  AC ISOLATOR 2P", 2.1)
    s.text(201, yL + 7.4, f"{D['ac_iso']:.0f} A  lockable", 2.1)
    s.line(217, yL, 285, yL, "ACL"); s.line(217, yN, 285, yN, "ACN")
    # PE bar & earth
    s.line(150, yP - 1.2, 235, yP - 1.2, "EQUIP")
    s.text(152, yP - 5, "PE BAR", 1.9)
    s.line(215, yP, 215, 160, "PEC")
    s.earth(215, 160, "PEC")
    s.text(223, 152, "EP-2 (AC / neutral earth)", 2.0)
    s.text(223, 148, "10 sq.mm Cu, <= 5 ohm", 2.0)
    s.text(250, yP - 4, f"AC-2: 3C x {D['ac_size']:.0f} sq.mm Cu, {D['L_am']:.0f} m", 2.1)
    s.text(250, yP - 8, f"VD {pct(D['vd_am'])} %  (total {pct(D['vd_ac'])} %)", 2.1)
    s.line(245, yP, 340, yP, "PE")
    # meter
    s.meter(310, (yL + yN) / 2, 11, "kWh")
    s.line(285, yL, 299.7, yL, "ACL"); s.line(285, yN, 299.7, yN, "ACN")
    s.line(320.3, yL, 335, yL, "ACL"); s.line(320.3, yN, 335, yN, "ACN")
    s.text(310, 232, "NET METER", 2.2, "TEXT", "C")
    s.text(310, 228.5, "bi-directional", 2.0, "NOTE", "C")
    # main DB
    s.rect(335, 180, 65, 70, "EQUIP")
    s.text(367, 245, "EXISTING MAIN LT DB", 2.3, "TEXT", "C")
    s.text(367, 240, "(consumer premises)", 1.9, "NOTE", "C")
    s.line(335, yL, 345, yL, "ACL"); s.line(335, yN, 345, yN, "ACN"); s.line(335, yP, 345, yP, "PE")
    s.text(367, 224, "Main MCB / isolator", 2.0, "NOTE", "C")
    s.text(367, 207, "Bus: L - N - PE", 2.0, "NOTE", "C")
    s.text(367, 191, "N-PE link at source only", 1.9, "NOTE", "C")
    # house loads & grid
    s.line(380, 180, 380, 160, "ACL"); s.line(388, 180, 388, 160, "ACN")
    s.text(376, 170, "service", 1.9, "NOTE", "R")
    s.rect(335, 128, 65, 32, "EQUIP")
    s.text(367, 152, "DISCOM SERVICE", 2.3, "TEXT", "C")
    s.text(367, 147, "CONNECTION / GRID", 2.3, "TEXT", "C")
    s.text(367, 139, "230 V, 1-phase, 50 Hz", 2.0, "NOTE", "C")
    s.text(367, 134, "import / export", 2.0, "NOTE", "C")

    # protection schedule
    s.text(15, 120, "PROTECTION & CABLE SCHEDULE (AC SIDE)", 2.6)
    rows = [["TAG", "DEVICE / CABLE", "RATING", "BASIS"],
            ["Q3", "MCB 2P, C-curve", f"{D['ac_mcb']:.0f} A", f"1.25 x {f(D['iac_max'], 1)} A = {f(1.25 * D['iac_max'], 1)} A -> next std"],
            ["F1", "RCCB 2P, Type A", f"{D['rccb']:.0f} A / {D['rcd_ma']:.0f} mA", "1.25 x upstream MCB, one size above"],
            ["F2", "SPD Type 2 (L-PE, N-PE)", f"Uc {D['ac_spd_uc']:.0f} V", f">= 1.1 x {D['vac']:.0f} V"],
            ["Q4", "AC isolator 2P, lockable", f"{D['ac_iso']:.0f} A", "DISCOM accessible"],
            ["AC-1", f"3C x {D['ac_size']:.0f} sq.mm Cu, {D['L_ia']:.0f} m", f"Iz {f(D['iz_ac'], 1)} A", f"In {D['ac_mcb']:.0f} A <= Iz;  VD {pct(D['vd_ia'])} %"],
            ["AC-2", f"3C x {D['ac_size']:.0f} sq.mm Cu, {D['L_am']:.0f} m", f"Iz {f(D['iz_ac'], 1)} A", f"Total AC VD {pct(D['vd_ac'])} % <= 2 %"]]
    s.table(15, 118, [14, 52, 30, 84], rows, row_h=5.2, h=2.1, aligns=["L", "L", "C", "L"])
    s.text(225, 120, "NOTES", 2.6)
    nts = ["1. Cable ampacity Iz includes derating for 45 deg C ambient.",
           "2. Rule used: Ib <= In <= Iz for every protected cable.",
           "3. Inverter has built-in anti-islanding / grid protection.",
           "4. Net meter is supplied/sealed by the DISCOM.",
           "5. Single-phase connection assumed; confirm sanctioned",
           "    load and phase with the DISCOM before finalising.",
           "6. Earth pits EP-1 / EP-2 / EP-3 / EP-4 are bonded (E-05)."]
    for i, t in enumerate(nts):
        s.text(225, 113 - i * 4.8, t, 2.1)
    return s


# =================================================================== E-04
def e04(D):
    s = Sheet("E-04", "ROOF PLAN - ARRAY LAYOUT", "String routing, row spacing, equipment location", 4, TOTAL, "1:50 (plan)  1:40 (section)")
    RX, RY, K = 30, 70, 20.0          # roof origin (mm) and mm per metre
    RW, RD = 11.0, 9.0                # roof size (m)
    P = lambda x, y: (RX + x * K, RY + y * K)
    s.text(RX, 258, "ROOF PLAN  (SCALE 1:50)", 3.4)
    s.rect(*P(0, 0), RW * K, RD * K, "EQUIP")
    s.rect(*P(0.23, 0.23), (RW - 0.46) * K, (RD - 0.46) * K, "THIN")
    s.text(RX + 2, RY - 3.5, "PARAPET 230 mm", 1.8, "NOTE")
    # stair head
    sx, sy, sw, sh = 0.23, RD - 0.23 - 2.6, 2.4, 2.6
    s.rect(*P(sx, sy), sw * K, sh * K, "EQUIP")
    s.hatch_rect(*P(sx, sy), sw * K, sh * K, 4)
    s.text(*P(sx + sw / 2, sy + sh / 2), "STAIR HEAD", 2.0, "TEXT", "C")
    # tank
    tx, ty = P(RW - 1.3, RD - 1.3)
    s.circle(tx, ty, 11, "EQUIP"); s.text(tx, ty, "TANK", 2.0, "TEXT", "C")
    # array
    ax0, ay0 = 3.7, 0.23 + 1.2
    pw, pd = D["mod_W"], D["proj"]
    rows_y = [ay0, ay0 + D["pitch"]]
    for r, yy in enumerate(rows_y):
        for k in range(int(D["n_ser"])):
            s.module(*P(ax0 + k * pw, yy), pw * K, pd * K)
        s.text(*P(ax0 + D["n_ser"] * pw + 0.18, yy + pd / 2), f"S{r + 1}", 2.6)
    s.text(*P(ax0 + D["width"] / 2, ay0 + pd / 2), f"ROW 1 - STRING 1 ({int(D['n_ser'])} x {D['mod_wp']:.0f} Wp)", 2.0, "NOTE", "C") if False else None
    # equipment on stair-head east wall
    dx, dy = P(2.65, 7.75)
    s.rect(dx, dy, 8, 6, "EQUIP"); s.text(dx + 4, dy + 3, "DCDB", 1.6, "TEXT", "C")
    ix, iy = P(2.65, 7.05)
    s.rect(ix, iy, 10, 8, "EQUIP"); s.text(ix + 5, iy + 4, "INV", 1.8, "TEXT", "C")
    # routes (metres)
    r1 = [(ax0, ay0 + pd / 2), (3.55, ay0 + pd / 2), (3.55, 7.9), (3.05, 7.9)]
    r2 = [(ax0, rows_y[1] + pd / 2), (3.3, rows_y[1] + pd / 2), (3.3, 7.8), (3.05, 7.8)]
    for rt, tag in ((r1, "DC-1"), (r2, "DC-2")):
        s.poly([P(*p) for p in rt], "DCP")
    s.text(*P(3.62, 4.2), "DC-1", 1.9, "TEXT", "L", 90)
    s.text(*P(3.22, 6.4), "DC-2", 1.9, "TEXT", "R", 90)
    # air terminals
    ay_mid = ay0 + D["pitch"] / 2 + pd / 2
    for tag, xr in (("AT-1", ax0 - D["rod_off"]), ("AT-2", ax0 + D["width"] + D["rod_off"])):
        cx, cy = P(xr, ay_mid)
        s.circle(cx, cy, 2.2, "LPS"); s.line(cx - 3.2, cy, cx + 3.2, cy, "LPS"); s.line(cx, cy - 3.2, cx, cy + 3.2, "LPS")
        s.text(cx, cy + 5.2, tag, 1.9, "TEXT", "C")
    # dimensions
    s.dim(*P(0, 0), *P(RW, 0), f"{RW * 1000:.0f}", off=9, side=-1)
    s.dim(*P(0, 0), *P(0, RD), f"{RD * 1000:.0f}", off=9, side=1)
    s.dim(*P(ax0, ay0 + D["pitch"] + pd), *P(ax0 + D["width"], ay0 + D["pitch"] + pd), f"{D['width'] * 1000:.0f}", off=7, side=1)
    s.dim(*P(ax0 + D["width"] / 2, 0.23), *P(ax0 + D["width"] / 2, ay0), "1200", off=0, side=-1) if False else None
    s.text(*P(ax0 + D["width"] / 2, 0.23 + 0.6), "1200 clearance (south)", 1.9, "NOTE", "C")
    s.north(RX + RW * K - 6, RY + RD * K + 14, 6)
    s.text(RX + 85, 258, "MODULES: PORTRAIT, TILT {0:.0f} deg, FACING SOUTH (DOWN OF SHEET)".format(D["tilt"]), 1.9, "NOTE")
    s.text(RX + 85, 254.2, "ROUTES SHOWN AS ONE LINE (+ AND - CABLE PAIR)", 1.9, "NOTE")

    # ---- section A-A
    s.text(265, 262, "SECTION A-A - ROW SPACING  (SCALE 1:40)", 3.0)
    kk = 25.0
    base = 195.0
    x1 = 263.0
    pj, rs = D["proj"] * kk, D["rise"] * kk
    low = D["struct_low"] * kk
    pitch = D["pitch"] * kk
    s.line(258, base, 405, base, "EQUIP")
    s.hatch_rect(258, base - 4, 147, 4, 3)
    for off in (0, pitch):
        xa, xb = x1 + off, x1 + off + pj
        ya, yb = base + low, base + low + rs
        s.line(xa, base, xa, ya, "EQUIP"); s.line(xb, base, xb, yb, "EQUIP")
        th = 0.9
        nx_, ny_ = -math.sin(math.radians(D["tilt"])) * th, math.cos(math.radians(D["tilt"])) * th
        s.poly([(xa, ya), (xb, yb), (xb + nx_, yb + ny_), (xa + nx_, ya + ny_)], "MODULE", True)
    prof = math.degrees(math.atan(math.tan(math.radians(D["alt"])) / math.cos(math.radians(D["azi"]))))
    xt, yt = x1 + pj, base + low + rs
    s.line(xt, yt, xt + (yt - (base + low)) / math.tan(math.radians(prof)), base + low, "BOUND")
    s.text(xt + 2, yt + 6, f"SUN RAY 09:00 / 15:00, 21 DEC", 1.8, "NOTE")
    s.text(xt + 2, yt + 3, f"(profile angle {prof:.1f} deg)", 1.8, "NOTE")
    s.arc(x1, base + low, 16, 0, D["tilt"], "DIM")
    s.text(x1 + 18, base + low + 2.2, f"{D['tilt']:.0f} deg", 1.9, "DIM")
    s.dim(x1, base, x1 + pj, base, f"{D['proj'] * 1000:.0f}", off=6, side=-1)
    s.dim(x1 + pj, base, x1 + pitch, base, f"{D['gap'] * 1000:.0f}", off=6, side=-1)
    s.dim(x1, base, x1 + pitch, base, f"{D['pitch'] * 1000:.0f}  (ROW PITCH)", off=14, side=-1)
    s.dim(x1, base, x1, base + low, f"{D['struct_low'] * 1000:.0f}", off=6, side=1)
    s.dim(x1 + pitch + pj, base, x1 + pitch + pj, base + low + rs, f"{D['top_h'] * 1000:.0f}", off=4, side=-1)
    s.text(x1 + 3, base + low + rs + 12, "ROW 1 (S1)", 1.9, "NOTE")
    s.text(x1 + pitch + 3, base + low + rs + 12, "ROW 2 (S2)", 1.9, "NOTE")
    s.text(263, base - 24, "< SOUTH", 2.0, "NOTE"); s.text(405, base - 24, "NORTH >", 2.0, "NOTE", "R")

    # data table
    s.text(262, 150, "ARRAY DATA", 2.6)
    rows = [["ITEM", "VALUE"],
            ["Modules", f"{D['n_mod']:.0f} x {D['mod_wp']:.0f} Wp = {f(D['kwp'], 2)} kWp"],
            ["Strings", f"{D['n_str']:.0f} x {D['n_ser']:.0f} (one string per row)"],
            ["Tilt / azimuth", f"{D['tilt']:.0f} deg / due south"],
            ["Module area", f"{f(D['area'], 1)} m2"],
            ["Row pitch / clear gap", f"{f(D['pitch'], 2)} m / {f(D['gap'], 2)} m"],
            ["Array footprint", f"{f(D['width'], 2)} x {f(D['depth'], 2)} m"],
            ["Min. roof (1 m clearance)", f"{f(D['roof_min'], 1)} m2   (roof: 99 m2)"],
            ["Shade check", "none 09:00-15:00, 21 Dec"]]
    s.table(262, 148, [52, 90], rows, row_h=5.0, h=2.1)
    s.text(262, 98, "NOTES", 2.6)
    nts = ["1. Row gap sized for no inter-row shade 09:00-15:00 on 21 Dec.",
           "2. DCDB and inverter on stair-head east wall, under a canopy.",
           "3. Air terminals AT-1 / AT-2 at mid-depth, 1 m outside the array.",
           "4. Route lengths on E-08 include rises, slack and margin.",
           "5. Keep 1 m clear walkway around the array for maintenance."]
    for i, t in enumerate(nts):
        s.text(262, 92 - i * 4.6, t, 2.0)
    return s
