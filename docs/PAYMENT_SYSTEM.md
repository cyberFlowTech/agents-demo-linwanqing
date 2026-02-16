# USDT 支付系统技术方案

> Fortune Master — 林晚晴塔罗牌解读师
>
> 最后更新：2026-02-16

---

## 一、系统概览

基于 BSC 链上 USDT (BEP-20) 的完整支付系统，采用 HD 热钱包架构，实现用户充值、余额管理、付费功能解锁、自动归集的全流程。

### 核心架构

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    用户       │     │   Bot 服务    │     │   BSC 链     │
│              │     │              │     │              │
│  /recharge   │────>│  生成专属地址  │     │              │
│              │<────│  展示给用户    │     │              │
│              │     │              │     │              │
│  链上转 USDT │─────────────────────────>│  热钱包到账   │
│              │     │              │     │              │
│              │     │  RPC 轮询     │<────│  Transfer 事件│
│              │<────│  到账通知      │     │              │
│              │     │              │     │              │
│              │     │  Gas 分发     │────>│  BNB → 热钱包│
│              │     │  USDT 归集   │────>│  USDT → 冷钱包│
└──────────────┘     └──────────────┘     └──────────────┘
```

### 资金流向

```
用户钱包
    │
    │ USDT (任意金额)
    ▼
用户专属热钱包 (HD 派生, 每人不同)
    │
    │ 余额 >= 5 USDT 时自动归集
    ▼
冷钱包 (BSC_WALLET_ADDRESS)
    │
    │ 管理员手动提现
    ▼
运营账户
```

---

## 二、HD 热钱包体系

### 2.1 派生原理

使用 BIP-44 标准，从一个助记词（12 个英文单词）派生无限个子钱包地址。

```
助记词 (HD_MNEMONIC)
    │
    │  BIP-39 → 种子 (Seed)
    │  BIP-44 路径: m/44'/60'/0'/0/{index}
    │
    ├── index 0    → 0xBcC792...  (用户 A 的充值地址)
    ├── index 1    → 0x7A3f...    (用户 B 的充值地址)
    ├── index 2    → 0xE91b...    (用户 C 的充值地址)
    ├── ...
    ├── index 9998 → 0x...        (最多支持 9999 个用户)
    └── index 9999 → 0xC600...    (Gas 中转钱包, 固定用途)
```

**关键特性**：同一助记词 + 同一 index = 永远得到相同的私钥和地址。因此私钥不需要存储，任何时候可以重新算出。

### 2.2 地址分配规则

| Index 范围 | 用途 | 说明 |
|-----------|------|------|
| 0 ~ 9998 | 用户热钱包 | 每个用户分配一个唯一 index |
| 9999 | Gas 中转钱包 | 管理员往这里打 BNB，系统自动分发 |

### 2.3 并发安全

用户首次充值时分配地址，采用乐观锁机制：

```python
for attempt in range(3):
    next_index = SELECT MAX(wallet_index) + 1
    try:
        INSERT INTO user_wallets (user_id, wallet_index, address)
        # 成功 → 返回
    except UNIQUE_CONSTRAINT:
        # 冲突 → 重试
```

数据库 `UNIQUE(wallet_index)` 和 `UNIQUE(address)` 约束保证绝对不会分配重复地址。

---

## 三、充值流程

### 3.1 用户发起充值

```
用户发送 /recharge 或点击"去充值"按钮
    │
    ▼
查询/创建用户专属钱包 (get_or_create_wallet)
    │
    ▼
展示专属充值地址 + BSC 链 USDT 提示
    │
    ▼
