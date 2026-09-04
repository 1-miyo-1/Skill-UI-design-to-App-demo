#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 logo.png 生成 Android 自适应图标 + 经典图标。

用法:
    python gen_adaptive_icons.py <logo.png> <android/app/src/main/res> --bg #FFFFFF --safe 0.66  # --bg 换成品牌色

生成:
    mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/ic_launcher.png          (经典: 品牌色背景 + logo 居中)
    mipmap-{...}/ic_launcher_round.png                                (同上)
    mipmap-{...}/ic_launcher_foreground.png                           (前景: 透明画布 + logo 居中)

注意: 还需手动确认 values/ic_launcher_background.xml 的颜色与 --bg 一致。
"""
import os
import argparse

from PIL import Image

# 各密度倍率；经典图标基础 48dp，自适应画布 108dp
DENSITIES = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
LEGACY_BASE = 48
ADAPTIVE_BASE = 108


def hex_to_rgba(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def main():
    ap = argparse.ArgumentParser(description="生成 Android 自适应/经典图标")
    ap.add_argument("logo", help="logo.png 路径")
    ap.add_argument("res_dir", help="android res 目录")
    ap.add_argument("--bg", default="#FFFFFF", help="经典图标背景色(默认占位白，换成品牌色)")
    ap.add_argument("--safe", type=float, default=0.66, help="logo 占画布比例(安全区)")
    args = ap.parse_args()

    logo = Image.open(args.logo).convert("RGBA")
    bg = hex_to_rgba(args.bg)

    for name, mult in DENSITIES.items():
        mip = os.path.join(args.res_dir, "mipmap-" + name)
        os.makedirs(mip, exist_ok=True)

        # 经典图标：logo 缩到 safe 比例，居中贴到纯色背景
        legacy = int(LEGACY_BASE * mult)
        icon = Image.new("RGBA", (legacy, legacy), bg)
        lw = int(legacy * args.safe)
        icon.alpha_composite(logo.resize((lw, lw), Image.LANCZOS),
                             ((legacy - lw) // 2, (legacy - lw) // 2))
        icon.save(os.path.join(mip, "ic_launcher.png"))
        icon.save(os.path.join(mip, "ic_launcher_round.png"))

        # 自适应前景：透明画布上居中放 logo（圆角处透明，露出背景色）
        fg_size = int(ADAPTIVE_BASE * mult)
        fg = Image.new("RGBA", (fg_size, fg_size), (0, 0, 0, 0))
        fw = int(fg_size * args.safe)
        fg.alpha_composite(logo.resize((fw, fw), Image.LANCZOS),
                           ((fg_size - fw) // 2, (fg_size - fw) // 2))
        fg.save(os.path.join(mip, "ic_launcher_foreground.png"))

    print("done:", args.res_dir)


if __name__ == "__main__":
    main()
