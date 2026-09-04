# 02 Scaffold

> Fixed conventions (tech stack / directory / routes / global state) live in `references/00_project_conventions.md`.

## Dependencies

```bash
npm create vite@latest . -- --template react
npm i react-router-dom
npm i @capacitor/core @capacitor/cli @capacitor/android
```

## Copy the templates

Copy the skeletons from `templates/` into `src/` (drop the `.skeleton` suffix):

| Template | Target |
|----------|--------|
| `main.jsx.skeleton` | `src/main.jsx` |
| `App.jsx.skeleton` | `src/App.jsx` |
| `index.css.skeleton` | `src/index.css` |
| `screens.css.skeleton` | `src/screens.css` |
| `Screen.jsx.skeleton` | `src/screens/*.jsx` (one copy per page) |
| `StatusBar.jsx.skeleton` | `src/components/StatusBar.jsx` |
| `BottomNav.jsx.skeleton` | `src/components/BottomNav.jsx` |
| `VoiceFab.jsx.skeleton` | `src/components/VoiceFab.jsx` |

- `App.jsx.skeleton` imports `./screens/Splash` and `./screens/Home`; copy those two pages out of `Screen.jsx.skeleton` first (or change them to your routes).
- Vite's demo leftovers (`src/App.css`, `src/assets/react.svg`, etc.) can be deleted — they don't matter.
- `capacitor.config.json` is used at the packaging stage (07).

## Self-check

`npm run dev` shows a **white phone frame** (`.phone` 390×844 + status bar / bottom tab / floating-ball placeholders, no real content yet), then move to stage 3.
