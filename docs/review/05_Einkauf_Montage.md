# Review 05 – Einkauf/Kalkulation & Montage

Prüfgegenstand: `docs/00_Konzept_v0.md` (Entenklappe DuckDoor, v0)
Rolle: Einkauf/Kalkulation, Montageleitung
Stand Recherche: 23.11.2026, Websuche (Suchmaschinen-Auszüge von Händlerseiten). Preise brutto inkl. MwSt., ohne Versand, Momentaufnahme. Die Herstellerseite shelly.com war aus der Recherche-Umgebung nicht direkt abrufbar; die Shelly-Angaben stammen aus Suchauszügen von shelly.com und Händlern.
Kennzeichnung: **[A]** = Annahme, **Schätzung** = kein Preis belegt.

---

## 1 Befunde

| Nr | Befund | Bewertung | Empfehlung |
|---|---|---|---|
| E1 | **Shelly Plus 2PM (Gen2)** ist nur noch als Restposten/Deal zu finden (Gen2 ca. 19,50 €). Aktuell: **Shelly 2PM Gen3** (ca. 18–26 €) und **Shelly 2PM Gen4** (ca. 22–30 €). | Info | Gen3 beschaffen (günstigster Stückpreis, Add-on am ehesten belegt). |
| E2 | **Add-on-Kompatibilität ist nicht eindeutig belegt.** Gen3 und Gen4 2PM haben laut Shelly-Doku eine Add-on-Schnittstelle („proprietary serial interface“). Die Add-on-Kompatibilitätslisten widersprechen sich je nach Länderseite: Einige nennen den 2PM Gen3 bzw. den 2PM Gen4, andere nur 1/1PM/i4/Dimmer Gen3 bzw. 1/1PM Gen4. | **Hoch (Projektrisiko)** | Vor Serienkauf 1 Satz 2PM Gen3 und Plus Add-on beschaffen und im **Cover-Modus** testen: Voltmeter 0–10 V und Digitaleingang gleichzeitig. Ausweichlösung: Plus 2PM Gen2 (Add-on sicher unterstützt) oder ein zweites Gerät (Shelly 1 Gen3 + Add-on) nur für die Sensorik. |
| E3 | An der Add-on-Schnittstelle des 2PM Gen3/Gen4 liegt **Netzspannung** an (Herstellerhinweis). Das Add-on ist galvanisch getrennt. | Mittel | Add-on nur im spannungsfreien Zustand stecken. Sensorleitungen (Lux, Reed) **nur über das Add-on** führen, nie direkt an den 2PM. |
| E4 | Der 2PM ist ein **Unterputzgerät, nicht für die Hutschiene**. Mit gestecktem Add-on wird er höher. | Mittel | Auf einer Montageplatte befestigen oder einen Hutschienen-Halter (Zubehör/Drittanbieter, **Schätzung**) verwenden. Gehäuse mit ≥ 110 mm Einbautiefe wählen. |
| E5 | **SW1/SW2 führen 230 V** (Tastereingänge am 2PM gegen L). | Mittel | Taster für 230 V AC ausgelegt und IP67, Leitung H07RN-F bzw. im Gehäuse. Kein Kleinspannungstaster. |
| E6 | **„Rohrmotor Ø35“** heißt im Handel „Mini“-Baureihe: Motorrohr Ø35 mm für **Achtkantwelle SW40**. Ein 35-mm-Motor für eine 35-mm-Welle ist nicht marktüblich. Kleinster Typ: **6 Nm** (Zugkraft 15 kg). | Info | Schellenberg Standard Mini 6 Nm (Art. 20106) oder gleichwertig (Rademacher RolloTube Basis Small). Welle SW40. |
| E7 | Die Mini-Rohrmotoren sind laut Händlerangaben nur **IP44**. Für die Standard-Linie ist **keine Bremse dokumentiert**, für die Plus-Linie wird eine „starke Bremse“ genannt. | **Hoch** | Den Antriebskasten regendicht ausführen (Tropfkante, Deckel überlappend, Entwässerung unten). Für den Aufhebelschutz (Konzept 2.1) **Plus Mini 6 Nm** (Art. 20406) wählen und die Bremse am Datenblatt bestätigen lassen. |
| E8 | Drehmomentreserve: Schieber ≈ 21 N, Wickelradius ≈ 25 mm [A] ergibt ≈ 0,5 Nm. Ein 6-Nm-Motor ist 10-fach überdimensioniert. | Info | Unkritisch, weil B1 nur hebt und durch Schwerkraft schließt. Der Gurt darf **nicht fest mit dem Schieber verklemmt** sein, sondern nur ziehen. Sonst wirkt beim Zufahren keine Motorkraft, beim Anheben aber volle Kraft auf ein eingeklemmtes Tier am oberen Rand (Hub-Endlage oben mit Abstand einstellen). |
| E9 | **Führung U 20×15 mm passt nicht zur geplanten Überdeckung 25 mm.** Bei 15 mm Schenkeltiefe sind maximal ≈ 13 mm Eingriff möglich. Bei der Variante „15 breit“ bleiben innen nur 12 mm für einen 10-mm-Schieber, also 1 mm Spiel je Seite. Das ist kritisch bei Eis und Schmutz. | **Hoch** | Führung mit **lichter Weite ≥ 14 mm** und **Tiefe ≥ 25 mm**, z. B. Alu-U 30×30×2 mm, oder Überdeckung auf 12 mm reduzieren. Mit der Mechanik abstimmen. |
| E10 | **B2: Ein 520-mm-Hub erfordert einen langen Antrieb.** Eingefahrene Länge ≈ Hub + 100–150 mm [A]. Die Bauhöhe steigt um ≈ 0,6–0,7 m gegenüber B1. Der IP65-Antrieb aus dem Fachhandel (RS PRO, 300 mm Hub) kostet 439 € und hat zu wenig Hub. Günstige Marktplatz-Antriebe mit 500 mm sind ohne belastbare Daten. | Hoch | Stützt die v0-Empfehlung **B1**. |
| E11 | **B2: Koppelrelais müssen eine 230-V-Spule haben**, weil die 2PM-Ausgänge L schalten. Zusätzlich sind ein 24-V-Netzteil mit ≥ 60 W und eine Schutzeinrichtung (Schaltleiste/Auswerter) nötig. | Mittel | In der Kalkulation berücksichtigt. |
| E12 | **Lux-Sensor**: Außen geeignete 0–10-V-Messumformer (IP65, 24 V) kosten ≈ 90–110 €. Das ist der teuerste Einzelposten der Steuerung. **Shelly BLU Door/Window** hat zwar Lux, ist aber nur für innen ausgelegt (−20…+40 °C) → **nicht geeignet**. Das Add-on-Voltmeter ist mit ±5 % spezifiziert, für einen Schwellwert reicht das. | Mittel | Option prüfen: **Astro-Betrieb ohne Lux-Sensor** (spart ≈ 105–120 € inkl. Netzteil). Lux-Sensor nur, wenn der Bauherr ihn ausdrücklich will. |
| E13 | Einschlaghülsen sind für **Holzpfosten** üblich. Ein Stahlpfosten 60×60 in einer Hülse 61 mm sitzt mit Spiel und wird nur über Klemmschrauben gehalten. Die Hülsenlänge von 750 mm reicht bei bindigem Boden. | Mittel | Bevorzugt **Punktfundament** (2× ca. 30×30×80 cm, ≈ 4 Sack Fertigbeton). Hülse nur bei steinfreiem, tragfähigem Boden. |
| E14 | **PE-HD 10 mm schwarz UV-stabilisiert** ist im Zuschnitt 400×560 mm nicht als Katalogware mit Preis gefunden. | Info | Zuschnitt bei einem Kunststoffhändler anfragen. Kalkuliert ist eine **Schätzung**. |

