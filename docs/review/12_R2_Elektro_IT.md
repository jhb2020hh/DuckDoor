# Review 12 – Runde 2: Elektro / Elektronik / IT-Sicherheit

Gegenstand: nur die Änderungen in `docs/01_Konzept_v1.md` (Kap. 2, 4, 5, 6). Vorbefunde: `02_Elektro.md`, `03_Steuerung_IT.md`.
Rollen: Elektroplanung DIN VDE 0100, Elektronik/PCB, IT-Security. Stand: 23.11.2026.

Kennzeichnung: **[A]** Annahme/Schätzung, **[H]** Herstellerangabe (Quelle), **[N-verif.]** Normbezug aus Fachkenntnis, nicht am Normtext geprüft, **[verif.]** vor Bestellung am Original-Datenblatt prüfen.
Methode: Websuche. Direktabruf von supabase.com war aus der Review-Umgebung gesperrt, deshalb stammen die Supabase-Angaben aus Suchauszügen der Doku-Seiten (Quellen S1–S9). Wortlaut vor der Umsetzung prüfen.

---

## 1 Befunde

### 1.1 Kritisch

| Nr | Befund | Begründung / Quelle |
|---|---|---|
| R2-K1 | **`aal2` ist keine Berechtigung.** Laut Konzept gilt „`commands` INSERT nur `aal2`“. Jeder Supabase-Benutzer, der einen eigenen TOTP-Faktor einrichtet, erreicht `aal2`. Ist die Registrierung offen oder fehlt eine RLS-Prüfung, kann also ein Fremder die Klappe öffnen. | Die RLS muss zusätzlich die **Zugehörigkeit zum Gerät** prüfen (`device_members`), und die öffentliche Registrierung muss aus sein. `aal2` restriktiv nach S2; Skizze in Kap. 6.3. |
| R2-K2 | **Der Verriegelungshub kann Spindelkraft auf ein Hindernis bringen.** Der Schwerkraftschluss schützt nur beim Absenken. Beim Verriegeln drückt der Bolzen am oberen Langlochende den Schieber mit Motorkraft nach unten. Meldet B1 fälschlich „unten“ (Fehljustage, Eis, Sensordefekt) und liegt ein Tier oder eine Hand unter dem Schieber, entsteht eine Quetschkraft. Abschätzung **[A]**: 0,4 N·m Haltemoment, Wirkungsgrad Tr8×2 ≈ 0,3, Axialkraft F = 2π·M·η/P = 2π·0,4·0,3/0,002 ≈ **380 N**. StallGuard und Strombegrenzung laufen nur in der Firmware, also einkanalig. | Schaltleiste B7 und Lichtschranke B6 müssen die Bewegungsrichtung „ZU/Verriegeln“ **hardwareseitig** sperren, unabhängig von der Firmware (Kap. 3, „Hardware-Sperre“). B1 muss mit der Spindelposition (Schrittzähler, B4) plausibilisiert werden. Den Verriegelungsstrom per UART auf das nötige Minimum begrenzen. |
| R2-K3 | **Die Sicherheitsfunktion der Kinderschutzmaßnahmen ist nicht festgelegt.** v1 nennt die Bauteile, aber weder die Auswertung noch die Testung oder eine Kategorie bzw. ein PL. Bei kraftbetätigten Toren dienen EN 12453 und EN 12978 als Referenz. ESPE-Typ 2 bedeutet PL c mit periodischem Test. | Q15, Q16. Bewertung **[A]**: Für einen Privatbau ist keine Normerfüllung gefordert, als Maßstab aber sinnvoll. Das Ziel lautet „1-Fehler-sicher gegen Quetschen beim Verriegeln“. |

### 1.2 Mittel

| Nr | Befund | Begründung / Quelle |
|---|---|---|
| R2-M1 | **Netzteil nicht festgelegt.** Die Leistungsbilanz (Kap. 2.2) ergibt bei Gleichzeitigkeit ≈ 52 W. Ein HDR-60-24 (60 W) wäre zu 87 % ausgelastet. Bei Sommerhitze im Kasten droht ein Derating. | Empfehlung **Mean Well HDR-100-24**: 24 V, 92 W, Betrieb −30…+70 °C (oberer Bereich mit Derating), lüfterlos [H] Q1, Q2. Den Derating-Wert bei +50/+60 °C an der Kurve im Datenblatt ablesen [verif.]. |
| R2-M2 | **Wenig Spannungsreserve beim TMC2209.** Der Treiber ist für VS 4,75…29 V spezifiziert [H] Q5. Bei 24 V nominal fehlen Reserven für ein hochgedrehtes Netzteil-Poti, Rückspeisung beim Abbremsen und die TVS-Klemmspannung, denn jede 24-V-TVS klemmt oberhalb von 29 V. | Netzteil fest auf 24,0 V einstellen und das Poti versiegeln. Am VM-Eingang ≥ 470 µF/35 V Low-ESR vorsehen. **Alternative TMC2240** (4,5…36 V, ca. 2 A RMS, UART/SPI, StallGuard4) [H] Q6. |
| R2-M3 | **RTC-Typ.** DS3231S ist für 0…+70 °C spezifiziert, DS3231SN für −40…+85 °C (±3,5 ppm) [H] Q9. Günstige Module tragen oft den falschen Typ oder sind Nachbauten. | Auf der Platine einen **DS3231SN** bestücken, Bezug über Distributor, kein fertiges Modul. |
| R2-M4 | **Lux-Sensor außen über I²C.** Der VEML7700 hat −25…+85 °C [H] Q10. Darunter liegt er außerhalb der Spezifikation. I²C ist nicht für Außenleitungen ausgelegt: 400 pF Buskapazität, kein ESD-/Überspannungsschutz. | Für ≤ 1 m: PCA9615 als differenzielles I²C, max. 3 m laut Datenblatt [H] Q11, dazu TVS/ESD am Stecker. Alternative ohne Außenleitung: Sensor **im Gehäuse hinter einem Lichtfenster** im Deckel, Kasten nicht verschattet [A]. Tiefste Standorttemperatur klären. |
| R2-M5 | **Lichtschranke bei Kälte.** Der vorgeschlagene Typ Marantec 99165 (Einweg, 12–24 V AC/DC, Relais-Wechsler, IP65, 0–10 m) ist für −20…+60 °C angegeben [H] Q13. Die Sommer-Einweg (IP55, −10 °C) ist ungeeignet [H] Q13. | Standorttemperatur prüfen. Bei < −20 °C einen Industrietyp mit −25/−30 °C wählen. Die Lichtschranke vor jedem Schließen über die Senderspannung testen („getestete Lichtschranke“, Kap. 3). |
| R2-M6 | **ESP32-Siliziumrevision.** Secure Boot V2 und der ROM-Schutz gegen Fault-Injection-Angriffe auf eFuse-Schlüssel gibt es erst ab ESP32-D0WD-**V3** [H] Q19, Q20. | Nur **ESP32-WROOM-32UE** verwenden (enthält V3), nicht den alten WROOM-32U. |
| R2-M7 | **Realtime auf dem ESP32 ist aufwendig.** Nötig sind Phoenix-Protokoll, Heartbeat und JWT-Erneuerung im Kanal. Ein Edge-Function-Polling alle 5 s ergibt ≈ 518 000 Aufrufe/Monat und liegt damit über dem Free-Kontingent von 500 000 [H] S5. | Kap. 6.2: Polling per PostgREST-RPC. Das ist nicht kontingentiert, nur der Egress zählt. |
| R2-M8 | **Free-Projekte pausieren** bei zu geringer Datenbankaktivität innerhalb einer Woche [H] S6. Dann fällt die Fernsteuerung aus, der lokale Betrieb bleibt erhalten. | Das Geräte-Polling erzeugt laufend DB-Abfragen und verhindert die Pause praktisch **[A]**. Den Status „Gerät offline > 1 h“ in der App anzeigen. |
| R2-M9 | **Die Heizung hat nur einen Temperaturfühler.** Ein DS18B20 kann die Betauung nicht erkennen. Ohne Übertemperaturbegrenzer kann ein MOSFET im Kurzschluss dauerhaft heizen. | I²C-Sensor für Temperatur und r. F. im Kasten vorsehen (z. B. SHT4x) **[A]**. Bimetall-Thermostat (öffnet bei ca. +40 °C) **in Reihe** zum MOSFET-Ausgang **[A]**. |
| R2-M10 | **Eingangsbeschaltung nicht spezifiziert.** Optokoppler verlieren bei Kälte und Alterung an CTR. | **TI ISO1212** (2 Kanäle, IEC 61131-2 Typ 1/2/3, Strombegrenzung 2,2–2,5 mA, keine feldseitige Versorgung nötig) [H] Q12. Davor je Eingang TVS und Reihenwiderstand (Kap. 3.3). |

