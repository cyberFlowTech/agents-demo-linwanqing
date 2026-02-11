import os
from dotenv import load_dotenv

load_dotenv()


def _to_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


# ===== TG 平台切换（快速切换 Telegram / Zapry）=====
# telegram : 使用官方 Telegram API
# zapry    : 使用 Zapry 私有化 TG 服务
TG_PLATFORM = os.getenv("TG_PLATFORM", "telegram").strip().lower()
if TG_PLATFORM not in {"telegram", "zapry"}:
    TG_PLATFORM = "telegram"

# ===== Telegram 基础配置 =====
# 根据平台自动选择对应的配置
if TG_PLATFORM == "zapry":
    BOT_TOKEN = os.getenv("ZAPRY_BOT_TOKEN")
    TELEGRAM_API_BASE_URL = os.getenv("ZAPRY_API_BASE_URL", "https://openapi.mimo.immo/bot").strip()
else:  # telegram
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_API_BASE_URL = ""  # 官方 API 不需要自定义 base_url

# ===== 运行模式（只改这一项）=====
# webhook   : 平台回调到你的服务（推荐线上）
# temporary : 本地临时调试（polling + 可选 hello 页面）
RUNTIME_MODE = os.getenv("RUNTIME_MODE", "webhook").strip().lower()
if RUNTIME_MODE not in {"webhook", "temporary"}:
    RUNTIME_MODE = "webhook"

# ===== Webhook 配置（RUNTIME_MODE=webhook 时生效）=====
# 根据平台自动选择对应的 Webhook URL
if TG_PLATFORM == "zapry":
    WEBHOOK_URL = os.getenv("ZAPRY_WEBHOOK_URL", "").strip()
else:  # telegram
    WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL", "").strip()

WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "").strip()
WEBAPP_HOST = os.getenv("WEBAPP_HOST", "0.0.0.0").strip()
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", "8443"))
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN", "").strip()

# ===== 临时调试页面（hello world）=====
HELLO_WORLD_ENABLED = _to_bool(os.getenv("HELLO_WORLD_ENABLED"), default=False)
HELLO_WORLD_PORT = int(os.getenv("HELLO_WORLD_PORT", "8080"))
HELLO_WORLD_TEXT = os.getenv("HELLO_WORLD_TEXT", "hello world")

# ===== 数据库配置 =====
DATABASE_PATH = os.getenv("DATABASE_PATH", "").strip()  # 为空则使用默认路径 data/elena.db

# ===== 其他配置 =====
DEBUG = _to_bool(os.getenv("DEBUG"), default=False)
LOG_FILE = os.getenv("LOG_FILE", "").strip()

# ===== OpenAI 配置 =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip()  # 如果使用国内中转，填写中转地址
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()  # 默认使用 gpt-4o-mini


def get_current_config_summary() -> str:
    """返回当前配置摘要，方便调试"""
    return f"""
==================== 当前配置 ====================
TG 平台: {TG_PLATFORM.upper()}
Bot Token: {BOT_TOKEN[:20]}... (已隐藏)
API Base URL: {TELEGRAM_API_BASE_URL or '官方API'}
运行模式: {RUNTIME_MODE.upper()}
Webhook URL: {WEBHOOK_URL[:50]}... (已截断) if WEBHOOK_URL else '未配置'
监听端口: {WEBAPP_PORT}
OpenAI Model: {OPENAI_MODEL}
OpenAI Base URL: {OPENAI_BASE_URL or '官方API'}
================================================
"""

