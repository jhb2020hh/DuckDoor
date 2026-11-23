#!/usr/bin/env python3
"""Erzeugt TZ-01_Gesamtansicht.svg, TZ-02_Details.svg und TZ_Positionsliste.csv
fuer die Entenklappe DuckDoor (Rev. A, Entwurf).

Grundlage: docs/02_Freigabestand_v2.md, docs/review/11_R2_Mechanik_Sicherheit.md (Massliste),
docs/review/01_Mechanik.md (Fundament/Schuerze/Zaun), docs/review/04_Tierhaltung_Sicherheit.md.
Koordinaten: x = 0 Mitte Oeffnung, y = 0 Mittelebene Schieber (+y Entenseite), z = 0 OKF.
Aufruf: python3 drawings/src/gen_tz.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from tzlib import Sheet, frame_and_title, f  # noqa: E402
from positionen import POS  # noqa: E402

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATUM = '2026-11-23'

# ------------------------------------------------------------------ Massliste (R2-11) + Annahmen
OK_ZU, OK_AUF = 565, 1115          # Oberkante Schieber
UK_ZU, UK_AUF = 30, 580
BZ_V, BZ_E, BZ_A = 594, 645, 1195  # Bolzenmitte verriegelt / ZU entriegelt / AUF
SL_U, SL_O = 28, 80                # Langloch-Mitte unten/oben relativ OK
KERBE = 61                         # Rastkerbe UK relativ OK [A] (Massliste +45)
SP_Y = 35                          # Spindelachse y

# Klinke (u = -x, z absolut bei ZU), [A]
KL_P = (22, 670)
KL_POLY = [(14, 628), (18, 628), (18, 622), (26, 622), (26, 664), (60, 664), (60, 676), (18, 676), (18, 634),
           (14, 634)]
KL_LUG = [(26, 624), (32, 624), (32, 638), (26, 638)]
KL_STOP = (50, 662)
KL_HALTER = [(16, 665), (40, 665), (40, 545), (48, 545), (48, 678), (16, 678)]


def kulisse(bolt):
    t = bolt + 7
    b = t - 40
    return [(15, t), (26, t), (34, t - 8), (34, b + 8), (26, b), (15, b)]


def common_fields(nr, ztitel, massstab, blatt, fmt):
    return dict(abt='Abwicklung Mechanik', ref='Freigabestand v2 / R2-11', art='Techn. Zeichnung',
                status='ENTWURF', ersteller='Techn. Zeichnen (Entwurf)', genehmigt='— offen —',
                massstab=massstab, tol='ISO 2768-m [A] / mm', format=fmt, kanten='entgratet, ISO 13715 [A]',
                titel='Entenklappe „DuckDoor“', ztitel=ztitel, projekt='DuckDoor', projekt2='Abwicklungsteam',
                nr=nr, rev='A (Entwurf)', datum=DATUM, stempel='Entwurf – nicht für Fertigung', blatt=blatt)


# ------------------------------------------------------------------ Balloon-Layout
def auto_balloons(sh, items, x, ymin, ymax, r=3.8, sp=9.0, side='right'):
    """items: (nr, target_xy). Balloons in Spalte bei x, sortiert nach Ziel-y, Mindestabstand sp."""
    items = sorted(items, key=lambda it: it[1][1])
    # Gruppen bilden und um Mittel der Zielhoehen zentrieren (Clusterverfahren)
    groups = [[min(max(t[1], ymin), ymax)] for _, t in items]
    pos = [g[0] for g in groups]
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(groups) - 1:
            end_i = pos[i] + (len(groups[i]) - 1) * sp
            if end_i + sp > pos[i + 1]:
                groups[i] = groups[i] + groups[i + 1]
                del groups[i + 1]
                del pos[i + 1]
                n = len(groups[i])
                pos[i] = sum(groups[i]) / n - (n - 1) * sp / 2
                changed = True
            else:
                i += 1
        for i in range(len(groups)):
            n = len(groups[i])
            pos[i] = min(max(pos[i], ymin), ymax - (n - 1) * sp)
    ys = []
    for p0, g in zip(pos, groups):
        ys += [p0 + k * sp for k in range(len(g))]
    for (n, t), y in zip(items, ys):
        sh.balloon((x, y), n, t, r=r)


# ================================================================== TZ-01
def tz01():
    sh = Sheet(841, 594, lw=0.5)
    S = 5.0
    FX, FZ = 235.0, 45.0 + 1400 / S   # Vorderansicht: x nach links (Blick von +y)
    AX = 505.0                         # Schnitt A-A: y nach rechts

    def T(x, z):
        return (FX - x / S, FZ - z / S)

    def A(y, z):
        return (AX + y / S, FZ - z / S)

    def R(tf, a1, a2, z1, z2):
        return [tf(a1, z1), tf(a2, z1), tf(a2, z2), tf(a1, z2)]

    def rect(tf, a1, a2, z1, z2, cls='w', fill='#fff'):
        sh.pl(R(tf, a1, a2, z1, z2), cls, fill=fill)

    def sym(fn):
        fn(1)
        fn(-1)

    U = lambda u, z: T(-u, z)  # noqa: E731  (u = -x, Klinkenseite)

    # ---------------------------------------------------------------- Vorderansicht
    # Gelaende, Fundament
    sh.ground(T(700, -20)[0], T(400, -20)[0], T(0, -20)[1])
    sh.ground(T(-400, -20)[0], T(-700, -20)[0], T(0, -20)[1])
    rect(T, -400, 400, -20, 0)
    for xx in (-400, 400):
        sh.line(T(xx, -20), T(xx, -800), 'h')
    sh.line(T(-400, -800), T(400, -800), 'h')
    # Schuerze (unter Gelaende, seitlich anschliessend) – verdeckt, mit Bruch
    for s in (1, -1):
        sh.line(T(s * 400, -95), T(s * 640, -95), 'h')
        sh.zigzag_v(T(s * 650, 0)[0], T(0, -75)[1], T(0, -115)[1], 1.5)

    # Schieber ZU
    rect(T, -200, 200, UK_ZU, OK_ZU)
    # Puffer + Schaltleiste
    rect(T, -175, 175, 0, 5)
    sh.pl(R(T, -170, 170, 5, 30), 'w', fill='#fff')
    sh.line(T(-170, 12), T(170, 12), 'n')
    # Lasche mit Langloch und Rastkerbe
    ok = OK_ZU
    las = [U(-20, ok - 15), U(20, ok - 15), U(20, ok + KERBE), U(14, ok + KERBE), U(14, ok + KERBE + 10),
           U(20, ok + KERBE + 10), U(20, ok + 95), U(-20, ok + 95)]
    sh.pl(las, 'w', fill='#fff')

    def slot(tf, zc1, zc2, r=4.5, cls='w'):
        a, b = tf(0, zc1), tf(0, zc2)
        rr = r / S if tf in (T, U) else r
        d = (f'M{f(a[0]-rr)},{f(a[1])} L{f(b[0]-rr)},{f(b[1])} A{f(rr)},{f(rr)} 0 0 1 {f(b[0]+rr)},{f(b[1])} '
             f'L{f(a[0]+rr)},{f(a[1])} A{f(rr)},{f(rr)} 0 0 1 {f(a[0]-rr)},{f(a[1])} Z')
        sh.path(d, cls)
    slot(T, ok + SL_U, ok + SL_O)
    for u in (-12, 12):
        sh.circle(U(u, ok - 7.5), 1.0, 'n')
    # Klinke + Halter + Anschlag
    sh.pl([U(*p) for p in KL_POLY], 'w', fill='#fff')
    sh.pl([U(*p) for p in KL_HALTER], 'w', fill='#fff')
    sh.circle(U(*KL_P), 0.6, 'w', fill='#fff')
    sh.circle(U(*KL_STOP), 0.4, 'w', fill='#fff')
    # Fuehrungstraeger (Schenkel vorn) + Kanalwange
    sym(lambda s: rect(T, s * 175, s * 215, 0, 1140))
    sym(lambda s: sh.line(T(s * 175, 545), T(s * 215, 545), 'n'))
    # Lichtschranke B6 (2 Strahlen)
    for z in (100, 300):
        sym(lambda s: rect(T, s * 180, s * 210, z - 8, z + 8))
        sh.line(T(175, z), T(-175, z), 'c')
    # B1, B2
    rect(T, 180, 210, 24, 40)
    rect(T, -180, -210, 1094, 1110)
    # Kulisse + Lasche-Lug (Ebene y 16..20)
    sh.pl([U(*p) for p in kulisse(BZ_V)], 'w', fill='#fff')
    sh.pl([U(*p) for p in KL_LUG], 'w', fill='#fff')
    # Spindel (sichtbar unter/ueber Block)
    rect(T, -4, 4, 570, 1240)
    sym(lambda s: sh.line(T(s * 2.75, 570), T(s * 2.75, 1240), 'n'))
    # Lagerbock
    rect(T, -14, 14, 535, 545)
    rect(T, -20, 20, 545, 565)
    # Mutterblock
    rect(T, -15, 15, BZ_V - 10, BZ_V + 30)
    rect(T, 18, 30, 566, BZ_V - 10)   # B4
    # Traverse
    rect(T, -215, 215, 530, 545)
    sh.line(T(-215, 542), T(215, 542), 'n')
    rect(T, -14, 14, 535, 545)
    # Sturzblende transparent (Strich-Zweipunkt) + Sicherheitsschrauben
    sh.pl(R(T, -215, 215, 530, 1140), 'p')
    for s in (1, -1):
        for z in (600, 780, 960, 1110):
            c = T(s * 195, z)
            sh.circle(c, 1.0, 'n', fill='#fff')
            sh.circle(c, 0.35, 'af')
    # Pfosten, Fussplatten, Anker
    sym(lambda s: rect(T, s * 215, s * 275, 10, 1140))
    sym(lambda s: rect(T, s * 215, s * 375, 0, 10))
    for s in (1, -1):
        for xx in (240, 350):
            rect(T, s * (xx - 9.5), s * (xx + 9.5), 10, 20)
            rect(T, s * (xx - 6), s * (xx + 6), 20, 26)
    # PA-Anschlussfahne
    rect(T, -275, -292, 60, 80)
    sh.circle(T(-284, 70), 0.8, 'n')
    rect(T, 275, 292, 60, 80)
    sh.circle(T(284, 70), 0.8, 'n')
    # Antriebskasten (opak)
    rect(T, -275, 275, 1140, 1400)
    sh.line(T(-275, 1142), T(275, 1142), 'n')
    # Warnschild + DAE
    rect(T, 110, 210, 1230, 1330, 'n')
    tri = [T(160, 1318), T(122, 1248), T(198, 1248)]
    sh.pl(tri, 'n')
    sh.text(T(160, 1262), '!', 4.5, 'middle', weight='bold')
    sh.circle(T(-230, 1180), 2.0, 'w', fill='#fff')
    sh.circle(T(-230, 1180), 1.0, 'n')
    # verdeckte Kanten
    sym(lambda s: sh.line(T(s * 200, UK_ZU), T(s * 200, OK_ZU), 'h'))
    sh.circle(T(0, BZ_V), 4 / S, 'h')
    slot(T, ok + SL_U, ok + SL_O, cls='h')
    rect(T, -21, 21, 1295, 1343, 'h', None)       # Motor
    rect(T, -60, 60, 1291, 1295, 'h', None)       # Motorplatte
    rect(T, -60, 60, 1245, 1255, 'h', None)       # Lagerplatte
    rect(T, -10, 10, 1260, 1290, 'h', None)       # Kupplung
    sh.line(T(-4, 1140), T(-4, 1240), 'h')
    sh.line(T(4, 1140), T(4, 1240), 'h')
    rect(T, 20, 32, 1230, 1244, 'h', None)        # B3
    for xx in (-50, 50):
        rect(T, xx - 3, xx + 3, 1255, 1291, 'h', None)
    sh.line(T(-215, 1140), T(215, 1140), 'h')      # Buerstendichtung
    # Stellung AUF (Strich-Zweipunkt)
    sh.pl(R(T, -200, 200, UK_AUF, OK_AUF), 'p')
    oka = OK_AUF
    sh.pl([U(-20, oka - 15), U(20, oka - 15), U(20, oka + 95), U(-20, oka + 95)], 'p')
    sh.pl(R(T, -15, 15, BZ_A - 10, BZ_A + 30), 'p')
    sh.circle(T(0, BZ_A), 4 / S, 'p')
    # Mittellinien
    sh.line(T(0, -840), T(0, 1425), 'c')
    for s in (1, -1):
        sh.line(T(s * 245, -15), T(s * 245, 1135), 'c')
    sh.line(T(185, 280), T(-185, 280), 'c')
    # Schnittverlauf A-A (Blick nach -x  => Pfeile nach rechts auf dem Blatt)
    sh.cutmark(T(0, 1460), T(0, -860), 'A', (1, 0), size=7)
    # Schnitt B-B (z = 300, Blick von oben)
    sh.cutmark(T(310, 300), T(150, 300), 'B', (0, 1), size=7, L=7)
    # Einzelheiten
    c = T(-28, 625)
    sh.circle(c, 90 / S, 'n')
    sh.text((c[0] + 15, c[1] - 14), 'Z', 7, 'middle', weight='bold')
    sh.text((c[0] + 15, c[1] - 9), 'TZ-02', 2.5, 'middle')

    # Bemassung Vorderansicht
    xl = T(400, 0)[0]
    sh.dim_v(T(400, 0), T(215, 30), xl - 12, '30')
    sh.dim_v(T(175, 30), T(175, 530), xl - 12, '500')
    sh.dim_v(T(215, 530), T(215, 1140), xl - 12, '610')
    sh.dim_v(T(275, 1140), T(275, 1400), xl - 12, '260')
    sh.dim_v(T(200, UK_ZU), T(200, OK_ZU), xl - 24, '535')
    sh.dim_v(T(200, OK_ZU), T(200, OK_AUF), xl - 24, 'Hub 550')
    sh.dim_v(T(400, 0), T(275, 1400), xl - 36, '1400')
    sh.dim_v(T(400, -20), T(400, 0), xl - 36, '20')
    sh.dim_v(T(400, -800), T(400, 0), xl - 24, '800')
    yb = T(0, -800)[1]
    sh.dim_h(T(245, -810), T(-245, -810), yb + 9, '490')
    sh.dim_h(T(275, 10), T(-275, 10), yb + 18, '550')
    sh.dim_h(T(400, -800), T(-400, -800), yb + 27, '800')
    sh.dim_h(T(175, 470), T(-175, 470), T(0, 470)[1], '350 (Lichtöffnung)', gap=0, over=0)
    sh.dim_h(T(200, 420), T(-200, 420), T(0, 420)[1], '400', gap=0, over=1.5)
    sh.dim_h(T(215, 1060), T(-215, 1060), T(0, 1060)[1], '430', gap=0, over=0, tshift=-12)
    sh.dim_h(T(-215, 0), T(-375, 0), T(0, -60)[1] - 0, '160', size=3.0)
    sh.dim_h(T(175, 640), T(215, 640), T(0, 640)[1], '40', size=3.0, gap=0, over=0)

    # Balloons Vorderansicht
    xr = T(-700, 0)[0] + 12
    auto_balloons(sh, [
        (1, T(-300, -400)), (2, T(-600, -95)), (5, T(-330, 5)), (6, T(-350, 23)), (7, T(-245, 760)),
        (8, T(-195, 160)), (10, T(-195, 980)), (12, T(-120, 2)), (13, T(-80, 220)), (14, T(-140, 17)),
        (31, T(-160, 537)), (33, T(-120, 1135)), (34, T(-195, 780)), (35, T(-260, 1380)),
        (37, T(-230, 1180)), (39, U(55, 670)), (41, U(44, 560)), (42, U(30, 575)), (44, T(-195, 1102)),
        (48, T(-195, 300)), (49, T(-286, 62)), (21, T(-17, 555)), (20, T(-2, 860)),
        (30, T(-15, 1320)), (36, T(-200, 1399)),
    ], xr, 40, 470)
    # links (x>0-Seite) im freien Kanalbereich
    for n, tgt, pos in [
        (15, T(8, 650), T(110, 840)), (18, T(10, 610), T(110, 800)), (17, T(0, BZ_V), T(110, 760)),
        (46, T(24, 575), T(110, 720)), (43, T(195, 32), T(110, 120)), (45, T(26, 1237), T(80, 1210)),
        (50, T(160, 1300), T(240, 1310)), (27, T(8, 1275), T(40, 1190)), (26, T(50, 1250), T(150, 1180)),
        (28, T(55, 1293), T(150, 1370)),
    ]:
        sh.balloon(pos, n, tgt)

    sh.text((T(0, 0)[0], T(0, -800)[1] + 45), 'Vorderansicht (von der Entenseite, +y)', 5, 'middle', weight='bold')
    sh.text((T(0, 0)[0], T(0, -800)[1] + 50.5), 'M 1:5 – Sturzblende (33) transparent, Kasten (35) verdeckt',
            3.5, 'middle')

    # ---------------------------------------------------------------- Schnitt A-A
    # Hintergrund (hinter Schnittebene, x < 0)
    rect(A, -30, 30, 10, 1140, 'w', None)                # Pfosten
    rect(A, -80, 80, 0, 10, 'w', None)                   # Fussplatte
    rect(A, -23, 17, 0, 1140, 'w', None)                 # Fuehrung/Traeger
    rect(A, 17, 62, 545, 1140, 'w', None)                # Kanalwange
    for z in (100, 300):
        rect(A, 17, 30, z - 8, z + 8, 'w', '#fff')       # B6
        sh.circle(A(20, z), 0.8, 'n')
        sh.circle(A(20, z), 0.25, 'af')
    rect(A, 6, 14, 545, 680, 'n', '#fff')                # Klinke/Halter (vereinfacht)
    # Fundament (geschnitten)
    sh.pl(R(A, -150, 150, -800, 0), 'w', fill='url(#hBeton)')
    sh.ground(A(-260, 0)[0], A(-150, 0)[0], A(0, -20)[1])
    sh.ground(A(150, 0)[0], A(260, 0)[0], A(0, -20)[1])
    # Schwellenwinkel (schmale Schnittflaeche geschwaerzt)
    sh.pl([A(-59, 0), A(-9, 0), A(-9, 30), A(-13, 30), A(-13, 4), A(-59, 4)], 'n', fill='#000')
    sh.pl(R(A, -8, 8, 0, 5), 'n', fill='url(#hGummi)')              # Puffer
    sh.pl(R(A, -6, 6, 5, 30), 'w', fill='#fff')                      # Schaltleiste
    sh.pl(R(A, -3.5, 3.5, 9, 26), 'n')
    sh.pl(R(A, -2, 2, UK_ZU, OK_ZU), 'n', fill='#000')               # Schieber
    sh.pl(R(A, 2, 6, OK_ZU - 15, OK_ZU + SL_U - 4.5), 'n', fill='#000')   # Lasche unter Langloch
    sh.pl(R(A, 2, 6, OK_ZU + SL_O + 4.5, OK_ZU + 95), 'n', fill='#000')  # Lasche ueber Langloch
    # Traverse, Lippe, Sturzblende
    sh.pl([A(8, 530), A(11, 530), A(11, 542), A(65, 542), A(65, 545), A(8, 545)], 'n', fill='#000')
    sh.pl(R(A, 2, 8, 530, 538), 'n', fill='url(#hGummi)')
    sh.pl(R(A, 62, 65, 545, 1140), 'n', fill='#000')
    # Lagerbock (geschnitten), Lager
    sh.pl([A(20, 545), A(24, 545), A(24, 535), A(46, 535), A(46, 545), A(50, 545), A(50, 565), A(20, 565)],
          'w', fill='url(#hA)')
    for zz in (552, 558):
        for ya, yb in ((25.5, 32), (38, 44.5)):
            sh.pl(R(A, ya, yb, zz, zz + 6), 'n', fill='#fff')
            sh.line(A(ya, zz), A(yb, zz + 6), 'n')
            sh.line(A(ya, zz + 6), A(yb, zz), 'n')
    # Spindel (Ansicht)
    rect(A, 31, 39, 570, 1240)
    sh.line(A(32.25, 570), A(32.25, 1240), 'n')
    sh.line(A(37.75, 570), A(37.75, 1240), 'n')
    rect(A, 32, 38, 540, 570)
    rect(A, 32, 38, 1240, 1275)
    # Mutterblock (geschnitten) mit Mutter, Bolzen (Ansicht)
    b = BZ_V
    sh.pl([A(20, b - 10), A(30, b - 10), A(30, b + 8), A(24, b + 8), A(24, b + 30), A(20, b + 30)],
          'w', fill='url(#hA)')
    sh.pl([A(40, b - 10), A(50, b - 10), A(50, b + 30), A(46, b + 30), A(46, b + 8), A(40, b + 8)],
          'w', fill='url(#hA)')
    sh.pl(R(A, 24, 31, b + 8, b + 30), 'n', fill='url(#hK)')
    sh.pl(R(A, 39, 46, b + 8, b + 30), 'n', fill='url(#hK)')
    rect(A, 0, 28, b - 4, b + 4)
    # Kasten (geschnitten), Deckel, Buerste
    zt = lambda y: 1375 + (y + 40) / 140 * 25  # noqa: E731
    sh.pl([A(-40, 1140), A(-38, 1140), A(-38, zt(-38) - 2), A(98, zt(98) - 2), A(98, 1142), A(65, 1142),
           A(65, 1140), A(100, 1140), A(100, zt(100)), A(-40, zt(-40))], 'n', fill='#000')
    sh.pl([A(-38, 1140), A(-3, 1140), A(-3, 1142), A(-38, 1142)], 'n', fill='#000')
    for yy in range(-2, 62, 3):
        sh.line(A(yy, 1137), A(yy + 1.5, 1143), 'n')
    # Lagerplatte, Motorplatte (geschnitten), Kupplung, Motor, Distanzbolzen
    sh.pl([A(5, 1245), A(25.5, 1245), A(25.5, 1255), A(5, 1255)], 'n', fill='url(#hB)')
    sh.pl([A(44.5, 1245), A(65, 1245), A(65, 1255), A(44.5, 1255)], 'n', fill='url(#hB)')
    sh.pl(R(A, 25.5, 32, 1247, 1253), 'n', fill='#fff')
    sh.pl(R(A, 38, 44.5, 1247, 1253), 'n', fill='#fff')
    sh.pl(R(A, 5, 65, 1291, 1295), 'n', fill='#000')
    rect(A, 25, 45, 1260, 1290)
    rect(A, 14, 56, 1295, 1343)
    for ya in (5, 59):
        rect(A, ya, ya + 6, 1255, 1291, 'n')
    # Stellung AUF
    sh.pl(R(A, -2, 2, UK_AUF, OK_AUF), 'p')
    sh.pl(R(A, 2, 6, OK_AUF - 15, OK_AUF + 95), 'p')
    sh.pl(R(A, 20, 50, BZ_A - 10, BZ_A + 30), 'p')
    sh.pl(R(A, 0, 28, BZ_A - 4, BZ_A + 4), 'p')
    # Mittellinien
    sh.line(A(SP_Y, 525), A(SP_Y, 1350), 'c')
    sh.line(A(0, -830), A(0, 1180), 'c')
    # Einzelheit Y (Lagerung)
    for zc, lab in ((560, 'Y1'), (1275, 'Y2')):
        c = A(35, zc)
        sh.circle(c, 9, 'n')
        sh.text((c[0] + 9.5, c[1] - 6.5), lab, 5, 'start', weight='bold')
    # Hoehenkoten
    xd = A(-150, 0)[0] - 22
    kot = [(-800, '−800', -150), (-20, '−20 Gelände', -150), (30, '+30', -13), (100, '+100 B6', 17),
           (300, '+300 B6', 17), (530, '+530', 8), (565, '+565 OK ZU', -2), (594, '+594 Bolzen', 0),
           (1115, '+1115 OK AUF', -2), (1140, '+1140', -40), (1195, '+1195 Bolzen AUF', 0),
           (1295, '+1295 Motor', 5), (1343, '+1343', 14), (1375, '+1375', -40)]
    sh.koten(xd, [(A(0, z)[1], t, A(y, 0)[0]) for z, t, y in kot], side='left', size=3.0,
             origin=A(0, 0)[1])
    sh.text((xd - 3.2, A(0, 0)[1] + 1.1), '±0 OKF', 3.0, 'end', weight='bold')
    # Masse y
    yt = A(0, 1400)[1]
    sh.dim_h(A(-40, zt(-40)), A(100, 1400), yt - 7, '140')
    sh.dim_h(A(0, 1180), A(SP_Y, 1350), yt - 15, '35', size=3.0)
    sh.dim_h(A(SP_Y, 1350), A(65, 1140), yt - 15, '30', size=3.0)
    ybA = A(0, -800)[1]
    sh.dim_h(A(-59, 0), A(100, 1140), ybA + 10, '159', gap=1.0)
    sh.dim_h(A(-150, -800), A(150, -800), ybA + 19, '300')
    sh.dim_h(A(-59, 0), A(0, -830), ybA + 28, '59', size=3.0)
    # Balloons A-A
    xrA = A(260, 0)[0] + 12
    auto_balloons(sh, [
        (1, A(100, -300)), (11, A(-40, 2)), (12, A(-4, 2)), (14, A(4, 20)), (13, A(0, 300)),
        (9, A(-18, 700)), (7, A(25, 900)), (31, A(40, 543.5)), (32, A(5, 534)), (21, A(48, 556)),
        (22, A(42, 561)), (18, A(48, 612)), (19, A(42, 615)), (17, A(14, BZ_V)), (15, A(4, 657)),
        (39, A(12, 650)), (10, A(55, 1000)), (33, A(63.5, 820)), (20, A(35, 760)), (38, A(30, 1140)),
        (26, A(60, 1250)), (29, A(62, 1270)), (27, A(45, 1275)), (28, A(62, 1293)), (30, A(56, 1320)),
        (35, A(99, 1250)), (36, A(60, 1393)), (48, A(30, 300)),
    ], xrA, 40, 470)
    sh.text((AX + 5, ybA + 45), 'Schnitt A–A (x = 0)', 5, 'middle', weight='bold')
    sh.text((AX + 5, ybA + 50.5), 'M 1:5 – vereinfacht', 3.5, 'middle')

    # ---------------------------------------------------------------- Hinweise
    hx, hy = 612, 26
    notes = [
        ('b', 'Hinweise'),
        ('', '1  Koordinaten: x = 0 Mitte Lichtöffnung, y = 0 Mittelebene Schieber'),
        ('', '   (+y Entenseite), z = 0 Oberkante Fundament OKF (+20 über Gelände [A]).'),
        ('', '2  Dargestellt: Zustand ZU_VERRIEGELT (Bolzen +594). Stellung AUF als'),
        ('', '   schmale Strich-Zweipunktlinie (Schieber 580…1115, Bolzen +1195).'),
        ('', '3  Maße in mm. Allgemeintoleranz ISO 2768-m [A]. Führungen parallel ±1'),
        ('', '   auf Länge; Spindelachse parallel zur Führung ±0,5; Lasche mittig ±0,5.'),
        ('', '4  Gesamtmaße H 1400 (über OKF) × B 550 × T 140 (Kasten), 159 mit Pos. 11.'),
        ('', '5  Hub 550, Fahrweg Mutter 601 (Bolzen +594 … +1195), Freiweg Langloch 52.'),
        ('', '6  Spindel (20) und Mitnehmer vollständig im Kanal hinter Sturzblende (33);'),
        ('', '   Sturzblende und Deckel nur mit Sicherheitsschrauben (34) – Kinder.'),
        ('', '7  Endschalter: B1 UK Schieber ≤ +32; B2 OK Schieber ≥ +1110;'),
        ('', '   B3 Bolzen +1200 (5 Überlauf); B4 Bolzen +594; B8 am Mutterblock.'),
        ('', '8  Lichtschranke B6: 2 Strahlen z +100 / +300, y +20 (Halter im'),
        ('', '   Führungsträger 8, außerhalb x ±175). Schaltleiste B7 an UK Schieber.'),
        ('', '9  Einzelheiten Z, Y1, Y2, Schnitt B–B, Fundament: siehe TZ-02.'),
        ('', '10 Positionsnummern = TZ_Positionsliste.csv.'),
        ('', '11 Betreiber (M8): Personentür des Nachtgeheges von innen ohne'),
        ('', '   Werkzeug öffenbar ausführen (Kind eingeschlossen).'),
        ('b', ''),
        ('b', 'Annahmen / Abweichungen von der Maßliste R2-11 [A]'),
        ('', 'A1 Schwellenwinkel (11) L 350 statt 430: zwischen den Führungen,'),
        ('', '   sonst Kollision mit Führungsprofil x ±175…±211.'),
        ('', 'A2 Fußplatte (5) außermittig x ±215…±375: mittig (x ±165…±325)'),
        ('', '   ragt sie in Lichtöffnung/Führung.'),
        ('', 'A3 Führung: PE-UHMW-Profil 36 × 26 mit Nut 6 × 30 (9) auf Winkel'),
        ('', '   40 × 40 × 4 (8); Kanalwange (10) trägt Sturzblende (33).'),
        ('', 'A4 Bolzen (17) nur y 0…+28 statt bis +35 (Spindelachse, Kollision);'),
        ('', '   Mutterblock z = Bolzen −10…+30, Mutter L 22 oberhalb des Bolzens.'),
        ('', 'A5 Rastkerbe UK OK+61 statt +45 (Bauraum Entriegelungskulisse 42).'),
        ('', 'A6 Schaltleiste (14) L 340, B ≤ 12: Nut nur 6 breit, Durchgang Traverse.'),
        ('', 'A7 Langloch: Mittenabstand 52 (= Freiweg), Gesamtlänge 61 (Liste: 60).'),
        ('', 'A8 Fundament T 800 ab OKF ⇒ 780 unter Gelände; Frosttiefe örtl. prüfen.'),
        ('', 'A9 Kastendeckel 10° fallend: OK +1400 Entenseite, +1375 Raubtierseite.'),
        ('', 'A10 Bürstendichtung (38): Durchtritt Lasche/Mutterblock offen.'),
    ]
    yy = hy
    for kind, t in notes:
        if kind == 'b':
            sh.text((hx, yy), t, 4.2, weight='bold')
            yy += 6.2
        else:
            sh.text((hx, yy), t, 3.2)
            yy += 4.75
    # Banner
    sh.text((30, 24), 'ENTWURF – NICHT FÜR FERTIGUNG', 6, weight='bold', fill='#c00000')
    sh.text((30, 30.5), 'Rev. A, 2026-11-23 – Grundlage Freigabestand v2 / Maßliste R2-11', 3.5)

    frame_and_title(sh, common_fields('TZ-01', 'Gesamtansicht: Vorderansicht, Schnitt A–A', '1:5',
                                      '1 / 2', 'A1 / 1 von 2'))
    return sh


# ================================================================== TZ-02
def rot(p, c, th):
    """Drehung um c (u,z mit z nach oben), th>0 = Gegenuhrzeigersinn"""
    dx, dz = p[0] - c[0], p[1] - c[1]
    return (c[0] + dx * math.cos(th) - dz * math.sin(th), c[1] + dx * math.sin(th) + dz * math.cos(th))


KL_TH = 0.205   # Entriegelungsdrehung [rad] ≈ 11,7°


def tz02():
    sh = Sheet(841, 594, lw=0.5)

    def R(tf, a1, a2, z1, z2):
        return [tf(a1, z1), tf(a2, z1), tf(a2, z2), tf(a1, z2)]

    def rect(tf, a1, a2, z1, z2, cls='w', fill='#fff'):
        sh.pl(R(tf, a1, a2, z1, z2), cls, fill=fill)

    def slot(tf, zc1, zc2, r=4.5, cls='w', sc=1.0, fill=None):
        a, b = tf(0, zc1), tf(0, zc2)
        rr = r * sc
        d = (f'M{f(a[0]-rr)},{f(a[1])} L{f(b[0]-rr)},{f(b[1])} A{f(rr)},{f(rr)} 0 0 1 {f(b[0]+rr)},{f(b[1])} '
             f'L{f(a[0]+rr)},{f(a[1])} A{f(rr)},{f(rr)} 0 0 1 {f(a[0]-rr)},{f(a[1])} Z')
        sh.path(d, cls, fill=fill)

    def caption(x, y, t1, t2):
        sh.text((x, y), t1, 5, 'middle', weight='bold')
        sh.text((x, y + 5.5), t2, 3.5, 'middle')

    # ------------------------------------------------------------ Einzelheit Z: 3 Stellungen, M 1:1
    states = [
        ('VERRIEGELT', OK_ZU, BZ_V, 0.0, 85, 690),
        ('ZU entriegelt', OK_ZU, BZ_E, KL_TH, 205, 690),
        ('AUF', OK_AUF, BZ_A, None, 325, 1240),
    ]
    ytop = 42
    for name, ok, bz, th, x0, zmax in states:
        W = lambda u, z, x0=x0, zmax=zmax: (x0 + u, ytop + (zmax - z))  # noqa: E731
        zmin = zmax - 150
        # Schieber (Ausschnitt mit Bruchkanten)
        rect(W, -30, 62, ok - 22, ok, 'n', '#fff')
        sh.line(W(-30, ok), W(62, ok), 'w')
        sh.breakline_h(W(0, ok - 22)[1], W(-30, 0)[0], W(62, 0)[0], 1.0)
        sh.text(W(48, ok - 15), '13', 3.0, 'middle')
        # Lasche
        las = [(-20, ok - 15), (18, ok - 15), (20, ok - 13), (20, ok + KERBE), (14, ok + KERBE),
               (14, ok + KERBE + 10), (20, ok + KERBE + 10), (20, ok + 95), (-20, ok + 95)]
        sh.pl([W(*p) for p in las], 'w', fill='#fff')
        slot(W, ok + SL_U, ok + SL_O)
        sh.line(W(0, ok + SL_U - 8), W(0, ok + SL_O + 8), 'c')
        for u in (-12, 12):
            sh.circle(W(u, ok - 7.5), 2.75, 'n')
            sh.circle(W(u, ok - 7.5), 5.0, 'n')
        rect(W, -14, -8, ok + 86, ok + 92, 'n', '#fff')   # Magnet B8
        sh.line(W(-14, ok + 86), W(-8, ok + 92), 'n')
        # Bolzen
        sh.circle(W(0, bz), 4, 'w', fill='#fff')
        sh.line(W(-6, bz), W(6, bz), 'c')
        # Mutterblock + Spindel (angrenzend, Strich-Zweipunkt)
        sh.pl(R(W, -15, 15, bz - 10, bz + 30), 'p')
        rect(W, -15, -11, bz + 6, bz + 12, 'p', None)       # Reed B8
        sh.line(W(-4, bz + 30), W(-4, min(zmax, bz + 45)), 'p')
        sh.line(W(4, bz + 30), W(4, min(zmax, bz + 45)), 'p')
        sh.line(W(-4, max(zmin, bz - 25)), W(-4, bz - 10), 'p')
        sh.line(W(4, max(zmin, bz - 25)), W(4, bz - 10), 'p')
        # Kulisse am Mutterblock
        kp = [(u, z) for u, z in kulisse(bz) if True]
        kz = [z for _, z in kp]
        if min(kz) < zmax and max(kz) > zmin:
            kp = [(u, max(min(z, zmax), zmin)) for u, z in kp]
            sh.pl([W(*p) for p in kp], 'w', fill='#fff')
        if th is not None:
            # Halter (angrenzend), Klinke, Lug, Achse, Anschlag
            sh.pl([W(*p) for p in KL_HALTER if p[1] >= zmin] + [W(48, zmin), W(40, zmin)], 'p')
            poly = [rot(p, KL_P, th) for p in KL_POLY]
            sh.pl([W(*p) for p in poly], 'w', fill='#fff')
            lug = [rot(p, KL_P, th) for p in KL_LUG]
            sh.pl([W(*p) for p in lug], 'w', fill='#fff')
            sh.circle(W(*KL_P), 3, 'w', fill='#fff')
            sh.line(W(KL_P[0] - 5, KL_P[1]), W(KL_P[0] + 5, KL_P[1]), 'c')
            sh.line(W(KL_P[0], KL_P[1] - 5), W(KL_P[0], KL_P[1] + 5), 'c')
            sh.circle(W(*KL_STOP), 2, 'w', fill='#fff')
            # Traverse (angrenzend)
        # Fenster-Rahmenhinweis
        sh.text((x0 + 16, ytop + 158), name, 4.2, 'middle', weight='bold')
        sh.text((x0 + 16, ytop + 163.5), f'Bolzen +{bz}, OK Schieber +{ok}', 3.0, 'middle')
        # Koten links je Stellung
    # Bemassung Stellung 1 (Lasche)
    x0 = 85
    W = lambda u, z: (x0 + u, ytop + (690 - z))  # noqa: E731
    ok = OK_ZU
    sh.dim_h(W(-20, ok + 95), W(20, ok + 95), W(0, ok + 95)[1] - 6, '40')
    sh.dim_h(W(-4.5, ok + SL_O), W(4.5, ok + SL_O), W(0, ok + SL_O)[1] - 10, '9 H11', size=3.0)
    sh.dim_h(W(14, ok + KERBE + 10), W(20, ok + KERBE + 10), W(0, ok + 95)[1] - 6, '6', size=3.0)
    sh.dim_v(W(20, ok + KERBE), W(20, ok + KERBE + 10), W(28, 0)[0], '10', size=3.0)
    sh.dim_v(W(0, ok + SL_U), W(0, ok + SL_O), W(-26, 0)[0], '52 (Freiweg)', size=3.0)
    sh.dim_v(W(-20, ok), W(0, ok + SL_U), W(-33, 0)[0], '28', size=3.0)
    sh.dim_v(W(-20, ok - 15), W(-20, ok + 95), W(-40, 0)[0] - 3, '110', size=3.0)
    sh.dim_v(W(-20, ok - 15), W(-20, ok), W(-33, 0)[0], '15', size=3.0)
    sh.leader_text(W(17, ok + KERBE + 5), (x0 + 30, W(0, ok + KERBE)[1] + 16),
                   ['Rastkerbe 6×10', 'UK = OK+61 [A]'], size=2.8, arrow=False, dot=True)
    sh.leader_text(W(-11, ok + 89), (x0 - 24, W(0, ok + 95)[1] - 14), ['Magnet B8 [A]'], size=2.8,
                   side='left', arrow=False, dot=True)
    sh.leader_text(W(19.3, ok - 14.3), (x0 + 36, W(0, ok)[1] + 8), ['Fase 2×45°'], size=2.8,
                   arrow=False, dot=True)
    for n, t, pos in [(15, W(-17, ok + 50), (x0 - 44, ytop + 40)), (17, W(2.5, BZ_V + 2.5), (x0 - 44, ytop + 108)),
                      (16, W(-12, ok - 7.5), (x0 - 44, ytop + 140)), (39, W(40, 670), (x0 + 72, ytop + 10)),
                      (42, W(30, 590), (x0 + 72, ytop + 110)), (41, W(44, 600), (x0 + 72, ytop + 90)),
                      (40, W(22, 670), (x0 + 50, ytop + 2))]:
        sh.balloon(pos, n, t, r=3.5, size=3.2)
    # Stellung 2: Hinweise
    x0 = 205
    W = lambda u, z: (x0 + u, ytop + (690 - z))  # noqa: E731
    sh.leader_text(W(33, 630), (x0 + 50, W(0, 615)[1]), ['Kulisse drückt', 'Lasche 34 →', 'Klinke 11,7° auf'],
                   size=2.8, arrow=False, dot=True)
    sh.leader_text(W(0, BZ_E - 4), (x0 + 66, W(0, 600)[1]), ['Bolzen am oberen', 'Langlochende:',
                                                                   'Schieber hängt am', 'Bolzen, B8 = Last'],
                   size=2.8, arrow=False, dot=True)
    # Stellung 3
    x0 = 325
    W = lambda u, z: (x0 + u, ytop + (1240 - z))  # noqa: E731
    sh.mtext((x0 + 24, ytop + 92), ['Klinke 39 in', 'Ruhelage auf', 'Anschlag (z +622…', '+676), Lasche frei'],
             size=2.8)
    sh.text((232, 25), 'Einzelheit Z – Langloch-Mitnehmer, Stellungen (Ansicht von +y, u = −x)', 5, 'middle',
            weight='bold')
    sh.text((232, 31), 'M 1:1 – Mutterblock 18, Spindel 20 und Halter 41 als angrenzende Teile (Strich-Zweipunkt)',
            3.5, 'middle')

    # ------------------------------------------------------------ Schwerkraftklinke M 2:1
    kx0, kz0, ky0 = 420, 686, 48
    K = lambda u, z: (kx0 + 2 * u, ky0 + 2 * (kz0 - z))  # noqa: E731
    ok = OK_ZU
    las = [(-6, 612), (20, 612), (20, ok + KERBE), (14, ok + KERBE), (14, ok + KERBE + 10), (20, ok + KERBE + 10),
           (20, 660), (-6, 660)]
    sh.pl([K(*p) for p in las], 'n', fill='#fff')
    sh.pl([K(-6, 612), K(20, 612), K(20, ok + KERBE), K(14, ok + KERBE), K(14, ok + KERBE + 10),
           K(20, ok + KERBE + 10), K(20, 660), K(-6, 660)], 'w', close=False)
    sh.breakline_v(K(-6, 0)[0], K(0, 660)[1], K(0, 612)[1], 1.5)
    sh.text(K(3, 650), '15', 3.0, 'middle')
    sh.pl([K(*p) for p in KL_HALTER if p[1] >= 612] + [K(48, 612), K(40, 612)], 'p')
    sh.pl([K(*rot(p, KL_P, KL_TH)) for p in KL_POLY], 'p')
    sh.pl([K(*p) for p in KL_POLY], 'w', fill='#fff')
    sh.pl([K(*p) for p in KL_LUG], 'w', fill='#fff')
    sh.circle(K(*KL_P), 6, 'w', fill='#fff')
    sh.line(K(KL_P[0] - 8, KL_P[1]), K(KL_P[0] + 8, KL_P[1]), 'c')
    sh.line(K(KL_P[0], KL_P[1] - 30), K(KL_P[0], KL_P[1] + 8), 'c')
    sh.circle(K(*KL_STOP), 4, 'w', fill='#fff')
    # Kulisse bei Beginn Entriegelung (Bolzen +617)
    kp = [(u, max(z, 612)) for u, z in kulisse(617)]
    sh.pl([K(*p) for p in kp], 'p')
    # Kraft beim Aufhebeln
    sh.arrow(K(16, 628), (0, -1), 3.5, 0.8)
    sh.line(K(16, 628), K(16, 620), 'w')
    sh.text((K(16, 620)[0] - 1.5, K(16, 620)[1] + 2), 'F (Aufhebeln)', 3.0, 'end')
    # Masse (relativ OK Schieber ZU = +565)
    sh.dim_h(K(16, 631), K(22, 670), K(0, 684)[1] - 3, '6', size=3.0)
    sh.dim_v(K(26, 631), K(22, 670), K(66, 0)[0], '39', size=3.0)
    sh.dim_h(K(14, 628), K(18, 628), K(0, 614)[1] + 4, '4', size=3.0)
    sh.dim_v(K(14, 628), K(14, 634), K(8, 0)[0], '6', size=3.0)
    sh.dim_h(K(22, 676), K(60, 676), K(0, 684)[1] - 3, '38', size=3.0)
    sh.mtext((kx0 - 6, ky0 + 165), [
        'Funktion (schematisch, Geometrie [A]):',
        '• Drehpunkt P (u 22, z +670) über dem Zahn, Hebel e = 6 nach außen:',
        '  Hebelkraft F am Zahn erzeugt Moment im Uhrzeigersinn ⇒ Zahn tiefer',
        '  in die Kerbe (selbstverstärkend). Schwerpunkt außen ⇒ fällt selbsttätig ein.',
        '• Entriegeln: Kulisse 42 am Mutterblock (Ebene y +16…+20) drückt Lasche',
        '  der Klinke um 8 nach außen ⇒ 11,7°, Zahn 8 aus Kerbe. Beginn Bolzen +617,',
        '  frei ab +625, also innerhalb Freiweg (+594 … +645). Kulisse hält bis +670,',
        '  beidseitige Anlaufschrägen ⇒ kein Klappmechanismus nötig.',
        '• Schließen: UK Lasche (Fase) drückt Zahn nach außen; Anschlag (41) begrenzt.',
        '• Nachweis im Funktionsmuster erforderlich (offener Punkt).',
    ], size=2.8, lh=1.4)
    sh.text((kx0 + 60, 25), 'Einzelheit K – Schwerkraftklinke 39', 5, 'middle', weight='bold')
    sh.text((kx0 + 60, 31), 'M 2:1 – Stellung VERRIEGELT (voll), entriegelt (Strich-Zweipunkt)', 3.5, 'middle')
    for n, t, pos in [(39, K(40, 670), (kx0 + 125, ky0 + 18)), (40, K(22, 673), (kx0 + 55, ky0 - 8)),
                      (41, K(44, 640), (kx0 + 125, ky0 + 40)), (42, K(30, 616), (kx0 + 125, ky0 + 120)),
                      (15, K(5, 625), (kx0 - 10, ky0 + 115))]:
        sh.balloon(pos, n, t, r=3.5, size=3.2)
    sh.text((K(KL_P[0], 0)[0] - 3, K(0, KL_P[1])[1] - 7), 'P', 3.5, 'end', weight='bold')

    # ------------------------------------------------------------ Spindellagerung M 1:1
    LX = 660
    L1 = lambda y, z: (LX + y, 238 + (632 - z))   # noqa: E731
    L2 = lambda y, z: (LX + y, 44 + (1350 - z))   # noqa: E731

    def bearing(tf, z0):
        for side in (1, -1):
            yo = lambda v: SP_Y + side * v  # noqa: E731
            sh.pl(R(tf, yo(6.5), yo(9.5), z0, z0 + 6), 'n', fill='url(#hA)')
            sh.pl(R(tf, yo(3), yo(5.2), z0, z0 + 6), 'n', fill='url(#hA)')
            sh.circle(tf(yo(5.85), z0 + 3), 1.6, 'n', fill='#fff')

    # unten
    T = L1
    sh.pl(R(T, -2, 2, 528, OK_ZU), 'n', fill='#000')
    sh.pl(R(T, 2, 6, OK_ZU - 15, OK_ZU + SL_U - 4.5), 'n', fill='#000')
    sh.pl([T(8, 530), T(11, 530), T(11, 542), T(23.5, 542), T(23.5, 545), T(8, 545)], 'n', fill='url(#hB)')
    sh.pl([T(46.5, 542), T(65, 542), T(65, 545), T(46.5, 545)], 'n', fill='url(#hB)')
    sh.pl(R(T, 2, 8, 530, 538), 'n', fill='url(#hGummi)')
    sh.pl(R(T, 62, 65, 545, 632), 'n', fill='url(#hB)')
    sh.pl([T(20, 565), T(25.5, 565), T(25.5, 552), T(29, 552), T(29, 535), T(24, 535), T(24, 545), T(20, 545)],
          'w', fill='url(#hA)')
    sh.pl([T(50, 565), T(44.5, 565), T(44.5, 552), T(41, 552), T(41, 535), T(46, 535), T(46, 545), T(50, 545)],
          'w', fill='url(#hA)')
    bearing(T, 552)
    bearing(T, 558)
    for ya in (24.3, 44.7):
        rect(T, ya, ya + 1.0 if ya < 30 else ya + 1.0, 564.0, 565.0, 'n', '#000')
    sh.pl(R(T, 30, 32, 564, 570), 'n', fill='url(#hB)')
    sh.pl(R(T, 38, 40, 564, 570), 'n', fill='url(#hB)')
    sh.pl(R(T, 29.5, 32, 545, 550), 'n', fill='url(#hB)')
    sh.pl(R(T, 38, 40.5, 545, 550), 'n', fill='url(#hB)')
    sh.pl(R(T, 29.5, 32, 550, 551), 'n', fill='#000')
    sh.pl(R(T, 38, 40.5, 550, 551), 'n', fill='#000')
    rect(T, 32, 38, 540, 570)
    sh.line(T(32.5, 540), T(32.5, 552), 'n')
    sh.line(T(37.5, 540), T(37.5, 552), 'n')
    rect(T, 31, 39, 570, 632)
    sh.line(T(32.25, 570), T(32.25, 632), 'n')
    sh.line(T(37.75, 570), T(37.75, 632), 'n')
    b = BZ_V
    sh.pl([T(20, b - 10), T(30, b - 10), T(30, b + 8), T(24, b + 8), T(24, b + 30), T(20, b + 30)], 'w',
          fill='url(#hA)')
    sh.pl([T(40, b - 10), T(50, b - 10), T(50, b + 30), T(46, b + 30), T(46, b + 8), T(40, b + 8)], 'w',
          fill='url(#hA)')
    sh.pl(R(T, 24, 31, b + 8, b + 30), 'n', fill='url(#hK)')
    sh.pl(R(T, 39, 46, b + 8, b + 30), 'n', fill='url(#hK)')
    rect(T, 0, 20, b - 4, b + 4)
    sh.pl(R(T, 20, 28, b - 3, b + 3), 'n', fill='#fff')
    sh.line(T(20, b - 2.5), T(28, b - 2.5), 'n')
    sh.line(T(20, b + 2.5), T(28, b + 2.5), 'n')
    sh.line(T(SP_Y, 532), T(SP_Y, 632), 'c')
    sh.line(T(-4, b), T(30, b), 'c')
    sh.breakline_h(T(0, 632)[1], T(-4, 0)[0], T(68, 0)[0], 1.2)
    # oben
    T = L2
    sh.breakline_h(T(0, 1180)[1], T(-4, 0)[0], T(68, 0)[0], 1.2)
    rect(T, 31, 39, 1180, 1240)
    sh.line(T(32.25, 1180), T(32.25, 1240), 'n')
    sh.line(T(37.75, 1180), T(37.75, 1240), 'n')
    rect(T, 32, 38, 1240, 1260)
    sh.pl(R(T, 5, 25.5, 1245, 1255), 'w', fill='url(#hB)')
    sh.pl(R(T, 44.5, 65, 1245, 1255), 'w', fill='url(#hB)')
    bearing(T, 1247)
    for ya in (5, 59):
        rect(T, ya, ya + 6, 1255, 1291, 'n')
    rect(T, 25, 45, 1260, 1272)
    rect(T, 26, 44, 1272, 1278)
    sh.pl(R(T, 26, 44, 1272, 1278), 'n', fill='url(#hK)')
    rect(T, 25, 45, 1278, 1290)
    sh.line(T(32, 1260), T(32, 1275), 'h')
    sh.line(T(38, 1260), T(38, 1275), 'h')
    sh.line(T(32, 1275), T(38, 1275), 'h')
    sh.line(T(32.5, 1280), T(32.5, 1295), 'h')
    sh.line(T(37.5, 1280), T(37.5, 1295), 'h')
    sh.line(T(32.5, 1280), T(37.5, 1280), 'h')
    sh.pl(R(T, 5, 24, 1291, 1295), 'w', fill='url(#hA)')
    sh.pl(R(T, 46, 65, 1291, 1295), 'w', fill='url(#hA)')
    rect(T, 24, 46, 1293, 1295)
    rect(T, 14, 56, 1295, 1343)
    sh.line(T(14, 1300), T(56, 1300), 'n')
    sh.line(T(14, 1338), T(56, 1338), 'n')
    sh.pl(R(T, 20, 50, 1185, 1225), 'p')
    sh.pl(R(T, 0, 28, BZ_A - 4, BZ_A + 4), 'p')
    sh.pl(R(T, 2, 6, 1180, OK_AUF + 95), 'p')
    sh.line(T(SP_Y, 1180), T(SP_Y, 1350), 'c')
    # Koten
    kl1 = [(535, '+535', 24), (545, '+545', 8), (552, '+552', 25.5), (565, '+565', 20), (570, '+570', 31),
           (584, '+584', 20), (594, '+594 Bolzen', 0)]
    sh.koten(LX - 14, [(L1(0, z)[1], t, L1(y, 0)[0]) for z, t, y in kl1], side='left', size=3.0)
    kl2 = [(1195, '+1195 (AUF)', 0), (1240, '+1240', 31), (1245, '+1245', 5), (1255, '+1255', 5),
           (1260, '+1260', 25), (1290, '+1290', 25), (1295, '+1295', 5), (1343, '+1343', 14)]
    sh.koten(LX - 14, [(L2(0, z)[1], t, L2(y, 0)[0]) for z, t, y in kl2], side='left', size=3.0)
    sh.dim_h(L1(0, 528), L1(SP_Y, 532), L1(0, 528)[1] + 6, '35', size=3.0)
    sh.dim_h(L1(25.5, 552), L1(44.5, 552), L1(0, 528)[1] + 13, 'Ø19 H7', size=3.0)
    sh.text(L1(46, 548), 'M6', 2.8)
    sh.text(L1(40.5, 600), 'Tr8×2', 2.8, rot=-90)
    sh.text(L2(41, 1210), 'Tr8×2', 2.8, rot=-90)
    sh.dim_h(L2(25, 1290), L2(45, 1290), L2(0, 1350)[1] - 3, 'Ø20', size=3.0)
    for n, t, pos in [(13, L1(0, 600), (LX - 2, 236)), (31, L1(15, 543.5), (LX + 92, 336)),
                      (32, L1(5, 534), (LX + 6, 343)),
                      (21, L1(48, 556), (LX + 92, 322)), (22, L1(41, 555), (LX + 92, 308)),
                      (25, L1(45, 564.5), (LX + 92, 294)), (24, L1(39, 567), (LX + 92, 280)),
                      (23, L1(40, 547), (LX + 78, 343)), (20, L1(39, 620), (LX + 92, 238)),
                      (19, L1(45, 610), (LX + 92, 252)), (18, L1(49, 590), (LX + 92, 266)),
                      (17, L1(10, b), (LX - 2, 250)), (33, L1(63.5, 625), (LX + 78, 236)),
                      (20, L2(35, 1200), (LX + 92, 196)), (26, L2(60, 1250), (LX + 92, 150)),
                      (22, L2(42, 1250), (LX + 92, 164)), (29, L2(62, 1270), (LX + 92, 136)),
                      (27, L2(45, 1265), (LX + 92, 122)), (28, L2(62, 1293), (LX + 92, 102)),
                      (30, L2(56, 1320), (LX + 92, 80))]:
        sh.balloon(pos, n, t, r=3.5, size=3.2)
    sh.mtext((LX + 72, 44), ['Y2 Loslager oben:', 'Außenring in Ø19 H7', 'axial frei; Kupplung', 'axial verschiebbar',
                             '⇒ keine Axiallast', 'auf Motorwelle (M3)'], size=2.8)
    sh.mtext((LX + 72, 350), ['Y1 Festlager unten: 2 × 626-2RS,', 'Innenringe zw. Hülse 24 und',
                              'Wellenmutter 23, Außenringe zw.', 'Bohrungsschulter und Ring 25.'], size=2.8)
    sh.text((LX + 50, 25), 'Einzelheiten Y1 / Y2 – Spindellagerung', 5, 'middle', weight='bold')
    sh.text((LX + 50, 31), 'Schnitt x = 0, M 1:1 (Stellung VERRIEGELT; AUF Strich-Zweipunkt)', 3.5, 'middle')

    # ------------------------------------------------------------ Schnitt B-B Fuehrungsnut M 1:1
    bx0, by0 = 50, 312
    B = lambda x, y: (bx0 + (x - 150), by0 - y)  # noqa: E731
    post_out = R(B, 215, 275, -30, 30)
    post_in = R(B, 218, 272, -27, 27)
    d = 'M' + ' L'.join(f'{f(p[0])},{f(p[1])}' for p in post_out) + ' Z M' + \
        ' L'.join(f'{f(p[0])},{f(p[1])}' for p in post_in) + ' Z'
    sh.raw(f'<path d="{d}" class="w" style="fill:url(#hA);fill-rule:evenodd"/>')
    sh.breakline_v(B(275, 0)[0] + 0.01, B(0, 30)[1], B(0, -30)[1], 0)
    sh.pl([B(*p) for p in [(211, -23), (215, -23), (215, 17), (175, 17), (175, 13), (211, 13)]], 'w',
          fill='url(#hB)')
    sh.pl([B(*p) for p in [(175, -13), (211, -13), (211, 13), (175, 13), (175, 3), (205, 3), (205, -3),
                           (175, -3)]], 'w', fill='url(#hK)')
    sh.pl(R(B, 150, 200, -2, 2), 'n', fill='#000')
    sh.breakline_v(B(150, 0)[0], B(0, 6)[1], B(0, -6)[1], 1.0)
    rect(B, 188, 192, 5, 17)
    rect(B, 186, 194, 17, 19.5)
    rect(B, 207, 224, -20, -16)
    rect(B, 207, 209.5, -22, -14)
    rect(B, 180, 210, 17.5, 30)
    sh.text(B(195, 22.3), 'B6', 3.0, 'middle')
    sh.line(B(180, 20), B(152, 20), 'c')
    sh.line(B(245, -36), B(245, 36), 'c')
    sh.line(B(213, 0), B(280, 0), 'c')
    sh.dim_h(B(175, 13), B(205, 3), B(0, 42)[1], '30')
    sh.dim_h(B(205, 3), B(211, 13), B(0, 42)[1], '6', size=3.0)
    sh.dim_h(B(215, 30), B(275, 30), B(0, 42)[1], '60')
    sh.dim_h(B(175, -13), B(200, -2), B(0, -36)[1], '25 Überdeckung', size=3.0)
    sh.dim_v(B(205, -3), B(205, 3), B(222, 0)[0] - 30, '6', size=3.0)
    sh.dim_v(B(175, -13), B(175, 13), B(165, 0)[0], '26', size=3.0)
    sh.text(B(205, -48), 'Nutgrund x = ±205, Spiel 5 je Seite', 2.8)
    for n, t, pos in [(7, B(272, 20), (B(290, 30))), (8, B(213, -20), B(232, -42)), (9, B(200, -9), B(185, -45)),
                      (13, B(160, 0), B(158, -22)), (48, B(205, 28), B(225, 50))]:
        sh.balloon(pos, n, t, r=3.5, size=3.2)
    caption(bx0 + 60, 372, 'Schnitt B–B (z = +300) – Führungsnut', 'M 1:1, rechte Seite (x > 0), Ansicht von oben')

    # ------------------------------------------------------------ Fundament / Schuerze / Zaun
    dx0, dy0 = 330, 272
    D = lambda x, y: (dx0 + x / 20, dy0 - y / 20)  # noqa: E731
    for s in (1, -1):
        sh.pl(R(D, s * 400, s * 1400, -1000, 0), 'h')
        sh.text(D(s * 900, -560), 'Schürze 2', 2.8, 'middle')
    sh.pl(R(D, -400, 400, -150, 150), 'w', fill='#fff')
    for s in (1, -1):
        rect(D, s * 215, s * 375, -80, 80, 'n')
        sh.pl(R(D, s * 215, s * 275, -30, 30), 'n', fill='#000')
        sh.circle(D(s * 355, 0), 1.5, 'w', fill='#000')
        sh.line(D(s * 385, 0), D(s * 1500, 0), 'w')
        sh.line(D(s * 275, 0), D(s * 325, 0), 'cut')
    sh.pl(R(D, -175, 175, -59, -9), 'n', fill='#000')
    sh.line(D(-1500, 0), D(1500, 0), 'c')
    sh.text(D(-1450, 60), 'Zaun (Bestand)', 2.8)
    sh.text(D(0, 330), 'Entenseite (+y, Nachtgehege)', 2.8, 'middle')
    sh.text(D(0, -1120), 'Raubtierseite (−y)', 2.8, 'middle')
    sh.dim_h(D(400, -1000), D(1400, -1000), D(0, -1000)[1] + 6, '≥ 1000', size=3.0)
    sh.dim_v(D(1400, 0), D(1400, -1000), D(1500, 0)[0] + 4, '1000', size=3.0)
    sh.dim_h(D(-400, 150), D(400, 150), D(0, 150)[1] - 4, '800', size=3.0)
    sh.dim_v(D(-400, 150), D(-400, -150), D(-400, 0)[0] - 4, '300', size=3.0)
    sh.leader_text(D(-300, 0), (D(-750, 360)), ['Spaltabdeckung 4, Abstand ≤ 100,', 'Restspalt ≤ 25'], size=2.8,
                   side='left', arrow=False, dot=True)
    for n, t, pos in [(1, D(150, -100), D(150, -420)), (3, D(355, 0), D(700, 330)), (4, D(300, 0), D(560, 420)),
                      (2, D(-900, -800), D(-1700, -800)), (5, D(-330, -60), D(-250, -420))]:
        sh.balloon(pos, n, t, r=3.5, size=3.2)
    caption(dx0, 343, 'Draufsicht Fundament, Schürze, Zaunanschluss', 'M 1:20 (ohne Antriebskasten)')

    fx0, fy0 = 492, 252
    F = lambda y, z: (fx0 + y / 20, fy0 + (1400 - z) / 20)  # noqa: E731
    sh.pl(R(F, -150, 150, -800, 0), 'w', fill='url(#hBeton)')
    sh.ground(F(-1150, 0)[0], F(-150, 0)[0], F(0, -20)[1])
    sh.ground(F(150, 0)[0], F(400, 0)[0], F(0, -20)[1])
    sh.line(F(-1000, -95), F(-150, -95), 'h')
    sh.pl(R(F, -30, 30, 10, 1140), 'n')
    sh.pl([F(-40, 1140), F(100, 1140), F(100, 1400), F(-40, 1375)], 'n')
    sh.pl([F(-59, 0), F(-9, 0), F(-9, 30), F(-13, 30), F(-13, 4), F(-59, 4)], 'n', fill='#000')
    sh.line(F(0, -830), F(0, 1420), 'c')
    sh.dim_v(F(-150, -800), F(-150, 0), F(-150, 0)[0] - 4, '800', size=3.0)
    sh.dim_v(F(150, -20), F(150, 0), F(150, 0)[0] + 5, '20', size=3.0)
    sh.dim_h(F(-150, -800), F(150, -800), F(0, -800)[1] + 5, '300', size=3.0)
    sh.dim_h(F(-1000, -95), F(-150, -95), F(0, -95)[1] + 7, '≥ 850 (1000 ab Zaun)', size=2.6)
    sh.leader_text(F(-950, -95), (F(-1250, -650)), ['Schürze 2 (hinter Schnitt,', '50…100 unter Gelände)'],
                   size=2.6, side='right', arrow=False, dot=True)
    caption(fx0 - 15, 378, 'Schnitt F–F (x = 0)', 'M 1:20, Fundament')

    # ------------------------------------------------------------ Hinweise
    notes = [
        ('b', 'Hinweise TZ-02'),
        ('', '1  Maße in mm; Höhen z bezogen auf OKF (z = 0). Allgemeintoleranz ISO 2768-m [A]. Positionsnummern = TZ_Positionsliste.csv.'),
        ('', '2  Mitnehmer (M1): Heben über OBERES Langlochende (Bolzen +645 bei ZU, +1195 bei AUF), Verriegeln über UNTERES (Bolzen +594, 1 über Langloch-'),
        ('', '   mitte unten). Freiweg 52. Abheben des Bolzens ≥ 3 vom oberen Ende ⇒ B8 meldet ⇒ Stopp beim Schließen (Ausnahme B1 aktiv).'),
        ('', '3  Klinke (M2): passiv, rastet in ZU ein; Entriegelung nur durch Mutterbewegung innerhalb des Freiwegs. Geometrie Klinke/Kulisse [A], Funktionsmuster.'),
        ('', '4  Spindel (M3): Festlager unten (axial geklemmt), Loslager oben (axial frei), Klauenkupplung mit Elastomerstern zum Motor; Spindel trocken, ohne Fett (M4).'),
        ('', '5  Führung: Nut 6 × 30, Schieber 4, Überdeckung 25, unten offen; PE-UHMW-Profil 9 einteilig [A]; Führungen parallel ±1 auf Länge.'),
        ('', '6  Fundament/Schürze/Zaun unverändert nach R1 (01_Mechanik Pos. 15–17): Beton C25/30 [A]; Schürze Masche ≤ 25, 1000 nach außen, beidseits ≥ 1000 entlang Zaun,'),
        ('', '   an Fundamentrand anschließen; Zaun mit eigenen Abspannpfosten ≤ 100 neben der Einheit, nur Spaltabdeckung (keine Krafteinleitung), Restspalt ≤ 25.'),
        ('', '7  Frosttiefe örtlich prüfen (T 800 ab OKF = 780 unter Gelände). Zaunhöhe unbekannt: Einheit darf nicht als Steighilfe wirken (Abstand/glatte Abdeckung).'),
        ('', '8  Kanten entgraten; Einzugs-/Scherstellen (Mutter/Langloch, Spindel) nur innerhalb der Einhausung (Sturzblende 33, Sicherheitsschrauben 34).'),
    ]
    yy = 400
    for kind, t in notes:
        if kind == 'b':
            sh.text((30, yy), t, 4.2, weight='bold')
            yy += 6
        else:
            sh.text((30, yy), t, 3.1)
            yy += 4.6
    sh.text((30, 18), 'ENTWURF – NICHT FÜR FERTIGUNG', 5, weight='bold', fill='#c00000')
    frame_and_title(sh, common_fields('TZ-02', 'Einzelheiten Mitnehmer, Klinke, Lagerung, Führung, Fundament',
                                      'siehe Ansicht', '2 / 2', 'A1 / 2 von 2'))
    return sh


def write_csv():
    p = os.path.join(OUT, 'TZ_Positionsliste.csv')
    with open(p, 'w', encoding='utf-8', newline='') as fh:
        fh.write('Pos;Benennung;Werkstoff;Abmessung;Menge\n')
        for pos, ben, wst, abm, m in POS:
            for v in (ben, wst, abm):
                assert ';' not in v
            fh.write(f'{pos};{ben};{wst};{abm};{m}\n')
    return p


def main():
    sh = tz01()
    with open(os.path.join(OUT, 'TZ-01_Gesamtansicht.svg'), 'w', encoding='utf-8') as fh:
        fh.write(sh.svg('TZ-01 Entenklappe DuckDoor – Gesamtansicht (Rev. A, Entwurf)',
                        'Vorderansicht und Schnitt A-A, M 1:5. Entwurf – nicht für Fertigung.'))
    if 'tz02' in globals():
        sh2 = globals()['tz02']()
        with open(os.path.join(OUT, 'TZ-02_Details.svg'), 'w', encoding='utf-8') as fh:
            fh.write(sh2.svg('TZ-02 Entenklappe DuckDoor – Einzelheiten (Rev. A, Entwurf)',
                             'Details Mitnehmer, Klinke, Spindellagerung, Führungsnut, Fundament.'))
    write_csv()


if __name__ == '__main__':
    main()
