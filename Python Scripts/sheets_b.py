"""Drawing sheets E-05 .. E-08."""
import math
from cad import Sheet
from sheets_a import f, pct, TOTAL


# =================================================================== E-05
def e05(D):
    s = Sheet("E-05", "EARTHING & LIGHTNING PROTECTION", "Roof air-termination, down conductors, earth pits, bonding", 5, TOTAL, "1:75 (plans)")
    K = 1000 / 75.0
    RW, RD = 11.0, 9.0
    ax0, ay0 = 3.7, 0.23 + 1.2
    rows_y = [ay0, ay0 + D["pitch"]]
    pd, pw = D["proj"], D["mod_W"]
    # ---------------- roof plan
    RX, RY = 22, 140
    PR = lambda x, y: (RX + x * K, RY + y * K)
    s.text(RX, 277, "ROOF PLAN - LIGHTNING PROTECTION & BONDING  (1:75)", 3.0)
    s.rect(*PR(0, 0), RW * K, RD * K, "EQUIP")
    s.rect(*PR(0.23, 0.23), (RW - 0.46) * K, (RD - 0.46) * K, "THIN")
    s.rect(*PR(0.23, RD - 0.23 - 2.6), 2.4 * K, 2.6 * K, "EQUIP")
    s.hatch_rect(*PR(0.23, RD - 0.23 - 2.6), 2.4 * K, 2.6 * K, 4)
    s.text(*PR(1.4, 7.5), "STAIR HEAD", 1.8, "TEXT", "C")
    for yy in rows_y:
        for k in range(int(D["n_ser"])):
            s.rect(*PR(ax0 + k * pw, yy), pw * K, pd * K, "MODULE")
    ymid = ay0 + D["pitch"] / 2 + pd / 2
    rods = [("AT-1", ax0 - D["rod_off"]), ("AT-2", ax0 + D["width"] + D["rod_off"])]
    for tag, xr in rods:
        cx, cy = PR(xr, ymid)
        s.line(*PR(xr, ymid), *PR(ax0 + D["width"] / 2, ay0), "BOUND")
        s.circle(cx, cy, 2.0, "LPS"); s.line(cx - 3, cy, cx + 3, cy, "LPS"); s.line(cx, cy - 3, cx, cy + 3, "LPS")
        s.text(cx, cy + 5, tag, 1.9, "TEXT", "C")
    mp = PR(ax0 + D["width"] / 2, ay0)
    s.text(mp[0], mp[1] - 4, "{0} m <= {1} m (protected radius)".format(f(D["rp_need"], 2), f(D["rp"], 2)), 1.8, "NOTE", "C")
    # roof conductors to down conductors
    a1 = PR(0.23, ymid); a2 = PR(RW - 0.23, ymid)
    s.line(*PR(rods[0][1], ymid), *a1, "LPS"); s.line(*PR(rods[1][1], ymid), *a2, "LPS")
    for tag, p in (("DC-A", a1), ("DC-B", a2)):
        s.rect(p[0] - 1.5, p[1] - 1.5, 3, 3, "LPS")
    s.text(a1[0] + 3, a1[1] - 4.5, "DOWN COND. A", 1.7, "NOTE")
    s.text(a2[0] - 3, a2[1] - 4.5, "DOWN COND. B", 1.7, "NOTE", "R")
    # equipment bonding
    pe = [PR(ax0, rows_y[0] + 0.35), PR(3.3, rows_y[0] + 0.35), PR(3.3, 7.62), PR(3.05, 7.62)]
    s.poly(pe, "PE")
    s.line(*PR(ax0, rows_y[1] + 0.35), *PR(3.3, rows_y[1] + 0.35), "PE")
    s.rect(*PR(2.65, 7.75), 0.4 * K, 0.3 * K, "EQUIP")
    s.text(*PR(2.85, 8.35), "DCDB / INV", 1.7, "TEXT", "C")
    s.text(RX, RY - 8, "- - - PE 6 sq.mm Cu: module frames + structure to DCDB PE bar, then to EP-1", 1.9, "NOTE")
    s.text(RX, RY - 12.5, "- - - check line: air terminal to farthest array point (inside protected radius)", 1.9, "NOTE")
    s.north(RX + RW * K + 4, RY + RD * K + 4, 5)

    # ---------------- ground plan
    BX, BY = 205, 140
    PG = lambda x, y: (BX + x * K, BY + y * K)
    s.text(195, 277, "GROUND LEVEL PLAN - EARTH PITS & RING  (1:75)", 3.0)
    s.rect(*PG(0, 0), RW * K, RD * K, "EQUIP")
    ring0, ring1 = (BX - 10, BY - 10), (BX + RW * K + 10, BY + RD * K + 10)
    s.rect(ring0[0], ring0[1], ring1[0] - ring0[0], ring1[1] - ring0[1], "LPS")
    s.rect(*PG(0.23, RD - 0.23 - 2.6), 2.4 * K, 2.6 * K, "EQUIP"); s.hatch_rect(*PG(0.23, RD - 0.23 - 2.6), 2.4 * K, 2.6 * K, 4)
    s.text(*PG(1.4, 7.5), "STAIR HEAD", 1.7, "TEXT", "C")
    s.rect(*PG(4.2, 0.23), 2.0 * K, 1.6 * K, "EQUIP")
    s.text(*PG(5.2, 1.0), "METER ROOM", 1.7, "TEXT", "C")
    s.text(*PG(5.5, 4.5), "BUILDING FOOTPRINT", 2.2, "NOTE", "C")
    s.text(*PG(5.5, 3.8), f"{RW:.0f} x {RD:.0f} m, height {D['bldg_h']:.0f} m", 1.9, "NOTE", "C")
    pits = {"EP-1": (ring0[0], PG(0, 7.6)[1]), "EP-2": (PG(5.2, 0)[0], ring0[1]),
            "EP-3": (ring0[0], PG(0, ymid)[1]), "EP-4": (ring1[0], PG(0, ymid)[1])}
    for tag, (px, py) in pits.items():
        s.circle(px, py, 3.2, "PEC"); s.line(px - 3.2, py, px + 3.2, py, "PEC"); s.line(px, py - 3.2, px, py + 3.2, "PEC")
        dx = -4.5 if px < BX else (4.5 if px > BX + 100 else 0)
        dy = -5.2 if tag == "EP-2" else 0
        s.text(px + dx * 0 + (-5 if px < BX else (5 if px > BX + 100 else 0)), py + dy, tag, 1.9, "TEXT", "R" if px < BX else ("L" if px > BX + 100 else "C"))
    s.line(pits["EP-1"][0], pits["EP-1"][1], BX, pits["EP-1"][1], "PEC")
    s.line(pits["EP-2"][0], pits["EP-2"][1], pits["EP-2"][0], PG(0, 0.23)[1], "PEC")
    for x0, x1, y in ((ring0[0], BX, pits["EP-3"][1]), (BX + RW * K, ring1[0], pits["EP-4"][1])):
        s.line(x0, y, x1, y, "LPS")
        s.rect(BX - 1.5 if x0 == ring0[0] else BX + RW * K - 1.5, y - 1.5, 3, 3, "LPS")
    s.text(BX + 2, ring0[1] - 3.5, "25x3 GI STRIP RING", 1.8, "LPS")

    # ---------------- earth pit detail
    px0 = 26
    s.text(px0, 122, "TYPICAL EARTH PIT DETAIL (NTS)", 2.6)
    g = 108
    s.line(px0, g, px0 + 92, g, "EQUIP"); s.hatch_rect(px0, g - 3, 92, 3, 3)
    s.rect(px0 + 38, g - 14, 22, 14, "EQUIP"); s.rect(px0 + 36, g, 26, 3, "EQUIP")
    s.text(px0 + 49, g + 5.5, "COVER", 1.7, "TEXT", "C")
    s.rect(px0 + 47, 58, 4, g - 4 - 58, "EQUIP")
    s.rect(px0 + 40, 58, 18, g - 20 - 58, "HATCH"); s.hatch_rect(px0 + 40, 58, 18, g - 20 - 58, 3)
    s.line(px0 + 51, g - 8, px0 + 90, g - 8, "LPS")
    s.text(px0 + 62, g - 11, "25x3 GI STRIP", 1.7)
    s.text(px0 + 62, g - 15, "TEST LINK", 1.7)
    s.text(px0 + 62, 80, "GI PIPE 50 NB (OR COPPER-BONDED", 1.7); s.text(px0 + 62, 76.5, "ROD), 3 m, CHEMICAL BACKFILL", 1.7)
    s.dim(px0 + 34, 58, px0 + 34, g - 4, "3000", off=5, side=1)
    s.text(px0, 55, "Pits at least 3 m apart; target <= {0:.0f} ohm each (measure on site).".format(D["r_earth"]), 1.8, "NOTE")

    # ---------------- tables
    s.text(135, 122, "EARTHING & LPS SCHEDULE", 2.6)
    rows = [["PIT", "SERVES", "CONDUCTOR", "TARGET"],
            ["EP-1", "Array frames, DCDB, inverter", "6 sq.mm Cu G/Y", f"<= {D['r_earth']:.0f} ohm"],
            ["EP-2", "ACDB earth bar, AC neutral", "10 sq.mm Cu G/Y", f"<= {D['r_earth']:.0f} ohm"],
            ["EP-3", "Down conductor A (west)", "25x3 mm GI strip", f"<= {D['r_earth']:.0f} ohm"],
            ["EP-4", "Down conductor B (east)", "25x3 mm GI strip", f"<= {D['r_earth']:.0f} ohm"],
            ["RING", "Bonds EP-1 to EP-4", "25x3 mm GI strip", "-"]]
    s.table(135, 120, [14, 62, 36, 22], rows, row_h=5.0, h=2.0)
    s.text(135, 87, "ROLLING-SPHERE CHECK (indicative)", 2.6)
    rs = [["ITEM", "VALUE"],
          ["Rolling-sphere radius R", f"{D['r_sph']:.0f} m (assumed LPL III)"],
          ["Air terminal height above roof", f"{D['rod_h']:.1f} m (x2)"],
          ["Highest array point", f"{f(D['top_h'], 2)} m"],
          ["Protected radius at array top", f"{f(D['rp'], 2)} m"],
          ["Farthest array point from a rod", f"{f(D['rp_need'], 2)} m  -> covered"]]
    s.table(135, 85, [58, 76], rs, row_h=5.0, h=2.0)
    s.text(285, 122, "NOTES", 2.6)
    for i, t in enumerate(["1. LPS layout is indicative; a site risk assessment",
                           "    (IEC 62305-2) decides the real protection level.",
                           "2. All earth pits bonded by the GI strip ring",
                           "    (equipotential bonding).",
                           "3. Maintain separation distance between lightning",
                           "    conductors and DC / AC cables.",
                           "4. Inspection chamber and test link on every pit.",
                           "5. Measure pit resistance before and after",
                           "    monsoon; record in the commissioning report.",
                           "6. DC SPDs in the DCDB and AC SPD in the ACDB",
                           "    complete the surge protection scheme."]):
        s.text(285, 116 - i * 4.7, t, 2.0)
    return s


