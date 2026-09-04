# 01 Read the design & extract assets

Goal: before writing code, turn the mockup into "structured, codable input".

## 1. Read the image (when the model has no native vision)

Models like DeepSeek have no vision; use `vision.cjs` to call `qwen-vl-max` (verified working). If the project already has this script, reuse it directly; otherwise build one from the `scripts/vision.cjs` skeleton. The essence: base64 the image, hand it to a multimodal model, get back a text description.

Key points:
- Describe **one page at a time**; don't have the model summarize the whole mockup in one go.
- Ask concretely: structure tree, primary color, font size, font family, key cutouts, fixed size.

Example call:

```bash
node vision.cjs "E:\...\app mockups\family-tree - split layers.png"
```

The returned description isn't the final answer — **retell it as "the layout I read" for the user to confirm** (element position / size / spacing / color, item by item) before coding.

## 2. Four things you must produce

1. **Page list**: all screens + the navigation between them.
   e.g. Splash → Register → Onboarding → Home → (Chat half/full · Tools · Family · Messages · Profile).
2. **Design tokens**: primary/secondary color, dark-theme color, functional colors, font-size scale, corner radius. (No brand color? use placeholder, see 00 §6)
3. **Font**: the design font (e.g. Alibaba PuHuiTi); confirm whether you have the .otf/.ttf file.
4. **Cutout list**: which things are images (logo, avatars, backgrounds, icons) vs. which can be drawn in code. **Make a list and actively ask the user for assets**, exporting each into `src/assets/`; whatever the user didn't give, mark "placeholder" and leave an Apple HIG slot (see 00 §8).

## 3. Measure the base size

Read the mockup's fixed width/height (default iOS **390×844** / Android **360×800**, replace with the measured mockup). **This number flows through all later scaling/icon calculations** — nail it down before continuing.

Read PNG width/height (IHDR header: bytes 16–19 are width, 20–23 are height):

```powershell
$b = [System.IO.File]::ReadAllBytes('xxx.png')
$w = [int]$b[16]*16777216 + [int]$b[17]*65536 + [int]$b[18]*256 + [int]$b[19]
$h = [int]$b[20]*16777216 + [int]$b[21]*65536 + [int]$b[22]*256 + [int]$b[23]
"$w x $h"
```

⚠️ Don't use `-shl` bit-shifting (PowerShell 5.1 has a bug that returns only the low byte — e.g. reading 1796×3824 as 4×240).

## 4. Self-check

Without looking at the image, you can retell: how many pages, the primary color, the font, the base size. If you can't retell them, you haven't read enough — don't rush into code.
