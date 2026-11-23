# Review 01 – Mechanik / Metallbau

Prüfgegenstand: `docs/00_Konzept_v0.md` (Konzept v0). Rolle: Konstruktion Maschinenbau/Metallbau.
Kennzeichnung: **[A]** = Annahme (nicht belegt), **[Qn]** = Quelle n (siehe Abschnitt 4), **[R]** = eigene Rechnung.

---

## 1 Befunde

### 1.1 Kritisch

**K1 – B1: Die Bremse des Rohrmotors verhindert ein Anheben des Schiebers nicht.**
Ein Gurt überträgt nur Zug. Hebt ein Tier den Schieber von unten an, wird der Gurt schlaff. Die Bremse hält dann die Welle, aber keine Last. Gegen das Anheben wirken nur das Eigengewicht des Schiebers (≈ 21 N [R]) und die Reibung in der Führung.
- Bei Rollläden gilt dasselbe: Hersteller verlangen für eine Hochschiebesicherung *starre* Wellenverbinder statt Aufhängefedern [Q1][Q2].
- Waschbären heben Schieber gezielt an. Eine Patentschrift zu Hühnerklappen nennt genau diese Schwäche von Fallschiebern [Q3].
- Eine Mindestverriegelung beim Schließen gilt in der Praxis als nötig [Q4]. Gewöhnliche Riegel reichen gegen Waschbären nicht [Q5].
→ Die Aussage „Motorbremse hält Gurt → Schieber nicht anhebbar“ ist **falsch**. B1 bietet ohne zusätzliche mechanische Verriegelung keinen Aufhebelschutz.

**K2 – B1: Ein festgefrorener oder klemmender Schieber kann frei herabfallen, und der Gurt kann sich falsch aufwickeln.**
Klemmt der Schieber oben oder auf halber Höhe, wickelt der Motor beim Befehl „Ab“ bis zur unteren Endlage ab. Der Gurt liegt dann mit bis zu ≈ 600 mm lose da.
- Löst sich der Schieber später, fällt er frei aus bis zu ≈ 0,53 m Höhe. Das ergibt E = m·g·h ≈ 2,1 kg · 9,81 m/s² · 0,53 m ≈ 11 J auf eine Ente im Durchgang [R].
- Loser Gurt kann beim nächsten Hochfahren schief oder doppelt wickeln. Folge: falsche Endlagen.
- Der Reedkontakt „ZU“ meldet nur, dass die Endlage nicht erreicht wurde. Er verhindert den Fall nicht.

**K3 – Die Maßkette passt nicht: Mit Hub 520 mm bleibt der Schieber 10 mm in der Öffnung.**
- Schieber 560 mm hoch, oben 30 mm Überdeckung → unten ebenfalls 30 mm Überdeckung.
- Unterkante „zu“ liegt also 30 mm unter der Lichtöffnung. Der nötige Hub ist 500 + 30 = 530 mm, ohne Freiraum. Mit 520 mm ragen 10 mm in die Öffnung [R].
- Die Rahmenhöhe „≈ 1250 mm“ vernachlässigt die Schieberhöhe über der Lichtöffnung im geöffneten Zustand. Die schlüssige Maßkette ergibt ≈ 1320 mm (Abschnitt 3).

### 1.2 Mittel

**M1 – Schieber aus PE-HD 10 mm: große Wärmedehnung, Verzug, Nagegefahr.**
- Ausdehnungskoeffizient α = 150…230·10⁻⁶ 1/K [Q6].
- Mit ΔT = 80 K [A: −25 °C … +55 °C bei schwarzer Platte in der Sonne]: Höhe 560 mm → +6,7…10,3 mm, Breite 400 mm → +4,8…7,4 mm [R].
- Folgen: Bei einseitiger Sonne wölbt sich die Platte; die Endlage „ZU“ und die Lage des Reedkontakts wandern; die Kanten bieten Angriff für Nagen und Hebeln.
- Die Masse im Konzept ist richtig gerechnet: 0,40 · 0,56 · 0,010 m³ · 950 kg/m³ = 2,13 kg (Dichte 0,95 g/cm³ [Q6]).

