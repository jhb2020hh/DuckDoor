# Review 02 – Elektro (Niederspannung, DIN VDE 0100)

Gegenstand: `docs/00_Konzept_v0.md`, Kap. 2, 2.1, 4, 5.
Rolle: Elektroplanung TGA. Stand: 2026-11-23.

**Hinweis zur Quellenlage:** Direkter Abruf von shelly.com / kb.shelly.cloud war aus der Review-Umgebung gesperrt (Netzwerk-Allowlist). Herstellerangaben stammen aus Websuche-Auszügen der Shelly-Dokuseiten (Q1–Q6) und sind vor Bestellung am Original-Datenblatt bzw. der gedruckten „User and Safety Guide“ zu verifizieren. Normabschnitte sind aus Fachkenntnis zitiert, nicht am Normtext geprüft → als **[N-verif.]** markiert.

Kennzeichnung: **[A]** = Annahme, **[H]** = Herstellerangabe (Quelle), **[N]** = Norm.

---

## 1 Befunde

### 1.1 Kritisch

| Nr | Befund | Begründung / Quelle |
|---|---|---|
| E-K1 | **Betriebstemperatur Shelly Plus 2PM und Plus Add-on: −20 °C … +40 °C, 30–70 % r. F.** Freiluft-Kasten am Pfosten erreicht im Winter < −20 °C (Standortabhängig) und bei Sonne im IP65-Kasten > +40 °C; r. F. im Freien regelmäßig > 70 %, Betauung. Konzept nennt Heizung nur „ggf.“. | [H] Q2, Q3. Ohne Klimatisierung Betrieb außerhalb der Herstellerspezifikation. |
| E-K2 | **Potentialtrennung Add-on:** Shelly bezeichnet das Plus Add-on als „galvanisch getrennte Sensorschnittstelle“, nennt aber **keine Isolationsspannung / Isolationsart** (Basis/doppelt/verstärkt). Damit ist nicht belegt, dass Sensorstromkreise (Lux-Messumformer, Reedkontakt, Leitungen außerhalb des Kastens) als SELV gelten dürfen. Für Gen4 warnt Shelly ausdrücklich: „High voltage on the add-on interface when the Device is powered!“ – d. h. die Steckerleiste am Grundgerät führt Netzpotential. Montage nur spannungsfrei. | [H] Q3, Q4, Q5. Die Auffassung „Add-on nicht getrennt“ ist so **nicht** korrekt; korrekt ist: Trennung angegeben, Isolationsniveau nicht belegt. |
| E-K3 | **Tasterein­gänge SW1/SW2 des Plus 2PM liegen auf Netzpotential** (Taster schaltet L auf SW) [A, aus Anschlussbild bekannt, am Datenblatt verifizieren]. Konzept sieht „Taster IP67 am Gehäuse“ vor, ohne Spannungsangabe. Taster und Leitung müssen für 230 V AC ausgelegt sein, Betätiger isoliert (SK II-Ausführung). Keine SELV-Taster an SW1/SW2! | [A]; Q2 (Anschlussplan). |
| E-K4 | **Leitungsschutz Motorleitung 4G0,75 mm² hinter LS B16 (Bestand):** Überlastschutz nach DIN VDE 0100-430 (I_b ≤ I_n ≤ I_z) für 0,75 mm² bei 16 A nicht erfüllt; Ausnahme für Geräteanschlussleitungen nur eingeschränkt. Abhilfe: eigener LS B6 (bzw. B10) im Kasten. | [N-verif.] DIN VDE 0100-430. |
| E-K5 | **Anwendungsbereich DIN VDE 0100-705 (Landwirtschaftliche und gartenbauliche Betriebsstätten – Tierhaltung) prüfen.** Falls anwendbar: RCD ≤ 30 mA für Endstromkreise, zusätzlicher Schutzpotentialausgleich im Tierbereich, Mindestschutzart IP44 / IP35 je nach Ort, Schutz gegen Nagetiere und mech. Beschädigung. Konzept berücksichtigt das nicht. | [N-verif.] DIN VDE 0100-705. [A] Hobby-Haltung im Privatgarten – Anwendbarkeit durch Errichter zu entscheiden. |

### 1.2 Mittel

