"""
Zapry 平台全局兼容配置
统一管理所有 Zapry 特性和兼容性处理
"""
from config import TG_PLATFORM

# 是否使用 Zapry 平台
IS_ZAPRY = (TG_PLATFORM == "zapry")

# Zapry 平台限制和特性
ZAPRY_LIMITATIONS = {
    "supports_markdown": False,          # 不支持 Markdown 格式
    "supports_edit_message": False,      # 不支持 editMessageText
    "supports_answer_callback": False,   # answerCallbackQuery 需要 chat_id
    "user_missing_fields": ["is_bot", "first_name"],  # User 对象缺失字段
    "chat_wrong_id": True,               # Chat.id 在私聊中是 bot 用户名
    "chat_missing_type": True,           # Chat.type 可能为空
    "message_missing_entities": True,    # Message 缺少 entities
    "id_fields_are_strings": True,      # 所有 ID 都是字符串
}


def should_use_markdown() -> bool:
    """是否应该使用 Markdown 格式"""
    if IS_ZAPRY:
        return False
    return True


def should_edit_message() -> bool:
    """是否应该编辑消息（否则发送新消息）"""
    if IS_ZAPRY:
        return False
    return True


def get_parse_mode() -> str:
    """获取应该使用的 parse_mode"""
    if IS_ZAPRY:
        return None  # Zapry 不支持
    return 'Markdown'


def clean_markdown(text: str) -> str:
    """
    清理文本中的 Markdown 标记
    Zapry 平台不支持 Markdown 渲染，AI 回复中的 **加粗** 等标记
    会原样显示给用户，所以需要去除。
    """
    import re
    # **加粗** → 加粗
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # __加粗__ → 加粗
    text = re.sub(r'__(.+?)__', r'\1', text)
    # *斜体* → 斜体（避免误伤 ** 中的 *）
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', text)
    # _斜体_ → 斜体
    text = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'\1', text)
    # `代码` → 代码
    text = re.sub(r'`(.+?)`', r'\1', text)
    # ### 标题 → 标题
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    return text