用户在自己的钱包 App 中转账 USDT 到该地址
```

### 3.2 链上监听

系统每 30 秒通过 BSC 公共 RPC 节点查询 USDT 合约的 Transfer 事件：

```python
# eth_getLogs 查询 USDT Transfer 事件
filter = {
    "fromBlock": last_checked_block,
    "toBlock": "latest",
    "address": "0x55d398326f99059fF775485246999027B3197955",  # USDT 合约
    "topics": [TRANSFER_EVENT_TOPIC]
}
```

**RPC 节点**（免费，无需 API Key）：
- https://bsc-dataseed.binance.org (主)
- https://bsc-dataseed1.defibit.io (备)
- https://bsc-dataseed1.ninicoin.io (备)
- https://bsc.publicnode.com (备)

自动轮转：如果主节点返回错误，自动切换到下一个。

### 3.3 到账确认

```
检测到 Transfer 事件
    │
    │  to_address 在热钱包地址集合中？
    │
    ├── 否 → 忽略（不是转给我们的）
    │
    └── 是 → to_address 直接映射到 user_id（零碰撞）
              │
              ├── 增加用户余额
              ├── 创建/更新充值订单记录
              ├── 发送到账通知给用户
              └── 触发归集流程
```

**零碰撞优势**：每个用户地址不同，无需靠金额匹配，任何金额都能准确识别归属。

### 3.4 到账通知

```
嘿，你的充值到啦~ 🎉

这次到账 10.00 USDT，你现在的余额是 10.00 USDT 💎

现在你可以：
• 解锁塔罗深度解读，看更完整的牌面故事
• 不限次数地占卜和聊天

有什么想问的，随时找我~

— 晚晴 🌿
```

---

## 四、自动归集

### 4.1 归集条件

| 条件 | 值 | 说明 |
|------|---|------|
| USDT 阈值 | >= 5 USDT | 小额等累积，减少链上交易 |
| BNB Gas | >= 0.000006 BNB | 约 ¥0.004，一次归集的 Gas 费 |

### 4.2 Gas 中转钱包

```
问题：归集 USDT 是一笔链上交易，需要 BNB 付 Gas
      但新创建的热钱包里没有 BNB

解决：Gas 中转钱包 (index=9999)
      管理员打 BNB 到这个固定地址
      系统检测到热钱包 BNB 不足时，自动从 Gas 钱包分发
```

**Gas 分发流程**：

```
检测到热钱包 BNB 不足
    │
    ▼
检查 Gas 中转钱包余额
    │
    ├── 不足 → 日志告警，等管理员打 BNB
    │
    └── 足够 → 构造 BNB 转账交易
              │  from: Gas 钱包 (index=9999)
              │  to:   热钱包 (index=N)
              │  amount: 0.005 BNB
              │
              ▼
         广播交易 → 等待 6 秒到账 → 继续归集
```

**Gas 消耗估算**：

| 操作 | Gas 消耗 | BNB 费用(~3 gwei) |
|------|---------|-------------------|
| 分发 BNB (21000 gas) | ~¥0.003 | 0.000063 BNB |
| 归集 USDT (60000 gas) | ~¥0.009 | 0.000180 BNB |
| 一次完整归集 | — | ~0.000243 BNB |

**0.005 BNB 够归集约 20 次**，0.05 BNB 够归集约 200 次。

### 4.3 归集交易构造

```python
# ERC-20 transfer(address to, uint256 amount)
tx = {
    "to": USDT_CONTRACT,           # USDT 合约地址
    "value": 0,                    # 不发 BNB
    "gas": 60000,                  # ERC-20 transfer 预估
    "gasPrice": current_gas_price, # 当前链上 Gas 价格
    "chainId": 56,                 # BSC 主网
    "data": "0xa9059cbb" + to_address_padded + amount_padded
}

# 用热钱包的 HD 派生私钥签名
signed_tx = hot_wallet_private_key.sign(tx)

