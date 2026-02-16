"""
HD 热钱包服务

职责：
- 从助记词派生用户专属 BSC 充值地址（BIP-44）
- 为每个用户分配唯一的派生索引，持久化到 user_wallets 表
- 构造并签名 USDT 归集交易（热钱包 → 冷钱包）
- 管理 Gas 中转钱包（自动为热钱包分发 BNB）

安全说明：
- 助记词存在 .env 环境变量中，不落库
- 子钱包私钥不持久化，每次需要时实时从助记词+index派生
- 冷钱包私钥不接触代码，归集只从热钱包单向转出

地址分配规则：
- index 0~9998：用户热钱包地址
- index 9999：Gas 中转钱包（管理员往这里打 BNB，系统自动分发给热钱包）
"""

import logging
from typing import Optional

from eth_account import Account
from eth_account.signers.local import LocalAccount

from db.database import db
from config import HD_MNEMONIC, BSC_WALLET_ADDRESS, BSC_USDT_CONTRACT

logger = logging.getLogger(__name__)

# 启用 HD 钱包功能（eth-account 要求显式启用）
Account.enable_unaudited_hdwallet_features()

# BSC 链 ID
BSC_CHAIN_ID = 56

# ERC-20 transfer(address,uint256) 函数选择器
ERC20_TRANSFER_SELECTOR = "0xa9059cbb"

# USDT 精度（BSC 上是 18 位）
USDT_DECIMALS = 18

# Gas 中转钱包的固定 index
GAS_WALLET_INDEX = 9999

# 每次分发给热钱包的 BNB 数量（足够归集约 100 次）
GAS_DISTRIBUTE_AMOUNT_WEI = 5_000_000_000_000_000  # 0.005 BNB

# 归集阈值：热钱包 USDT 达到多少才归集（美元）
SWEEP_THRESHOLD_USDT = 5.0


