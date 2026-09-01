# JetBrains 系 IDE (PyCharm / WebStorm / IntelliJ) — 大肥鱼背景图

背景图是 JetBrains 官方 UI 功能, 脚本负责生成高清素材, 之后只需 2 次点击。

## 步骤 (可让 AI 自动执行)
1. 生成全部素材:
   ```bash
   python tools/wallpaper.py all --out "%USERPROFILE%\DeepSkin"   # Windows
   python tools/wallpaper.py all --out ~/DeepSkin                 # macOS / Linux
   ```
   输出: `grid-*.jpg` 2×2 拼贴 + `single1..4-*.jpg` 单图, 共 5 张。
2. 打开 IDE: **Settings / Preferences → Appearance & Behavior → Appearance → Background Image**
3. 点击 `+` 添加图片 → 选择刚生成的任意一张 (推荐 `grid-` 2×2 拼贴)
4. 可对 **Editor / Welcome / Menus and Tool windows** 分别设置不同图片

## 说明
- 背景图支持按 UI 区域分别设置: 编辑器区建议单图, 欢迎页建议 2×2 拼贴。
- 想换壁纸时重复第 3 步选择另一张即可。
- 生成的图片也通用: 任意支持背景图的 JetBrains IDE、以及 Windows 桌面壁纸都能直接用。
