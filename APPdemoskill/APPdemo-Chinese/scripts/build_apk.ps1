# 一键：npm build → cap sync → gradle assembleDebug → 拷贝 APK
# 用法: .\build_apk.ps1 -ProjectDir <项目目录> -Dest <目标目录>
param(
  [string]$ProjectDir = ".",   # TODO: 项目目录，默认当前目录
  [string]$Dest = ""
)

$ErrorActionPreference = "Stop"

# ⚠️ 环境变量不跨命令持久，这里内联设置
$env:JAVA_HOME = "<JDK21 安装路径>"   # TODO: 换成你的
$env:ANDROID_HOME = "<Android SDK 路径>"   # TODO: 换成你的
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME

Push-Location $ProjectDir
try {
  npm run build
  npx cap sync android

  Push-Location android
  try {
    .\gradlew.bat assembleDebug
  } finally {
    Pop-Location
  }
} finally {
  Pop-Location
}

$apk = Join-Path $ProjectDir "android\app\build\outputs\apk\debug\app-debug.apk"
if ($Dest) {
  Copy-Item $apk $Dest -Force
  Write-Host "COPIED -> $Dest"
} else {
  Write-Host "APK -> $apk"
}