### 1.3 Gering

| Nr | Befund |
|---|---|
| R2-G1 | SELV: 0 V **nicht** mit PE verbinden, sonst entsteht PELV. Das Netzteil muss als Sicherheitstransformator nach EN 61558-2-16 / EN 62368-1 gelten. Für HDR-60 wird EN 61558 als Zulassung genannt [H] Q3, für HDR-100 [verif.]. Ob das Gerät Schutzklasse II ohne PE-Anschluss ist [verif.]. |
| R2-G2 | Einschaltstrom des Netzteils gegen LS B6 Char. B prüfen [verif. Datenblatt „Inrush“]. Ist er zu hoch, C6 verwenden, sofern die Abschaltbedingung erfüllt ist [N-verif.] DIN VDE 0100-410. |
| R2-G3 | Externe Antenne: Die Funkkonformität (RED) des Moduls gilt nur für Antennen bis zum zertifizierten Gewinn **[A, verif. Modul-Zertifikat]**. Eine 2–3-dBi-Dipolantenne mit RP-SMA-Schottdurchführung und IP67 verwenden. U.FL-Pigtail ≤ 15 cm **[A]**. |
| R2-G4 | Pufferbatterie der RTC: CR2032 bei −30 °C mit Kapazitätsverlust **[A]**. Das Gehäuse ist beheizt, daher unkritisch. Alternativ einen Superkondensator vorsehen, der ≥ 3 Tage überbrückt **[A]**. |
| R2-G5 | Der Leitungstyp H07RN-F ist für Signal- und Motorleitungen ungeschirmt. Für die Schrittmotorleitung (EMV) eine geschirmte PUR-Leitung verwenden, Schirm über EMV-Verschraubung auflegen **[A]**. |
| R2-G6 | TMC2209: Den Motor nie unter Spannung stecken oder trennen, das zerstört den Treiber **[A, Fachpraxis]**. Motorstecker verriegelbar ausführen. Das `shaft`-Bit (Drehrichtungsumkehr per UART) nach dem Booten zurücklesen, damit die Hardware-Sperre nicht durch falsche Richtung umgangen wird. |

---

## 2 Elektro: Auslegung

### 2.1 Netzteil und Absicherung

| BMK | Vorgabe | Quelle |
|---|---|---|
| -T1 | **Mean Well HDR-100-24**, 24 V DC, 92 W (3,83 A), Hutschiene, −30…+70 °C mit Derating, lüfterlos. Ausgang auf 24,0 V einstellen. | Q1, Q2 [verif. Derating, SELV, Schutzklasse] |
| Rückfalloption | HDR-60-24 (60 W, 2,5 A, −30…+70 °C), nur mit firmwareseitiger Lastabwurfregel „Heizung AUS während Motorfahrt“. | Q3 |
| -F1 | LS 1P+N B6, EN 60898-1, ≥ 6 kA (Leitungsschutz der Innenverdrahtung 1,5 mm²). | [N-verif.] DIN VDE 0100-430 |
| -Q1 | Reparaturschalter 2-polig, abschließbar (aus R1 übernommen; in v1 nicht mehr genannt → wieder aufnehmen). | 02_Elektro E6 |
| -F11 | 24 V Motortreiber: Feinsicherung 2 A T. | [A] |
| -F12 | 24 V Heizung: 1,25 A T. | [A] |
| -F13 | 24 V Elektronik (DC/DC auf -A1): 1 A T. | [A] |
| -F14 | 24 V Feldsensorik (B1–B4, B6): 0,5 A T. | [A] |
| -F15 | 24 V Schaltleisten-Auswerter -K1: 0,5 A T. | [A] |

Die Sicherungen als Sicherungs-Reihenklemmen 5×20 mm mit Defektanzeige ausführen **[A]**. Die Kurzschlussauslösung bei HDR prüfen, Datenblatt „Protection – Short circuit“ [verif.].

### 2.2 Leistungsbilanz (24 V)

