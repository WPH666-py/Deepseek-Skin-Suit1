# -*- coding: utf-8 -*-
"""
DeepSeek 蓝色大肥鱼 · 皮肤套件 —— 核心库
跨平台: Windows / macOS / Linux
功能: 素材定位、2x2 拼贴壁纸、单图壁纸(模糊填充)、系统壁纸设置
"""
import os
import platform
import subprocess
import sys

APP_DIR = os.path.join(os.path.expanduser("~"), ".deepskin")
WALLPAPER_DIR = os.path.join(APP_DIR, "wallpapers")
CACHE_DIR = os.path.join(APP_DIR, "cache")
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(TOOLS_DIR), "assets")

IMAGE_FILES = ["01-pat-head.jpg", "02-kiss.jpg", "03-deepsleep.jpg", "04-hooray.jpg"]
IMAGE_NAMES = [
    "摸摸大肥鱼的脑袋",
    "亲亲！",
    "深睡 deepsleep",
    "小肥鱼太棒了！",
]
# 可切换的壁纸模式: ("grid" | "single1".."single4", 显示名)
MODES = [("grid", "2×2 拼贴(默认)")] + [
    ("single%d" % (i + 1), IMAGE_NAMES[i]) for i in range(len(IMAGE_FILES))
]


def ensure_dirs():
    for d in (APP_DIR, WALLPAPER_DIR, CACHE_DIR):
        os.makedirs(d, exist_ok=True)


