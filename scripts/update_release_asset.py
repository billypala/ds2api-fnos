# -*- coding: utf-8 -*-
"""更新 Release 资产：删除旧 ds2api.fpk 资产 → 上传新版本。"""
import os
import sys
import json
import hashlib
import urllib.request
import urllib.error

TOKEN = os.environ.get("GH_TOKEN")
REPO = "billypala/ds2api-fnos"
TAG = sys.argv[1] if len(sys.argv) > 1 else "v3.7.0.1"
FPK = sys.argv[2] if len(sys.argv) > 2 else "ds2api.fpk"
# 默认资产文件名带版本号（ds2api-3.7.0.1.fpk）；可用第 3 个参数覆盖
ASSET_NAME = sys.argv[3] if len(sys.argv) > 3 else f"ds2api-{TAG.lstrip('v')}.fpk"
LABEL = f"fnOS 应用包 {TAG}（Native 自包含，零 Docker 依赖）"


def req(url, method="GET", data=None, content_type=None):
    headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}
    body = None
    if data is not None:
        if isinstance(data, bytes):
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


# 1. 找 release + 旧资产
print(f"===== 查找 Release {TAG} =====")
status, body = req(f"https://api.github.com/repos/{REPO}/releases/tags/{TAG}")
if status != 200:
    print(f"HTTP {status}: 找不到 release"); sys.exit(1)
rel = json.loads(body)
rel_id = rel["id"]
print(f"Release id: {rel_id}")

for a in rel["assets"]:
    if a["name"] == ASSET_NAME or a["name"] == "ds2api.fpk":
        old_asset_id = a["id"]
        print(f"旧资产: id={old_asset_id}, name={a['name']}, size={a['size']} bytes")
        break
else:
    old_asset_id = None
    print(f"未找到旧 {ASSET_NAME} / ds2api.fpk 资产")

# 2. 删除旧资产
if old_asset_id:
    status, _ = req(
        f"https://api.github.com/repos/{REPO}/releases/assets/{old_asset_id}",
        method="DELETE",
    )
    print(f"删除旧资产 → HTTP {status}")

# 3. 上传新资产
print(f"===== 上传新 {ASSET_NAME} =====")
with open(FPK, "rb") as f:
    fpk_bytes = f.read()
status, body = req(
    f"https://uploads.github.com/repos/{REPO}/releases/{rel_id}/assets?name={ASSET_NAME}&label={urllib.parse.quote(LABEL)}",
    method="POST", data=fpk_bytes, content_type="application/octet-stream",
)
print(f"HTTP {status}")
asset = json.loads(body)
print(f"新资产: {asset['name']} | {asset['size']} bytes | label={asset.get('label')}")
print(f"  URL: {asset['browser_download_url']}")

# 4. 验证下载
print("===== 验证下载 =====")
import urllib.request as ur
with ur.urlopen(asset["browser_download_url"]) as resp:
    dl = resp.read()
print(f"本地: {len(fpk_bytes)} bytes, MD5={hashlib.md5(fpk_bytes).hexdigest()}")
print(f"下载: {len(dl)} bytes, MD5={hashlib.md5(dl).hexdigest()}")
print("✅ 完全一致" if fpk_bytes == dl else "❌ 不一致")
print(f"\n🎉 完成: https://github.com/{REPO}/releases/tag/{TAG}")