| Verbraucher | Dauer | Spitze | Annahme |
|---|---|---|---|
| Motor -M1 über TMC2209 (NEMA 17, ≈ 1,0 A RMS, R ≈ 1,5 Ω/Phase) | 0 W (Halt mit Haltestrom ≈ 2 W) | ≈ 8–12 W real, **24 W** als Auslegungsobergrenze | [A] Kupferverluste 2·I²·R ≈ 3 W + mech. 0,5 W/η + Treiberverluste |
| Heizung -E1 (PTC/Heizwiderstand 24 V) | 0–20 W | 20 W | Kap. 2.3 |
| ESP32 + WLAN, DC/DC η ≈ 0,85 | ≈ 1 W | ≈ 2 W | [A] |
| Endlagensensoren B1–B4 (PNP, 24 V) | ≈ 1,2 W | 1,2 W | [A] 4 × 12 mA |
| Lichtschranke B6 (Sender + Empfänger) | ≈ 2 W | 2 W | [A, Datenblatt prüfen] |
| Schaltleisten-Auswerter -K1 | ≈ 2 W | 2 W | [A] |
| ISO1212, Lux, RTC, Sonstiges | < 0,5 W | 0,5 W | [A] |
| **Summe** | ≈ 7 W (ohne Heizung) | **≈ 52 W** | Gleichzeitigkeit 1 angesetzt |

HDR-100-24 ist damit zu ≈ 56 % ausgelastet. Reserve für Derating und Alterung ist vorhanden.

### 2.3 Heizleistung Gehäuse [A]

- Gehäuse PC/GFK 400 × 300 × 200 mm (H × B × T) **[A]**.
- Wirksame Oberfläche nach IEC 60890, frei aufgestellt: A = 1,8·H·(B+T) + 1,4·B·T = 1,8·0,4·0,5 + 1,4·0,3·0,2 = **0,44 m²** (Q17).
- k = 3,5 W/(m²·K) für Polyester (Q17, Kunststoffgehäuse **[A]** übertragen). ΔT = 5 K als Betauungsschutz.
- Q = A·ΔT·k = 0,44·5·3,5 = 7,7 W. Bei Außenaufstellung verdoppeln (Q17) → **≈ 15,5 W**.
- **Vorgabe: Heizung 24 V DC, 20 W.** Zweipunktregelung durch die Firmware: EIN bei T_innen < +5 °C oder r. F. > 65 %, AUS bei +10 °C bzw. 55 %. Bimetall-Begrenzer +40 °C in Reihe.
- Frostschutz für die Elektronik ist nicht nötig: Elektronik −40 °C, Netzteil −30 °C, siehe Q1, Q7, Q9. Die Heizung dient nur gegen Betauung. Die Eigenverlustleistung (≈ 5 W) unterstützt sie **[A]**.

### 2.4 Bauteilwahl Elektronik

| Funktion | Vorgabe | Quelle / Begründung |
|---|---|---|
| MCU | **ESP32-WROOM-32UE-N8** (U.FL, 8 MB Flash für 2 OTA-Partitionen), −40…+85 °C. Variante -H4: bis +105 °C (nur 4 MB Flash) | Q7, Q8 |
| Antenne | 2,4-GHz-Dipol 2–3 dBi, RP-SMA-Schottdurchführung IP67, U.FL-Pigtail ≤ 15 cm | [A], R2-G3 |
| Schrittmotortreiber | **Steckmodul** TMC2209 StepStick (z. B. BTT/FYSETC) auf Buchsenleiste statt Onboard. Begründung: QFN-Gehäuse mit Exposed Pad ist von Hand schwer zu löten, das Modul ist im Defektfall tauschbar. Dauerstrom des Moduls laut Modulhersteller (oft ≈ 1,4 A RMS, Q5). Kühlkörper vorsehen, Strom ≤ 1,0 A RMS. Bei Neuentwurf mit Reflow: TMC2240 onboard (R2-M2). | Q5, Q6 |
| Eingänge 24 V | 4 × **ISO1212** (8 Kanäle). Je Eingang: TVS SMBJ33A gegen 0 V, R_SENSE nach Datenblatt (Typ 3), Steckklemme. Ausgang 3,3 V CMOS direkt an den GPIO. | Q12 |
| Spannungsversorgung -A1 | Eingang: Verpolschutz (P-MOSFET), TVS SMBJ33A, LC-Filter. DC/DC 24 → 5 V (≥ 1 A, Synchronwandler) → LDO 3,3 V (≥ 600 mA) [A]. VM des TMC separat hinter -F11 mit ≥ 470 µF/35 V. | [A] |
| RTC | **DS3231SN** (−40…+85 °C) + CR2032 oder Superkondensator | Q9 |
| Klima Kasten | SHT4x (I²C, onboard) + DS18B20 optional | [A] |
| Lux -B5 | **BH1750** oder **VEML7700** (−25 °C, Q10) auf Außenplatine mit **PCA9615** (Q11), Kabel 2 × 2 × 0,25 mm² geschirmt + 2 × 0,5 mm² Versorgung, ≤ 3 m. Untergrenze BH1750 [verif.] | Q10, Q11 |
| Heizungsausgang | Low-Side-N-MOSFET (Logic-Level, ≥ 5 A), Gate-Pulldown 100 kΩ (beim Booten AUS), Freilaufdiode nicht nötig (ohmsche Last) | [A] |
| Lichtschranke -B6 | **Marantec 99165** Einweg, 12–24 V AC/DC, Relais-Wechsler, IP65, 0–10 m, −20…+60 °C | Q13 |
| Schaltleiste -B7 | **ASO SENTIR edge** (z. B. 25.30 TT) mit 8,2-kΩ-Endwiderstand: unbetätigt 8,2 kΩ ± 500 Ω, betätigt ≤ 500 Ω. Temperaturbereich am Datenblatt prüfen | Q14 |
| Auswerter -K1 | **Sensotek SAE-41-312-A** (8k2-Eingang, 24 V AC/DC, Kat. 3) oder ASO ELMON/INDUS (8,2 kΩ, Kat. 3 / PL e) | Q14 |
| Endlagen B1–B4 | Induktive Näherungsschalter M12, PNP-Schließer, 24 V, IP67, ≥ −25 °C **[A]** | [A] |

### 2.5 Hardware-Sperre ZU-Richtung (zu R2-K2)

```
ENN_TMC (aktiv LOW) = NOT( EN_CPU  AND  ( DIR_AUF  OR  ( K1_OK AND B6_FREI ) ) )
```
- Die Logik mit Einzelgattern (74LVC1G08/32) auf -A1 aufbauen. K1_OK ist der Relaiskontakt des Auswerters -K1 (Schließer, unbetätigt geschlossen), eingelesen über einen ISO1212-Kanal. B6_FREI ist der Relaiskontakt des Empfängers der Lichtschranke.
- Wirkung: Bei ausgelöster Schaltleiste oder Lichtschranke ist nur noch „AUF“ möglich, auch wenn die Firmware fehlerhaft ist. ENN hat einen Pull-up auf 3,3 V, beim Reset ist der Treiber also gesperrt.
- Test der Lichtschranke: Vor jedem Schließen schaltet die Firmware den Sender ab (GPIO18 → P-MOSFET in +24 V des Senders) und erwartet „unterbrochen“. Danach wird der Sender wieder eingeschaltet.
- Die DIR-Polarität ist fest verdrahtet. Das `shaft`-Bit muss 0 sein und wird zurückgelesen (R2-G6).