---

## 2 Komponententabelle

Legende Variante: **G** = gemeinsam, **B1** / **B2** = nur diese Variante.

| Pos | Var | Bezeichnung | Hersteller/Typ | Menge | Richtpreis (Stk.) | Summe | Quelle |
|---|---|---|---|---|---|---|---|
| 1 | G | Schaltaktor Cover | Shelly 2PM Gen3 (Alt.: 2PM Gen4 ≈ 22–30 €; Plus 2PM Gen2 ≈ 19,50 €) | 1 | 20,00 € | 20,00 € | shelly.com/de Shop, tink.de 19,99 € |
| 2 | G | Sensor-Add-on | Shelly Plus Add-on (SHELLY_PLUS_ADD) | 1 | 14,61 € | 14,61 € | Bürklin; Geizhals ab 13,94 € |
| 3 | G | Lux-Messumformer 0–10 V, IP65 | B+B Thermo-Technik 0555 3005 (Alt.: S+S Photasgard AHKF-U 107,95 €) | 1 | 91,38 € | 91,38 € | voelkner.de |
| 4 | G | Hutschienen-Netzteil 24 V/15 W (für Lux) | Mean Well HDR-15-24 | 1 | 15,00 € | 15,00 € | eBay 11–14,49 €, Bürklin 25,69 € |
| 5 | G | Gehäuse IP65 mit Hutschiene/Montageplatte, ≈ 200×200 mm | Spelsberg AK Compact (RS 533-7206) | 1 | 42,23 € | 42,23 € | RS Components |
| 6 | G | Druckausgleichselement M12, IP68 | Helukabel M12 (Alt.: Spelsberg DA M12 19,25 €, Lapp) | 1 | 11,80 € | 11,80 € | preissuchmaschine.de |
| 7 | G | Kabelverschraubung M20 + Gegenmutter | Lapp Skintop ST-M 20×1,5 (53111420) + GMP-GL-M20 | 4 | 0,70 € | 2,80 € | elektromax24.de (100er-Pack 56,21 €) |
| 8 | G | Kabelverschraubung M12/M16 (Sensoren) | Lapp Skintop ST-M 12/16 | 3 | 1,00 € | 3,00 € | Schätzung |
| 9 | G | Reedkontakt IP67 + Betätigungsmagnet | Littelfuse (Hamlin) 59135-1-S-05-A + Magnet 57140 | 1 | 8,19 € + 4,00 € | 12,19 € | Bürklin; Magnet Schätzung |
| 10 | G | Taster IP67, 230 V, Auf/Ab, Einbau Ø22 im Deckel | Eaton M22 (Drucktaster + Kontaktelement) | 2 | 12,00 € | 24,00 € | Schätzung (Alt.: Eaton Tasterstation 2-fach IP66/67, 91,09 €, Bürklin) |
| 11 | G | Hutschiene, Klemmen, Aderendhülsen, Montageplatte | Wago 221 / 2002 o. ä. | 1 Satz | – | 20,00 € | Schätzung |
| 12 | G | Heizwiderstand Gehäuse (optional, Kondensat) | z. B. Stego/Finder, 10–20 W | 1 | – | 30,00 € | Schätzung |
| 13 | G | Leitungen H07RN-F 3G1,5 / 4G0,75, Sensorleitung LiYY | – | Satz | – | 25,00 € | Schätzung |
| 14 | G | Schieber PE-HD 10 mm, schwarz, UV-stab., Zuschnitt 400×560 | z. B. Röchling PE 300 | 1 | – | 35,00 € | Schätzung (Kaufland: 6 mm 100×90 = 72,30 €) |
| 15 | G | Führungsprofil Alu U (siehe E9) | U 20×15×1,5 (Hornbach) → besser U 30×30×2 | 2,6 m | 7,69 €/m | 20,00 € | Hornbach (20×15); 30×30 Schätzung gleiche Größenordnung |
| 16 | G | Rahmen Alu-Vierkant 40×40×2 | – | 4 m | ≈ 12 €/m | 48,00 € | Schätzung (Alberts 40×40: 48,50 €/m als Obergrenze) |
| 17 | G | Verbinder, Edelstahlschrauben A2, Nieten | – | Satz | – | 30,00 € | Schätzung |
| 18 | G | Pfosten Stahl 60×60, feuerverzinkt, 2000 mm | Doppelstabmatten-Eckpfosten 60×60 | 2 | 61,99 € | 123,98 € | Kaufland-Marktplatz |
| 19a | G | Einschlagbodenhülse 61×750 (nur bei geeignetem Boden) | Domax PSG 61×750×1,8 | 2 | 9,99 € | 19,98 € | Kaufland |
| 19b | G | alternativ Punktfundament, Fertigbeton | – | 4 Sack | 5,00 € | 20,00 € | Schätzung |
| 20 | G | Zaunanschluss (Spannschellen/Klemmen) | – | 4 | 4,00 € | 16,00 € | Schätzung |
| 21 | G | Antriebskasten/Abdeckung Alu-Blech, Wartungsdeckel | Eigenfertigung | 1 | – | 40,00 € | Schätzung |
| 22 | G | Untergrabschutz Drahtgitter verzinkt, 50 cm | – | 2 m | – | 20,00 € | Schätzung |
| **B1-1** | B1 | Rohrmotor 230 V, Ø35 (Mini), 6 Nm, mech. Endlagen | Schellenberg Standard Mini 6 Nm (20106); **empfohlen Plus Mini 6 Nm (20406)** wegen Bremse | 1 | 44,85 € (Standard) / ≈ 60 € (Plus) | 60,00 € | Hornbach (Standard); Plus: lan.de, Preis Schätzung |
| B1-2 | B1 | Achtkantwelle SW40, 1000 mm | Schellenberg Mini | 1 | 10,55 € | 10,55 € | Hornbach |
| B1-3 | B1 | Wandlager Mini (Motorlager) + Gegenlager/Kugellager | Schellenberg 83600 | 2 | 3,95 € | 7,90 € | Hornbach |
| B1-4 | B1 | Gurtscheibe Mini/Walzenhülse + Gurt 14 mm (Kunststoff, UV) | Schellenberg | 1 Satz | 1,95 € + ≈ 6 € | 8,00 € | Bauhaus; Gurt Schätzung |
| **B2-1** | B2 | Linearantrieb 24 V DC, Hub ≥ 520 mm, IP65, int. Endschalter | Marktplatzware (z. B. 1000 N IP65) / Fachhandel RS PRO 177-4513 (nur 300 mm, 438,94 €) | 1 | 90 € (Budget) – 450 € (Fachhandel) | 90,00 € | Schätzung / RS Components |
| B2-2 | B2 | Koppelrelais, Spule 230 V AC, 1 Wechsler | Finder 38.51.0.240.0060 | 2 | 10,00 € | 20,00 € | Schätzung (24-V-Variante 7,68 €, elektromax24) |
| B2-3 | B2 | Netzteil 24 V ≥ 60 W (statt Pos. 4) | Mean Well HDR-60-24 | 1 | 30,00 € | 15,00 € (Mehrpreis) | Schätzung |
| B2-4 | B2 | Schutzeinrichtung Schließkante (Schaltleiste 8k2 + Auswerter) | z. B. Gummischaltleiste + Sicherheitsrelais | 1 | – | 130,00 € | Schätzung |
| B2-5 | B2 | Befestigung Gabelkopf/Schwenklager, Edelstahl | – | 1 Satz | – | 15,00 € | Schätzung |

