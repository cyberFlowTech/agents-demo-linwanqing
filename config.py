import os
from dotenv import load_dotenv

load_dotenv()


def _to_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


# ===== Telegram 基础配置 =====
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# 私有化 TG 服务时填写，必须以 /bot 结尾；留空则使用官方 API
TELEGRAM_API_BASE_URL = os.getenv("TELEGRAM_API_BASE_URL", "").strip()

# ===== 运行模式（只改这一项）=====
# webhook   : 平台回调到你的服务（推荐线上）
# temporary : 本地临时调试（polling + 可选 hello 页面）
RUNTIME_MODE = os.getenv("RUNTIME_MODE", "webhook").strip().lower()
if RUNTIME_MODE not in {"webhook", "temporary"}:
    RUNTIME_MODE = "webhook"

# ===== Webhook 配置（RUNTIME_MODE=webhook 时生效）=====
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "").strip()
WEBAPP_HOST = os.getenv("WEBAPP_HOST", "0.0.0.0").strip()
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", "8443"))
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN", "").strip()

# ===== 临时调试页面（hello world）=====
HELLO_WORLD_ENABLED = _to_bool(os.getenv("HELLO_WORLD_ENABLED"), default=False)
HELLO_WORLD_PORT = int(os.getenv("HELLO_WORLD_PORT", "8080"))
HELLO_WORLD_TEXT = os.getenv("HELLO_WORLD_TEXT", "hello world")

# ===== 其他配置 =====
DEBUG = _to_bool(os.getenv("DEBUG"), default=False)
LOG_FILE = os.getenv("LOG_FILE", "").strip()
