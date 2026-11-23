"""EL-02 Blockschaltbild 24 V / Platine -A1 – Entenklappe DuckDoor (=DD). Erzeugt ../EL-02_Blockschaltbild_24V.svg"""
import os
from svglib import Svg

OUT = os.path.join(os.path.dirname(__file__), "..", "EL-02_Blockschaltbild_24V.svg")
s = Svg(title="EL-02 Blockschaltbild 24 V DuckDoor")

# ---------------- Einspeisung 24 V ----------------
s.psu(40, 40, 70)
s.mtext(118, 52, ["-T1 HDR-100-24", "24,0 V DC SELV", "(von EL-01)"], 10, 12, bold_first=True)
BUS = 160
s.line(75, 110, 75, BUS, "s24")
s.dot(75, BUS)
s.line(60, BUS, 1600, BUS, "s24")
s.line(60, BUS, 60, 790, "s24")
s.text(330, BUS - 8, "+24 V SELV  (−V / 0 V: -X2:0V-Brückenkamm, nicht mit PE verbunden)", 11, bold=True)

# ---------------- -A1 Rahmen ----------------
AX, AY, AR, AB = 330, 230, 1230, 900
s.rect(AX, AY, AR - AX, AB - AY, "boxa")
s.text(AX + 8, AY + 20, "-A1 Steuerplatine", 13, bold=True)
s.text(AX + 140, AY + 20, "(Eigenbau, Ort +K1)", 9.5)

# Versorgung (F13)
s.fuse_v(700, 172, 212)
s.dot(700, BUS)
s.line(700, BUS, 700, 172, "s24")
s.line(700, 212, 700, 252, "s24")
s.mtext(708, 184, ["-F13 1 A T"], 10, bold_first=True)
s.text(706, 244, "24V_IN", 9, bold=True)
s.rect(570, 252, 310, 62, "boxg")
s.mtext(578, 268, ["Eingang: Verpolschutz P-MOSFET, TVS SMBJ33A, LC",
                   "DC/DC 24→5 V (≥ 1 A) → LDO 3,3 V (≥ 600 mA)",
                   "-A1.U14 / -A1.U15 [A]"], 9.5, 13)
s.arrow(735, 314, 735, 340)
s.text(741, 332, "3,3 V / 5 V", 9)

# ISO1212
s.rect(360, 262, 180, 598, "boxg")
s.mtext(450, 276, ["-A1.U3…U6, U11 [A]", "ISO1212, 5×2 Kanäle", "IEC 61131-2 Typ 3"], 9.5, 12, "middle", True)
s.mtext(450, 840, ["je Eingang: TVS SMBJ33A", "+ R_SENSE, Steckklemme"], 8.8, 11, "middle")

# ESP32
s.rect(600, 340, 280, 360, "box")
s.text(740, 358, "-A1.U1 ESP32-WROOM-32UE-N8", 11, "middle", bold=True)
s.text(740, 371, "Chip-Rev. ≥ V3, Secure Boot V2 + Flash-Enc.", 8.8, "middle")
gp = ["IN1 B1 unten ............ GPIO36", "IN2 B2 oben ............. GPIO39", "IN3 B3 Mutter oben ...... GPIO34",
      "IN4 B4 Mutter unten ..... GPIO35", "IN5 B6 LS frei .......... GPIO32", "IN6 B8 Schlaff [A] ...... GPIO4",
      "IN7 K1_OK Schaltleiste .. GPIO33", "IN8 S1 AUF .............. GPIO13", "IN9 S2 ZU ............... GPIO14",
      "STEP 26 · DIR 27 · EN_CPU 25", "UART2 TX17 / RX16 · DIAG 19", "I²C SDA 21 / SCL 22",
      "LS-Test 18 · Heizung 23", "Strapping 0/2/5/12/15: frei", "Prog.-Header TX0/RX0/EN/IO0"]
s.mtext(610, 392, gp, 9.6, 19)
s.raw('<rect x="540" y="508" width="60" height="16" fill="#000"/>')
s.text(570, 503, "IN1…IN9", 9, "middle", bold=True)

# rechte Spalte: TMC, Sperre, LS-Test, Heizung
RX, RW = 1000, 210
s.rect(RX, 260, RW, 120, "box")
s.mtext(RX + 105, 278, ["-A1.U2 TMC2209-Modul", "StepStick, Kühlkörper", "≤ 1,0 A RMS, UART, StallGuard",
                        "VM: ≥ 470 µF/35 V Low-ESR", "(Alt. TMC2240, 36 V)", "shaft-Bit = 0 rücklesen"],
        9.5, 16, "middle", True)
s.fuse_v(1100, 172, 212)
s.dot(1100, BUS)
s.line(1100, BUS, 1100, 172, "s24")
s.line(1100, 212, 1100, 260, "s24")
s.text(1108, 192, "-F11 2 A T", 10, bold=True)
s.text(1106, 252, "VM", 9, bold=True)

