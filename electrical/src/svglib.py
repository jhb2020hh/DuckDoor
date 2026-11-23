"""Kleine SVG-Hilfsbibliothek fuer die Elektro-Zeichnungen DuckDoor (EL-01, EL-02).

Symbole vereinfacht in Anlehnung an DIN EN 60617 (IEC 60617). Massstab: 1 px = 0,25 mm (A3 quer = 1680 x 1188 px).
"""
from xml.sax.saxutils import escape

W, H = 1680, 1188
FONT = "DejaVu Sans, Arial, Helvetica, sans-serif"

CSS = """
.bg{fill:#ffffff}
.frame{fill:none;stroke:#000;stroke-width:2}
.p230{fill:none;stroke:#000;stroke-width:2.4}
.s24{fill:none;stroke:#000;stroke-width:1.6}
.sig{fill:none;stroke:#000;stroke-width:1.1}
.pe{fill:none;stroke:#1a7f37;stroke-width:2.2;stroke-dasharray:12 3 2 3}
.best{fill:none;stroke:#000;stroke-width:2.4;stroke-dasharray:7 4}
.bestbox{fill:none;stroke:#555;stroke-width:1.3;stroke-dasharray:4 4}
.loc{fill:none;stroke:#666;stroke-width:1.2;stroke-dasharray:14 5 3 5}
.mech{fill:none;stroke:#000;stroke-width:1;stroke-dasharray:4 3}
.box{fill:#ffffff;stroke:#000;stroke-width:1.4}
.boxg{fill:#f4f4f4;stroke:#000;stroke-width:1.4}
.boxa{fill:#ffffff;stroke:#000;stroke-width:2}
.term{fill:#ffffff;stroke:#000;stroke-width:1.3}
.dot{fill:#000}
.barrier{fill:none;stroke:#b00;stroke-width:1.4;stroke-dasharray:10 4 2 4}
.t{font-family:%s;fill:#000}
.b{font-weight:bold}
.red{fill:#b00000}
.grey{fill:#444}
.peT{fill:#1a7f37}
""" % FONT


