import random
from telegram import Update
from telegram.ext import ContextTypes

# Simple random responses for the "Master" persona
MASTER_RESPONSES = [
    "贫道掐指一算，此事虽有波折，但终将柳暗花明。",
    "施主莫急，时机未到，静待花开。",
    "此乃天机，不可泄露... 但贫道暗示你：向东行有贵人。",
    "吉兆已现，放手去做吧。",
    "今日不宜操之过急，退一步海阔天空。",
    "心诚则灵，施主若有疑虑，不妨明日再问。",
    "卦象显示：大吉大利，百无禁忌！",
    "施主印堂发亮，必有喜事将近。",
    "凡事随缘，莫强求。",
    "贫道看你骨骼精奇，定是虽然大器晚成，但前途无量。",
]

async def fortune_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a fortune telling response."""
    user_name = update.effective_user.first_name
    question = ' '.join(context.args)

    if not question:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"施主 {user_name}，请问您想问什么？\nUsage: /fortune [您的疑问]"
        )
        return

    # TODO: Add LLM integration here
    response = random.choice(MASTER_RESPONSES)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"🤔 **关于「{question}」...**\n\n🔮 {response}",
        parse_mode='Markdown'
    )
