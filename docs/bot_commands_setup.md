# Telegram 机器人命令设置指南

## 📋 如何设置命令菜单

### 第一步：找到 BotFather

1. 在 Telegram 中搜索 `@BotFather`
2. 打开对话

### 第二步：设置命令

1. 发送: `/setcommands`
2. 选择你的机器人
3. 复制下面的命令列表，直接粘贴发送

---

## 🔮 完整命令列表（直接复制使用）

### 中文版本

```
start - 开始使用运势大师
help - 查看功能列表和使用说明
tarot - 专业塔罗占卜（三张牌）
fortune - 向大师求问前程
luck - 查看今日运势
group_fortune - 查看群今日运势（仅群组）
ranking - 群运势排行榜（仅群组）
pk - 塔罗对决（仅群组，需回复对手消息）
```

### English Version（英文版本）

```
start - Start using Fortune Master
help - View features and usage guide
tarot - Professional tarot reading (3 cards)
fortune - Ask master about your future
luck - Check today's fortune
group_fortune - Check group daily fortune (groups only)
ranking - Group fortune leaderboard (groups only)
pk - Tarot duel (groups only, reply to opponent)
```

---

## 📝 详细说明

### 个人功能命令

| 命令 | 描述（中文） | 描述（English） |
|------|------------|----------------|
| `/start` | 开始使用运势大师 | Start using Fortune Master |
| `/help` | 查看功能列表和使用说明 | View features and usage guide |
| `/tarot [问题]` | 专业塔罗占卜（三张牌） | Professional tarot reading (3 cards) |
| `/fortune [问题]` | 向大师求问前程 | Ask master about your future |
| `/luck` | 查看今日运势 | Check today's fortune |

### 群组功能命令

| 命令 | 描述（中文） | 描述（English） |
|------|------------|----------------|
| `/group_fortune` | 查看群今日运势（仅群组） | Check group daily fortune (groups only) |
| `/ranking` | 群运势排行榜（仅群组） | Group fortune leaderboard (groups only) |
| `/pk` | 塔罗对决（仅群组，需回复对手消息） | Tarot duel (groups only, reply to opponent) |

---

## 🎯 推荐设置方案

### 方案1：简洁版（推荐）

适合不想让命令列表太长的情况：

```
start - 开始使用
help - 查看帮助
tarot - 塔罗占卜
luck - 今日运势
group_fortune - 群运势
ranking - 排行榜
pk - 塔罗对决
```

### 方案2：详细版（完整功能）

包含所有功能：

```
start - 开始使用运势大师
help - 查看功能列表和使用说明
tarot - 专业塔罗占卜（三张牌）
fortune - 向大师求问前程
luck - 查看今日运势
group_fortune - 查看群今日运势（仅群组）
ranking - 群运势排行榜（仅群组）
pk - 塔罗对决（仅群组，需回复对手消息）
```

### 方案3：分场景版

**仅个人聊天可见的命令**：

使用 BotFather 的 `/setcommands` 后，再使用 `/setmyprivatecommands`

```
start - 开始使用
help - 查看帮助
tarot - 塔罗占卜
fortune - 前程问卜
luck - 今日运势
```

**仅群组可见的命令**：

使用 `/setmygroupcommands`

```
help - 查看帮助
tarot - 塔罗占卜
group_fortune - 群运势
ranking - 排行榜
pk - 塔罗对决
```

---

## 🔧 设置步骤详解

### 完整操作流程

1. **打开 BotFather**
   ```
   在 Telegram 搜索: @BotFather
   ```

2. **发送设置命令**
   ```
   /setcommands
   ```

3. **选择机器人**
   - 点击你的机器人名称
   - 或者输入 @your_bot_name

4. **粘贴命令列表**
   - 复制上面的命令列表
   - 直接粘贴发送

5. **确认成功**
   - BotFather 会回复 "Success!"
   - 现在用户输入 / 就能看到命令菜单了

---

## 💡 使用效果

设置完成后，用户在机器人对话框输入 `/` 时，会看到：

