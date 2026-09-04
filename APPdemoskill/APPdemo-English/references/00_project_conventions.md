# Project conventions (single source of truth)

This document is the **single authoritative convention** for "design mockup → app". All fixed facts in every stage's reference come from here; if you change a convention, change only this file — don't scatter edits across other files.

> The completion criteria (what counts as done / failure) live in `SKILL.md`'s "Completion rules".

## 1. Tech stack

React 19 + Vite + react-router-dom (**HashRouter**) + Capacitor 8, producing an Android APK (debug-signed, enough for coursework/demo).

## 2. Base size & defaults

**Ask for the spec first, then set the values**:
- Before starting, ask for and read the user's design spec (Design System / design-spec document).
- When the user has no design spec, default to **Apple Human Interface Guidelines (HIG)** and use the mockup's measured size as the truth.
- After reading the user's design spec, hand back the corresponding values for the user to confirm.

Actively ask for the following basics; use the user's values when given, fall back to defaults only when you can't get them:

- **Primary color**: button/icon background `#FFFFFF`, brand gradient `#FFFFFF → #000000`.
- **appName**: default "YourApp".
- **Icon logo**: occupies the **66% safe zone**.
- **Mockup fixed size**: default iOS/iPhone: **390px × 844px**; default Android: **360px × 800px** (the single base for all later scaling/icons/layout).
- **Bottom menu**: default 5 tabs (3–5 is fine; ask the user for tab labels/icons, see §9).

> Don't overwrite information the user already gave with defaults.

## 3. Directory structure

```
src/
  assets/        # cutouts (logo, avatars, icons…)
  components/    # cross-page reusable (BottomNav, StatusBar, VoiceFab…)
  screens/       # one file per page (Home.jsx, Chat.jsx…)
  App.jsx        # routes + global state + scaling logic
  index.css      # global: tokens, .phone scaling, adaptation
  screens.css    # per-page styles
public/
  fonts/         # embedded fonts (Vite must ignore, to avoid EBUSY)
```

## 4. Routes & component granularity

- **Routes must use HashRouter** (under WebView `file://`, BrowserRouter white-screens 404).
- Granularity: one file per page (screens/); cross-page reusable components (components/); in-flow overlays (like EmergencyCall) hang on the App layer and toggle via state.
- `main.jsx` only mounts + imports `index.css`.

## 5. Global state

State that "stays set once set in the session" (added a contact? / set an emergency contact? / has onboarding finished?) is **lifted to the App layer**; returning to a page doesn't reset it. The floating-ball position `fabPos` also lives at the App layer.

## 6. Design tokens (`:root` CSS variables)

**Neutral placeholders by default; ask the user for the brand color** (matching §2 "primary color"): if no brand color is given, use placeholder white `#FFFFFF`, gradient `#FFFFFF → #000000`, text `#000` / secondary text `#8E8E93`, background `#FFFFFF` / deep `#000000`; use neutral variable names (`--brand` / `--bg` / `--ink` / `--gray`). Once the user gives a brand color, replace with the brand values.

```css
:root {
  --brand: #FFFFFF;                                              /* primary: placeholder white, awaiting user's brand color */
  --brand-grad: linear-gradient(#FFFFFF, #000000);              /* gradient: placeholder */
  --bg: #FFFFFF;                                                 /* background */
  --bg-deep: #000000;                                            /* deep background */
  --ink: #000000;                                                /* primary text */
  --gray: #8E8E93;                                               /* secondary text */
}
```

Pin colors into variables, don't scatter hex; for multiple themes switch variables, don't hardcode.

## 7. Font embedding (⚠️ EBUSY pitfall)

```css
@font-face {
  font-family: "Alibaba PuHuiTi";
  src: url("/fonts/AlibabaPuHuiTi-Regular.otf") format("opentype");
  font-weight: 400;
  font-display: swap;
}
```

- Put font files in `public/fonts/`.
- **Vite must ignore `public/fonts`**, otherwise on Windows the file is locked and you get `EBUSY` (a pitfall we hit).

## 8. Images & assets

**Always ask the user for assets; leave Apple HIG placeholders for what's missing**:

1. Before starting, make an asset list (logo / avatars / backgrounds / icons / fonts), ask the user item by item, don't find images yourself, don't draw them.
2. For assets the user didn't provide, **keep placeholder slots**, mark `TODO`, wait for the user to fill them:

| What's missing | Apple HIG placeholder |
|----------------|----------------------|
| Icons | SF Symbols system icons, or equal-size gray rounded blocks |
| Avatars / people | system person glyph `person.crop.circle` (gray) |
| Images / backgrounds | system gray block `#E5E5EA` + hint text |
| Fonts | system font (PingFang / San Francisco) |

> Placeholders must be at the **correct size and position**; when the user supplies assets, "replace only, don't change the layout".

- Cutouts go in `src/assets/`, imported with `import` (Vite hashes + bundles them).
- Large images (backgrounds, videos) go in `public/` and are referenced directly.
- **Naming convention**: lowercase + hyphens; `nav-` / `bg-` / `icon-` prefixes show purpose; page-specific assets carry a page prefix (`nav-family-*`); stateful assets get `-idle` / `-active`.
- **Mapping table**: record a table from design name → code name, check sizes one by one (e.g. the family-tree page example), using the asset content the user actually provided:

