"""Team „Gestell“: Gründung, Gestell, Führung, Kanal/Kasten, Schaltkasten =DD+K1.

Maße aus drawings/src/gen_tz.py (TZ-01 Vorderansicht/Schnitt A-A, TZ-02 Schnitt B-B,
Draufsicht Fundament, Schnitt F-F) und Maßliste R2-11 (docs/review/11_R2_Mechanik_Sicherheit.md).
Geometrie in globalen Koordinaten (siehe common.py), Zustand ZU_VERRIEGELT.

Seitenbezeichnung [A]: „links“ = +x, „rechts“ = −x, wie in der Vorderansicht TZ-01
(Blick von der Entenseite +y, x nach links aufgetragen).

Nicht modelliert (Team „Antrieb“ bzw. bauseits): Pos 3, 13–30, 39–48, Schaltleiste B7.
Freiraum: Nut der Führung (x ±175…±205, y ±3), Kanal y +8…+62 / z +545…+1140
(Spindel y 35, Mutterblock, Lasche), Kasteninnenraum, Durchtritt Bürstendichtung x ±25.
"""
import math

import cadquery as cq

from common import (Part, box, cyl_z, cyl_y, C_BETON, C_STAHL_VZ, C_ALU, C_EDELSTAHL,
                    C_KUNSTSTOFF_W, C_KUNSTSTOFF_S, C_GUMMI, C_KAUFTEIL, C_WARN)

# ------------------------------------------------------------------ Hauptmaße (TZ-01/R2-11)
Z_TOP = 1140                       # OK Pfosten/Führung, UK Antriebskasten
X_POST_I, X_POST_A = 215, 275      # Pfosten x ±215…±275 (Mitte ±245)
KASTEN_Y0, KASTEN_Y1 = -40, 100    # Antriebskasten y
T_BLECH = 2


def zt(y):
    """OK Kastendeckel (A9): +1375 bei y = −40, +1400 bei y = +100 (≈ 10,1° fallend zur −y-Seite)."""
    return 1375 + (y + 40) / 140 * 25


def prism_yz(pts, x0, x1):
    """Prisma aus Profil (y, z) entlang x von x0 bis x1."""
    return (cq.Workplane("YZ").polyline(pts).close().extrude(x1 - x0)
            .translate((x0, 0, 0)))


def prism_xy(pts, z0, z1):
    """Prisma aus Profil (x, y) entlang z von z0 bis z1."""
    return cq.Workplane("XY").polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0))


SIDES = ((1, "links"), (-1, "rechts"))   # links = +x, rechts = −x [A]


