# 一键构建 ds2api.fpk（Windows PowerShell）
# 用法: .\build.ps1   （产物输出到当前目录 ds2api.fpk）
$ErrorActionPreference = "Stop"

$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ROOT

# 1. 准备 fnpack 工具
& "$ROOT\scripts\fetch-fnpack.ps1"

# 2. 生成应用图标（ICON.PNG / ICON_256.PNG / ui images）
& python "scripts\gen_icons.py"

# 3. 打包 .fpk
& "$ROOT\tools\fnpack.exe" build --directory app

Write-Host ""
Write-Host "OK: $ROOT\ds2api.fpk"
