"""
私有化 Telegram API 兼容层。

部分私有化 API 服务返回的 User 对象格式与官方 API 不同，
导致 python-telegram-bot 解析失败。此模块提供兼容的 Bot 类。
"""
from telegram import User
from telegram.ext import ExtBot

# User 类接受的参数字段
_USER_FIELDS = {"id", "first_name", "is_bot", "last_name", "username", "language_code",
                "can_join_groups", "can_read_all_group_messages", "supports_inline_queries",
                "is_premium", "added_to_attachment_menu", "api_kwargs"}

# 私有 API 可能使用的字段名映射
_FIELD_ALIASES = {
    "bot_id": "id",
    "user_id": "id",
    "name": "first_name",
}


def _normalize_user_data(data: dict) -> dict:
    """
    将私有 API 返回的 User 格式转换为标准格式。
    处理：嵌套的 user 对象、字段名映射、移除多余字段（如 token）
    """
    if not isinstance(data, dict):
        return data
    data = dict(data)
    # 若 result 为 {"user": {...}, "token": "..."} 等嵌套结构，提取 user
    if "user" in data and isinstance(data["user"], dict):
        data = data["user"].copy()
    # 字段名映射
    for old_key, new_key in _FIELD_ALIASES.items():
        if old_key in data and new_key not in data:
            data[new_key] = data.pop(old_key)
    # getMe 返回的必为 bot，补全 is_bot
    if "is_bot" not in data:
        data["is_bot"] = True
    # 移除 User 不接受的字段（token 等），保留 User 接受的字段
    return {k: v for k, v in data.items() if k in _USER_FIELDS}


class PrivateAPIExtBot(ExtBot):
    """
    兼容私有化 Telegram API 的 ExtBot。

    当私有 API 返回 `name` 而非 `first_name` 时，自动转换以兼容标准库。
    """

    async def get_me(
        self,
        *,
        read_timeout=None,
        write_timeout=None,
        connect_timeout=None,
        pool_timeout=None,
        api_kwargs=None,
    ):
        """覆盖 get_me，在解析前规范化 User 数据。"""
        result = await self._post(
            "getMe",
            read_timeout=read_timeout,
            write_timeout=write_timeout,
            connect_timeout=connect_timeout,
            pool_timeout=pool_timeout,
            api_kwargs=api_kwargs,
        )
        result = _normalize_user_data(result)
        self._bot_user = User.de_json(result, self)
        return self._bot_user
