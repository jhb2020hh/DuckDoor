# Review R2-11 – Mechanik und Sicherheit (Konzept v1)

Prüfgegenstand: `docs/01_Konzept_v1.md`, nur die Änderungen gegenüber v0 (Schrittmotor NEMA 17, Spindel Tr8×2, Langloch-Mitnehmer, Kinderzugang). Bezug: `review/01_Mechanik.md`, `review/04_Tierhaltung_Sicherheit.md`.
Kennzeichnung: **[Qn]** = Quelle n (Abschnitt 5), **[R]** = eigene Rechnung, **[A]** = Annahme, nicht belegt.

---

## 1 Befunde

### 1.1 Kritisch

**K1 – Der Langloch-Mitnehmer wird bei klemmendem Schieber zur starren Druckkupplung.**
- Der Freiweg im Langloch beträgt nur 60 − 8 (Bolzen) = 52 mm [R]. Klemmt der Schieber mehr als 52 mm über der Endlage (Eis, Schmutz, Tier), fährt die Mutter weiter. Dann liegt der Bolzen am anderen Langlochende an und drückt den Schieber mit Motorkraft nach unten.
- Die Firmware prüft B1 erst am Ende des Hubs. Bis dahin wird nicht erkannt, dass der Schieber der Mutter nicht folgt.
- Mögliche Druckkraft: F = 2π·η·T/P. Mit T = 0,59 Nm [Q7], P = 2 mm und η = 0,29…0,46 (µ = 0,2…0,1) ergeben sich ≈ 540…840 N [R]. Das ist ein Vielfaches der Richtwerte (150 N statisch, 400 N dynamisch [Q14]).
- Bei Eis im Langloch ist die Kupplung von Anfang an starr.
- Löst sich der klemmende Schieber, fällt er bis zu 52 mm frei: E = 23,7 N · 0,052 m ≈ 1,2 J [R]. Das ist gering, aber nur wenn die Mutter rechtzeitig stoppt.
→ Ohne Erkennung, dass der Bolzen vom Hubende abhebt, und ohne Strombegrenzung in Richtung AB gilt die Aussage „keine Motorkraft auf das Hindernis“ **nicht**.

**K2 – Der Aufhebelschutz verlässt sich auf eine Selbsthemmung, die nur knapp oder gar nicht vorliegt.**
- Steigungswinkel Tr8×2: α = arctan(P/(π·d₂)) = arctan(2/(π·7)) = 5,2° [R]; d₂ = d − 0,5·P [Q1].
- Reibwinkel: tan ρ′ ≈ 1,07·µ [Q1]. Damit ist die Spindel erst ab µ > 0,085 selbsthemmend [R]. Bei µ = 0,1 beträgt der Abstand nur 5,2° zu 6,1°.
- Der Hersteller Neff nennt für Trapezspindeln: keine Selbsthemmung über 4,5° [Q2]. Nach dieser Regel ist Tr8×2 **nicht** selbsthemmend.
- Selbsthemmung gilt nur statisch. Schon geringe Vibration kann die Mutter in Bewegung setzen. Für sicherheitsrelevante Lasten wird eine zusätzliche Bremse empfohlen [Q3][Q4][Q5].
- Ein Fuchs oder Waschbär, der am Schieber rüttelt, erzeugt genau diese Vibration [A].
- Schmierfett senkt µ, Kälte und Schmutz erhöhen µ. Damit streut µ im Jahreslauf um mehr als den Abstand 0,085…0,1 [A].
- Rechnung ohne Reibung (ungünstigster Fall): Eine Hebelkraft von 300 N [A] erzeugt am Motor T = F·P/2π = 0,095 Nm [R]. Mit Haltestrom hält ein NEMA 17 (0,4…0,59 Nm [Q7][Q8]) das sicher. Bei Stromausfall hält nur das Rastmoment. Dafür gibt es keinen Datenblattwert [A].

### 1.2 Mittel

