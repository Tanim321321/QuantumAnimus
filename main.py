import os
import time
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)

    # Check if user exists
    url = f"{SUPABASE_URL}/rest/v1/user_data?telegram_id=eq.{telegram_id}"
    r = requests.get(url, headers=headers)

    if r.status_code == 200 and len(r.json()) == 0:
        # Create new user
        data = {
            "telegram_id": telegram_id,
            "points": 0,
            "level": 0,
            "referral_code": telegram_id,
            "referred_by": None,
            "last_claim_time": 0,
            "referral_count": 0
        }
        create = requests.post(f"{SUPABASE_URL}/rest/v1/user_data", headers=headers, json=[data])

    keyboard = [
        [InlineKeyboardButton("🚀 Open App", web_app=InlineKeyboardButton.WebAppInfo(url="https://qerion.vercel.app/"))],
        [InlineKeyboardButton("👥 Join Community", url="https://t.me/airdrop9810")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Qerion ⚡️", reply_markup=reply_markup)

async def claim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    url = f"{SUPABASE_URL}/rest/v1/user_data?telegram_id=eq.{telegram_id}"
    r = requests.get(url, headers=headers)

    if r.status_code != 200 or not r.json():
        await update.message.reply_text("User not found. Please send /start first.")
        return

    user = r.json()[0]
    last_claim = int(user.get("last_claim_time", 0))
    now = int(time.time() * 1000)
    three_hours = 3 * 60 * 60 * 1000

    if now - last_claim < three_hours:
        mins = int((three_hours - (now - last_claim)) / 60000)
        await update.message.reply_text(f"⏳ Please wait {mins} more minutes before claiming again.")
        return

    new_points = user.get("points", 0) + 100
    update_data = {
        "points": new_points,
        "last_claim_time": now
    }

    update_req = requests.patch(
        f"{SUPABASE_URL}/rest/v1/user_data?telegram_id=eq.{telegram_id}",
        headers=headers,
        json=update_data
    )

    if update_req.status_code == 204:
        await update.message.reply_text(f"✅ Claimed 100 points! Total: {new_points} ⚡️")
    else:
        await update.message.reply_text("❌ Failed to update your claim. Try again.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("claim", claim))

    app.run_polling()
