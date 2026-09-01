@echo off
chcp 65001 >nul
title DeepSeek 大肥鱼 · 皮肤安装器
where python >nul 2>nul
if errorlevel 1 (
  echo [错误] 未找到 Python。
  echo 请先安装: winget install Python.Python.3.11
  pause
  exit /b 1
)
echo 正在安装 DeepSeek 大肥鱼皮肤套件 ...
python "%~dp0tools\install.py"
pause