**M1 – Die Langloch-Logik in v1 ist sprachlich vertauscht.**
Zum Heben muss der Bolzen am **oberen** Langlochende anliegen. Verriegelt ist der Schieber, wenn der Bolzen am **unteren** Ende anliegt: Dann drückt der Schieber beim Anheben über das untere Langlochende auf den Bolzen. In v1 steht es umgekehrt. Für die Zeichnung ist die Logik in Abschnitt 3 korrigiert.

**M2 – Festlager oben führt zu Knickgefahr der Spindel.**
- Hebelt ein Tier den verriegelten Schieber an, liegt die Mutter unten. Die Spindel ist dann von der Mutter bis zum oberen Festlager auf ≈ 600 mm Länge auf Druck belastet.
- Kerndurchmesser d₃ = 5,5 mm [A, DIN 103 nicht eingesehen]: I = π·d₃⁴/64 = 44,9 mm⁴. Euler-Knickkraft bei gelenkiger Lagerung, L = 600 mm, E = 200 GPa: F_k ≈ 246 N [R]. Bei frei hängendem unteren Ende ist F_k nur ≈ 62 N [R].
- Abhilfe: **Festlager unten** (an der Traverse über der Öffnung), Loslager oben, Motor oben. Dann wird beim Aufhebeln nur das kurze Stück unter der Mutter gedrückt.
- Beim normalen Heben im oberen Bereich wirken 34 N auf L ≤ 640 mm. F_k ≈ 216 N, Sicherheit ≈ 6 [R]. Das Losbrechen bei Eis findet in der unteren Stellung statt, die Knicklänge ist dort kurz.

**M3 – Die Motorwelle darf keine Axiallast tragen.**
NEMA-17-Wellen sind typisch nur für 25 N Druck und 65 N Zug ausgelegt [Q9]. Gefordert sind deshalb eine Klauenkupplung mit Elastomerstern (axial verschiebbar) und eine Spindellagerung, die die Axiallast vollständig aufnimmt.

**M4 – Werkstoffpaarung und Schmierung.**
- Messing auf Stahl hat ein hohes µ und neigt trocken zum Fressen. Die Beckhoff-Tabelle nennt für Stahl/Messing µ = 0,19 bzw. 0,35 [Q10]; welcher Wert trocken und welcher geschmiert gilt, ist im Auszug nicht eindeutig.
- POM reagiert empfindlich auf die Rauheit des Gegenkörpers [Q11].
- Fett nimmt im Freien Schmutz auf und wird bei Kälte zäh [A].
- Empfehlung: Edelstahlspindel gerollt mit Gleitkunststoffmutter für Trockenlauf (z. B. igus dryspin/iglidur [Q6]), **ohne Fett**. Für die Mutter liegt kein Reibwert-Datenblatt vor. Mit µ = 0,1…0,3 [A] rechnen.

**M5 – Referenzfahrt nach Stromausfall darf nachts nicht öffnen.**
v1 referenziert auf B3 (oben) und B4 (unten). Fährt die Steuerung nach dem Wiedereinschalten auf B3, öffnet sie die Klappe. Regel: Ist B1 aktiv, wird auf B4 referenziert (Verriegelungsrichtung). Fehlt B1 bei Nacht, geht die Steuerung in STÖRUNG mit Meldung und fährt nicht.

**M6 – Neue Einzugs- und Scherstellen durch Spindel und Mitnehmer (Kinder).**
- Mutter und Langloch bilden eine Scherstelle. Die Spindel ist eine drehende Welle.
- Beim Öffnen läuft der Schieber an der Unterkante des Spindelkanals (Sturz) vorbei. Diese Einzugstelle wird mit Motorkraft angetrieben.
- Mindestabstände gegen Quetschen: Finger 25 mm, Hand 100 mm, Arm 120 mm [Q12]. Kinderverhalten muss berücksichtigt werden, wenn Kinder zur gefährdeten Gruppe gehören [Q12].
- Abhilfe: Spindel und Mitnehmer vollständig einhausen (Sturzblende mit Sicherheitsschrauben). An der Einlaufkante eine weiche Abstreiflippe vorsehen. Den Strom in Richtung AUF auf den nötigen Wert begrenzen (siehe 1.4).

