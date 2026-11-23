# Review 03 – Steuerung (MSR) und IT-Sicherheit

Grundlage: `docs/00_Konzept_v0.md` (Shelly Plus 2PM im Cover-Modus mit Plus Add-on, WLAN, Shelly Cloud/App, Anforderung „Authenticator“).
Rolle: Automatisierer (MSR/GA) und IT-Security. Stand der Recherche: 23.11.2026.

**Hinweis zur Methode:** Die Herstellerseiten (shelly-api-docs.shelly.cloud, kb.shelly.cloud, community.shelly.cloud, shelly-forum.com, support.shelly.cloud) waren aus der Review-Umgebung **nicht direkt abrufbar**, weil die Hosts nicht freigegeben sind. Alle Belege stammen deshalb aus den Treffern und Auszügen der Websuche auf diesen Domains. Wortlaute vor der Umsetzung bitte am Original prüfen. **[A]** kennzeichnet eine Annahme oder Bewertung des Reviewers ohne Herstellerbeleg.

---

## 1 Befunde

### Kritisch

| Nr | Befund | Beleg |
|---|---|---|
| K1 | **Die Shelly Cloud bietet keine TOTP-2FA (Authenticator-App), soweit belegbar. Aussage: Nein.** Es gibt keine offizielle Dokumentation und keine Ankündigung dazu. Im Shelly-Community-Forum steht seit Mai 2025 der offene Feature-Request „Request for 2FA support to secure account access“. Die Antworten (auch von „QA members“) nennen nur Workarounds, keinen Termin. Ein älterer Forum-Thread „2 Faktor Authentifizierung für Cloud Konto“ ist ebenfalls ein Wunsch. Die App-Anmeldung besteht aus E-Mail und Passwort. Die App-Funktionen „Lock PIN“ (Sperre der App) und „Restrict Login“ (lokales Web-UI) sind **kein** zweiter Faktor für das Cloud-Konto. Die Anforderung R6 ist damit mit der Shelly Cloud allein **nicht erfüllbar**. | [Q1], [Q2], [Q3], [Q4], [Q5] |
| K2 | **Folge von K1:** Wer das Cloud-Konto übernimmt, kann die Klappe nachts öffnen, denn Cloud-Steuerung ist Fernsteuerung. Das gilt etwa nach einem Phishing-Angriff, nach Passwort-Wiederverwendung oder nach Übernahme des E-Mail-Kontos, über das die Passwort-Rücksetzung läuft. Ein Raubtier hätte dann Zugang. Zusätzlich gibt es den Cloud-„Authorization cloud key“ (auth_key) für die Cloud-API. Er ändert sich erst mit dem Kontopasswort. | [Q5] (auth_key); Bewertung [A] |
| K3 | **Ein Stromausfall kann die Position verlieren.** Laut API-Doku kann die Cover-Komponente nach einem Stromausfall die aktuelle Position verlieren. Die Wiederherstellung nach einem Absturz wurde mit FW 1.1.0 verbessert, ist aber nicht in allen Fällen garantiert. `Cover.GoToPosition` wird ohne Kalibrierung abgelehnt. `initial_state` legt das Verhalten beim Einschalten fest (open, closed oder stopped, Standard stopped). | [Q6], [Q7] |

### Mittel

