# GymAmpel – Live Studio-Auslastungstracker

Wer kennt es nicht: Man möchte trainieren, aber das Fitnessstudio ist überfüllt und man muss an jedem Gerät warten? 

Mit **GymAmpel** siehst du die Auslastung deiner Studios in Echtzeit, kannst Standorte vergleichen und findest sofort die besten und ruhigsten Trainingszeiten.

---

## Schnellzugriff

* **[Live Web-App öffnen (GitHub Pages)](https://risas-git.github.io/gym-utilization-tracker/)**
* **[Natives Android Studio Projekt (Java)](android/)**

---

## Features

- **Live-Auslastungsampel**: Schneller Überblick über den aktuellen Füllstand (🟢 Gering, 🟡 Mittel, 🔴 Hoch, ⚪ Geschlossen).
- **Deutschlandweites Studio-Tracking**: Automatische Erfassung von über **200+ All Inclusive / AI Fitness Studios in ganz Deutschland**.
- **Interaktive Suche & Vergleich**: Suche nach Städten oder Studios (z. B. Bielefeld, Berlin, Köln, München, Frankfurt) und vergleiche sie direkt nebeneinander.
- **Verlaufs-Analytics & 24h-Profile**: Zeitreihendiagramme (15-Minuten-Intervalle) und stündliche Durchschnittsauslastungen zur optimalen Trainingsplanung.
- **15-Minuten automatisches Scraping**: Läuft vollautomatisch im 15-Minuten-Takt via GitHub Actions ([scrape.yml](.github/workflows/scrape.yml)) und hochpräzisem Webhook-Trigger (z. B. via [cron-job.org](https://cron-job.org)). Parallele Abfragen aller 200+ Studios in ~10 Sekunden.
- **Supabase Cloud-Datenbank**: Sichere und performante Speicherung aller Auslastungsdaten in einer PostgreSQL-Cloud-Datenbank (REST API).
- **Native Android App (Java)**: Bereit zum Öffnen in Android Studio und Testen auf dem Smartphone per USB.

---

## ⚙️ Architektur & Daten-Pipeline

```
[ All Inclusive / AI Fitness API ]
               │
               ▼ (alle 15 Min)
    [ GitHub Actions Scraper ] ◄── [ Cron-Job.org Webhook Trigger ]
          (tracker.py)
               │
               ▼
   [ Supabase PostgreSQL DB ]
          (Cloud REST API)
          ╱              ╲
         ▼                ▼
[ Web-App (GitHub Pages) ]  [ Native Android App (Java) ]
```

1. **Automatischer Trigger**: Ein externer Webhook-Cronjob triggert alle 15 Minuten per GitHub Actions `workflow_dispatch` API den Scraper.
2. **Datenabruf**: `tracker.py` holt per Multithreading (`ThreadPoolExecutor`) in Sekunden die aktuellen Auslastungsdaten für alle 200+ Studios in Deutschland ab.
3. **Persistierung**: Die Datensätze werden gebatcht in Supabase gespeichert.
4. **Visualisierung & Auswertung**: Sowohl die GitHub Pages Web-App als auch die native Android App rufen die Live- und Historiendaten direkt via Supabase REST API ab.

## 📱 Android App starten

Die Android-Version liegt im Unterordner [`android/`](android/):
1. **Android Studio** öffnen.
2. Den Ordner `android/` auswählen.
3. Auf den grünen **Run-Button** (▶️) klicken.