# 下载 fnOS 官方打包工具 fnpack（Windows）
$ErrorActionPreference = "Stop"

$Ver = "1.2.3"
$Tools = Join-Path (Split-Path -Parent $PSScriptRoot) "tools"
New-Item -ItemType Directory -Force -Path $Tools | Out-Null

$Dest = Join-Path $Tools "fnpack.exe"
if (Test-Path $Dest) {
    Write-Host "fnpack already exists: $Dest"
    exit 0
}

$Url = "https://static2.fnnas.com/fnpack/fnpack-$Ver-windows-amd64"
Write-Host "Downloading fnpack $Ver (windows-amd64) -> $Dest"
Invoke-WebRequest -Uri $Url -OutFile $Dest
Write-Host "done"