| Nr | Befund | Beleg |
|---|---|---|
| M1 | **Bei Antrieb B1 (Schließen durch Schwerkraft) ist die Hinderniserkennung über Leistung für „Zu“ praktisch wirkungslos.** `obstruction_detection` (enable, direction, action stop/reverse, power_thr, holdoff) löst bei einem *Anstieg* der Leistung aus. Bei B1 wickelt der Motor in Richtung „Zu“ nur ab. Liegt der Schieber auf, wird der Gurt schlaff, die Leistung steigt nicht und der Motor läuft bis zur mechanischen Endlage weiter. Funktional ist das unkritisch, weil keine Quetschkraft entsteht. Ein „Zu“ wird aber ohne Reedkontakt **nicht erkannt**. Der Reedkontakt ist daher **Pflicht**, nicht nur Option. In Richtung „Auf“ (Heben) ist die Erkennung sinnvoll, etwa bei festgefrorenem Schieber. | [Q6]; Bewertung [A] |
| M2 | **Die Endlagenerkennung kommt nicht direkt aus der Leistung, sondern aus dem Stillstand.** Der Shelly erkennt das Ende der Fahrt, wenn die Leistung unter `motor.idle_power_thr` fällt (0–50 W, Standard 2 W), bestätigt über `idle_confirm_period`. Das passt zu einem Rohrmotor mit mechanischen Endschaltern. Die Kalibrierung misst die Fahrzeiten und setzt `power_thr` auf Spitzenleistung + 15 %. Bei hohem Restverbrauch des Motors scheitert die Kalibrierung. Dann `idle_power_thr` anheben. | [Q6], [Q8] |
| M3 | **Die Lux-Logik geht nur per Script.** Die nativen Zeitpläne (Schedule) können `@sunrise`/`@sunset` mit einem Offset von ±12 h und Cron-Feldern. Eine UND-Verknüpfung „Astro + Lux-Schwelle + Entprellung“ gibt es nativ nicht belegt. Hierfür ist ein Shelly-Script (mJS) nötig. Plus-Geräte unterstützen Scripte. | [Q9], [Q10], [Q11] |
| M4 | **Virtuelle Komponenten gibt es auf der Plus-Gen2 nicht.** Damit sind Schwellwerte in der App nicht einstellbar. Laut API-Doku sind Virtual Components „nur für Gen3 und Gen2 Pro“ verfügbar. Beim Plus 2PM (Gen2) stehen Parameter dann als Konstanten im Script. Ein 2PM Gen3/Gen4 wäre komfortabler, die Add-on-Kompatibilität ist je Modell zu prüfen. | [Q12], [Q13] |
| M5 | **Bei Zeitverlust gibt es keinen Astro-Betrieb.** Zeitpläne brauchen den konfigurierten Standort (lat/lon) und die Ortszeit. Dass der Plus 2PM keine gepufferte Echtzeituhr hat, ist **[A]**. Nach einem Stromausfall ohne Internet/NTP ist die Uhrzeit dann unbekannt und die Zeitpläne greifen nicht. Das Script muss eine gültige Zeit prüfen und gegebenenfalls nur lichtgeführt schließen. | [Q9]; [A] |
| M6 | **Störmeldungen per Push hängen von der Cloud ab.** Smart-Control-Szenen können Gerätezustände als Auslöser oder Bedingung nutzen (Bedingungen UND/ODER, „Once“/„On any change“). Als Aktionen stehen Telefon-Push, E-Mail, Ereignisprotokoll und Alexa-Benachrichtigung zur Verfügung. Ist die Cloud deaktiviert (siehe Empfehlung E1, Variante V2), entfällt dieser Weg. Eine Offline-Meldung des Geräts per Push/E-Mail ist laut KB eine Premium-Funktion. | [Q14], [Q15] |

### Gering

| Nr | Befund | Beleg |
|---|---|---|
| G1 | **Das lokale Passwort ist vorhanden, schützt aber nicht alles.** Digest-Auth mit SHA-256 (RFC 7616) ist verfügbar, für einen Benutzer `admin`. Ungeschützt bleiben MQTT, UART, ausgehende WebSockets, `Shelly.GetDeviceInfo` und `/shelly`. Laut Changelog FW 2.2.1 (13.11.2026) konnte ein unter 2.2.0 gesetztes Passwort ungültig werden. Abhilfe ist `Shelly.SetAuth` erneut. | [Q16], [Q17] |
| G2 | **Der Access Point ist ab Werk offen.** Er wird nach dem Bezug einer IP automatisch deaktiviert (wenn kein Passwort gesetzt ist), ebenso BLE-RPC. Ein Reset per Taste (5 s) aktiviert den AP für 15 min. Das bedeutet ein geringes Risiko bei physischem Zugang zum Schaltkasten. | [Q18], [Q19] |
| G3 | **Automatische Firmware-Updates verändern das Verhalten ungeprüft.** Auto-Update legt einen Zeitplan an und installiert die neueste Stable-Version. Bei Plus 2PM im Cover-Betrieb berichten Nutzer von ungewollten Wechseln von Beta zu Stable. Cover-Fixes kommen regelmäßig, z. B. 1.4.0 mit der Meldung „position lost“ bei geschlossener Klappe. | [Q20], [Q21] |
| G4 | **Die Sicherheitsfunktion „Safety-Switch“ ist mit Vor-Ort-Tastern Auf/Ab nicht kombinierbar.** Ein Hardware-Sicherheitseingang am 2PM geht nur mit `in_mode=single`. Dann bedient nur ein Taster Auf/Stopp/Ab. Bei zwei Tastern bleibt die Reed-Auswertung auf dem Add-on und im Script. Im Modus `detached` werden Eingänge ignoriert. | [Q22] |
| G5 | **Ein BLU-Lux-Sensor ist als Alternative zum 0–10-V-Messumformer möglich.** Der Shelly BLU Door/Window sendet Beleuchtungsstärke (BTHome 0x05, lx). Die ZB-Variante liefert nur Stufen 0/1/2 (ca. 50/500 lx). BTHomeSensor-Werte sind im Script über den Status-Handler auswertbar. Nutzer berichten von schwankenden Werten. Hinzu kommen Batteriebetrieb und Funkreichweite im Freien **[A]**. | [Q23], [Q24], [Q25] |