| Nr | Befund | Begründung / Quelle |
|---|---|---|
| E-M1 | RCD 30 mA „Bestand prüfen“ reicht nicht als Planungsaussage: Für Außen-Endstromkreise ≤ 32 A ist zusätzlicher Schutz durch RCD I_Δn ≤ 30 mA gefordert. Typ (A/F/B) festlegen; Shelly-Netzteil und 24-V-Schaltnetzteil → mind. Typ A. | [N-verif.] DIN VDE 0100-410, 411.3.3. |
| E-M2 | Shelly fordert Vorschaltung LS nach EN 60898-1, Char. B oder C, **max. 16 A**, Schaltvermögen **≥ 6 kA**, Energiebegrenzungsklasse 3. B10/B16 im Bestand passt, Schaltvermögen Bestand prüfen. | [H] Q6 (Wortlaut gleich für Plus 2PM / Gen4). |
| E-M3 | Plus 2PM: 10 A je Kanal, 16 A gesamt, 240 V AC, Cover-Modus für „bidirektionale AC-Motoren“, Hinderniserkennung und Sicherheitsschalter im Cover-Modus, Lasten induktiv mit RC-Glied. Für Rohrmotor Ø35 (typ. ≤ 150 W, < 1 A [A]) **geeignet**. Gegenseitige Verriegelung beider Richtungen ist im Cover-Modus firmwareseitig; **hardwareseitige Verriegelung nicht belegt** → Motorhersteller­vorgabe („nie beide Richtungen gleichzeitig“) nur per Software erfüllt. Kalibrierung setzt Stromabfall an mech. Endlage voraus → Rohrmotor mit **mechanischen** Endschaltern (keine elektronischen/Funk-Motoren). Nur **ein** Motor je Kanalpaar, keine Parallelschaltung. | [H] Q2, Q7; [A] Motorwerte. |
| E-M4 | Kondensatormotor: am jeweils nicht angesteuerten Ausgang steht über den Betriebskondensator Spannung an (Rückspeisung) [A, Fachpraxis]. Folge: Freischalten immer allpolig über -Q1, nicht über Shelly; Messgeräte bei Prüfung beachten. | [A] |
| E-M5 | Erdverlegung: Konzept nennt keine Zuleitungsart. H07RN-F ist für bewegliche Anwendung/Freiluft, nicht als Dauer-Erdkabel vorgesehen. Erdreich: **NYY-J** (oder NYCWY), Verlegetiefe ≥ 0,6 m [A, Fachpraxis], Sandbett, Trassenwarnband, Schutzrohr an Austritt/Pfosten. | [N-verif.] DIN VDE 0100-520; DIN VDE 0298-3 (Verwendung von Leitungen). |
| E-M6 | Rohrmotor-Anschlussleitung ab Werk häufig PVC (H05VV-F) [A] – nicht UV-/kältebeständig. Nur innerhalb Antriebskasten bzw. in Schutzrohr führen; Übergang auf H07RN-F über Klemmdose -X2 oder direkt im Schaltkasten. | [A] |
| E-M7 | Überspannung: Freiluft-Pfosten mit längerer Zuleitung. Risikobewertung nach DIN VDE 0100-443 fehlt. Empfehlung SPD Typ 2 in speisender UV (Bestand), optional Typ 3 im Kasten. Shelly-„overvoltage protection“ ist eine Geräteabschaltung, kein SPD. | [N-verif.] DIN VDE 0100-443, -534; [H] Q2. |
| E-M8 | Abschaltbedingung bei langer Zuleitung: Schleifenimpedanz für B16 bzw. RCD-Auslösung messtechnisch nachweisen (Erstprüfung). | [N-verif.] DIN VDE 0100-600. |
| E-M9 | Fremde leitfähige Teile: Alu-Rahmen + verzinkte Stahlpfosten im Erdreich. Bei Rohrmotor SK I wird der Rahmen über Motorgehäuse/Lager mit PE verbunden [A]. Schutzpotentialausgleich des Rahmens festlegen (bei VDE 0100-705 Pflicht). | [N-verif.] DIN VDE 0100-410, -540, -705. |

### 1.3 Gering

