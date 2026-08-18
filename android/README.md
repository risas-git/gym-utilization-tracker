# Gym Utilization Tracker - Android App (Java)

This is the native Android Studio project for the Gym Utilization Tracker, built with Java and modern AndroidX components.

---

## 🚀 Getting Started with Android Studio

### 1. Open the Project in Android Studio
1. Launch **Android Studio**.
2. Click **Open** (or `File > Open`).
3. Select the `android/` directory inside this project:
   `c:\Users\risas\Uni\project\gym-utilization-tracker\android`
4. Android Studio will automatically recognize Gradle and sync all dependencies.

---

### 2. Running on an Emulator or Physical Device
* **On Emulator**: Click the green **▶ Run** button at the top toolbar. If you don't have a virtual device, create one via **Device Manager** (e.g. Pixel 8, Android 14).
* **On Real Phone**:
  1. Enable **Developer Options** and **USB Debugging** on your phone.
  2. Connect your phone to your PC via USB.
  3. Select your device from the dropdown and click **▶ Run**.

---

### 3. How to Share with Friends (Export APK)
To share an installable `.apk` directly with friends:
1. In Android Studio, go to the top menu: **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
2. Once complete, click **locate** in the bottom-right popup.
3. Send the `.apk` file (`app-debug.apk`) to your friends (via Telegram, WhatsApp, Google Drive, etc.).
4. Your friends can open and install it directly on any Android device!

---

### 4. How to Publish on the Google Play Store
When you are ready for Google Play:
1. Go to **Build > Generate Signed Bundle / APK...**
2. Choose **Android App Bundle (.aab)**.
3. Create or select your **Release Keystore** (save your key password!).
4. Choose **release** build variant and click **Finish**.
5. Upload the resulting `.aab` to your [Google Play Console](https://play.google.com/console).

---

### 5. Syncing Web Updates
If you make changes to the main web app at root `../index.html`, copy it into the Android assets folder:
```powershell
Copy-Item ..\index.html .\app\src\main\assets\index.html -Force
```
Then rebuild or re-run the app.