---

## 3 Single-Line-Vorgabe (230-V-Teil)

Anlage `=DD`. Orte: `+UV` Bestandsverteilung, `+K1` Schaltkasten am Pfosten, `+M` Antriebskasten oben, `+R` Rahmen/Durchgang, `+A` außen (Lux). Kennzeichnung nach DIN EN IEC 81346-1/-2 [N-verif.].

```
=DD+UV   L/N/PE ── -F0 RCD 30 mA Typ A (Bestand, nachweisen) ── -F01 LS B16/B10 ≥ 6 kA (Bestand)
                     │                                             [SPD Typ 2 in +UV prüfen, VDE 0100-443]
                     └── -W1 NYY-J 3×1,5 (Erdreich ≥ 0,6 m [A], Schutzrohr am Austritt)
                           │
=DD+K1   -X1:1 L ─┐
         -X1:2 N ─┼─ -Q1 Rep.-Schalter 2-pol., abschließbar ── -F1 LS B6 1P+N, ≥ 6 kA
         -X1:PE ──┼──────────────────────────────────────────┐        │
                  │                                          │        ├── -X1:3 L' ── -T1 HDR-100-24 :L
                  │                                          │        └── -X1:4 N' ── -T1 :N
                  │                                          │                      -T1 :+V/-V → SELV 24 V (Kap. 4)
                  │                                     -X1:PE ── -X0 PE-Schiene
                  │                                                 ├── Potentialausgleich Rahmen/Pfosten
                  │                                                 │   (H07V-K gn/ge ≥ 4 mm² Cu [N-verif.] VDE 0100-540)
                  │                                                 └── -T1 PE (nur falls SK I [verif.])
                  │   SELV-0 V NICHT mit PE verbinden.
```
Hinweise:
- Im Kasten liegen 230 V nur zwischen -X1, -Q1, -F1 und -T1. Diesen Bereich abdecken (Berührungsschutz) und durch Trennsteg von 24 V trennen [N-verif.] DIN VDE 0100-410, Abschn. 414.
- RCD Typ A ist ausreichend, weil nur ein Schaltnetzteil mit Gleichrichter einspeist **[A]**.
- Erstprüfung nach DIN VDE 0100-600. Bei der Isolationsmessung -T1 abklemmen [N-verif.].

---

## 4 Blockschaltbild-/Verdrahtungsvorgabe (24-V-Teil)

```
-T1 +24V ──┬─ -F11 2AT ──────────────── -A1:VM ──(TMC2209 -A1.U2)── -X2:1..4 ── -W11 ── -M1 Schrittmotor (+M)
           ├─ -F12 1,25AT ─ -B10 Bimetall 40°C ─ -X2:40 ── -E1 Heizung 20 W ── -X2:41 ── -A1:HEAT (Low-Side-MOSFET)
           ├─ -F13 1AT ─────────────── -A1:24V_IN → DC/DC 5 V → LDO 3,3 V → ESP32 -A1.U1, RTC, ISO1212, SHT4x
           ├─ -F14 0,5AT ─ -X2:10/13/16/19 (+24 V Sensoren) ── -W12..15 ── -B1..-B4 (+M/+R)
           │             └ -A1:LS_TX (P-MOSFET, GPIO18) ─ -X2:30 ── -W16 ── -B6.1 Sender LS (+R)
           │             └ -X2:32 ── -W17 ── -B6.2 Empfänger LS (+R), Relais COM ─ -X2:34 ; NO ─ -X2:35 → -A1:IN6
           ├─ -F15 0,5AT ─ -K1 Auswerter Schaltleiste :A1 ; -K1 Eingang ── -X2:37/38 ── -W18 ── -B7 Schaltleiste 8k2 (+R)
           │                 -K1 Sicherheitskontakt 13-14 ── -A1:IN7 (K1_OK) + Hardware-Sperre (Kap. 2.5)
           └─ -X2:50/51 ── -S1 AUF / -S2 ZU (Deckel +K1) → -A1:IN8/IN9 (über ISO1212)
-T1 0V ──── -X2:0V-Brückenkamm (alle 0-V-Klemmen), -A1:GND        (SELV, nicht geerdet)

-A1 I²C (SDA/SCL) ─ DS3231SN, SHT4x, PCA9615 ─ -X2:22..28 ── -W19 (geschirmt, ≤ 3 m) ── -B5 Lux-Kopf (+A) mit PCA9615 + BH1750/VEML7700
-A1 U.FL ── -W20 Pigtail ── Schottdurchführung RP-SMA ── Antenne -B20 (Kennbuchstabe nach 81346-2 prüfen)
-A1 Prog-Header (TX/RX/EN/IO0/3V3/GND), Status-LED -P1 über I²C-Expander
```

### 4.1 Betriebsmittelliste (Ergänzung zu v1)

| BMK | Ort | Betriebsmittel |
|---|---|---|
| -X1 | +K1 | Reihenklemmen 230 V (L, N, PE, L', N') |
| -Q1 | +K1 | Reparaturschalter 2-polig, abschließbar |
| -F1 | +K1 | LS B6 1P+N |
| -T1 | +K1 | Netzteil HDR-100-24 |
| -F11…-F15 | +K1 | Sicherungsklemmen 5×20 |
| -X2 | +K1 | Reihenklemmen 24 V Feld (SELV) |
| -X0 | +K1 | PE-Schiene / Potentialausgleich |
| -A1 | +K1 | Steuerplatine (U1 ESP32-WROOM-32UE, U2 TMC2209-Modul, U3–U6 ISO1212, U7 DS3231SN, U8 SHT4x, U9 PCA9615, U10 TCA9534) |
| -K1 | +K1 | Auswerter Schaltleiste 8k2 |
| -E1 | +K1 | Heizung 24 V, 20 W |
| -B10 | +K1 | Bimetall-Begrenzer, Öffner +40 °C |
| -M1 | +M | Schrittmotor NEMA 17 |
| -B1 / -B2 | +R | Schieber unten / oben |
| -B3 / -B4 | +M | Mutter oben / unten |
| -B5 | +A | Lux-Kopf (I²C differenziell) |
| -B6.1 / -B6.2 | +R | Lichtschranke Sender / Empfänger |
| -B7 | +R | Schaltleiste 8,2 kΩ an der Schieberunterkante (Spiralkabel bzw. Schleppkabel) |
| -S1 / -S2 | +K1 | Taster AUF / ZU, 24 V, IP67 |
| -P1 | +K1 | Status-LED (Deckel) |
| -W11 | +K1→+M | Motorleitung PUR 4 × 0,5 geschirmt **[A]** |
| -W12…-W19 | | Sensorleitungen PUR 3 × 0,34 bzw. 2 × 2 × 0,25 geschirmt **[A]**, UV-beständig |

