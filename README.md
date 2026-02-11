# Fortune Master Bot

一个基于 `python-telegram-bot` 的运势机器人，支持：

- `/start`、`/help`
- `/tarot` 三张牌占卜
- `/fortune` 前程问卜
- `/luck` 今日运势

项目已按“开发与上线分离”的实践重构，提供两种运行模式并支持一键切换。

## 目录结构

- `main.py`：程序入口（日志、应用构建、模式启动）
- `config.py`：环境变量读取与配置归一化
- `handlers/`：命令处理逻辑
- `services/`：业务数据与服务（如塔罗牌数据）
- `utils/private_api_bot.py`：私有化 TG API 兼容层

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 配置

复制并编辑环境变量：

```bash
cp .env.example .env
```

核心开关只有一个：

- `RUNTIME_MODE=webhook`：Webhook 模式（推荐线上）
- `RUNTIME_MODE=temporary`：临时模式（Polling，本地开发推荐）

## 运行

```bash
python3 main.py
```

## 模式说明

### 1) temporary（本地开发推荐）

- 机器人使用 Polling，不依赖公网地址
- 可选启用 hello 页面（`HELLO_WORLD_ENABLED=true`）
- 优点：稳定、迭代快，不受 ngrok 地址变化影响

### 2) webhook（联调/线上推荐）

- 机器人启动时自动调用 `setWebhook`
- 需要正确配置：
  - `WEBHOOK_URL`
  - `WEBHOOK_SECRET_TOKEN`（若平台要求）

## 本地联调建议（最佳实践）

日常开发：

1. 用 `RUNTIME_MODE=temporary`
2. 专注调 handler 与业务逻辑

需要验证平台回调链路时：

1. 启动 ngrok 映射 `WEBAPP_PORT`
2. 切换 `RUNTIME_MODE=webhook`
3. 更新 `WEBHOOK_URL` 为当前 ngrok 地址
4. 重启 `python3 main.py`

## 常见问题

### Q: 启动后无回复，日志只有 `No new updates found`

A: 说明机器人进程正常，但没有收到 update。优先检查：

- 是否发消息给了当前 token 对应的机器人
- 是否有其他进程在消费同一 token 的 updates
- webhook/polling 是否混用冲突

### Q: ngrok 地址变化怎么办？

A: 免费版会变化。建议：

- 开发期默认用 `temporary`
- 仅在需要回调联调时切 `webhook`

