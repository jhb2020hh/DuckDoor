"""Antrieb, Mitnehmer, Klinke, Sensorik – Entenklappe DuckDoor (Team „Antrieb“).

Zustand ZU_VERRIEGELT (Bolzen z = +594, OK Schieber +565).
Maße aus drawings/src/gen_tz.py (TZ-01/TZ-02) und Maßliste R2-11; [A] = Annahme.
Konvention der Zeichnung: u = -x (Klinkenseite liegt bei x < 0).
Alle Geometrien in globalen Koordinaten (siehe common.py).
"""
import cadquery as cq

from common import (Part, box, cyl_z, cyl_y, C_ALU, C_EDELSTAHL, C_KAUFTEIL,
                    C_KUNSTSTOFF_W, C_KUNSTSTOFF_S, C_GUMMI, C_WARN)

# ------------------------------------------------------------------ Kenngrößen (TZ / R2-11)
OK = 565            # OK Schieber ZU
UK = 30             # UK Schieber ZU
BZ = 594            # Bolzenmitte verriegelt
SL_U, SL_O = 28, 80  # Langlochmitte relativ OK
KERBE = 61          # Rastkerbe UK relativ OK [A, TZ-01 A5]
SP_Y = 35           # Spindelachse y (x = 0)

KL_P = (22, 670)    # Klinkendrehpunkt (u, z)
KL_POLY = [(14, 628), (18, 628), (18, 622), (26, 622), (26, 664), (60, 664), (60, 676), (18, 676), (18, 634),
           (14, 634)]
KL_LUG = (26, 32, 624, 638)
KL_HALTER = [(16, 665), (40, 665), (40, 545), (48, 545), (48, 678), (16, 678)]

# y-Ebenen Mitnehmerbereich [A] (A-A: Klinke/Halter y 6…14, Kulisse y 16…20)
Y_LAS = (2, 6)      # Lasche
Y_KL = (6, 10)      # Klinkenblech
Y_HA = (10, 14)     # Klinkenhalter
Y_KU = (16, 20)     # Kulissenebene

C_MAGNET = (0.6, 0.1, 0.1)


# ------------------------------------------------------------------ Helfer
def poly_xz(pts_xz, y0, y1):
    """Polygon in der x-z-Ebene (global), extrudiert von y0 bis y1."""
    return (cq.Workplane("XZ").polyline(pts_xz).close()
            .extrude(-(y1 - y0)).translate((0, y0, 0)))


def poly_uz(pts_uz, y0, y1):
    """Polygon in Zeichnungskoordinaten (u = -x, z)."""
    return poly_xz([(-u, z) for u, z in pts_uz], y0, y1)


def ring_z(x, y, z0, z1, d_out, d_in):
    return cyl_z(x, y, z0, z1, d_out).cut(cyl_z(x, y, z0 - 1, z1 + 1, d_in))


def cone_y(x, z, y0, h, r0, r1):
    s = cq.Solid.makeCone(r0, r1, h, cq.Vector(x, y0, z), cq.Vector(0, 1, 0))
    return cq.Workplane("XY").add(s)


def cyl_x(y, z, x0, x1, d):
    return cq.Workplane("YZ").circle(d / 2).extrude(x1 - x0).translate((x0, y, z))


