# Release 产物说明

`ds2api-3.7.0.fpk.b64` 是已构建好的应用包 `ds2api.fpk` 的 **Base64 文本编码**（仓库不直接存放二进制）。

## 解码得到 .fpk

**Linux / macOS**

```bash
base64 -d ds2api-3.7.0.fpk.b64 > ds2api.fpk
# 校验（可选；MD5 因每次构建含时间戳会略有不同，此处为随仓库发布版本）
md5sum ds2api.fpk    # 当前应为 25ec62e0f06a0720c8fc7e53eac55f0e
```

**Windows（PowerShell）**

```powershell
certutil -decode ds2api-3.7.0.fpk.b64 ds2api.fpk
# 校验（可选）
Get-FileHash ds2api.fpk -Algorithm MD5   # 当前应为 25ec62e0f06a0720c8fc7e53eac55f0e
```

## 安装

将解码得到的 `ds2api.fpk` 上传到飞牛设备，在 **应用中心 → 手动安装** 中选择即可。

> 也可点击仓库 **Releases** 页下载未编码的 `ds2api.fpk`（若已发布）。
