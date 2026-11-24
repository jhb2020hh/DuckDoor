"""Integration DuckDoor: Baugruppe, Exporte, Teileliste, Kollisionsprüfung, Vorschau.

Aufruf (aus dem Repo-Wurzelverzeichnis):
    /home/user/cadenv/bin/python cad/src/build_assembly.py [--no-preview] [--no-sweep]

Erzeugt unter cad/:
    DuckDoor_Baugruppe.step   STEP AP214, Baugruppe mit Unterbaugruppen nach Part.group
    DuckDoor_Baugruppe.glb    glTF-Binärvorschau
    parts/<Name>.step         Einzelteile (je ein benanntes Teil)
    Teileliste_CAD.csv        Teileliste (; getrennt, Dezimalkomma)
    Kollisionsprotokoll.txt   Kollisionsprüfung ZU_VERRIEGELT / AUF / Hubweg
    preview/*.svg, *.png      Vorschaubilder (PNG über Playwright/Chromium, falls verfügbar)
"""
import math
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cadquery as cq  # noqa: E402
from cadquery.occ_impl.exporters.assembly import exportAssembly, exportGLTF  # noqa: E402
from OCP.IFSelect import IFSelect_RetDone  # noqa: E402
from OCP.Interface import Interface_Static  # noqa: E402
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB  # noqa: E402
from OCP.STEPCAFControl import STEPCAFControl_Reader, STEPCAFControl_Writer  # noqa: E402
from OCP.STEPControl import STEPControl_AsIs  # noqa: E402
from OCP.TCollection import TCollection_ExtendedString  # noqa: E402
from OCP.TDataStd import TDataStd_Name  # noqa: E402
from OCP.TDF import TDF_LabelSequence  # noqa: E402
from OCP.TDocStd import TDocStd_Document  # noqa: E402
from OCP.XCAFApp import XCAFApp_Application  # noqa: E402
from OCP.XCAFDoc import XCAFDoc_ColorSurf, XCAFDoc_DocumentTool  # noqa: E402

import parts_antrieb  # noqa: E402
import parts_gestell  # noqa: E402

CAD = os.path.dirname(HERE)
PARTS_DIR = os.path.join(CAD, "parts")
PREV_DIR = os.path.join(CAD, "preview")
STEP_ASSY = os.path.join(CAD, "DuckDoor_Baugruppe.step")
GLB = os.path.join(CAD, "DuckDoor_Baugruppe.glb")
CSV = os.path.join(CAD, "Teileliste_CAD.csv")
KOLL = os.path.join(CAD, "Kollisionsprotokoll.txt")

GROUP_ORDER = ["GRUENDUNG", "GESTELL", "FUEHRUNG", "SCHIEBER", "ANTRIEB", "KASTEN", "ELEKTRO", "KAUFTEIL"]
V_TOL = 1.0      # mm³ – Schnittvolumen darüber = Kollision

# Hub ZU_VERRIEGELT -> AUF (TZ-01): Schieber +550, Mutterblock/Bolzen +601 (Langloch-Freiweg 52 − 1)
HUB_SCHIEBER = 550.0
HUB_BLOCK = 601.0


# ====================================================================== Teile laden
def load_parts():
    parts = parts_gestell.build() + parts_antrieb.build()
    names = [p.name for p in parts]
    dup = {n for n in names if names.count(n) > 1}
    if dup:
        raise SystemExit(f"Doppelte Bauteilnamen: {sorted(dup)}")
    solids = {}
    for p in parts:
        s = p.shape.combine().val() if len(p.shape.vals()) > 1 else p.shape.val()
        if not s.isValid():
            print(f"WARNUNG: ungültige Geometrie {p.name}")
        solids[p.name] = s
    return parts, solids


def hub_of(p):
    """Hub einer Komponente beim Fahren nach AUF (Zuordnung aus parts_antrieb.py).

    Am Schieber 13 befestigt: 14 Schaltleiste, 15 Lasche, 16 Schrauben, 47 Magnet (auf Lasche).
    Mit der Spindelmutter bewegt: 17 Bolzen (in Block 18 geschraubt), 18, 19, 42 Kulisse (am Block),
    47 Reedkontakt (am Block). Klinke 39/Achse 40/Halter 41 sitzen auf Traverse 31 -> fest.
    """
    pre = p.name.split("_")[0]
    if pre in ("P13", "P14", "P15", "P16") or p.name == "P47_Schlaffschalter_B8_Magnet":
        return HUB_SCHIEBER
    if pre in ("P17", "P18", "P19", "P42") or p.name == "P47_Schlaffschalter_B8_Reed":
        return HUB_BLOCK
    return 0.0


