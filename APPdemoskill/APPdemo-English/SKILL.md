---
name: design-to-app
description: Turn a high-fidelity design mockup (Figma / image, fixed pixels) into an installable, runnable mobile app — read the design → scaffold a React+Vite project → restore visuals & interactions → package with Capacitor into an Android APK / iOS app. Use when the user wants to "turn a design into an app", "design-to-code", "make a high-fidelity prototype", "package an APK to install on a phone for a demo", or "turn a UI mockup into something clickable and runnable".
---

# Design mockup → runnable app

Turn one or a set of high-fidelity design mockups into an app that can be installed and run on a phone.

Default tech stack: **React 19 + Vite + react-router-dom (HashRouter) + Capacitor 8**, producing an Android APK / iOS app (debug-signed, enough for coursework/demos; iOS builds require macOS + Xcode). All fixed conventions live in `references/00_project_conventions.md`.

## Overall flow (8 stages, in order)

| # | Stage | Which reference | Output |
|---|-------|-----------------|--------|
| 1 | Read design & extract assets | `references/01_read_design.md` | page list, colors/fonts, cutouts, base size |
| 2 | Scaffold | `references/02_scaffold.md` | an empty project that runs via `npm run dev` |
| 3 | Pages & routes | `references/03_screens_and_routes.md` | route table + component skeletons |
| 4 | Restore visuals | `references/04_visual_tokens.md` | static UI matching the mockup |
| 5 | Restore interactions | `references/05_interactions.md` | interactions you can click/drag/navigate |
| 6 | Mobile adaptation | `references/06_mobile_adaptation.md` | no distortion on phones, keyboard doesn't push up |
| 7 | Package | `references/07_build_apk.md` | an installable .apk / iOS app |
| 8 | Deliver & verify | references/07_build_apk.md (install & verify) | real-device install + screenshot confirmation |

## Hard constraints that run through the whole process (remember these first)

- **Change one thing → confirm one thing → continue**: don't batch a bunch of edits and report once; if unsure, ask — don't guess.
- **Use only the user's assets**: don't add rings / strokes / change colors / swap images on your own; only change what the user asked for, don't "optimize" other parts as a side effect.
- **Ask the user for assets; leave Apple HIG placeholders for what's missing**: use SF Symbols for icons, the system person glyph for avatars, a system gray block for images, and mark them `TODO` — don't grab web images or draw substitutes yourself.
- **Measure the base size first**: the mockup's fixed width/height (default iOS 390×844 / Android 360×800, replace with the measured mockup size) is the single base for all later scaling, icons, and layout.
- **Ask about the platform after the layout is done**: once the overall UI layout (visuals) is complete, ask the user whether it targets iOS or Android, determine the base size accordingly (§2) and emit the matching platform code structure (`cap add ios` / `cap add android`); don't default to Android.
- **Routes must use HashRouter**: in a WebView under `file://`, BrowserRouter white-screens with a 404.
- **Self-check at every stage**: after reading, you can retell the pages; visuals are visible in `npm run dev`; adaptation is verified in the real-device APK.
- **PowerShell env vars don't persist across commands**: inline `JAVA_HOME` / `ANDROID_HOME` every time gradle runs.

## Completion rules (what counts as done / what counts as failure)

**Only when the user says "okay / fine / that's it" is it done**; you can't declare victory just because the steps are finished.

### ✅ Correctly done (meets requirements)

1. All 8 stages' self-checks pass, and **every step was confirmed with the user first** (see "change one thing → confirm one thing").
2. **Visuals**: page-by-page against the mockup, pixel-identical — no distortion, misplacement, extra or missing elements.
3. **Adaptation**: the real-device APK ① width fills exactly without distortion ② the keyboard doesn't move the UI ③ no mock status bar at the top ④ taps don't flash blue.
4. **Assets**: all come from the user; missing ones are marked `TODO` as placeholders (Apple HIG), at the correct size/position, waiting for the user to supply.
5. **Interactions**: every interaction is walked through by hand on a real device — can click, drag, navigate, no white screen.
6. **Delivery**: APK installed on a real device, screenshot shown to the user for confirmation, copied to the target directory.

### ❌ Wrongly ended (doesn't meet requirements)

- Layout / colors / sizes don't match the mockup, or there's distortion/misalignment.
- The UI gets compressed or pushed up when the keyboard appears (correct behavior is the keyboard overlays).
- A mock 9:41 status bar still lingers at the top, or taps still flash blue.
- Using assets the user didn't provide: found your own images, drew your own, changed colors, added rings/strokes.
- Copied the "(LaoLao example) / (this example)" content from the docs verbatim instead of deriving it from your own mockup per the conventions.
- Changed extra things the user didn't ask for ("side optimization").
- Only "it compiles / BUILD SUCCESSFUL" without real-device verification, then claiming done.

### Verdict

**All 6 "correctly done" items satisfied + zero "wrongly ended" items** = done; if any item fails, keep fixing — don't wrap up.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/gen_adaptive_icons.py` | generate adaptive + legacy icons from logo.png |
| `scripts/strip_statusbar.py` | bulk-remove the StatusBar component from pages |
| `scripts/build_apk.ps1` | one-shot build → sync → assembleDebug → copy |
| `scripts/vision.cjs` | read images when the model has no native vision (calls qwen-vl-max) |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/App.jsx.skeleton` | App skeleton: routes + global state + scaling + BottomNav/VoiceFab |
| `templates/main.jsx.skeleton` | entry: imports index.css/screens.css + mounts App |
| `templates/index.css.skeleton` | global styles: tokens, `.phone` scaling, `.screen` base + reusable-component styles |
| `templates/screens.css.skeleton` | empty per-page stylesheet |
| `templates/Screen.jsx.skeleton` | new-page skeleton |
| `templates/StatusBar.jsx.skeleton` | mock status bar component |
| `templates/BottomNav.jsx.skeleton` | bottom Tab Bar component |
| `templates/VoiceFab.jsx.skeleton` | voice floating-button component |
| `templates/capacitor.config.json` | Capacitor config |

## Common defaults (known with no mockup)

Base size, brand color, icon, appName, and other fixed values live in `references/00_project_conventions.md` §2.

## Extra reference (the single source of truth)

- `references/00_project_conventions.md` — all fixed conventions for this project (tech stack / directory / routes / tokens / fonts / components / z-index / scaling / asset naming); change a convention only here.