**M7 – Kind kann im Nachtgehege eingeschlossen werden.**
Die Öffnung 350 × 500 mm ist für Kleinkinder durchkriechbar (R1 T-K5). Die Lichtschranke verhindert nur das Schließen, solange das Kind in der Öffnung ist, nicht danach. Das Nachtgehege braucht deshalb eine Personentür, die sich von innen ohne Werkzeug öffnen lässt [A].

### 1.3 Gering

- **G1 – Verkanten des Schieberblechs:** Der Mitnehmer greift mittig an. Nach der Schubladenregel klemmt das Blech erst ab einem Außermittenmaß e ≥ L/(2µ). Mit L = 560 und µ = 0,2 [A] sind das 1400 mm [R]. Ein Verkanten ist damit nicht zu erwarten, solange der Bolzen innerhalb ±2 mm mittig sitzt.
- **G2 – Achsfehler Spindel zu Führung:** Ist die Spindel nicht parallel zur Führung, klemmt die Mutter. Abhilfe: Langloch 1 mm breiter als der Bolzen (Spiel in x), Bolzen in Achsrichtung (y) verschiebbar. Das Langloch dient zugleich als Verdrehsicherung der Mutter. Die Seitenkraft ist ≈ 0,2 Nm / 35 mm ≈ 6 N [R].
- **G3 – Spindelschutz:** Ein Faltenbalg über ≈ 600 mm Hub im Freien vereist und reißt [A]. Besser ist es, Spindel und Mitnehmer in den geschlossenen Kanal zwischen Schieberebene und Sturzblende zu legen. Dann wird kein Balg benötigt.
- **G4 – Motor oben im Kasten:** Die Lage ist richtig, weil dort kein Spritzwasser ankommt und die Welle nach unten zeigt. Stepper haben in der Regel keine IP-Schutzart [A]. Deshalb Kasten mit Druckausgleich und Bürstendichtung zum Spindelkanal.
- **G5 – StallGuard4 als Rückfallebene:** StallGuard4 funktioniert nur mit StealthChop und nur in einem bestimmten Drehzahlbereich [Q13][Q15]. Bei langsamer Fahrt ist es nicht verlässlich. Es darf deshalb keine Sicherheitsfunktion tragen.

### 1.4 Nachrechnung Antrieb [R]

| Größe | Wert | Basis |
|---|---|---|
| Last Heben normal | 23,7 N (Schieber) + 10 N (Führung) ≈ 34 N | R1 1.4 [A] |
| Last Losbrechen Eis | 130 N | R1 [A] |
| Antriebsmoment T = F·d₂/2·tan(α+ρ′) | normal 0,024…0,050 Nm; Eis 0,09…0,19 Nm (µ 0,1…0,3) | [Q1] |
| + Lager/Kupplung | ≈ 0,02 Nm | [A] |
| Bedarf max. | ≈ 0,21 Nm | – |
| Motor 17HS19-2004S1 (48 mm) | Haltemoment 0,59 Nm, 2 A | [Q7] |
| Motor 17HS4401 (40 mm) | Haltemoment 0,40…0,43 Nm | [Q8] |
| Drehzahl bei 20 mm/s | 10 U/s = 600 U/min | – |
| Moment bei 600 U/min, 24 V | nicht belegt, Kennlinie anfordern; erwartet ≈ 50 % des Haltemoments [A] | [Q7] |
| Sicherheit 48-mm-Motor | ≈ 0,3/0,21 ≈ 1,4 bei 600 U/min; ≈ 2,8 beim Losbrechen mit ≤ 60 U/min | [A] |
| Fahrweg Mutter | 550 Hub + 52 Langloch-Freiweg ≈ 602 mm | – |
| Fahrzeit | 20 mm/s → 30 s; 15 mm/s → 40 s; 10 mm/s → 60 s | – |
| Max. Schubkraft bei vollem Strom | 540…840 N (µ 0,2…0,1) | K1 |
| Moment für ≤ 150 N Schubkraft (µ 0,1) | 0,105 Nm → Strom AB ≤ ≈ 18 % des Nennstroms [A, Moment ≈ proportional zum Strom] | [Q14] |
| Treiber TMC2209 | bis 2 A RMS | [Q13] |

