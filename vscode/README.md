# DeepSkin Suit — VSCode / Trae / CodeX 扩展

DeepSeek 蓝色大肥鱼皮肤套件的编辑器侧扩展:
活动栏出现 🐳 **大肥鱼** 图标 → **皮肤画廊**, 点按钮即可一键换壁纸;
也可以在命令面板 (Ctrl+Shift+P) 搜索 `大肥鱼` 执行换壁纸 / 切换器 / 桌宠。

## 依赖
- Python 3.9+ (含 `pip`)
- 皮肤套件仓库: 默认识别 `%USERPROFILE%\DeepSkin-Suit` 或 `~/.deepskin-suit`
  可通过设置 `deepskin.repoPath` 修改。

## 安装 (二选一)
1. 已打包: `code --install-extension deepskin-suit-0.1.0.vsix` (Trae/CodeX 同样支持)
2. 或手动复制 `vscode/` 目录到 `%USERPROFILE%\.vscode\extensions\wp666.deepskin-suit-0.1.0` 后重启编辑器

Pillow 缺失时扩展会自动 `pip install --user pillow`。

## 打包
```bash
cd vscode && npx --yes @vscode/vsce package
```