---

## 2 Empfehlungen

### E1 Fernzugriff ohne TOTP der Shelly Cloud – Alternativen

| Variante | Beschreibung | Sicherheit | Aufwand/Komfort | Bewertung |
|---|---|---|---|---|
| **V1 Cloud + Härtung** | Cloud bleibt aktiv. Langes, einmaliges Passwort aus dem Passwortmanager. Das **E-Mail-Konto des Shelly-Kontos mit TOTP absichern**: Das ist der eigentliche Rücksetz-Weg, und hier ist ein Authenticator möglich. Lock PIN in der App, Smartphone mit Biometrie und Bildschirmsperre. Keine Weitergabe des auth_key. Zusätzlich die Script-„Nachtsperre“ (siehe 3.4). | Mittel. Ein einzelner Faktor auf Shelly-Seite bleibt. | Gering, voller App-Komfort inkl. Push | **Mindestmaß**, falls die Cloud gewünscht ist |
| **V2 Router-VPN, Cloud aus** | FritzBox ab FRITZ!OS 7.50: WireGuard „Einzelgerät verbinden“, QR-Code in die WireGuard-App, Zugriff über die IP des Shelly auf das lokale Web-UI (Digest-Auth). Cloud im Shelly deaktivieren, dann ist die Klappe von außen nur noch über VPN erreichbar. Voraussetzungen: öffentliche IPv4- oder IPv6-Adresse, kein Standard-IP-Netz (192.168.178.0 o. ä. ändern), 6490/6590 Cable ohne WireGuard. | Hoch. Schlüssel auf dem Gerät + Smartphone-Sperre (Besitz + Wissen/Biometrie). Keine Cloud-Angriffsfläche. | Mittel. Push aus der Cloud entfällt (Ersatz siehe E4). Bedienung über Web-UI oder lokale App | **Empfohlen**, wenn „Authenticator-Niveau“ gefordert ist |
| V3 Hybrid | Wie V2, Cloud aber für Push/Status aktiv. Fernsteuern per Script-Nachtsperre stark eingeschränkt. | Mittel–hoch, abhängig von der Wirksamkeit der Sperre **[A]** | Mittel | Möglich, die Sperre muss getestet werden |
| – | Portfreigabe auf das Web-UI | Niedrig (HTTP, keine 2FA, offene Endpunkte s. G1) | – | **Nicht zulässig** (Konzept korrekt) |

Belege für V2: [Q26]. Belege für Cloud aus: [Q18] („If you disable the device cloud support, you will lose connection … from outside its local network“).

### E2 Cover-Parametrierung (Antrieb B1)
- Endlagen am Rohrmotor mechanisch einstellen, danach kalibrieren (Weg frei halten). Bei Abbruch `idle_power_thr` erhöhen bzw. `holdoff` < Fahrzeit wählen [Q6], [Q8].
- `maxtime_open`/`maxtime_close` auf gemessene Fahrzeit × 1,3 setzen **[A]**, statt Standard 60 s.
- `obstruction_detection`: enable, `direction=open`, `action=stop`. `power_thr` aus der Kalibrierung, Plausibilität prüfen.
- `initial_state=stopped`, also keine Bewegung nach Netzwiederkehr. Den Sollzustand stellt das Script her (siehe 3.3).
- Taster: `in_mode=dual` (Auf/Ab), oder `single` + Safety-Eingang, falls ein Hardware-Endschalter am 2PM gewünscht ist [Q22].