Ergebnis:
- Der 48-mm-NEMA-17 reicht aus. Der 40-mm-Typ ist bei 600 U/min und Eis zu knapp.
- Losbrechen langsam fahren (≤ 2 mm/s), danach 10…15 mm/s.
- Für die Richtung AB den Strom getrennt und niedrig einstellen.

---

## 2 Empfehlungen

1. **Mitnehmer-Schlaffschalter B8** (zu K1): Mikroschalter oder Reedkontakt am Mutterblock. Er meldet „Bolzen am oberen Langlochende“. Hebt der Bolzen beim SCHLIESSEN um mehr als 3 mm ab, stoppt die Fahrt sofort. Ausnahme: B1 ist aktiv, dann ist das Abheben der gewollte Verriegelungshub. Danach Wiederauffahren und Meldung. Die freie Fallhöhe sinkt damit auf ≤ 5 mm.
2. **Strombegrenzung getrennt nach Richtung:**
   - AB: so einstellen, dass am Schieber ≤ 150 N statisch wirken, Ziel ≤ 50 N [Q14]. Mit Kraftmesser an der Schieberunterkante nachweisen.
   - AUF: nur so viel Strom wie für das Losbrechen nötig, ≈ 40 % [A].
   - Den Maximalstrom zusätzlich hardwareseitig über R_sense/VREF deckeln [Q13].
3. **Hardware-Abschaltung:** Schaltleiste B7, Lichtschranke B6 und Schlaffschalter B8 schalten in Richtung AB per Logikgatter direkt den ENABLE-Eingang des Treibers ab, nicht nur über die Firmware. Ausführung mit dem Elektro-Review abstimmen.
4. **Passive Verriegelungsklinke** (zu K2, empfohlen): Eine Schwerkraftklinke aus Edelstahl rastet in ZU in eine Kerbe der Mitnehmerlasche ein. Beim Öffnen hebt eine Nocke am Mutterblock die Klinke innerhalb des Langloch-Freiwegs an, bevor sich der Schieber bewegt. Die Verriegelung hängt dann nicht mehr an der Selbsthemmung.
   **Mindestens** (falls keine Klinke): Im Zustand ZU_VERRIEGELT Haltestrom ≥ 50 % (IHOLD) [Q13]; Stromausfall melden (Akku-Puffer der Platine). Monatlich prüfen, ob sich der Schieber von Hand anheben lässt.
5. **Lagerung:** Festlager unten aus 2 × Rillenkugellager 626-2RS, geklemmt [A]. Loslager oben aus 1 × 626-2RS, axial frei. Darüber Klauenkupplung und Motor mit Welle nach unten.
6. **Werkstoffe:** Spindel Tr8×2 eingängig, Edelstahl, gerollt. Mutter aus Gleitkunststoff, trocken laufend, ohne Fett. Mitnehmerlasche und Bolzen aus A4.
7. **Einhausung:** Spindel und Mitnehmer liegen im Kanal hinter der Sturzblende. Unten schließt eine Traverse den Kanal ab, mit EPDM-Abstreiflippe zum Schieber und Ablaufbohrung. Sturzblende und Kastendeckel mit Sicherheitsschrauben befestigen (Kinder).
8. **Sensorik:** B1 mit einem Schaltfenster von ≤ 2 mm vor der Endlage. Ein Finger unter der Leiste darf B1 nicht auslösen. Referenzierung nach M5.
9. **Bewertung Lichtschranke + Schaltleiste:** Sie reichen als Schutz **nur zusammen mit** den Empfehlungen 1–3. Erst dann wirkt beim Schließen nur das Eigengewicht (≈ 24 N statisch, ≤ 5 mm Fall). Damit liegen die Werte unter den Richtwerten 150 N statisch / 400 N dynamisch [Q14].
   Ohne B8 und Strombegrenzung **reicht es nicht**: Ist das Langloch vereist oder klemmt der Schieber mehr als 52 mm über der Endlage, wirken bis zu 840 N.
   Lichtschranke zweistrahlig auf z = +100 und +300 [A], damit Kopf und Hals der Enten sowie ein kriechendes Kind erfasst werden. Das Restrisiko aus M6 und M7 bleibt.