# =================================================================== E-06
def _gland(s, x, y, label, above=True):
    s.circle(x, y, 2.4, "EQUIP")
    s.text(x, y + (5 if above else -5), label, 1.7, "TEXT", "C")


def _term(s, x, y, tag, layer="EQUIP"):
    s.rect(x - 3, y - 2.5, 6, 5, layer)
    s.text(x, y, tag, 1.4, "TEXT", "C")


def _pole_box(s, x0, x1, y0, y1, tag, cols, layer_for):
    s.rect(x0, y0, x1 - x0, y1 - y0, "EQUIP")
    s.text((x0 + x1) / 2, (y0 + y1) / 2, tag, 2.4, "TEXT", "C")


def e06(D):
    s = Sheet("E-06", "DCDB & ACDB WIRING SCHEMATIC", "Internal connections, terminal numbers, wire numbers", 6, TOTAL)
    # ================= DCDB
    s.rect(20, 112, 180, 160, "BOUND")
    s.text(20, 283, "DC DISTRIBUTION BOX (DCDB)  IP65", 3.0)
    cols = {"S1+": (55, "DCP"), "S1-": (85, "DCN"), "S2+": (135, "DCP"), "S2-": (165, "DCN")}
    _gland(s, 70, 272, "GLAND IN  DC-1"); _gland(s, 150, 272, "GLAND IN  DC-2")
    for i, (k, (x, ly)) in enumerate(cols.items()):
        _term(s, x, 258, f"X1:{i + 1}")
        s.text(x, 264.5, k, 1.8, "TEXT", "C")
        s.line(x, 255.5, x, 242, ly)
        s.text(x + 1.6, 249, f"10{i + 1}", 1.5, "NOTE")
        s.line(x, 218, x, 150, ly)
        s.text(x + 1.6, 212, f"11{i + 1}", 1.5, "NOTE")
        _term(s, x, 150, f"X2:{i + 1}")
    for tag, x0, x1 in (("Q1", 40, 100), ("Q2", 120, 180)):
        s.rect(x0, 218, x1 - x0, 24, "EQUIP")
        s.text((x0 + x1) / 2, 236, tag, 2.6, "TEXT", "C")
        s.text((x0 + x1) / 2, 229, "DC MCB 2P", 1.9, "TEXT", "C")
        s.text((x0 + x1) / 2, 224, f"{D['dc_mcb']:.0f} A / {D['dc_dev_v']:.0f} V DC", 1.9, "TEXT", "C")
    for tag, c1, c2, xs in (("F1", 55, 85, 70), ("F2", 135, 165, 150)):
        yb = 205
        s.line(c1, yb, xs - 5, yb, "DCP"); s.line(c2, yb, xs + 5, yb, "DCN")
        s.dot(c1, yb, "DCP"); s.dot(c2, yb, "DCN")
        s.line(xs - 5, yb, xs - 5, 192, "DCP"); s.line(xs + 5, yb, xs + 5, 192, "DCN")
        s.rect(xs - 9, 172, 18, 20, "EQUIP")
        s.text(xs, 184, tag, 2.4, "TEXT", "C"); s.text(xs, 177, "SPD T2", 1.6, "TEXT", "C")
        s.line(xs, 172, xs, 125, "PEC")
        s.text(xs + 1.6, 160, "121" if tag == "F1" else "122", 1.5, "NOTE")
        s.dot(xs, 125, "PEC")
        s.text(xs + 1.6, 198, "SPD +", 1.4, "NOTE") if False else None
    s.text(35, 142, "to inverter MPPT-1 (DC-3)", 1.8); s.text(115, 142, "to inverter MPPT-2 (DC-3)", 1.8)
    _gland(s, 70, 112, "GLAND OUT", above=False); _gland(s, 150, 112, "GLAND OUT", above=False)
    s.line(30, 125, 190, 125, "EQUIP"); s.line(30, 125.9, 190, 125.9, "EQUIP")
    s.text(32, 129, "PE BAR", 1.8)
    s.text(24, 120, "PE from array structure (6 sq.mm Cu)", 1.7, "NOTE")
    s.text(100, 120, "PE to EP-1", 1.7, "NOTE")
    # ================= ACDB
    s.rect(215, 112, 180, 160, "BOUND")
    s.text(215, 283, "AC DISTRIBUTION BOX (ACDB)  IP65", 3.0)
    _gland(s, 295, 272, "GLAND IN  AC-1")
    xl, xn, xp = 260, 330, 375
    for x, tag, ly in ((xl, "L", "ACL"), (xn, "N", "ACN")):
        _term(s, x, 258, f"X1:{1 if tag == 'L' else 2}")
        s.text(x, 264.5, tag, 1.8, "TEXT", "C")
        s.line(x, 255.5, x, 250, ly)
        s.line(x, 232, x, 226, ly)
        s.line(x, 206, x, 160, ly)
        s.line(x, 148, x, 138.5, ly)
        _term(s, x, 136, f"X2:{1 if tag == 'L' else 2}")
    _term(s, xp, 258, "X1:3"); s.text(xp, 264.5, "PE", 1.8, "TEXT", "C")
    s.line(xp, 255.5, xp, 125, "PEC")
    s.rect(245, 232, 100, 18, "EQUIP"); s.text(295, 244, "Q3  MCB 2P", 2.4, "TEXT", "C"); s.text(295, 237, f"{D['ac_mcb']:.0f} A, C-curve", 1.9, "TEXT", "C")
    s.rect(245, 206, 100, 20, "EQUIP"); s.text(295, 220, "F1  RCCB 2P", 2.4, "TEXT", "C"); s.text(295, 213, f"{D['rccb']:.0f} A / {D['rcd_ma']:.0f} mA, Type A", 1.9, "TEXT", "C")
    # SPD between columns
    yb = 197
    s.line(xl, yb, 290, yb, "ACL"); s.line(xn, yb, 300, yb, "ACN"); s.dot(xl, yb, "ACL"); s.dot(xn, yb, "ACN")
    s.line(290, yb, 290, 190, "ACL"); s.line(300, yb, 300, 190, "ACN")
    s.rect(285, 172, 20, 18, "EQUIP"); s.text(295, 184, "F2", 2.4, "TEXT", "C"); s.text(295, 177, "SPD T2", 1.6, "TEXT", "C")
    s.line(295, 172, 295, 125, "PEC"); s.dot(295, 125, "PEC")
    # isolator as two pole boxes
    for x in (xl, xn):
        s.rect(x - 11, 148, 22, 12, "EQUIP")
    s.text(xl, 154, "Q4", 2.2, "TEXT", "C"); s.text(xn, 154, "Q4", 2.2, "TEXT", "C")
    s.text(295, 166, "", 1)
    s.text(222, 154, "AC ISOLATOR 2P", 1.5, "NOTE") if False else None
    s.text(222, 129, f"to AC-2 (meter / main DB)", 1.8)
    _gland(s, 295, 112, "GLAND OUT  AC-2", above=False)
    s.line(235, 125, 385, 125, "EQUIP"); s.line(235, 125.9, 385, 125.9, "EQUIP")
    s.text(340, 129, "PE BAR", 1.8)
    s.text(300, 120, "PE to EP-2", 1.7, "NOTE")
    s.text(222, 120, "N-PE link NOT made here", 1.7, "NOTE")
    # ================= lists
    s.text(20, 100, "DCDB COMPONENT & WIRE LIST", 2.4)
    rows = [["TAG", "ITEM", "RATING / SIZE"],
            ["Q1, Q2", "DC MCB 2P (one per string)", f"{D['dc_mcb']:.0f} A, {D['dc_dev_v']:.0f} V DC"],
            ["F1, F2", "DC SPD Type 2 (one per MPPT)", f"Uc {D['dc_spd_uc']:.0f} V DC"],
            ["X1, X2", "Feed-through terminals (4 + 4)", "6 sq.mm, 1000 V DC"],
            ["101-104", "X1 to Q1 / Q2", f"{D['dc_size']:.0f} sq.mm Cu, red (+) black (-)"],
            ["111-114", "Q1 / Q2 to X2", f"{D['dc_size']:.0f} sq.mm Cu, red (+) black (-)"],
            ["121, 122", "SPD branch + PE tap", f"{D['dc_size']:.0f} sq.mm / 6 sq.mm G/Y"]]
    s.table(20, 98, [20, 84, 76], rows, row_h=5.0, h=2.0)
    s.text(215, 100, "ACDB COMPONENT & WIRE LIST", 2.4)
    rows = [["TAG", "ITEM", "RATING / SIZE"],
            ["Q3", "MCB 2P, C-curve", f"{D['ac_mcb']:.0f} A"],
            ["F1", "RCCB 2P, Type A", f"{D['rccb']:.0f} A / {D['rcd_ma']:.0f} mA"],
            ["F2", "AC SPD Type 2 (L-PE, N-PE)", f"Uc {D['ac_spd_uc']:.0f} V AC"],
            ["Q4", "AC isolator 2P, lockable", f"{D['ac_iso']:.0f} A"],
            ["X1, X2", "Terminals L, N, PE", f"{D['ac_size']:.0f} sq.mm"],
            ["Wiring", "L brown, N blue, PE green-yellow", f"{D['ac_size']:.0f} sq.mm Cu (SPD: 6 sq.mm)"]]
    s.table(215, 98, [20, 84, 76], rows, row_h=5.0, h=2.0)
    return s