```
┌─────────────────────────────┐
│ /start                      │
│ 开始使用运势大师              │
│                             │
│ /help                       │
│ 查看功能列表和使用说明         │
│                             │
│ /tarot                      │
│ 专业塔罗占卜（三张牌）         │
│                             │
│ /luck                       │
│ 查看今日运势                 │
│                             │
│ ... (更多命令)               │
└─────────────────────────────┘
```

---

## 🌟 进阶设置（可选）

### 1. 设置机器人描述

```
/setdescription
```

建议文案：
```
🔮 专业塔罗占卜大师

提供深度塔罗解读、运势预测、群组互动等功能。
支持智能问题识别，针对性建议。

• 个人占卜
• 群日运势
• 排行榜竞赛
• 好友PK对战

让每一天都充满神秘与期待！
```

### 2. 设置关于信息

```
/setabouttext
```

建议文案：
```
专业的 Telegram 运势机器人，提供塔罗占卜、运势预测、群组社交互动等功能。
```

### 3. 设置机器人头像

```
/setuserpic
```

上传一张塔罗牌相关的图片作为头像

---

## 📱 各平台显示效果

### Telegram Desktop（桌面版）
- 命令出现在输入框上方
- 点击即可插入命令

### Telegram Mobile（手机版）
- 输入 / 后弹出命令菜单
- 向上滑动查看所有命令

### Telegram Web
- 与桌面版类似
- 命令列表浮动显示

---

## ❓ 常见问题

### Q1: 命令设置后不显示？

**解决方法**：
1. 重启 Telegram 客户端
2. 清除对话后重新打开
3. 等待几分钟让缓存更新

### Q2: 可以设置不同语言的命令吗？

**答**：可以，使用 `/setlanguage` 为不同语言设置不同的命令列表。

### Q3: 命令太多了，用户看起来很乱？

**答**：
- 使用"简洁版"命令列表
- 只保留最常用的命令
- 在 /help 中提供完整功能说明

### Q4: 如何删除已设置的命令？

**答**：
```
/deletecommands
```
选择你的机器人即可删除所有命令

### Q5: 可以让某些命令只在群组显示吗？

**答**：可以，使用：
- `/setmyprivatecommands` - 仅私聊显示
- `/setmygroupcommands` - 仅群组显示

---

## 🎯 最佳实践建议

### 命令命名原则

1. **简短易记**
   - ✅ `/tarot` 
   - ❌ `/tarot_divination_reading`

2. **语义清晰**
   - ✅ `/ranking` (排行榜)
   - ❌ `/r` (不明确)

3. **避免冲突**
   - 不要使用 Telegram 系统保留命令
   - 如: `/settings`, `/cancel` 等

### 描述撰写原则

1. **简洁明了**（不超过50个字符）
   - ✅ "查看群今日运势"
   - ❌ "查看本群今天的塔罗运势预测和详细分析"

2. **突出价值**
   - ✅ "专业塔罗占卜（三张牌）"
   - ❌ "塔罗"

3. **标注限制**
   - ✅ "塔罗对决（仅群组）"
   - ✅ "需回复对手消息"

---

## 📋 最终推荐配置

### 🏆 推荐使用（平衡版）

```
start - 开始使用
help - 查看帮助
tarot - 塔罗占卜
luck - 今日运势
group_fortune - 群运势（仅群组）
ranking - 排行榜（仅群组）
pk - 对决（回复对手消息）
```

**优点**：
- ✅ 命令数量适中（7个）
- ✅ 描述简洁清晰
- ✅ 功能覆盖完整
- ✅ 用户易于理解

---

## 🚀 立即设置

### 一步到位

1. 打开 Telegram
2. 搜索 `@BotFather`
3. 发送 `/setcommands`
4. 选择你的机器人
5. 复制粘贴下面的内容：

```
start - 开始使用
help - 查看帮助
tarot - 塔罗占卜
luck - 今日运势
group_fortune - 群运势（仅群组）
ranking - 排行榜（仅群组）
pk - 对决（回复对手消息）
```

6. 完成！🎉

---

需要我帮您生成其他语言的命令列表吗？或者调整命令描述的风格？