---

## 3 Kostenvergleich (Material, brutto)

| Block | B1 Rohrmotor + Gurt | B2 Linearantrieb |
|---|---|---|
| Steuerung/Elektrik (Pos. 1–13) | 312 € | 312 € |
| Mechanik/Gestell (Pos. 14–22, Pfosten mit Hülse) | 353 € | 353 € |
| Antrieb variantenspezifisch | 86 € | 270 € (Budget) / ≈ 630 € (Fachhandel IP65) |
| **Summe Material** | **≈ 750 €** | **≈ 935 € – 1.295 €** |
| Reserve 10 % (Kleinteile, Versand) | ≈ 75 € | ≈ 95–130 € |
| **Gesamt Material inkl. Reserve** | **≈ 825 €** | **≈ 1.030 – 1.425 €** |
| Einsparoption ohne Lux-Sensor (Astro) | − 106 € → ≈ 720 € | − 91 € (Netzteil bleibt) |

Eigenleistung ist nicht bewertet. Elektroanschluss 230 V durch eine Elektrofachkraft [A]: ≈ 2 h à 70 € = 140 € (**Schätzung**), für beide Varianten gleich.
Ergebnis: B1 ist **≈ 200–600 € günstiger**, hat weniger Teile, keine Schutzeinrichtung und eine geringere Bauhöhe.

