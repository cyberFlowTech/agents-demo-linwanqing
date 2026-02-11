# 林晚晴长期记忆系统设计文档

**设计时间**: 2026-02-12  
**目标**: 让林晚晴拥有长期记忆，记住每个用户的核心信息

---

## 🎯 系统目标

### 核心需求
用户希望林晚晴能够：
- 记住用户的基本信息（年龄、职业、性格等）
- 记住用户的生活背景（关系状态、困扰、目标等）
- 在对话中自然引用这些信息
- 信息持久化，Bot重启后不丢失

### 示例场景
```
第1次对话：
用户: 我今年19岁，刚上大学...
Elena: 19岁正是充满可能性的年纪...

[几天后]

第10次对话：
用户: 我最近很焦虑
Elena: 19岁的年纪面对焦虑很正常。记得你之前说过刚上大学，
      是学业压力还是人际关系的困扰？
```

---

## 🏗️ 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────┐
│                    用户发送消息                      │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│          handlers/chat.py (对话处理)                │
│  1. 记录对话到临时缓冲区                            │
│  2. 判断是否需要触发记忆提取                        │
└─────────────────┬───────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌─────────────┐    ┌─────────────────────────────┐
│  直接回复   │    │  触发记忆提取               │
│  (使用AI)   │    │  services/memory_extractor  │
└─────────────┘    └──────────┬──────────────────┘
                              │
                              ▼
                   ┌────────────────────────┐
                   │  AI分析对话内容        │
                   │  提取关键信息：        │
                   │  - 基本信息            │
                   │  - 性格特征            │
                   │  - 生活背景            │
                   │  - 关注点              │
                   └──────────┬─────────────┘
                              │
                              ▼
                   ┌────────────────────────┐
                   │  更新用户档案          │
                   │  services/user_memory  │
                   │  ↓                     │
                   │  保存到文件/数据库     │
                   └────────────────────────┘
                              
┌─────────────────────────────────────────────────────┐
│          下次对话时                                  │
│  1. 加载用户档案 (user_memory)                      │
│  2. 加载塔罗历史 (tarot_history)                    │
│  3. 加载对话历史 (conversation_history)             │
│  4. 合并为完整上下文传递给AI                        │
└─────────────────────────────────────────────────────┘
```

---

## 💾 数据结构设计

### 用户档案 (UserMemory)

```json
{
  "user_id": "123456789",
  "user_name": "小明",
  "created_at": "2026-02-10 14:30",
  "last_updated": "2026-02-12 16:45",
  "conversation_count": 25,
  
  "basic_info": {
    "age": 19,
    "gender": "男",
    "location": "上海",
    "occupation": "大学生",
    "school": "复旦大学",
    "major": "计算机"
  },
  
  "personality": {
    "traits": ["内向", "敏感", "理性"],
    "values": ["重视友情", "追求自我成长"],
    "communication_style": "温和、谨慎"
  },
  
  "life_context": {
    "relationships": {
      "romantic": "单身，前段时间刚分手",
      "family": "父母关系和睦，有一个姐姐",
      "friends": "朋友不多，但关系很深"
    },
    "concerns": [
      "担心未来职业发展",
      "学业压力大",
      "社交焦虑"
    ],
    "goals": [
      "想考研",
      "希望提升社交能力",
      "想找到人生方向"
    ],
    "recent_events": [
      "刚分手一个月",
      "期末考试压力大",
      "在考虑是否要考研"
    ]
  },
  
  "interests": ["编程", "阅读", "音乐"],
  
  "tarot_summary": {
    "total_readings": 5,
    "common_topics": ["感情", "学业", "职业"],
    "last_reading": {
      "date": "2026-02-12",
      "question": "我应该考研吗",
      "brief": "牌面显示有挑战但趋势积极"
    }
  },
  
  "conversation_summary": "用户是一个19岁的大学生，性格内向敏感。最近刚分手，正在经历学业压力和对未来的迷茫。主要关注感情、学业和自我成长。",
  
  "meta": {
    "memory_extraction_count": 5,
    "last_extraction": "2026-02-12 16:45",
    "extraction_trigger": "每5条对话提取一次"
  }
}
```

---

## 🔧 核心模块设计

### 1. UserMemory Manager (`services/user_memory.py`)

**职责**：
- 管理用户档案的加载、保存、更新
- 提供档案查询接口
- 处理数据持久化

**核心方法**：
```python
class UserMemoryManager:
    def get_user_memory(user_id: str) -> dict
    def update_user_memory(user_id: str, updates: dict) -> None
    def create_user_memory(user_id: str, user_name: str) -> dict
    def format_memory_for_ai(memory: dict) -> str
```

### 2. Memory Extractor (`services/memory_extractor.py`)

**职责**：
- 从对话中提取关键信息
- 使用AI分析对话内容
- 生成结构化的用户信息

**核心方法**：
```python
class MemoryExtractor:
    async def extract_from_conversations(
        conversations: list, 
        current_memory: dict
    ) -> dict
    
    async def should_trigger_extraction(
        user_id: str,
        conversation_count: int
    ) -> bool
```

### 3. Conversation Buffer (`services/conversation_buffer.py`)

**职责**：
- 临时存储未提取记忆的对话
- 管理触发提取的逻辑

**核心方法**：
```python
class ConversationBuffer:
    def add_message(user_id: str, role: str, content: str)
    def get_pending_conversations(user_id: str) -> list
    def clear_buffer(user_id: str)
    def should_extract(user_id: str) -> bool