### E3 Zeitlogik
Native Grundfunktion ohne Script, als Rückfallebene: zwei Zeitpläne „Schließen“ (`@sunset+X` und feste Uhrzeit Y) sowie zwei „Öffnen“ (`@sunrise+X` und feste Uhrzeit Z). Schließen ist idempotent, daher gilt praktisch „frühestens das erste Ereignis“ [Q9]. Für Lux mit Hysterese und Priorität das Script nach Abschnitt 3 verwenden, die nativen Zeitpläne „spätestens Y“ als Fallback behalten.

### E4 Störmeldung „Klappe nicht ZU“
- **Mit Cloud:** Szene mit Auslöser „Add-on-Eingang Reed = offen“ UND Bedingung Uhrzeit/Zeitfenster Nacht, Aktion Telefon-Push [Q14]. Ob die Uhrzeit als Szenenbedingung verfügbar ist, ist **[A]** zu prüfen. Besser ist ein virtueller Status aus dem Script. Auf Plus Gen2 nicht verfügbar (M4), daher Script → Szene über Eingangszustand oder direkt per HTTP.
- **Ohne Cloud:** Das Script sendet `HTTP.GET` an einen Push-Dienst [Q27]. Das wäre ein Fremddienst (z. B. ntfy, Pushover) **[A]** und steht damit im Konflikt mit R4 „nur Shelly“. Die Entscheidung trifft der Bauherr.

### E5 Lokale Härtung (Checkliste)
1. Web-UI-Authentifizierung aktivieren, Passwort ≥ 16 Zeichen [Q16], [Q18].
2. AP: deaktiviert bzw. Passwort setzen. BLE-RPC aus (`BLE.SetConfig rpc.enable=false`, ab FW 2.0.0) [Q19]. Hinweis: Einen BLU-Lux-Sensor betrifft das nicht, BLE-Scan läuft automatisch.
3. Eigenes IoT-WLAN/Gastnetz bzw. VLAN für die Shelly-Geräte. Kein Zugriff aus dem IoT-Netz ins Heimnetz, der Admin-Client darf ins IoT-Netz **[A]** (Router-Funktion).
4. Ungenutztes deaktivieren: MQTT, ausgehende WebSockets, Cloud bei V2. MQTT ist nicht durch Digest geschützt [Q16].
5. Firmware: Auto-Update **aus**, Updates manuell nach Changelog-Prüfung, nach dem Update Funktionstest (Kalibrierung, Script läuft, Reed) [Q20], [Q21]. Nach dem Update auf ≥ 2.2.1 das Passwort neu setzen, falls es unter 2.2.0 gesetzt wurde [Q17].
6. Configuration Backup und Script-Quelltext dokumentieren (Projektablage).

### E6 Sensorik
- Add-on am Plus 2PM ist kompatibel und galvanisch getrennt. Digitaleingang: Reed (logisch invertierbar). Analogeingang 0–10 V (Genauigkeit besser ±5 %) [Q28], [Q10].
- **Den Lux-Messumformer 0–10 V bevorzugen** (verkabelt, ohne Batterie). Kennlinie z. B. 0–10 V = 0–1000 lx **[A]**. Der Bereich muss die Schwellen 5–100 lx gut auflösen. Hersteller mit kleinem Messbereich wählen (z. B. 0–200 lx) **[A]**.
- Reed als **Öffner-Schaltung bezüglich „ZU“** **[A]**: Kontakt geschlossen bei Klappe zu. Ein Drahtbruch wird dann als „nicht ZU“ gemeldet, also fehlersicher.

---

## 3 Steuerungslogik

### 3.1 Prioritäten (höchste zuerst)
1. **Sicherheitsabschaltungen im Shelly** (Hindernis, Überlast, maxtime). Nicht übersteuerbar.
2. **Vor-Ort-Taster.** Direkt über die Cover-Eingänge. Das Script akzeptiert das Ergebnis bis zum nächsten Automatik-Ereignis.
3. **Manueller Fernbefehl** (App/Web-UI). Wirkt bis zum nächsten Automatik-Ereignis. Optional Nachtsperre (3.4).
4. **Automatik** Astro + Lux mit Zeitgrenzen.
5. **Fallback** Zeitpläne (native Schedules) bei Lux-Fehler.

