"""EL-01 Einlinienschema 230 V / 24 V – Entenklappe DuckDoor (=DD). Erzeugt ../EL-01_Single-Line.svg"""
import os
from svglib import Svg

OUT = os.path.join(os.path.dirname(__file__), "..", "EL-01_Single-Line.svg")
s = Svg(title="EL-01 Einlinienschema DuckDoor")

Y = 150  # Hauptlinie 230 V

# ---------------- +UV Bestand ----------------
s.rect(40, 40, 410, 215, "bestbox")
s.text(48, 58, "=DD+UV  Bestandsunterverteilung", 12, bold=True)
s.text(48, 73, "Bestand – nicht im Lieferumfang, Werte nachweisen", 10, cls="grey")
s.text(48, 90, "L/N/PE 230 V 50 Hz, TN-S [A]", 10)
s.line(40, Y, 95, Y, "best")
s.tick(70, Y, 3)
s.switch_h(95, Y, "ls", "best", actuator="IΔ")
s.raw(f'<ellipse cx="105" cy="{Y}" rx="5" ry="12" class="sig"/>')  # Summenstromwandler
s.mtext(130, Y + 28, ["-F0", "RCD 30 mA Typ A", "(Bestand, nachweisen)"], 10.5, 13, "middle", True)
s.line(165, Y, 250, Y, "best")
s.switch_h(250, Y, "ls", "best", actuator="I>")
s.mtext(285, Y + 28, ["-F01", "LS B16/B10, ≥ 6 kA", "(Bestand)"], 10.5, 13, "middle", True)
s.line(320, Y, 450, Y, "best")
s.mtext(48, 232, ["SPD Typ 2 in +UV prüfen (DIN VDE 0100-443) [N-verif.]",
                  "Schleifenimpedanz / RCD-Auslösung messen (VDE 0100-600)"], 9.5, 12, cls="grey")

# ---------------- Zuleitung -W1 ----------------
s.line(450, Y, 620, Y, "p230")
s.tick(472, Y, 3)
s.text(530, Y - 24, "-W1", 12, "middle", bold=True)
s.text(530, Y - 10, "NYY-J 3×1,5 mm²", 10.5, "middle")
s.mtext(530, Y + 18, ["Erdreich ≥ 0,6 m [A]", "Schutzrohr Austritt", "Länge offen [A]"], 9.5, 12, "middle")

# ---------------- +K1 Ortsgrenze ----------------
s.polygon([(585, 36), (1648, 36), (1648, 800), (140, 800), (140, 268), (585, 268)], "loc")
s.text(594, 52, "=DD+K1  Schaltkasten am Pfosten (PC/GFK, IP66 [A], beheizt)", 12, bold=True)

# -X1
s.terminal(625, Y)
s.mtext(625, Y + 26, ["-X1:1,2,PE", "Einspeisung"], 10, 12, "middle")
# PE-Abzweig nach oben zur PE-Schiene
s.line(625, Y - 4, 625, 78, "pe")
s.line(625, 78, 1270, 78, "pe")
s.text(632, 92, "PE", 10, cls="peT")
s.line(629, Y, 690, Y, "p230")
s.tick(655, Y, 2)
# -Q1
s.switch_h(690, Y, "trenn", "p230")
s.line(725, Y - 9, 725, Y - 40, "mech")
s.handle_lock(725, Y - 40)
s.mtext(725, Y + 26, ["-Q1", "Reparaturschalter", "2-pol., ≥ 16 A [A]", "abschließbar"], 10, 12, "middle", True)
s.line(760, Y, 820, Y, "p230")
# -F1
s.switch_h(820, Y, "ls", "p230", actuator="I>")
s.mtext(855, Y + 26, ["-F1", "LS B6 1P+N", "≥ 6 kA, EN 60898-1", "(C6 falls Inrush [verif.])"], 10, 12, "middle", True)
s.line(890, Y, 960, Y, "p230")
s.terminal(960, Y)
s.mtext(960, Y + 26, ["-X1:3,4", "L', N'"], 10, 12, "middle")
s.line(964, Y, 1050, Y, "p230")
s.text(1024, Y - 10, "H07V-K 1,5", 9.5, "middle")
s.tick(986, Y, 2)
# -T1
s.psu(1050, 110, 80)
s.mtext(1140, 118, ["-T1", "Mean Well HDR-100-24", "230 V AC / 24,0 V DC fest,", "Poti versiegelt; 92 W, 3,83 A",
                    "SELV (EN 61558-2-16) [verif.]", "−30…+70 °C, Hutschiene"], 10.5, 13, bold_first=True)
