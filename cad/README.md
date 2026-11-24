# DuckDoor – 3D-CAD-Modell (CadQuery)

3D-Modell der Entenklappe DuckDoor, erzeugt aus den Zeichnungen TZ-01/TZ-02 (`drawings/`) und der Maßliste R2-11.
Das Modell ist vollständig skriptbasiert (CadQuery 2.8) und wird aus `cad/src/` regeneriert.

## Inhalt

| Datei / Ordner | Inhalt |
|---|---|
| `DuckDoor_Baugruppe.step` | STEP AP214 (AUTOMOTIVE_DESIGN), Baugruppe „DuckDoor_Baugruppe“ mit Unterbaugruppen GRUENDUNG, GESTELL, FUEHRUNG, SCHIEBER, ANTRIEB, KASTEN, ELEKTRO, KAUFTEIL; 85 benannte, farbige Bauteile |
| `DuckDoor_Baugruppe.glb` | glTF-Binärvorschau (z. B. im Browser, Windows 3D-Viewer, Blender) |
| `parts/<Name>.step` | 85 Einzelteile als STEP AP214 (Produktname = Bauteilname) |
| `Teileliste_CAD.csv` | Teileliste, `;`-getrennt, Dezimalkomma, UTF-8 mit BOM (Excel): Name; Pos; Gruppe; Material; Kaufteil; Volumen_cm3; Masse_kg; BBox; Bemerkung |
| `Kollisionsprotokoll.txt` | automatisch erzeugtes Prüfprotokoll (siehe unten) |
| `preview/*.png`, `*.svg` | Vorschaubilder: 01 iso Entenseite, 02 iso Raubtierseite, 03 Detail Mitnehmer, 04 Detail Antriebskasten |
| `src/common.py` | Schnittstelle: `Part`-Datenklasse, Farben, Hilfsfunktionen |
| `src/parts_gestell.py` | Team Gestell: Gründung, Gestell, Führung, Kanal/Kasten, Schaltkasten (45 Parts) |
| `src/parts_antrieb.py` | Team Antrieb: Schieber, Mitnehmer, Spindelantrieb, Klinke, Sensorik (40 Parts inkl. 2 × 26a) |
| `src/build_assembly.py` | Integration: Baugruppe, Exporte, Teileliste, Kollisionsprüfung, Vorschau |

Teileanzahl je Unterbaugruppe: GRUENDUNG 13, GESTELL 6, FUEHRUNG 8, SCHIEBER 4, ANTRIEB 21, KASTEN 15, ELEKTRO 11, KAUFTEIL 7 (gesamt 85, davon 34 Kaufteile).

Masse der Eigenfertigungsteile (CSV, Dichten Stahl 7,85 / Edelstahl 7,95 / Alu 2,70 / PE-UHMW 0,94 / EPDM 1,2 / Beton 2,4 / sonst 1,0 [A]):
**≈ 524 kg**, davon Streifenfundament 460 kg, übrige Gründung (Schürze als Vollblech, Fußplatten) ≈ 35 kg,
Stahl-/Alu-Bau oberhalb OKF ≈ 28 kg. Kaufteile ohne Masse („–“). Schürze 2 und Spaltabdeckung 4 sind als
Vollblech gerechnet – real (Gitter/Lochblech) deutlich leichter.

## Koordinatensystem und Zustand

* Einheit **mm**, alle Teile direkt in **globalen Koordinaten** modelliert (identisch TZ-01/TZ-02):
  * x = 0 Mitte Lichtöffnung (quer zur Durchgangsrichtung); „links“ = +x, „rechts“ = −x (wie Vorderansicht TZ-01) [A]
  * y = 0 Mittelebene Schieber; **+y = Entenseite** (Gehege), −y = Raubtierseite
  * z = 0 Oberkante Fundament (OKF); Gelände = −20
* Dargestellter Zustand: **ZU_VERRIEGELT** (UK Schieber +30, OK Schieber +565, Mitnehmerbolzen z +594).
* Zustand AUF (nur für die Prüfung): Schieberteile +550, Mutterblock/Bolzen/Kulisse/Reed +601 in z.