| Nr | Befund |
|---|---|
| E-G1 | Plus 2PM ist kein Reiheneinbaugerät → Hutschienenadapter oder Montageplatte. Add-on steckt auf dem 2PM; Bauhöhe beachten. |
| E-G2 | Gehäuse aus Polycarbonat/GFK statt Metall (WLAN-Dämpfung, Schutzisolierung). |
| E-G3 | Add-on-Kontakte: VCC max. 10 mA → Lux-Messumformer braucht separates Netzteil (im Konzept korrekt vorgesehen). [H] Q3 |
| E-G4 | Add-on Digitaleingang: „True“ −15…0,5 V, „False“ 2,5…15 V, invertierbar; Analogeingang 0–10 V, Genauigkeit ±5 %. Für Lux-Schwelle ausreichend. [H] Q3 |
| E-G5 | Kompatibilität: Plus Add-on unterstützt u. a. Plus 2PM und 2PM Gen3 (Herstellerliste); Gen4 nicht eindeutig belegt → bei Gen4 vor Kauf prüfen. [H] Q1, Q4 |
| E-G6 | „Do not install the Device where it can get wet“ (Add-on). → nur im geschlossenen, beheizten Kasten. [H] Q5 |

---

## 2 Empfehlungen

1. **Kasten klimatisieren:** PTC-Heizer 10–20 W [A] mit Thermostat (EIN < +5 °C) bzw. Hygrostat (EIN > 65 % r. F.), Druckausgleichselement unten, Kasten verschattet/hell, nicht Südseite. Ziel: Innentemperatur −20…+40 °C, r. F. < 70 % (E-K1).
2. **Gerätewahl Temperatur:** Falls Standort < −20 °C erreicht: Heizer zwingend, Alarm über Add-on-Temperaturfühler (DS18B20 an DATA, optional) [A].
3. **Add-on-Sensorkreis wie Netzpotential behandeln, bis Isolationsniveau belegt:** Sensorleitungen innerhalb des Kastens bzw. in Schutzrohr, Sensoren mit Isolierstoffgehäuse, keine berührbaren leitfähigen Teile; 24-V-Netzteil als SELV-Gerät (EN 61558-2-16 / EN IEC 62368-1) wählen; Anfrage an Shelly nach Isolationsspannung (E-K2).
4. **Taster S1/S2** für 250 V AC, IP67, Kunststoffbetätiger; Leitung im Kasten (E-K3). Alternativ Taster entfallen lassen und Shelly BLU Button (batteriebetrieben, Bluetooth) – dann keine Netzspannung am Bedienelement [A, Kompatibilität prüfen].
5. **Eigener Gerätschutz im Kasten:** -F2 LS B6, 1P+N (Motor, Shelly, Netzteil, Heizer) → Leitungsschutz für 0,75/1,0 mm², Selektivität zur B16 im Bestand (E-K4).
6. **Wartungs-/Reparaturschalter -Q1** allpolig (L+N), abschließbar, im oder am Kasten (E-M4).
7. **RCD:** Bestand Typ A, 30 mA nachweisen; falls nicht vorhanden: FI/LS-Kombi B16/30 mA Typ A in der speisenden UV (E-M1).
8. **Zuleitung Erdreich:** NYY-J 3×1,5 mm² (bei > 30 m oder Reserve: 3×2,5 mm²) [A]; ab Erdaustritt im Schutzrohr bis Kasten (E-M5).
9. **Motorleitung:** H07RN-F 4G1,0 (Reserve, mech. Robustheit) statt 4G0,75; im Freien UV-beständig, gegen Tierverbiss im Metall-Schutzschlauch.
10. **Rohrmotor-Spezifikation:** 230 V, mech. Endschalter, Thermoschutz, SK I, IP44 oder besser, Hinderniserkennungs-Kompatibilität mit Shelly prüfen (Stromsignatur), nur 1 Motor.
11. **Potentialausgleich:** Rahmen + Pfosten mit PE verbinden (Cu ≥ 4 mm², [N-verif.] DIN VDE 0100-540) (E-M9).
12. **SPD Typ 2** in speisender UV prüfen/nachrüsten; Typ 3 im Kasten optional (E-M7).
13. **Erstprüfung** nach DIN VDE 0100-600 mit Protokoll; bei Isolationsmessung Shelly und Netzteil abklemmen.
14. **Antrieb B2 (24 V):** Elektrisch aufwendiger (Netzteil-Leistung, Koppelrelais -K2/-K3, DC-Schaltvermögen, Hinderniserkennung entfällt). Aus Elektrosicht **B1 bevorzugt**.
15. **Lux-Sensor:** siehe Kap. 3.

