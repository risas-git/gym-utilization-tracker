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
- **15-Minuten automatisches Scraping**: Läuft vollautomatisch via GitHub Actions ([scrape.yml](.github/workflows/scrape.yml)) mit parallelen Abfragen in ~5 Sekunden.
- **Supabase Cloud-Datenbank**: Sichere und performante Speicherung aller Auslastungsdaten in einer PostgreSQL-Cloud-Datenbank.
- **Native Android App (Java)**: Bereit zum Öffnen in Android Studio und Testen auf dem Smartphone per USB.

---

## Android App starten

Die Android-Version liegt im Unterordner [`android/`](android/):
1. **Android Studio** öffnen.
2. Den Ordner `android/` auswählen.
3. Auf den grünen **Run-Button** klicken.

Ausführliche Details findest du in der [Android Dokumentation](android/README.md).