**M2 – Führung U 20×15 mm ist zu flach.**
- 25 mm seitliche Überdeckung plus Dehnspiel brauchen ≥ 30 mm Nuttiefe.
- Ein U-Profil 20×15 mm hat ≤ 18 mm Innentiefe.
- Nutbreite und Spiel sind nicht festgelegt. Zu viel Spiel bietet einen Hebelansatz und lässt Eis einwachsen; zu wenig Spiel lässt den Schieber klemmen.

**M3 – Pfostenabstand und Antriebskastenbreite hängen an der Motorlänge.**
- Rohrmotoren Ø35 sind ≈ 470–490 mm lang (Beispiele: 472 mm und 485 mm, beide 10 Nm [Q7]).
- Mit Wellenlager ergibt sich eine Kasten-Innenbreite ≥ 540 mm. Das ist deutlich mehr als die Lichtweite von 350 mm.
- Im Konzept fehlt diese Abhängigkeit.

**M4 – Konstruktion doppelt (Alu-Rahmen 40×40 und Stahlpfosten 60×60) und Gründung mit Einschlaghülse.**
- Der doppelte Aufbau bringt zusätzliche Toleranzen und Kontaktstellen für Korrosion.
- Einschlaghülsen sind nicht frostsicher und lassen sich schlecht ausrichten. Die Führungen brauchen aber Parallelität (Anforderung siehe Abschnitt 3).
- Als frostfreie Gründungstiefe gilt in DE üblicherweise ≥ 0,8 m, regional mehr [Q8]. Dieser Wert stammt nur aus einem Ratgeber; im Einzelfall die örtliche Frosttiefe klären.

**M5 – Zaunanschluss mit Spannschellen leitet die Spannkräfte des Zauns in die Türpfosten.**
- Die Türeinheit ist nicht als Abspann- oder Endpfosten ausgelegt. Folgen: die Pfosten verdrehen sich, die Führungen laufen aus der Flucht, der Schieber klemmt.
- Der Spalt zwischen Zaun und Rahmen ist nicht festgelegt. Ausgewachsene Marder passen durch ≈ 5 cm, Jungtiere möglicherweise durch ≈ 3 cm [Q9].

**M6 – Untergrabschutz ist unterbestimmt.**
- In den Quellen reichen die Empfehlungen von 50 cm Eingrabtiefe plus 40 cm Platten bis zu 1 m Schürzenbreite [Q10][Q11]. Eine Norm dafür gibt es nicht.
- Direkt unter dem Schieber ist der Bereich am kritischsten, weil der Fuchs dort die Schnauze unter die Unterkante bringen kann.

**M7 – B2: Bauhöhe und Spindelart.**
- Eingefahrene Länge = Hub + Grundlänge. Beispiele: PA-14 mit ≈ 123 mm Grundlänge [Q12]; Industrieantrieb mit Hub 550 und L ≈ 802 mm [Q13].
- Bei Einbau über dem Schieber wächst die Rahmenhöhe auf ≈ 1,9–2,0 m [R].
- Selbsthemmend sind nur Trapez- bzw. Gleitgewindespindeln. Kugelgewindetriebe brauchen eine Bremse [Q13]. Das muss im Datenblatt ausdrücklich gefordert werden.

### 1.3 Gering

- **G1 – Korrosion:**
  - Aluminium an feuerverzinktem Stahl gilt als gering gefährdet [Q14].
  - Edelstahlschrauben an verzinktem Stahl sind meist unbedenklich. In nasser Umgebung mit Kunststoffscheiben trennen [Q14][Q15].
  - Aluminium nicht direkt in frischen Beton oder Mörtel setzen, sondern eine Trennlage vorsehen. Dafür gibt es nur Forenquellen [Q16]; als Vorsichtsmaßnahme behandeln.
  - Kot, Ammoniak und Feuchte im Bodenbereich [A]: Pfostenfuß zusätzlich beschichten (Duplex).
- **G2 – Gurt:** Ein Mini-Gurt 14 mm × 1,2 mm hält bis ≈ 210 daN [Q17]. Das liegt weit über der Last (siehe 1.4). UV-Alterung bei freier Gurtstrecke [A]: Gurt in der Führung oder im Kasten verdeckt führen.
- **G3 – Reedkontakt:** Montage auf Aluminium oder PE ist unkritisch. Nicht direkt auf den Stahlpfosten setzen (Magnetfeld wird abgelenkt) [A].
- **G4 – Kletterhilfe:** Der Rahmen ist ≈ 1,3 m hoch. Ist der Zaun niedriger, dient die Einheit als Aufstieg [A: Zaunhöhe unbekannt]. Kastendeckel schräg ausführen.
- **G5 – Schwelle:** Ein Bodenanschlag ohne Rinne ist richtig. Der Schwellenwinkel muss die Schieberunterkante aber auf der Raubtierseite abdecken (Abschnitt 3).

