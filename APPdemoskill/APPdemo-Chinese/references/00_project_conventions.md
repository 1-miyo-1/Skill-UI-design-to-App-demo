# 项目约定（单一事实来源）

本文是「设计稿 → App」的**唯一权威约定**。所有阶段 reference 里的固定事实都以这里为准；改约定只改这一处，别在其他文件里散改。

> 收工标准（什么算完成 / 失败）见 `SKILL.md` 的「结束规则」。

## 1. 技术栈

React 19 + Vite + react-router-dom（**HashRouter**）+ Capacitor 8，输出 Android APK（debug 签名，课程作业/demo演示）。

## 2. 基准尺寸与默认值

**先问规范、再定值**：
- 开工前先询问并阅读用户的设计规范（Design System / 设计稿规范文档）。
- 用户没有设计规范时，默认参考**苹果人机界面指南（Apple HIG）**，并以设计稿实测尺寸为准。
- 阅读用户设计规范后，返还界面对应数据，让用户确认。

主动询问以下基础信息，用户给了就优先采用，拿不到才落默认值：

- **界面主色**：按钮/图标底 `#FFFFFF`，品牌渐变 `#FFFFFF → #000000`。
- **appName**：默认「您的APP」。
- **图标 logo**：占 **66% 安全区**。
- **设计稿固定尺寸**：默认iOS/苹果/iPhone ：**390px × 844px**；默认安卓：**360px × 800px**（后续缩放/图标/布局的唯一基准）
- **界面菜单栏**：默认五个文字 “首页”、“发现”、“工具”、“消息”、“我的”、素材位置

> 不要用默认值覆盖用户给过的信息。

## 3. 目录结构

```
src/
  assets/        # 切图（logo、头像、icon…）
  components/    # 跨页复用（BottomNav、StatusBar、VoiceFab…）
  screens/       # 一页一文件（Home.jsx、Chat.jsx…）
  App.jsx        # 路由 + 全局状态 + 缩放逻辑
  index.css      # 全局：token、.phone 缩放、适配
  screens.css    # 各页面样式
public/
  fonts/         # 内嵌字体（Vite 需忽略，防 EBUSY）
```

## 4. 路由与组件粒度

- **路由必须 HashRouter**（WebView 里 `file://` 下 BrowserRouter 会白屏 404）。
- 粒度：页面（screens/）一页一文件；复用组件（components/）跨页；流程内弹层（如 EmergencyCall）挂 App 层用状态控制显隐。
- `main.jsx` 只做挂载 + 引 `index.css`。

## 5. 全局状态

「会话内设置过就保持」的状态（是否已加联系人 / 已设紧急联系人 / 引导是否播完）**提到 App 层**，返回页面不重置；悬浮球位置 `fabPos` 也在 App 层。

## 6. 设计 token（`:root` CSS 变量）

**默认中性占位，品牌色问用户要**（对应 §2「界面主色」）：没给品牌色就用占位白 `#FFFFFF`、渐变 `#FFFFFF → #000000`，文字 `#000` / 次文字 `#8E8E93`，背景 `#FFFFFF` / 深色 `#000000`；变量名用中性（`--brand` / `--bg` / `--ink` / `--gray`）。用户给了品牌色再替换成品牌值。

```css
:root {
  --brand: #FFFFFF;                                              /* 主色：占位白，等用户品牌色 */
  --brand-grad: linear-gradient(#FFFFFF, #000000);              /* 渐变：占位 */
  --bg: #FFFFFF;                                                 /* 背景 */
  --bg-deep: #000000;                                            /* 深色背景 */
  --ink: #000000;                                                /* 主文字 */
  --gray: #8E8E93;                                               /* 次文字 */
}
```

颜色固化进变量，别散落 hex；多主题用变量切换，别硬编码。

## 7. 字体内嵌（⚠️ EBUSY 坑）

```css
@font-face {
  font-family: "Alibaba PuHuiTi";
  src: url("/fonts/AlibabaPuHuiTi-Regular.otf") format("opentype");
  font-weight: 400;
  font-display: swap;
}
```

- 字体文件放 `public/fonts/`。
- **Vite 需忽略 `public/fonts`**，否则 Windows 下文件被占用报 `EBUSY`（本次踩坑）。

## 8. 图片与素材

**素材一律问用户要，缺的按苹果 HIG 留占位空位**：

1. 开工前列一份素材清单（logo / 头像 / 背景 / icon / 字体），逐项问用户要，别自己找图、别自己画。
2. 用户没给的素材，**保留占位空位**、标 `TODO`，等用户补：

| 缺什么 | 苹果 HIG 占位 |
|--------|--------------|
| 图标 | SF Symbols 系统图标，或等尺寸灰色圆角块 |
| 头像 / 人物 | 系统人形 `person.crop.circle`（灰色） |
| 图片 / 背景 | 系统灰块 `#E5E5EA` + 提示文字 |
| 字体 | 系统字体（苹方 / San Francisco） |

> 占位要占对**尺寸和位置**，用户补素材时「只替换、不改布局」。