---

## 3 Lux-Sensor-Optionen

| Kriterium | L1: 0–10-V-Messumformer an Add-on | L2: Shelly BLU (Motion oder Door/Window, mit Lichtsensor) |
|---|---|---|
| Versorgung | 24 V DC, Netzteil -T1 nötig | Batterie |
| Temperatur | Messumformer-abhängig, Industriegeräte typ. −30…+60 °C [A] | **−20…+40 °C** [H] Q8 |
| Messbereich | wählbar (z. B. 0–1000 lx) [A] | **nicht dokumentiert** [H] Q8 |
| Aktualisierung | kontinuierlich, Schwellwert 0,1 V [H] Q3 | BLU Motion: Beacon alle 30 s; BLU Door/Window: nur bei Ereignis [H] Q8 → für Dämmerung **ungeeignet** |
| Installation | Leitung, Klemmen, Potentialfrage E-K2 | kabellos, Plus 2PM als BLU-Gateway [A, verifizieren] |
| Bewertung | robust, deterministisch, mehr Aufwand | einfach, aber Kälte/Batterie/Funk; nur BLU Motion sinnvoll |

Empfehlung: **L1** für Betriebssicherheit. Alternativ ohne Lux nur **Astro + Offset** (keine Hardware) – Lux dann nur als Plausibilisierung.

---

## 4 Single-Line-/Verdrahtungsvorgabe (Vorlage Zeichnung)

Kennzeichnung nach DIN EN IEC 81346-1/-2. Anlage `=DD` (DuckDoor), Ort `+K1` (Schaltkasten), `+M` (Antriebskasten), `+R` (Rahmen außen).

### 4.1 Betriebsmittelliste

| BMK | Ort | Betriebsmittel | Kennwerte |
|---|---|---|---|
| -F0 | Bestand UV | RCD Typ A | 30 mA (nachweisen) |
| -F1 | Bestand UV | LS EN 60898-1 | B16 (oder B10), ≥ 6 kA |
| -W1 | Erdreich | Zuleitung | NYY-J 3×1,5 [A] |
| -X1 | +K1 | Einspeiseklemmen | L, N, PE |
| -Q1 | +K1 | Lasttrenn-/Reparaturschalter 2-pol., abschließbar | ≥ 16 A |
| -F2 | +K1 | LS 1P+N | B6 |
| -K1 | +K1 | Shelly Plus 2PM (Cover-Modus) | 10 A/Kanal, 16 A ges. |
| -K1.1 | +K1 | Shelly Plus Add-on (auf -K1 gesteckt) | AI 0–10 V, DI |
| -T1 | +K1 | Netzteil 24 V DC, SELV, Hutschiene | ≥ 0,5 A [A] |
| -F3 | +K1 | Feinsicherung / Elektronik-Sicherung 24 V | 0,5 A T [A] |
| -E1 | +K1 | PTC-Heizer | 10–20 W [A] |
| -B3 | +K1 | Thermostat/Hygrostat für -E1 | Öffner bei Temp., Schließer bei r. F. |
| -X2 | +K1 | Klemmen Motor | L↑, L↓, N, PE |
| -X3 | +K1 | Klemmen Kleinspannung (räumlich getrennt, Trennsteg) | 24 V, 0 V, AI, DI |
| -X4 | +K1 | Klemmen Taster 230 V | L, SW1, SW2 |
| -W2 | +K1→+M | Motorleitung | H07RN-F 4G1,0 |
| -M1 | +M | Rohrmotor 230 V, mech. Endlagen | SK I [A] |
| -S1 / -S2 | +K1 (Deckel/Wand) | Taster AUF / ZU, 250 V AC, IP67 | Schließer |
| -W3 | +K1→+R | Leitung Reed | H05RN-F / UV-best. 2×0,5 [A] |
| -B2 | +R | Reedkontakt „ZU“, Kunststoff, IP67 | Schließer bei Klappe zu |
| -W4 | +K1→Sensor | Leitung Lux | UV-best. 3×0,5 [A] |
| -B1 | +R (Mast, frei zum Himmel, nicht beschattet) | Lux-Messumformer 0–10 V | Versorgung 24 V DC |
| -X5 | +K1 | PE-Schiene / Potentialausgleich | Rahmen, Pfosten |