### 1.4 Nachrechnung B1 (Rohrmotor + Gurt) [R]

| Größe | Wert | Basis |
|---|---|---|
| Masse Schieber PE-HD 400×560×10 | 2,13 kg → G = 20,9 N | ρ 0,95 g/cm³ [Q6] |
| Masse Schieber Al 400×560×4 (Empfehlung) | 2,42 kg → G = 23,7 N | ρ 2,7 g/cm³ [A] |
| Wickelradius Anfang r₀ | 20 mm | Achtkantwelle SW40 [Q7], Gurtscheibe [A] |
| Gurtlänge L, Dicke t | 610 mm (Hub 550 + 60), 1,2 mm | [Q17] |
| Wickelradius Ende r = √(r₀² + L·t/π) | √(400 + 233) = 25,2 mm | Wickelformel |
| Umdrehungen bei mittlerem Radius ≈ 22,6 mm | ≈ 4,3 U | – |
| Nötiges Moment, normal: (G + Reibung 10 N [A]) · r | (24 + 10) N · 0,025 m ≈ 0,9 Nm | – |
| Nötiges Moment beim Losbrechen von Eis: 130 N [A] · r | ≈ 3,3 Nm | – |
| Verfügbares Moment, Ø35-Motoren am Markt | 5–10 Nm [Q7][Q18] | – |
| Max. Gurtzug bei 10 Nm und r₀ = 20 mm | 500 N | – |
| Sicherheit gegen Gurtbruch (2100 N) | ≈ 4,2 | [Q17] |
| Laufzeit bei 16–21 U/min | ≈ 12–16 s | [Q7][Q18] |

Ergebnis:
- Das Drehmoment reicht auch für einen 5-Nm-Motor deutlich (Faktor ≥ 1,5 auch bei Eis [A]).
- Die mechanische Endlage muss sich auf ≈ 4–5 Umdrehungen einstellen lassen. Das Datenblatt des gewählten Motors muss diesen kleinen Einstellbereich zulassen.
- Ein Motor über 6 Nm bringt keinen Nutzen. Er erhöht nur die Kraft, die bei einem Fehler auf Gurt und Befestigung wirkt.

---

## 2 Empfehlungen

**E1 – Antrieb aus mechanischer Sicht: B1 nur in geänderter Form („B1+“). B2 ist die Ausweichlösung.**

B1+ besteht aus Rohrmotor, Gurt und einer **Zugentriegelung mit Schwerkraftriegel**:
- Der Gurt greift nicht am Schieber an, sondern an einem Kipphebel auf der Schieberoberkante (Entenseite).
- Ist der Gurt schlaff, schieben Eigengewicht des Hebels und eine Edelstahl-Druckfeder zwei Riegelbolzen (Ø 8 mm, A4) seitlich durch Bohrungen in den Führungsschienen.
- Gurtzug dreht zuerst den Hebel und zieht die Bolzen zurück. Erst danach hebt sich der Schieber. Es ist kein zusätzlicher Aktor und keine Elektrik nötig.
- Die Riegelbolzen sitzen in der Führung und sind von außen nicht erreichbar. Damit gilt auch die Waschbär-Anforderung [Q5].
- Den Reedkontakt so setzen, dass er den Riegel in Endlage meldet und nicht nur die Schieberposition.

Zusätzlich für B1+:
- **Schlaffgurtschalter** (Öffner, im Kasten): unterbricht die Richtung „Ab“, sobald der Gurt schlaff wird. Das beseitigt K2. Die elektrische Einbindung (L↓-Ader am 2PM) mit dem Review Elektrik abstimmen.

Begründung gegen B2 als erste Wahl:
- Schließkraft 100–1000 N gegen eine Ente.
- Zusätzlich nötig: Schließkantensicherung, Polwende-Relais und 24-V-Netzteil.
- Bauhöhe ≈ 1,9 m oder seitlicher Antrieb im Schmutzbereich.

