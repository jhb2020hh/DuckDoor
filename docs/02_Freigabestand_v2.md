# Entenklappe „DuckDoor“ – Freigabestand v2 (Übergabe an Abwicklung)

Basis: `01_Konzept_v1.md` + Review Runde 2 (`review/11_R2_Mechanik_Sicherheit.md`, `review/12_R2_Elektro_IT.md`).
Bei Widerspruch gilt dieses Dokument vor v1. Kennzeichnung [A] = Annahme.

## 1 Verbindliche Änderungen gegenüber v1
### Mechanik
| Nr | Festlegung |
|---|---|
| M1 | Langloch-Logik: **Heben über oberes Langlochende, Verriegeln über unteres** (v1 war vertauscht). Freiweg ≈ 52 mm. |
| M2 | **Passive Schwerkraftklinke** als Aufhebelschutz zusätzlich zur Spindel (Tr8×2 allein nicht sicher selbsthemmend). Entriegelung durch Mutter innerhalb des Freiwegs. |
| M3 | Spindel: **Festlager unten**, Loslager oben, Klauenkupplung zum Motor (keine Axiallast auf Motorwelle). |
| M4 | Motor NEMA 17, **48 mm Baulänge, ≥ 0,59 Nm**. Spindel Edelstahl, Mutter Kunststoff, trocken. |
| M5 | Spindel + Mitnehmer im geschlossenen Kanal hinter Sturzblende; Einhausung mit Sicherheitsschrauben (Einzugsstellen). |
| M6 | Schlaffschalter **B8** am Mutterblock (Mutter läuft ohne Schieberlast). |
| M7 | Gesamtmaße ≈ **H 1400 × B 550 × T 140 mm**. Maßliste: `review/11_R2_Mechanik_Sicherheit.md`. |
| M8 | Hinweis Betreiber: Personentür des Nachtgeheges von innen öffenbar (Kind eingeschlossen). |

### Elektrik / Elektronik
| Nr | Festlegung |
|---|---|
| E1 | Reparaturschalter **-Q1** allpolig im Kasten, LS **-F1 B6 1P+N**, Netzteil **-T1 Mean Well HDR-100-24** (24,0 V fest). Leistungsbilanz ≈ 52 W. |
| E2 | 24-V-Abgänge über Feinsicherungen **-F11…-F15**. |
| E3 | **Hardware-Sperre Richtung ZU** durch Schaltleiste B7 und Lichtschranke B6 (TMC ENABLE), unabhängig von Firmware. Lichtschranken-Test vor jedem Schließen. B1 über Spindelposition plausibilisiert. |
| E4 | Getrennte Strombegrenzung AB (Ziel ≤ 50 N, max. 150 N); Losbrechen ≤ 2 mm/s; Fahrt 10–20 mm/s. |
| E5 | ESP32-WROOM-32UE-N8 (Chip-Rev. ≥ V3), TMC2209-Steckmodul (Alt. TMC2240), RTC **DS3231SN**, Eingänge **ISO1212**, Lux-Sensor hinter Fenster im Gehäusedeckel (kein I²C-Außenkabel). |
| E6 | Heizung 24 V / 20 W [A] + Temperatur-/Feuchtesensor + Bimetall-Begrenzer in Reihe. |
| E7 | Lichtschranke Marantec 99165, Schaltleiste ASO SENTIR edge 8,2 kΩ + Auswerter (Kat. 3). |
| E8 | Pinbelegung, Klemmenplan -X1/-X2, Single-Line- und Blockschaltbild-Vorgabe: `review/12_R2_Elektro_IT.md`. |

### IT
| Nr | Festlegung |
|---|---|
| I1 | RLS: `aal2` **und** Gerätezugehörigkeit (`device_members`); öffentliche Registrierung deaktiviert. |
| I2 | Gerät als eigener Device-User, Zugriff nur über RPC-Funktionen; Polling 5 s; Realtime optional später. |
| I3 | Flash-Encryption + Secure Boot V2, Credentials in verschlüsseltem NVS. |
| I4 | Nachtsperre zweistufig (Server-Trigger + Gerät), Befehle mit Nonce und 60 s Gültigkeit, OTA nur Owner/Stillstand mit Rollback. |
| I5 | Referenzfahrt nach Stromausfall nachts nicht öffnend; bei B1 aktiv Referenz nach unten (B4). |

## 2 Offene Punkte (blockieren den Entwurf nicht)
| Nr | Punkt | Annahme für Entwurf |
|---|---|---|
| O1 | Standort **PLZ 22397 Hamburg** (Duvenstedt/Wohldorf-Ohlstedt/Lemsahl-Mellingstedt), Koordinaten für Astro ≈ 53,70° N / 10,10° E [A, auf Grundstück präzisieren]. Rekord-Tiefstwert Hamburg-Fuhlsbüttel −29,1 °C (13.02.1940, DWD-Daten lt. Sekundärquelle). Norm-Außentemperatur DIN/TS 12831-1 für 22397 nicht belegt (BWP-Klimakarte prüfen). | **Auslegung −10 °C** [Bauherrenvorgabe 2026-11-23]. Restrisiko: Tiefere Temperaturen am Standort möglich (Rekord −29,1 °C). Marantec 99165 (−20 °C) bleibt zulässig. Firmware: bei Außentemperatur < −10 °C Warnmeldung (Betrieb außerhalb Auslegung), < −20 °C Störmeldung (Lichtschranke außerhalb Spezifikation). Gehäuseheizung bleibt (Kondensat). |
| O2 | Isolations-/Datenblattwerte Netzteil, Lichtschranke, Motor-Kennlinie 24 V am Original prüfen | gem. Review |
| O3 | Anwendbarkeit DIN VDE 0100-705 (landwirtschaftl. Betriebsstätte) durch Errichter | Schutzpotentialausgleich Rahmen vorgesehen |
| O4 | Supabase-Angaben (Limits) am Original prüfen | gem. Review |
