# Release 产物说明

> **当前版本（待测试）：v3.7.0.1** — Native 应用，自包含 Go 静态二进制
>
> 命名规范：`v<上游版本>.<我们的修订号>`，便于追溯上游版本。本版本基于 [ds2api v3.7.0](https://github.com/ouqiting/ds2api/releases/tag/v3.7.0)。

## v3.7.0.1（待测试）

`ds2api-3.7.0.1.fpk.b64` 是修复路径 bug 与版本号显示的 Native 应用包。

**相对上一版的修复**：
- 修正 `cmd/install_callback` 与 `cmd/main` 中错误的 `${TRIM_APPDEST}/app/...` 路径
  - 正确路径：`${TRIM_APPDEST}/config.example.json`、`${TRIM_APPDEST}/ds2api`、`${TRIM_APPDEST}/static/admin`
  - 原因：fnpack 打包后，`app.tgz` 内部路径已**剥掉 `app/` 前缀**平铺到 target 下
- **自编译 Go 二进制并注入 `BuildVersion=v3.7.0.1`**：之前用上游预编译包导致管理台显示 `v3.7.0`（上游 ldflags 硬编码），现在管理台会正确显示我们开发的版本号

**关于示例账号**：管理台默认出现 3 个账号 `+12345678901` / `example2@example.com` / `example1@example.com` + 2 个 API Key `your-api-key-1/2`，**是上游 [config.example.json](https://github.com/ouqiting/ds2api/blob/v3.7.0/config.example.json) 模板预置的测试占位账号**（邮箱 `example.com` 是 RFC 2606 保留测试域名，密码 `your-password-*` 是占位文本，**无法真实登录 DeepSeek**）。首次安装后请在管理台删除这 3 个示例账号，再添加你自己的 DeepSeek 账号与 API Key。

**Linux / macOS**

```bash
base64 -d ds2api-3.7.0.1.fpk.b64 > ds2api.fpk
md5sum ds2api.fpk   # 应为 2e72a388916383940eb5ba9181f27644
```

**Windows（PowerShell）**

```powershell
certutil -decode ds2api-3.7.0.1.fpk.b64 ds2api.fpk
Get-FileHash ds2api.fpk -Algorithm MD5
```

## 安装步骤

1. 解码得到 `ds2api.fpk`（11,449,963 字节 / 约 11.5 MB）
2. 上传到飞牛设备
3. **应用中心 → 手动安装** → 选择 `ds2api.fpk`
4. 向导**必须设置管理台密钥**（≥8 位，妥善保存）
5. 点击桌面「DS2API 管理台」→ 用密钥登录 `/admin`
6. 管理台内配置 DeepSeek 账号与 API Key

## 命名约定

| 字段 | 当前 | 说明 |
|---|---|---|
| 上游版本 | v3.7.0 | [ds2api v3.7.0 release](https://github.com/ouqiting/ds2api/releases/tag/v3.7.0) |
| 我们的修订号 | .1 | 首次移植修订 |
| 完整 tag | v3.7.0.1 | GitHub Release tag |
| manifest.version | 3.7.0.1 | fnOS 应用中心显示版本 |

后续上游升级到 v3.7.1 时，我们发布 v3.7.1.0；上游 v3.8.0 时，我们发布 v3.8.0.0，以此类推。

## 历史版本（已废）

- `ds2api-3.7.2.fpk.b64`：路径错误
- `ds2api-3.7.1.fpk.b64`：Docker 方案 + init 容器
- `ds2api-3.7.0.fpk.b64`：Docker 方案，env_file 时序 bug
