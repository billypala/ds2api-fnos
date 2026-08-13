# Release 产物说明

> **当前推荐版本：[v3.7.2](https://github.com/billypala/ds2api-fnos/releases/tag/v3.7.2)（Native 应用，自包含）**
>
> v3.7.0/v3.7.1 均为 Docker 应用方案，**已废弃**——无法在用户环境正常启动。

## v3.7.2（当前推荐，Native 应用）

`ds2api-3.7.2.fpk.b64` 是 Native 应用包，**自包含 Go 静态二进制 + WebUI 静态资源**，无任何 Docker 依赖，离线安装。

**Linux / macOS**

```bash
base64 -d ds2api-3.7.2.fpk.b64 > ds2api.fpk
md5sum ds2api.fpk   # 应为 116be95de53209d9e75458a85ab92502
```

**Windows（PowerShell）**

```powershell
certutil -decode ds2api-3.7.2.fpk.b64 ds2api.fpk
Get-FileHash ds2api.fpk -Algorithm MD5
```

## 安装步骤

1. 解码得到 `ds2api.fpk`（约 11.5MB）
2. 上传到飞牛设备
3. **应用中心 → 手动安装** → 选择 `ds2api.fpk`
4. 向导**必须设置管理台密钥**（≥8 位，妥善保存）
5. 点击桌面「DS2API 管理台」→ 用密钥登录 `/admin`
6. 管理台内配置 DeepSeek 账号与 API Key

## 旧版本（不推荐）

- `ds2api-3.7.1.fpk.b64`：Docker 方案 + init 容器，仍然无法安装（容器名冲突）
- `ds2api-3.7.0.fpk.b64`：Docker 方案，env_file 时序 bug

> 也可点击仓库 **Releases** 页直接下载未编码的 `ds2api.fpk`。
