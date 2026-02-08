import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Временное хранилище (потом можно БД)
waiting_player = None
active_battle = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Участвовать", callback_data="join")]
    ]
    await update.message.reply_text(
        "Добро пожаловать в битвы!\nНажми кнопку ниже 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_player, active_battle
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if query.data == "join":
        if waiting_player is None:
            waiting_player = user.username
            await query.edit_message_text(
                f"⏳ Ожидание соперника...\nТы: @{user.username}"
            )
        else:
            active_battle = (waiting_player, user.username)
            waiting_player = None

            text = (
                "⚔️ БИТВЫ!\n\n"
                "Раунд 1 ⚡\n\n"
                f"@{active_battle[0]} VS @{active_battle[1]}\n\n"
                "Приглашённые:\n"
                f"@{active_battle[0]}: 0\n"
                f"@{active_battle[1]}: 0\n\n"
                "⏰ Время раунда: 10 часов"
            )

            await query.edit_message_text(text)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