---

## 5 Klemmenplan

### 5.1 -X1 (230 V, Netzbereich, abgedeckt)

| Klemme | Funktion | intern | extern | Leitung |
|---|---|---|---|---|
| -X1:1 | L Einspeisung | -Q1:1 | -W1 br | NYY-J 3×1,5 |
| -X1:2 | N Einspeisung | -Q1:3 | -W1 bl | |
| -X1:PE | PE | -X0 | -W1 gn/ge | |
| -X1:3 | L' nach LS | -F1:2 | -T1:L | H07V-K 1,5 |
| -X1:4 | N' nach LS | -F1:N | -T1:N | H07V-K 1,5 |

### 5.2 -X2 (24 V SELV, Feld)

| Klemme | Funktion | intern | extern | Leitung |
|---|---|---|---|---|
| -X2:1 / 2 | Motor A+ / A− | -A1.U2 A1/A2 | -M1 Spule A | -W11 |
| -X2:3 / 4 | Motor B+ / B− | -A1.U2 B1/B2 | -M1 Spule B | -W11 |
| -X2:5 | Schirm Motor | EMV-Verschraubung | Schirm | -W11 |
| -X2:10 / 11 / 12 | B1 +24 V / Signal / 0 V | -F14 / -A1:IN1 / 0 V | -B1 | -W12 |
| -X2:13 / 14 / 15 | B2 +24 V / Signal / 0 V | -F14 / -A1:IN2 / 0 V | -B2 | -W13 |
| -X2:16 / 17 / 18 | B3 +24 V / Signal / 0 V | -F14 / -A1:IN3 / 0 V | -B3 | -W14 |
| -X2:19 / 20 / 21 | B4 +24 V / Signal / 0 V | -F14 / -A1:IN4 / 0 V | -B4 | -W15 |
| -X2:22 / 23 | Lux +5 V / 0 V | -A1 | -B5 | -W19 |
| -X2:24 / 25 | Lux DSDA+ / DSDA− | -A1.U9 | -B5 | -W19 Paar 1 |
| -X2:26 / 27 | Lux DSCL+ / DSCL− | -A1.U9 | -B5 | -W19 Paar 2 |
| -X2:28 | Schirm Lux | EMV-Verschraubung | | -W19 |
| -X2:30 / 31 | LS-Sender +24 V (getestet) / 0 V | -A1:LS_TX / 0 V | -B6.1 | -W16 |
| -X2:32 / 33 | LS-Empfänger +24 V / 0 V | -F14 / 0 V | -B6.2 | -W17 |
| -X2:34 / 35 | LS-Relais COM / NO (frei = geschlossen) | +24 V (-F14) / -A1:IN5 | -B6.2 | -W17 |
| -X2:37 / 38 | Schaltleiste 8k2 | -K1 Eingang | -B7 | -W18 2 × 0,5 |
| -X2:40 / 41 | Heizung + / − | -B10 / -A1:HEAT | -E1 (intern) | 0,75 mm² |
| -X2:50 / 51 / 52 | Taster +24 V / AUF / ZU | -F14 / -A1:IN8 / -A1:IN9 | -S1, -S2 | intern |
| -X2:0V | 0-V-Brückenkamm | -T1 −V | alle 0 V | |

-A1:IN6 entfällt bzw. ist Reserve. -A1:IN7 = K1_OK (intern von -K1:14).

---

## 6 Pinbelegung ESP32-WROOM-32UE

Gemieden werden die Strapping-Pins **GPIO0, 2, 5, 12, 15** (Q18), die Flash-Pins **GPIO6–11** sowie UART0 GPIO1/3 (nur Programmierung). ADC2 ist bei aktivem WLAN nicht nutzbar **[A]**. GPIO34–39 sind reine Eingänge ohne internen Pull-up (Q18). Sie sind für ISO1212-Ausgänge geeignet, weil diese aktiv treiben.

| GPIO | Funktion | Richtung | Beschaltung |
|---|---|---|---|
| 36 (VP) | IN1 B1 Schieber unten | E | ISO1212 |
| 39 (VN) | IN2 B2 Schieber oben | E | ISO1212 |
| 34 | IN3 B3 Mutter oben | E | ISO1212 |
| 35 | IN4 B4 Mutter unten | E | ISO1212 |
| 32 | IN5 B6 Lichtschranke frei | E | ISO1212, zusätzlich Hardware-Sperre |
| 33 | IN7 K1_OK Schaltleiste | E | ISO1212, zusätzlich Hardware-Sperre |
| 13 | IN8 Taster AUF | E | ISO1212 |
| 14 | IN9 Taster ZU | E | ISO1212 (liefert beim Booten ein PWM-Signal, als Eingang unkritisch **[A]**) |
| 26 | TMC STEP | A | Serien-R 100 Ω |
| 27 | TMC DIR | A | zusätzlich Hardware-Sperre |
| 25 | TMC EN_CPU | A | Gatterlogik, ENN-Pull-up 10 kΩ |
| 17 | UART2 TX → TMC PDN_UART | A | 1 kΩ zur Eindraht-UART |
| 16 | UART2 RX ← TMC PDN_UART | E | |
| 19 | TMC DIAG (StallGuard) | E | |
| 21 / 22 | I²C SDA / SCL | E/A | 4,7 kΩ (DS3231SN, SHT4x, PCA9615, TCA9534) |
| 4 | 1-Wire DS18B20 (optional) | E/A | 4,7 kΩ |
| 18 | LS-Test Sender AUS | A | P-MOSFET-Treiber, Pulldown (Sender beim Booten EIN) |
| 23 | Heizung MOSFET | A | Gate-Pulldown 100 kΩ |
| EN, IO0, TX0, RX0 | Programmierung | | Auto-Reset-Schaltung, Header |

Status-LED -P1 und Reserve-Ausgänge laufen über einen I²C-Expander TCA9534 **[A]**, weil keine Nicht-Strapping-GPIO frei sind. Das ist ein Hinweis für den PCB-Entwurf: GPIO2 mit LED gegen GND wäre zwar beim Booten unkritisch, wird aber gemäß Vorgabe gemieden.

---

## 7 IT: Geräteanbindung und Sicherheit

### 7.1 Geräteauthentifizierung (Empfehlung)

