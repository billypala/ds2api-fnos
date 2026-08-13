# DS2API for 飞牛 OS（fnOS）

![DS2API](assets/icon.svg)

将 **DeepSeek Web 对话**转换为 **OpenAI / Claude / Gemini / Ollama 兼容 API** 的自托管网关，打包为飞牛 fnOS 原生应用包（`.fpk`），可直接在 fnOS 应用中心安装运行。

- 上游项目：[ouqiting/ds2api](https://github.com/ouqiting/ds2api) v3.7.0
- 应用形态：Docker 应用（`docker-compose.yaml` 编排，host 网络）
- 许可证：[AGPL-3.0](LICENSE)

## 功能特性

| 能力 | 说明 |
|---|---|
| 多协议兼容 | OpenAI（`/v1/*`）、Claude（`/anthropic/v1/*`）、Gemini（`/v1beta/*`）、Ollama（`/api/*`） |
| 多账号轮询 | DeepSeek 托管账号自动轮询、token 自动刷新、并发队列控制 |
| 流式输出 | SSE 流式响应，高性能 |
| WebUI 管理台 | 桌面图标直达 `/admin`，配置账号 / API Key / 代理 / 会话管理 |
| 代理桥 | Mihomo 一号一 IP（可选），自动测速与故障转移 |
| fnOS 原生集成 | 应用中心启停、安装向导、数据持久化、卸载数据保留 |

## 快速安装

1. **获取 `.fpk`**：
   - 方式 A：直接下载 `release/ds2api-3.7.1.fpk.b64`（Base64 文本，见 [release 说明](release/README.md) 解码）
   - 方式 B：点击上方 **Releases** 页下载 `ds2api.fpk`（推荐 v3.7.1）
   - 方式 C：自行构建（见下节）
2. 将 `.fpk` 上传到飞牛设备（scp / 文件管理器均可）。
3. 打开 **fnOS 应用中心 → 手动安装** → 选择 `ds2api.fpk`。
4. 安装向导**必须设置管理台密钥**（≥8 位，妥善保存）。
5. 点击桌面 **DS2API 管理台** 图标，用密钥登录 `/admin`。

> 首次启动会拉取镜像 `ouqiting/ds2api:latest`，视网络 1–3 分钟。国内网络慢时可先为 Docker 配置镜像加速器。

## 从源码构建

```bash
# Linux / macOS
./build.sh

# Windows (PowerShell)
.\build.ps1
```

或手动：

```bash
# 1. 下载 fnOS 打包工具 fnpack（或手动放置到 tools/）
bash scripts/fetch-fnpack.sh

# 2. 生成应用图标（ICON.PNG / ICON_256.PNG / ui images，需 Python + Pillow）
python scripts/gen_icons.py

# 3. 打包
./tools/fnpack build --directory app
# 产物: ds2api.fpk
```

仓库已内置 GitHub Actions（`.github/workflows/build-fpk.yml`），打 `v*` tag 即自动构建并发布到 Releases。

## 仓库结构

```text
.
├── app/                        # fnOS 应用包源目录（fnpack build --directory app）
│   ├── manifest                # 应用清单（appname/version/service_port/...）
│   ├── cmd/                    # 生命周期脚本（main / install_callback / ...）
│   ├── config/                 # privilege + resource（docker-project 声明）
│   ├── wizard/install          # 安装向导（管理台密钥）
│   ├── ICON.PNG / ICON_256.PNG # 应用图标（构建时生成）
│   └── app/
│       ├── docker/             # docker-compose.yaml + config.example.json
│       └── ui/                 # 桌面入口配置 + 图标
├── scripts/                    # gen_icons.py / fetch-fnpack.sh(.ps1)
├── assets/icon.svg             # 项目图标（矢量）
├── release/                    # 已构建产物（Base64 文本）
├── docs/移植说明.md             # 移植方案与设计决策
├── build.sh / build.ps1        # 一键构建
└── .github/workflows/          # CI：自动构建 + Release 发布
```

## 运行机制

- **网络模式**：`network_mode: host`（官方 compose 强制要求）。代理桥 Mihomo 一号一 IP 的 SOCKS5 监听需直落宿主机，bridge 模式会导致 `Connection Refused`。
- **数据持久化**（`/vol{n}/@appdata/ds2api/`）：
  - `config.json` → 容器内 `/data/config.json`（DeepSeek 账号 / API Key / token）
  - `data/` → 容器内 `/app/data/`（WebUI 调用记录等）
  - `.env` → 管理密钥 `DS2API_ADMIN_KEY`
- **首次启动**：`cmd/install_callback` 从包内 `config.example.json` 复制生成 `config.json`，登录管理台后配置真实账号。
- **状态管理**：`cmd/main` 通过 `docker inspect ds2api` 判断容器运行状态。

## 镜像说明

- 默认镜像：`ouqiting/ds2api:latest`（Docker Hub）。
- 上游 Dockerfile 支持 `amd64` / `arm64` 多架构构建；x86_64 设备可直接使用。
- **ARM 设备**：若官方镜像无 arm64 变体，请自行 `docker buildx` 构建多架构镜像并修改 `app/app/docker/docker-compose.yaml` 的 `image:` 字段后重新打包。

## 合规声明

- 本项目基于上游 [ouqiting/ds2api](https://github.com/ouqiting/ds2api)（AGPL-3.0）二次封装，保留上游许可证与致谢。
- ds2api 通过逆向方式调用 DeepSeek Web 对话，仅供学习、研究、个人实验与内部验证使用，**不提供商业授权或稳定性保证**；请勿用于违反服务条款、法律法规或平台规则的场景。
- 使用风险由使用者自行承担。

## 致谢

- [ouqiting/ds2api](https://github.com/ouqiting/ds2api) / [CJackHwang/ds2api](https://github.com/CJackHwang/ds2api) —— 上游项目
- 飞牛 OS 应用开放平台：[developer.fnnas.com](https://developer.fnnas.com)
