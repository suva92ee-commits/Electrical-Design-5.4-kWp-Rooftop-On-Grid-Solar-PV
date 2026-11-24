"""Reads the recalculated Excel workbook so drawings and README use the SAME numbers."""
from pathlib import Path
from openpyxl import load_workbook

XLSX = Path(__file__).resolve().parent.parent / "calculations" / "Solar_PV_Design_Calculations.xlsx"


def load():
    wb = load_workbook(XLSX, data_only=True)
    a = {}
    for row in wb["Assumptions"].iter_rows(min_row=5, values_only=True):
        if row[0] and row[1] is not None:
            a[row[0]] = row[1]
    s, c, p, g, b, pb = (wb[n] for n in ["Stringing", "Cables", "Protection", "Generation", "BOM_Cost", "Payback"])
    d = {
        # assumptions (by label)
        "site": a["Site (illustrative)"], "lat": a["Latitude"], "tilt": a["Module tilt (fixed)"],
        "tmin": a["Design minimum ambient temperature"], "tcell": a["Maximum cell temperature"],
        "vac": a["AC supply voltage (1-phase)"], "n_mod": a["Number of modules"], "mod_wp": a["Module power (STC)"],
        "voc": a["Open-circuit voltage Voc"], "vmp": a["Voltage at max power Vmp"], "isc": a["Short-circuit current Isc"],
        "imp": a["Current at max power Imp"], "mod_L": a["Module length"], "mod_W": a["Module width"],
        "inv_kw": a["Rated AC power"], "vdc_max": a["Max DC input voltage"], "mppt_min": a["MPPT range - minimum"],
        "mppt_max": a["MPPT range - maximum"], "iac_max": a["Max AC output current"],
        "n_ser": a["Modules in series per string"], "n_str": a["Number of strings"],
        "dc_size": a["DC cable size (Cu, PV cable)"], "ac_size": a["AC cable size (Cu, 3-core)"],
        "L_s1": a["Length - String 1 to DCDB (one way)"], "L_s2": a["Length - String 2 to DCDB (one way)"],
        "L_dd": a["Length - DCDB to inverter (one way)"], "L_ia": a["Length - inverter to ACDB"],
        "L_am": a["Length - ACDB to meter / main DB"], "n_pits": a["Earth pits"], "r_earth": a["Earth resistance target (each pit)"],
        "rod_h": a["Air-terminal height above roof"], "rod_off": a["Air terminal offset from array edge"],
        "bldg_h": a["Building height (roof to ground)"], "struct_low": a["Module lower-edge height above roof"],
        "rcd_ma": a["RCCB sensitivity"], "r_sph": a["Rolling-sphere radius (assumed LPL III)"],
        "dc_spd_uc": a["DC SPD (Type 2) Uc"], "ac_spd_uc": a["AC SPD (Type 2) Uc"], "dc_dev_v": a["DC MCB / isolator rated voltage"],
        "tariff": a["Grid tariff"], "subsidy": a["Capital subsidy (CFA)"],
        # stringing
        "voc_c": s["C5"].value, "vmp_h": s["C6"].value, "vmp_c": s["C7"].value,
        "n_max": s["C8"].value, "n_min": s["C9"].value, "v_str_oc": s["C13"].value, "v_str_h": s["C14"].value, "v_str_c": s["C15"].value, "v_str_n": s["C16"].value,
        "kwp": s["C20"].value, "dcac": s["C21"].value, "rise": s["C24"].value, "proj": s["C25"].value,
        "alt": s["C26"].value, "azi": s["C27"].value, "gap": s["C28"].value, "pitch": s["C29"].value,
        "width": s["C31"].value, "depth": s["C32"].value, "area": s["C33"].value, "roof_min": s["C34"].value,
        "top_h": s["C35"].value,
        # cables
        "vd_s1": c["I5"].value, "vd_s2": c["I6"].value, "vd_dd": c["I7"].value, "vd_dc": c["I8"].value,
        "vd_ia": c["I11"].value, "vd_am": c["I12"].value, "vd_ac": c["I13"].value,
        "iz_dc": c["K5"].value, "iz_ac": c["K11"].value, "ib_dc": c["F5"].value,
        # protection
        "dc_mcb": p["E6"].value, "ac_mcb": p["E8"].value, "rccb": p["E9"].value, "ac_iso": p["E11"].value,
        "rp": p["D19"].value, "rp_need": p["D20"].value,
        # generation
        "pr": g["B14"].value, "gen": g["E30"].value, "yield": g["D33"].value, "cuf": g["D34"].value,
        "psh": g["C30"].value, "credited": g["D35"].value, "load": g["G30"].value,
        # cost
        "capex": None, "perwp": None, "net": None,
    }
    for r in range(5, 40):
        v = b.cell(r, 2).value
        if v == "Total project cost":
            d["capex"] = b.cell(r, 7).value
            d["perwp"] = b.cell(r + 1, 7).value
            d["net"] = b.cell(r + 3, 7).value
    d["payback"] = pb["D7"].value
    d["irr"] = pb["H5"].value
    d["co2"] = pb["H7"].value
    d["sav1"] = pb["D6"].value
    d["bom"] = [(b.cell(r, 1).value, b.cell(r, 2).value, b.cell(r, 3).value, b.cell(r, 4).value, b.cell(r, 5).value)
                for r in range(5, 20)]
    d["months"] = [(g.cell(r, 1).value, g.cell(r, 5).value, g.cell(r, 7).value) for r in range(18, 30)]
    return d


if __name__ == "__main__":
    import pprint
    pprint.pprint(load())
