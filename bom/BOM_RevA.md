# Entenklappe „DuckDoor“: Stückliste (BOM) Rev. A, Entwurf

Stand: 23.11.2026 · Rolle: Einkauf/Arbeitsvorbereitung · Grundlage: `docs/02_Freigabestand_v2.md` (verbindlich, Auslegung −10 °C), `drawings/TZ_Positionsliste.csv`, `electrical/EL_Betriebsmittelliste.csv`, `electrical/EL-03_Klemmenplan.csv`, `docs/review/05_Einkauf_Montage.md`, `docs/review/12_R2_Elektro_IT.md`.

**Dateien**
- `BOM_RevA.csv`: Gesamtstückliste mit 100 Positionen (Pos. 010 bis 1000). Trennzeichen `;`, UTF-8, Dezimalkomma.
- `PCB_BOM_RevA.csv`: Bestückliste der Steuerplatine -A1 mit 47 Zeilen, inklusive Leiterplattenfertigung. In der BOM ist sie in zwei Summenzeilen (PLATINE) enthalten.

Alle Preise sind brutto inkl. 19 % MwSt., ohne Versand, Momentaufnahme vom 23.11.2026. Nettopreise der Distributoren (Digi-Key, Mouser, RS, Farnell) sind mit dem Faktor 1,19 umgerechnet.

Status:
- **belegt**: Preis aus einer Händlerquelle (Websuche).
- **Annahme**: Preis geschätzt, Typ oder Menge von uns angenommen.
- **Typ offen**: Typ in der E-Planung noch nicht festgelegt. Der genannte Typ ist nur ein Vorschlag.

---

## 1 Summen je Baugruppe

| Baugruppe | Inhalt | Summe € brutto |
|---|---|---:|
| MECH | Fundament, Pfosten, Führung, Schieber, Kanal, Antriebskasten, Klinke, Warnschilder | 707,45 |
| ANTRIEB | Schrittmotor, Spindel, Mutter, Lagerung, Kupplung, Motorplatte | 145,47 |
| BEFESTIGUNG | Verbundanker, Sicherheitsschrauben, Kleinteile A4, Zaun- und Kastenbefestigung | 219,20 |
| ELEKTRO-230V | Schaltkasten IP66, -Q1, -F1, -T1, -X1, -X0, DAE, Berührungsschutz | 317,43 |
| ELEKTRO-24V | -F11…-F15, -X2, Auswerter -K1, Heizung -E1/-B10, Taster, LED, Antenne mit Pigtail | 328,02 |
| PLATINE | -A1: Bauteile 101,45 € + Leiterplatte/Schablone 40,00 € (siehe PCB_BOM) | 141,45 |
| FELD | B1–B4, Lichtschranke B6 (2 Sätze), Schaltleiste B7, B8, B9 | 381,96 |
| LEITUNG | W1 bis W30, Motorsteckverbinder, Kabelverschraubungen | 213,75 |
| CLOUD | Vercel Hobby, Supabase Free | 0,00 |
| **Gesamt Material** | | **2.454,73** |
| Reserve 10 % (Versand, Mindermengen, Verschnitt), Empfehlung | | ≈ 245 |
| **Gesamt inkl. Reserve** | | **≈ 2.700** |

**Belegqualität (BOM):** 482 € (20 %) sind belegt, 1.273 € (52 %) sind Annahmen und 700 € (28 %) entfallen auf Positionen mit offenem Typ. Die größten unbelegten Posten sind:
- Lichtschranke Marantec 99165: 2 × 80 €, kein Händlerpreis gefunden.
- Auswerter -K1: 120 €.
- Schaltkasten: 137 €.
- Blechteile und Frästeile der Mechanik.

Nicht enthalten sind die Eigenleistung, die Elektrofachkraft (Anschluss und Prüfung nach VDE 0100-600) und die Bestandsgeräte in +UV (-F0 RCD 30 mA, -F01).

---

## 2 Annahmen und offene Typen (Auswahl, alle Einzelheiten in den CSV-Dateien)