class WalletManager:
    """HD 热钱包管理器"""

    def __init__(self):
        self._mnemonic = HD_MNEMONIC
        self._address_to_user: dict[str, str] = {}

    # ------------------------------------------------------------------
    # HD 派生（内部方法）
    # ------------------------------------------------------------------

    def _derive_account(self, index: int) -> LocalAccount:
        """从助记词派生第 index 个子钱包账户"""
        if not self._mnemonic:
            raise RuntimeError("HD_MNEMONIC 未配置，无法派生钱包")
        return Account.from_mnemonic(
            self._mnemonic,
            account_path=f"m/44'/60'/0'/0/{index}"
        )

    def derive_address(self, index: int) -> str:
        """派生第 index 个地址（不暴露私钥）"""
        return self._derive_account(index).address

    # ------------------------------------------------------------------
    # Gas 中转钱包
    # ------------------------------------------------------------------

    def get_gas_wallet_address(self) -> str:
        """获取 Gas 中转钱包地址（index=9999）"""
        return self.derive_address(GAS_WALLET_INDEX)

    def build_gas_distribute_tx(
        self,
        to_address: str,
        amount_wei: int,
        nonce: int,
        gas_price: int,
    ) -> str:
        """
        构造 Gas 分发交易：Gas 中转钱包 → 热钱包（发送 BNB）
        """
        tx = {
            "to": to_address,
            "value": amount_wei,
            "gas": 21000,  # 标准 BNB 转账
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": BSC_CHAIN_ID,
        }
        acct = self._derive_account(GAS_WALLET_INDEX)
        signed = acct.sign_transaction(tx)
        return signed.raw_transaction.hex()

    # ------------------------------------------------------------------
    # 用户地址分配（并发安全）
    # ------------------------------------------------------------------

    async def get_or_create_wallet(self, user_id: str) -> dict:
        """
        获取或创建用户的专属充值钱包。
        并发安全：INSERT 失败时自动重试查询。
        """
        # 1. 查询已有钱包
        existing = await db.fetch_one(
            "SELECT * FROM user_wallets WHERE user_id = ?",
            (user_id,)
        )
        if existing:
            return dict(existing)

        # 2. 分配新索引（取当前最大 index + 1，跳过 Gas 钱包的 9999）
        for attempt in range(3):
            max_row = await db.fetch_one(
                "SELECT MAX(wallet_index) as max_idx FROM user_wallets WHERE wallet_index < ?",
                (GAS_WALLET_INDEX,)
            )
            next_index = (max_row["max_idx"] or -1) + 1 if max_row else 0

            # 3. 派生地址
            address = self.derive_address(next_index)

            # 4. 尝试持久化（UNIQUE 约束保证并发安全）
            try:
                await db.execute(
                    "INSERT INTO user_wallets (user_id, wallet_index, address) VALUES (?, ?, ?)",
                    (user_id, next_index, address)
                )
                self._address_to_user[address.lower()] = user_id
                logger.info(f"🔑 新钱包创建 | 用户: {user_id} | index: {next_index} | 地址: {address}")
                return {"user_id": user_id, "wallet_index": next_index, "address": address}
            except Exception as e:
                if "UNIQUE" in str(e).upper() and attempt < 2:
                    logger.warning(f"⚠️ index {next_index} 冲突，重试... (attempt {attempt + 1})")
                    # 可能已被另一个请求创建，再查一次
                    existing = await db.fetch_one(
                        "SELECT * FROM user_wallets WHERE user_id = ?", (user_id,)
                    )
                    if existing:
                        return dict(existing)
                    continue
                raise

        raise RuntimeError(f"钱包创建失败：用户 {user_id} 经过 3 次重试仍无法分配 index")

    async def get_user_by_address(self, address: str) -> Optional[str]:
        """通过热钱包地址查找对应的 user_id"""
        addr_lower = address.lower()
        if addr_lower in self._address_to_user:
            return self._address_to_user[addr_lower]
        row = await db.fetch_one(
            "SELECT user_id FROM user_wallets WHERE LOWER(address) = ?",
            (addr_lower,)
        )
        if row:
            self._address_to_user[addr_lower] = row["user_id"]
            return row["user_id"]
        return None

    async def get_wallet_by_user(self, user_id: str) -> Optional[dict]:
        """通过 user_id 查找钱包信息"""
        row = await db.fetch_one(
            "SELECT * FROM user_wallets WHERE user_id = ?", (user_id,)
        )
        return dict(row) if row else None

    async def get_all_addresses(self) -> set[str]:
        """获取所有用户热钱包地址集合（小写，不含 Gas 钱包）"""
        rows = await db.fetch_all(
            "SELECT user_id, address FROM user_wallets WHERE wallet_index < ?",
            (GAS_WALLET_INDEX,)
        )
        addresses = set()
        for row in rows:
            addr = row["address"].lower()
            addresses.add(addr)
            self._address_to_user[addr] = row["user_id"]
        return addresses

    async def load_cache(self):
        """启动时加载所有地址映射到缓存"""
        rows = await db.fetch_all(
            "SELECT user_id, address FROM user_wallets WHERE wallet_index < ?",
            (GAS_WALLET_INDEX,)
        )
        for row in rows:
            self._address_to_user[row["address"].lower()] = row["user_id"]
        if rows:
            logger.info(f"🔑 已加载 {len(rows)} 个热钱包地址到缓存")

        # 打印 Gas 中转钱包地址供管理员打 BNB
        if self._mnemonic:
            gas_addr = self.get_gas_wallet_address()
            logger.info(f"⛽ Gas 中转钱包地址: {gas_addr}")

    # ------------------------------------------------------------------
    # 归集交易构造
    # ------------------------------------------------------------------

    def build_sweep_tx(
        self,
        wallet_index: int,
        usdt_amount_wei: int,
        nonce: int,
        gas_price: int,
    ) -> str:
        """
        构造并签名 USDT 归集交易（热钱包 → 冷钱包）
        """
        if not BSC_WALLET_ADDRESS:
            raise RuntimeError("BSC_WALLET_ADDRESS（冷钱包）未配置")

        to_padded = BSC_WALLET_ADDRESS.lower().replace("0x", "").zfill(64)
        amount_padded = hex(usdt_amount_wei)[2:].zfill(64)
        data = ERC20_TRANSFER_SELECTOR + to_padded + amount_padded

        tx = {
            "to": BSC_USDT_CONTRACT,
            "value": 0,
            "gas": 60000,
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": BSC_CHAIN_ID,
            "data": data,
        }

        acct = self._derive_account(wallet_index)
        signed = acct.sign_transaction(tx)
        return signed.raw_transaction.hex()


# 全局单例
wallet_manager = WalletManager()
