"""Small drafting helper on top of ezdxf: sheet frame, title block, symbols, rendering."""
import math
from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment as TA

W_A3, H_A3 = 420, 297
PROJECT = "5.4 kWp ROOFTOP ON-GRID SOLAR PV SYSTEM"
LOCATION = "Kolkata, West Bengal (illustrative residential site)"
DATE = "24-NOV-2026"
DRAWN = "S. MALLIK"

LAYERS = {
    # name: (rgb, lineweight[1/100 mm], linetype)
    "FRAME": ((0, 0, 0), 50, "Continuous"),
    "THIN": ((0, 0, 0), 18, "Continuous"),
    "EQUIP": ((0, 0, 0), 35, "Continuous"),
    "DCP": ((200, 0, 0), 40, "Continuous"),
    "DCN": ((0, 70, 200), 40, "Continuous"),
    "ACL": ((160, 90, 0), 40, "Continuous"),
    "ACN": ((0, 70, 200), 40, "Continuous"),
    "PE": ((0, 140, 0), 35, "DASHED"),
    "PEC": ((0, 140, 0), 35, "Continuous"),
    "LPS": ((170, 0, 170), 35, "Continuous"),
    "BOUND": ((90, 90, 90), 25, "DASHED"),
    "DIM": ((0, 110, 160), 18, "Continuous"),
    "TEXT": ((0, 0, 0), 18, "Continuous"),
    "NOTE": ((90, 90, 90), 18, "Continuous"),
    "HATCH": ((150, 150, 150), 13, "Continuous"),
    "MODULE": ((30, 60, 120), 30, "Continuous"),
}