| Nr | Punkt | Wirkung |
|---|---|---|
| A1 | **Auswerter -K1 Sensotek SAE-41-312-A:** Laut Herstellerdatenblatt (Art. 10001393) ist die Versorgung **230 V AC**. EL-03 speist -K1 aber über -F15 mit **24 V DC**. Benötigt wird eine 24-V-Variante (z. B. ELMON relay 41-312 in 24-V-Ausführung), sonst wechselt -K1 in den 230-V-Bereich. | **Klären vor Bestellung**, Typ offen |
| A2 | **Schaltleiste -B7:** Die Länge ist widersprüchlich: TZ Pos. 14 nennt L 340, die Betriebsmittelliste L 400 mm. Angesetzt ist 400 mm (Sensotek SE 25.30 TT „ab 73,01 €“). Ob der Preis netto oder brutto ist, ist unklar. | Länge mit der Mechanik festlegen |
| A3 | **Lichtschranke -B6:** Nach TZ Pos. 48 (2 Strahlen) sind 2 Sätze angesetzt. Im Klemmenplan ist nur 1 Satz verdrahtet. Annahme: Empfängerkontakte in Reihe an -X2:34/35, Sender parallel an -X2:30. Für 99165 wurde kein Preis gefunden (Schätzung 80 €/Satz). Kabel sind vormontiert (12 m/3 m), deshalb sind -W16/-W17 nur als Reserve angesetzt. | Klemmenplan ergänzen; Preis anfragen |
| A4 | **DC/DC -A1.U14:** Angesetzt ist TRACO TSR 1-2450 (Vin 6,5–36 V). Die Klemmspannung der SMBJ33A (≈ 53 V) liegt über Vin max. Nötig ist entweder ein DC/DC mit Vin ≥ 60 V oder ein anderes TVS- und Filterkonzept. Typ offen lt. EL. | PCB-Entwurf |
| A5 | **Leitungslängen:** -W1 ist mit 25 m angenommen (offen lt. EL). Die Feldleitungen sind mit 3 bis 5 m angenommen, weil +K1 nahe an der Klappe sitzt. | Aufmaß vor Ort |
| A6 | **Endlagen B1–B4:** M12-Ausführung mit Steckerabgang; -W12…-W15 als konfektionierte PUR-Leitungen 5 m. Den Temperaturbereich ≥ −25 °C am Datenblatt bestätigen. | [verif.] |
| A7 | **B8:** Reedkontakt mit Magnet (TZ Pos. 47) statt Mikroschalter. Als 2-Leiter-Ausführung ist -X2:44 Reserve. | – |
| A8 | **Spindel und Mutter:** Bezug von igus angenommen. Der Preis von 18,10 €/m ist ein Spannenpreis, die Verfügbarkeit von Tr8×2 in Edelstahl ist nicht bestätigt. Zapfenbearbeitung mit 25 € geschätzt. | Angebot igus |
| A9 | **Fertigteile Mechanik** (Pos. TZ 5, 8–11, 13, 15, 17, 18, 21, 26, 28, 31, 33, 35, 36, 39, 41, 42): Schätzpreise für Zuschnitt, Kanten und Fräsen. Die Lohnverzinkung ist mit einer Pauschale von 60 € angesetzt. | Sammelangebot Blech- und Zerspanungsbetrieb |
| A10 | **-Q1, -F1:** Typen Schneider iSW A9S60220 und Hager MBN506 angenommen. Für -F1 gilt laut Hager-Liste 51,20 € netto; angesetzt ist ein Straßenpreis von 20 € (Schätzung). Den Einschaltstrom von -T1 bei B6 prüfen (sonst C6). | Typ offen |
| A11 | **Heizung -E1:** Schneider ClimaSys NSYCR20WU1C (12–24 V DC, 20 W) angenommen, Preis geschätzt. Bimetall KSD301 40 °C angenommen. | Typ offen |
| A12 | **Antenne -B20 / Pigtail -W20:** Siretta Tango 25 (2 dBi) und RS PRO 150 mm angenommen. Den Gewinn gegen das RED-Zertifikat des ESP32-WROOM-32UE prüfen. | [verif.] |
| A13 | **PCB:** Größe ≈ 120×100 mm angenommen (über 100×100 mm gilt nicht der Einstiegspreis von JLCPCB). Bestückung von Hand durch den Bauherrn. Die Widerstandswerte für ISO1212 Typ 3 (R_SENSE/R_THR) nach Datenblatt SLLSEY7 festlegen. | [verif.] |
| A14 | **Cloud:** Vercel Hobby ist nur für nicht-kommerzielle Nutzung zugelassen. Supabase Free: Limits und Pausierung am Original prüfen (O4). Beide sind mit 0 € angesetzt, wie vorgegeben. | – |
| A15 | **Fundament:** 17 Sack Trockenbeton C25/30 à 25 kg (≈ 12,5 l Frischbeton je Sack, 0,192 m³ + 10 %). Bewehrung und Schalung sind nicht angesetzt. | Statik/Errichter |

---

## 3 Abgleich-Protokoll