| Kriterium | A: eigener Device-User (Supabase Auth) + RPC | B: Edge Function + Device-Token |
|---|---|---|
| Identität | JWT des Device-Users, `devices.device_user = auth.uid()` | 256-Bit-Token, Hash in der DB, Prüfung in der Function (`service_role`) |
| Angriffsfläche | Nur `SECURITY DEFINER`-RPCs, keine Tabellenrechte für das Gerät | Schmal, aber `service_role` liegt in der Function |
| Realtime | möglich (JWT, private Channel, S3) | nicht ohne selbst ausgestelltes JWT |
| Free-Kontingent | PostgREST nicht kontingentiert (nur Egress) | **500 000 Aufrufe/Monat** (S5). Polling alle 5 s ≈ 518 400/Monat → überschritten. Alle 10 s ≈ 259 200 |
| Rotation/Sperre | Passwort per Admin-API ändern, User sperren (ban) | Token in der DB ersetzen |
| **Bewertung** | **empfohlen** (einfach, ohne Kontingentproblem, RLS-nativ) | Alternative, falls zusätzlich Request-Signatur gewünscht |

Vorgaben zu A:
- Device-User mit zufälligem Passwort (≥ 32 Zeichen). `app_metadata.role = 'device'` wird nur per `service_role` gesetzt. **Öffentliche Registrierung aus.** Der Device-User erhält **keinen** Eintrag in `device_members`.
- Auf dem Gerät liegt nur der **Publishable/Anon-Key**, nie der `service_role`-Key.
- Beim Booten meldet sich das Gerät mit Passwort an. Den Refresh-Token hält es im RAM, damit nach einem Stromausfall kein Rotationskonflikt entsteht **[A]**.
- TLS: ESP-IDF-Zertifikatsbundle, kein Leaf-Pinning, weil Zertifikatswechsel bei Supabase nicht steuerbar sind **[A]**.
- **Schlüsselablage:** Zugangsdaten im **verschlüsselten NVS**. Auf dem ESP32 (klassisch) gilt das Schema mit Flash-Verschlüsselung: Partition `nvs_keys`, Flash Encryption ist Voraussetzung (Q21). Ein HMAC-Schema für den klassischen ESP32 ist nicht belegt [verif.]. **Flash Encryption (Release-Modus) + Secure Boot V2** aktivieren, wie von Espressif für die Serie empfohlen. Beides ist im Release-Modus irreversibel (Q20). **Schlüssel je Gerät eindeutig** (Q19). JTAG und UART-Download werden dadurch eingeschränkt.
- Restrisiko: Wer physisch an die Platine gelangt, kann im schlimmsten Fall die Gerätezugangsdaten auslesen. Das erlaubt **keine** Befehle, denn das Gerät darf nicht in `commands` schreiben. Es erlaubt nur falsche Statusmeldungen. Gegenmaßnahme: Benutzer sperren und Passwort neu setzen.

### 7.2 Realtime oder Polling (Free Tier)

| Limit Free | Wert | Quelle |
|---|---|---|
| Realtime gleichzeitige Verbindungen | 200 | S4 |
| Realtime-Nachrichten | 2 Mio./Monat, 100/s | S4 |
| Edge-Function-Aufrufe | 500 000/Monat | S5 |
| Pausieren | bei zu geringer DB-Aktivität in 1 Woche | S6 |

Bewertung: Die Kontingente sind für 1 Gerät und wenige Browser unkritisch. **Empfehlung: Phase 1 HTTPS-Polling per RPC alle 5 s** (Latenz ≤ 5 s ist akzeptabel, robust, keine Socket-Wiederaufnahme). Das hält das Projekt aktiv (R2-M8). **Phase 2 optional Realtime Broadcast** auf einem privaten Kanal `device:<id>`, nur als „Weckruf“: der Befehl selbst wird weiter per RPC abgeholt. RLS auf `realtime.messages`, öffentlichen Zugriff in den Realtime-Einstellungen abschalten (S3).

### 7.3 RLS-Skizze (SQL, nicht getestet)

```sql
-- Zuordnung Mensch ↔ Gerät
create table public.devices (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  device_user uuid unique references auth.users,          -- Device-User
  night_from timestamptz, night_to timestamptz,            -- vom Gerät täglich gemeldet (Astro)
  last_seen timestamptz
);
create table public.device_members (
  device_id uuid references public.devices on delete cascade,
  user_id   uuid references auth.users on delete cascade,
  role text not null check (role in ('owner','operator')),
  primary key (device_id, user_id)
);
create type public.cmd_kind as enum ('open','close','stop','ota','reboot');
create table public.commands (
  id uuid primary key default gen_random_uuid(),           -- Nonce
  device_id uuid not null references public.devices,
  kind public.cmd_kind not null,
  night_confirm boolean not null default false,
  created_by uuid not null default auth.uid(),
  created_at timestamptz not null default now(),
  expires_at timestamptz not null default now() + interval '60 seconds',
  status text not null default 'pending'
    check (status in ('pending','taken','done','rejected','expired')),
  result text, taken_at timestamptz, done_at timestamptz
);
alter table public.devices        enable row level security;
alter table public.device_members enable row level security;
alter table public.commands       enable row level security;

create function public.is_member(d uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.device_members m
                 where m.device_id = d and m.user_id = (select auth.uid()));
$$;

-- MFA als restriktive Klammer (S2)
create policy cmd_mfa on public.commands as restrictive to authenticated
  using ((select auth.jwt()->>'aal') = 'aal2')
  with check ((select auth.jwt()->>'aal') = 'aal2');
-- zusätzlich Zugehörigkeit (R2-K1)
create policy cmd_ins on public.commands for insert to authenticated
  with check (public.is_member(device_id) and created_by = (select auth.uid()));
create policy cmd_sel on public.commands for select to authenticated
  using (public.is_member(device_id));
-- kein UPDATE/DELETE für authenticated → Status nur über Geräte-RPC

-- Server erzwingt Ablaufzeit, Rate-Limit, Nachtsperre
create function public.commands_guard() returns trigger
language plpgsql security definer set search_path = '' as $$
declare dv public.devices; totp_ts bigint;
begin
  new.created_at := now(); new.expires_at := now() + interval '60 seconds';
  new.status := 'pending'; new.created_by := auth.uid();
  if exists (select 1 from public.commands c where c.device_id = new.device_id
             and c.created_at > now() - interval '5 seconds') then
    raise exception 'rate limit';
  end if;
  select * into dv from public.devices where id = new.device_id;
  if new.kind = 'open' and now() between dv.night_from and dv.night_to then
    select max((e->>'timestamp')::bigint) into totp_ts
      from jsonb_array_elements(auth.jwt()->'amr') e where e->>'method' = 'totp';
    if not new.night_confirm or coalesce(totp_ts,0) < extract(epoch from now()) - 300 then
      raise exception 'Nachtsperre: Bestaetigung + TOTP < 5 min erforderlich';
    end if;
  end if;
  if new.kind = 'ota' and not exists (select 1 from public.device_members m
       where m.device_id = new.device_id and m.user_id = auth.uid() and m.role = 'owner') then
    raise exception 'OTA nur owner';
  end if;
  return new;
end $$;
create trigger commands_guard before insert on public.commands
  for each row execute function public.commands_guard();

-- Gerät holt atomar genau einen gültigen Befehl (Replay-/Doppelausführungsschutz)
create function public.device_take_command() returns setof public.commands
language plpgsql security definer set search_path = '' as $$
declare d uuid;
begin
  select id into d from public.devices where device_user = auth.uid();
  if d is null then raise exception 'not a device'; end if;
  update public.devices set last_seen = now() where id = d;
  update public.commands set status = 'expired'
   where device_id = d and status = 'pending' and expires_at < now();
  return query
  update public.commands set status = 'taken', taken_at = now()
   where id = (select id from public.commands
               where device_id = d and status = 'pending' and expires_at >= now()
               order by created_at limit 1 for update skip locked)
  returning *;
end $$;
-- analog: device_ack(p_id uuid, p_ok boolean, p_result text), device_report(p_state jsonb, p_night_from, p_night_to)
revoke all on function public.device_take_command() from public, anon;
grant execute on function public.device_take_command() to authenticated;
```
Der Aufbau des `amr`-Claims (Array aus `method` und `timestamp`) ist dokumentiert (S7). Die Auswertung im Trigger ist zu testen. Die `aal2`-Policy muss **jede** Tabelle mit Steuerwirkung abdecken (`schedules`), siehe Hinweis in S2.