s.rect(RX, 410, RW, 122, "boxg")
s.mtext(RX + 105, 423, ["Hardware-Sperre ZU (diskret)", "SPERRE_ZU = B6 ∨ B7 ∨ (B8 ∧ ¬B1)",
                        "ENN = ¬( EN_CPU ∧ ( DIR_AUF ∨", "(K1_OK ∧ B6_FREI ∧", "(B8_ANL ∨ B1_UNTEN))))",
                        "-A1.U12a–e: 2×1G08, 2×1G32, 1G00", "Eing. ISO1212 IN1/IN5/IN6/IN7",
                        "ENN Pull-up 10 kΩ → Reset gesperrt"], 8.8, 13.5, "middle", True)
s.arrow(1105, 410, 1105, 382, "s24")
s.text(1111, 400, "ENN", 9.5, bold=True)

s.rect(RX, 552, RW, 60, "box")
s.mtext(RX + 105, 568, ["LS-Test: P-MOSFET in +24 V", "Sender; Pulldown → Boot EIN", "24V_FLD von -F14"], 9.2, 15, "middle")
s.rect(RX, 640, RW, 70, "box")
s.mtext(RX + 105, 657, ["Heizungs-MOSFET Low-Side", "Logic-Level ≥ 5 A", "Gate-Pulldown 100 kΩ (Boot AUS)"],
        9.2, 16, "middle")

# ESP32 -> rechte Spalte
s.arrow(880, 360, 1000, 360)
s.text(940, 354, "STEP/DIR/UART/DIAG", 8.5, "middle")
s.arrow(880, 470, 1000, 470)
s.text(940, 464, "EN_CPU, DIR", 8.5, "middle")
s.arrow(880, 580, 1000, 580)
s.text(940, 574, "GPIO18", 8.5, "middle")
s.arrow(880, 680, 1000, 680)
s.text(940, 674, "GPIO23", 8.5, "middle")

# I2C-Block
s.rect(600, 740, 240, 140, "box")
s.mtext(608, 756, ["I²C-Bus GPIO21/22, 4,7 kΩ", "-A1.U7 DS3231SN + CR2032", "-A1.U8 SHT4x (Temp./r. F.)",
                   "-A1.U10 TCA9534 → -P1", "-A1.U13 DS2482-100 1-Wire [A]",
                   "Stecker -A1:XB5 → -B5 (intern)"], 9.3, 17, bold_first=True)
s.line(720, 700, 720, 740, "sig")
s.line(712, 718, 728, 722, "sig")

# Antenne
s.line(865, 700, 865, 960, "s24")
s.text(871, 914, "U.FL", 9)
s.antenna(865, 1000 - 30)
s.mtext(882, 940, ["-B20 Antenne 2–3 dBi", "RP-SMA, IP67 [A]", "-W20 Pigtail ≤ 15 cm"], 9.2, 12)

# Ausgaenge nach unten: B5, P1, B9
for x, lines, w, term in [(625, ["-B5 Lux", "BH1750/VEML7700", "Deckelfenster +K1"], 110, None),
                          (725, ["-P1", "Status-LED", "Deckel"], 76, None),
                          (800, ["-B9", "DS18B20 +A", "Außentemp."], 66, "X2:45…47")]:
    s.line(x, 880, x, 935, "sig")
    if term:
        s.terminal(x, 912)
        s.text(x - 8, 908, term, 8.5, "end")
    s.rect(x - w / 2, 935, w, 46, "box")
    s.mtext(x, 948, lines, 8.6, 11, "middle", True)
s.text(800, 993, "Warn < −10 °C, Stör < −20 °C", 8.3, "middle", cls="red")

# ---------------- Feldeingaenge links ----------------
s.fuse_h(78, 118, 220)
s.dot(60, 220)
s.line(60, 220, 78, 220, "s24")
s.line(118, 220, 160, 220, "s24")
s.text(78, 206, "-F14 0,5 A T", 10, bold=True)
s.line(160, 220, 160, 675, "s24")
s.text(166, 236, "+24 V Feld", 9.5, bold=True)
rows = [(290, "-B1 +R", "Schieber unten", "X2:11", "IN1"), (345, "-B2 +R", "Schieber oben", "X2:14", "IN2"),
        (400, "-B3 +M", "Mutter oben", "X2:17", "IN3"), (455, "-B4 +M", "Mutter unten", "X2:20", "IN4"),
        (510, "-B6.2 +R", "LS-Empf. NO", "X2:35", "IN5"), (565, "-B8 +M", "Schlaffschalter", "X2:43", "IN6"),
        (620, "-S1 Deckel", "Taster AUF", "X2:51", "IN8"), (675, "-S2 Deckel", "Taster ZU", "X2:52", "IN9")]
for y, a, b, xt, inn in rows:
    s.dot(160, y)
    s.line(160, y, 180, y, "s24")
    s.rect(180, y - 20, 112, 40, "box")
    s.mtext(236, y - 5, [a, b], 9.6, 13, "middle", True)
    s.line(292, y, 360, y, "sig")
    s.terminal(312, y)
    s.text(312, y - 8, xt, 8.5, "middle")
    s.text(366, y + 4, inn, 9.5, bold=True)