# 通过 RPC 广播
eth_sendRawTransaction(signed_tx)
```

---

## 五、付费功能与配额

### 5.1 免费额度（每日刷新）

| 功能 | 免费次数 | 配置项 |
|------|---------|--------|
| 塔罗占卜 (/tarot) | 1 次/天 | FREE_TAROT_DAILY |
| AI 对话 | 10 次/天 | FREE_CHAT_DAILY |
| 今日运势 (/luck) | 无限 | — |
| 快速求问 (/fortune) | 无限 | — |
| 占卜历史 (/history) | 无限 | — |

### 5.2 付费定价

| 功能 | 单价 | 配置项 |
|------|------|--------|
| 深度解读 | 0.5 USDT | PRICE_TAROT_DETAIL |
| 超额塔罗占卜 | 0.3 USDT | PRICE_TAROT_READING |
| 超额 AI 对话 | 0.1 USDT | PRICE_AI_CHAT |

### 5.3 配额检查流程

```
用户触发付费功能
    │
    ▼
检查今日免费次数 (daily_usage 表)
    │
    ├── 有免费额度 → 计数+1 → 允许使用
    │
    └── 免费用完 → 检查余额 (user_balances 表)
                    │
                    ├── 余额充足 → 扣费 → 记录消费 → 允许使用
                    │
                    └── 余额不足 → 提示充值 + 显示"去充值"按钮
```

---

## 六、数据库表结构

### 6.1 用户钱包 (user_wallets)

```sql
CREATE TABLE user_wallets (
    user_id      TEXT PRIMARY KEY,
    wallet_index INTEGER UNIQUE NOT NULL,  -- HD 派生索引
    address      TEXT UNIQUE NOT NULL,     -- BSC 地址
    created_at   TEXT DEFAULT (datetime('now', 'localtime'))
);
```

### 6.2 用户余额 (user_balances)

```sql
CREATE TABLE user_balances (
    user_id         TEXT PRIMARY KEY,
    balance         REAL DEFAULT 0.0,
    total_recharged REAL DEFAULT 0.0,
    total_spent     REAL DEFAULT 0.0,
    updated_at      TEXT DEFAULT (datetime('now', 'localtime'))
);
```

### 6.3 充值订单 (recharge_orders)

```sql
CREATE TABLE recharge_orders (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         TEXT NOT NULL,
    order_id        TEXT UNIQUE NOT NULL,
    amount          REAL NOT NULL,
    deposit_address TEXT,                -- 用户的热钱包地址
    status          TEXT DEFAULT 'pending',  -- pending/confirmed/swept/expired
    tx_hash         TEXT,                -- 充值交易哈希
    sweep_tx_hash   TEXT,                -- 归集交易哈希
    from_address    TEXT,                -- 充值来源地址
    created_at      TEXT,
    confirmed_at    TEXT,
    expired_at      TEXT
);
```

### 6.4 消费记录 (spend_records)

```sql
CREATE TABLE spend_records (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    TEXT NOT NULL,
    feature    TEXT NOT NULL,    -- 'tarot_detail' / 'ai_chat' / 'tarot_reading'
    amount     REAL NOT NULL,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);
```

### 6.5 每日用量 (daily_usage)

```sql
CREATE TABLE daily_usage (
    user_id    TEXT NOT NULL,
    usage_date TEXT NOT NULL,    -- YYYY-MM-DD
    tarot_count INTEGER DEFAULT 0,
    chat_count  INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, usage_date)
);
```

---

## 七、安全设计

### 7.1 密钥管理

| 密钥 | 存储位置 | 接触代码 | 风险评估 |
|------|---------|---------|---------|
| HD 助记词 | .env 环境变量 | wallet.py (运行时) | 泄露=所有热钱包丢失 |
| 热钱包私钥 | 不存储（实时派生） | 签名时短暂存在于内存 | 低 |
| 冷钱包私钥 | 不接触代码 | 无 | 零风险 |
| Gas 钱包私钥 | 不存储（实时派生） | 分发 Gas 时短暂存在 | 低 |

### 7.2 资金安全

```
热钱包被盗的最大损失 = 未归集的 USDT 总额

