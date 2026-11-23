"""Kleine SVG-Hilfsbibliothek fuer technische Zeichnungen (DIN EN ISO 128 / 129 / 7200 angelehnt).

Alle Koordinaten in mm (Blattkoordinaten, y nach unten). Ansichten bilden Modellkoordinaten
ueber eine Transformationsfunktion auf das Blatt ab.
"""
import math

FONT = "Arial, 'Liberation Sans', Helvetica, sans-serif"


def f(v):
    s = f"{v:.3f}".rstrip('0').rstrip('.')
    return s if s not in ('-0', '') else '0'


def esc(t):
    return (str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


class Sheet:
    def __init__(self, w, h, lw=0.5):
        self.w, self.h = w, h
        self.lw = lw            # Volllinie breit
        self.ln = lw / 2        # schmal
        self.o = []
        self.defs = []

    # ------------------------------------------------------------ Grundelemente
    def raw(self, s):
        self.o.append(s)

    def line(self, a, b, cls='w', extra=''):
        self.o.append(f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" class="{cls}" {extra}/>')

    def pl(self, pts, cls='w', close=True, fill=None, extra=''):
        tag = 'polygon' if close else 'polyline'
        st = f' style="fill:{fill}"' if fill else ''
        p = ' '.join(f'{f(x)},{f(y)}' for x, y in pts)
        self.o.append(f'<{tag} points="{p}" class="{cls}"{st} {extra}/>')

    def path(self, d, cls='w', fill=None):
        st = f' style="fill:{fill}"' if fill else ''
        self.o.append(f'<path d="{d}" class="{cls}"{st}/>')

    def circle(self, c, r, cls='w', fill=None):
        st = f' style="fill:{fill}"' if fill else ''
        self.o.append(f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}" class="{cls}"{st}/>')

    def text(self, p, t, size=3.5, anchor='start', rot=0, weight='normal', fill='#000', italic=False,
             baseline='auto'):
        tr = f' transform="rotate({f(rot)} {f(p[0])} {f(p[1])})"' if rot else ''
        it = ' font-style="italic"' if italic else ''
        bl = f' dominant-baseline="{baseline}"' if baseline != 'auto' else ''
        self.o.append(f'<text x="{f(p[0])}" y="{f(p[1])}" font-size="{f(size)}" text-anchor="{anchor}" '
                      f'font-weight="{weight}" fill="{fill}"{it}{bl}{tr}>{esc(t)}</text>')

    def mtext(self, p, lines, size=3.5, lh=1.45, anchor='start', weight='normal', fill='#000'):
        for i, t in enumerate(lines):
            self.text((p[0], p[1] + i * size * lh), t, size, anchor, weight=weight, fill=fill)

    @staticmethod
    def tw(t, size):
        """grobe Textbreite (Arial)"""
        w = 0
        for ch in str(t):
            if ch in 'il.,:;|!\'1 ()[]-':
                w += 0.33
            elif ch in 'mwMW':
                w += 0.85
            elif ch.isupper() or ch in '×±≥≤ØÄÖÜ':
                w += 0.68
            else:
                w += 0.56
        return w * size

    # ------------------------------------------------------------ Pfeile, Masse
    def arrow(self, tip, d, L=2.5, W=0.45):
        dx, dy = d
        n = math.hypot(dx, dy)
        dx, dy = dx / n, dy / n
        px, py = -dy, dx
        b = (tip[0] - dx * L, tip[1] - dy * L)
        self.pl([tip, (b[0] + px * W, b[1] + py * W), (b[0] - px * W, b[1] - py * W)], cls='af')

    def dim_h(self, p1, p2, yd, txt, size=3.5, tshift=0, gap=1.0, over=1.5, L=2.5, tside='above'):
        """Horizontalmass zwischen p1, p2 (Blattkoord.), Masslinie bei y=yd."""
        x1, x2 = sorted([p1[0], p2[0]])
        for p in (p1, p2):
            s = 1 if yd > p[1] else -1
            if abs(yd - p[1]) > gap + 0.01:
                self.line((p[0], p[1] + s * gap), (p[0], yd + s * over), 'n')
        w = x2 - x1
        tw = self.tw(txt, size)
        if w >= 2 * L + 1:
            self.line((x1, yd), (x2, yd), 'n')
            self.arrow((x1, yd), (-1, 0), L)
            self.arrow((x2, yd), (1, 0), L)
            tx = (x1 + x2) / 2 + tshift
            if tw + 2 > w and tshift == 0:
                tx = x2 + 2 + tw / 2
                self.line((x2, yd), (x2 + 3 + tw, yd), 'n')
        else:
            self.line((x1 - L - 3, yd), (x2 + L + 3, yd), 'n')
            self.arrow((x1, yd), (1, 0), L)
            self.arrow((x2, yd), (-1, 0), L)
            tx = x2 + L + 2 + tw / 2 + tshift
        ty = yd - 0.9 if tside == 'above' else yd + size + 0.6
        self.text((tx, ty), txt, size, 'middle')

    def dim_v(self, p1, p2, xd, txt, size=3.5, tshift=0, gap=1.0, over=1.5, L=2.5):
        y1, y2 = sorted([p1[1], p2[1]])
        for p in (p1, p2):
            s = 1 if xd > p[0] else -1
            if abs(xd - p[0]) > gap + 0.01:
                self.line((p[0] + s * gap, p[1]), (xd + s * over, p[1]), 'n')
        h = y2 - y1
        tw = self.tw(txt, size)
        if h >= 2 * L + 1:
            self.line((xd, y1), (xd, y2), 'n')
            self.arrow((xd, y1), (0, -1), L)
            self.arrow((xd, y2), (0, 1), L)
            ty = (y1 + y2) / 2 + tshift
            if tw + 2 > h and tshift == 0:
                ty = y1 - 2 - tw / 2
                self.line((xd, y1), (xd, y1 - 3 - tw), 'n')
        else:
            self.line((xd, y1 - L - 3), (xd, y2 + L + 3), 'n')
            self.arrow((xd, y1), (0, 1), L)
            self.arrow((xd, y2), (0, -1), L)
            ty = y1 - L - 2 - tw / 2 + tshift
        self.text((xd - 0.9, ty), txt, size, 'middle', rot=-90)

    def koten(self, xd, pts, side='left', size=3.5, minsp=None, origin=None, L=2.2, xobj=None):
        """Steigende Bemassung (Hoehenkoten) entlang senkrechter Linie bei xd.
        pts: Liste (y_blatt, text, x_objekt). origin: y des Ursprungs (Kreis)."""
        minsp = minsp or size * 1.25
        ys = [p[0] for p in pts]
        top, bot = min(ys + [origin or ys[0]]), max(ys + [origin or ys[0]])
        self.line((xd, top), (xd, bot), 'n')
        if origin is not None:
            self.circle((xd, origin), 0.9, 'n', fill='#fff')
        # Hilfslinien + Pfeile
        for y, t, xo in pts:
            if xo is not None:
                s = 1 if xd > xo else -1
                self.line((xo + s * 1.0, y), (xd + s * 1.5, y), 'n')
            if origin is not None and abs(y - origin) > 0.01:
                self.arrow((xd, y), (0, -1 if y < origin else 1), L, 0.4)
        # Texte verteilen (sortiert von unten nach oben)
        order = sorted(pts, key=lambda p: -p[0])
        placed = []
        last = None
        for y, t, xo in order:
            ty = y + size * 0.35
            if last is not None and ty > last - minsp:
                ty = last - minsp
            placed.append((y, ty, t))
            last = ty
        # zweiter Durchgang: nach unten verschieben, falls nach oben weggelaufen (nicht noetig)
        tx = xd - 3.2 if side == 'left' else xd + 3.2
        an = 'end' if side == 'left' else 'start'
        for y, ty, t in placed:
            yy = ty - size * 0.35
            k = xd - 1.2 if side == 'left' else xd + 1.2
            if abs(yy - y) > 0.3:
                self.line((xd, y), (k, y), 'n')
                self.line((k, y), (tx + (0.4 if side == 'left' else -0.4), yy), 'n')
            else:
                self.line((xd, y), (tx + (0.4 if side == 'left' else -0.4), y), 'n')
            self.text((tx, ty), t, size, an)

    # ------------------------------------------------------------ Positionsnummern
    def balloon(self, c, num, target, r=3.8, size=3.5, dot=True):
        cx, cy = c
        self.circle(c, r, 'n', fill='#fff')
        self.text((cx, cy + size * 0.36), str(num), size, 'middle', weight='bold')
        if target is not None:
            dx, dy = target[0] - cx, target[1] - cy
            n = math.hypot(dx, dy)
            if n > r + 0.5:
                s = (cx + dx / n * r, cy + dy / n * r)
                self.line(s, target, 'n')
                if dot:
                    self.circle(target, 0.55, 'af')
                else:
                    self.arrow(target, (dx, dy), 2.2, 0.4)

    def leader_text(self, target, p, lines, size=3.5, side='right', dot=False, arrow=True):
        """Hinweislinie mit Text, Knick bei p."""
        if arrow:
            self.arrow(target, (target[0] - p[0], target[1] - p[1]), 2.2, 0.4)
        elif dot:
            self.circle(target, 0.55, 'af')
        self.line(target, p, 'n')
        wmax = max(self.tw(t, size) for t in lines)
        if side == 'right':
            self.line(p, (p[0] + wmax + 1, p[1]), 'n')
            for i, t in enumerate(lines):
                self.text((p[0] + 0.5, p[1] - 0.9 + i * size * 1.35), t, size, 'start')
        else:
            self.line(p, (p[0] - wmax - 1, p[1]), 'n')
            for i, t in enumerate(lines):
                self.text((p[0] - 0.5, p[1] - 0.9 + i * size * 1.35), t, size, 'end')

    # ------------------------------------------------------------ Sonderzeichen
    def cutmark(self, a, b, label, arrow_dir, size=7, L=8):
        """Schnittverlauf: breite Strichpunkt-Enden + Pfeile (Blickrichtung) + Buchstabe."""
        ax, ay = a
        bx, by = b
        dx, dy = bx - ax, by - ay
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        for p, s in ((a, 1), (b, -1)):
            q = (p[0] + ux * s * L, p[1] + uy * s * L)
            self.line(p, q, 'cut')
            # Pfeil senkrecht
            tail = (p[0] + ux * s * 2.5, p[1] + uy * s * 2.5)
            tip = (tail[0] + arrow_dir[0] * 7, tail[1] + arrow_dir[1] * 7)
            self.line(tail, tip, 'n')
            self.arrow(tip, arrow_dir, 3.0, 0.6)
            tp = (tip[0] + arrow_dir[0] * 2 - ux * s * 3.5, tip[1] + arrow_dir[1] * 2 - uy * s * 3.5 + size * 0.35)
            self.text(tp, label, size, 'middle', weight='bold')

    def breakline_v(self, x, y1, y2, amp=1.5):
        """Freihand-Bruchlinie (schmal) senkrecht"""
        n = max(3, int(abs(y2 - y1) / 4))
        pts = []
        for i in range(n + 1):
            y = y1 + (y2 - y1) * i / n
            xx = x + (amp if i % 2 else -amp) * (0 if i in (0, n) else 1) * 0.6
            pts.append((xx, y))
        self.pl(pts, 'n', close=False)

    def breakline_h(self, y, x1, x2, amp=1.5):
        n = max(3, int(abs(x2 - x1) / 4))
        d = f'M{f(x1)},{f(y)} '
        for i in range(n):
            xa = x1 + (x2 - x1) * (i + 0.5) / n
            xb = x1 + (x2 - x1) * (i + 1) / n
            d += f'Q{f(xa)},{f(y + (amp if i % 2 else -amp))} {f(xb)},{f(y)} '
        self.path(d, 'n')

    def zigzag_h(self, y, x1, x2, h=3):
        xm = (x1 + x2) / 2
        self.pl([(x1, y), (xm - 1.5, y), (xm - 0.5, y - h), (xm + 0.5, y + h), (xm + 1.5, y), (x2, y)], 'n',
                close=False)

    def zigzag_v(self, x, y1, y2, h=3):
        ym = (y1 + y2) / 2
        self.pl([(x, y1), (x, ym - 1.5), (x - h, ym - 0.5), (x + h, ym + 0.5), (x, ym + 1.5), (x, y2)], 'n',
                close=False)

    def proj_symbol(self, x, y, s=1.0):
        """Projektionsmethode 1 (ISO 5456-2), Kegelstumpf, Mittelpunkt links unten (x,y)."""
        # Methode 1: Kegelstumpf links (schmales Ende links), Kreise rechts
        cy = y
        tx = x + 2 * s
        self.pl([(tx, cy - 1.5 * s), (tx + 8 * s, cy - 3 * s), (tx + 8 * s, cy + 3 * s), (tx, cy + 1.5 * s)], 'n')
        cx = x + 16 * s
        self.circle((cx, cy), 3 * s, 'n')
        self.circle((cx, cy), 1.5 * s, 'n')
        self.line((x, cy), (cx + 4.5 * s, cy), 'c')

    def ground(self, x1, x2, y, depth=2.2, cls='n'):
        """Gelaendelinie mit kurzer Erdreich-Schraffur darunter"""
        self.line((x1, y), (x2, y), 'w')
        k = x1
        while k < x2 - 2.5:
            self.line((k + 0.5, y + depth), (k + 2.5, y + 0.2), 'n')
            k += 3.0

    # ------------------------------------------------------------ Ausgabe
    def svg(self, title, desc=''):
        lw, ln = self.lw, self.ln
        css = f"""
  .w{{stroke:#000;stroke-width:{lw};fill:none;stroke-linecap:round;stroke-linejoin:round}}
  .n{{stroke:#000;stroke-width:{ln};fill:none;stroke-linecap:round;stroke-linejoin:round}}
  .h{{stroke:#000;stroke-width:{ln};fill:none;stroke-dasharray:{f(12*ln)} {f(3*ln)}}}
  .c{{stroke:#000;stroke-width:{ln};fill:none;stroke-dasharray:{f(24*ln)} {f(3*ln)} {f(0.6*ln)} {f(3*ln)}}}
  .p{{stroke:#000;stroke-width:{ln};fill:none;stroke-dasharray:{f(24*ln)} {f(3*ln)} {f(0.6*ln)} {f(3*ln)} {f(0.6*ln)} {f(3*ln)}}}
  .cut{{stroke:#000;stroke-width:{lw*1.4};fill:none}}
  .cw{{stroke:#000;stroke-width:{lw};fill:none;stroke-dasharray:{f(24*ln)} {f(3*ln)} {f(0.6*ln)} {f(3*ln)}}}
  .af{{fill:#000;stroke:none}}
  .fr{{stroke:#000;stroke-width:{lw*1.4};fill:none}}
  .red{{stroke:#c00000;stroke-width:{lw};fill:none}}
  text{{font-family:{FONT};fill:#000}}
"""
        pat = f"""
  <pattern id="hA" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.6" stroke="#000" stroke-width="{ln*0.8}"/></pattern>
  <pattern id="hB" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="1.6" stroke="#000" stroke-width="{ln*0.8}"/></pattern>
  <pattern id="hA2" patternUnits="userSpaceOnUse" width="2.5" height="2.5" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="2.5" stroke="#000" stroke-width="{ln*0.8}"/></pattern>
  <pattern id="hB2" patternUnits="userSpaceOnUse" width="2.5" height="2.5" patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="2.5" stroke="#000" stroke-width="{ln*0.8}"/></pattern>
  <pattern id="hK" patternUnits="userSpaceOnUse" width="2.2" height="2.2" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="2.2" stroke="#000" stroke-width="{ln*0.7}"/><line x1="0" y1="1.1" x2="2.2" y2="1.1" stroke="#000" stroke-width="{ln*0.7}"/></pattern>
  <pattern id="hBeton" patternUnits="userSpaceOnUse" width="7" height="7"><line x1="0" y1="7" x2="7" y2="0" stroke="#000" stroke-width="{ln*0.7}"/><circle cx="1.6" cy="1.8" r="0.35" fill="#000"/><circle cx="5" cy="4.6" r="0.5" fill="none" stroke="#000" stroke-width="{ln*0.6}"/><circle cx="4.3" cy="1.2" r="0.25" fill="#000"/></pattern>
  <pattern id="hGummi" patternUnits="userSpaceOnUse" width="1.2" height="1.2"><rect width="1.2" height="1.2" fill="#000" fill-opacity="0.55"/></pattern>
"""
        body = '\n'.join(self.o)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">
<title>{esc(title)}</title>
<desc>{esc(desc)}</desc>
<defs>
<style>{css}</style>{pat}
</defs>
<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="#ffffff"/>
{body}
</svg>
"""


# ---------------------------------------------------------------- Rahmen + Schriftfeld
def frame_and_title(sh, fields, fmt='A1'):
    W, H = sh.w, sh.h
    # Rahmen: links 20 (Heftrand), sonst 10
    sh.pl([(20, 10), (W - 10, 10), (W - 10, H - 10), (20, H - 10)], 'fr')
    # Zentriermarken
    for p, q in (((W / 2, 0), (W / 2, 10)), ((W / 2, H - 10), (W / 2, H)), ((0, H / 2), (20, H / 2)),
                 ((W - 10, H / 2), (W, H / 2))):
        sh.line(p, q, 'w')
    # Feldeinteilung am Rand (Zahlen/Buchstaben)
    nx = 8 if fmt == 'A1' else 6
    ny = 6 if fmt == 'A1' else 4
    for i in range(nx + 1):
        x = 20 + (W - 30) * i / nx
        sh.line((x, 10), (x, 5), 'n')
        sh.line((x, H - 10), (x, H - 5), 'n')
    for i in range(nx):
        x = 20 + (W - 30) * (i + 0.5) / nx
        sh.text((x, 8.6), str(i + 1), 3.5, 'middle')
        sh.text((x, H - 5.9), str(i + 1), 3.5, 'middle')
    letters = 'ABCDEFGH'
    for j in range(ny + 1):
        y = 10 + (H - 20) * j / ny
        sh.line((20, y), (15, y), 'n')
        sh.line((W - 10, y), (W - 5, y), 'n')
    for j in range(ny):
        y = 10 + (H - 20) * (j + 0.5) / ny
        sh.text((17.5, y + 1.2), letters[j], 3.5, 'middle')
        sh.text((W - 7.5, y + 1.2), letters[j], 3.5, 'middle')

    # Schriftfeld nach Art DIN EN ISO 7200, Breite 180
    x0, x1 = W - 10 - 180, W - 10
    y1 = H - 10
    rows = [8, 8, 8, 13, 9, 8]  # von oben nach unten
    hT = sum(rows)
    y0 = y1 - hT
    sh.pl([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 'w', fill='#fff')
    ys = [y0]
    for r in rows:
        ys.append(ys[-1] + r)
    for y in ys[1:-1]:
        sh.line((x0, y), (x1, y), 'n')

    def cell(xa, xb, ya, yb, label, val, vsize=3.5, bold=False, vfill='#000'):
        sh.line((xa, ya), (xa, yb), 'n')
        sh.text((xa + 1, ya + 2.6), label, 2.0)
        sh.text((xa + 1.2, yb - 1.4), val, vsize, weight='bold' if bold else 'normal', fill=vfill)

    F = fields
    # Zeile 1: Verantw. Abt. | Techn. Referenz | Dokumentenart | Dokumentenstatus
    r = 0
    cell(x0, x0 + 40, ys[r], ys[r + 1], 'Verantwortl. Abteilung', F['abt'], 3.0)
    cell(x0 + 40, x0 + 90, ys[r], ys[r + 1], 'Technische Referenz', F['ref'], 3.0)
    cell(x0 + 90, x0 + 130, ys[r], ys[r + 1], 'Dokumentenart', F['art'], 3.0)
    cell(x0 + 130, x1, ys[r], ys[r + 1], 'Dokumentenstatus', F['status'], 3.0, True, '#c00000')
    r = 1
    cell(x0, x0 + 40, ys[r], ys[r + 1], 'Erstellt durch', F['ersteller'], 3.0)
    cell(x0 + 40, x0 + 90, ys[r], ys[r + 1], 'Genehmigt von', F['genehmigt'], 3.0)
    cell(x0 + 90, x0 + 130, ys[r], ys[r + 1], 'Maßstab', F['massstab'], 3.0, True)
    cell(x0 + 130, x1, ys[r], ys[r + 1], 'Allgemeintoleranz / Maßeinheit', F['tol'], 3.0)
    r = 2
    cell(x0, x0 + 40, ys[r], ys[r + 1], 'Projektionsmethode', '', 3.0)
    sh.proj_symbol(x0 + 10, ys[r] + 5.0, 0.42)
    cell(x0 + 40, x0 + 90, ys[r], ys[r + 1], 'Format / Blatt', F['format'], 3.0)
    cell(x0 + 90, x0 + 130, ys[r], ys[r + 1], 'Werkstoff / Halbzeug', 'siehe Positionsliste', 3.0)
    cell(x0 + 130, x1, ys[r], ys[r + 1], 'Oberfläche / Kanten', F['kanten'], 3.0)
    r = 3
    sh.text((x0 + 1, ys[r] + 2.6), 'Titel, zusätzlicher Titel', 2.0)
    sh.text((x0 + 2, ys[r] + 7.4), F['titel'], 5.0, weight='bold')
    sh.text((x0 + 2, ys[r] + 11.6), F['ztitel'], 3.5)
    sh.line((x0 + 130, ys[r]), (x0 + 130, ys[r + 2]), 'n')
    sh.text((x0 + 131, ys[r] + 2.6), 'Eigentümer / Projekt', 2.0)
    sh.text((x0 + 132, ys[r] + 7.4), F['projekt'], 3.5, weight='bold')
    sh.text((x0 + 132, ys[r] + 11.6), F['projekt2'], 3.0)
    r = 4
    cell(x0, x0 + 70, ys[r], ys[r + 1], 'Sachnummer / Zeichnungsnummer', F['nr'], 5.0, True)
    cell(x0 + 70, x0 + 100, ys[r], ys[r + 1], 'Änd.-Index', F['rev'], 3.5, True)
    cell(x0 + 100, x0 + 130, ys[r], ys[r + 1], 'Ausgabedatum', F['datum'], 3.5)
    r = 5
    sh.line((x0 + 130, ys[r]), (x0 + 130, ys[r + 1]), 'n')
    sh.text((x0 + 2, ys[r] + 5.6), F['stempel'], 4.2, weight='bold', fill='#c00000')
    cell(x0 + 130, x0 + 155, ys[r], ys[r + 1], 'Sprache', 'de', 3.5)
    cell(x0 + 155, x1, ys[r], ys[r + 1], 'Blatt', F['blatt'], 3.5)
    # Aenderungstabelle ueber dem Schriftfeld
    ya = y0 - 12
    sh.pl([(x0, ya), (x1, ya), (x1, y0), (x0, y0)], 'n', fill='#fff')
    sh.line((x0, ya + 5), (x1, ya + 5), 'n')
    for xx in (x0 + 12, x0 + 40, x0 + 150):
        sh.line((xx, ya), (xx, y0), 'n')
    sh.text((x0 + 1, ya + 3.6), 'Index', 2.5)
    sh.text((x0 + 13, ya + 3.6), 'Datum', 2.5)
    sh.text((x0 + 41, ya + 3.6), 'Änderung', 2.5)
    sh.text((x0 + 151, ya + 3.6), 'Name', 2.5)
    sh.text((x0 + 2, ya + 10.2), 'A', 3.0, weight='bold')
    sh.text((x0 + 13, ya + 10.2), F['datum'], 3.0)
    sh.text((x0 + 41, ya + 10.2), 'Erstausgabe Entwurf auf Basis Freigabestand v2', 3.0)
    sh.text((x0 + 151, ya + 10.2), 'TZ', 3.0)
    return (x0, ya)