s.mtext(186, 708, ["+24 V: X2:10,13,16,19,", "32,34,42,50 · 0 V: X2:12,", "15,18,21,33,44 → Kamm", "B1–B4 PNP M12, IP67"], 8.5, 11)

# K1 / B7
s.fuse_h(78, 118, 790)
s.line(60, 790, 78, 790, "s24")
s.line(118, 790, 180, 790, "s24")
s.text(78, 776, "-F15 0,5 A T", 10, bold=True)
s.rect(180, 765, 112, 52, "box")
s.mtext(236, 780, ["-K1 Auswerter", "8k2, Kat. 3", "SAE-41-312-A"], 9.3, 12, "middle", True)
s.line(292, 790, 360, 790, "sig")
s.text(326, 784, "13-14", 8.5, "middle")
s.text(366, 794, "IN7 K1_OK", 9.5, bold=True)
s.line(236, 817, 236, 860, "s24")
s.terminal(236, 838)
s.text(244, 842, "X2:37,38 · -W18", 8.5)
s.rect(180, 860, 112, 40, "box")
s.mtext(236, 875, ["-B7 +R", "Schaltleiste 8,2 kΩ"], 9.3, 12, "middle", True)

# ---------------- rechte Feldseite ----------------
# Motor
s.line(1210, 320, 1340, 320, "s24")
s.terminal(1258, 320)
s.text(1258, 310, "X2:1…5", 8.5, "middle")
s.tick(1302, 320, 4)
s.text(1290, 337, "-W11 PUR 4×0,5 C [A]", 8.5, "middle")
s.motor(1370, 320, 28)
s.mtext(1370, 364, ["-M1 +M", "NEMA 17, 48 mm, ≥ 0,59 Nm", "Stecker verriegelbar"], 9.2, 12, "middle", True)

# LS-Sender
s.line(1210, 580, 1380, 580, "s24")
s.terminal(1258, 580)
s.text(1258, 570, "X2:30,31", 8.5, "middle")
s.text(1320, 596, "-W16", 8.5, "middle")
s.rect(1380, 555, 170, 50, "box")
s.mtext(1465, 572, ["-B6.1 +R LS-Sender", "Marantec 99165, 12–24 V", "IP65, −20…+60 °C"], 9.2, 12, "middle", True)
s.text(1465, 620, "Empfänger -B6.2 → IN5 (links)", 8.5, "middle", cls="grey")

# Heizung F12 -> B10 -> E1 -> HEAT
s.fuse_v(1600, 172, 212)
s.dot(1600, BUS)
s.line(1600, BUS, 1600, 172, "s24")
s.text(1588, 192, "-F12 1,25 A T", 10, "end", bold=True)
s.line(1600, 212, 1600, 226, "s24")
s.nc_thermal_v(1600, 226)
s.mtext(1590, 244, ["-B10 Bimetall", "Öffner +40 °C"], 9.3, 12, "end", True)
s.line(1600, 276, 1600, 288, "s24")
s.terminal(1600, 292)
s.text(1590, 296, "X2:40", 8.5, "end")
s.line(1600, 296, 1600, 306, "s24")
s.heater(1600, 306, 40, 30)
s.mtext(1574, 318, ["-E1 Heizung", "24 V / 20 W [A]"], 9.3, 12, "end", True)
s.line(1600, 336, 1600, 352, "s24")
s.terminal(1600, 356)
s.text(1590, 360, "X2:41", 8.5, "end")
s.line(1600, 360, 1600, 680, "s24")
s.line(1600, 680, 1210, 680, "s24")
s.text(1420, 674, "HEAT (−) zum Low-Side-MOSFET", 8.8, "middle")

# ---------------- Hinweise ----------------
s.mtext(40, 1012, [
    "Hinweise / Annahmen",
    "• Hardware-Sperre: Bei ausgelöster -B7, unterbrochener -B6 oder -B8 schlaff (B1 nicht aktiv) ist nur AUF",
    "  möglich – unabhängig von der Firmware (Freigabe E3). -B8 sperrt ZU, außer bei B1 aktiv (Verriegelungshub).",
    "• LS-Test vor jedem Schließen: GPIO18 schaltet den Sender ab, IN5 muss „unterbrochen“ melden.",
    "• -B8 Schlaffschalter (Freigabe M6) an IN6/GPIO4 über 5. ISO1212 -A1.U11 [A]; 1-Wire -B9 daher über",
    "  I²C-Bridge DS2482-100 -A1.U13 [A]. Lux -B5 hinter Deckelfenster (E5), kein Außenkabel.",
    "• SELV: 0 V nicht mit PE verbinden. Motor nie unter Spannung stecken (TMC2209).",
], 9.6, 13, bold_first=True)

s.frame_and_titleblock("Blockschaltbild 24 V / Platine -A1", "-T1 → -F11…-F15 → -A1 (ESP32, TMC2209, ISO1212, DS3231SN) → Feldgeräte",
                       "EL-02", "2 von 2")
s.save(OUT, "Blockschaltbild 24 V Entenklappe DuckDoor, Rev. A Entwurf 2026-11-23")
print("ok", OUT)
