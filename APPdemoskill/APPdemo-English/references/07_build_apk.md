# 07 Package (Android APK / iOS app)

> Confirm the platform (iOS / Android) first — see `SKILL.md`'s hard constraint "ask about the platform after the layout is done". Fixed values like appName and the 66% icon safe zone live in `references/00_project_conventions.md` §2.

## Platform branch

- **Android**: follow "Wire up Capacitor → build APK" below.
- **iOS**: `npx cap add ios` generates the Xcode project, needs **macOS + Xcode** (see "iOS build" at the end); on Windows you can only do Android.

## Environment (one-time)

- JDK 21 (Temurin), `JAVA_HOME` pointing to it.
- Android SDK: `cmdline-tools` + `platforms;android-36` + `build-tools;36.0.0`.
- `ANDROID_HOME` pointing to the SDK.

## Wire up Capacitor

```bash
npm i @capacitor/core @capacitor/cli @capacitor/android
npx cap init "YourApp" com.example.app --web-dir dist
npm run build
npx cap add android   # for iOS, use npx cap add ios instead
```

- `capacitor.config.json`: appId / appName / webDir (`keyboard.resize` can stay; Android ignores it).
- `app_name` in `strings.xml` = the name shown on the home screen.

## Icons (adaptive)

- **Foreground** `ic_launcher_foreground.png`: logo scaled to the **66% safe zone**, centered on a **transparent** canvas.
- **Legacy** `ic_launcher.png` / `ic_launcher_round.png`: logo 66% centered on a **brand-color background** (ask the user; if not given use placeholder white `#FFFFFF`).
- `values/ic_launcher_background.xml`: `<color name="ic_launcher_background">#FFFFFF</color>` (swap to the brand color).

Script:

```bash
python scripts/gen_adaptive_icons.py <logo.png> <res dir> --bg #FFFFFF --safe 0.66  # --bg to the brand color
```

## Build (⚠️ PowerShell env vars don't persist, inline them)

```powershell
$env:JAVA_HOME='<JDK 21 path>'   # TODO: your path
$env:ANDROID_HOME='<Android SDK path>'   # TODO: your path
$env:ANDROID_SDK_ROOT=$env:ANDROID_HOME
cd android; .\gradlew.bat assembleDebug
```

Output: `android/app/build/outputs/apk/debug/app-debug.apk`.

One-shot script: `scripts/build_apk.ps1`.

## Install to phone + verify

Install (either):
- Copy the `.apk` to the phone → open it in a file manager to install (allow "unknown sources").
- USB connect → `adb install app-debug.apk`.

Verification checklist (matching 06's changes):
1. Home-screen icon has the brand-color background, centered logo, rounded corners without black edges.
2. Tapping anywhere doesn't flash blue.
3. No mock 9:41 status bar at the top (keep the system status bar).
4. UI width fills exactly without distortion; keyboard doesn't slide up or compress the UI.

## iOS build (needs macOS + Xcode)

```bash
npx cap add ios
cd ios && pod install        # only if you added plugins
open App.xcworkspace          # open in Xcode
```
In Xcode pick device/simulator → Run (real device needs signing). Output `.app`; for distribution go Archive → IPA. On iOS `keyboard.resize` takes effect; the native status bar means no mock to remove — adaptation details same as 06.

## Delivery

Copy to the target directory. **Debug-signed** is demo-only; distribution needs formal signing. Success = build succeeds (Android `BUILD SUCCESSFUL` / iOS Xcode compiles) + installs on a real device.