---

## 3 Maßliste für die technische Zeichnung

Koordinaten: x = 0 Mitte Öffnung (entlang Zaun); y = 0 Mittelebene Schieber, +y = Entenseite (innen); z = 0 Oberkante Fundament (OKF, +20 über Gelände [A]). Maße in mm. Allgemeintoleranz ISO 2768-m [A]; Führungen parallel ±1 auf Länge; Spindelachse parallel zur Führung ±0,5.

**Blätter:**
- Blatt 1: Ansicht von der Entenseite, Sturzblende transparent, M 1:10.
- Blatt 2: Seitenansicht von rechts, M 1:10.
- Blatt 3: Schnitt A–A bei x = 0 durch Spindel und Mitnehmer, M 1:5.
- Blatt 4: Detail Z Mitnehmer, M 1:1.

| Pos. | Bauteil | Maß / Ausführung | Blatt |
|---|---|---|---|
| 1 | Lichtöffnung | B 350 (x ±175) × H 500 (z +30…+530) | 1 |
| 2 | Schwellenwinkel | Al L 50×30×4, Länge 430, Oberkante +30, senkrechter Schenkel auf Raubtierseite (−y), Gummipuffer z +0…+5 | 1, 3 |
| 3 | Schieberblech | Al EN AW-5754, t 4, B 400 (x ±200) × H 535; y −2…+2. ZU: UK Blech +30, OK +565. AUF: UK +580, OK +1115 | 1, 3 |
| 4 | Schaltleiste | Hohlkammerprofil H 25 an UK Blech, ZU z +5…+30; Länge 400 | 1, 3 |
| 5 | Hub Schieber | 550 | 1 |
| 6 | Führungsnut | PE-UHMW, Breite 6, Tiefe 30, Nutgrund x ±205; z 0…+1140, unten offen | 1 |
| 7 | Mitnehmerlasche | 1.4404, t 4, B 40 × H 110, mittig x = 0 ±0,5; y +2…+6; von OK Blech −15 bis OK +95; 2 × M5 A4 Senkkopf | 3, 4 |
| 8 | Langloch | Breite 9 H11, Länge 60, Mitte unten OK +28, Mitte oben OK +80 (Freiweg 52) | 4 |
| 9 | Rastkerbe für Klinke (Empf. 4) | 6 × 10 an Laschenkante, Unterkante OK +45 [A] | 4 |
| 10 | Mitnehmerbolzen | Ø 8 h9, A4, Achse in y, aus Mutterblock von y +35 bis y 0, axial ±3 frei | 3, 4 |
| 11 | Bolzenlage (Mitte) | verriegelt +594 (Bolzen 1 über unterem Langlochende); ZU entriegelt +645; AUF +1195; Fahrweg 601 | 3 |
| 12 | Mutter + Mutterblock | Tr8×2 Kunststoff, L ≈ 30 [A]; Block Al 30 × 30 × 40 | 3, 4 |
| 13 | Schlaffschalter B8 | am Mutterblock, schaltet bei ≥ 3 Abhub Bolzen vom oberen Langlochende | 4 |
| 14 | Spindel | Tr8×2 rechts, eingängig, Edelstahl gerollt; Achse x = 0, y = +35; Gewinde z +570…+1240; Zapfen unten Ø 6 k6 × 30, oben Ø 6 k6 × 35; Gesamtlänge ≈ 735 | 3 |
| 15 | Festlager unten | 2 × 626-2RS in Lagerbock Al, z +535…+565, axial geklemmt (Wellenmutter M6) | 3 |
| 16 | Loslager oben | 1 × 626-2RS, z +1245…+1255, axial frei | 3 |
| 17 | Kupplung | Klauenkupplung Elastomer Ø 20 × 30, Bohrung 5/6, z +1260…+1290 [A] | 3 |
| 18 | Motor | NEMA 17, 42 × 42 × 48, Welle Ø 5 nach unten; Flansch z +1295, Oberseite +1343; Motorplatte Al t 4 | 1, 3 |
| 19 | Traverse (Kanalboden) | Al Winkel, z +530…+545, y +8…+65, x ±215; EPDM-Lippe zum Schieber (Restspalt 0); Ablauf Ø 6 | 3 |
| 20 | Sturzblende | Al 5754, t 3, x ±215, y +62…+65, z +530…+1140, Sicherheitsschrauben A4 | 1, 3 |
| 21 | Antriebskasten | Al t 2; außen B 550 × T 140 (y −40…+100); z +1140…+1400 (Entenseite), Deckel ≥ 10° fallend zur −y-Seite; Druckausgleichselement; Bürstendichtung Kanal/Kasten | 1, 2 |
| 22 | Endschalter | B3 Bolzen +1200 (5 Überlauf); B4 Bolzen +594; B1 UK Blech ≤ +32; B2 OK Blech ≥ +1110 | 3 |
| 23 | Lichtschranke B6 | 2 Strahlen z +100 und +300, y +20, Sender/Empfänger in den Führungsträgern außerhalb x ±175 | 1, 2 |
| 24 | Pfosten | □ 60×60×3 fvz, x-Mitte ±245 (lichter Abstand 430), z 0…+1140, Fußplatte 160×160×10 | 1, 2 |
| 25 | Gesamtmaße | H ≈ 1400 über OKF (≈ 1420 über Gelände); B 550; T 140 (Kasten) bzw. ≈ 160 mit Schwellenwinkel | 1, 2 |
| 26 | Fundament, Schürze, Zaunanschluss | unverändert nach R1 Abschnitt 3, Pos. 15–17 | – |