# ====================================================================== Kollisionsprüfung
def _bb_overlap(a, b, m=0.0):
    return not (a.xmin > b.xmax + m or b.xmin > a.xmax + m or a.ymin > b.ymax + m or
                b.ymin > a.ymax + m or a.zmin > b.zmax + m or b.zmin > a.zmax + m)


def collide(items_a, items_b=None):
    """Paarweise Schnittvolumen; items = [(name, solid)]. Ohne items_b: alle Paare in items_a."""
    out, n_pairs = [], 0
    same = items_b is None
    items_b = items_a if same else items_b
    bbs_a = [s.BoundingBox() for _, s in items_a]
    bbs_b = bbs_a if same else [s.BoundingBox() for _, s in items_b]
    for i, (na, sa) in enumerate(items_a):
        for j, (nb, sb) in enumerate(items_b):
            if same and j <= i:
                continue
            n_pairs += 1
            if not _bb_overlap(bbs_a[i], bbs_b[j]):
                continue
            v = sa.intersect(sb).Volume()
            if v > V_TOL:
                out.append((na, nb, v))
    return out, n_pairs


def sweep_check(parts, solids, steps=100):
    """Hubweg ZU->AUF in `steps` Schritten: bewegte gegen feste Teile (Klinke ohne Drehung)."""
    mov = [(p.name, solids[p.name], hub_of(p)) for p in parts if hub_of(p)]
    fix = [(p.name, solids[p.name]) for p in parts if not hub_of(p)]
    fbb = [s.BoundingBox() for _, s in fix]
    res = {}
    for na, sa, h in mov:
        for k in range(steps + 1):
            dz = h * k / steps
            t = sa.translate(cq.Vector(0, 0, dz))
            bt = t.BoundingBox()
            for (nb, sb), bb in zip(fix, fbb):
                if not _bb_overlap(bt, bb):
                    continue
                v = t.intersect(sb).Volume()
                if v > V_TOL:
                    r = res.setdefault((na, nb), [dz, dz, 0.0])
                    r[1] = dz
                    r[2] = max(r[2], v)
    return res


SWEEP_BEWERTUNG = {
    ("P15_Mitnehmerlasche", "P39_Schwerkraftklinke"):
        "funktional: Klinkenzahn liegt in der Rastkerbe der Lasche; vor dem Hub schwenkt die Kulisse 42 "
        "die Klinke aus (Drehung um x −22/z +670 hier nicht simuliert) – keine Kollision im Betrieb.",
    ("P16_Senkschraube_2", "P39_Schwerkraftklinke"):
        "funktional wie oben (Schraubenkopf/-mutter x −12 passiert die ausgeschwenkte Klinke).",
    ("P42_Entriegelungskulisse", "P39_Schwerkraftklinke"):
        "beabsichtigt: Kulissenschräge drückt den Klinken-Lug (y +16…+20) und hebt die Klinke aus.",
    ("P14_Schaltleiste_B7", "P32_Abstreiflippe"):
        "OFFEN: Schaltleiste (y ±6) streift beim Einfahren in den Kanal (Hub ≈ 500…528) die "
        "Abstreiflippe (y +2…+8, z +530…+538) – Überdeckung 4 mm, EPDM gegen EPDM; Risiko "
        "Fehlauslösung B7 / Verschleiß. Vorschlag: Lippe in diesem Bereich ausklinken oder "
        "Schaltleiste-Freigabe B7 oberhalb z ≈ +500 per Software maskieren (Team Mechanik/EL entscheiden).",
}


# ====================================================================== Teileliste / Masse
def density(p):
    """Dichte g/cm³ aus Materialtext (Kaufteile -> None)."""
    if p.kaufteil:
        return None
    m = p.material.lower()
    if "beton" in m:
        return 2.40
    if "pe-uhmw" in m:
        return 0.94
    if "epdm" in m:
        return 1.20
    if any(k in m for k in ("1.4404", "1.4301", "a4", "edelstahl")):
        return 7.95
    if any(k in m for k in ("s235", "fvz", "stahl")):
        return 7.85
    if any(k in m for k in ("en aw", "al ", "al/", "alu")) or m.startswith("al"):
        return 2.70
    return 1.00   # [A] sonstige Kunststoffe