# T1 PE (nur falls SK I)
s.line(1070, 110, 1070, 78, "pe")
s.dot(1070, 78)
s.text(1066, 100, "PE nur falls SK I [verif.]", 8.5, "end", cls="peT")

# PE-Schiene -X0
s.line(1270, 78, 1300, 78, "pe")
s.rect(1300, 72, 240, 12, "boxg")
s.text(1300, 66, "-X0  PE-Schiene / Potentialausgleich", 10.5, bold=True)
for xx in (1320, 1380, 1440, 1500):
    s.line(xx, 72, xx, 84, "sig")
s.line(1540, 78, 1628, 78, "pe")
s.line(1628, 78, 1628, 930, "pe")
s.text(1616, 300, "-W30 H07V-K 4 mm² gn/ge (≥ 4 mm² Cu [N-verif.])", 9.5, "middle", cls="peT", rot=-90)

# Barriere 230 V / SELV
s.line(600, 290, 1040, 290, "barrier")
s.text(604, 284, "Abdeckung / Trennsteg: oben 230 V, unten SELV 24 V (VDE 0100-410, 414) [N-verif.]", 9.5, cls="red")

# Hinweise
s.mtext(1300, 232, ["Hinweise:",
                    "• 230 V nur zwischen -X1, -Q1, -F1, -T1",
                    "• Freischalten allpolig über -Q1",
                    "• Erstprüfung DIN VDE 0100-600;",
                    "  bei Riso-Messung -T1 abklemmen",
                    "• -F11…-F15 Sicherungsklemmen 5×20,",
                    "  Defektanzeige [A]",
                    "• Leistungsbilanz ≈ 52 W (HDR-100 ≈ 56 %)"], 10, 13, bold_first=True)

# ---------------- 24-V-Verteilung ----------------
BUS = 380
s.line(1090, 190, 1090, BUS, "s24")
s.tick(1090, 330, 2, vertical=True)
s.text(1100, 352, "SELV +24 V / 0 V – 0 V nicht mit PE verbinden", 9.5, cls="red")
s.line(170, BUS, 1270, BUS, "s24")
s.dot(1090, BUS)
s.text(176, BUS - 8, "+24 V DC / 0 V (SELV, ungeerdet)", 10.5, bold=True)
s.tick(160 + 330, BUS, 2)

FX = {"F11": 220, "F12": 460, "F13": 680, "F14": 980, "F15": 1260}
FV = {"F11": ("2 A T", "Motortreiber"), "F12": ("1,25 A T", "Heizung"), "F13": ("1 A T", "Elektronik"),
      "F14": ("0,5 A T", "Feldsensorik"), "F15": ("0,5 A T", "Auswerter -K1")}
for k, x in FX.items():
    s.dot(x, BUS)
    s.line(x, BUS, x, 410, "s24")
    s.fuse_v(x, 410, 452)
    s.mtext(x + 12, 422, ["-" + k, FV[k][0], FV[k][1]], 10, 12, bold_first=True)

