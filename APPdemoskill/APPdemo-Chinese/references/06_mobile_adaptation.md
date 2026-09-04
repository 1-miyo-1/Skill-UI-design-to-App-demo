# 06 移动端适配

> 缩放铺屏（`.phone` / `scale` / 去蓝闪 / 桌面分离）的固定约定见 `references/00_project_conventions.md` §11。

## 1. 状态栏：去「设计里的 mock」，留「系统状态栏」

- 删除页面里的 `StatusBar` 组件（mock 的 9:41 时间 / 信号图标）。
- 同时把预留的顶部间距（如 `margin-top: 40px`）清零，内容顶到最上。
- 脚本：`scripts/strip_statusbar.py`。

## 2. 键盘：Android 必须改 manifest

`capacitor.config.json` 里的 `keyboard.resize` **在 Android 上被忽略**（本次验证）。

正确做法：`AndroidManifest.xml` 的 `<activity>` 加：

```xml
android:windowSoftInputMode="adjustNothing"
```

效果：键盘盖在界面上，界面不上滑、不压缩。

## 自检

真机安装 APK：① 宽度正好铺满不畸变 ② 键盘弹出界面不动 ③ 顶部无 mock 状态栏。
