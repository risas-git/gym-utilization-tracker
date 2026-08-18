# 🚦 GymAmpel – Android App (Java)

Dies ist das native Android Studio Projekt für **GymAmpel**, entwickelt in Java mit modernen AndroidX-Komponenten und WebView.

---

## 🚀 Erste Schritte mit Android Studio

### 1. Projekt in Android Studio öffnen
1. Starte **Android Studio**.
2. Klicke auf **Open** (oder `Datei > Öffnen`).
3. Wähle den Unterordner `android/` in diesem Projekt aus:
   ```text
   c:\Users\risas\Uni\project\gym-utilization-tracker\android
   ```
4. Android Studio erkennt Gradle automatisch und synchronisiert alle Abhängigkeiten.

---

### 2. Auf dem Emulator oder Smartphone testen
* **Auf dem Emulator**: Klicke oben in der Menüleiste auf den grünen **▶ Play / Run-Button**. Falls kein Gerät vorhanden ist, erstelle eines über den **Device Manager** (z. B. Pixel 8, Android 14).
* **Auf dem echten Smartphone**:
  1. Aktiviere die **Entwickleroptionen** und **USB-Debugging** auf deinem Handy.
  2. Verbinde dein Handy per USB-Kabel mit dem PC.
  3. Bestätige auf dem Handy die Abfrage *„USB-Debugging zulassen?“*.
  4. Wähle dein Handy im Dropdown-Menü in Android Studio aus und klicke auf **▶ Run**.

---

### 3. App an Freunde weitergeben (APK exportieren)
Um eine installierbare `.apk`-Datei direkt an Freunde zu senden (z. B. via WhatsApp, Telegram oder Google Drive):
1. Gehe im Menü auf: **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
2. Nach Abschluss unten rechts auf **locate** klicken.
3. Die erzeugte Datei (`app-debug.apk`) kannst du direkt weiterleiten. Deine Freunde können sie mit einem Tippen auf jedem Android-Gerät installieren!

---

### 4. Im Google Play Store veröffentlichen
Wenn du bereit für den Play Store bist:
1. Gehe auf **Build > Generate Signed Bundle / APK...**
2. Wähle **Android App Bundle (.aab)**.
3. Erstelle oder wähle deinen **Release Keystore** (Schlüssel-Passwort gut merken!).
4. Wähle die Build-Variante **release** und klicke auf **Finish**.
5. Lade die erstellte `.aab`-Datei in deiner [Google Play Console](https://play.google.com/console) hoch.

---

### 5. Web-Updates synchronisieren
Wenn du Änderungen an der Datei `../index.html` vornimmst, kopiere sie einfach in den Android-Assets-Ordner:
```powershell
Copy-Item ..\index.html .\app\src\main\assets\index.html -Force
```
Danach die App in Android Studio neu starten oder bauen.