# -A1 Platine
A1Y, A1B = 620, 710
s.rect(150, A1Y, 770, A1B - A1Y, "boxa")
s.text(160, 688, "-A1  Steuerplatine 24 V (Details: Blatt EL-02)", 12, bold=True)
s.text(160, 703, "ESP32-WROOM-32UE-N8 · TMC2209 · ISO1212 · DS3231SN · DC/DC 24→5/3,3 V · Hardware-Sperre ZU", 9.5)
# F11 -> VM
s.line(220, 452, 220, A1Y, "s24")
s.text(226, 638, "VM", 10, bold=True)
# F13 -> 24V_IN
s.line(680, 452, 680, A1Y, "s24")
s.text(686, 638, "24V_IN", 10, bold=True)
# F12 -> B10 -> X2:40 -> E1 -> X2:41 -> HEAT
s.line(460, 452, 460, 462, "s24")
s.nc_thermal_v(460, 462)
s.text(500, 478, "-B10 Bimetall", 10, bold=True)
s.text(500, 490, "Öffner, öffnet +40 °C", 9.5)
s.line(460, 512, 460, 524, "s24")
s.terminal(460, 528)
s.text(470, 532, "-X2:40", 9.5)
s.line(460, 532, 460, 542, "s24")
s.heater(460, 542, 40, 30)
s.text(486, 556, "-E1 Heizung 24 V / 20 W [A]", 10, bold=True)
s.text(486, 568, "im Kasten +K1", 9.5)
s.line(460, 572, 460, 588, "s24")
s.terminal(460, 592)
s.text(470, 596, "-X2:41", 9.5)
s.line(460, 596, 460, A1Y, "s24")
s.text(466, 638, "HEAT (Low-Side-MOSFET)", 10, bold=True)
# F14 -> Feld + 24V_FLD
s.line(980, 452, 980, 756, "s24")
s.dot(980, 660)
s.line(980, 660, 920, 660, "s24")
s.text(914, 656, "24V_FLD (LS-Sender, getestet)", 9.5, "end", bold=True)
# F15 -> K1
s.line(1260, 452, 1260, 600, "s24")
s.rect(1205, 600, 110, 70, "box")
s.mtext(1260, 618, ["-K1", "Auswerter 8k2", "Kat. 3 [A]", "24 V AC/DC"], 10, 13, "middle", True)
s.mtext(1325, 612, ["Sensotek SAE-41-312-A", "(Alt. ASO ELMON/INDUS)", "13-14 K1_OK → -A1:IN7", "+ Hardware-Sperre (intern)"], 9.5, 12)
s.line(1260, 670, 1260, 756, "s24")

# ---------------- Abgaenge -X2 und Feldgeraete ----------------
XT = 760
LOC_Y, LOC_H = 860, 140
DEV_Y = 885


def drop(x, tlabel, wl, n, y_end=DEV_Y):
    s.terminal(x, XT)
    s.text(x - 7, XT - 6, tlabel, 9, "end")
    s.line(x, XT + 4, x, y_end, "s24")
    s.tick(x, 788, n, vertical=True)
    s.mtext(x + 5, 818, wl, 8.8, 11)


def dev(cx, lines, w=78, h=64):
    s.rect(cx - w / 2, DEV_Y, w, h, "box")
    s.mtext(cx, DEV_Y + 15, lines, 9.2, 12, "middle", True)


# Motor
s.line(220, A1B, 220, XT - 4, "s24")
s.text(226, 726, "A1/A2/B1/B2", 9)
drop(220, "-X2:1…5", ["-W11 PUR 4×0,5", "geschirmt [A]", "Schirm EMV-Vs."], 4, 872)
s.rect(150, LOC_Y, 140, LOC_H, "loc")
s.motor(220, 900, 26)
s.mtext(220, 942, ["-M1 NEMA 17, 48 mm", "≥ 0,59 Nm, ≤ 1,0 A eff"], 9, 11, "middle")
s.text(156, 994, "+M Antriebskasten", 9.5, bold=True)

# Aussentemperatur B9
s.line(340, A1B, 340, XT - 4, "s24")
s.text(346, 726, "1-Wire", 9)
drop(340, "-X2:45…47", ["-W22", "3×0,34 C [A]"], 3)
s.rect(298, LOC_Y, 84, LOC_H, "loc")
dev(340, ["-B9", "DS18B20", "außen IP68", "beschattet"], 74)
s.text(304, 994, "+A außen", 9.5, bold=True)

# LS-Sender
s.line(450, A1B, 450, XT - 4, "s24")
s.text(456, 726, "LS_TX", 9)
drop(450, "-X2:30,31", ["-W16", "PUR 2×0,5 [A]"], 2)
s.rect(398, LOC_Y, 106, LOC_H, "loc")
dev(450, ["-B6.1", "LS-Sender", "Marantec", "99165, IP65"], 92)
s.text(404, 994, "+R Rahmen", 9.5, bold=True)