```

---

## ⚙️ API 使用优化策略

### 问题分析
记忆提取需要额外的API调用，需要优化：

### 优化策略

#### 1. 批量提取，而非实时提取
```
❌ 每条消息都提取 → 成本高
✅ 每5条消息提取一次 → 成本降低80%
```

#### 2. 使用更便宜的模型提取记忆
```
对话回复: 使用 GPT-4 (高质量)
记忆提取: 使用 GPT-3.5-turbo (便宜60%)
```

#### 3. 增量更新，而非全量重写
```
只更新变化的信息，不重写整个档案
```

#### 4. 智能触发机制
```python
# 触发条件（满足任一即触发）：
1. 每5条新对话
2. 用户提到重要的个人信息（关键词检测）
3. 距离上次提取超过24小时
4. 用户明确更新信息（如："我今年20岁了"）
```

#### 5. 提取prompt优化
```python
# 使用精简的prompt，减少token消耗
MEMORY_EXTRACTION_PROMPT = """
分析以下对话，提取用户的关键信息（仅提取明确提到的）：
1. 基本信息（年龄、职业、位置）
2. 性格特征
3. 当前困扰/目标
4. 重要事件

输出JSON格式。
"""
```

### API 成本估算

**假设**：
- 对话回复：每条 800 tokens (GPT-4: $0.06/1K input)
- 记忆提取：每次 1500 tokens (GPT-3.5: $0.001/1K input)

**用户对话100条的成本**：
- 对话回复：100 × 800 × 0.00006 = $4.8
- 记忆提取：20次 × 1500 × 0.000001 = $0.03

**记忆提取仅占总成本的 0.6%** ✅

---

## 📂 文件结构

```
fortune_master/
├── services/
│   ├── user_memory.py          # 用户记忆管理器
│   ├── memory_extractor.py     # 记忆提取器
│   └── conversation_buffer.py  # 对话缓冲区
│
├── data/
│   └── user_memories/          # 用户档案存储
│       ├── 123456789.json      # 用户1的档案
│       ├── 987654321.json      # 用户2的档案
│       └── ...
│
├── config.py                   # 配置（增加记忆相关配置）
└── handlers/
    └── chat.py                 # 集成记忆系统
```

---

## 🔄 工作流程

### 完整流程

```
1. 用户发送消息
   ↓
2. 添加到对话缓冲区 (conversation_buffer)
   ↓
3. 判断是否需要提取记忆？
   - No → 直接回复，结束
   - Yes → 继续
   ↓
4. 调用 memory_extractor 提取记忆
   - 获取最近的对话（5-10条）
   - 调用 AI 分析提取关键信息
   ↓
5. 更新用户档案 (user_memory)
   - 合并新信息到现有档案
   - 保存到文件
   ↓
6. 清空对话缓冲区
   ↓
7. 使用更新后的档案回复用户
```

### 对话时的上下文构建

```python
# AI 接收的完整上下文
context = {
    "system_prompt": ELENA_SYSTEM_PROMPT,
    "user_memory": """
        【用户档案】
        姓名: 小明 (19岁，男)
        职业: 复旦大学计算机系学生
        性格: 内向、敏感、理性
        当前困扰: 刚分手，学业压力大，担心未来
        ...
    """,
    "tarot_history": "...",  # 已有功能
    "conversation_history": [...]  # 已有功能
}
```

---

## 🛡️ 隐私与安全

### 数据保护
1. **本地存储**：用户档案保存在本地，不上传第三方
2. **加密选项**：敏感信息可以加密存储
3. **访问控制**：只有用户本人能访问自己的档案
4. **数据清除**：提供命令让用户清除自己的档案

### 用户控制
```
/memory - 查看我的档案
/forget - 清除我的档案
/memory_off - 关闭记忆功能
/memory_on - 开启记忆功能
```

---

## 📈 实现阶段

### Phase 1: 基础框架（核心功能）
- ✅ UserMemoryManager - 档案管理
- ✅ 文件存储系统
- ✅ 基本的记忆格式化和加载

### Phase 2: 记忆提取（AI驱动）
- ✅ MemoryExtractor - AI提取关键信息
- ✅ ConversationBuffer - 对话缓冲
- ✅ 智能触发机制

### Phase 3: 集成与优化
- ✅ 集成到现有对话流程
- ✅ API使用量优化
- ✅ 用户命令（查看/清除档案）

### Phase 4: 增强功能（可选）
- 🔲 数据库存储（SQLite）
- 🔲 档案导出功能
- 🔲 记忆分析和可视化
- 🔲 多维度记忆（短期/长期）

---

## 🎯 成功指标

### 功能指标
- ✅ 记忆准确率：>90%
- ✅ 记忆召回率：能引用80%以上的关键信息
- ✅ 延迟：记忆提取不影响正常对话速度

### 成本指标
- ✅ API成本增加：<5%
- ✅ 存储空间：每用户 <50KB

### 用户体验
- ✅ 对话更连贯、更有温度
- ✅ Elena真的"认识"用户
- ✅ 用户感受到被记住、被理解

---

## 🚀 开始实现

接下来我会按照Phase 1 → Phase 2 → Phase 3 的顺序实现整个系统。
