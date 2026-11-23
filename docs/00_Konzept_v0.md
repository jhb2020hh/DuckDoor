# Entenklappe „DuckDoor“ – Konzept v0 (Review-Entwurf)

Status: Entwurf zur fachübergreifenden Prüfung. Alle Maße/Werte sind Annahmen, sofern nicht belegt.

## 1 Anforderungen (vom Bauherrn bestätigt)
| Nr | Anforderung |
|---|---|
| R1 | Tür für Laufenten, Lichtmaß 350 × 500 mm (B × H), vertikaler Schieber |
| R2 | Eigenständige Einheit mit eigenem Rahmen/Pfosten, in Zaunlinie eingebunden, Freiluft (Regen, Frost, UV, Schmutz) |
| R3 | Versorgung 230 V AC, Zuleitung am Standort vorhanden |
| R4 | Steuerung ausschließlich mit Shelly-Geräten (kein ESP32); mehrere Shelly zulässig |
| R5 | WLAN am Standort vorhanden |
| R6 | Fernbedienung über Internet (Shelly Cloud/App), Absicherung „Authenticator“ gewünscht – **TOTP-2FA der Shelly Cloud nicht belegt, offen** |
| R7 | Betriebsarten: Timer (feste Uhrzeit), Astro (Sonnenauf-/-untergang + Offset), Lichtsensor, manuell (App + Vor-Ort-Taster) |

## 2 Systemkonzept
- **Steuerung:** Shelly Plus 2PM (Gen2/Gen3/Gen4 je Verfügbarkeit) im Cover-Modus. Zeitpläne inkl. Sonnenauf-/-untergang mit Offset nativ im Shelly.
- **Sensorik:** Shelly Plus Add-on am 2PM: Analogeingang 0–10 V für Lux-Messumformer; Digitaleingang für Endlagenmeldung „ZU“ (Reedkontakt) zur Zustandsprüfung (Klappe hängt fest/vereist).
- **Vor-Ort-Taster:** SW1/SW2 des 2PM (Auf/Ab), Taster IP67 am Gehäuse.
- **Fernzugriff:** Shelly Cloud + App. Zusätzlich lokal Web-UI mit Passwort (Digest-Auth). Keine Portfreigabe.

### 2.1 Antriebsvarianten (Entscheidung durch Review)
| | B1 Rohrmotor + Gurt (Schwerkraftschluss) | B2 24-V-DC-Linearantrieb (Spindel) |
|---|---|---|
| Prinzip | 230-V-Rollladen-Rohrmotor Ø35 mm mit mech. Endlagen wickelt Gurt; Schieber schließt durch Eigengewicht | Spindel-Linearantrieb mit int. Endschaltern schiebt Schieber aktiv |
| Ansteuerung | Direkt 2PM (Cover-Modus, typischer Anwendungsfall) | 2PM + 2 Koppelrelais (Polwende/H-Brücke) + 24-V-Netzteil |
| Klemmgefahr Tier | Schließkraft = Gewicht Schieber (≈ 20 N, Annahme) → gering | Schließkraft typ. 100–1000 N → **hoch**, Schutzeinrichtung nötig |
| Aufhebelschutz | Motorbremse hält Gurt → Schieber nicht anhebbar (zu prüfen) | Spindel selbsthemmend |
| Hinderniserkennung | Gurt läuft schlaff, Schieber liegt auf → keine Quetschkraft | Leistungsmessung 2PM wirkt nur auf Relaisspulen → nicht nutzbar |
| Frost | Schieber kann festfrieren → „ZU“ nicht erreicht → Reedkontakt meldet | Antrieb kann Eis brechen |

Vorschlag v0: **B1**.

## 3 Mechanik (Vorschlag)
- Schieber PE-HD 10 mm, 400 × 560 mm (Überdeckung 25 mm seitlich, 30 mm oben), Masse ≈ 2,1 kg (Rechnung 0,40·0,56·0,01 m³ · 950 kg/m³).
- Führungen: Aluminium-U-Profil 20×15 mm, unten offen (Schmutz/Eis fällt heraus), Bodenanschlag nicht als Rinne.
- Rahmen: Aluminium-Vierkant 40×40 mm, Höhe Unterkante bis Oberkante Antriebskasten ≈ 1250 mm (Lichtmaß 500 + Hub 520 + Antriebskasten ~200 + Schwelle ~30).
- Pfosten: 2× Stahl verzinkt 60×60 mm, Einschlaghülse oder Punktfundament; Zaunanschluss links/rechts mit Spannschellen.
- Antriebskasten oben: Rohrmotor + Wickelwelle, regengeschützt, Wartungsdeckel.
- Untergrabschutz: Bodenplatte/Schwelle Beton oder Drahtgitter 50 cm horizontal (Fuchs).
- Schwelle ≤ 50 mm Höhe (Laufenten, Annahme).

## 4 Elektrik (Vorschlag)
- Zuleitung 230 V vorhanden → Anschluss in Schaltkasten IP65 am Rahmen.
- Vorgeschaltet: RCD 30 mA (Bestand prüfen) + LS B10/B16 im Bestand.
- Schaltkasten: Hutschiene, Shelly Plus 2PM, Add-on, Klemmen, Druckausgleichselement, ggf. Heizwiderstand gegen Kondensat.
- Motorleitung H07RN-F 4G0,75 (L↑, L↓, N, PE).
- Lux-Messumformer 0–10 V, Versorgung 24 V DC → Netzteil Hutschiene 24 V.
- Reedkontakt „ZU“ an Add-on Digitaleingang.

## 5 Offene Punkte
1. TOTP-2FA Shelly Cloud: belegt / nicht belegt? Falls nein: Alternative?
2. B1 vs. B2.
3. Kondensatschutz Gehäuse.
4. Lux-Sensor-Typ (Add-on-Analog vs. Shelly BLU mit Lux per Bluetooth).
5. Normative Anforderungen (Elektro, Maschinen-/Tierschutz).
