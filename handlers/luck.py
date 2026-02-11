import random
from telegram import Update
from telegram.ext import ContextTypes
import datetime

async def luck_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a daily luck score."""
    user = update.effective_user
    # Use user ID and date as seed for consistent daily luck
    today = datetime.date.today().isoformat()
    seed_val = f"{user.id}-{today}"
    random.seed(seed_val)
    
    score = random.randint(0, 100)
    
    # Reset seed to random
    random.seed()

    comment = ""
    if score >= 90:
        comment = "大吉！诸事皆宜，福星高照！"
    elif score >= 75:
        comment = "吉！运势不错，适合进取。"
    elif score >= 60:
        comment = "中平。平平淡淡才是真。"
    elif score >= 40:
        comment = "小凶。谨言慎行，通过努力可化解。"
    else:
        comment = "大凶... 咳咳，今日宜宅，不宜远行，多行善事。"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"🍀 **{user.first_name} 今日运势** 🍀\n\n"
             f"📊 **幸运指数**: {score}/100\n"
             f"📝 **大师点评**: {comment}",
        parse_mode='Markdown'
    )