### 3.1 Doppelungen entfernt
| Quelle | Befund | Behandlung |
|---|---|---|
| TZ 14, 30, 43–48 („E-Stückliste“) | Diese Positionen sind auch als BMK in der Betriebsmittelliste geführt (-B7, -M1, -B1…-B4, -B8, -B6). | Jeweils nur **eine** Zeile (Baugruppe ANTRIEB bzw. FELD) mit beiden Kennzeichen, z. B. „-B7 (TZ 14)“. |
| TZ 37 / EL -U1 „mit DAE“ | Es handelt sich um zwei **verschiedene** Gehäuse: Antriebskasten und Schaltkasten. | Keine Doppelung, deshalb 2 DAE (Pos. MECH und ELEKTRO-230V). |
| EL -A1.U1…U15, -B5 | Bauteile der Platine | Nur in `PCB_BOM_RevA.csv`. Die BOM enthält davon nur die Summenzeilen PLATINE. |
| -W16/-W17 vs. vormontiertes Kabel Marantec 99165 | Das Kabel ist bereits im Lieferumfang der Lichtschranke. | Nur 10 m Reserve PUR 4×0,5 statt eigener Leitungen. |
| Review 05 (Runde 1) | Shelly 2PM, Add-on, Rohrmotor, Gurt, Lux-Messumformer 0–10 V, HDR-15-24, Linearantrieb, PE-HD-Schieber, Alu-U-Führung, Einschlaghülsen | **Entfallen:** alte Variante (v0), ersetzt durch v2. Übernommen wurden nur Preise für DAE M12, Skintop-Verschraubungen, Reedkontakt und Tasterschätzung. |
| PCA9615 / Lux außen (Review 12) | Durch Freigabestand E5 überholt: Lux-Sensor hinter dem Deckelfenster, kein I²C-Außenkabel | Nicht aufgenommen, ebenso -W19. |
| -F0, -F01 (EL) | Bestand in +UV, nicht im Lieferumfang | Nicht aufgenommen. Nachweis durch den Errichter. |

### 3.2 Lücken ergänzt
| Ergänzung | BOM-Bereich |
|---|---|
| Fundamentbeton C25/30 (17 Sack), Injektionsmörtel für Verbundanker, Lohnverzinkung Pfosten und Fußplatten | MECH / BEFESTIGUNG |
| Kleinteilesatz A4 (Schrauben, Muttern, Scheiben, Niete), Bit für Sicherheitsschrauben, Zaun-Spannschellen, Befestigung +K1 am Pfosten, Sensorwinkel M12, UV-Kabelbinder | BEFESTIGUNG |
| Kabelverschraubungen M20/M16-EMV/M12 (22 Stk), Verschlussstopfen, Kabelschutzrohr und Warnband für -W1, verriegelbarer Motorsteckverbinder (R2-G6) | LEITUNG |
| Zweites Druckausgleichselement (Schaltkasten), Montageplatte mit Hutschiene, Lichtfenster im Deckel, Berührungsschutz Netzbereich, PE- und Trennplatten -X1 | ELEKTRO-230V |
| Feinsicherungen 5×20 mit Ersatzsatz, Klemmenzubehör -X2 (0-V-Kamm, Endhalter, Beschriftung), Antenne -B20 und Pigtail -W20, Platinenträger, BMK-Schilder | ELEKTRO-24V |
| Strahlungsschutz für -B9 (beschattete Montage) | FELD |
| Warnschilder (TZ 50, 2 Stk) | MECH |
| PCB: Buchsenleisten TMC-Modul, CR2032 und Halter, ESD 1-Wire, PTC für LS_TX und B9, SMD-Sicherung 24V_IN, LC-Filter, 470 µF VM, Auto-Reset, Programmierheader, USB-UART-Adapter, SMD-Schablone, Leiterplattenfertigung | PLATINE |

### 3.3 Vollständigkeitsprüfung
- **TZ_Positionsliste:** Pos. 1–50 sind vollständig zugeordnet. Pos. 2 (2 Gitter) ist als 1 Rolle 5 m beschafft, Pos. 6 (8 Anker) als 1 VPE à 10 Stück.
- **EL_Betriebsmittelliste:** Alle BMK außer dem Bestand -F0/-F01 sind zugeordnet. Zusätzlich zur Aufgabenliste wurden -A1.U8 SHT4x und -A1.U10 TCA9534 aus der Betriebsmittelliste in die PCB_BOM übernommen.
- **EL-03 Klemmenplan:** -X2 hat 36 Klemmpunkte. Angesetzt sind 46 Klemmen, davon 10 für 0 V, plus Brückenkamm. -X1 hat 4 Klemmen plus PE.

---

## 4 Offene Punkte für den Einkauf (Priorität)
1. -K1: 24-V-Ausführung bestätigen und Angebot einholen (A1).
2. Angebot für Marantec 99165 (2 Sätze); Klemmplan für den zweiten Satz ergänzen (A3).
3. Länge der Schaltleiste -B7 (340 oder 400 mm) und Bezugsquelle ASO/Sensotek festlegen (A2).
4. Sammelanfrage Blech, Laser und Zerspanung (A9); Anfrage Spindel und Mutter bei igus (A8).
5. Typ DC/DC und TVS-Konzept auf -A1 festlegen (A4); danach die PCB-Größe einfrieren und bestellen.
6. Aufmaß der Leitungslängen und des Standorts +K1 (A5).