# =================================================================== E-07
def e07(D):
    s = Sheet("E-07", "EQUIPMENT MOUNTING & CABLE ROUTING", "Equipment wall elevation (1:15) and building section (NTS)", 7, TOTAL, "1:15 / NTS")
    # ---------------- elevation
    ox, oy, k = 25, 78, 1 / 15.0
    X = lambda mm: ox + mm * k
    Y = lambda mm: oy + mm * k
    s.text(ox, 266, "STAIR-HEAD EQUIPMENT WALL - ELEVATION  (SCALE 1:15)", 3.0)
    s.rect(X(0), Y(0), 3000 * k, 2700 * k, "EQUIP")
    s.hatch_rect(X(0), Y(-120), 3000 * k, 120 * k, 3)
    s.line(X(0), Y(0), X(3000), Y(0), "EQUIP")
    # canopy
    s.rect(X(0), Y(2150), 3000 * k, 60 * k, "EQUIP"); s.hatch_rect(X(0), Y(2150), 3000 * k, 60 * k, 3)
    s.text(X(1500), Y(2330), "RAIN / SUN CANOPY", 2.0, "NOTE", "C")
    eq = {"DCDB": (300, 1300, 400, 300), "INVERTER": (1000, 1250, 500, 400), "ACDB": (1800, 1300, 400, 300)}
    for name, (x, y, w, h) in eq.items():
        s.rect(X(x), Y(y), w * k, h * k, "EQUIP")
        s.text(X(x + w / 2), Y(y + h / 2), name, 2.2, "TEXT", "C")
    # conduits / cables
    s.line(X(500), Y(2700), X(500), Y(1600), "DCP"); s.line(X(560), Y(2700), X(560), Y(1600), "DCN")
    s.text(X(600), Y(2000), "DC-1 / DC-2 from array", 1.9); s.text(X(600), Y(1900), "in 25 mm HDPE conduit", 1.9)
    s.line(X(700), Y(1450), X(1000), Y(1450), "DCP"); s.text(X(850), Y(1520), "DC-3", 1.9, "TEXT", "C")
    s.line(X(1500), Y(1450), X(1800), Y(1450), "ACL"); s.text(X(1650), Y(1520), "AC-1", 1.9, "TEXT", "C")
    s.line(X(2000), Y(1300), X(2000), Y(0), "ACL"); s.line(X(2060), Y(1300), X(2060), Y(0), "ACN")
    s.text(X(2120), Y(700), "AC-2: 3C x {0:.0f} sq.mm armoured".format(D["ac_size"]), 1.9)
    s.text(X(2120), Y(600), "in 32 mm conduit to meter / main DB", 1.9)
    # earth bar
    s.rect(X(300), Y(250), 1900 * k, 60 * k, "EQUIP")
    s.text(X(300), Y(170), "PE BUSBAR (WALL MOUNTED)", 1.8)
    for xx in (500, 1250, 2000):
        s.line(X(xx), Y(1250 if xx == 1250 else 1300), X(xx), Y(310), "PE") if xx != 2000 else s.line(X(1900), Y(1300), X(1900), Y(310), "PE")
    s.line(X(300), Y(280), X(100), Y(280), "PEC")
    s.line(X(100), Y(280), X(100), Y(-100), "PEC"); s.text(X(320), Y(90), "6 sq.mm Cu to EP-1", 1.8, "NOTE")
    # dims
    s.dim(X(3000), Y(0), X(3000), Y(1300), "1300", off=6, side=-1)
    s.dim(X(300), Y(1600), X(700), Y(1600), "400", off=5, side=1)
    s.dim(X(700), Y(1300), X(1000), Y(1300), "300", off=-5, side=1)
    s.dim(X(1500), Y(1300), X(1800), Y(1300), "300", off=-5, side=1)
    s.dim(X(0), Y(0), X(0), Y(2700), "2700", off=8, side=1)
    # notes
    s.text(ox, 62, "NOTES: 1. Inverter: keep 300 mm clear each side and 500 mm below; display at eye level.", 1.9)
    s.text(ox, 58, "2. Mount equipment on the east wall under the canopy; avoid direct rain and afternoon sun.", 1.9)
    s.text(ox, 54, "3. DC and AC cables in separate conduits; label every cable at both ends.", 1.9)
    s.text(ox, 50, "4. Typical enclosure sizes shown (DCDB / ACDB 400x300 mm, inverter 500x400 mm) - check actual products.", 1.9)

    # ---------------- building section
    g = 100.0
    km = 10.0
    u = km / 8.0
    bx0, bx1 = 268, 358
    s.text(262, 277, "BUILDING SECTION - CABLE & EARTH ROUTES (NTS)", 3.0)
    s.text(262, 270, "Building height {0:.0f} m, G+2 (illustrative).".format(D["bldg_h"]), 1.9, "NOTE")
    s.line(255, g, 405, g, "EQUIP"); s.hatch_rect(255, g - 3, 150, 3, 3)
    s.rect(bx0, g, bx1 - bx0, 10 * km, "EQUIP")
    for fl in (3.3, 6.6):
        s.line(bx0, g + fl * km, bx1, g + fl * km, "THIN")
    roof = g + 10 * km
    s.rect(bx0, roof, 16 * u, 2.4 * km, "EQUIP"); s.hatch_rect(bx0, roof, 16 * u, 2.4 * km, 4)
    low, rise, pj, pit_ = D["struct_low"] * km, D["rise"] * km, D["proj"] * km, D["pitch"] * km
    ax = bx0 + 24 * u
    for off in (0, pit_):
        xa = ax + off
        s.line(xa, roof, xa, roof + low, "EQUIP"); s.line(xa + pj, roof, xa + pj, roof + low + rise, "EQUIP")
        s.line(xa, roof + low, xa + pj, roof + low + rise, "MODULE")
    for xr in (bx0 + 19 * u, bx1 - 3):
        s.line(xr, roof, xr, roof + D["rod_h"] * km, "LPS"); s.circle(xr, roof + D["rod_h"] * km, 1.0, "LPS")
    s.rect(bx0 + 16.5 * u, roof + 7 * u, 4, 4, "EQUIP"); s.rect(bx0 + 16.5 * u, roof + 12 * u, 4, 4, "EQUIP")
    s.poly([(ax + pj, roof + low + 1), (bx0 + 22 * u, roof + 1.5), (bx0 + 22 * u, roof + 9 * u), (bx0 + 20.5 * u, roof + 9 * u)], "DCP")
    s.poly([(bx0 + 16.5 * u, roof + 4 * u), (bx0 + 8 * u, roof + 4 * u), (bx0 + 8 * u, roof)], "ACL")
    s.poly([(bx0 + 8 * u, roof), (bx0 + 8 * u, g + 17), (bx0 + 14 * u, g + 17)], "ACL")
    s.rect(bx0 + 14 * u, g + 9, 14, 14, "EQUIP"); s.text(bx0 + 14 * u + 7, g + 16, "METER", 1.6, "TEXT", "C")
    s.line(bx0 - 1.5, roof, bx0 - 1.5, g - 0.5, "LPS"); s.line(bx1 + 1.5, roof, bx1 + 1.5, g - 0.5, "LPS")
    pit_depth = 3 * km
    pitx = {"EP-3": bx0 - 1.5, "EP-1": bx0 + 12 * u, "EP-2": bx0 + 45 * u, "EP-4": bx1 + 1.5}
    s.line(bx0 - 1.5, g - 5, bx1 + 1.5, g - 5, "LPS")
    for tag, x in pitx.items():
        s.rect(x - 1.2, g - pit_depth, 2.4, pit_depth - 5, "PEC")
        s.text(x, g - pit_depth - 3.5, tag, 1.7, "TEXT", "C")

    def call(n, x, y):
        s.circle(x, y, 2.6, "THIN")
        s.text(x, y, str(n), 2.0, "TEXT", "C")
    call(1, ax + pit_ / 2 + pj / 2, roof + 24); s.line(ax + pit_ / 2 + pj / 2, roof + 21.4, ax + pit_ / 2 + pj / 2, roof + low + rise + 3, "THIN")
    call(2, bx1 - 3, roof + D["rod_h"] * km + 5)
    call(3, bx0 + 8 * u, roof + 2.4 * km + 5)
    call(4, bx0 - 12, g + 50); s.line(bx0 - 9.4, g + 50, bx0 - 3, g + 50, "THIN")
    call(5, bx0 + 14 * u + 20, g + 16)
    call(6, bx1 + 12, g + 55); s.line(bx1 + 9.4, g + 55, bx1 + 2.5, g + 55, "THIN")
    call(7, bx0 + 30 * u, g - pit_depth - 10)
    key = ["1  PV array on roof (S1, S2)", "2  Air terminals AT-1 / AT-2", "3  Stair head: DCDB + inverter + ACDB",
           "4  AC-2 riser to meter room", "5  Net meter + main LT DB", "6  Down conductors A / B (25x3 GI)",
           "7  Earth pits EP-1 to EP-4 + GI ring"]
    for i, t in enumerate(key):
        col, row = divmod(i, 4)
        s.text(255 + col * 78, 62 - row * 4.6, t, 1.9)
    return s


