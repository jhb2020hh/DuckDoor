# Entenklappe „DuckDoor“ – Konzept v1

Status: konsolidiert nach Fachreview Runde 1 (`docs/review/01…05`) und Bauherrenentscheidungen. Ersetzt v0.
Kennzeichnung: **[A]** = Annahme/Schätzung, **[B]** = beim Bauherrn bestätigt, **[R]** = aus Review übernommen.

## 1 Anforderungen
| Nr | Anforderung | Status |
|---|---|---|
| R1 | Laufenten, ≤ 6 Tiere, größter Erpel ≤ 45 cm → Lichtmaß **350 × 500 mm**, vertikaler Schieber | [B] |
| R2 | Eigenständige Einheit mit eigenem Rahmen/Pfosten, in Zaunlinie, Freiluft | [B] |
| R3 | 230 V AC am Standort vorhanden | [B] |
| R4 | Antrieb **Schrittmotor** mit Trapezgewindespindel | [B] |
| R5 | Steuerung **eigene Platine mit ESP32** (Löten/Bestücken durch Bauherrn) | [B] |
| R6 | Fernbedienung über Internet, **Authenticator (TOTP)** zwingend → Web-App Vercel + Supabase Auth MFA | [B] |
| R7 | Betriebsarten: Timer, Astro + Offset, **Lichtsensor**, manuell (App + Vor-Ort-Taster) | [B] |
| R8 | **Kinder haben Zugang** → Lichtschranke + Schaltleiste + Warnschild | [B] |
| R9 | WLAN am Standort vorhanden | [B] |
| R10 | Vercel (Hobby) und Supabase (Free) vorhanden | [B] |

## 2 Systemarchitektur
```
[Smartphone/Browser] --HTTPS--> [Vercel: Web-App (Next.js)] --supabase-js--> [Supabase: Auth (Passwort+TOTP), Postgres+RLS, Realtime]
                                                                                    ^
                                                              ausgehend TLS (WSS/HTTPS), keine Portfreigabe
                                                                                    |
[Klappe vor Ort: ESP32-Platine] -- WLAN --> [Router]
```
- Steuerbefehle werden nur akzeptiert mit JWT-Claim `aal = 'aal2'` (TOTP verifiziert), durchgesetzt per RLS-Policy. Quelle: https://supabase.com/docs/guides/auth/auth-mfa
- **Lokale Autarkie:** Timer, Astro, Lux, Sicherheitsfunktionen laufen auf dem ESP32. Internetausfall ≠ Funktionsausfall.
- **Uhrzeit:** NTP + RTC DS3231 mit Pufferbatterie (Review IT: Uhrzeit nach Stromausfall ohne Internet unbekannt) [R].
- **Nachtsperre:** Fern-„AUF“ zwischen Astro-Untergang und -Aufgang nur mit zusätzlicher Bestätigung in der App.
- Kein Shelly.

## 3 Mechanik
### 3.1 Antrieb: Schrittmotor + Spindel + Langloch-Mitnehmer (Schwerkraftschluss mit formschlüssiger Verriegelung)
- NEMA 17, Trapezspindel **Tr8×2** (selbsthemmend [A]: Steigungswinkel ≈ 5,2° < Reibwinkel Stahl/Messing-Mutter ≈ 5,7–11° bei µ 0,1–0,2), Mutter Messing/POM.
- Mutter trägt Bolzen, der in einem **Langloch (≈ 60 mm [A])** am Schieber läuft:
  - **AUF:** Bolzen liegt am unteren Langlochende an und hebt den Schieber.
  - **ZU:** Mutter fährt abwärts, Schieber folgt **nur durch Eigengewicht** (≈ 23 N, Rechnung Alu 0,40·0,56·0,004 m³·2660 kg/m³ = 2,4 kg). Liegt er auf einem Tier/Kind auf, läuft der Bolzen im Langloch frei → keine Motorkraft auf das Hindernis.
  - **Verriegeln:** Erst wenn Sensor „Schieber unten“ (B1) aktiv ist, fährt die Mutter den Rest-Hub, bis der Bolzen am **oberen** Langlochende aufsitzt → Schieber formschlüssig über selbsthemmende Spindel gegen Anheben gesichert. Ohne B1 kein Verriegelungshub (Firmware) + Strombegrenzung/StallGuard als Rückfallebene.
  - Freie Fallhöhe begrenzt auf Langlochlänge.
- Geschwindigkeit ≤ 20 mm/s [A] (Review Tierhaltung: ≤ 0,1 m/s), Fahrzeit ≈ 30–60 s [A].
- Referenzierung: Endschalter „Mutter oben“ (B3) und „Mutter unten“ (B4); B2 „Schieber oben“.