Vorteile von B2:
- Selbsthemmung bei Trapezspindel.
- Kann Eis brechen.

Wählt das Gesamt-Review B2, dann:
- Trapezspindel, IP66, mit Bremse bzw. Selbsthemmung laut Datenblatt.
- Kraftbegrenzung ≤ 150 N [A] und Kontaktleiste an der Schieberunterkante.
- Einbau seitlich neben einer Führung, Fußpunkt ≥ 100 mm über Gelände.

**E2 – Schieberwerkstoff:** Aluminium EN AW-5754 (AlMg3), 4 mm, Kanten entgratet.
- Gegenüber PE-HD: ≈ 10× geringere Wärmedehnung (α ≈ 23·10⁻⁶ 1/K [A, Tabellenwert]), nicht nagbar, formstabil.
- Masse 2,4 kg verbessert den Schwerkraftschluss.
- Unterkante mit Flachstahl-Ballast 20×5 Edelstahl möglich, falls die Reibung höher ist als angenommen.

**E3 – Führung:**
- Führungsnut aus zwei PE-UHMW-Leisten auf einem Alu-Winkel als Träger.
- Geringe Reibung, Eis haftet schlecht [A].
- Unten offen, oben unter dem Kasten abgedeckt.

**E4 – Tragwerk vereinfachen:** Die Pfosten tragen direkt Führungen und Kasten. Kein separater Alu-Rahmen.
- Fußplatten auf einem frostfreien Streifenfundament statt Einschlaghülsen.
- Das Fundament dient zugleich als Untergrabschutz unter der Schwelle.

**E5 – Zaunanschluss:**
- Der Zaun erhält eigene Abspannpfosten im Abstand ≤ 100 mm zur Türeinheit.
- Die Verbindung zur Tür ist nur eine Spaltabdeckung, keine Krafteinleitung. Ausführung: verzinktes Schweißgitter oder Lochblech, verschraubt.
- Restspalt überall ≤ 25 mm [abgeleitet aus Q9].

**E6 – Untergrabschutz:**
- Unter der Tür: Streifenfundament 800 mm tief.
- Seitlich anschließend: Schürze aus Schweißgitter, Masche ≤ 25 mm [A, abgeleitet aus Q9], 1000 mm breit nach außen, 50–100 mm unter Gelände [Q11]. Die Schürze an den Fundamentrand anschließen.

**E7 – Frost/Eis:**
- Schieberunterkante setzt auf einem Gummipuffer im Schwellenwinkel auf, nicht auf Beton. Fundamentoberkante +20 mm über Gelände mit 2 % Gefälle nach außen [A].
- Kein Ablagerungsraum unter dem Schieber.
- Optional selbstregelndes Heizband in der Schwelle (Abstimmung mit Elektrik).

**E8 – Wartung:**
- Kastendeckel von oben abnehmbar, 4 Schrauben A4.
- Schieber nach oben ausbaubar (Führungen oben offen, sobald der Deckel ab ist).
- Gurt einzeln tauschbar.
- Intervalle [A]: Führung reinigen ½-jährlich und vor dem Winter, Gurt jährlich prüfen und nach 3–5 Jahren tauschen, Riegelfunktion monatlich prüfen (Schieber von Hand anheben).

---

## 3 Maßvorgaben für die Zeichnung (B1+)

Bezug z = 0: Oberkante Fundament (OKF), +20 mm über Gelände [A]. x = 0: Mitte der Öffnung. Maße in mm. Toleranz der Führungen: parallel ±1 mm über die Länge [A].

