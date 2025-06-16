
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Async start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌐 Open App", web_app=WebAppInfo(url="https://qerion-web.onrender.com"))],
        [InlineKeyboardButton("👥 Join Community", url="https://t.me/QuantumAnimus_Official")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome to Quantum Animus!", reply_markup=markup)

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

# Entry point
if __name__ == "__main__":
    main()
