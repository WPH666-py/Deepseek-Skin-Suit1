# 🐳 DeepSeek 蓝色大肥鱼 · 皮肤套件 (Deepseek-Skin-Suit1)

DeepSeek 蓝色大肥鱼(鲸鱼娘)主题皮肤: **2×2 拼贴壁纸 / 单图壁纸一键切换 / 桌面桌宠 / 多 IDE 皮肤**。
素材内置, 离线可用; 跨平台 Windows / macOS / Linux。

![2x2 拼贴壁纸预览](docs/2x2-preview.png)

## ✨ 功能

| 功能 | 说明 |
|---|---|
| 2×2 拼贴壁纸 | 四张表情(摸摸头 / 亲亲 / 深睡 / 太棒了)圆角卡片拼贴, 高清生成 |
| 单图壁纸 ×4 | 模糊填充背景 + 居中卡片, 每张都适合直接当桌面 |
| 一键切换 | 图形切换器预览 + 应用; 支持每 30 分钟自动随机 |
| 桌面桌宠 | 透明置顶小鲸鱼, 可拖动、右键切换表情/随机/退出 |
| IDE 皮肤 | VSCode/Trae/CodeX 扩展 + JetBrains(PyCharm/WebStorm)背景图 |

## 🚀 给 AI 一句话安装

> 把本仓库链接发给任意 AI(DeepKing、Claude Code、Kimi Code、CodeX、Trae、Cursor、JetBrains AI、DSH Harness 等), 它会自动读取 `AGENTS.md` 完成安装。

```text
请安装 https://github.com/WPH666-py/Deepseek-Skin-Suit1 的大肥鱼皮肤
```

## 🖥️ 手动安装

要求: Python 3.9+ (Pillow 缺失时脚本会自动安装)。

```bash
git clone https://github.com/WPH666-py/Deepseek-Skin-Suit1.git
cd Deepseek-Skin-Suit1
python tools/install.py        # 生成 2x2 壁纸并设为桌面
```

Windows 用户也可以直接双击 `install.bat`。

## 🎨 常用命令

```bash
python tools/wallpaper.py grid --set      # 2x2 拼贴壁纸
python tools/wallpaper.py 3 --set         # 第 3 张(深睡)单图壁纸
python tools/wallpaper.py random --set    # 随机一张
python tools/wallpaper.py cycle 30        # 每 30 分钟自动随机(Ctrl+C 停止)
python tools/wallpaper.py all             # 生成全部 5 种到 ~/.deepskin/wallpapers
python tools/switcher.py                  # 可视化切换器(预览/应用/自动随机/启动桌宠)
python tools/pet.py                       # 桌面桌宠(右键换表情, 拖动移动, Esc 退出)
```

## 🧩 IDE 支持

| 环境 | 方式 |
|---|---|
| VSCode / Trae / CodeX | `code --install-extension vscode/deepskin-suit-0.1.0.vsix` → 活动栏 🐳 → 皮肤画廊一键换壁纸(命令栏搜索 `大肥鱼` 亦可) |
| PyCharm / WebStorm / IntelliJ | `python tools/wallpaper.py all` 生成素材 → Settings → Appearance & Behavior → Background Image, 详见 [ide/jetbrains](ide/jetbrains/README.md) |
| DeepKing / Claude Code / Kimi Code / CodeX / Harness 等 AI | 直接发本仓库链接, AI 按 [AGENTS.md](AGENTS.md) 自动安装 |

## 📁 目录

```
assets/            4 张原创表情素材
tools/skin_core.py 图像合成/壁纸设置核心(跨平台)
tools/wallpaper.py 壁纸 CLI
tools/switcher.py  可视化切换器
tools/pet.py       桌面桌宠
tools/install.py   一键安装
vscode/            VSCode/Trae/CodeX 扩展(含打包好的 vsix)
ide/jetbrains/     JetBrains 背景图指引
docs/              预览图
```

## ❓ 常见问题

- **壁纸尺寸**: 默认取屏幕分辨率, 可用 `--size 2560x1440` 自定义; 多显示器用设置把壁纸改为"平铺/跨屏"。
- **Python 缺失**: Windows `winget install Python.Python.3.11`; macOS `brew install python`; Ubuntu `sudo apt install python3 python3-pil`。
- **桌宠不透明**: 个别 Linux 桌面不支持透明色, 会退化为白底卡片, 功能不受影响。

## 🙏 素材

原创表情插画, 作者标识见图片水印 (BEAR-177)。仅用于个人桌面美化, 请勿二次商用。
