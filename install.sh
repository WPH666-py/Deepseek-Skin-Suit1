#!/usr/bin/env bash
# DeepSeek 大肥鱼 · 皮肤安装器 (macOS / Linux)
set -e
cd "$(dirname "$0")"
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "[错误] 未找到 Python, 请先安装 Python 3 (macOS: brew install python; Linux: sudo apt install python3)"
  exit 1
fi
echo "正在安装 DeepSeek 大肥鱼皮肤套件 ..."
"$PY" tools/install.py