def fmt(x, nd=3):
    return f"{x:.{nd}f}".replace(".", ",")


def write_csv(parts, solids):
    rows, total, total_kauf_vol = [], 0.0, 0.0
    for p in parts:
        s = solids[p.name]
        vol = s.Volume() / 1000.0          # cm³
        rho = density(p)
        if rho is None:
            masse = "–"
            total_kauf_vol += vol
        else:
            mk = vol * rho / 1000.0
            total += mk
            masse = fmt(mk)
        b = s.BoundingBox()
        bbox = (f"x {b.xmin:.1f}…{b.xmax:.1f} / y {b.ymin:.1f}…{b.ymax:.1f} / "
                f"z {b.zmin:.1f}…{b.zmax:.1f}")
        note = p.note
        if rho is not None and p.pos in ("2", "4"):
            note += " – Masse als Vollblech berechnet (real Gitter/Lochblech deutlich leichter)."
        if rho == 1.0:
            note += " – [A] Dichte 1,0 angesetzt."
        rows.append([p.name, p.pos, p.group, p.material, "ja" if p.kaufteil else "nein",
                     fmt(vol, 2), masse, bbox, note.replace(";", ",").replace("\n", " ")])
    with open(CSV, "w", encoding="utf-8-sig", newline="") as f:
        f.write("Name;Pos;Gruppe;Material;Kaufteil;Volumen_cm3;Masse_kg;BBox;Bemerkung\r\n")
        for r in rows:
            f.write(";".join(r) + "\r\n")
        f.write(f"SUMME Eigenfertigung;;;;;;{fmt(total)};;Kaufteile ohne Masse "
                f"(Volumen gesamt {fmt(total_kauf_vol, 1)} cm³)\r\n")
    return total


# ====================================================================== Baugruppe / STEP
def build_assembly(parts, solids):
    top = cq.Assembly(name="DuckDoor_Baugruppe")
    used = [g for g in GROUP_ORDER if any(p.group == g for p in parts)]
    for g in sorted({p.group for p in parts} - set(GROUP_ORDER)):
        used.append(g)
    for g in used:
        sub = cq.Assembly(name=g)
        for p in parts:
            if p.group == g:
                sub.add(cq.Workplane("XY").add(solids[p.name]), name=p.name, color=cq.Color(*p.color, 1.0))
        top.add(sub, name=g)
    return top, used