# =================================================================== E-08
def e08(D):
    s = Sheet("E-08", "CABLE SCHEDULE & BILL OF MATERIALS", "Quantities from the Excel BOM (prices not shown)", 8, TOTAL)
    earth_wire = next(b for b in D["bom"] if b[1] == "Earth wire")[4]
    s.text(14, 280, "CABLE SCHEDULE", 3.2)
    rows = [["TAG", "FROM", "TO", "CABLE", "SIZE", "LEN (m)", "Ib (A)", "DEVICE", "VD (%)"],
            ["DC-1", "String 1 (array)", "DCDB", "1C Cu PV cable, red + black", f"{D['dc_size']:.0f} sq.mm", f"{D['L_s1']:.0f}", f(D["ib_dc"], 1), f"{D['dc_mcb']:.0f} A", pct(D["vd_s1"])],
            ["DC-2", "String 2 (array)", "DCDB", "1C Cu PV cable, red + black", f"{D['dc_size']:.0f} sq.mm", f"{D['L_s2']:.0f}", f(D["ib_dc"], 1), f"{D['dc_mcb']:.0f} A", pct(D["vd_s2"])],
            ["DC-3", "DCDB", "Inverter (per string)", "1C Cu PV cable, red + black", f"{D['dc_size']:.0f} sq.mm", f"{D['L_dd']:.0f}", f(D["ib_dc"], 1), f"{D['dc_mcb']:.0f} A", pct(D["vd_dd"])],
            ["AC-1", "Inverter", "ACDB", "3C Cu armoured (L, N, PE)", f"{D['ac_size']:.0f} sq.mm", f"{D['L_ia']:.0f}", f(D["iac_max"], 1), f"{D['ac_mcb']:.0f} A", pct(D["vd_ia"])],
            ["AC-2", "ACDB", "Net meter / main DB", "3C Cu armoured (L, N, PE)", f"{D['ac_size']:.0f} sq.mm", f"{D['L_am']:.0f}", f(D["iac_max"], 1), f"{D['ac_mcb']:.0f} A", pct(D["vd_am"])],
            ["PE-1", "Frames / DCDB / inverter", "EP-1", "1C Cu green-yellow", "6 sq.mm", f"{earth_wire:.0f} total", "-", "-", "-"],
            ["PE-2", "ACDB PE bar", "EP-2", "1C Cu green-yellow", "10 sq.mm", "as site", "-", "-", "-"],
            ["LPS", "AT-1 / AT-2", "EP-3 / EP-4", "GI strip, 25 x 3 mm", "25x3 mm", "see BOM", "-", "-", "-"]]
    s.table(14, 277, [14, 44, 40, 62, 22, 18, 14, 18, 16], rows, row_h=5.2, h=2.1, aligns=["L", "L", "L", "L", "C", "C", "C", "C", "C"])
    s.text(14, 224, "Voltage drop limits: DC 1.5 % (worst string DC-1/2 + DC-3 = {0} %), AC 2.0 % (total AC-1 + AC-2 = {1} %).".format(pct(D["vd_dc"]), pct(D["vd_ac"])), 2.0, "NOTE")

    s.text(14, 217, "BILL OF MATERIALS", 3.2)
    brow = [["#", "ITEM", "SPECIFICATION", "UNIT", "QTY"]]
    for n, item, spec, unit, qty in D["bom"]:
        brow.append([str(n), item, spec, unit, f"{qty:,.0f}"])
    s.table(14, 214, [8, 52, 148, 14, 16], brow, row_h=5.5, h=2.0, aligns=["C", "L", "L", "C", "R"])
    s.text(262, 217, "SYSTEM SUMMARY", 3.2)
    sm = [["PARAMETER", "VALUE"], ["Array", f"{f(D['kwp'], 2)} kWp"], ["Inverter", f"{f(D['inv_kw'], 0)} kW, 1-phase"],
          ["Annual generation", f"{f(D['gen'], 0)} kWh"], ["Specific yield", f"{f(D['yield'], 0)} kWh/kWp"],
          ["Performance ratio", f"{pct(D['pr'], 1)} %"], ["Module area", f"{f(D['area'], 1)} m2"],
          ["Min. roof area", f"{f(D['roof_min'], 0)} m2"]]
    s.table(262, 214, [60, 78], sm, row_h=5.5, h=2.1)
    s.text(262, 160, "NOTES", 3.0)
    for i, t in enumerate(["1. Quantities include 10 % cable wastage.",
                           "2. Cable lengths include rises, slack and margin.",
                           "3. Representative module / inverter data -",
                           "    replace with the selected datasheets.",
                           "4. Costing is in the Excel workbook (BOM_Cost),",
                           "    with illustrative rates - not shown here."]):
        s.text(262, 154 - i * 4.8, t, 2.0)
    return s