class Svg:
    def __init__(self, w=W, h=H, title=""):
        self.w, self.h, self.title = w, h, title
        self.el = []

    # --- Grundelemente -------------------------------------------------
    def line(self, x1, y1, x2, y2, cls="s24"):
        self.el.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"/>')

    def pline(self, pts, cls="s24"):
        p = " ".join(f"{x},{y}" for x, y in pts)
        self.el.append(f'<polyline points="{p}" class="{cls}"/>')

    def polygon(self, pts, cls="loc"):
        p = " ".join(f"{x},{y}" for x, y in pts)
        self.el.append(f'<polygon points="{p}" class="{cls}"/>')

    def rect(self, x, y, w, h, cls="box", rx=0):
        self.el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>')

    def circle(self, cx, cy, r, cls="term"):
        self.el.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{cls}"/>')

    def dot(self, x, y, r=3.2):
        self.circle(x, y, r, "dot")

    def raw(self, s):
        self.el.append(s)

    def text(self, x, y, s, size=12, anchor="start", bold=False, cls="", rot=None):
        c = "t" + (" b" if bold else "") + (" " + cls if cls else "")
        tr = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
        self.el.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" class="{c}"{tr}>{escape(s)}</text>')

    def mtext(self, x, y, lines, size=12, lh=None, anchor="start", bold_first=False, cls=""):
        lh = lh or round(size * 1.3)
        for i, s in enumerate(lines):
            self.text(x, y + i * lh, s, size, anchor, bold=(bold_first and i == 0), cls=cls)

    # --- Symbole -------------------------------------------------------
    def tick(self, x, y, n, vertical=False, cls="s24"):
        """Mehrleiter-Kennzeichnung (Schraegstrich + Leiterzahl)."""
        if vertical:
            self.line(x - 7, y + 5, x + 7, y - 5, "sig")
            self.text(x + 9, y + 4, str(n), 11)
        else:
            self.line(x - 5, y + 7, x + 5, y - 7, "sig")
            self.text(x + 2, y - 10, str(n), 11, "middle")

    def terminal(self, x, y, r=4.2):
        self.circle(x, y, r, "term")
        self.line(x - 3, y + 3, x + 3, y - 3, "sig")  # trennbare Klemme

    def fuse_v(self, cx, y1, y2, cls="s24"):
        """Sicherung senkrecht zwischen y1 und y2 (Rechteck mit Mittellinie)."""
        h = y2 - y1
        self.rect(cx - 7, y1, 14, h, "box")
        self.line(cx, y1, cx, y2, "sig")

    def fuse_h(self, x1, x2, cy):
        self.rect(x1, cy - 7, x2 - x1, 14, "box")
        self.line(x1, cy, x2, cy, "sig")

    def switch_h(self, x, y, kind="ls", cls="p230", actuator=None):
        """Schliesser waagerecht, Laenge 70 px. kind: ls (Leistungsschalter x), trenn (Lasttrennschalter)."""
        self.line(x, y, x + 18, y, cls)
        self.line(x + 18, y, x + 52, y - 17, cls)
        self.line(x + 55, y, x + 70, y, cls)
        if kind == "ls":
            self.line(x + 51, y - 4, x + 59, y + 4, "s24")
            self.line(x + 51, y + 4, x + 59, y - 4, "s24")
        elif kind == "trenn":
            self.circle(x + 58, y, 3.2, "term")
            self.line(x + 55, y - 7, x + 55, y + 7, "s24")
        if actuator:
            self.line(x + 35, y - 9, x + 35, y - 34, "mech")
            self.rect(x + 22, y - 54, 26, 20, "box")
            self.text(x + 35, y - 39, actuator, 11, "middle")

    def handle_lock(self, x, y):
        """Handbetaetigung + abschliessbar, Bezugspunkt = Ende Wirklinie oben."""
        self.line(x - 9, y, x + 9, y, "s24")  # Handantrieb (T-Griff)
        # Vorhaengeschloss (vereinfacht)
        self.rect(x + 14, y - 6, 12, 10, "box")
        self.raw(f'<path d="M{x+16},{y-6} v-4 a4,4 0 0 1 8,0 v4" class="sig"/>')

    def nc_thermal_v(self, cx, y1):
        """Oeffner senkrecht mit Bimetall-Ausloeser, Hoehe 50 px ab y1."""
        self.line(cx, y1, cx, y1 + 12, "s24")
        self.line(cx - 2, y1 + 12, cx + 13, y1 + 40, "s24")  # Kontaktzunge
        self.line(cx, y1 + 36, cx + 14, y1 + 36, "s24")      # Gegenkontakt (Oeffner)
        self.line(cx, y1 + 36, cx, y1 + 50, "s24")
        self.line(cx + 6, y1 + 26, cx + 26, y1 + 26, "mech")
        self.raw(f'<path d="M{cx+26},{y1+20} h6 v12 h6" class="sig"/>')  # Bimetall

    def psu(self, x, y, s=80):
        """Stromversorgung AC/DC (Quadrat mit Diagonale, ~ und =)."""
        self.rect(x, y, s, s, "box")
        self.line(x, y + s, x + s, y, "sig")
        self.text(x + 18, y + 30, "~", 22, "middle")
        self.text(x + s - 20, y + s - 14, "=", 22, "middle")

    def motor(self, cx, cy, r=26, step=True):
        self.circle(cx, cy, r, "box")
        self.text(cx, cy + 3, "M", 18, "middle", bold=True)
        if step:  # Schrittmotor-Kennzeichen
            self.raw(f'<path d="M{cx-10},{cy+14} h5 v-5 h5 v5 h5 v-5 h5" class="sig"/>')

    def heater(self, cx, y1, w=44, h=34):
        self.rect(cx - w / 2, y1, w, h, "box")
        for i in (-10, 0, 10):
            self.line(cx + i, y1 + 5, cx + i, y1 + h - 5, "sig")

    def ground_pa(self, x, y):
        """Potentialausgleich (Aequipotential, IEC 60417-5021, vereinfacht)."""
        self.line(x, y, x, y + 10, "pe")
        self.raw(f'<path d="M{x-12},{y+10} L{x+12},{y+10} L{x},{y+26} Z" class="sig" style="stroke:#1a7f37;fill:none"/>')

    def antenna(self, x, y):
        self.line(x, y, x, y - 30, "s24")
        self.raw(f'<path d="M{x-12},{y-42} L{x},{y-30} L{x+12},{y-42}" class="s24"/>')
        self.line(x, y - 30, x, y - 44, "s24")

    def arrow(self, x1, y1, x2, y2, cls="sig", head=7):
        import math
        self.line(x1, y1, x2, y2, cls)
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - head * math.cos(a - 0.4), y2 - head * math.sin(a - 0.4))
        p2 = (x2 - head * math.cos(a + 0.4), y2 - head * math.sin(a + 0.4))
        self.raw(f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" class="dot"/>')

    # --- Rahmen und Schriftfeld ---------------------------------------
    def frame_and_titleblock(self, title, sub, dwg, sheet):
        self.rect(20, 20, self.w - 40, self.h - 40, "frame")
        x0, y0, w = 1040, 1008, 620
        y1 = self.h - 20
        self.rect(x0, y0, w, y1 - y0, "box")
        rows = [y0 + 26, y0 + 70, y0 + 98, y0 + 126]
        for r in rows:
            self.line(x0, r, x0 + w, r, "sig")
        self.line(x0 + 440, y0, x0 + 440, y0 + 26, "sig")
        for xx in (x0 + 210, x0 + 400):
            self.line(xx, rows[1], xx, rows[3], "sig")
        self.text(x0 + 8, y0 + 18, "Entenklappe „DuckDoor“ – Anlage =DD", 12, bold=True)
        self.text(x0 + 448, y0 + 18, "Rev. A – Entwurf", 12, bold=True, cls="red")
        self.text(x0 + 8, y0 + 46, title, 17, bold=True)
        self.text(x0 + 8, y0 + 63, sub, 11)
        self.text(x0 + 8, rows[1] + 11, "Zeichnungs-Nr.", 9, cls="grey")
        self.text(x0 + 8, rows[1] + 24, dwg, 13, bold=True)
        self.text(x0 + 218, rows[1] + 11, "Blatt", 9, cls="grey")
        self.text(x0 + 218, rows[1] + 24, sheet, 13, bold=True)
        self.text(x0 + 408, rows[1] + 11, "Datum", 9, cls="grey")
        self.text(x0 + 408, rows[1] + 24, "2026-11-23", 13, bold=True)
        self.text(x0 + 8, rows[2] + 11, "Bearbeitet", 9, cls="grey")
        self.text(x0 + 8, rows[2] + 24, "Elektro-CAD, Abwicklungsteam", 11)
        self.text(x0 + 218, rows[2] + 11, "Geprüft / Freigabe", 9, cls="grey")
        self.text(x0 + 218, rows[2] + 24, "– (offen)", 11)
        self.text(x0 + 408, rows[2] + 11, "Normen", 9, cls="grey")
        self.text(x0 + 408, rows[2] + 24, "DIN EN 60617 · DIN EN IEC 81346", 10)
        self.text(x0 + w / 2, rows[3] + 22, "Entwurf – Ausführung nur durch Elektrofachkraft", 15, "middle", bold=True, cls="red")

    def save(self, path, desc=""):
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
               f'viewBox="0 0 {self.w} {self.h}">',
               f"<title>{escape(self.title)}</title>",
               f"<desc>{escape(desc)}</desc>",
               f"<style>{CSS}</style>",
               f'<rect x="0" y="0" width="{self.w}" height="{self.h}" class="bg"/>']
        out += self.el
        out.append("</svg>")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out) + "\n")