| Code filename | Design source | Size |
|---------------|---------------|------|
| `family-tree-bg.png` | `tree.png` | 1796×3824 |
| `ginkgo-tree.png` | `ginkgo-tree.png` | 1796×2424 |
| `yeye.png` | `selected icon\grandpa.png` | 374×424 |
| `xiaoming.png` | `selected icon\xiaoming.png` | 375×392 |
| `xiaoli.png` | `selected icon\xiaoli.png` | 400×392 |
| `nav-family-bg.png` | `family-tree menu bar background.png` | 1860×338 |
| `nav-family-home.png` | `family-tree menu bar\home.png` | 118×188 |
| `nav-family-tools.png` | `family-tree menu bar\tools.png` | 117×196 |
| `nav-family-tree.png` | `family-tree menu bar\family tree.png` | 304×304 |
| `nav-family-msg.png` | `family-tree menu bar\messages.png` | 137×188 |
| `nav-family-profile.png` | `family-tree menu bar\me.png` | 108×188 |

- (LaoLao example) avatar-style assets **already come with a rounded white border** — don't draw another circle / add a stroke in code, paste the original image directly.
- The whole menu-bar icon set keeps the same size as other pages, only swaps assets and keeps the animation.

## 9. Reusable components

> The following are general conventions; entries marked "(LaoLao example)" are this project's specific implementation — swap them per Apple HIG (Tab Bar / SF Symbols / system components) when changing projects.
>
> Runnable skeletons for the three components live in `templates/`: `StatusBar.jsx.skeleton` / `BottomNav.jsx.skeleton` / `VoiceFab.jsx.skeleton` (copy → rename `Xxx.jsx` into `src/components/`); their CSS is at the end of `index.css.skeleton`.

### StatusBar
- `<StatusBar />` → black text (`#000`), for light backgrounds.
- `<StatusBar light />` → white text (`#fff`), for dark/image backgrounds.
- Signal/WiFi/battery icons drawn with `currentColor`, color follows the text.
- `z-index: 20`. **Delete it entirely before building the APK** (real devices have a system status bar, see 06).

### BottomNav (bottom navigation)
- General: bottom navigation defaults to Apple **Tab Bar** — ask the user how many tabs, each tab's icon and label; 3–5 is good, active tab highlighted.
- (LaoLao example) 5 tabs (home / tools / family tree / messages / me), colored icons + text.
- The floating white indicator `.bottom-nav__indicator` slides with `transition:left .35s`; the active item switches to a white highlighted icon.
- Special pages (like family tree) switch to white icons + a dedicated background, **only on that route**; the animation is unchanged, only the assets swap.
- `z-index: 150`.

### VoiceFab (voice floating ball)
- First ask the user whether they have this piece and its rules, and confirm the need. If the feature exists but has no specific requirement, follow the content below:

- Stays above all main-interface pages; position stored at the App layer `fabPos`.
- Two states: `ai-ball-idle.png` (idle) / `ai-ball-active.png` (glowing/spinning), controlled by `glow`.
- **Clicking must return to the idle state**: use an independent `voiceActive` state to toggle, don't hardcode "can only open, can't close".
- Drag conversion uses `getBoundingClientRect()` (the page's `clientWidth` drifts after `scale`, see 05).
- `z-index: 200`; weak hint bubbles sit below it.
- The ball's bubble adapts automatically when it touches the screen edge, fitting the text block size.

## 10. z-index hierarchy table

| Layer | z-index | Element |
|-------|---------|---------|
| Page content | 0–4 | background / main image / avatar / badge |
| Status bar | 20 | StatusBar |
| Page weak hints | 30 | family-tree hint bubbles, etc. |
| Dialogs / onboarding | 60–161 | permission dialogs, onboarding guide bubbles |
| Bottom nav | 150 | BottomNav |
| Floating ball / SOS | 200 | VoiceFab, SOS rail |

> For new overlays don't use arbitrary values like 100 or 1000; pick the nearest value from this table to avoid layer conflicts.

## 11. Mobile scaling to fill screen

```css
#app-shell { display: flex; align-items: center; justify-content: center; overflow: hidden; }
.phone {
  width: 390px; height: 844px; flex: none;          /* base size per §2, replace with measured mockup; flex:none prevents shrink */
  transform: scale(var(--app-scale, 1));
  transform-origin: center center;                  /* center matches the web version */
}
* { -webkit-tap-highlight-color: transparent; }     /* remove tap blue-flash */
```

```js
useEffect(() => {
  let lastW = -1
  const applyScale = () => {
    const w = window.innerWidth
    if (w === lastW) return
    lastW = w
    document.documentElement.style.setProperty(
      '--app-scale', String(Math.min(w / 390, window.innerHeight / 844))
    )
  }
  applyScale()
  window.addEventListener('resize', applyScale)
  window.addEventListener('orientationchange', applyScale)
  return () => {
    window.removeEventListener('resize', applyScale)
    window.removeEventListener('orientationchange', applyScale)
  }
}, [])
```

Three pitfalls: `flex:none` (prevents flex shrink); `min` (keep aspect ratio, don't stretch width and height separately); `center` anchor (don't anchor to top). Desktop preview uses `@media (min-width:520px)` for "phone frame + no scaling"; phones use the scaling above.