实际风险很低，因为：
1. 归集阈值 5 USDT，达到就自动归集
2. 归集后热钱包余额为 0
3. 小额充值（<5U）即使被盗损失也极小
```

### 7.3 防御措施

| 措施 | 说明 |
|------|------|
| .gitignore 包含 .env | 助记词不会提交到代码仓库 |
| 私钥不落库 | 数据库只存地址和 index |
| 日志不打印私钥 | 只打印地址前几位 |
| tx_hash 去重 | 同一笔交易不会重复确认 |
| 订单过期机制 | pending 订单 1 小时后自动过期 |
| UNIQUE 约束 | 防止 index 重复分配 |

---

## 八、运维指南

### 8.1 环境变量

```env
# 冷钱包地址（归集目标）
BSC_WALLET_ADDRESS=0xYourColdWalletAddress

# HD 助记词（极其重要！务必保密！）
HD_MNEMONIC=word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12

# 定价
PRICE_TAROT_DETAIL=0.5
PRICE_TAROT_READING=0.3
PRICE_AI_CHAT=0.1

# 免费额度
FREE_TAROT_DAILY=1
FREE_CHAT_DAILY=10

# 管理员（可执行 /topup 手动充值）
ADMIN_USER_IDS=548348
```

### 8.2 日常运维

**查看 Gas 中转钱包地址**（启动日志）：
```
⛽ Gas 中转钱包地址: 0xC60044fec91BD86EBb2ff7D9ce697D397c4f6277
```

**往 Gas 钱包打 BNB**：
- 地址：启动日志中的 Gas 中转钱包地址
- 链：BSC (BNB Smart Chain)
- 金额：0.05 BNB（够用几个月）
- 低于 0.01 BNB 时日志会告警

**手动给用户充值**：
```
/topup 用户ID 金额
```
例如：`/topup 548348 10`（给用户 548348 充 10 USDT）

### 8.3 监控告警

查看支付相关日志：
```bash
sudo journalctl -u fortune-master | grep -E '充值|归集|Gas|⛽|sweep|BNB'
```

关键日志含义：

| 日志 | 含义 |
|------|------|
| `✅ 热钱包到账` | 用户充值成功 |
| `✅ 归集成功` | USDT 已转入冷钱包 |
| `💰 暂不归集` | 金额 < 5U，等累积 |
| `⛽ Gas 分发成功` | 自动给热钱包打了 BNB |
| `⚠️ Gas 中转钱包余额不足` | 需要管理员打 BNB |
| `⚠️ HD_MNEMONIC 未配置` | .env 缺少助记词 |

---

## 九、代码文件索引

| 文件 | 职责 |
|------|------|
| `services/wallet.py` | HD 钱包派生、地址分配、Gas 钱包管理、归集签名 |
| `services/payment.py` | 余额管理、充值确认、消费扣费、订单管理 |
| `services/chain_monitor.py` | BSC 链上监听、到账检测、自动归集、Gas 分发 |
| `services/quota.py` | 配额检查、免费额度追踪、付费扣费逻辑 |
| `handlers/payment.py` | /recharge、/balance、/topup 命令处理 |
| `config.py` | 支付相关环境变量加载 |
| `db/database.py` | 支付相关表定义 |

---

## 十、FAQ

**Q: 用户不走 /recharge 直接转账到热钱包，能到账吗？**
A: 能。系统通过 to_address 匹配用户，不依赖订单。会自动创建一条 confirmed 状态的订单。

**Q: 用户充值后多久到账？**
A: 链上确认后 30 秒内（一个轮询周期）。BSC 出块约 3 秒，所以总延迟约 30 秒。

**Q: 助记词丢了怎么办？**
A: 无法恢复热钱包中未归集的资金。用户余额（记录在数据库中）不受影响。

**Q: 可以支持其他链吗？**
A: 当前只支持 BSC。扩展到 Ethereum、Polygon 等链需要修改合约地址、chainId 和 RPC 节点。

**Q: 用户量上限是多少？**
A: 热钱包 index 范围 0~9998，支持 9999 个用户同时充值。可通过修改 GAS_WALLET_INDEX 扩展。