class Sheet:
    def __init__(self, dwg_no, title, subtitle, sheet_no, total, scale="NTS"):
        self.doc = ezdxf.new("R2018", setup=True)
        self.doc.units = ezdxf.units.MM
        self.doc.header["$LTSCALE"] = 1.0
        for name, (rgb, lw, lt) in LAYERS.items():
            lay = self.doc.layers.add(name)
            lay.rgb = rgb
            lay.dxf.lineweight = lw
            lay.dxf.linetype = lt
        self.msp = self.doc.modelspace()
        self.no, self.title, self.sub, self.n, self.total, self.scale = dwg_no, title, subtitle, sheet_no, total, scale
        self._frame()

    # ---------------------------------------------------------------- primitives
    def _attr(self, layer):
        a = {"layer": layer}
        rgb = LAYERS[layer][0]
        if rgb != (0, 0, 0):
            a["true_color"] = ezdxf.colors.rgb2int(rgb)
        return a

    def line(self, x1, y1, x2, y2, layer="EQUIP"):
        return self.msp.add_line((x1, y1), (x2, y2), dxfattribs=self._attr(layer))

    def poly(self, pts, layer="EQUIP", close=False):
        return self.msp.add_lwpolyline(pts, close=close, dxfattribs=self._attr(layer))

    def rect(self, x, y, w, h, layer="EQUIP"):
        return self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], layer, True)

    def circle(self, x, y, r, layer="EQUIP"):
        return self.msp.add_circle((x, y), r, dxfattribs={"layer": layer})

    def arc(self, x, y, r, a0, a1, layer="EQUIP"):
        return self.msp.add_arc((x, y), r, a0, a1, dxfattribs={"layer": layer})

    def dot(self, x, y, layer="EQUIP", r=0.9):
        h = self.msp.add_hatch(dxfattribs={"layer": layer})
        h.set_solid_fill()
        h.paths.add_edge_path().add_arc((x, y), r, 0, 360)

    def text(self, x, y, s, h=2.5, layer="TEXT", align="L", rot=0, width=None):
        a = {"L": TA.MIDDLE_LEFT, "C": TA.MIDDLE_CENTER, "R": TA.MIDDLE_RIGHT,
             "TL": TA.TOP_LEFT, "TC": TA.TOP_CENTER}[align]
        t = self.msp.add_text(str(s), height=h, dxfattribs={"layer": layer, "rotation": rot})
        t.set_placement((x, y), align=a)
        return t

    def lines(self, x, y, strs, h=2.5, gap=1.6, layer="TEXT", align="L"):
        for i, s in enumerate(strs):
            self.text(x, y - i * h * gap, s, h, layer, align)

    def hatch_rect(self, x, y, w, h, spacing=3, layer="HATCH"):
        """diagonal hatch lines inside a rectangle (drawn as simple lines)"""
        k = -h
        while k < w:
            x1, y1, x2, y2 = x + k, y, x + k + h, y + h
            if x1 < x:
                y1 += x - x1; x1 = x
            if x2 > x + w:
                y2 -= x2 - (x + w); x2 = x + w
            if x2 > x1:
                self.line(x1, y1, x2, y2, layer)
            k += spacing

    def dim(self, x1, y1, x2, y2, label, off=6, h=2.3, side=1):
        """Aligned dimension drawn with simple lines + text. off = distance of dimension line."""
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        nx, ny = -uy * side, ux * side
        a = (x1 + nx * off, y1 + ny * off)
        b = (x2 + nx * off, y2 + ny * off)
        self.line(x1 + nx * 1.5, y1 + ny * 1.5, a[0] + nx * 1.5, a[1] + ny * 1.5, "DIM")
        self.line(x2 + nx * 1.5, y2 + ny * 1.5, b[0] + nx * 1.5, b[1] + ny * 1.5, "DIM")
        self.line(a[0], a[1], b[0], b[1], "DIM")
        for p in (a, b):
            self.line(p[0] - 1.2 * (ux - nx) * 0.7, p[1] - 1.2 * (uy - ny) * 0.7,
                      p[0] + 1.2 * (ux - nx) * 0.7, p[1] + 1.2 * (uy - ny) * 0.7, "DIM")
        mx, my = (a[0] + b[0]) / 2 + nx * 2.2, (a[1] + b[1]) / 2 + ny * 2.2
        ang = math.degrees(math.atan2(dy, dx))
        if ang > 90 or ang < -90:
            ang += 180
        self.text(mx, my, label, h, "DIM", "C", ang)

    # ---------------------------------------------------------------- symbols
    def earth(self, x, y, layer="PEC", size=4):
        """earth symbol, line comes in from above at (x, y)"""
        self.line(x, y, x, y - size, layer)
        for i, f in enumerate((1.0, 0.65, 0.3)):
            yy = y - size - i * 1.3
            self.line(x - size * f, yy, x + size * f, yy, layer)

    def switch(self, x, y, layer, w=12):
        """horizontal switch/breaker contact centred at x; returns (left, right) x"""
        l, r = x - w / 2, x + w / 2
        self.line(l, y, x - 3, y, layer)
        self.line(x - 3, y, x + 3.5, y + 4.5, "EQUIP")
        self.line(x + 3, y, r, y, layer)
        self.line(x + 1.2, y + 2.2, x + 5.2, y - 1.8, "EQUIP")  # cross on blade (breaker mark)
        self.line(x + 1.2, y - 1.8, x + 5.2, y + 2.2, "EQUIP")
        return l, r

    def varistor(self, x, y1, y2, layer="EQUIP"):
        """vertical varistor between y1 (top) and y2 (bottom) at x"""
        m = (y1 + y2) / 2
        self.line(x, y1, x, m + 3.5, layer)
        self.line(x, m - 3.5, x, y2, layer)
        self.rect(x - 1.8, m - 3.5, 3.6, 7, "EQUIP")
        self.line(x - 3, m - 2.5, x + 3, m + 2.5, "EQUIP")  # diagonal = non-linear

    def meter(self, x, y, r=8, label="kWh"):
        self.circle(x, y, r, "EQUIP")
        self.text(x, y + 0.5, label, 3.2, "TEXT", "C")
        self.text(x, y - 3.2, "BI-DIR", 1.8, "TEXT", "C")

    def module(self, x, y, w, h):
        self.rect(x, y, w, h, "MODULE")
        self.line(x + w * 0.15, y + h * 0.2, x + w * 0.85, y + h * 0.8, "MODULE")
        self.line(x + w * 0.15, y + h * 0.8, x + w * 0.4, y + h * 0.8, "MODULE")

    def north(self, x, y, r=7):
        self.circle(x, y, r, "THIN")
        self.poly([(x, y + r), (x - 2.4, y - r * 0.5), (x, y - r * 0.15), (x + 2.4, y - r * 0.5)], "THIN", True)
        self.text(x, y + r + 3, "N", 3, "TEXT", "C")

    # ---------------------------------------------------------------- tables
    def table(self, x, y_top, col_w, rows, row_h=5.2, h=2.2, header=True, aligns=None):
        """rows: list of lists of strings. Draws grid; returns bottom y."""
        total_w = sum(col_w)
        n = len(rows)
        for i, row in enumerate(rows):
            yy = y_top - (i + 1) * row_h
            xx = x
            for j, cell in enumerate(row):
                self.rect(xx, yy, col_w[j], row_h, "THIN")
                al = (aligns[j] if aligns else "L")
                tx = xx + 1.2 if al == "L" else (xx + col_w[j] / 2 if al == "C" else xx + col_w[j] - 1.2)
                self.text(tx, yy + row_h / 2, cell, h, "TEXT", al)
                xx += col_w[j]
            if header and i == 0:
                self.rect(x, yy, total_w, row_h, "EQUIP")
        return y_top - n * row_h

    # ---------------------------------------------------------------- frame & title block
    def _frame(self):
        self.rect(10, 10, 400, 277, "FRAME")
        self.rect(5, 5, 410, 287, "THIN")
        # title block
        self.rect(10, 10, 400, 32, "FRAME")
        self.line(120, 10, 120, 42, "EQUIP")
        self.line(270, 10, 270, 42, "EQUIP")
        self.text(14, 38, "PROJECT", 1.8, "NOTE")
        self.text(14, 31, PROJECT, 3.0, "TEXT")
        self.text(14, 25.5, LOCATION, 2.3, "TEXT")
        self.text(14, 19.5, "Designed for 230 V, 50 Hz single-phase LT supply", 2.0, "NOTE")
        self.rect(14, 12.2, 102, 4.6, "THIN")
        self.text(65, 14.5, "PORTFOLIO STUDY - NOT FOR CONSTRUCTION", 2.2, "TEXT", "C")
        self.text(124, 38, "DRAWING TITLE", 1.8, "NOTE")
        self.text(124, 30, self.title, 4.2, "TEXT")
        self.text(124, 22, self.sub, 2.4, "TEXT")
        # right grid: 3 rows (42-31, 31-20.5, 20.5-10) x 2 columns
        self.line(270, 31, 410, 31, "THIN")
        self.line(270, 20.5, 410, 20.5, "THIN")
        self.line(340, 10, 340, 42, "THIN")
        for lab, val, x, top, big in [("DWG NO.", self.no, 274, 42, 3.6), ("SHEET", f"{self.n} OF {self.total}", 344, 42, 3.6),
                                      ("SCALE", self.scale, 274, 31, 3.0), ("DATE", DATE, 344, 31, 3.0),
                                      ("DRAWN BY", DRAWN, 274, 20.5, 3.0), ("REVISION", "0 - Issued for portfolio", 344, 20.5, 2.4)]:
            self.text(x, top - 2.3, lab, 1.6, "NOTE")
            self.text(x, top - 7.2, val, big, "TEXT")

    def save(self, folder):
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        p = folder / f"{self.no}.dxf"
        self.doc.saveas(p)
        return p


def render(sheet, png_path, pdf_path=None, dpi=170):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from ezdxf.addons.drawing import Frontend, RenderContext, layout
    from ezdxf.addons.drawing.config import BackgroundPolicy, ColorPolicy, Configuration, LineweightPolicy
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

    fig = plt.figure(figsize=(W_A3 / 25.4, H_A3 / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.COLOR,
                        lineweight_policy=LineweightPolicy.ABSOLUTE, lineweight_scaling=1.0,
                        min_lineweight=0.35)
    ctx = RenderContext(sheet.doc)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out, config=cfg).draw_layout(sheet.msp, finalize=True)
    ax.set_xlim(0, W_A3)
    ax.set_ylim(0, H_A3)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.set_size_inches(W_A3 / 25.4, H_A3 / 25.4)
    fig.savefig(png_path, dpi=dpi, facecolor="white")
    if pdf_path:
        fig.savefig(pdf_path, facecolor="white")
    plt.close(fig)
