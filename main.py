from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Get the BOT token from Render's Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌐 Open App", web_app=WebAppInfo(url="https://quantumanimus.onrender.com"))],
        [InlineKeyboardButton("👥 Join Community", url="https://t.me/QuantumAnimus_Official")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome to Quantum Animus!", reply_markup=reply_markup)

# Start the bot
def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN is missing. Please set it in Render's environment variables.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

# Entry point
if __name__ == "__main__":
    main()
