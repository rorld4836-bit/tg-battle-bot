import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

waiting_player = None
active_battle = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Uchastvovat", callback_data="join")]
    ]
    await update.message.reply_text(
        "Dobro pozhalovat v bitvy!\nNazhmi knopku nizhe 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_player, active_battle

    query = update.callback_query
    user = query.from_user
    await query.answer()

    username = user.username or f"id{user.id}"

    if query.data == "join":
        if waiting_player is None:
            waiting_player = username
            await query.edit_message_text(
                f"⏳ Ozhidanie sopernika...\nTy: @{username}"
            )
        else:
            active_battle = (waiting_player, username)
            waiting_player = None

            await query.edit_message_text(
                "⚔️ Bitva nachalas!\n\n"
                f"@{active_battle[0]} VS @{active_battle[1]}\n\n"
                "⏰ Raund 1 — 10 chasov"
            )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()


if __name__ == "__main__":
    main()