## Import

### Onshape
1. Dokument öffnen oder neu anlegen → **Import** (Pfeil-Symbol „+“ unten links → *Import*) → `DuckDoor_Baugruppe.step` wählen.
2. Im Importdialog **„Import as assembly“ / Baugruppe** belassen (Standard für Mehrkörper-STEP); „Flatten assembly“ nicht wählen, damit die Unterbaugruppen erhalten bleiben.
3. Einheiten: STEP enthält mm – falls abgefragt, **Millimeter** wählen.
4. Ergebnis: ein Assembly-Tab mit 8 Unterbaugruppen und Part Studios für die Teile; Farben werden übernommen.

### SolidWorks
1. **Datei → Öffnen**, Dateityp **STEP AP203/214/242 (*.step;*.stp)**, `DuckDoor_Baugruppe.step` wählen.
2. Unter *Optionen…*: „Als Baugruppe importieren“ (Standard für Mehrkörper-STEP), ggf. „3D Interconnect“ deaktivieren, wenn bearbeitbare Teile gewünscht sind.
3. Einheiten: mm (aus der Datei). Ergebnis: Hauptbaugruppe `DuckDoor_Baugruppe` mit 8 Unterbaugruppen, alle Komponenten **fixiert**.

Einzelteile aus `parts/` können genauso als Teil geöffnet werden (Lage in globalen Koordinaten – Ursprung ist der Baugruppen-Ursprung, nicht das Teilezentrum).

## Hinweise

* **Keine Mates/Verknüpfungen** – alle Teile sind in globalen Koordinaten fixiert. Für Bewegungsstudien Schieber/Mutterblock im CAD-System selbst verknüpfen.
* **Gewinde nicht modelliert** (Tr8×2, M-Gewinde als Kern- bzw. Nenndurchmesser-Zylinder); Schweißnähte, Fasen/Radien weitgehend nicht modelliert.
* **Kaufteile vereinfacht** (Hüllkörper): Schaltleiste, Lager, Motor, Sensoren, Lichtschranke, Bürstendichtung, Schaltkasten, Anker, Schrauben.
* Schürze 2 als Vollplatte t 2 statt Schweißgitter; Spaltabdeckung 4 ohne Lochung.
* Alle Annahmen sind in den Bauteil-Notizen mit **[A]** gekennzeichnet (Spalte „Bemerkung“ der CSV).
* Seitenbezeichnung links/rechts, Lage Schaltkasten, Warnschild Raubtierseite, Haltewinkel 26a: Annahmen [A].

## Integrationsänderungen (durch CAD-Integrator, als [A] in den Notizen dokumentiert)

1. **Bürstendichtung 38** (`parts_gestell.py`): Durchtritt von x ±25 auf **x −38…+25** erweitert. Grund: Hubweg-Prüfung zeigte, dass die Entriegelungskulisse 42 (x −34…−15) beim Fahren nach AUF die Dichtung durchfährt (Hub ≈ 541…583, 216 mm³).
2. **Haltewinkel Lagerplatte, Pos 26a** (neu, `parts_antrieb.py`, 2 Stück, EN AW-5754 t 3): Z-Kantteil x ±32…±60, Fuß auf dem Kastenboden y +65…+96 (außerhalb der Bodenöffnung y −3…+65), Kopf unter der Lagerplatte 26 (z +1242…+1245). Die Lagerplatte hatte vorher keine Befestigung. Motorplatte 28/Motor 30 hängen über Distanzbolzen 29 an der Lagerplatte.

## Geprüfte Schnittstellen

