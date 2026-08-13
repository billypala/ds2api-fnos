#!/usr/bin/env bash
# 下载 fnOS 官方打包工具 fnpack（按当前系统平台自动选择）
set -euo pipefail

VER="1.2.3"
TOOLS="$(cd "$(dirname "$0")/.." && pwd)/tools"
mkdir -p "$TOOLS"

OS="$(uname -s)"
ARCH="$(uname -m)"

case "$OS" in
  Linux)
    case "$ARCH" in
      x86_64|amd64) PLAT="linux-amd64" ;;
      aarch64|arm64) PLAT="linux-arm64" ;;
      *) echo "Unsupported arch: $ARCH" >&2; exit 1 ;;
    esac
    ;;
  Darwin)
    case "$ARCH" in
      x86_64) PLAT="darwin-amd64" ;;
      arm64) PLAT="darwin-arm64" ;;
      *) echo "Unsupported arch: $ARCH" >&2; exit 1 ;;
    esac
    ;;
  MINGW*|MSYS*|CYGWIN*)
    PLAT="windows-amd64"
    ;;
  *)
    echo "Unsupported OS: $OS" >&2; exit 1
    ;;
esac

DEST="$TOOLS/fnpack"
[ "$PLAT" = "windows-amd64" ] && DEST="$TOOLS/fnpack.exe"

if [ -x "$DEST" ]; then
  echo "fnpack already exists: $DEST"
  exit 0
fi

URL="https://static2.fnnas.com/fnpack/fnpack-${VER}-${PLAT}"
echo "Downloading fnpack ${VER} (${PLAT}) -> $DEST"
curl -fsSL "$URL" -o "$DEST"
chmod +x "$DEST"
echo "done"