def build() -> list[Part]:
    P = []

    def add(name, pos, shape, mat, group, color, kauf=False, note=""):
        P.append(Part(name, pos, shape, mat, group, color, kauf, note))

    # ============================================================== Schieber
    # Pos 13 Schieberblech x ±200, y -2…+2, z +30…+565; 2 Bohrungen Ø5,5 für Lasche
    sch = box(-200, 200, -2, 2, UK, OK)
    for xs in (-12, 12):
        sch = sch.cut(cyl_y(xs, OK - 7.5, -3, 3, 5.5))
    add("P13_Schieberblech", "13", sch, "EN AW-5754 H22", "SCHIEBER", C_ALU,
        note="400×535×4; 2× Ø5,5 für Pos 16 bei x ±12, z +557,5 (TZ-02 Z)")

    # Pos 14 Schaltleiste -B7: x ±170, y -6…+6, z +5…+30, Hohlkammer 7×17
    sl = box(-170, 170, -6, 6, 5, 30).cut(box(-171, 171, -3.5, 3.5, 9, 26))
    add("P14_Schaltleiste_B7", "14 / -B7", sl, "EPDM / Al-Träger (ASO SENTIR edge)", "KAUFTEIL", C_GUMMI,
        kauf=True, note="vereinfacht; L 340, B 12, H 25; Hohlkammer 7×17 nach TZ-01 A-A; "
                        "[A] Befestigung (C-Schiene) nicht modelliert")

    # Pos 15 Mitnehmerlasche (u-Koordinaten der Zeichnung)
    las_uz = [(-20, OK - 15), (18, OK - 15), (20, OK - 13), (20, OK + KERBE), (14, OK + KERBE),
              (14, OK + KERBE + 10), (20, OK + KERBE + 10), (20, OK + 95), (-20, OK + 95)]
    las = poly_uz(las_uz, *Y_LAS)
    zc1, zc2 = OK + SL_U, OK + SL_O
    slot = (box(-4.5, 4.5, 0, 8, zc1, zc2)
            .union(cyl_y(0, zc1, 0, 8, 9)).union(cyl_y(0, zc2, 0, 8, 9)))
    las = las.cut(slot)
    for xs in (-12, 12):
        las = las.cut(cyl_y(xs, OK - 7.5, 1, 7, 5.5)).cut(cone_y(xs, OK - 7.5, 3.2, 2.81, 2.75, 5.0))
    add("P15_Mitnehmerlasche", "15", las, "1.4404", "SCHIEBER", C_EDELSTAHL,
        note="110×40×4, y +2…+6, z +550…+660; Langloch 9 Mitten +593/+645 (Freiweg 52); "
             "Rastkerbe 6×10 UK +626 an x −20…−14 [A, TZ A5]; Fase 2×45° unten x −20; 2× Senkung 90° Ø10")

    # Pos 16 Senkschrauben M5×12 + Sicherungsmutter (vereinfacht)
    for i, xs in enumerate((12, -12), 1):
        s = (cyl_y(xs, OK - 7.5, -6, 3.2, 5.0)
             .union(cone_y(xs, OK - 7.5, 3.2, 2.8, 2.5, 5.0))
             .union(cyl_y(xs, OK - 7.5, -7, -2, 9.0)))
        add(f"P16_Senkschraube_{i}", "16", s, "A4-70", "SCHIEBER", C_EDELSTAHL,
            note="ISO 10642 M5×12 + DIN 985 M5 (vereinfacht: Schaft Ø5, Kopf-Kegel, Mutter Ø9×5 y −7…−2) [A]")

    # Pos 17 Mitnehmerbolzen Ø8 y 0…+20, Gewindezapfen M6 (Ø6) y +20…+28
    bol = cyl_y(0, BZ, 0, 20, 8).union(cyl_y(0, BZ, 20, 28, 6))
    add("P17_Mitnehmerbolzen", "17", bol, "1.4404", "ANTRIEB", C_EDELSTAHL,
        note="Ø8 h9 y 0…+20 + Zapfen M6 (als Ø6) y +20…+28, Gesamt 28 nach TZ-02 Y1 [A, TZ A4]")

    # ============================================================== Mutter / Spindel
    # Pos 18 Mutterblock x ±15, y +20…+50, z BZ-10…BZ+30
    mb = box(-15, 15, 20, 50, BZ - 10, BZ + 30)
    mb = mb.cut(cyl_z(0, SP_Y, BZ - 11, BZ + 8, 10))            # Spindeldurchgang Ø10
    mb = mb.cut(cyl_z(0, SP_Y, BZ + 8, BZ + 31, 22))            # Mutteraufnahme Ø22
    mb = mb.cut(cyl_y(0, BZ, 19, 28, 6))                        # Gewinde M6 für Bolzen (als Ø6)
    add("P18_Mutterblock", "18", mb, "EN AW-6082 T6", "ANTRIEB", C_ALU,
        note="30×30×40, z +584…+624; Bohrung Ø10 / Ø22×22, M6×8 für Bolzen; "
             "[A] Mutter-Axialsicherung und Befestigung Kulisse/Reed nicht modelliert")

    # Pos 19 Spindelmutter Ø22×22, z BZ+8…BZ+30
    add("P19_Spindelmutter", "19", ring_z(0, SP_Y, BZ + 8, BZ + 30, 22, 8), "iglidur (Gleitkunststoff) [A]",
        "ANTRIEB", C_KUNSTSTOFF_W, note="Tr8×2 als Bohrung Ø8 (kein Gewinde), Ø22×22 [A]")

    # Pos 20 Gewindespindel: Zapfen Ø6 z 540…570, Ø8 z 570…1240, Zapfen Ø6 z 1240…1275
    sp = (cyl_z(0, SP_Y, 540, 570, 6).union(cyl_z(0, SP_Y, 570, 1240, 8))
          .union(cyl_z(0, SP_Y, 1240, 1275, 6)))
    add("P20_Gewindespindel", "20", sp, "1.4301 gerollt [A]", "ANTRIEB", C_EDELSTAHL,
        note="Tr8×2 als Zylinder Ø8, L 735 (z +540…+1275); Zapfen Ø6 ×30 unten / ×35 oben")

    # Pos 21 Lagerbock Festlager
    lb = box(-20, 20, 20, 50, 545, 565).union(cyl_z(0, SP_Y, 535, 545, 22))
    lb = (lb.cut(cyl_z(0, SP_Y, 534, 552, 12))
          .cut(cyl_z(0, SP_Y, 552, 564, 19))
          .cut(cyl_z(0, SP_Y, 564, 566, 20)))
    add("P21_Lagerbock_Festlager", "21", lb, "EN AW-6082 T6", "ANTRIEB", C_ALU,
        note="40×30×20 (z +545…+565) + Zentrierbund Ø22×10 (z +535…+545, durch Traverse 31); "
             "Bohrung Ø12 / Ø19 H7 / Ringnut Ø20 [A]; [A] Schrauben zur Traverse nicht modelliert")

    # Pos 22 Rillenkugellager 626-2RS (6×19×6), 3 Stück
    for i, z0 in enumerate((552, 558, 1247), 1):
        add(f"P22_Rillenkugellager_{i}", "22", ring_z(0, SP_Y, z0, z0 + 6, 19, 6), "Wälzlagerstahl",
            "KAUFTEIL", C_KUNSTSTOFF_S, kauf=True,
            note=("Festlager unten" if i < 3 else "Loslager oben") + ", vereinfacht als Vollring 6×19×6")

    # Pos 23 Wellenmutter M6 + Sicherungsscheibe
    wm = ring_z(0, SP_Y, 546, 551, 11, 6).union(ring_z(0, SP_Y, 551, 552, 11, 6))
    add("P23_Wellenmutter", "23", wm, "A4", "ANTRIEB", C_EDELSTAHL,
        note="M6 (Ø11 vereinf.) z +546…+551 + Scheibe z +551…+552 [A: TZ zeigt +545…+551, "
             "um 1 angehoben, damit Innenring geklemmt]")

    # Pos 24 Distanzhülse Ø10/Ø6,1×6, z 564…570
    add("P24_Distanzhuelse", "24", ring_z(0, SP_Y, 564, 570, 10, 6.1), "1.4301", "ANTRIEB", C_EDELSTAHL)

    # Pos 25 Sicherungsring DIN 472 19×1 in Nut Ø20, z 564…565
    add("P25_Sicherungsring", "25", ring_z(0, SP_Y, 564, 565, 20, 16), "Federstahl", "ANTRIEB", C_KUNSTSTOFF_S,
        note="vereinfacht als Ring Ø20/Ø16×1 [A]")

    # Pos 26 Lagerplatte Loslager x ±60, y +5…+65, z 1245…1255
    lp = box(-60, 60, 5, 65, 1245, 1255).cut(cyl_z(0, SP_Y, 1244, 1256, 19))
    add("P26_Lagerplatte_Loslager", "26", lp, "EN AW-5754", "ANTRIEB", C_ALU,
        note="120×60×10, Ø19 H7; [A] M4-Gewinde für Pos 29 nicht modelliert; "
             "[A] Integration: Befestigung im Kasten (35) über Haltewinkel 26a")

    # Pos 26a Haltewinkel Lagerplatte [A, Integration]: Z-Kantteil t 3, Fuß auf Kastenboden
    # (y +68…+96, außerhalb Bodenöffnung y −3…+65), Steg y +65…+68, Kopf unter Lagerplatte.
    for side, sx in (("links", 1), ("rechts", -1)):
        x0, x1 = sorted((sx * 32, sx * 60))
        hw = (box(x0, x1, 65, 96, 1142, 1145)          # Fuß auf Kastenboden (OK Boden +1142)
              .union(box(x0, x1, 65, 68, 1145, 1242))  # Steg
              .union(box(x0, x1, 45, 68, 1242, 1245)))  # Kopf unter Lagerplatte 26
        hw = hw.cut(cyl_z(sx * 46, 82, 1141, 1146, 4.5)).cut(cyl_z(sx * 46, 55, 1241, 1246, 4.5))
        add(f"P26a_Haltewinkel_Lagerplatte_{side}", "26a", hw, "EN AW-5754", "ANTRIEB", C_ALU,
            note="[A] Integration (neu): Z-Kantteil t 3, B 28, x ±32…±60; Fuß auf Kastenboden 35 "
                 "(y +65…+96), Kopf y +45…+68 unter Lagerplatte 26; je 1× Ø4,5 für M4 (Boden: "
                 "Blindnietmutter, Lagerplatte: Gewinde M4) – Schrauben nicht modelliert")

    # Pos 27 Klauenkupplung Ø20×30, z 1260…1290
    ku = (cyl_z(0, SP_Y, 1260, 1272, 20).union(cyl_z(0, SP_Y, 1272, 1278, 18))
          .union(cyl_z(0, SP_Y, 1278, 1290, 20)))
    ku = ku.cut(cyl_z(0, SP_Y, 1259, 1276, 6)).cut(cyl_z(0, SP_Y, 1276, 1291, 5))
    add("P27_Klauenkupplung", "27", ku, "Al / Elastomer 92 Sh A", "ANTRIEB", C_ALU,
        note="Naben Ø20×12, Stern Ø18×6 [A]; Bohrung 6 (unten) / 5 (oben)")

    # Pos 28 Motorplatte x ±60, y +5…+65, z 1291…1295
    mp = box(-60, 60, 5, 65, 1291, 1295).cut(cyl_z(0, SP_Y, 1290, 1296, 22))
    for dx in (-15.5, 15.5):
        for dy in (-15.5, 15.5):
            mp = mp.cut(cyl_z(dx, SP_Y + dy, 1290, 1296, 3.4))
    add("P28_Motorplatte", "28", mp, "EN AW-5754", "ANTRIEB", C_ALU,
        note="120×60×4, Zentrierung Ø22, 4× Ø3,4 Lochbild 31 [A]")

    # Pos 29 Distanzbolzen M4×36 (als Ø6), x ±50, y +8 / +62, z 1255…1291
    i = 0
    for dx in (-50, 50):
        for yy in (8, 62):
            i += 1
            add(f"P29_Distanzbolzen_{i}", "29", cyl_z(dx, yy, 1255, 1291, 6), "A4", "ANTRIEB", C_EDELSTAHL,
                note="M4×36, vereinfacht Ø6 ohne Gewinde [A]")

    # Pos 30 Schrittmotor NEMA 17: Körper z 1295…1343, Zentrierbund Ø22×2, Welle Ø5 z 1280…1293
    mo = (box(-21, 21, SP_Y - 21, SP_Y + 21, 1295, 1343).edges("|Z").chamfer(3.5)
          .union(cyl_z(0, SP_Y, 1293, 1295, 22))
          .union(cyl_z(0, SP_Y, 1280, 1293, 5)))
    for dx in (-15.5, 15.5):
        for dy in (-15.5, 15.5):
            mo = mo.cut(cyl_z(dx, SP_Y + dy, 1295, 1299.5, 3.0))
    add("P30_Schrittmotor_M1", "30 / -M1", mo, "–", "KAUFTEIL", C_KUNSTSTOFF_S, kauf=True,
        note="NEMA 17 42×42×48, Welle Ø5 nach unten (13 frei), Flansch-Bohrbild 31 (M3 als Ø3×4,5) "
             "[A]; Motorschrauben M3 nicht modelliert")

    # ============================================================== Klinke
    kl = poly_uz(KL_POLY, *Y_KL)
    kl = kl.union(poly_uz([(14, 628), (18, 628), (18, 634), (14, 634)], Y_LAS[0], Y_KL[0]))   # Zahn in Laschenebene
    u0, u1, z0, z1 = KL_LUG
    kl = kl.union(box(-u1, -u0, Y_KL[0], Y_KU[1], z0, z1))                                    # Lug bis Kulissenebene
    kl = kl.cut(cyl_y(-KL_P[0], KL_P[1], Y_KL[0] - 1, Y_KL[1] + 1, 6))
    add("P39_Schwerkraftklinke", "39", kl, "1.4404", "ANTRIEB", C_EDELSTAHL,
        note="t 4 (y +6…+10), 46×54 nach TZ KL_POLY; Zahn 4×6 nach y +2…+6 abgesetzt, Lug 6×14 "
             "bis y +20 (Kulissenebene) [A]; Drehpunkt x −22, z +670")

    add("P40_Klinkenachse", "40",
        cyl_y(-KL_P[0], KL_P[1], Y_KL[0], Y_HA[1], 6).union(cyl_y(-KL_P[0], KL_P[1], Y_HA[1], 15.5, 9)),
        "A4", "ANTRIEB", C_EDELSTAHL,
        note="[A] Ø6 nur y +6…+14 + Kopf Ø9×1,5: Ø6×20 passt nicht zwischen Lasche (y 6) und "
             "Kulissenebene (y 16); Sicherung offen")

    ha = poly_uz(KL_HALTER, *Y_HA).union(box(-52, -44, Y_KL[0], Y_HA[1], 660, 664))
    ha = ha.cut(cyl_y(-KL_P[0], KL_P[1], Y_HA[0] - 1, Y_HA[1] + 1, 6))
    add("P41_Klinkenhalter", "41", ha, "1.4404", "ANTRIEB", C_EDELSTAHL,
        note="Flach 8×4 x −48…−40, y +10…+14, z +545…+678 (steht auf Traverse 31) + Arm + "
             "Anschlag 8×8×4 unter Klinkenarm (z +660…+664) [A]")

    t = BZ + 7
    b = t - 40
    kul_uz = [(15, t), (26, t), (34, t - 8), (34, b + 8), (26, b), (15, b)]
    kul = poly_uz(kul_uz, *Y_KU).union(box(-19, -15, 20, 40, BZ - 10, t))
    add("P42_Entriegelungskulisse", "42", kul, "1.4404", "ANTRIEB", C_EDELSTAHL,
        note="t 4, 19×40, Schrägen 8×45°, y +16…+20, z +561…+601; Befestigungsschenkel "
             "4×20 an Mutterblock-Seite x −15 [A]")

    # ============================================================== Sensorik (Kaufteile vereinfacht)
    M12 = 12.0
    add("P43_Endschalter_B1", "43 / -B1", cyl_y(195, 32, 17.5, 67.5, M12), "Kaufteil", "ELEKTRO", C_KAUFTEIL,
        kauf=True, note="[A] induktiv M12×50 PNP (EL R2-12), x +195, z +32, Achse y ab +17,5 "
                        "(TZ: x +180…+210, z +24…+40); Bedämpfung/Target offen")
    add("P44_Endschalter_B2", "44 / -B2", cyl_y(-162, 1102, 4, 54, M12), "Kaufteil", "ELEKTRO", C_KAUFTEIL,
        kauf=True, note="[A] induktiv M12×50, im Kanal x −162, z +1102, Stirnfläche y +4 (2 vor Schieber); "
                        "TZ x −180…−210 läge in Kanalwange 10; Halter nicht modelliert")
    add("P45_Endschalter_B3", "45 / -B3", cyl_x(SP_Y, 1230, 18, 68, M12), "Kaufteil", "ELEKTRO", C_KAUFTEIL,
        kauf=True, note="[A] induktiv M12×50, Achse x, Stirn x +18 (3 zum Mutterblock), z +1230 "
                        "(TZ +1230…+1244, abgesenkt für Schaltpunkt Bolzen +1200)")
    add("P46_Endschalter_B4", "46 / -B4", cyl_x(SP_Y, 586, 18, 68, M12), "Kaufteil", "ELEKTRO", C_KAUFTEIL,
        kauf=True, note="[A] induktiv M12×50, Achse x, Stirn x +18, z +586 (TZ +566…+584 läge "
                        "unter dem Block, kein Target); Schaltpunkt Bolzen ≈ +594…+596")
    add("P47_Schlaffschalter_B8_Reed", "47 / -B8", box(10, 15, 14.5, 20, BZ + 0, BZ + 18), "Kaufteil",
        "ELEKTRO", C_KAUFTEIL, kauf=True,
        note="[A] Reedkontakt 5×5,5×18 an Mutterblock-Vorderseite (y 20), x +10…+15; "
             "fluchtet mit Magnet bei Bolzen am oberen Langlochende")
    add("P47_Schlaffschalter_B8_Magnet", "47 / -B8", box(8, 14, Y_LAS[1], 10, OK + 86, OK + 92), "Kaufteil",
        "ELEKTRO", C_MAGNET, kauf=True, note="[A] Betätigungsmagnet 6×4×6 auf Lasche, x +8…+14, z +651…+657")

    for z in (100, 300):
        for side, x0, x1 in (("Sender", 180, 210), ("Empfaenger", -210, -180)):
            add(f"P48_Lichtschranke_B6_{side}_z{z}", "48 / -B6", box(x0, x1, 17.5, 30, z - 8, z + 8),
                "Marantec 99165", "ELEKTRO", C_WARN, kauf=True,
                note=f"[A] Gehäuse 30×12,5×16 auf Führungsträger 8 (y +17,5…+30), Strahl z +{z}, y +20; "
                     "Seitenzuordnung Sender/Empfänger [A]; Befestigungsschraube nicht modelliert")
    return P
