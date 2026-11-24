"""Generate all drawing sheets (DXF + PNG + PDF) from the Excel design data.
Run after build_excel.py + recalculation:  python scripts/make_drawings.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import design_data
from cad import render
import sheets_a
try:
    import sheets_b
except ImportError:
    sheets_b = None

ROOT = Path(__file__).resolve().parent.parent
D = design_data.load()
only = sys.argv[1:]            # e.g. E-02 E-03
fns = [sheets_a.e01, sheets_a.e02, sheets_a.e03, sheets_a.e04]
if sheets_b:
    fns += [sheets_b.e05, sheets_b.e06, sheets_b.e07, sheets_b.e08]
for fn in fns:
    sh = fn(D)
    if only and sh.no not in only:
        continue
    sh.save(ROOT / "drawings" / "dxf")
    (ROOT / "drawings" / "pdf").mkdir(parents=True, exist_ok=True)
    (ROOT / "images").mkdir(exist_ok=True)
    render(sh, ROOT / "images" / f"{sh.no}.png", ROOT / "drawings" / "pdf" / f"{sh.no}.pdf")
    print("done", sh.no)