- 切图统一放 `src/assets/`，用 `import` 引入（Vite 哈希 + 打进包）。
- 大图（背景、视频）放 `public/` 直接引用。
- **命名约定**：小写英文 + 连字符；`nav-` / `bg-` / `icon-` 前缀表用途；页面专属带页面前缀（`nav-family-*`）；有态切换加 `-idle` / `-active`。
- **映射表**：设计名 → 代码名记一张表，逐张核对尺寸（如家族树页实例），具体的素材使用用户提供的素材内容：

| 代码文件名 | 设计素材源 | 尺寸 |
|-----------|-----------|------|
| `family-tree-bg.png` | `树.png` | 1796×3824 |
| `ginkgo-tree.png` | `银杏树.png` | 1796×2424 |
| `yeye.png` | `选中icon\爷爷.png` | 374×424 |
| `xiaoming.png` | `选中icon\小明.png` | 375×392 |
| `xiaoli.png` | `选中icon\小丽.png` | 400×392 |
| `nav-family-bg.png` | `家族树菜单栏背景.png` | 1860×338 |
| `nav-family-home.png` | `家族树菜单栏\首页.png` | 118×188 |
| `nav-family-tools.png` | `家族树菜单栏\工具.png` | 117×196 |
| `nav-family-tree.png` | `家族树菜单栏\家族树.png` | 304×304 |
| `nav-family-msg.png` | `家族树菜单栏\消息.png` | 137×188 |
| `nav-family-profile.png` | `家族树菜单栏\我的.png` | 108×188 |

- （唠唠实例）人物头像这类素材**自带圆角白边**，代码里不要再画圈 / 加描边，直接贴原图。
- 菜单栏整套图标，尺寸和其他页一致，仅替换素材、保留动画。

## 9. 复用组件

> 下面是通用约定；带「（唠唠实例）」标注的是本项目具体实现，换项目时按苹果 HIG 相应替换（Tab Bar / SF Symbols / 系统组件）。
>
> 三个组件的可跑骨架见 `templates/`：`StatusBar.jsx.skeleton` / `BottomNav.jsx.skeleton` / `VoiceFab.jsx.skeleton`（复制 → 改名 `Xxx.jsx` 放 `src/components/`），配套 CSS 在 `index.css.skeleton` 末尾。

### StatusBar（状态栏）
- `<StatusBar />` → 黑字（`#000`），浅色背景用。
- `<StatusBar light />` → 白字（`#fff`），深色/图片背景用。
- 信号/WiFi/电池图标用 `currentColor` 画，颜色跟着文字走。
- `z-index: 20`。**打 APK 前整体删掉**（真机有系统状态栏，见 06）。

### BottomNav（底部导航）
- 通用：底部导航默认走苹果 **Tab Bar**——问用户几个 tab、各 tab 的图标和文案，3–5 个为宜，选中高亮。
- （唠唠实例）5 tab（首页 / 工具 / 家族树 / 消息 / 我的），彩色图标 + 文字。
- 浮动白色指示条 `.bottom-nav__indicator` 用 `transition:left .35s` 滑动，选中项切白色高亮图标。
- 特殊页（如家族树）换白色图标 + 专属背景，**只在该路由生效**，动画不变、仅换素材。
- `z-index: 150`。

### VoiceFab（语音悬浮球「悬浮球」）
- 先询问用户是否有这部分内容以及相关规则，并确认需求。如果有该功能且没有具体需求时，执行下面的内容：

- 常驻主界面各页之上，位置存 App 层 `fabPos`。
- 两态：`ai-ball-idle.png`（静止）/ `ai-ball-active.png`（发光/旋转），由 `glow` 控制。
- **点击要能回到静止态**：用独立 `voiceActive` 状态 toggle，别写死只能开不能关。
- 拖拽换算用 `getBoundingClientRect()`（页面被 `scale` 后 `clientWidth` 会漂，见 05）。
- `z-index: 200`，弱提示气泡在其下。
- 悬浮球的气泡接触到屏幕边缘自动变化，适配文字段落大小

## 10. z-index 层级总表

| 层级 | z-index | 元素 |
|------|---------|------|
| 页面内容 | 0–4 | 背景图 / 主体图 / 头像 / 角标 |
| 状态栏 | 20 | StatusBar |
| 页面弱提示 | 30 | 家族树提示气泡等 |
| 弹窗 / 引导 | 60–161 | 权限弹窗、新手引导气泡 |
| 底部导航 | 150 | BottomNav |
| 悬浮球 / SOS | 200 | VoiceFab、SOS 滑轨 |

> 新增浮层别用 100、1000 这种随意值，按上表就近取，避免层级打架。

## 11. 移动端缩放铺屏

```css
#app-shell { display: flex; align-items: center; justify-content: center; overflow: hidden; }
.phone {
  width: 390px; height: 844px; flex: none;          /* 基准尺寸见 §2，量稿子替换；flex:none 防压缩 */
  transform: scale(var(--app-scale, 1));
  transform-origin: center center;                  /* center 与网页版一致 */
}
* { -webkit-tap-highlight-color: transparent; }     /* 去点击蓝闪 */
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

三个坑：`flex:none`（防 flex 压缩）；`min`（等比，别横竖分别拉伸）；`center` 锚点（别 top 锚定）。桌面预览用 `@media (min-width:520px)` 走「手机框 + 无缩放」，手机端走上面的缩放。