def build() -> list[Part]:
    P = []

    # ============================================================ GRUENDUNG
    # Pos 6 Ankerpositionen: Lochbild 110 × 110 bei x ±240 / ±350, y ±55
    anchors = [(s * xx, yy) for s, _ in SIDES for xx in (240, 350) for yy in (-55, 55)]
    SETZ = 110  # Setztiefe [A]

    fund = box(-400, 400, -150, 150, -800, 0)
    for (ax, ay) in anchors:
        fund = fund.cut(cyl_z(ax, ay, -SETZ, 0, 14))
    P.append(Part("P01_Streifenfundament", "1", fund, "Beton C25/30 [A]", "GRUENDUNG", C_BETON,
                  note="800 × 300 × 800, OK = OKF ±0 (+20 über Gelände). [A] Bohrlöcher Ø14 × 110 "
                       "für Verbundanker modelliert."))

    # Pos 2 Schürze: x ±400…±1400, y 0…−1000 (Raubtierseite), z −95 (Mitte), t 2 vereinfacht
    for s, side in SIDES:
        x0, x1 = sorted((s * 400, s * 1400))
        P.append(Part(f"P02_Schuerze_{side}_vereinfacht", "2", box(x0, x1, -1000, 0, -96, -94),
                      "Schweißgitter fvz, Masche ≤ 25 × 25, Draht ≥ 2,0", "GRUENDUNG", C_STAHL_VZ,
                      note="vereinfacht als Vollplatte t 2 (Gitter nicht modelliert); z −95 = 75 unter "
                           "Gelände (Soll 50…100); [A] seitlich neben Fundament x ±400…±1400, "
                           "1000 nach außen (−y) lt. Draufsicht TZ-02."))

    # Pos 5 Fußplatten 160 × 160 × 10, außermittig x ±215…±375 (A2)
    for s, side in SIDES:
        x0, x1 = sorted((s * X_POST_I, s * 375))
        fp = box(x0, x1, -80, 80, 0, 10)
        for xx in (240, 350):
            for yy in (-55, 55):
                fp = fp.cut(cyl_z(s * xx, yy, -1, 11, 14))
        P.append(Part(f"P05_Fussplatte_{side}", "5", fp, "S235JR feuerverzinkt", "GRUENDUNG",
                      C_STAHL_VZ, note="160 × 160 × 10, 4 × Ø14, Lochbild 110 × 110, außermittig (A2)."))

    # Pos 6 Verbundanker M12 (vereinfacht: Stange Ø12 z −110…+26, Mutter+Scheibe Ø19 z +10…+20)
    i = 0
    for (ax, ay) in anchors:
        i += 1
        a = cyl_z(ax, ay, -SETZ, 26, 12).union(cyl_z(ax, ay, 10, 20, 19))
        side = "links" if ax > 0 else "rechts"
        P.append(Part(f"P06_Verbundanker_{side}_{i}", "6", a, "A4-70", "GRUENDUNG", C_EDELSTAHL,
                      kaufteil=True, note="vereinfacht Zylinder M12 (Ø12) + Scheibe/Mutter Ø19 × 10; "
                                          "[A] Setztiefe 110, Überstand bis +26 lt. TZ-01."))

    # ============================================================ GESTELL
    # Pos 7 Pfosten □60×60×3, z +10…+1140, hohl
    for s, side in SIDES:
        x0, x1 = sorted((s * X_POST_I, s * X_POST_A))
        tube = box(x0, x1, -30, 30, 10, Z_TOP).cut(box(x0 + 3, x1 - 3, -27, 27, 9, Z_TOP + 1))
        P.append(Part(f"P07_Pfosten_{side}", "7", tube, "S235JRH feuerverzinkt", "GESTELL", C_STAHL_VZ,
                      note="Quadratrohr 60 × 60 × 3, L 1130 (z +10…+1140), x-Mitte ±245; oben durch "
                           "Kastenboden abgedeckt."))

    # Pos 4 Spaltabdeckung Zaunanschluss: an Pfosten-Außenfläche, Zaunebene y = 0
    for s, side in SIDES:
        x0, x1 = sorted((s * X_POST_A, s * (X_POST_A + 60)))
        P.append(Part(f"P04_Spaltabdeckung_{side}", "4", box(x0, x1, -1.5, 1.5, 10, Z_TOP),
                      "Lochblech fvz", "GESTELL", C_STAHL_VZ,
                      note="[A] als Blech t 3, 60 × 1130 in Zaunebene y = 0, x ±275…±335 (Restspalt bis "
                           "Abspannpfosten x ±355 ≤ 25); Lochung/Verschraubung nicht modelliert."))

    # Pos 49 PA-Anschlussfahne x ±275…±292, z +60…+80
    for s, side in SIDES:
        x0, x1 = sorted((s * X_POST_A, s * (X_POST_A + 17)))
        fa = box(x0, x1, 20, 24, 60, 80).cut(cyl_y(s * 284, 70, 19, 25, 9))
        P.append(Part(f"P49_PA_Fahne_{side}", "49", fa, "A4", "GESTELL", C_EDELSTAHL,
                      note="Flach 17 × 20 × 4 mit Loch Ø9 für M8; [A] Lage y +20…+24 (Zeichnung gibt y "
                           "nicht an; außerhalb Spaltabdeckung)."))

    # ============================================================ FUEHRUNG
    for s, side in SIDES:
        # Pos 8 Führungsträger Winkel 40×40×4 (Schnitt B-B)
        wk = [(211, -23), (215, -23), (215, 17), (175, 17), (175, 13), (211, 13)]
        P.append(Part(f"P08_Fuehrungstraeger_{side}", "8", prism_xy([(s * x, y) for x, y in wk], 0, Z_TOP),
                      "EN AW-6060 T66", "FUEHRUNG", C_ALU,
                      note="Winkel 40 × 40 × 4, L 1140 (z 0…+1140). Halter B6 (Team Antrieb) nicht enthalten."))
        # Pos 9 Führungsprofil 36 × 26 mit Nut 6 × 30 (Nutgrund x ±205)
        pr = [(175, -13), (211, -13), (211, 13), (175, 13), (175, 3), (205, 3), (205, -3), (175, -3)]
        P.append(Part(f"P09_Fuehrungsprofil_{side}", "9", prism_xy([(s * x, y) for x, y in pr], 0, Z_TOP),
                      "PE-UHMW", "FUEHRUNG", C_KUNSTSTOFF_W,
                      note="36 × 26, Nut 6 × 30, Nutgrund x ±205, L 1140, unten offen."))
        # Pos 10 Kanalwange z +545…+1140: Steg x ±211…±215 (y +17…+62), Schenkel y +58…+62
        kw = box(*sorted((s * 211, s * 215)), 17, 62, 545, Z_TOP).union(
            box(*sorted((s * 175, s * 211)), 58, 62, 545, Z_TOP))
        for zz in (600, 780, 960, 1110):
            kw = kw.cut(cyl_y(s * 195, zz, 57, 63, 5))
        P.append(Part(f"P10_Kanalwange_{side}", "10", kw, "EN AW-5754", "FUEHRUNG", C_ALU,
                      note="[A] Kantprofil 45 × 40 × 4 (Liste: 48 × 40): Sturzblende y +62…+65 schließt "
                           "außen an; Bohrungen Ø5 für Sicherheitsschrauben (34)."))

    # Pos 11 Schwellenwinkel 50 × 30 × 4, L 350 (A1), OK +30
    sw = [(-59, 0), (-9, 0), (-9, 30), (-13, 30), (-13, 4), (-59, 4)]
    P.append(Part("P11_Schwellenwinkel", "11", prism_yz(sw, -175, 175), "EN AW-6060", "FUEHRUNG", C_ALU,
                  note="Winkel 50 × 30 × 4, L 350 (A1), y −59…−9, OK +30."))
    # Pos 12 Gummipuffer 16 × 5, L 350
    P.append(Part("P12_Gummipuffer", "12", box(-175, 175, -8, 8, 0, 5), "EPDM 60 Shore A [A]", "FUEHRUNG",
                  C_GUMMI, note="16 × 5, L 350, z 0…+5."))

    # ============================================================ KANAL / KASTEN
    # Pos 31 Traverse: Kantteil t 3, 57 × 15, y +8…+65, z +530…+545
    tv = prism_yz([(8, 530), (11, 530), (11, 542), (65, 542), (65, 545), (8, 545)], -215, 215)
    for s, _ in SIDES:
        tv = tv.cut(box(*sorted((s * 175, s * 216)), -24, 17, 520, 550))   # Ausklinkung Führung
    tv = tv.cut(cyl_z(0, 35, 540, 546, 22))      # Durchgang Zentrierbund Lagerbock (21)
    tv = tv.cut(cyl_z(100, 40, 540, 546, 6))     # Ablauf Ø6
    P.append(Part("P31_Traverse", "31", tv, "EN AW-5754", "KASTEN", C_ALU,
                  note="Kantteil t 3, 57 × 15, L 430. [A] Ausklinkung x ±175…±215 / y < +17 (Führung), "
                       "Bohrung Ø22 für Zentrierbund Lagerbock bei (0, 35), Ablauf Ø6 bei x +100, y +40."))
    # Pos 32 Abstreiflippe y +2…+8, z +530…+538
    P.append(Part("P32_Abstreiflippe", "32", box(-175, 175, 2, 8, 530, 538), "EPDM", "KASTEN", C_GUMMI,
                  note="6 × 8; [A] L 350 statt 400 (bei x > ±175 Kollision mit Führungsprofil). "
                       "Liegt an Schieber (y +2) an."))
    # Pos 33 Sturzblende x ±215, y +62…+65
    sb = box(-215, 215, 62, 65, 545, Z_TOP)
    for s, _ in SIDES:
        for zz in (600, 780, 960, 1110):
            sb = sb.cut(cyl_y(s * 195, zz, 61, 66, 5))
    P.append(Part("P33_Sturzblende", "33", sb, "EN AW-5754", "KASTEN", C_ALU,
                  note="t 3, x ±215. [A] z +545…+1140 (H 595) wie Schnitt A-A/Y1; Positionsliste nennt "
                       "610 (ab +530) – kollidiert mit Traverse y +62…+65. 8 Bohrungen Ø5."))
    # Pos 34 Sicherheitsschrauben (8 Stk. Sturzblende), vereinfacht
    k = 0
    for s, side in SIDES:
        for zz in (600, 780, 960, 1110):
            k += 1
            sc = cyl_y(s * 195, zz, 52, 65, 5).union(cyl_y(s * 195, zz, 65, 68, 8.5))
            P.append(Part(f"P34_Sicherheitsschraube_{side}_z{zz}", "34", sc, "A4", "KASTEN", C_EDELSTAHL,
                          kaufteil=True, note="vereinfacht: Schaft Ø5 × 13, Kopf Ø8,5 × 3 (M5 × 10 Torx mit "
                                              "Stift); Gegenmutter/Einnietmutter nicht modelliert. "
                                              "4 Schrauben Deckel nicht modelliert."))

    # Pos 35 Antriebskasten t 2, außen 550 × 140 × 260, oben offen, Boden mit Kanalöffnung
    outer = prism_yz([(KASTEN_Y0, Z_TOP), (KASTEN_Y1, Z_TOP), (KASTEN_Y1, zt(KASTEN_Y1) - T_BLECH),
                      (KASTEN_Y0, zt(KASTEN_Y0) - T_BLECH)], -275, 275)
    inner = box(-273, 273, KASTEN_Y0 + T_BLECH, KASTEN_Y1 - T_BLECH, Z_TOP + T_BLECH, 1500)
    ks = outer.cut(inner)
    ks = ks.cut(box(-215, 215, -3, 65, Z_TOP - 1, Z_TOP + T_BLECH + 1))   # Kanalöffnung
    ks = ks.cut(cyl_y(-230, 1180, KASTEN_Y1 - 3, KASTEN_Y1 + 1, 12))       # Bohrung DAE
    P.append(Part("P35_Antriebskasten", "35", ks, "EN AW-5754", "KASTEN", C_ALU,
                  note="Blech t 2, außen 550 × 140 (y −40…+100) × 235…260, z +1140…OK schräg (Deckelauflage "
                       "zt−2). Bodenöffnung x ±215, y −3…+65 (Kanal, Bürstendichtung). Bohrung Ø12 für DAE."))
    # Pos 36 Kastendeckel ≈ 560 × 150, ≈ 10,1° fallend zur −y-Seite, OK +1375/+1400
    ya, yb = KASTEN_Y0 - 5, KASTEN_Y1 + 5
    dk = prism_yz([(ya, zt(ya) - T_BLECH), (yb, zt(yb) - T_BLECH), (yb, zt(yb)), (ya, zt(ya))], -280, 280)
    P.append(Part("P36_Kastendeckel", "36", dk, "EN AW-5754", "KASTEN", C_ALU,
                  note=f"t 2 (senkrecht gemessen), 560 × 150 (Grundriss), Neigung "
                       f"{math.degrees(math.atan(25 / 140)):.1f}° zur −y-Seite; [A] Überstand 5 je Seite, "
                       "Abkantung/Tropfkante und Lichtfenster nicht modelliert."))
    # Pos 37 Druckausgleichselement M12 × 1,5 auf Entenseite (x −230, z +1180)
    dae = (cyl_y(-230, 1180, 94, 100, 12).union(cyl_y(-230, 1180, 94, 98, 18))
           .union(cyl_y(-230, 1180, 100, 106, 20)))
    P.append(Part("P37_Druckausgleichselement", "37", dae, "PA / ePTFE", "KAUFTEIL", C_KUNSTSTOFF_S,
                  kaufteil=True, note="vereinfacht: Kopf Ø20 × 6 außen, Gewinde M12, Mutter Ø18 innen [A]."))
    # Pos 38 Bürstendichtung im Bodenausschnitt, Durchtritt x ±25 offen (A10)
    bd = box(-215, -25, -3, 65, Z_TOP, Z_TOP + 6).union(box(25, 215, -3, 65, Z_TOP, Z_TOP + 6))
    P.append(Part("P38_Buerstendichtung", "38", bd, "PA-Borste, Al-Träger", "KAUFTEIL", C_KUNSTSTOFF_S,
                  kaufteil=True, note="vereinfacht als Hüllkörper z +1140…+1146; [A] Durchtritt "
                                      "Lasche/Mutterblock/Spindel x ±25 offen (A10)."))
    # Pos 50 Warnschilder 100 × 100
    P.append(Part("P50_Warnschild_Entenseite", "50", box(110, 210, KASTEN_Y1, KASTEN_Y1 + 1.5, 1230, 1330),
                  "Kunststoff UV-beständig", "KASTEN", C_WARN,
                  note="100 × 100 × 1,5 [A] auf Kastenfront +y, x +110…+210, z +1230…+1330 lt. TZ-01."))
    P.append(Part("P50_Warnschild_Raubtierseite", "50",
                  box(110, 210, KASTEN_Y0 - 1.5, KASTEN_Y0, 1230, 1330), "Kunststoff UV-beständig", "KASTEN",
                  C_WARN, note="[A] 2. Schild auf Kastenrückseite −y (Lage nicht gezeichnet)."))

    # ============================================================ ELEKTRO: Schaltkasten =DD+K1-U1
    # BOM Pos 520: PC IP66 ≈ 400 × 300 × 210 (H × B × T), z. B. Fibox ARCA 403021
    k1 = box(-475, -175, -30 - 210, -30, 600, 1000).edges("|Y").fillet(8)
    P.append(Part("K1_U1_Schaltkasten", "=DD+K1-U1", k1, "PC, IP66", "ELEKTRO", C_KAUFTEIL, kaufteil=True,
                  note="Hüllkörper 400 × 300 × 210 (H × B × T) lt. BOM 520. [A] Montageort: Pfosten rechts "
                       "(x −245), Raubtierseite (Rückwand an y −30), x −475…−175 (Kante bündig "
                       "Lichtöffnung), z +600…+1000; Halter/Mastschellen (BOM 490), Verschraubungen, "
                       "Deckelfenster B5 und Taster S1/S2 nicht modelliert."))
    return P
