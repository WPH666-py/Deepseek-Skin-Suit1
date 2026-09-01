# -*- coding: utf-8 -*-
"""
DeepSeek 蓝色大肥鱼 · 皮肤套件 —— 桌面桌宠
用法: python tools/pet.py

功能:
  • 透明无边框置顶小鲸鱼, 可拖动
  • 右键菜单: 切换 4 种表情 / 随机 / 打开皮肤切换器 / 退出
  • 自动保存位置与表情
"""
import json
import math
import os
import random
import subprocess
import sys
import time
import tkinter as tk
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skin_core as sc  # noqa: E402

WORK_SIZE = 640          # 去背景工作分辨率
DISPLAY_SIZE = 230       # 桌宠显示尺寸
MAGIC = "#010203"        # Windows 透明色
STATE_FILE = os.path.join(sc.APP_DIR, "pet.json")
SLEEP_STEM = "03-deepsleep"

MODES = [
    ("01-pat-head", "摸摸大肥鱼的脑袋"),
    ("02-kiss", "亲亲！"),
    ("03-deepsleep", "深睡 (slow)"),
    ("04-hooray", "小肥鱼太棒了！"),
]


def cut_white_bg(img, thresh=232):
    """从四边泛洪去除白底, 并对边缘做羽化。返回 RGBA。"""
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    kept = bytearray([1]) * (w * h)

    def is_white(x, y):
        r, g, b, a = px[x, y]
        return a > 0 and r >= thresh and g >= thresh and b >= thresh

    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_white(x, y) and kept[y * w + x]:
                kept[y * w + x] = 0
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_white(x, y) and kept[y * w + x]:
                kept[y * w + x] = 0
                q.append((x, y))

    while q:
        x, y = q.popleft()
        px[x, y] = (255, 255, 255, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h:
                i = ny * w + nx
                if kept[i] and is_white(nx, ny):
                    kept[i] = 0
                    q.append((nx, ny))

    # 边缘羽化: 靠近透明的偏白像素, 按亮度线性降不透明度
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if not kept[i]:
                continue
            r, g, b = px[x, y][0], px[x, y][1], px[x, y][2]
            if min(r, g, b) < 200:
                continue
            near = False
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < w and 0 <= ny < h and not kept[ny * w + nx]:
                    near = True
                    break
            if near:
                t = (min(r, g, b) - 190) / 42.0
                t = 0.0 if t < 0 else (1.0 if t > 1 else t)
                px[x, y] = (r, g, b, int(255 * t))
    return img


def load_cut(stem):
    """加载并缓存去底贴图。"""
    cache = os.path.join(sc.CACHE_DIR, "pet-%s.png" % stem)
    from PIL import Image
    if not os.path.exists(cache):
        full = Image.open(os.path.join(sc.ASSETS_DIR, stem + ".jpg"))
        src = full.resize((WORK_SIZE, int(WORK_SIZE * full.height / full.width)), Image.LANCZOS)
        cut = cut_white_bg(src)
        cut.save(cache)
    return Image.open(cache).convert("RGBA")


class Pet:
    def __init__(self):
        import tkinter as _tk
        from PIL import Image, ImageTk
        self.Image = Image
        self.ImageTk = ImageTk

        self.root = tk.Tk()
        self.root.title("deepskinko")
        self.transparent = False
        try:
            self.root.overrideredirect(True)
            self.root.wm_attributes("-topmost", True)
            self.root.wm_attributes("-transparentcolor", MAGIC)
            self.transparent = True
        except _tk.TclError:
            pass

        state = self.load_state()
        if state.get("x") is not None:
            geo = "%dx%d+%d+%d" % (DISPLAY_SIZE, DISPLAY_SIZE + 14, state["x"], state["y"])
        else:
            sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            geo = "%dx%d+%d+%d" % (DISPLAY_SIZE, DISPLAY_SIZE + 14, sw - DISPLAY_SIZE - 80, sh - DISPLAY_SIZE - 140)
        self.root.geometry(geo)

        self.label = tk.Label(self.root, bg=MAGIC if self.transparent else "#ffffff", bd=0)
        self.label.place(x=0, y=0)

        self.images = {}
        stem, _name = MODES[0]
        for s, _n in MODES:
            cut = load_cut(s)
            box = Image.new("RGBA", (DISPLAY_SIZE, DISPLAY_SIZE), (0, 0, 0, 0))
            cut.thumbnail((DISPLAY_SIZE, DISPLAY_SIZE), Image.LANCZOS)
            box.paste(cut, ((DISPLAY_SIZE - cut.width) // 2, (DISPLAY_SIZE - cut.height) // 2), cut)
            bg = Image.new("RGBA", box.size, tuple(int(MAGIC[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
            rgb = Image.alpha_composite(bg, box).convert("RGB")
            self.images[s] = ImageTk.PhotoImage(rgb)

        self.mode = state.get("mode", 0)
        self.random_mode = bool(state.get("random", False))
        self.random_timer = time.time()

        m = tk.Menu(self.root, tearoff=0)
        for i, (s, name) in enumerate(MODES):
            m.add_command(label=name, command=lambda i=i: self.set_mode(i))
        m.add_separator()
        m.add_command(label="随机 30 秒", command=self.toggle_random)
        m.add_command(label="打开皮肤切换器", command=self.open_switcher)
        m.add_separator()
        m.add_command(label="退出", command=self.quit)
        self.menu = m
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.label.bind("<ButtonRelease-1>", self.end_drag)
        self.root.bind("<Button-3>", lambda e: self.menu.tk_popup(e.x_root, e.y_root))
        self.root.bind("<Escape>", lambda e: self.quit())

        self.t = 0.0
        self.drag_off = (0, 0)
        self.set_mode(self.mode, save=False)
        self.loop()

    # ------------------------------------------------------------ state
    def load_state(self):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_state(self):
        try:
            pos = self.root.winfo_x(), self.root.winfo_y()
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump({"x": pos[0], "y": pos[1], "mode": self.mode, "random": self.random_mode}, f)
        except Exception:
            pass

    # ------------------------------------------------------------ ui
    def set_mode(self, idx, save=True):
        self.mode = idx % len(MODES)
        stem = MODES[self.mode][0]
        self.label.configure(image=self.images[stem], width=DISPLAY_SIZE, height=DISPLAY_SIZE)
        if save:
            self.save_state()

    def toggle_random(self):
        self.random_mode = not self.random_mode
        self.random_timer = time.time()
        self.save_state()

    def open_switcher(self):
        exe = sys.executable
        if os.name == "nt":
            w = os.path.join(os.path.dirname(exe), "pythonw.exe")
            if os.path.exists(w):
                exe = w
        subprocess.Popen([exe, os.path.join(sc.TOOLS_DIR, "switcher.py")], cwd=sc.TOOLS_DIR)

    def quit(self):
        self.save_state()
        self.root.destroy()

    def start_drag(self, e):
        self.drag_off = (e.x, e.y)

    def on_drag(self, e):
        x = self.root.winfo_x() + e.x - self.drag_off[0]
        y = self.root.winfo_y() + e.y - self.drag_off[1]
        self.root.geometry("+%d+%d" % (x, y))

    def end_drag(self, _e):
        self.save_state()

    # ------------------------------------------------------------ animation
    def loop(self):
        self.t += 0.09
        stem = MODES[self.mode][0]
        if stem == SLEEP_STEM:
            amp, freq = 2.0, 0.9       # 深睡: 轻轻起伏
        else:
            amp, freq = 7.0, 2.2       # 活跃: 上下漂浮
        bob = int((1 + math.sin(self.t * freq)) * amp)
        self.label.place(x=0, y=bob)
        if self.random_mode and time.time() - self.random_timer > 30:
            self.random_timer = time.time()
            self.set_mode(random.randrange(len(MODES)), save=False)
        self.root.after(40, self.loop)


def main():
    sc.prepare_console()
    sc.ensure_pillow()
    sc.ensure_dirs()
    print("桌宠启动中 ... 右键切换表情, 拖动移动, Esc 退出")
    Pet().root.mainloop()


if __name__ == "__main__":
    main()
