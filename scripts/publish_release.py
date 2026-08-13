# -*- coding: utf-8 -*-
"""Create Release v3.7.1 and upload ds2api.fpk asset."""
import os
import sys
import json
import urllib.request
import urllib.error

TOKEN = os.environ.get("GH_TOKEN")
if not TOKEN:
    print("GH_TOKEN env not set")
    sys.exit(1)

REPO = "billypala/ds2api-fnos"
FPK = sys.argv[1] if len(sys.argv) > 1 else "ds2api.fpk"

def req(url, method="GET", data=None, content_type=None, raw=False):
    headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}
    body = None
    if data is not None:
        if isinstance(data, (dict, list)):
            body = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif isinstance(data, bytes):
            body = data
            if content_type:
                headers["Content-Type"] = content_type
        else:
            body = data.encode("utf-8")
            if content_type:
                headers["Content-Type"] = content_type
    r = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()

# 1. 创建 Release
print("===== 创建 Release v3.7.1 =====")
release_payload = {
    "tag_name": "v3.7.1",
    "target_commitish": "main",
    "name": "DS2API v3.7.1 for 飞牛 fnOS (修复安装时序 bug)",
    "body": (
        "## v3.7.1（推荐）\n\n"
        "修复 **v3.7.0 安装时 `env file ... .env not found` 的问题**。\n\n"
        "### 修复内容\n\n"
        "- 引入 **init 容器**（alpine）从包内 target 模板复制 `config.json` 到 PKGVAR，"
        "解耦 fnOS install_callback 时序依赖\n"
        "- `DS2API_ADMIN_KEY` 改用 wizard 必填变量直接注入 compose environment"
        "（不再依赖 install_callback 创建 .env）\n"
        "- 移除 compose `env_file` 引用\n"
        "- wizard `ds2api_admin_key` 改为必填（≥8 位）\n"
        "- `cmd/install_callback` 简化为仅记录诊断日志\n\n"
        "### 安装\n\n"
        "1. 下载 `ds2api.fpk`\n"
        "2. 飞牛应用中心 → 手动安装 → 选择文件\n"
        "3. **必须**设置管理台密钥（≥8 位，妥善保存）\n"
        "4. 桌面「DS2API 管理台」→ `/admin` 登录\n\n"
        "### 上游\n\n"
        "- ouqiting/ds2api v3.7.0 · AGPL-3.0\n"
        "- 镜像：ouqiting/ds2api:latest（x86_64 直接可用）\n"
        "- 源码构建：`./build.sh` 或 `build.ps1`"
    ),
    "draft": False,
    "prerelease": False,
}
status, body = req(f"https://api.github.com/repos/{REPO}/releases", method="POST", data=release_payload)
print(f"HTTP {status}")
if status not in (200, 201):
    print("body:", body.decode("utf-8", errors="replace")[:1000])
    sys.exit(1)
rel = json.loads(body)
rel_id = rel["id"]
print(f"Release id: {rel_id}")
print(f"URL: {rel['html_url']}")

# 2. 上传资产
print("\n===== 上传 ds2api.fpk 资产 =====")
with open(FPK, "rb") as f:
    fpk_bytes = f.read()
status, body = req(
    f"https://uploads.github.com/repos/{REPO}/releases/{rel_id}/assets?name=ds2api.fpk&label=fnOS+%E5%BA%94%E7%94%A8%E5%8C%85",
    method="POST", data=fpk_bytes, content_type="application/octet-stream",
)
print(f"HTTP {status}")
asset = json.loads(body)
print(f"资产: {asset['name']} | {asset['size']} bytes | {asset['browser_download_url']}")

# 3. 验证下载（公开下载，不带 token）
print("\n===== 验证下载 =====")
import hashlib
import urllib.request as ur
with ur.urlopen(asset["browser_download_url"]) as resp:
    dl = resp.read()
local_md5 = hashlib.md5(fpk_bytes).hexdigest()
dl_md5 = hashlib.md5(dl).hexdigest()
print(f"本地: {len(fpk_bytes)} bytes, MD5={local_md5}")
print(f"下载: {len(dl)} bytes, MD5={dl_md5}")
print("✅ 完全一致" if fpk_bytes == dl else "❌ 不一致")

print(f"\n🎉 发布完成：https://github.com/{REPO}/releases/tag/v3.7.1")