| Pos. | Bauteil | Maß / Ausführung |
|---|---|---|
| 1 | Lichtöffnung | B 350 × H 500, von z = +30 bis +530 |
| 2 | Schwellenwinkel | Al EN AW-6060, L 50×30×4, liegend; senkrechter Schenkel 30 hoch auf der Raubtierseite, deckt die Schieberunterkante ab; Länge 430; Oberkante +30 (Stufe für Enten 30 ≤ 50 ✓) |
| 3 | Schieber | Al EN AW-5754, 4 mm, B 400 × H 560 (seitlich je 25 Überdeckung, oben 35); zu: UK +5 (Puffer), OK +565; offen: UK +555, OK +1115 |
| 4 | Hub | 550 (Freiraum über der Lichtöffnung 25) |
| 5 | Führungsnut | Breite 6 (Schieber 4 + 2 × 1 Spiel), Tiefe 30 (25 Überdeckung + 5 Spiel); Nutgrund bei x = ±205; PE-UHMW-Leisten 30×10 auf Alu-Winkel 40×40×4; Länge 0 … +1140; unten offen |
| 6 | Riegel | 2 × Bolzen Ø 8 A4, Hub 12; Bohrung Ø 10 in Führung/Pfosten bei z = +540 (Schieber zu) |
| 7 | Pfosten | 2 × Stahlrohr □ 60×60×3, feuerverzinkt (EN ISO 1461), Fußzone Duplex; Länge 1300; lichter Abstand 430, Achsabstand 490 |
| 8 | Fußplatten | 160×160×10, je 4 × Verbundanker M12 A4, Lochbild 110×110; Trennlage Fußplatte/Beton |
| 9 | Sturzblende | Al 5754, 3 mm, zwischen den Pfosten, z = +530 … +1140, auf der Entenseite der Schieberebene (schließt den Bereich oberhalb der Lichtöffnung) |
| 10 | Antriebskasten | Al 5754, 2 mm; außen B 600 × H 160 × T 180; Unterkante +1140, Oberkante +1300, Deckel mit Gefälle ≥ 10° (max. +1320); innen ≥ 560 breit für Rohrmotor ≈ 485 + Lager |
| 11 | Wickelwelle | Achtkant SW40 mit Gurtscheibe Ø 40; Achse bei z ≈ +1220, mittig über dem Schieber |
| 12 | Gurt | 14 × 1,2 Polyester, Länge ≈ 610 + 150 Befestigung; Austritt durch Bürstendichtung |
| 13 | Gesamthöhe | ≈ 1320 über OKF |
| 14 | Gesamtbreite | 600 (Kasten); Pfosten außen 550 |
| 15 | Streifenfundament | Beton C25/30 [A], L 800 × B 300 × T 800 (frostfrei [Q8], örtlich prüfen); Oberkante +20 über Gelände |
| 16 | Untergrabschutz seitlich | Schweißgitter verzinkt, Masche ≤ 25 × 25, Draht ≥ 2,0 [A]; 1000 breit nach außen, 50–100 unter Gelände, beidseits ≥ 1000 entlang des Zauns |
| 17 | Zaunanschluss | eigene Abspannpfosten ≤ 100 neben der Einheit; Spaltabdeckung aus Gitter/Lochblech; Restspalt ≤ 25 |
| 18 | Reedkontakt | am Riegelhebel bzw. an der Führung bei z ≈ +540, nicht auf Stahl |

Für B2 (zum Vergleich): Antrieb seitlich neben Pfosten 7, eingefahrene Länge ≈ 680–800 bei Hub 550 [Q12][Q13]. Gesamtbreite ≈ 700. Bei Einbau über dem Schieber Gesamthöhe ≈ 1900–2000.

---

## 4 Quellen