### 7.4 Nachtsperre
- Zweistufig: **(1) Server**: Trigger nach 7.3 (Bestätigung + TOTP-Anmeldung jünger als 5 min). **(2) Gerät**: lokal berechnete Astro-Nacht. Ein Fern-`open` nachts wird nur ausgeführt, wenn `night_confirm = true`. Ohne gültige Uhrzeit (RTC und NTP ungültig) wird ein Fern-`open` immer abgelehnt.
- Die Gerätestufe ist maßgeblich, weil die Serverstufe durch eine Kompromittierung von `service_role` umgangen werden kann.
- Der Vor-Ort-Taster bleibt immer wirksam.

### 7.5 Replay-Schutz
- Nonce = `commands.id` (UUID). Gültigkeit 60 s, **vom Server gesetzt** und in der RPC gegen die Serverzeit geprüft. Das Gerät braucht dafür keine eigene Uhr.
- Ein Befehl wird nur einmal ausgeführt: Statuswechsel `pending → taken` atomar (`for update skip locked`). Das Gerät führt zusätzlich einen Ringpuffer der letzten 32 IDs im RAM.
- Ein abgelaufener Befehl wird nicht ausgeführt. Die App meldet „verfallen“ und fordert einen erneuten Befehl.
- Optional bei erhöhtem Schutzbedarf: Befehl über eine Edge Function mit Ed25519 signieren. Das Gerät prüft mit dem öffentlichen Schlüssel im Flash. Das schützt auch bei kompromittierter DB **[A]**.

### 7.6 OTA
- ESP-IDF `esp_https_ota` mit 2 OTA-Partitionen (8 MB Flash) und **App-Rollback** (`CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE`). Selbsttest nach dem Booten: UART-Antwort des TMC, Eingänge plausibel, I²C-Geräte vorhanden, WLAN. Danach `esp_ota_mark_app_valid_cancel_rollback()` (Q22).
- **Secure Boot V2** prüft die Signatur. **Anti-Rollback** (`CONFIG_BOOTLOADER_APP_ANTI_ROLLBACK`, Security-Version in eFuse) verhindert das Zurückspielen alter, signierter Versionen mit bekannter Lücke (Q22).
- Quelle: privater Supabase-Storage-Bucket, Download per Signed URL, die nur die RPC an den Device-User ausgibt. Auslösung nur über `commands.kind = 'ota'` (Owner, `aal2`). Ausführung nur im Zustand **ZU_VERRIEGELT** oder AUF im Stillstand, nie während einer Fahrt, und tagsüber **[A]**.
- Den Signierschlüssel offline aufbewahren (nicht in Vercel oder Supabase).

---

## 8 Empfehlungen (priorisiert)

1. RLS um die Gerätezugehörigkeit ergänzen und die Registrierung abschalten (R2-K1).
2. Richtungsselektive Hardware-Sperre und getestete Lichtschranke umsetzen, B1 plausibilisieren (R2-K2, R2-K3).
3. HDR-100-24 einsetzen und auf 24,0 V einstellen. TMC-VM-Beschaltung nach R2-M2, Wechsel auf TMC2240 prüfen.
4. DS3231SN, ESP32-WROOM-32UE-N8 und ISO1212 einplanen. Lux mit PCA9615 oder hinter einem Fenster im Gehäuse.
5. Heizung 24 V/20 W mit Temperatur- und Feuchtefühler sowie Bimetall-Begrenzer.
6. Gerätezugang nach Variante A, Polling per RPC 5 s, Flash Encryption + Secure Boot V2 + verschlüsseltes NVS, schlüssel je Gerät eindeutig.
7. Reparaturschalter -Q1 wieder ins Konzept aufnehmen.
8. Offen beim Bauherrn: tiefste Standorttemperatur, Gehäusegröße, Leitungslängen zu +M, +R und +A.

---

## 9 Quellen

