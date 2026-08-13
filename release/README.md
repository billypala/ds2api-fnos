# Release 产物说明

> **当前推荐版本：[v3.7.1](https://github.com/billypala/ds2api-fnos/releases/tag/v3.7.1)**
> 修复了 v3.7.0 安装时 `env file ... .env not found` 的问题（详见 [docs/移植说明.md](../docs/移植说明.md)）。

## v3.7.1（推荐）

`ds2api-3.7.1.fpk.b64` 是修复版的 Base64 编码，下载后解码即可安装。

**Linux / macOS**

```bash
base64 -d ds2api-3.7.1.fpk.b64 > ds2api.fpk
# MD5 校验：当前应为 98d24e02308a058786abe6337a88ef0b（时间戳可能微变）
md5sum ds2api.fpk
```

**Windows（PowerShell）**

```powershell
certutil -decode ds2api-3.7.1.fpk.b64 ds2api.fpk
Get-FileHash ds2api.fpk -Algorithm MD5
```

## v3.7.0（历史版本，不推荐）

`ds2api-3.7.0.fpk.b64` 是首发版本，存在安装时序 bug，请使用 v3.7.1。

## 安装步骤

1. 解码得到 `ds2api.fpk`
2. 将其上传到飞牛设备
3. **应用中心 → 手动安装** → 选择 `ds2api.fpk`
4. 安装向导中**设置管理台密钥**（必填，≥8 位）
5. 点击桌面「DS2API 管理台」图标，用密钥登录 `/admin`

> 也可点击仓库 **Releases** 页下载未编码的 `ds2api.fpk`。
