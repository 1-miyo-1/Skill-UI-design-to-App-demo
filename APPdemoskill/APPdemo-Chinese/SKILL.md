---
name: design-to-app
description: 把高保真设计稿（Figma / 图片，固定像素）转成可安装运行的移动 App——识图抽资源 → 搭 React+Vite 项目 → 还原视觉与交互 → 用 Capacitor 打包成 Android APK / iOS App。当用户要「把设计稿做成 App」「设计稿转代码」「做高保真原型」「打包 APK 装手机演示」「把 UI 稿变可点可跑」时使用。
---

# 设计稿 → 可运行 App

把一张/一套高保真设计稿变成「可在手机安装运行」的 App。

默认技术栈：**React 19 + Vite + react-router-dom(HashRouter) + Capacitor 8**，可输出 Android APK / iOS App（debug 签名，课程作业/演示足够；iOS 构建需 macOS + Xcode）。所有固定约定见 `references/00_project_conventions.md`。

## 总流程（8 阶段，按顺序）

| # | 阶段 | 读哪个 reference | 产物 |
|---|------|------------------|------|
| 1 | 读稿抽资源 | `references/01_read_design.md` | 页面清单、配色/字体、切图、基准尺寸 |
| 2 | 搭脚手架 | `references/02_scaffold.md` | 可 `npm run dev` 的空项目 |
| 3 | 页面拆分与路由 | `references/03_screens_and_routes.md` | 路由表 + 组件骨架 |
| 4 | 视觉还原 | `references/04_visual_tokens.md` | 与稿一致的静态界面 |
| 5 | 交互还原 | `references/05_interactions.md` | 可点可拖可跳的交互 |
| 6 | 移动端适配 | `references/06_mobile_adaptation.md` | 手机上不变形、键盘不顶起 |
| 7 | 打包 | `references/07_build_apk.md` | 可安装的 .apk / iOS App |
| 8 | 交付验证 | references/07_build_apk.md（安装与验证） | 真机安装截图确认 |

## 贯穿全程的硬约束（务必先记住）

- **每改一点 → 确认一点 → 再继续**：不批量改动后一次汇报；不确定就问，不猜。
- **严格用用户给的素材**：不擅自画圈 / 加描边 / 改配色 / 换图；只改用户要改的，不顺手"优化"其他部分。
- **素材问用户要，缺的留苹果 HIG 占位空位**：图标用 SF Symbols、头像用系统人形、图片用系统灰块占位并标 `TODO`，别拿网络图或自己画顶替。
- **先量基准尺寸**：稿子的固定宽高（默认 iOS 390×844 / 安卓 360×800，量设计稿替换）是后续缩放、图标、布局的唯一基准。
- **布局完成后先问平台**：整体界面布局（视觉）完成后，问用户装 iOS 还是 Android，据此定基准尺寸（§2）并输出对应平台的代码结构（`cap add ios` / `cap add android`）；别默认 Android。
- **路由必须 HashRouter**：WebView 里 `file://` 下 BrowserRouter 会白屏 404。
- **每阶段自检**：读稿能复述页面；视觉在 `npm run dev` 里看得到；适配在真机 APK 里验。
- **PowerShell 环境变量不跨命令持久**：gradle 每次都要内联 `JAVA_HOME` / `ANDROID_HOME`。

## 结束规则（什么算完成 / 什么算失败）

**只有用户说「可以 / 没问题 / 就是这样」才算结束**；不能「步骤做完了」就自己收工。

### ✅ 正确完成（满足要求）

1. 8 个阶段自检全过，且**每一步都先和用户确认**（见「每改一点 → 确认一点」）。
2. **视觉**：逐页对照设计稿，像素级一致——无畸变、错位、多画/漏画元素。
3. **适配**：真机 APK ① 宽度正好铺满不变形 ② 键盘弹出界面不动 ③ 顶部无 mock 状态栏 ④ 点击不闪蓝。
4. **素材**：全部来自用户；没给的标 `TODO` 占位（苹果 HIG），尺寸/位置正确，等用户补。
5. **交互**：每个交互真机手动走一遍，能点能拖能跳、不白屏。
6. **交付**：APK 装到真机、截图给用户确认，拷贝到目标目录。

### ❌ 错误结束（不满足要求）

- 布局 / 颜色 / 尺寸和设计稿对不上，或出现变形、错位。
- 键盘弹出时界面被压缩或上滑（正确是键盘覆盖）。
- 顶部还残留 mock 的 9:41 状态栏，或点击还有蓝色高亮。
- 用了用户没给的素材：自己找图、自己画、改配色、画圈加描边。
- 照抄了文档里的「（唠唠实例）/（本次示例）」，而不是按约定从自己的设计稿推导。
- 擅自多改了用户没要求的东西（"顺手优化"）。
- 只「能编译 / BUILD SUCCESSFUL」，没真机验证就说完成。

### 判据

**6 条「正确完成」全满足 + 没有一条「错误结束」** = 结束；任一项不达标就继续改，别收工。

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/gen_adaptive_icons.py` | 从 logo.png 生成自适应 + 经典图标 |
| `scripts/strip_statusbar.py` | 批量移除页面里的 StatusBar 组件 |
| `scripts/build_apk.ps1` | 一键 build → sync → assembleDebug → 拷贝 |
| `scripts/vision.cjs` | 无原生视觉模型时读图（调 qwen-vl-max） |

## 模板

| 模板 | 用途 |
|------|------|
| `templates/App.jsx.skeleton` | App 骨架：路由 + 全局状态 + 缩放 + BottomNav/VoiceFab |
| `templates/main.jsx.skeleton` | 入口：引 index.css/screens.css + 挂载 App |
| `templates/index.css.skeleton` | 全局样式：token、`.phone` 缩放、`.screen` 基类 + 复用组件样式 |
| `templates/screens.css.skeleton` | 各页面样式空壳 |
| `templates/Screen.jsx.skeleton` | 新页面骨架 |
| `templates/StatusBar.jsx.skeleton` | mock 状态栏组件 |
| `templates/BottomNav.jsx.skeleton` | 底部 Tab Bar 组件 |
| `templates/VoiceFab.jsx.skeleton` | 语音悬浮球组件 |
| `templates/capacitor.config.json` | Capacitor 配置 |

## 常用默认值（无稿已知）

基准尺寸、品牌色、图标、appName 等固定值见 `references/00_project_conventions.md` §2。

## 补充参考（唯一权威约定）

- `references/00_project_conventions.md` —— 本项目全部固定约定（技术栈 / 目录 / 路由 / token / 字体 / 组件 / z-index / 缩放 / 素材命名），改约定只改这一处。