# Verteilung F14
s.terminal(980, XT)
s.text(973, XT - 6, "-X2:10…21, 32–35, 42–44, 50–52", 9, "end")
s.line(980, XT + 4, 980, 830, "s24")
s.line(580, 830, 1175, 830, "s24")
s.dot(980, 830)
for x, wl, n in [(580, ["-W23 [A]", "intern"], 3), (705, ["-W14", "3×0,34"], 3), (795, ["-W15", "3×0,34"], 3),
                 (885, ["-W21", "3×0,34"], 3), (1005, ["-W12", "3×0,34"], 3), (1090, ["-W13", "3×0,34"], 3),
                 (1175, ["-W17", "4×0,5"], 4)]:
    s.line(x, 830, x, DEV_Y, "s24")
    s.tick(x, 845, n, vertical=True)
    s.mtext(x + 5, 866, wl, 8.5, 10)

s.rect(520, LOC_Y, 124, LOC_H, "loc")
dev(580, ["-S1 / -S2", "Taster AUF/ZU", "24 V, IP67", "Deckel"], 100)
s.text(526, 994, "+K1 Deckel", 9.5, bold=True)

s.rect(658, LOC_Y, 280, LOC_H, "loc")
dev(705, ["-B3", "Mutter oben", "PNP M12", "IP67"], 84)
dev(795, ["-B4", "Mutter unten", "PNP M12", "IP67"], 84)
dev(885, ["-B8", "Schlaff-", "schalter", "Mikroschalter"], 84)
s.text(664, 994, "+M Antriebskasten", 9.5, bold=True)

s.rect(952, LOC_Y, 370, LOC_H, "loc")
dev(1005, ["-B1", "Schieber", "unten", "PNP M12"], 80)
dev(1090, ["-B2", "Schieber", "oben", "PNP M12"], 80)
dev(1175, ["-B6.2", "LS-Empf.", "Relais", "Mar. 99165"], 80)
dev(1265, ["-B7", "Schaltleiste", "8,2 kΩ", "ASO SENTIR"], 86)
s.text(958, 994, "+R Rahmen / Durchgang", 9.5, bold=True)
# B7 von K1
drop(1265, "-X2:37,38", ["-W18", "2×0,5"], 2)

# Potentialausgleich Rahmen
s.rect(1342, LOC_Y, 270, LOC_H, "loc")
s.line(1628, 930, 1560, 930, "pe")
s.ground_pa(1560, 930)
s.mtext(1350, 882, ["Schutzpotentialausgleich", "Rahmen, Pfosten (fvz),", "Schwelle, Sturzblende",
                    "(VDE 0100-540/-705, O3)"], 9.8, 13, bold_first=True)
s.text(1348, 994, "+R Rahmen / Pfosten", 9.5, bold=True)

# ---------------- Legende ----------------
lx, ly = 40, 1022
s.text(lx, ly, "Legende / Kennzeichnung", 11, bold=True)
items = [("p230", "230 V AC (L, N; PE separat)"), ("s24", "24 V DC SELV"), ("pe", "PE / Potentialausgleich"),
         ("best", "Bestand (nicht Lieferumfang)"), ("loc", "Ortsgrenze (+UV, +K1, +M, +R, +A)"),
         ("barrier", "Berührungsschutz / Trennsteg")]
for i, (c, t) in enumerate(items):
    xx = lx + (i % 3) * 330
    yy = ly + 18 + (i // 3) * 18
    s.line(xx, yy - 4, xx + 40, yy - 4, c)
    s.text(xx + 48, yy, t, 10)
s.mtext(lx, ly + 66, [
    "Schrägstrich mit Zahl = Anzahl Leiter (ohne Schirm). BMK nach DIN EN IEC 81346-1/-2 [N-verif.], Symbole vereinfacht nach DIN EN 60617.",
    "[A] = Annahme, [verif.] = am Original-Datenblatt prüfen, [N-verif.] = Normbezug nicht am Normtext geprüft.",
    "Auslegung −10 °C (Bauherr, Standort 22397 Hamburg); -B9 außen: Warnung < −10 °C, Störung < −20 °C (Grenze -B6 Marantec 99165).",
    "Klemmenplan: EL-03, Pinbelegung: EL-04, Betriebsmittelliste: EL_Betriebsmittelliste.csv."], 9.5, 13)

s.frame_and_titleblock("Einlinienschema 230 V / 24 V", "Bestand-UV → -X1 → -Q1 → -F1 → -T1 → -F11…-F15 → Abgänge",
                       "EL-01", "1 von 2")
s.save(OUT, "Einlinienschema Entenklappe DuckDoor, Rev. A Entwurf 2026-11-23")
print("ok", OUT)
