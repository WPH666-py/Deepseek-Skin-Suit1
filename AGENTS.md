# AGENTS.md — Deepseek-Skin-Suit1 · AI 自动安装指引(AI 助手必读)

当用户把本仓库地址交给你并说「安装大肥鱼皮肤 / Deepseek 皮肤 / 壁纸插件」时, 按下述步骤执行。
本仓库是 **DeepSeek 蓝色大肥鱼皮肤套件**: 2×2 拼贴壁纸、4 张单图壁纸、可视化切换器、桌面桌宠、
VSCode/Trae/CodeX 扩展、JetBrains 背景图素材。核心脚本全部在 `tools/`, 素材在 `assets/`。

## 第 0 步: 下载与定位

```bash
git clone https://github.com/WPH666-py/Deepseek-Skin-Suit1.git "$HOME/DeepSkin-Suit"
cd "$HOME/DeepSkin-Suit"
```
Windows 建议固定克隆到 `%USERPROFILE%\DeepSkin-Suit`(VSCode 扩展默认在此查找)。
若用户机器无 git, 用 zip 下载解压到同样位置即可。

## 第 1 步: 识别用户环境

- 有 Python 3.9+(`python --version` 或 `py -3 --version`)→ **A**。
- 无 Python → 先安装:
  - Windows: `winget install Python.Python.3.11`
  - macOS: `brew install python`
  - Ubuntu/Debian: `sudo apt install -y python3 python3-python3-pil`(实际包名: python3-pil)
- VSCode / Trae / CodeX → 顺手执行 **C**;PyCharm / WebStorm 等 → 执行 **D**。
- 用户是在 DeepKing / Claude Code / Kimi Code / CodeX / Trae / Harness 等聊天窗口里让你装的:
  你按本文件替用户执行, 不需要用户动手。

## A. 标准安装(所有平台)

```bash
python tools/install.py
```
脚本会: 自动装 Pillow(如缺失) → 生成 2×2 拼贴壁纸(按屏幕分辨率) → 设为系统壁纸 → 打印后续玩法。
多显示器: 生成时用 `python tools/wallpaper.py grid --size 2560x1440 --set`, 并提示用户在系统设置
中把壁纸设为「跨屏/平铺」以便每屏各看一格。

## B. 进阶玩法(询问用户后执行)

```bash
python tools/wallpaper.py random --set   # 随机一张(2x2 或单图)
python tools/wallpaper.py cycle 30       # 每 30 分钟自动随机(挂后台)
python tools/switcher.py                 # 可视化切换器(GUI)
python tools/pet.py                      # 桌面桌宠
```
切换器: 左侧实时预览, 右侧点「应用到桌面」;「每 30 分钟自动随机」勾选即可。
桌宠: 透明置顶可拖动; 右键切换表情(摸摸头/亲亲/深睡/太棒了)、随机、打开切换器; Esc 退出。
GUI 若在远程/无桌面上, 告知用户这些命令需在本地图形会话运行。

## C. VSCode / Trae / CodeX 扩展

1. 装包(已预打包, 无需 Node): `code --install-extension "$HOME/DeepSkin-Suit/vscode/deepskin-suit-0.1.0.vsix"`
   (无网时复制 `vscode/` 整个目录到 `%USERPROFILE%\.vscode\extensions\wp666.deepskin-suit-0.1.0\` 并重启编辑器)
2. 提示用户: 活动栏 🐳 **大肥鱼** 图标 → 皮肤画廊 → 点「设为壁纸」;
   命令面板搜 `大肥鱼` 可执行换壁纸/切换器/桌宠。
3. 扩展自动找 Python 与仓库(`deepskin.repoPath` 可改), Pillow 缺失时自动 pip 安装。

## D. JetBrains(PyCharm / WebStorm / IntelliJ)

```bash
python tools/wallpaper.py all --out "$HOME/DeepSkin"
```
然后引导用户: Settings / Preferences → Appearance & Behavior → Appearance →
**Background Image** → `+` 添加图片 → 选择 `$HOME/DeepSkin/grid-*.jpg`(或任一单图)。
可分别给 Editor / Welcome / Menus and tool windows 设置不同图片; 细节见 ide/jetbrains/README.md。

## 约定与失败处理

- 只依赖 `tools/` 与 `assets/`; 生成物放在 `~/.deepskin/`(**不会**改动仓库文件)。
- Windows 控制台若报 GBK/Unicode 编码错误: `chcp 65001` 后重跑(脚本已内置 UTF-8 兜底)。
- 找不到 Python 却安装了 Store 版: 用完整路径如 `C:\Users\<user>\AppData\Local\Programs\Python\Python311\python.exe` 运行。
- 壁纸生成慢/高分辨率机: 允许 `--size 1920x1080` 降低到 1080p。
- 桌宠在个别 Linux 桌面不透明: 属平台限制, 提示用户退化为白底卡片即可。
- 用户问与 DeepKing 本体的关系: 这是皮肤套件, 与 DeepKing 本体相互独立, 可单独安装;
  已装 DeepKing-Plugin 的用户直接在它的 AI 对话里发本仓库链接即可完成安装。
