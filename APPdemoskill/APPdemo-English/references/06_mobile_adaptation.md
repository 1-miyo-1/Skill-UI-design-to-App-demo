# 06 Mobile adaptation

> Fixed conventions for scaling to fill the screen (`.phone` / `scale` / remove blue-flash / desktop separation) live in `references/00_project_conventions.md` §11.

## 1. Status bar: remove the "mock in the design", keep the "system status bar"

- Delete the `StatusBar` component from pages (the mock 9:41 time / signal icons).
- Also zero out the reserved top spacing (like `margin-top: 40px`); content sits flush to the top.
- Script: `scripts/strip_statusbar.py`.

## 2. Keyboard: Android must change the manifest

`keyboard.resize` in `capacitor.config.json` is **ignored on Android** (verified).

Correct approach: add to `<activity>` in `AndroidManifest.xml`:

```xml
android:windowSoftInputMode="adjustNothing"
```

Effect: the keyboard overlays the UI; the UI doesn't slide up or get compressed.

## Self-check

Install the APK on a real device: ① width fills exactly without distortion ② keyboard appears without moving the UI ③ no mock status bar at the top.