def export_part_step(p, solid, path):
    """Einzelteil als STEP AP214 mit Produktname = Bauteilname und Farbe."""
    app = XCAFApp_Application.GetApplication_s()
    doc = TDocStd_Document(TCollection_ExtendedString("XmlOcaf"))
    app.InitDocument(doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    ct = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    lab = st.AddShape(solid.wrapped, False)
    TDataStd_Name.Set_s(lab, TCollection_ExtendedString(p.name))
    ct.SetColor(lab, Quantity_Color(*p.color, Quantity_TOC_RGB), XCAFDoc_ColorSurf)
    w = STEPCAFControl_Writer()
    w.SetNameMode(True)
    w.SetColorMode(True)
    Interface_Static.SetCVal_s("write.step.schema", "AP214IS")
    Interface_Static.SetCVal_s("write.step.unit", "MM")
    w.Transfer(doc, STEPControl_AsIs)
    if w.Write(path) != IFSelect_RetDone:
        raise RuntimeError(f"STEP-Export fehlgeschlagen: {path}")


def verify_step(path):
    """Re-Import über XCAF: liefert Baumstruktur [(Ebene, Name, ist_Baugruppe)]."""
    app = XCAFApp_Application.GetApplication_s()
    doc = TDocStd_Document(TCollection_ExtendedString("XmlOcaf"))
    app.InitDocument(doc)
    r = STEPCAFControl_Reader()
    r.SetNameMode(True)
    r.SetColorMode(True)
    if r.ReadFile(path) != IFSelect_RetDone or not r.Transfer(doc):
        raise RuntimeError("STEP-Re-Import fehlgeschlagen")
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    tree = []

    def name_of(lab):
        a = TDataStd_Name()
        return a.Get().ToExtString() if lab.FindAttribute(TDataStd_Name.GetID_s(), a) else "?"

    def walk(lab, lvl):
        ref = lab
        if st.IsReference_s(lab):
            from OCP.TDF import TDF_Label
            ref = TDF_Label()
            st.GetReferredShape_s(lab, ref)
        is_asm = st.IsAssembly_s(ref)
        tree.append((lvl, name_of(lab), name_of(ref), is_asm))
        if is_asm:
            seq = TDF_LabelSequence()
            st.GetComponents_s(ref, seq, False)
            for i in range(1, seq.Length() + 1):
                walk(seq.Value(i), lvl + 1)

    roots = TDF_LabelSequence()
    st.GetFreeShapes(roots)
    for i in range(1, roots.Length() + 1):
        walk(roots.Value(i), 0)
    return tree


# ====================================================================== Vorschau (SVG -> PNG)
def _norm(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def render_svg(parts, solids, path, view_dir, title, include=None, exclude=(), clip=None, width=1600,
               height=1200, tol=0.4, max_edge=None):
    """Einfacher Flächen-Renderer (Maleralgorithmus, Lambert-Schattierung) als SVG.

    view_dir: Richtung vom Objekt zur Kamera (Parallelprojektion), z nach oben.
    clip: (xmin,xmax,ymin,ymax,zmin,zmax) – Teile werden auf diesen Quader beschnitten.
    """
    d = _norm(view_dir)
    if max_edge is None:
        max_edge = 15.0 if clip else 80.0
    fwd = tuple(-c for c in d)
    right = _norm(_cross(fwd, (0, 0, 1)))
    up = _cross(right, fwd)
    light = _norm((0.35 * d[0] + 0.3, 0.35 * d[1] - 0.2, 0.9))
    tris = []
    for p in parts:
        if include and not include(p):
            continue
        if p.name in exclude:
            continue
        sol = solids[p.name]
        if clip:
            bb = sol.BoundingBox()
            cb = cq.Solid.makeBox(clip[1] - clip[0], clip[3] - clip[2], clip[5] - clip[4],
                                  cq.Vector(clip[0], clip[2], clip[4]))
            if not _bb_overlap(bb, cb.BoundingBox()):
                continue
            sol = sol.intersect(cb)
            if sol.Volume() < 1e-3:
                continue
        verts, faces = sol.tessellate(tol, 0.3)
        V = [(v.x, v.y, v.z) for v in verts]
        stack = [(V[a], V[b], V[c]) for a, b, c in faces]
        while stack:
            A, B, C = stack.pop()
            # lange Dreiecke teilen (verbessert die Tiefensortierung des Maleralgorithmus)
            el = [math.dist(A, B), math.dist(B, C), math.dist(C, A)]
            k = el.index(max(el))
            if el[k] > max_edge:
                P0, P1, P2 = ((A, B, C), (B, C, A), (C, A, B))[k]
                M = tuple((P0[i] + P1[i]) / 2 for i in range(3))
                stack += [(P0, M, P2), (M, P1, P2)]
                continue
            cen = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3, (A[2] + B[2] + C[2]) / 3)
            n = _cross(tuple(B[i] - A[i] for i in range(3)), tuple(C[i] - A[i] for i in range(3)))
            ln = math.sqrt(_dot(n, n))
            if ln < 1e-12:
                continue
            n = tuple(c / ln for c in n)
            if _dot(n, d) < 0:           # Rückseite
                continue
            sh = 0.35 + 0.65 * max(0.0, _dot(n, light))
            col = tuple(min(255, int(255 * c * sh + 0.5)) for c in p.color)
            pts = [(_dot(P_, right), -_dot(P_, up)) for P_ in (A, B, C)]
            tris.append((_dot(cen, d), pts, col))
    if not tris:
        raise RuntimeError("keine Dreiecke für Vorschau")
    xs = [x for t in tris for x, _ in t[1]]
    ys = [y for t in tris for _, y in t[1]]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    m = 40
    s = min((width - 2 * m) / (x1 - x0), (height - 2 * m - 40) / (y1 - y0))
    ox = m + (width - 2 * m - s * (x1 - x0)) / 2 - s * x0
    oy = m + 40 + (height - 2 * m - 40 - s * (y1 - y0)) / 2 - s * y0
    tris.sort(key=lambda t: t[0])
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}">',
           f'<rect width="{width}" height="{height}" fill="#f4f5f7"/>',
           f'<text x="{m}" y="{m + 10}" font-family="sans-serif" font-size="22" fill="#222">{title}</text>']
    for _, pts, col in tris:
        c = "#%02x%02x%02x" % col
        ps = " ".join(f"{ox + s * x:.1f},{oy + s * y:.1f}" for x, y in pts)
        out.append(f'<polygon points="{ps}" fill="{c}" stroke="{c}" stroke-width="0.6" '
                   f'stroke-linejoin="round"/>')
    # Achsenkreuz
    ax0 = (width - 120, height - 60)
    for vec, lab, cc in (((1, 0, 0), "x", "#c00"), ((0, 1, 0), "+y Ente", "#080"), ((0, 0, 1), "z", "#00c")):
        ex, ey = _dot(vec, right) * 45, -_dot(vec, up) * 45
        out.append(f'<line x1="{ax0[0]}" y1="{ax0[1]}" x2="{ax0[0] + ex:.1f}" y2="{ax0[1] + ey:.1f}" '
                   f'stroke="{cc}" stroke-width="3"/>')
        out.append(f'<text x="{ax0[0] + ex * 1.2:.1f}" y="{ax0[1] + ey * 1.2:.1f}" font-family="sans-serif" '
                   f'font-size="14" fill="{cc}">{lab}</text>')
    out.append("</svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return len(tris)


SVG2PNG_JS = r"""
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const f of process.argv.slice(2)) {
    const svg = fs.readFileSync(f, 'utf8');
    const w = +/width="(\d+)"/.exec(svg)[1], h = +/height="(\d+)"/.exec(svg)[1];
    await page.setViewportSize({ width: w, height: h });
    await page.setContent('<html><body style="margin:0">' + svg + '</body></html>');
    await page.screenshot({ path: f.replace(/\.svg$/, '.png'), clip: { x: 0, y: 0, width: w, height: h } });
  }
  await browser.close();
})();
"""


def make_previews(parts, solids):
    os.makedirs(PREV_DIR, exist_ok=True)
    svgs = []
    ohne_kasten = ("1", "2", "33", "34", "35", "36", "37", "10", "7", "4", "49", "50", "=DD+K1-U1")
    views = [
        ("01_iso_Entenseite", (1.0, 1.25, 0.9),
         "DuckDoor – isometrisch Entenseite (+y), ZU_VERRIEGELT (ohne Kastendeckel 36, Schürze 2)",
         dict(exclude=("P36_Kastendeckel", "P02_Schuerze_links_vereinfacht",
                       "P02_Schuerze_rechts_vereinfacht"))),
        ("02_iso_Raubtierseite", (-1.0, -1.25, 0.9),
         "DuckDoor – isometrisch Raubtierseite (−y), Zustand ZU_VERRIEGELT", {}),
        ("03_Detail_Mitnehmer", (1.0, 1.6, 0.5),
         "Detail Mitnehmer/Klinke/Festlager, ZU_VERRIEGELT (Ausschnitt x ±90, z +500…+720)",
         dict(include=lambda p: p.pos not in ohne_kasten, clip=(-90, 90, -60, 70, 500, 720))),
        ("04_Detail_Kasten", (1.0, 1.6, 0.7),
         "Detail Antriebskasten: Loslager, Haltewinkel 26a, Motor (Kasten/Deckel ausgeblendet)",
         dict(include=lambda p: p.pos not in ohne_kasten, clip=(-120, 120, -60, 100, 1120, 1400))),
    ]
    for fn, vd, title, kw in views:
        path = os.path.join(PREV_DIR, fn + ".svg")
        n = render_svg(parts, solids, path, vd, title, **kw)
        print(f"  Vorschau {fn}: {n} Dreiecke")
        svgs.append(path)
    node = shutil.which("node")
    if not node:
        print("  node nicht gefunden – nur SVG erzeugt")
        return svgs
    js = os.path.join(PREV_DIR, "_svg2png.js")
    with open(js, "w") as f:
        f.write(SVG2PNG_JS)
    env = dict(os.environ)
    env.setdefault("NODE_PATH", "/usr/local/lib/node_modules_global")
    try:
        subprocess.run([node, js] + svgs, check=True, env=env, timeout=300)
    except Exception as e:  # noqa: BLE001
        print(f"  PNG-Erzeugung fehlgeschlagen ({e}) – nur SVG vorhanden")
    finally:
        os.remove(js)
    return svgs


# ====================================================================== Hauptprogramm
def main():
    t0 = time.time()
    args = set(sys.argv[1:])
    parts, solids = load_parts()
    print(f"{len(parts)} Parts geladen (Gestell {len(parts_gestell.build())}, Antrieb "
          f"{len(parts_antrieb.build())})")

    # ---------------------------------------------------------------- Kollisionen
    items = [(p.name, solids[p.name]) for p in parts]
    zu, n_zu = collide(items)
    mov = [(p.name, solids[p.name].translate(cq.Vector(0, 0, hub_of(p)))) for p in parts if hub_of(p)]
    fix = [(p.name, solids[p.name]) for p in parts if not hub_of(p)]
    auf1, n_a1 = collide(mov, fix)
    auf2, n_a2 = collide(mov)
    sweep = {} if "--no-sweep" in args else sweep_check(parts, solids)
    L = ["Kollisionsprotokoll DuckDoor (automatisch erzeugt von build_assembly.py)",
         f"Kriterium: Schnittvolumen > {V_TOL} mm³. Parts: {len(parts)}.", "",
         f"1) Zustand ZU_VERRIEGELT, alle Paare ({n_zu}): {len(zu)} Kollision(en)"]
    L += [f"   {a} <-> {b}: {v:.1f} mm³" for a, b, v in zu]
    L += ["", f"2) Zustand AUF (Schieber-Teile +{HUB_SCHIEBER:.0f}, Block-Teile +{HUB_BLOCK:.0f} in z)",
          "   bewegt: " + ", ".join(f"{n} (+{hub_of(p):.0f})" for p in parts for n in [p.name] if hub_of(p)),
          f"   bewegt gegen fest ({n_a1} Paare): {len(auf1)} Kollision(en)"]
    L += [f"   {a} <-> {b}: {v:.1f} mm³" for a, b, v in auf1]
    L += [f"   bewegt gegen bewegt ({n_a2} Paare): {len(auf2)} Kollision(en)"]
    L += [f"   {a} <-> {b}: {v:.1f} mm³" for a, b, v in auf2]
    if "--no-sweep" not in args:
        L += ["", "3) Hubweg ZU -> AUF (101 Zwischenstellungen, reine z-Translation, Klinke starr) – "
                  "Information, kein Endlagenkriterium:"]
        if not sweep:
            L.append("   keine Berührung mit Volumen")
        for (a, b), (h0, h1, v) in sweep.items():
            L.append(f"   {a} <-> {b}: Hub {h0:.1f}…{h1:.1f} mm, max {v:.0f} mm³")
            L.append(f"      Bewertung: {SWEEP_BEWERTUNG.get((a, b), 'nicht bewertet – prüfen')}")
    txt = "\n".join(L) + "\n"
    with open(KOLL, "w", encoding="utf-8") as f:
        f.write(txt)
    print(txt)

    # ---------------------------------------------------------------- Teileliste
    total = write_csv(parts, solids)
    print(f"Teileliste: {CSV} – Masse Eigenfertigung {total:.2f} kg")

    # ---------------------------------------------------------------- Baugruppe
    assy, used = build_assembly(parts, solids)
    Interface_Static.SetCVal_s("write.step.schema", "AP214IS")
    exportAssembly(assy, STEP_ASSY, unit="MM")
    tree = verify_step(STEP_ASSY)
    leafs = [t for t in tree if not t[3]]
    names_ok = {t[1] for t in leafs} | {t[2] for t in leafs}
    missing = [p.name for p in parts if p.name not in names_ok]
    with open(STEP_ASSY, encoding="latin-1") as f:
        head = f.read(4000)
    schema = "AP214" if "AUTOMOTIVE_DESIGN" in head.upper() else "?"
    print(f"STEP: {STEP_ASSY} – Schema {schema}; Re-Import: {len(tree)} Knoten, "
          f"{len(leafs)} Teile, Unterbaugruppen "
          f"{[t[2] for t in tree if t[3] and t[0] == 1]}; fehlende Namen: {missing or 'keine'}")
    if missing:
        raise SystemExit("Bauteilnamen nicht erhalten!")

    try:
        exportGLTF(assy, GLB, binary=True, tolerance=0.2, angularTolerance=0.2)
        print(f"glTF: {GLB}")
    except Exception as e:  # noqa: BLE001
        print(f"glTF-Export nicht möglich: {e}")

    os.makedirs(PARTS_DIR, exist_ok=True)
    for fn in os.listdir(PARTS_DIR):
        if fn.endswith(".step"):
            os.remove(os.path.join(PARTS_DIR, fn))
    for p in parts:
        export_part_step(p, solids[p.name], os.path.join(PARTS_DIR, p.name + ".step"))
    print(f"Einzelteile: {len(parts)} STEP in {PARTS_DIR}")

    if "--no-preview" not in args:
        make_previews(parts, solids)
    print(f"fertig in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
