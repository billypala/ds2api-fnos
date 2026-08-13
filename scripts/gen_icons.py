# -*- coding: utf-8 -*-
"""生成 DS2API fnOS 应用图标（64 / 256 两尺寸，含包根与 ui/images 两处）。

用法:
    python scripts/gen_icons.py [app_dir]

app_dir 缺省为脚本同级目录的 ../app（fnOS 应用包目录）。
生成: <app>/ICON.PNG, <app>/ICON_256.PNG, <app>/app/ui/images/icon_64.png, icon_256.png
"""
import os
import sys

from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "..", "app"))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_icon(size: int, out_path: str):
    s = float(size)
    img = Image.new("RGB", (size, size), (27, 42, 107))
    d = ImageDraw.Draw(img)

    # 垂直渐变背景（亮蓝 -> 深靛蓝）
    top = (77, 107, 254)      # #4D6BFE
    bottom = (23, 38, 94)     # #17265E
    for y in range(size):
        t = y / (s - 1)
        d.line([(0, y), (size - 1, y)], fill=lerp(top, bottom, t))

    # 圆角遮罩
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    r = int(s * 0.22)
    md.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=255)
    img.putalpha(mask)

    d = ImageDraw.Draw(img)

    # 顶部源节点
    cx = int(s * 0.5)
    cy = int(s * 0.10)
    rr = int(s * 0.035)
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 255, 255))

    # 白色闪电（网关/转换速度感）
    bolt = [
        (int(s * 0.60), int(s * 0.16)),
        (int(s * 0.33), int(s * 0.56)),
        (int(s * 0.49), int(s * 0.56)),
        (int(s * 0.40), int(s * 0.88)),
        (int(s * 0.70), int(s * 0.46)),
        (int(s * 0.54), int(s * 0.46)),
        (int(s * 0.65), int(s * 0.16)),
    ]
    d.polygon(bolt, fill=(255, 255, 255))

    # 底部链路弧线（API 桥接感）
    arc_w = int(s * 0.045)
    d.arc(
        [int(s * 0.28), int(s * 0.74), int(s * 0.72), int(s * 1.02)],
        start=200, end=340, fill=(255, 255, 255), width=arc_w,
    )

    img.save(out_path, "PNG")
    print("saved:", out_path, img.size)


def main():
    for rel in [
        "ICON.PNG",
        "ICON_256.PNG",
        os.path.join("app", "ui", "images", "icon_64.png"),
        os.path.join("app", "ui", "images", "icon_256.png"),
    ]:
        out = os.path.join(APP, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        draw_icon(64 if rel.endswith("64.png") or rel == "ICON.PNG" else 256, out)
    print("done")


if __name__ == "__main__":
    main()