### 3.2 Bauteile [R aus Review Mechanik, angepasst]
- Schieber Alu EN AW-5754, 4 mm, 400 × 560 mm, Unterkante mit weichem Gummiprofil (Schaltleiste 8,2 kΩ, s. Elektrik).
- Führungen PE-UHMW, Nut 6 × 30 mm; unten offen (Schmutz/Eis).
- Hub 550 mm. Gesamthöhe ≈ 1320 mm + Spindelüberstand [A] – Antriebskasten oben nimmt Motor auf (kein 600 mm Rohrmotor mehr → Kasten schmaler).
- Pfosten Stahl 60×60×3 feuerverzinkt, lichter Abstand 430 mm, Achsabstand 490 mm; Fundament frostfrei 800 mm tief.
- Schwelle ≤ 30 mm, gefast; Spalt unter Schieber ≤ 10 mm, sonst ≤ 20 mm [R].
- Untergrabschutz: Schürze ≥ 500 mm, 1000 mm breit, lückenloser Zaunanschluss, Zaun mit eigenen Abspannpfosten [R].
- Spindel geschützt (Faltenbalg oder Abdeckprofil) gegen Schmutz/Eis [A].

## 4 Elektrik / Elektronik
- 230 V nur bis Netzteil: Zuleitung Bestand (RCD 30 mA + LS im Bestand prüfen) → Klemme -X1 → LS B6 (-F1) → Netzteil 24 V DC Hutschiene (-T1), Betriebstemperatur ≥ −25 °C [A, prüfen].
- Alles nach -T1 SELV 24 V: Motor, Sensoren, Taster, Lichtschranke, Heizung.
- **Platine (-A1):** ESP32-Modul mit U.FL-Antennenanschluss + externe Antenne; Schrittmotortreiber TMC2209 (UART, Strombegrenzung, StallGuard); DC/DC 24→5/3,3 V; RTC DS3231; Eingänge optogekoppelt/geschützt 24 V für B1–B4, Lichtschranke, Schaltleiste (8,2-kΩ-Auswertung), Taster AUF/ZU; I²C für Lux-Sensor; 1-Wire DS18B20 Gehäusetemperatur; MOSFET-Ausgang Gehäuseheizung; Status-LED; Programmierschnittstelle.
- **Lichtsensor (-B5):** Vorschlag digital I²C (VEML7700/BH1750) in IP67-Gehäuse mit Lichtfenster, Leitung ≤ 1 m [A]. Alternative 0–10 V Messumformer (≈ 100 € [R]).
- **Sicherheit Kinder/Tiere:** Lichtschranke (-B6) in Durchgangsebene, Schaltleiste (-B7) an Schieberunterkante; beide stoppen Schließen und lösen Wiederauffahren aus.
- **Gehäuse (-U1):** IP65/IP66, Druckausgleichselement, Heizung 24 V thermostatisch (Kondensat/Frost) [R], Kabelverschraubungen, Potentialausgleich Rahmen/Pfosten prüfen [R].
- Motor-/Sensorleitungen: H07RN-F bzw. PUR-Steuerleitung, UV-beständig.

## 5 Software
- **Firmware (ESP32, Arduino/ESP-IDF):** Zustandsautomat (REFERENZ, ZU_VERRIEGELT, ÖFFNEN, AUF, SCHLIESSEN, VERRIEGELN, STÖRUNG); Astro-Berechnung lokal; Lux-Hysterese (Schließen frühestens Astro-Untergang + X UND Lux < Schwelle seit 10 min, spätestens Uhrzeit Y) [R]; Supabase-Anbindung (Realtime-WSS, Fallback HTTPS-Polling); OTA-Update signiert.
- **Supabase:** Tabellen `devices`, `commands`, `device_state`, `events`, `schedules`; RLS: `commands` INSERT nur `aal2`; Gerät mit eigenem, eingeschränktem Zugang (nur eigene Zeilen).
- **Web-App (Vercel):** Login + TOTP-Enrollment, Status, AUF/ZU, Zeitplan, Protokoll, Störmeldung (Web-Push oder E-Mail [A]).

## 6 Offene Punkte für Review Runde 2
1. Langloch-Mitnehmer: Funktion, Selbsthemmung Tr8×2 im Freien (Vibration, Fett, Eis), Verriegelungssicherheit.
2. Lichtschranke/Schaltleiste: Bauart für 24 V, Bewertung gegenüber Schwerkraftschluss.
3. Geräteauthentifizierung ESP32 ↔ Supabase (Schlüsselablage, Rotation, Free-Tier-Limits Realtime).
4. Netzteiltyp, Temperaturbereich, Heizleistung.