---

## 4 Montageablauf (B1)

| Schritt | Tätigkeit | Zeit [A] |
|---|---|---|
| 0 | Vorbereitung: Muster-Test 2PM Gen3 + Add-on (E2), Zuschnittliste, Zuleitung und RCD 30 mA am Bestand prüfen | 1,5 h |
| 1 | Werkstatt: Alu-Rahmen ablängen, Führungen bohren/nieten, Antriebskasten kanten/fertigen, Entgraten | 4–5 h |
| 2 | Schieber zuschneiden lassen, Kanten fasen, Gurtanschlag und Magnet für den Reedkontakt montieren | 0,5 h |
| 3 | Schaltkasten vorverdrahten: Montageplatte, 2PM + Add-on, Netzteil, Klemmen, Taster, DAE, Verschraubungen; Isolationsprüfung | 2 h |
| 4 | Vor Ort: Lage in der Zaunlinie einmessen, Löcher graben oder Hülsen einschlagen, Pfosten lot- und fluchtgerecht setzen (2 Personen). Bei Beton 2 Tage aushärten lassen. | 2–3 h |
| 5 | Schwelle/Untergrabschutz einbauen (Gitter 50 cm horizontal, Schwelle ≤ 50 mm) | 1–1,5 h |
| 6 | Rahmen an die Pfosten schrauben, Zaun mit Spannschellen anschließen | 1,5 h |
| 7 | Welle, Rohrmotor und Lager in den Antriebskasten einbauen, Gurt an Welle und Schieber, Schieber einsetzen | 1 h |
| 8 | Schaltkasten montieren, Motorleitung, Lux-Sensor (Nord-/Schattenseite, nicht auf Stalllicht gerichtet) und Reedkontakt anschließen, Leitungen mit UV-festen Bindern sichern | 1,5 h |
| 9 | 230-V-Anschluss durch eine Elektrofachkraft, Prüfung nach DIN VDE 0100-600 (Schutzleiter, Isolation, RCD) | 1 h |
| 10 | Inbetriebnahme: mechanische Endlagen mit Einstellstift setzen (oben mit Restabstand, unten Gurt leicht schlaff), 2PM im Cover-Modus kalibrieren, Add-on-Eingänge, Zeitplan/Astro/Lux-Schwelle, Cloud und Passwort einrichten | 1,5 h |
| 11 | Funktionstest: 10 Zyklen, Hindernistest (Schieber blockiert → Gurt schlaff, Reed meldet „nicht ZU“), Aufhebeltest, Taster vor Ort; Übergabe und Doku | 1 h |