- [Q1] Rademacher, Montageanleitung starre Wellenverbinder / Rohrmotor: „Feste Wellenverbinder oder Hochschiebesicherungen … Es dürfen keine Aufhängefedern verwendet werden“ – https://service.rademacher.de/hc/article_attachments/17289885701778 ; Rohrmotor AE2: https://rollladen-schroeder.de/Ordner/WTS/bedienungsanleitung%20wts/Antriebstechnik/Rohrmotoren%20Elektronisch%20Rollladen%20Plug%2BPlay%20Serie%20AE2.pdf
- [Q2] Becker, Starre Sicherheitsfeder („wirkt als Hochschiebesicherung“) – https://produktcenter.becker-antriebe.com/out/media/BAPIM001/Pixelboxx/starre%20sicherheitsfeder%204902%20300%20007%200%20de.pdf
- [Q3] US-Patent 8,020,519 „Chicken coop door module“ (Waschbären heben Fallschieber an) – https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8020519
- [Q4] FARM Infrastructure, raccoon-proof coop doors (selbstverriegelnde Türen, tiefe Führungen) – https://www.farmstandapp.com/330158/6-best-raccoon-proof-coop-doors-for-automatic-openers/ ; ChickenGuard Self-Locking Kit – https://www.farmandfleet.com/products/1495161-my-favorite-chicken-chickenguard-pro-opener-and-self-locking-chicken-coop-door-kit.html
- [Q5] VEVOR DIY, raubtiersicherer Hühnerstall (Waschbären öffnen normale Riegel) – https://www.vevor.com/de/diy-ideas/predator-proof-chicken-coop/
- [Q6] Röchling, Polystone G natur / G HD schwarz, Techn. Datenblätter (ρ 0,95 g/cm³; α 150…230·10⁻⁶ 1/K nach DIN 53752) – https://www.roechling.com/fileadmin/assets/Polystone®%20G%20natur%20–%20Technisches%20Datenblatt%20(DE).pdf
- [Q7] Rademacher RTBS 10/16Z (10 Nm, 16 U/min, L 472 mm, mech. Endlagen) – https://www.elektro-wandelt.de/Rademacher-RTBS-10-16Z-Rohrmotor-RolloTube-Basis-Small-10Nm-16U-min.html ; CLIS 10/16PZ (Ø35, SW40, L 485 mm) – https://www.elektro-wandelt.de/Rademacher-CLIS-10-16PZ-Rohrmotor-C-line-elektr-10Nm-SW40.html
- [Q8] baustoffshop.de, Zaunpfosten einbetonieren (frostfrei ≥ 80 cm, regional 120–150 cm) – https://www.baustoffshop.de/infothek/zaunpfosten-einbetonieren/ (Ratgeber, nicht normativ)
- [Q9] gartenjournal.net, Marder Lochdurchmesser (≥ 5 cm adult, ≈ 3 cm Jungtiere) – https://www.gartenjournal.net/marder-lochdurchmesser
- [Q10] Luxemburg, Umweltverwaltung, Flyer Schutz Haus-/Nutztiere (Zaun 50 cm eingraben, 40 cm Platten) – https://environnement.public.lu/dam-assets/fr/conserv_nature/publications/2020/Flyer-Schutz-Haus-Nutztiere-web.pdf
- [Q11] DVL Herdenschutz, Kapitel Untergrabschutz (≥ 40 cm eingraben oder ≥ 1 m Schürze) – https://www.herdenschutz.dvl.org/fileadmin/user_upload_herdenschutz/Infosammlung/kapitel_Untergrabschutz.pdf
- [Q12] Progressive Automations, PA-14 (Hub 6″ → eingefahren 10,85″) – https://www.progressiveautomations.com/blogs/how-to/tips-to-extend-your-linear-actuators-lifespan
- [Q13] Thomson Electrak HD24B100-0550 (24 V, Hub 550, IP66 dyn., Kugelgewinde, L 801,9) – https://thomsonlinear.com/en/product/HD24B100-0550LLX1EMS ; DA24 (selbsthemmende Gleitgewindespindel als Option) – https://www.thomsonlinear.com/en/product/DA24-05B65M55M0N-DMM
- [Q14] baulinks.de, Kontaktkorrosion feuerverzinkter Stahl mit anderen Metallen (Al–Zn gering) – https://www.baulinks.de/webplugin/2006/1254.php4
- [Q15] Institut Feuerverzinken, Arbeitsblatt E.5 Kontaktkorrosion – https://www.feuerverzinken.com/wissen/arbeitsblaetter/e-weiterverarbeitung/e5-kontaktkorrosion.pdf (Inhalt nur über die Suchzusammenfassung geprüft, Host im Netz dieser Sitzung gesperrt)
- [Q16] bau.de-Forum, Aluminium und Beton (Trennlage) – https://bau.de/forum/balkon-terrasse/10281.php (Forum, schwache Quelle)
- [Q17] Diwaro Mini-Gurt 14 × 1,2 mm, Bruchfestigkeit 210 daN – https://www.hornbach.de/p/diwaro-mini-rollladengurt-gurtbreite-14-mm-gurtstaerke-1-2-mm-grau-50-m-rolle/12563893/
- [Q18] Cherubini Roll Ø35 (5 Nm/21 U/min, 9 Nm/16 U/min) – https://set-gmbh.de/21-rpm__230V_1

Nicht belegt, bewusst als [A] markiert: Zahlen zum Kraftaufwand von Fuchs und Waschbär, Losbrechkraft von Eis, Dichte und α von Aluminium (Tabellenwerte), Betongüte, Wartungsintervalle.