def prepare_console():
    """Windows GBK 控制台避免 Unicode 打印崩溃。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def ensure_pillow():
    """确保 Pillow 可用; 缺失时自动 pip 安装。"""
    try:
        import PIL  # noqa: F401
        return
    except ImportError:
        pass
    print("[deepskin] 未检测到 Pillow, 正在自动安装 ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pillow"])
    import PIL  # noqa: F401


def asset_path(idx):
    """idx: 1..4"""
    return os.path.join(ASSETS_DIR, IMAGE_FILES[idx - 1])


def screen_size():
    """返回主屏幕尺寸 (W, H), 失败时回退 1920x1080。"""
    env = os.environ.get("DEEPSKIN_SIZE", "").strip()
    if env:
        try:
            w, h = env.lower().split("x")
            return int(w), int(h)
        except ValueError:
            pass
    try:
        if platform.system() == "Windows":
            import ctypes
            user32 = ctypes.windll.user32
            return int(user32.GetSystemMetrics(0)), int(user32.GetSystemMetrics(1))
    except Exception:
        pass
    return 1920, 1080


# ---------------------------------------------------------------- 图像合成

def _gradient(size, top=(250, 252, 255), bottom=(232, 242, 253)):
    """极浅蓝白渐变背景。"""
    from PIL import Image
    w, h = size
    g = Image.new("RGB", (1, max(h, 2)))
    for y in range(h):
        t = y / max(h - 1, 1)
        g.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    return g.resize((w, h))


def _paste_card(base, src, cell, margin_ratio=0.045, radius_ratio=0.05, shadow=True):
    """把 src 按 contain 方式贴进 cell, 圆角 + 柔和阴影。"""
    from PIL import Image, ImageDraw, ImageFilter

    x0, y0, cw, ch = cell
    margin = max(6, int(min(cw, ch) * margin_ratio))
    tw, th = cw - 2 * margin, ch - 2 * margin
    scale = min(tw / src.width, th / src.height)
    nw, nh = max(1, int(src.width * scale)), max(1, int(src.height * scale))
    tile = src.resize((nw, nh), Image.LANCZOS)
    x, y = x0 + (cw - nw) // 2, y0 + (ch - nh) // 2
    radius = max(6, int(min(cw, ch) * radius_ratio))

    mask = Image.new("L", (nw, nh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, nw - 1, nh - 1], radius=radius, fill=255)

    if shadow:
        pad = max(10, radius)
        sh = Image.new("RGBA", (nw + 2 * pad, nh + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle(
            [pad, pad, pad + nw - 1, pad + nh - 1], radius=radius, fill=(24, 55, 110, 64)
        )
        sh = sh.filter(ImageFilter.GaussianBlur(max(8, radius // 2)))
        base.alpha_composite(sh, (x - pad, y - pad))
    base.paste(tile, (x, y), mask)


def compose_grid(size=(3840, 2160), cols=2, rows=2):
    """紧贴式 2x2 拼贴壁纸: 四张卡片几乎挨在一起(细缝), 整体居中成一块相片墙。
    卡片大小由屏幕高度决定; 缝隙/外边距比例可用环境变量 DEEPSKIN_GRID_GAP 调整(百分比, 默认 1.5)。"""
    ensure_pillow()
    from PIL import Image

    if len(IMAGE_FILES) > cols * rows:
        raise ValueError("素材数量超过网格容量")
    W, H = size
    try:
        gap_pct = float(os.environ.get("DEEPSKIN_GRID_GAP", "1.5"))
    except ValueError:
        gap_pct = 1.5
    m = min(W, H)
    pad = max(6, int(m * 0.015))  # 外圈边距
    gap = max(4, int(m * gap_pct / 100.0))  # 卡片之间细缝
    t = min(
        (H - 2 * pad - (rows - 1) * gap) // rows,
        (W - 2 * pad - (cols - 1) * gap) // cols,
    )
    t = max(t, 64)
    total_w = cols * t + (cols - 1) * gap
    total_h = rows * t + (rows - 1) * gap
    x0 = (W - total_w) // 2
    y0 = (H - total_h) // 2

    base = _gradient(size).convert("RGBA")
    for i, f in enumerate(IMAGE_FILES):
        src = Image.open(os.path.join(ASSETS_DIR, f)).convert("RGB")
        r, c = divmod(i, cols)
        cell = (x0 + c * (t + gap), y0 + r * (t + gap), t, t)
        _paste_card(base, src, cell, margin_ratio=0.018, radius_ratio=0.03, shadow=False)
    return base.convert("RGB")


def compose_single(idx, size=(1920, 1080)):
    """单图壁纸: 模糊填充背景 + 居中圆角卡片。"""
    ensure_pillow()
    from PIL import Image, ImageFilter

    src = Image.open(asset_path(idx)).convert("RGB")
    w, h = size
    # 模糊填充背景
    s = 96
    small = src.resize((s, max(1, int(s * src.height / src.width))), Image.BOX)
    bg = small.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(32))
    base = bg.convert("RGBA")
    _paste_card(base, src, (0, 0, w, h), margin_ratio=0.035, radius_ratio=0.035)
    return base.convert("RGB")


def compose(mode, size=None):
    """按模式名合成壁纸: mode ∈ {grid, single1..single4}"""
    size = tuple(size) if size else screen_size()
    if mode == "grid":
        return compose_grid(size)
    if mode.startswith("single"):
        return compose_single(int(mode[6:]), size)
    raise ValueError("未知模式: %s" % mode)


def wallpaper_path(mode, size):
    return os.path.join(WALLPAPER_DIR, "%s-%dx%d.jpg" % (mode, size[0], size[1]))


def build(mode, size=None, force=False):
    """合成并保存, 返回文件路径。"""
    ensure_dirs()
    size = tuple(size) if size else screen_size()
    out = wallpaper_path(mode, size)
    if not force and os.path.exists(out):
        return out
    img = compose(mode, size)
    img.save(out, quality=92)
    return out


# ---------------------------------------------------------------- 系统壁纸

def set_wallpaper(path):
    """跨平台设置系统壁纸。"""
    path = os.path.abspath(path)
    system = platform.system()
    if system == "Windows":
        import ctypes
        # SPI_SETDESKWALLPAPER=20, SPIF_UPDATEINIFILE|SPIF_SENDWININICHANGE=3
        ok = ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
        if not ok:
            raise RuntimeError("Windows 设置壁纸失败")
    elif system == "Darwin":
        subprocess.run(
            [
                "osascript", "-e",
                'tell application "System Events" to set picture of every desktop '
                'to POSIX file "%s"' % path,
            ],
            check=True,
        )
    else:
        import pathlib
        uri = pathlib.Path(path).as_uri()
        ok = True
        try:
            subprocess.run(
                ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri],
                check=False,
            )
        except Exception:
            ok = False
        try:
            subprocess.run(
                ["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri],
                check=False,
            )
        except Exception:
            pass
        if not ok:
            subprocess.run(["feh", "--bg-fill", path], check=False)
    print("[deepskin] 壁纸已设置: %s" % path)


if __name__ == "__main__":
    from PIL import Image  # noqa: F401  (仅为检查)