**Montagezeit gesamt B1: ≈ 19–22 h** (Werkstatt ≈ 8 h, vor Ort ≈ 11–13 h, davon ≈ 3 h mit 2 Personen), plus 2 Tage Wartezeit bei Beton.
**B2:** zusätzlich ≈ 3–4 h (Antriebskonsole, Relais-Polwende, Schaltleiste und Auswerter, Sicherheitsprüfung).

### Werkzeug
- Metall: Kapp-/Gehrungssäge mit Alu-Blatt, Akku-Bohrschrauber, Bohrer HSS 3–10 mm, Stufenbohrer (Verschraubungen M12–M20, Ø22 für Taster), Blindnietzange, Gewindeschneider M5/M6, Feile/Entgrater
- Erdbau: Spaten, Erdlochbohrer Ø200–300 oder Einschlaghilfe/Fäustel für Hülsen, Wasserwaage, Richtschnur, Maßband, Mörtelkübel
- Elektro: Abisolier- und Crimpzange (Aderendhülsen), VDE-Schraubendreher, Spannungsprüfer, Installationstester (Elektrofachkraft), Multimeter (0–10-V-Signal prüfen)
- Sonstiges: Einstellstift Rohrmotor (liegt dem Motor bei), Smartphone mit Shelly-App, Leiter

---

## 5 Offene Punkte für Einkauf
1. Musterkauf und Test 2PM Gen3 + Plus Add-on im Cover-Modus (E2), **vor** der Bestellung der übrigen Teile.
2. Datenblatt Schellenberg Plus Mini 6 Nm: Bremse und Haltemoment bestätigen (E7).
3. Führungsprofil anpassen (E9). Zuschnitt PE-HD anfragen (E14).
4. Entscheidung Lux-Sensor ja/nein (E12).
5. Bodenbeschaffenheit für Hülse oder Fundament klären (E13).

---

