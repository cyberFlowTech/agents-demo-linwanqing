# Fortune Master Bot (运势大师)

一个专业的 Telegram 运势机器人，提供**大师级塔罗占卜**和**群组社交互动**功能。

## ✨ 核心特色

### 🔮 专业塔罗占卜
- **三张牌阵**：过去-现在-未来完整解读
- **深度分析**：每张牌都有专业的深层解读
- **智能识别**：自动识别问题类型（事业/爱情/财运/健康/学业）
- **针对性建议**：根据问题类型给出具体指导
- **22张大阿卡纳**：完整收录塔罗最重要的22张牌
- **精简/详细切换**：默认精简版，点击查看完整解读

### 👥 群组社交玩法（MVP已上线！）
- **🌅 群日运势播报**：每个群每天独特的运势，增加群凝聚力
- **🏆 群运势排行榜**：实时排名，激发竞争心理
- **⚔️ 塔罗PK对战**：好友1v1对决，比拼牌面能量
- **📊 战绩统计**：记录胜负，显示胜率

## 🎮 功能列表

### 个人功能
- `/start` - 开始使用
- `/help` - 查看帮助
- `/tarot [问题]` - 专业塔罗占卜（三张牌）
- `/fortune [问题]` - 前程问卜
- `/luck` - 今日运势

### 群组功能（🆕 MVP）
- `/group_fortune` - 查看群今日运势
- `/ranking` - 群运势排行榜（自动统计）
- `/pk` - 塔罗对决（回复对手消息）

**群组特色**：
- 在群里使用 `/tarot` 占卜，结果会**自动加入排行榜**
- 每天看看谁的运势最好，激发互动
- 和好友PK，围观效应带动参与

## 🚀 快速开始

### 目录结构

- `main.py`：程序入口（日志、应用构建、模式启动）
- `config.py`：环境变量读取与配置归一化
- `handlers/`：命令处理逻辑
- `services/`：业务数据与服务（如塔罗牌数据）
- `utils/private_api_bot.py`：私有化 TG API 兼容层
- `docs/`：功能文档

### 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 配置

复制并编辑环境变量：

```bash
cp .env.example .env
```

#### 核心配置项

**1. 平台切换（TG_PLATFORM）**
```bash
# telegram - 使用官方 Telegram API
# zapry    - 使用 Zapry 私有化服务
TG_PLATFORM=telegram
```

**2. 运行模式（RUNTIME_MODE）**
```bash
# webhook   - Webhook 模式（推荐线上）
# temporary - 临时模式（Polling，本地开发推荐）
RUNTIME_MODE=webhook
```

只需修改这两个配置，其他相关配置会自动切换！

### 运行

```bash
python3 main.py
```

## 📖 模式说明

### 1) temporary（本地开发推荐）

- 机器人使用 Polling，不依赖公网地址
- 可选启用 hello 页面（`HELLO_WORLD_ENABLED=true`）
- 优点：稳定、迭代快，不受 ngrok 地址变化影响

### 2) webhook（联调/线上推荐）

- 机器人启动时自动调用 `setWebhook`
- 需要正确配置：
  - `WEBHOOK_URL`（Telegram官方）或 `ZAPRY_WEBHOOK_URL`（Zapry）
  - `WEBHOOK_SECRET_TOKEN`（若平台要求）

## 🛠️ 平台切换

### 快速切换 Telegram / Zapry

**方法1：手动修改 .env**
```bash
# 切换到 Zapry
TG_PLATFORM=zapry

# 切换回 Telegram
TG_PLATFORM=telegram
```

**方法2：使用切换脚本**
```bash
# 切换到 Zapry（webhook 模式）
./scripts/switch_platform.sh zapry webhook

# 切换到 Telegram（临时模式）
./scripts/switch_platform.sh telegram temporary
```

## 💡 本地联调建议（最佳实践）

日常开发：

1. 用 `RUNTIME_MODE=temporary`
2. 专注调 handler 与业务逻辑

需要验证平台回调链路时：

1. 启动 ngrok 映射 `WEBAPP_PORT`
2. 切换 `RUNTIME_MODE=webhook`
3. 更新 `WEBHOOK_URL` 为当前 ngrok 地址
4. 重启 `python3 main.py`

## ❓ 常见问题

### Q: 启动后无回复，日志只有 `No new updates found`

A: 说明机器人进程正常，但没有收到 update。优先检查：

- 是否发消息给了当前 token 对应的机器人
- 是否有其他进程在消费同一 token 的 updates
- webhook/polling 是否混用冲突

### Q: ngrok 地址变化怎么办？

A: 免费版会变化。建议：

- 开发期默认用 `temporary`
- 仅在需要回调联调时切 `webhook`

### Q: 如何在 Telegram 和 Zapry 之间切换？

A: 只需修改 `.env` 中的 `TG_PLATFORM` 配置：
- `TG_PLATFORM=telegram` - 使用官方 Telegram
- `TG_PLATFORM=zapry` - 使用 Zapry 私有化服务

其他相关配置（Bot Token、API 地址、Webhook URL）会自动切换。

## 📝 开发说明

### 项目结构

```
fortune_master/
├── main.py                 # 程序入口
├── config.py              # 配置管理
├── handlers/              # 命令处理器
│   ├── tarot.py          # 塔罗占卜
│   ├── fortune.py        # 前程问卜
│   ├── luck.py           # 今日运势
│   └── group.py          # 群组功能（🆕）
├── services/             # 业务逻辑
│   ├── tarot_data.py    # 塔罗牌数据
│   └── group_manager.py # 群组数据管理（🆕）
├── utils/               # 工具类
│   └── private_api_bot.py
├── data/                # 数据存储（🆕）
│   ├── groups.json      # 群运势
│   ├── rankings.json    # 排行榜
│   └── pk_records.json  # PK记录
├── docs/                # 文档
│   ├── tarot_guide.md
│   ├── interaction_flow.md
│   └── mvp_features.md  # MVP功能说明（🆕）
└── tests/               # 测试脚本
```

### 添加新的塔罗牌

编辑 `services/tarot_data.py`，在 `MAJOR_ARCANA` 列表中添加新牌：

```python
{
    "name": "牌名",
    "meaning_upright": "正位简要牌意",
    "meaning_reversed": "逆位简要牌意",
    "deep_meaning_upright": "正位详细解读（大师级）",
    "deep_meaning_reversed": "逆位详细解读（大师级）"
}
```

### 自定义问题类别

在 `services/tarot_data.py` 的 `_get_question_category` 方法中添加新类别关键词。

### 数据管理

所有群组数据存储在 `data/` 目录的 JSON 文件中：
- 简单可靠，易于备份
- 无需额外数据库服务
- 适合中小规模应用

如需扩展到大规模，可以迁移到 Redis 或 PostgreSQL。

## 🎯 MVP 功能详解

完整的群组社交化功能已实现！详见：
- [MVP 功能文档](docs/mvp_features.md)
- [交互流程说明](docs/interaction_flow.md)
- [快速开始指南](MVP_DONE.md)

## 📄 许可

MIT License
