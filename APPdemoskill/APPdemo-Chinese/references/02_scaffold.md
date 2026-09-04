# 02 搭脚手架

> 技术栈 / 目录结构 / 路由 / 全局状态等固定约定见 `references/00_project_conventions.md`。

## 依赖

```bash
npm create vite@latest . -- --template react
npm i react-router-dom
npm i @capacitor/core @capacitor/cli @capacitor/android
```

## 复制模板

把 `templates/` 下的骨架复制进 `src/`（去掉 `.skeleton` 后缀）：

| 模板 | 目标 |
|------|------|
| `main.jsx.skeleton` | `src/main.jsx` |
| `App.jsx.skeleton` | `src/App.jsx` |
| `index.css.skeleton` | `src/index.css` |
| `screens.css.skeleton` | `src/screens.css` |
| `Screen.jsx.skeleton` | `src/screens/*.jsx`（每页复制一份） |
| `StatusBar.jsx.skeleton` | `src/components/StatusBar.jsx` |
| `BottomNav.jsx.skeleton` | `src/components/BottomNav.jsx` |
| `VoiceFab.jsx.skeleton` | `src/components/VoiceFab.jsx` |

- `App.jsx.skeleton` 引用了 `./screens/Splash`、`./screens/Home`，先用 `Screen.jsx.skeleton` 复制出这两页（或改成你的路由）。
- Vite 自带的 demo 残留（`src/App.css`、`src/assets/react.svg` 等）删掉即可，不影响。
- `capacitor.config.json` 到打包阶段（07）再用。

## 自检

`npm run dev` 出**白色手机框**（`.phone` 390×844 + 状态栏 / 底部 tab / 悬浮球占位，还没填真实内容），再进入第 3 阶段。
