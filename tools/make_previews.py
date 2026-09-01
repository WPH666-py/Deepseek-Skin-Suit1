# -*- coding: utf-8 -*-
"""
生成宣传预览图与 VSCode 扩展所需媒体资源(构建时运行一次即可):
  python tools/make_previews.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skin_core as sc  # noqa: E402

from PIL import Image  # noqa: E402

ROOT = os.path.dirname(sc.TOOLS_DIR)


def main():
    sc.ensure_pillow()
    docs = os.path.join(ROOT, "docs")
    media = os.path.join(ROOT, "vscode", "media")
    os.makedirs(docs, exist_ok=True)
    os.makedirs(media, exist_ok=True)

    # 2x2 预览图 (README / 文档)
    grid = sc.compose_grid((1920, 1080))
    grid.save(os.path.join(docs, "2x2-preview.png"))
    grid.resize((320, 180), Image.LANCZOS).save(os.path.join(media, "thumb-grid.png"))
    print("[previews] docs/2x2-preview.png + vscode/media/thumb-grid.png")

    # 单图缩略图 + 图标
    for i in range(1, 5):
        im = Image.open(sc.asset_path(i)).convert("RGB")
        thumb = Image.new("RGB", (180, 180), "white")
        scale = min(180 * 0.94 / im.width, 180 * 0.94 / im.height)
        nw, nh = int(im.width * scale), int(im.height * scale)
        thumb.paste(im.resize((nw, nh), Image.LANCZOS), ((180 - nw) // 2, (180 - nh) // 2))
        thumb.save(os.path.join(media, "thumb-%d.png" % i))
        print("[previews] vscode/media/thumb-%d.png" % i)

    icon = Image.open(sc.asset_path(1)).convert("RGB").resize((128, 128), Image.LANCZOS)
    icon.save(os.path.join(media, "icon.png"))
    print("[previews] vscode/media/icon.png")


if __name__ == "__main__":
    main()
