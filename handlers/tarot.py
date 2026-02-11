from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import asyncio
from services.tarot_data import TarotDeck

tarot_deck = TarotDeck()

async def tarot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /tarot command.
    Usage: /tarot [Question]
    """
    if not context.args:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🔮 请告诉我你想占卜的具体问题。\n例如：`/tarot 我应该换工作吗？`",
            parse_mode='Markdown'
        )
        return

    question = ' '.join(context.args)
    if len(question) > 200:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🔮 问题太长了，请精简到 200 字以内。"
        )
        return

    # Store question in user_data for later retrieval in callback
    context.user_data['tarot_question'] = question

    keyboard = [
        [InlineKeyboardButton("🎴 抽牌", callback_data='draw_tarot')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"🔮 问题已收到：**{question}**\n\n请在心中默念你的问题。\n当你准备好时，点击下方按钮抽取三张塔罗牌。",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def tarot_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the 'draw_tarot' callback."""
    query = update.callback_query
    await query.answer()

    if query.data != 'draw_tarot':
        return

    question = context.user_data.get('tarot_question', '未指定问题')
    
    # Shuffling animation
    shuffling_states = [
        "🔮 洗牌中...",
        "🔮 洗牌中.. .",
        "🔮 洗牌中. . .",
        "🎴 抽取中..."
    ]

    for state in shuffling_states:
        await query.edit_message_text(text=state)
        await asyncio.sleep(0.8)

    # Perform Draw
    spread = tarot_deck.get_three_card_spread()
    
    # Generate Interpretation
    interpretation = tarot_deck.generate_spread_interpretation(spread, question)
    
    # Format Result
    result_text = (
        f"🔮 **问题**：{question}\n\n"
        f"🃏 **你抽到的牌是**：\n"
        f"1️⃣ 过去：{spread[0]['name_full']}\n"
        f"2️⃣ 现在：{spread[1]['name_full']}\n"
        f"3️⃣ 未来：{spread[2]['name_full']}\n\n"
        f"{interpretation}"
    )

    # Buttons for next actions
    keyboard = [
        [InlineKeyboardButton("🔁 再抽一次", callback_data='tarot_again')],
        #[InlineKeyboardButton("📜 查看详细解读", callback_data='tarot_detail')], # Placeholder
        #[InlineKeyboardButton("🌙 今日运势", callback_data='tarot_luck')] # Placeholder
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=result_text, reply_markup=reply_markup, parse_mode='Markdown')

async def tarot_again_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resets the state to ask for a new question."""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
         text="🔮 请重新输入 `/tarot [问题]` 开启新的占卜。",
         parse_mode='Markdown'
    )