Hinweis: v1 nennt „≈ 1320 + Spindelüberstand“. Mit Motor, Kupplung und Loslager über der oberen Mutterstellung ergeben sich ≈ 1400 [R]. Weniger Höhe ist möglich, wenn der Motor neben der Spindel sitzt und über einen Zahnriemen antreibt [A].

---

## 4 Offene Punkte
1. Motor-Kennlinie Moment über Drehzahl bei 24 V für den gewählten Motor beschaffen.
2. Reibwert der gewählten Mutter (Datenblatt) beschaffen und Selbsthemmung neu bewerten.
3. Hebelkraft von Fuchs und Waschbär ist nicht belegt (300 N angesetzt [A]).
4. Gatterlogik für ENABLE und Strombegrenzung mit dem Elektro-Review abstimmen.
5. Kinderspezifische Öffnungsweiten nach EN ISO 13857 am Normtext prüfen. Die Tabelle gilt laut Pilz erst ab 14 Jahren [Q16].

---

## 5 Quellen
- [Q1] ZIMM, Konstruktionshinweise Gewindetechnik (tan ρ′ ≈ 1,07·µ; η = tan α / tan(α+ρ′); d₂ = d − 0,5·P), nur über Suchauszug geprüft, weil der Host im Netz dieser Sitzung gesperrt ist – https://de.zimm.com/wp-content/uploads/2018/10/konstruktionshinweise-gewindetechnik_1.pdf
- [Q2] Neff, Berechnungsgrundlagen Trapezgewindetriebe („keine Selbsthemmung > 4,5°“), nur über Suchauszug geprüft – https://neff-gewindetriebe.de/fileadmin/PDF-Datenblaetter/berechnungsgrundlagen/trapezgewindetriebe/berechnungsgrundlagen_tgt.pdf
- [Q3] Wikipedia, Leadscrew (Vibration hebt die Selbsthemmung auf, zusätzliche Bremse) – https://en.wikipedia.org/wiki/Leadscrew
- [Q4] ZIMM Wiki, Self-locking in screw jacks (Selbsthemmung ist statisch, keine Bremse) – https://zimm.com/ai/wiki/what-is-self-locking-in-screw-jacks-and-when-is-it-important.md
- [Q5] igus, Self-locking Wiki (gilt nur, solange die Haftreibung nicht überschritten wird) – https://www.igus.eu/threaded-rod/wiki/self-locking
- [Q6] igus, dryspin Trapezgewindespindeln (eingängig selbsthemmend, zweigängig nur resthemmend) – https://www.igus.de/dryspin/trapezgewindespindeln
- [Q7] StepperOnline 17HS19-2004S1 (0,59 Nm, 2 A, 42 × 48 mm) – https://omc-stepperonline.com/nema-17-bipolar-59ncm-84oz-in-2a-42x48mm-4-wires-w-1m-cable-and-connector.html
- [Q8] 17HS4401(S), Datenblatt (40…43 Ncm, 40 mm) – https://datasheetspdf.com/datasheet/17HS4401S.html
- [Q9] PBC Linear, NEMA-17-Datenblatt (Wellenlast axial 25 N Druck / 65 N Zug) – https://www.scribd.com/document/367922371/Motor-a-Pasos-Nema-17-Data
- [Q10] Beckhoff, Reibwerttabelle (Stahl/Messing 0,19 / 0,35) – https://infosys.beckhoff.com/content/1031/tc_motion_designer/2761712779.html
- [Q11] BASF, Reibung und Verschleiß bei Polymerwerkstoffen (POM rauigkeitsempfindlich) – https://download.basf.com/p1/8a8081c57fd4b609017fd66047f138c3/de/Reibung_und_Verschlei%25C3%259F%250Abei_Polymerwerkstoffen
- [Q12] ISO 13854:2017 / EN ISO 13854:2019, Mindestabstände (Finger 25, Hand 100, Arm 120, Kopf 300, Körper 500 mm; Kinder berücksichtigen) – https://cdn.standards.iteh.ai/samples/66459/46ce3b47790e4526802912dbbd921354/ISO-13854-2017.pdf
- [Q13] Analog Devices/Trinamic, TMC2209 Datenblatt (2 A RMS, IHOLD/IRUN, StallGuard4 mit StealthChop) – https://www.analog.com/en/tmc2209
- [Q14] BGN, DGUV Regel 208-022 Kap. 6 (400 N dyn., 150 N stat., 25 N Restkraft nach EN 12453) – https://vorschriften.bgn-branchenwissen.de/daten/dguv/208_022/6.htm
- [Q15] Analog Devices, AN-002 StallGuard/CoolStep (Geschwindigkeitsbereich) – https://www.analog.com/en/resources/app-notes/AN-002.html
- [Q16] Pilz, Booklet Safety Distance (Tabelle Durchgreifen ab 14 Jahren) – https://www.pilz.com/mam/pilz/content/editors_subsidiaries/tg-de/presentations/booklet_safety_distance.pdf

Nicht belegt, als [A] gekennzeichnet: Moment bei Drehzahl, Reibwert der Mutter, Rastmoment, Hebelkraft von Raubtieren, Eis-Losbrechkraft, d₃ nach DIN 103, Lagertragzahlen 626.