### 4.2 Single-Line (textuell)

```
Bestand UV: L1/N/PE ── -F0 (RCD 30 mA, Typ A) ── -F1 (LS B16, 6 kA)
   │
   └─ -W1 NYY-J 3×1,5 (Erdreich, ≥0,6 m, Schutzrohr am Austritt)
        │
=DD+K1  -X1 (L,N,PE) ── -Q1 (2-pol. Rep.-Schalter) ── -F2 (LS B6 1P+N)
                                                     │
          ┌──────────────────────┬───────────────────┼─────────────────────┐
          │                      │                   │                     │
       -K1 Shelly Plus 2PM    -T1 24 V SELV      -B3 Thermostat ── -E1 Heizer
       L, N                   L, N → +24/0 V
       O1 ─ -X2:1 ─┐            │
       O2 ─ -X2:2 ─┤ -W2        -F3 ── -X3:1 (+24 V) ── -W4 ── -B1 Lux (+V)
       N  ─ -X2:3 ─┤ H07RN-F    0 V ── -X3:2 ──────────────────── -B1 (0 V)
       PE ─ -X2:4 ─┘ 4G1,0                                  -B1 (Out 0–10 V)
                    └── -M1 Rohrmotor                             │
       SW1 ─ -X4:2 ─ -S1 ─ -X4:1 (L nach -F2)                     │
       SW2 ─ -X4:3 ─ -S2 ─┘                                       │
       -K1.1 Add-on: ANALOG IN ─ -X3:3 ───────────────────────────┘
                     GND ─ -X3:2 (gemeinsam mit 0 V -T1)
                     DIGITAL IN ─ -X3:4 ── -W3 ── -B2 Reed ── -X3:5 ── GND
                     VREF+R1 OUT ─ Brücke auf DIGITAL IN (Pull-up 10 kΩ) [A]
PE: -X1:PE ── -X5 ── -X2:4 (Motor), Rahmen/Pfosten (Potentialausgleich)
```

Hinweise zur Zeichnung:
- Netz- und Kleinspannungsklemmen räumlich getrennt (Trennplatte), Kleinspannungsleitungen nicht im selben Kanal wie 230 V ohne Trennung [N-verif.] DIN VDE 0100-410 Abschn. 414.
- Reed-Pull-up: ob DIGITAL IN intern hochgezogen ist, ist nicht belegt; Beschaltung mit VREF+R1 OUT nach Anschlussbild Shelly (Q3) verifizieren.
- Cover-Richtung O1/O2 in App tauschbar; Motoradern lt. Motorhersteller (typ. braun/schwarz = Richtungen, blau = N, gn/ge = PE [A]).
- Klemmenbezeichnungen 2PM (L, N, O1, O2, SW1, SW2) am Geräteaufdruck prüfen.

---

## 5 Klemmenplan-Vorschlag

Reihenklemmen Hutschiene; Querschnitt Netz 1,5–2,5 mm², Kleinspannung 0,5–1,5 mm² [A].

| Klemme | Bezeichnung | Ziel intern | Ziel extern | Leitung | Potential |
|---|---|---|---|---|---|
| -X1:1 | L | -Q1:1 | -W1 br | NYY-J 3×1,5 | 230 V |
| -X1:2 | N | -Q1:3 | -W1 bl | | 230 V |
| -X1:PE | PE | -X5 | -W1 gn/ge | | PE |
| -X2:1 | L↑ (AUF) | -K1:O1 | -M1 (z. B. sw) | H07RN-F 4G1,0 | 230 V |
| -X2:2 | L↓ (ZU) | -K1:O2 | -M1 (z. B. br) | | 230 V |
| -X2:3 | N | -F2:N | -M1 bl | | 230 V |
| -X2:4 | PE | -X5 | -M1 gn/ge | | PE |
| -X4:1 | L Taster | -F2:L | -S1/-S2 gemeinsam | H05RN-F 3×1,0 / Einzeladern | 230 V |
| -X4:2 | SW1 (AUF) | -K1:SW1 | -S1 | | 230 V |
| -X4:3 | SW2 (ZU) | -K1:SW2 | -S2 | | 230 V |
| -X4:4 | L Heizer | -F2:L → -B3 | -E1 | intern | 230 V |
| -X3:1 | +24 V | -F3 | -B1 +V | UV-best. 3×0,5 | SELV |
| -X3:2 | 0 V / GND | -T1 0 V, -K1.1 GND | -B1 0 V | | SELV [E-K2] |
| -X3:3 | AI 0–10 V | -K1.1 ANALOG IN | -B1 Out | | SELV [E-K2] |
| -X3:4 | DI Reed | -K1.1 DIGITAL IN (+ VREF+R1 OUT) | -B2 | UV-best. 2×0,5 | SELV [E-K2] |
| -X3:5 | DI GND | -K1.1 GND | -B2 | | SELV [E-K2] |
| -X5 | PE-Schiene | -X1:PE, -X2:4, -T1 PE (falls SK I) | Rahmen, Pfosten (Cu ≥ 4 mm²) | H07V-K gn/ge | PE |