## 6 Quellen (abgerufen 23.11.2026, über Websuche)
- Shelly Plus Add-on Doku (Kompatibilität, Voltmeter 0–10 V): https://www.shelly.com/de/blogs/documentation/shelly-plus-add-on ; https://us.shelly.com/blogs/documentation/shelly-plus-add-on ; https://asia.shelly.com/blogs/documentation/shelly-plus-add-on
- Shelly 2PM Gen3 Doku/Shop: https://www.shelly.com/blogs/documentation/shelly-2pm-gen3 ; https://www.shelly.com/de/products/shelly-2pm-gen3-1 ; https://www.tink.de/p/shelly-2pm-gen-3-smart-wlan-2-kanal-relais-max-16a
- Shelly 2PM Gen4: https://www.shelly.com/de/products/shelly-2pm-gen4 ; https://www.billiger.de/baseproducts/117324-shelly-2pm-gen4 ; https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen4/Shelly2PMG4
- Plus 2PM Gen2 Preis: https://www.mydealz.de/deals/ibood-3x-shelly-plus-2pm-wlan-schalter-mit-energiemessung-gen2-esp32-2820230
- Plus Add-on Preis: https://www.buerklin.com/en/p/shelly/relays-accessories/shelly_plus_add/70P1279/ ; https://geizhals.at/shelly-plus-addon-a2912771.html
- Praxis Add-on-Voltmeter: https://community.simon42.com/t/erfahrungen-zum-shelly-plus-addon-dmm-dc-voltmeter-gleichspannung/74375
- Shelly BLU Door/Window: https://www.shelly.com/de/products/shelly-blu-door-window-1 ; https://shop.primeo-energie.ch/en/Wireless-window-and-door-contact-BLU-Door-Window/242618
- Rohrmotor Schellenberg Mini: https://www.hornbach.de/p/rohrmotor-standard-mini-6-nm-schellenberg-20106-zugkraft-15-kg/12297882/ ; https://lan.de/as-20406-rohrmotor-plus-mini-6-nm-fuer-40er-welle ; https://www.bauhaus.info/rollladenmotoren/schellenberg-rohrmotor-mini-plus-10/p/21779727 ; https://www.obi.de/p/7112725/schellenberg-rollladenmotor-standard-mini-6-nm
- Welle/Lager/Gurtscheibe: https://www.hornbach.de/p/wandlager-mini-schellenberg-83600/7674831/ ; https://www.bauhaus.info/rollladenzubehoer/schellenberg-gurtscheibe-mini/p/10428637 ; https://www.bauhaus.info/rollladenzubehoer/schellenberg-achtkantwellen-set-mini/p/27405349
- Lux-Sensor: https://www.voelkner.de/products/13529340/B-B-Thermo-Technik-0555-3005-Lichtsensor-12-V-24V-13mA-1-St.-L-x-B-x-H-40.7-x-59.3-x-65.7mm.html ; https://spluss.de/cdn/shop/files/AHKF__DE.pdf
- Gehäuse: https://de.rs-online.com/web/p/universalgehause/5337206
- Druckausgleich: https://www.preissuchmaschine.de/trend/DRUC/Druckausgleichselement.html?mehr=10 ; https://www.ebay.de/p/1204240821
- Kabelverschraubungen: https://www.elektromax24.de/100-st.-lapp-kabelverschraubung-skintop-st-m-20x1-5-lichtgrau ; https://buerklin.com/en/p/lapp/cable-glands/53111420/32P3056
- Netzteil: https://buerklin.com/en/p/mean-well/din-rail-power-supplies/hdr-15-24/62C1514 ; https://www.ebay.de/p/770524934
- Reedkontakt: https://buerklin.com/en/p/littelfuse/proximity-switches-reed-switches/59135-1-s-05-a/75P2285 ; https://littelfuse.com/products/magnetic-sensors-and-reed-switches/reed-sensors/59135.aspx
- Taster: https://buerklin.com/en/c/electromechanics/switches/control-and-signaling-components/control-devices-in-housings/30112115/?view=LIST
- PE-HD: https://www.kaufland.at/product/508416659/ ; https://www.roechling.com/de/industrial/werkstoffe/thermoplastics/industrial-plastics/pe/pe-hd-pe-300/play-tec-uv-stabilized-bicolor-590974
- Alu-Profile: https://www.hornbach.at/p/u-profil-aluminium-silber-15-x-20-x-1-5-mm-1-5-mm-1-m/8829199/
- Pfosten/Hülsen: https://www.kaufland.de/t/zaunpfaehle/zaunpfosten-verzinkt/~7671/ ; https://www.kaufland.de/product/544950558/
- Linearantrieb: https://at.rs-online.com/web/p/elektrische-linearantriebe/1774513 ; https://www.ebay.de/itm/205755303199
- Koppelrelais: https://www.elektromax24.de/finder-koppelrelais-38.51.7.024.0050-24vdc-1wechsler
