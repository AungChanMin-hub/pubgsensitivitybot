import google.generativeai as genai
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load from Railway ENV variables
GEMINI_API_KEY = os.getenv("AIzaSyBTthKBzd5cJUiey1AJLBAIbY3z2rLGQUs")
TELEGRAM_BOT_TOKEN = os.getenv("8188050582:AAFAKpa1Qq9yTPv8omQgcWsHlBUKyEPf0-Y")

# Gemini config
genai.configure(api_key=GEMINI_API_KEY)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send your phone model (e.g. iPhone 12) and I’ll send you AI-generated PUBG sensitivity.")

# Phone model handler
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_model = update.message.text.strip()
    prompt = f"""
Suggest the best PUBG Mobile sensitivity settings for {phone_model}. Include:
- Camera Sensitivity
- ADS Sensitivity
- Gyroscope Sensitivity
- Layout Type (2-finger/3-finger/4-finger/gyro)
- Fake sensitivity code like 7176-xxxx-xxxx-xxxx
"""

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    await update.message.reply_text(f"🤖 AI Result for {phone_model}:\n\n{response.text}")

# Bot Setup
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

app.run_polling()