| Schnittstelle | Ergebnis |
|---|---|
| Traverse 31 Bohrung Ø22 bei (x 0, y 35) ↔ Zentrierbund Lagerbock 21 Ø22 (x 0, y 35, z +535…+545) | Lage passt, Lagerbock sitzt auf OK Traverse +545. **Passung Ø22/Ø22 ohne Spiel** – Toleranz festlegen (z. B. Bohrung Ø22 H11, Bund Ø22 h9) |
| Kasten 35 y −40…+100 (außen, t 2) ↔ Annahme Antrieb y −38…+98 | stimmt (−38…+98 ist das Innenmaß) |
| Lagerplatte 26 (y +5…+65, z +1245…+1255) und Motor 30 (z bis +1343) im Kasten | liegen im Kasten; Abstand Motor-OK zu Deckel-UK ≈ 40 mm; keine Kollision; Befestigung über 26a ergänzt |
| Durchtritt Bürstendichtung | erweitert (s. o.); Lasche x ±20, Mutterblock x ±15, Spindel x 0 frei |

## Kollisionsprotokoll

Kriterium: Schnittvolumen > 1 mm³ (BRep-Schnitt, paarweise, mit Bounding-Box-Vorfilter). Details: `Kollisionsprotokoll.txt`.

| Prüfung | Paare | Ergebnis |
|---|---|---|
| ZU_VERRIEGELT, alle 85 Parts paarweise | 3570 | **0 Kollisionen** |
| AUF: 11 bewegte gegen 74 feste Teile | 814 | **0 Kollisionen** |
| AUF: bewegte untereinander | 55 | **0 Kollisionen** |

Bewegte Teile (Zuordnung aus `parts_antrieb.py`): +550 – Schieberblech 13, Schaltleiste 14, Lasche 15, Senkschrauben 16, Magnet 47; +601 – Bolzen 17, Mutterblock 18, Spindelmutter 19, Kulisse 42, Reedkontakt 47. Klinke 39, Achse 40 und Halter 41 stehen auf der Traverse 31 und sind **fest**.

Zusätzlich Hubweg ZU → AUF (101 Zwischenstellungen, reine z-Translation, Klinke ohne Drehung) – nach der Korrektur der Bürstendichtung verbleiben:

| Paar | Hub | Bewertung |
|---|---|---|
| Lasche 15 / Senkschraube 16 ↔ Klinke 39 | 5…83 | funktional: Klinke wird vorher von der Kulisse ausgeschwenkt (Drehung nicht simuliert) |
| Kulisse 42 ↔ Klinke 39 | 24…72 | beabsichtigt: Kulissenschräge hebt die Klinke aus |
| **Schaltleiste 14 ↔ Abstreiflippe 32** | 500…528 | **offen**: Schaltleiste (y ±6) überdeckt die Lippe (y +2…+8) um 4 mm beim Einfahren in den Kanal → Risiko Fehlauslösung B7 / Verschleiß. Nicht durch Geometriekorrektur ohne Funktionsentscheidung lösbar (Lippe ausklinken, Lippe auf Schieber verlegen oder B7 oberhalb z ≈ +500 per Software maskieren) |

## Offene Punkte

* Schaltleiste 14 streift Abstreiflippe 32 beim Hub (s. o.) – Entscheidung Mechanik/EL.
* Passung Zentrierbund Lagerbock 21 / Traverse 31 (Ø22/Ø22) festlegen; Schrauben Lagerbock nicht modelliert.
* Halter für Endschalter B2/B3/B4 sowie Befestigung Kulisse/Reed am Mutterblock nicht modelliert (Team Antrieb).
* Klinkenachse 40: Sicherung offen (siehe Notiz).
* Gewinde, Verschraubungen (Deckel, Lagerplatte/26a), Kabel/Verschraubungen Schaltkasten nicht modelliert.

## Regenerieren

```bash
# einmalig
python -m venv /home/user/cadenv && /home/user/cadenv/bin/pip install cadquery==2.8.0
# Modell bauen (aus dem Repo-Wurzelverzeichnis), Dauer ≈ 15 s
/home/user/cadenv/bin/python cad/src/build_assembly.py
# Optionen: --no-preview (keine Bilder), --no-sweep (ohne Hubweg-Prüfung)
```

Die PNG-Vorschau nutzt Node.js mit dem global installierten Paket `playwright` (Chromium); fehlt es, werden nur die SVG-Dateien erzeugt. Die Vorschau ist ein einfacher Flächen-Renderer (Parallelprojektion, Maleralgorithmus) – kleine Darstellungsfehler an berührenden Flächen sind möglich.