Elektro/Elektronik:
- Q1 Mean Well HDR-100 Spezifikation (Derating-Kurve −30…70 °C, 2000 m): https://static6.arrow.com/aropdfconversion/15fafb9a9b059401b7a0042556fc945429eb11f4/hdr100spec.pdf ; https://assets.rs-online.com/v1699022686/Datasheets/cd71cd59b00f20c99cbb6477ad6bb984.pdf
- Q2 HDR-100-24 (92 W, −30…+70 °C, lüfterlos), Händler: https://www.bravoelectro.com/hdr-100-24.html
- Q3 HDR-60-24 (60 W, 2,5 A, −30…+70 °C, EN 61558): https://www.bravoelectro.com/hdr-60-24.html ; https://static6.arrow.com/aropdfconversion/73dc421abba22053424d277a12937056b6de4d27/hdr60spec.pdf
- Q5 TMC2209 (4,75–29 V, 2 A RMS, 2,8 A Spitze, UART, StallGuard4): https://www.analog.com/en/products/tmc2209.html ; https://wcm-cce.cldnet.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.08.pdf
- Q6 TMC2240 (4,5–36 V, ≈ 2 A RMS): https://www.analog.com/en/products/tmc2240.html
- Q7 ESP32-WROOM-32E/32UE Datenblatt (−40…85/105 °C, U.FL): https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.pdf
- Q8 Mouser ESP32-WROOM-32 Varianten (UE-H4 105 °C): https://www.mouser.in/new/espressif/espressif-esp32-wroom-32-modules/
- Q9 DS3231 Datenblatt (S: 0…70 °C, SN: −40…85 °C; ±2 ppm 0…40 °C, ±3,5 ppm −40…85 °C): https://www.analog.com/en/products/DS3231.html ; https://courses.physics.illinois.edu/PHYS371/sp2023/code/DS3231.pdf
- Q10 VEML7700 (−25…+85 °C, I²C 0x10): https://www.vishay.com/docs/84286/veml7700.pdf ; https://cdn.sparkfun.com/assets/8/7/4/4/1/VEML7700_Application_Note.pdf
- Q11 NXP PCA9615 (differenzielles I²C, max. 3 m): https://www.nxp.com/products/analog/interfaces/ic-bus/ic-bus-repeaters-hubs-extenders/2-channel-multipoint-fast-mode-plus-differential-i2c-bus-buffer-with-hot-swap-logic:PCA9615DP ; https://www.farnell.com/datasheets/4000002.pdf
- Q12 TI ISO1211/ISO1212 (IEC 61131-2, 2,2–2,47 mA): https://www.ti.com/product/ISO1212 ; https://www.ti.com/lit/pdf/SLLSEY7 ; https://ti.com/lit/SLLA370
- Q13 Marantec Einweg-Lichtschranke 99165 (12–24 V AC/DC, IP65, −20…60 °C, 10 m): https://shop.marantec.com/eu_en/through-beam-photoelectric-sensor-12-24-v-ac-dc-99165-eu-en.html ; Sommer Einweg (IP55, −10 °C): https://www.tor7.de/sommer-einweg-lichtschranke-20m-4-draht-batteriebetrieben
- Q14 ASO SENTIR edge (8,2 kΩ ± 500 Ω, betätigt ≤ 500 Ω): https://venusautomation.com.au/wp-content/uploads/2022/01/Sentir-Edge-25.45-TT-Instructions.pdf ; ASO INDUS/ELMON (8,2 kΩ, Kat. 3, PL e): https://www.manualslib.de/manual/158021/Indus-Classic-74-312.html?page=21 ; Sensotek SAE-41-312-A: https://www.sensotek.com/en/SAE-41-312-A/10001393
- Q15 DIN EN 12453 (Nutzungssicherheit kraftbetätigter Tore), EN 12978 (Schutzeinrichtungen): https://www.din.de/de/mitwirken/normenausschuesse/nasg/veroeffentlichungen/wdc-beuth:din21:349956830 ; https://standards.iteh.ai/catalog/standards/cen/d5270547-aac4-4266-9db2-86e518016015/en-12978-2024 [N-verif.]
- Q16 IEC 61496-1, ESPE Typ 2 = PL c mit periodischem Test: https://www.pilz.com/en-INT/iec-en-61496-1
- Q17 Heizleistung: Rittal Q = A·ΔT·k, Stahl k = 5,5, außen verdoppeln: https://www.rittal.com/imf/none/3_962 ; Polyester k = 3,5, A nach IEC 60890: https://treesoft.de/wp-content/uploads/dokumente/DE_BerechnungSchaltschrankklimatisierung-6.pdf
- Q18 ESP-IDF GPIO (Strapping 0/2/5/12/15, GPIO34–39 nur Eingang ohne Pull-up): https://docs.espressif.com/projects/esp-idf/en/v5.1.2/esp32/api-reference/peripherals/gpio.html
- Q19 Espressif Security Advisory Fault Injection / eFuse (CVE-2019-17391, Abhilfe ESP32-D0WD-V3, Schlüssel je Gerät): https://espressif.com/en/news/Security_Advisory_Concerning_Fault_Injection_and_eFuse_Protections ; https://nvd.nist.gov/vuln/detail/CVE-2019-17391
- Q20 Flash Encryption + Secure Boot V2 (Empfehlung, Irreversibilität, ab ESP32 v3.0): https://docs.espressif.com/projects/esp-idf/en/v5.1/esp32/security/security.html ; https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/security.html ; https://developer.espressif.com/blog/flash-encryption-and-secure-boot/
- Q21 NVS-Verschlüsselung (Schema mit Flash Encryption, `nvs_keys`): https://docs.espressif.com/projects/esp-idf/zh_CN/v5.5/esp32/api-reference/storage/nvs_encryption.html
- Q22 OTA, Rollback, Anti-Rollback: https://docs.espressif.com/projects/esp-idf/en/v4.4.8/esp32c3/api-reference/system/ota.html ; https://developer.espressif.com/workshops/introduction-to-esp32-s31-security/assignment-5/
- Normen [N-verif.]: DIN VDE 0100-410 (414 SELV), -430, -443, -540, -600; DIN EN 60898-1; DIN EN 61558-2-16; DIN EN IEC 62368-1; DIN EN IEC 81346-1/-2; IEC 60890; DIN EN ISO 13849-1.

Supabase:
- S1 Supabase MFA (aal/aal2): https://supabase.com/docs/guides/auth/auth-mfa
- S2 MFA über RLS, restriktive Policy, Grenzen (Storage, security definer, service_role): https://supabase.com/blog/mfa-auth-via-rls ; https://supabase.com/docs/guides/auth/auth-mfa
- S3 Realtime Authorization (RLS auf `realtime.messages`, `private: true`, öffentlichen Zugriff abschalten): https://supabase.com/docs/guides/realtime/authorization
- S4 Realtime Limits/Pricing (Free: 200 Verbindungen, 100 Nachr./s, 2 Mio./Monat): https://supabase.com/docs/guides/realtime/limits ; https://supabase.com/pricing
- S5 Edge Functions (Free 500 000 Aufrufe/Monat): https://supabase.com/docs/guides/functions/pricing ; https://supabase.com/docs/guides/platform/manage-your-usage/edge-function-invocations
- S6 Pausieren von Free-Projekten: https://supabase.com/docs/guides/platform/project-pausing ; https://github.com/orgs/supabase/discussions/13121
- S7 JWT-Claims (`amr` mit method/timestamp): https://supabase.com/docs/guides/auth/jwt-fields
