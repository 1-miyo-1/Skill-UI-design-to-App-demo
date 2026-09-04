# design-to-app · 设计稿转 App

> **EN** — Turn a high-fidelity design mockup (Figma / image) into a runnable mobile app.
> **中文** — 把高保真设计稿（Figma / 图片）转成可安装运行的移动 App。

A reusable [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code/skills) that runs the full pipeline — **read the design → extract assets → scaffold a React + Vite project → restore visuals & interactions → package with Capacitor → an installable Android APK / iOS app**.

一个可复用的 Claude Code skill，走完整流程：**识图抽资源 → 搭 React + Vite 项目 → 还原视觉与交互 → Capacitor 打包成 Android APK / iOS App**。

## What it does · 功能

8 stages, in order · 8 个阶段，按顺序：

| # | Stage · 阶段 | Output · 产物 |
|---|-------------|--------------|
| 1 | Read design & extract assets · 读稿抽资源 | page list, colors/fonts, cutouts, base size · 页面清单、配色/字体、切图、基准尺寸 |
| 2 | Scaffold · 搭脚手架 | a runnable `npm run dev` project · 可 `npm run dev` 的项目 |
| 3 | Pages & routes · 页面拆分与路由 | route table + component skeletons · 路由表 + 组件骨架 |
| 4 | Restore visuals · 视觉还原 | pixel-accurate static UI · 与稿一致的静态界面 |
| 5 | Restore interactions · 交互还原 | clickable / draggable / navigable · 可点可拖可跳 |
| 6 | Mobile adaptation · 移动端适配 | no distortion, keyboard doesn't push up · 不变形、键盘不顶起 |
| 7 | Package · 打包 | installable `.apk` / iOS app · 可安装的 .apk / iOS App |
| 8 | Deliver & verify · 交付验证 | real-device install + screenshot · 真机安装 + 截图 |

## Tech stack · 技术栈

React 19 + Vite + react-router-dom (HashRouter) + Capacitor 8 → Android APK (debug-signed) / iOS app (requires macOS + Xcode) · Android APK（debug 签名）/ iOS App（需 macOS + Xcode）。

## Structure · 目录结构

Two complete, self-contained skill versions · 两个完整、可独立安装的版本：

```
APPdemoskill/
├─ README.md                # this file · 本文件
├─ APPdemo-Chinese/         # 中文完整版
│  ├─ SKILL.md
│  ├─ references/  (00–07)  # 中文文档
│  ├─ scripts/      (4)     # 图标 / 删状态栏 / 打包 / 识图
│  └─ templates/    (9)     # 可复制骨架
└─ APPdemo-English/         # English complete version
   ├─ SKILL.md
   ├─ references/  (00–07)  # English docs
   ├─ scripts/      (4)
   └─ templates/    (9)
```

## Install · 安装

Copy the contents of the language folder you want into your skills directory · 把你要的语言文件夹里的内容复制进 skills 目录：

```bash
# 中文版 · Chinese
~/.claude/skills/design-to-app/        ← copy APPdemo-Chinese/ contents here

# English version
~/.claude/skills/design-to-app/        ← copy APPdemo-English/ contents here

# 或项目级 · or project-level
<project>/.claude/skills/design-to-app/
```

Restart Claude Code · 重启后生效。The skill triggers when you ask things like · 触发词如：

- 「把设计稿做成 App」/ "turn a design into an app"
- 「设计稿转代码」/ "design-to-code"
- 「打包 APK 装手机演示」/ "package an APK to install on a phone for a demo"

## Prerequisites · 前置依赖

- Node.js + npm
- Android packaging: JDK 21 + Android SDK (`cmdline-tools`) · Android 打包需 JDK 21 + Android SDK
- iOS packaging: macOS + Xcode · iOS 打包需 macOS + Xcode
- Optional: a DashScope API key for `scripts/vision.cjs`（模型无原生视觉时识图用）

## Notes · 说明

- When the user provides no design spec, defaults follow Apple HIG; assets are asked from the user and left as placeholders when missing. · 用户没给设计规范时默认走苹果 HIG；素材一律问用户要，缺的留占位空位。