### 3.2 Bedingungen (Parameter **[A]**, vor Ort einzustellen)

| Parameter | Vorschlag |
|---|---|
| `OPEN_EARLIEST` | 07:00 (Schutz vor Raubwild in der Dämmerung, mit Tierhaltung abstimmen) |
| `OPEN_ASTRO` | Sonnenaufgang + 30 min |
| `OPEN_LATEST` | 09:00 |
| `CLOSE_ASTRO` | Sonnenuntergang + 15 min |
| `CLOSE_LATEST` | 22:00 |
| `LUX_OPEN` / `LUX_CLOSE` | 30 lx / 8 lx (Hysterese) |
| `T_DEBOUNCE` | 10 min Schwelle ununterbrochen über- bzw. unterschritten |
| `T_CHECK` | maxtime_close + 10 s |

- **Öffnen:** `(t ≥ max(OPEN_EARLIEST, OPEN_ASTRO) UND Lux > LUX_OPEN seit T_DEBOUNCE) ODER t ≥ OPEN_LATEST`
- **Schließen:** `(t ≥ CLOSE_ASTRO UND Lux < LUX_CLOSE seit T_DEBOUNCE) ODER t ≥ CLOSE_LATEST`
- Jedes Ereignis **einmal pro Tag** (Merker, Reset um 12:00 bzw. 00:00), damit ein manuelles Öffnen am Abend nicht sofort übersteuert wird. Ausnahme: Nachtsperre.

### 3.3 Pseudocode (mJS-Skizze, nicht lauffähig getestet)

```javascript
// Konstanten (Plus Gen2: keine virtuellen Komponenten -> im Script)
let P = { luxOpen:30, luxClose:8, debounceMin:10,
          openEarliest:"07:00", openLatest:"09:00", closeLatest:"22:00",
          offRise:30, offSet:15, tCheckS:60 };
let S = { openedToday:false, closedToday:false, luxHi:0, luxLo:0, alarm:false };

function timeValid()   { /* Sys-Status: unixtime != null */ }
function lux()         { /* Add-on Analog/Voltmeter V -> lx (Kennlinie); NaN bei Fehler */ }
function reedZu()      { /* Add-on Digitaleingang, true = ZU */ }
function sunTimes()    { /* Sonnenauf-/-untergang: [A] nicht als Script-API belegt ->
                            Alternative: native Schedules @sunrise+X/@sunset+X rufen
                            das Script bzw. setzen Merker "astroOpenOk"/"astroCloseOk" */ }

function tick() {                          // Timer.set(60000, true, tick)
  let l = lux();
  if (!isNaN(l)) {                         // Entprellung/Hysterese
    S.luxHi = (l > P.luxOpen)  ? S.luxHi + 1 : 0;
    S.luxLo = (l < P.luxClose) ? S.luxLo + 1 : 0;
  }
  let hell   = S.luxHi >= P.debounceMin;
  let dunkel = S.luxLo >= P.debounceMin;   // Lux-Fehler -> bleibt false -> nur Zeit-Fallback
  if (!timeValid()) {                      // nach Stromausfall ohne NTP
    if (S.luxLo >= P.debounceMin && !reedZu()) close("lux_notime");
    return;                                // niemals ohne gültige Zeit öffnen
  }
  if (!S.closedToday && ((astroCloseOk && dunkel) || now() >= P.closeLatest)) close("auto");
  if (!S.openedToday && ((astroOpenOk && now() >= P.openEarliest && hell)
                         || now() >= P.openLatest))                      open("auto");
  if (nacht() && !reedZu()) alarm("Klappe nicht ZU");   // zyklisch, Push 1x je Ereignis
}

function close(src) {
  Shelly.call("Cover.Close", {id:0});
  S.closedToday = true;
  Timer.set(P.tCheckS*1000, false, function () {
    if (!reedZu()) {                       // 1 Wiederholung (Eis/Schmutz)
      Shelly.call("Cover.Open",  {id:0, duration:2});
      Timer.set(4000, false, function(){ Shelly.call("Cover.Close",{id:0}); });
      Timer.set((P.tCheckS+6)*1000, false, function(){ if(!reedZu()) alarm("Schliessen fehlgeschlagen"); });
    }
  });
}
// Boot: initial_state=stopped; Script startet automatisch; erster tick stellt Sollzustand her
// (Nacht + gültige Zeit -> close). Reset der Tagesmerker 12:00/00:00.
```

