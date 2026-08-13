#!/usr/bin/env bash
# 一键构建 ds2api.fpk（Linux / macOS）
# 用法: ./build.sh   （产物输出到当前目录 ds2api.fpk）
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

# 1. 准备 fnpack 工具
bash scripts/fetch-fnpack.sh

# 2. 生成应用图标（ICON.PNG / ICON_256.PNG / ui images）
python3 scripts/gen_icons.py

# 3. 打包 .fpk
./tools/fnpack build --directory app

echo ""
echo "✅ 构建完成: $(pwd)/ds2api.fpk"
