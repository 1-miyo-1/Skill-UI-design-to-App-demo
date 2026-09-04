# 07 打包（Android APK / iOS App）

> 先确认平台（iOS / Android）——见 `SKILL.md` 硬约束「布局完成后先问平台」。appName、图标 66% 安全区等固定值见 `references/00_project_conventions.md` §2。

## 平台分支

- **Android**：走下面的「接入 Capacitor → 构建 APK」。
- **iOS**：`npx cap add ios` 生成 Xcode 工程，需 **macOS + Xcode**（见文末「iOS 构建」）；Windows 上只能做 Android。

## 环境（一次性）

- JDK 21（Temurin），`JAVA_HOME` 指向它。
- Android SDK：`cmdline-tools` + `platforms;android-36` + `build-tools;36.0.0`。
- `ANDROID_HOME` 指向 SDK。

## 接入 Capacitor

```bash
npm i @capacitor/core @capacitor/cli @capacitor/android
npx cap init "您的APP" com.example.app --web-dir dist
npm run build
npx cap add android   # 目标 iOS 则换成 npx cap add ios
```

- `capacitor.config.json`：appId / appName / webDir（`keyboard.resize` 可留，Android 忽略）。
- `strings.xml` 里 `app_name` = 桌面显示名。

## 图标（自适应）

- **前景** `ic_launcher_foreground.png`：logo 缩到 **66% 安全区**，居中贴在**透明**画布上。
- **经典** `ic_launcher.png` / `ic_launcher_round.png`：logo 66% 居中贴到**品牌色背景**（问用户，没给用占位白 `#FFFFFF`）。
- `values/ic_launcher_background.xml`：`<color name="ic_launcher_background">#FFFFFF</color>`（换成品牌色）。

脚本：

```bash
python scripts/gen_adaptive_icons.py <logo.png> <res目录> --bg #FFFFFF --safe 0.66  # --bg 换成品牌色
```

## 构建（⚠️ PowerShell 环境变量不持久，内联）

```powershell
$env:JAVA_HOME='<JDK21 安装路径>'   # TODO: 换成你的
$env:ANDROID_HOME='<Android SDK 路径>'   # TODO: 换成你的
$env:ANDROID_SDK_ROOT=$env:ANDROID_HOME
cd android; .\gradlew.bat assembleDebug
```

产物：`android/app/build/outputs/apk/debug/app-debug.apk`。

一键脚本：`scripts/build_apk.ps1`。

## 安装到手机 + 验证

安装（任选其一）：
- 把 `.apk` 拷到手机 → 文件管理器点开安装（需允许「未知来源」）。
- USB 连手机 → `adb install app-debug.apk`。

验证清单（对应 06 的改动）：
1. 桌面图标品牌色背景、logo 居中、圆角不填黑边。
2. 点任何地方不闪蓝。
3. 顶部没有 mock 的 9:41 状态栏（保留系统状态栏）。
4. 界面宽度正好铺满、不变形；键盘弹出界面不上滑、不压缩。

## iOS 构建（需 macOS + Xcode）

```bash
npx cap add ios
cd ios && pod install        # 装了插件才需要
open App.xcworkspace          # Xcode 打开
```
Xcode 里选真机/模拟器 → Run（真机需签名）。产物 `.app`；上架走 Archive → IPA。iOS 上 `keyboard.resize` 生效、原生状态栏无需删 mock，适配细节同 06。

## 交付

拷贝到目标目录。**debug 签名**仅供演示，上架需正式签名。构建成功（Android `BUILD SUCCESSFUL` / iOS Xcode 编译通过）+ 真机安装成功。