Hinweise:
- Die Script-Aufrufe `Shelly.call`, `Timer.set` (max. 5 Timer je Script) und `HTTP.GET` sind belegt [Q27]. Die Auswertung von BTHomeSensor bzw. Status-Handlern ebenfalls [Q24].
- Ob Sonnenauf- und Sonnenuntergang im Script direkt abrufbar sind, ist **nicht belegt**. Robuste Lösung: native Schedules mit `@sunset+15m` bzw. `@sunrise+30m` setzen per `Script.Eval` oder KVS einen Merker **[A]**. Alternativ zeitgleich `Cover.Close` direkt und das Script entscheidet nur über Lux. Vor der Umsetzung klären.
- Bei Lux-Fehler (NaN, Messwert außerhalb 0–10 V) bleiben `hell`/`dunkel` false. Dann gelten nur `CLOSE_LATEST`/`OPEN_LATEST`, also die Zeit-Fallbacks.

### 3.4 Nachtsperre (optional, gegen Missbrauch über Cloud)
Zwischen dem Schließereignis und `OPEN_EARLIEST`: Meldet die Cover-Komponente die Bewegung „opening“ und ist kein Vor-Ort-Taster der Auslöser, folgt sofort `Cover.Close` und eine Push-Meldung „Öffnungsversuch nachts“. Ob die Status-/Event-Daten die Quelle (Taster/Cloud/HTTP) eindeutig liefern, ist **[A]** und per Test zu prüfen. Ohne Quelleninformation gilt: Sperre ganz, Ausnahme nur über den Vor-Ort-Taster (Eingangs-Event im Script erkennbar [Q11]).

### 3.5 Stromausfall
- `initial_state=stopped` [Q6]. Das Script stellt beim Start den Zustand nach Uhrzeit bzw. Lux her (Schließen ist immer erlaubt, Öffnen nur mit gültiger Zeit).
- Position verloren (K3): `Cover.Close` und `Cover.Open` laufen bis zur Endlage bzw. maxtime **[A]**. Eine Positionsanfahrt ist nicht nötig. Nach Bedarf neu kalibrieren.

---

## 4 Offene Punkte für den Bauherrn
1. Entscheidung V1/V2/V3 (E1). Bei der Forderung „Authenticator“ wird **V2** empfohlen.
2. Push ohne Cloud ist ein Fremddienst und widerspricht R4. Zulässig?
3. Hardware-Generation: Plus 2PM (Gen2) oder 2PM Gen3/Gen4 (virtuelle Komponenten, Add-on-Kompatibilität prüfen).
4. Zeitwerte/Lux-Schwellen mit der Tierhaltung abstimmen (Laufenten gehen nicht zuverlässig allein in den Stall **[A]**).

---

## 5 Quellen
Alle Quellen wurden über die Websuche am 23.11.2026 ermittelt. Direktabruf nicht möglich (siehe Methode).

