import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from logging.handlers import RotatingFileHandler
from telegram import Update
from telegram.error import NetworkError
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    TypeHandler,
)

from config import (
    BOT_TOKEN,
    DEBUG,
    HELLO_WORLD_ENABLED,
    HELLO_WORLD_PORT,
    HELLO_WORLD_TEXT,
    LOG_FILE,
    RUNTIME_MODE,
    TELEGRAM_API_BASE_URL,
    WEBAPP_HOST,
    WEBAPP_PORT,
    WEBHOOK_PATH,
    WEBHOOK_SECRET_TOKEN,
    WEBHOOK_URL,
)
from utils.private_api_bot import PrivateAPIExtBot


def setup_logging() -> logging.Logger:
    """统一初始化日志：终端 + 可选文件。"""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level = logging.DEBUG if DEBUG else logging.INFO

    logging.basicConfig(level=log_level, format=log_format, force=True)
    for name in ("httpx", "httpcore"):
        logging.getLogger(name).setLevel(logging.WARNING)

    if LOG_FILE:
        log_dir = os.path.dirname(LOG_FILE)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(file_handler)

    logger = logging.getLogger(__name__)
    if LOG_FILE:
        logger.info("日志已写入文件: %s", LOG_FILE)
    return logger


logger = setup_logging()


def start_hello_world_server(port: int, text: str) -> ThreadingHTTPServer:
    """启动最小 HTTP 服务，用于验证公网连通。"""

    class HelloHandler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            body = text.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):  # noqa: A003
            return

    server = ThreadingHTTPServer(("0.0.0.0", port), HelloHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


async def log_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """记录用户对机器人输入的信息（仅日志，不阻断后续处理）"""
    user = update.effective_user
    user_info = f"{user.first_name}(id:{user.id})" if user else "未知用户"
    chat_id = update.effective_chat.id if update.effective_chat else "?"

    if update.message and update.message.text:
        text = update.message.text.strip()
        logger.info("[用户输入] chat_id=%s 用户=%s 内容=%s", chat_id, user_info, text)
    elif update.callback_query:
        data = update.callback_query.data or ""
        logger.info("[用户输入] chat_id=%s 用户=%s 回调=%s", chat_id, user_info, data)
    elif update.inline_query and update.inline_query.query:
        logger.info("[用户输入] 用户=%s 内联查询=%s", user_info, update.inline_query.query.strip())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message."""
    user = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"施主 {user}，贫道有礼了。\n\n每日一卦，趋吉避凶。\n输入 /help 查看贫道能为您做什么。"
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 API 错误，避免刷屏"""
    err = context.error
    if isinstance(err, NetworkError) and "provider not found" in str(err):
        logger.warning("私有 API 返回 provider 错误，请检查 mimo.immo 后台配置: %s", err)
    else:
        logger.exception("处理更新时出错: %s", err)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a help message."""
    help_text = """
    贫道不仅通晓塔罗，亦略懂天机。

    /start - 拜见贫道
    /tarot [问题] - 塔罗占卜（抽取三张牌）
    /fortune [问题] - 向贫道求问前程
    /luck - 测测今日运势
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


def build_application() -> Application:
    if not BOT_TOKEN:
        logger.error("No BOT_TOKEN found! Please set TELEGRAM_BOT_TOKEN in .env file.")
        exit(1)

    if TELEGRAM_API_BASE_URL:
        bot = PrivateAPIExtBot(
            token=BOT_TOKEN,
            base_url=TELEGRAM_API_BASE_URL,
            base_file_url=TELEGRAM_API_BASE_URL.replace("/bot", "/file/bot"),
        )
        builder = ApplicationBuilder().bot(bot)
    else:
        builder = ApplicationBuilder().token(BOT_TOKEN)
    application = builder.build()
    from handlers.tarot import tarot_command, tarot_callback_handler, tarot_again_callback
    from handlers.fortune import fortune_command
    from handlers.luck import luck_command

    application.add_handler(TypeHandler(Update, log_user_input), group=-1)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tarot", tarot_command))
    application.add_handler(CallbackQueryHandler(tarot_callback_handler, pattern="^draw_tarot$"))
    application.add_handler(CallbackQueryHandler(tarot_again_callback, pattern="^tarot_again$"))
    application.add_handler(CommandHandler("fortune", fortune_command))
    application.add_handler(CommandHandler("luck", luck_command))

    application.add_error_handler(error_handler)
    return application


def run_application(application: Application) -> None:
    should_start_hello = HELLO_WORLD_ENABLED or RUNTIME_MODE == "temporary"
    if should_start_hello:
        try:
            start_hello_world_server(HELLO_WORLD_PORT, HELLO_WORLD_TEXT)
            logger.info("Hello 页面已启动: http://127.0.0.1:%s/", HELLO_WORLD_PORT)
        except OSError as exc:
            logger.warning("Hello 页面启动失败（端口 %s 可能被占用）: %s", HELLO_WORLD_PORT, exc)

    if RUNTIME_MODE == "webhook":
        if not WEBHOOK_URL:
            logger.error("RUNTIME_MODE=webhook 但 WEBHOOK_URL 为空，请在 .env 中配置后重试。")
            exit(1)
        if should_start_hello and HELLO_WORLD_PORT == WEBAPP_PORT:
            logger.warning(
                "HELLO_WORLD_PORT 与 WEBAPP_PORT 相同，Webhook 模式下 hello 页面将启动失败，请使用不同端口。"
            )
        webhook_full_url = WEBHOOK_URL.rstrip("/") + ("/" + WEBHOOK_PATH.strip("/") if WEBHOOK_PATH else "")
        logger.info("Webhook 模式: %s", webhook_full_url)
        print("Fortune Master Bot is starting (Webhook mode)...")
        application.run_webhook(
            listen=WEBAPP_HOST,
            port=WEBAPP_PORT,
            url_path=WEBHOOK_PATH.strip("/") if WEBHOOK_PATH else "",
            webhook_url=webhook_full_url,
            secret_token=WEBHOOK_SECRET_TOKEN or None,
        )
    else:
        print("Fortune Master Bot is starting (Temporary mode: Polling + optional hello page)...")
        application.run_polling()


def main() -> None:
    application = build_application()
    run_application(application)


if __name__ == "__main__":
    main()
