#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量移除 React 页面里的 StatusBar 组件（import + JSX 使用行）。

用法:
    python strip_statusbar.py <screens目录>
"""
import glob
import os
import re
import sys


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    for f in glob.glob(os.path.join(d, "*.jsx")):
        with open(f, encoding="utf-8") as fh:
            s = fh.read()
        orig = s
        # 去掉 import StatusBar ...
        s = re.sub(r'^\s*import\s+StatusBar\s+from\s+[^\n]+\n', '', s, flags=re.M)
        # 去掉 <StatusBar .../> 使用行（含 <StatusBar light /> 带 props 的写法）
        s = re.sub(r'^\s*<StatusBar[^>]*/>\s*\n', '', s, flags=re.M)
        if s != orig:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(s)
            print("stripped", f)


if __name__ == "__main__":
    main()