Kabelverschraubungen: M16/M20 IP68, Einführung nur von unten; Druckausgleichselement unten.

---

## 6 Offene Punkte an Bauherr/Errichter

1. Tiefste Standorttemperatur (Klimazone) → Heizerauslegung.
2. Bestand UV: RCD-Typ, LS-Charakteristik, Schaltvermögen, SPD vorhanden?
3. Länge und Art der vorhandenen Zuleitung, Verlegeart.
4. Anwendbarkeit DIN VDE 0100-705 (Entscheidung Errichter).
5. Anfrage Shelly: Isolationsspannung Plus Add-on; Kompatibilität Gen4 + Add-on im Cover-Modus.
6. Gerätegeneration festlegen (Plus 2PM Gen2 bzw. 2PM Gen3 – beide in Add-on-Liste [H] Q1, Q4).

---

## 7 Quellen

- Q1 Shelly Plus Add On – Dokumentation (unterstützte Geräte, Beschreibung „galvanisch getrennt“): https://www.shelly.com/de/blogs/documentation/shelly-plus-add-on, https://shelly.com/products/shelly-plus-add-on
- Q2 Shelly Plus 2PM – Dokumentation/Produktseite (10 A/Kanal, 16 A ges., 18 A Spitze, 240 V AC, −20…+40 °C, 30–70 % r. F., Cover-Modus, Hinderniserkennung, Schutzfunktionen): https://www.shelly.com/blogs/documentation/shelly-plus-2pm, https://www.shelly.com/products/shelly-plus-2pm
- Q3 Shelly Plus Add-on – technische Daten (0–10 V, ±5 %, DI-Pegel, VCC 10 mA, VREF 1 mA, VREF+R1 10 kΩ, −20…+40 °C, 30–70 % r. F.): https://www.shelly.com/de/products/shelly-plus-add-on, https://us.shelly.com/blogs/documentation/shelly-plus-add-on
- Q4 Shelly 2PM Gen3 / Gen4 – Dokumentation (Add-on-Schnittstelle, Warnung „High voltage on the add-on interface when the Device is powered!“): https://shelly.com/products/shelly-2pm-gen3, https://www.shelly.com/blogs/documentation/shelly-2pm-gen4
- Q5 Shelly Plus Add-on User and Safety Guide (spannungsfreie Montage, „Do not install the Device where it can get wet“): https://manuals.plus/m/7725643676a0e8ab718b60625562b363b25a58697be851ce545a9e23617d2295
- Q6 Shelly 2PM User and Safety Guide (LS EN 60898-1, B/C, max. 16 A, ≥ 6 kA, Energiebegrenzungsklasse 3): https://manuals.plus/shelly/2pm-wifi-and-bluetooth-2-channels-smart-relay-switch-manual.pdf
- Q7 Shelly Plus 2PM Cover-Modus: https://www.shelly.com/de/blogs/documentation/shelly-plus-2-pm-device-smart-control-cover-mode
- Q8 Shelly BLU Motion / BLU Door Window (−20…+40 °C, Lichtsensor, Sendeverhalten): https://www.shelly.com/de/blogs/documentation/blu-motion, https://www.shelly.com/de/blogs/documentation/blu-door-window
- Q9 Normen (Abschnitte nicht am Normtext geprüft, [N-verif.]): DIN VDE 0100-410, -430, -443, -520, -534, -540, -600, -705; DIN VDE 0298-3; DIN EN IEC 81346-1/-2; DIN EN 60898-1.
