# DS2API for 飞牛 OS（fnOS）

![DS2API](assets/icon.svg)

将 **DeepSeek Web 对话**转换为 **OpenAI / Claude / Gemini / Ollama 兼容 API** 的自托管网关，打包为飞牛 fnOS 原生应用包（`.fpk`），可直接在 fnOS 应用中心安装运行。

- 上游项目：[ouqiting/ds2api](https://github.com/ouqiting/ds2api) v3.7.0
- 应用形态：**Native 应用**（自包含 Go 静态二进制 linux/amd64 + WebUI 静态资源，**零 Docker 依赖**）
- 包大小：~11.5 MB（gzip 压缩后；解压含 27.6 MB 静态二进制）
- 许可证：[AGPL-3.0](LICENSE)

## 功能特性

| 能力 | 说明 |
|---|---|
| **自包含** | 单个 `.fpk` 含完整 Go 运行时与 WebUI，**离线安装、零 Docker 依赖** |
| 多协议兼容 | OpenAI（`/v1/*`）、Claude（`/anthropic/v1/*`）、Gemini（`/v1beta/*`）、Ollama（`/api/*`） |
| 多账号轮询 | DeepSeek 托管账号自动轮询、token 自动刷新、并发队列控制 |
| 流式输出 | SSE 流式响应，高性能 |
| WebUI 管理台 | 桌面图标直达 `/admin`，配置账号 / API Key / 代理 / 会话管理 |
| 代理桥 | Mihomo 一号一 IP（可选），自动测速与故障转移 |
| fnOS 原生集成 | 应用中心启停、安装向导、数据持久化、卸载数据保留 |

## 快速安装

> **当前版本：v3.7.0.1**（Native 应用，自包含 Go 静态二进制，离线可装）——**待测试**

1. **获取 `.fpk`**：
   - 方式 A：直接下载 `release/ds2api-3.7.0.1.fpk.b64`（Base64 文本，见 [release 说明](release/README.md) 解码）
   - 方式 B：点击上方 **Releases** 页下载 `ds2api-3.7.0.1.fpk`（发布后可用）
   - 方式 C：自行构建（见下节）
2. 将 `.fpk` 上传到飞牛设备（scp / 文件管理器均可）。
3. 打开 **fnOS 应用中心 → 手动安装** → 选择 `ds2api.fpk`。
4. 安装向导**必须设置管理台密钥**（≥8 位，妥善保存）。
5. 点击桌面 **DS2API 管理台** 图标，用密钥登录 `/admin`。

> 首次启动无需拉取镜像（已内嵌），瞬时启动。

## 版本号规范

`v<上游版本>.<我们的修订号>`，例如 `v3.7.0.1` 表示基于 [ds2api v3.7.0](https://github.com/ouqiting/ds2api/releases/tag/v3.7.0) 的首次修订。后续上游小版本（如 v3.7.1）发布时，我们对应发 `v3.7.1.0`。

## 从源码构建

前置依赖：Python 3 + Pillow（生成图标）、fnpack（fnOS 打包工具，自动下载）。

```bash
# Linux / macOS
./build.sh

# Windows (PowerShell)
.\build.ps1
```

构建脚本自动完成：下载 fnpack → 生成应用图标 → `fnpack build --directory app`。

或手动：

```bash
bash scripts/fetch-fnpack.sh        # 下载 fnpack 工具
python scripts/gen_icons.py          # 生成 ICON.PNG / ICON_256.PNG
./tools/fnpack build --directory app # 产物: ds2api.fpk
```

构建要求：上游 `ds2api` 静态二进制必须存在于 `app/app/ds2api`。从上游 release 下载 `ds2api_v3.7.0_linux_amd64.tar.gz` 解压取得。

仓库已内置 GitHub Actions（`.github/workflows/build-fpk.yml`），打 `v*` tag 自动构建并发布。

## 仓库结构

```text
.
├── app/                        # fnOS 应用包源目录（fnpack build --directory app）
│   ├── manifest                # 应用清单（platform=x86 / service_port=5001）
│   ├── cmd/                    # 生命周期脚本（main 启停二进制 / install_callback 初始化）
│   ├── config/                 # privilege + resource（data-share 声明）
│   ├── wizard/install          # 安装向导（必填管理台密钥）
│   ├── ICON.PNG / ICON_256.PNG # 应用图标（构建时生成）
│   └── app/
│       ├── ds2api              # Go 静态二进制（linux/amd64，27.6 MB）
│       ├── config.example.json # 配置模板
│       ├── static/admin/       # WebUI 静态资源（22 文件）
│       └── ui/                 # 桌面入口配置 + 图标
├── scripts/                    # gen_icons.py / fetch-fnpack / publish_release
├── assets/icon.svg             # 项目图标（矢量）
├── release/                    # 已构建产物（Base64 文本）
├── docs/移植说明.md             # 移植方案与设计决策
├── build.sh / build.ps1        # 一键构建
└── .github/workflows/          # CI：自动构建 + Release 发布
```

## 运行机制

- **数据持久化**（`/vol{n}/@appdata/ds2api/`）：
  - `config.json` —— DeepSeek 账号 / API Key / token 持久化
  - `app.log` —— 应用运行日志
  - `app.pid` —— 进程 PID 文件（cmd/main 维护）
- **首次启动**：`cmd/install_callback` 从包内 `app/config.example.json` 复制生成 `config.json`。
- **进程管理**：`cmd/main` 通过 `nohup` 启动 ds2api，记录 PID；stop 时先 TERM 超时后 KILL。
- **环境变量**：`PORT`、`DS2API_ADMIN_KEY`、`DS2API_CONFIG_PATH`、`DS2API_STATIC_ADMIN_DIR` 全部通过 `cmd/main` 注入。
- **管理密钥**：`DS2API_ADMIN_KEY` 来源于 wizard `ds2api_admin_key` 必填字段，由 fnOS 作为环境变量提供给生命周期脚本。

## 合规声明

- 本项目基于上游 [ouqiting/ds2api](https://github.com/ouqiting/ds2api)（AGPL-3.0）二次封装，保留上游许可证与致谢。
- ds2api 通过逆向方式调用 DeepSeek Web 对话，仅供学习、研究、个人实验与内部验证使用，**不提供商业授权或稳定性保证**；请勿用于违反服务条款、法律法规或平台规则的场景。
- 使用风险由使用者自行承担。

## 致谢

- [ouqiting/ds2api](https://github.com/ouqiting/ds2api) / [CJackHwang/ds2api](https://github.com/CJackHwang/ds2api) —— 上游项目
- 飞牛 OS 应用开放平台：[developer.fnnas.com](https://developer.fnnas.com)