- [Q1] Shelly Community: „Request for 2FA support to secure account access“ (Mai 2025, offen): https://community.shelly.cloud/topic/9986-request-for-2fa-support-to-secure-account-access/ (S. 2/3: …/page/2/, …/page/3/)
- [Q2] Shelly Forum: „2 Faktor Authentifizierung für Cloud Konto“: https://shelly-forum.com/thread/19402-2-faktor-authentifizierung-fuer-cloud-konto/
- [Q3] Shelly USA: Account Registration / Smart Control Guide: https://us.shelly.com/blogs/documentation/account-registration, https://kb.shelly.cloud/knowledge-base/shelly-smart-control-guide
- [Q4] Shelly Support: Lock PIN vs. Restricted Login: https://support.shelly.cloud/en/support/solutions/articles/103000221551-differences-between-lock-pin-and-authentication
- [Q5] Shelly Cloud API access (auth_key ändert sich mit Passwort): https://shellysa.co.za/wp-content/uploads/2020/10/Shelly-1-Cloud-API-Access.pdf (Händler-PDF, sekundär)
- [Q6] Shelly API Gen2 – Cover: https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Cover/
- [Q7] Shelly API Gen2 – Changelog (1.1.0, 1.4.0, 2.2.1): https://shelly-api-docs.shelly.cloud/gen2/changelog/
- [Q8] Shelly KB – Cover Mode / Plus 2PM Smart Control Cover Mode: https://kb.shelly.cloud/knowledge-base/cover-mode, https://kb.shelly.cloud/knowledge-base/shelly-plus-2-pm-device-smart-control-cover-mode
- [Q9] Shelly API Gen2 – Schedule (@sunrise/@sunset, Offset ±12 h, Standort nötig): https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Schedule/
- [Q10] Shelly KB – Plus 2PM Web Interface Guide: https://kb.shelly.cloud/knowledge-base/shelly-plus-2pm-web-interface-guide
- [Q11] Shelly API Gen2 – Script Tutorial / Input: https://shelly-api-docs.shelly.cloud/gen2/Scripts/Tutorial/, https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Input/
- [Q12] Shelly API Gen2 – Virtual Components (Script-API, „Gen3 und Gen2 Pro“): https://shelly-api-docs.shelly.cloud/gen2/Scripts/APIs/Virtual/
- [Q13] Shelly API Gen2 – Dynamic Components Virtual: https://shelly-api-docs.shelly.cloud/gen2/DynamicComponents/Virtual/
- [Q14] Shelly Support – Condition types in Scenes; Alexa Notify (Szenen-Aktionen): https://support.shelly.cloud/en/support/solutions/articles/103000206275-what-does-condition-types-mean-in-scenes-, https://support.shelly.cloud/en/support/solutions/articles/103000294080-alexa-notify-in-shelly-smart-control-app-scenes-
- [Q15] Shelly KB – Shelly 1 Gen4 Device Smart Control (Offline-Notifications Premium): https://kb.shelly.cloud/knowledge-base/shelly-1-gen4-device-smart-control
- [Q16] Shelly API Gen2 – Authentication: https://shelly-api-docs.shelly.cloud/gen2/General/Authentication/
- [Q17] Shelly API Gen2 – Changelog 2.2.1: https://shelly-api-docs.shelly.cloud/gen2/changelog/
- [Q18] Shelly KB – Plus 2PM Web Interface Guide (Cloud, Authentication, AP): https://kb.shelly.cloud/knowledge-base/shelly-plus-2pm-web-interface-guide
- [Q19] Shelly API Gen2 – System / BLE: https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Sys/, https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/BLE/
- [Q20] Shelly Community – Firmware update setting: https://community.shelly.cloud/topic/14937-firmware-update-setting
- [Q21] Shelly Forum – Plus 2PM automatisches Downgrade Beta → Stable: https://shelly-forum.com/thread/21687-shelly-plus-2pm-automatisches-downgrade-von-beta-version-auf-stable/
- [Q22] Shelly API Gen2 – Cover (safety_switch nur in_mode=single, detached ignoriert Eingänge); KB Cover Mode
- [Q23] Shelly BLE API – BLU Door Window (BTHome 0x05 Illuminance): https://shelly-api-docs.shelly.cloud/docs-ble/Devices/BLU/dw/ ; ZB: https://shelly-api-docs.shelly.cloud/docs-ble/Devices/BLU_ZB/dw_ZB/
- [Q24] Shelly API Gen2 – BTHomeSensor: https://shelly-api-docs.shelly.cloud/gen2/DynamicComponents/BTHome/BTHomeSensor/
- [Q25] Shelly Produktseite BLU Door/Window (Nutzerbewertung Lux): https://www.shelly.com/products/shelly-blu-door-window-white
- [Q26] FRITZ!: WireGuard-VPN zur FRITZ!Box am Smartphone einrichten: https://fritz.com/service/vpn/wireguard-vpn-zur-fritzbox-am-smartphone-oder-tablet-einrichten/
- [Q27] Shelly API Gen2 – Script APIs Shelly Core / Timer: https://shelly-api-docs.shelly.cloud/gen2/Scripts/APIs/Shelly/, https://shelly-api-docs.shelly.cloud/gen2/Scripts/APIs/Timer/
- [Q28] Shelly KB – Plus Add-on (kompatibel Plus 2PM, galvanisch getrennt, 0–10 V, Digitaleingang invertierbar): https://kb.shelly.cloud/knowledge-base/shelly-plus-add-on
