import os
import random
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Environment Variable တွေ ရယူ
GEMINI_API_KEY = os.getenv("AIzaSyBTthKBzd5cJUiey1AJLBAIbY3z2rLGQUs")
TELEGRAM_BOT_TOKEN = os.getenv("8188050582:AAFAKpa1Qq9yTPv8omQgcWsHlBUKyEPf0-Y")

# Gemini API Configure
genai.configure(api_key=GEMINI_API_KEY)

def generate_fake_code():
    parts = ["".join(random.choices("0123456789", k=4)) for _ in range(4)]
    return "-".join(parts)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 မင်္ဂလာပါ။ ဖုန်းမော်ဒယ် (ဥပမာ iPhone 12) ပို့လိုက်ပါ၊ AI က PUBG Sensitivity ကို ပေးပါမယ်။"
    )

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_model = update.message.text.strip()

    if len(phone_model) < 3:
        await update.message.reply_text("❌ ဖုန်းမော်ဒယ် မဟုတ်ပါ၊ ဥပမာ - iPhone 12, Samsung Galaxy S21")
        return

    prompt = f"""
Suggest PUBG Mobile sensitivity settings for {phone_model}:
- Camera Sensitivity
- ADS Sensitivity
- Gyroscope Sensitivity
- Layout Type (2-finger/3-finger/4-finger/gyro)
"""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    fake_code = generate_fake_code()

    reply = f"🤖 PUBG Sensitivity for {phone_model}:\n\n{response.text}\n\n🎮 Fake Sensitivity Code: {fake_code}"

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))
    app.run_polling()

if __name__ == "__main__":
    main()
