import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file (useful for local testing)
load_dotenv()

# Get API keys
GEMINI_API_KEY = os.getenv("AIzaSyAb-Qo0kzndfAHPciJJmztxYgU9miEWV54")
TELEGRAM_BOT_TOKEN = os.getenv("8188050582:AAFAKpa1Qq9yTPv8omQgcWsHlBUKyEPf0-Y")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Handle /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n📱 Send me your phone model (e.g. iPhone 12, Redmi Note 13).\n\n🎯 I will generate the best PUBG sensitivity settings for you!"
    )

# Handle user input (phone model)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    prompt = f"""
You are a PUBG Mobile sensitivity expert.

Suggest the best PUBG Mobile sensitivity settings for the phone model: {user_input}

Include:
- Camera Sensitivity
- ADS Sensitivity
- Gyroscope Sensitivity
- Recommended Layout (2-finger / 3-finger / 4-finger / gyroscope)
- Fake Sensitivity Code (e.g. 1234-5678-9101-1121)

Respond in a clean, easy-to-read format.
"""

    try:
        response = model.generate_content(prompt)
        await update.message.reply_text(f"📱 Phone: {user_input}\n\n{response.text}")
    except Exception as e:
        await update.message.reply_text("❌ Something went wrong. Please try again.")
        print(f"[ERROR] {e}")

# Start bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()
