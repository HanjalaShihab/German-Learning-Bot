import os
import time
import logging
import asyncio
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Translation function
def translate_to_german(english_word):
    try:
        translation = GoogleTranslator(source='en', target='de').translate(english_word)
        return translation if translation else "Sorry, I couldn't translate that at the moment."
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return "Sorry, I couldn't translate that at the moment."

# Telegram Handlers
async def telegram_message_handler(update: Update, context):
    user_input = update.message.text
    bot_response = translate_to_german(user_input)
    await update.message.reply_text(f"German for '{user_input}' is: {bot_response}")

async def start(update: Update, context):
    await update.message.reply_text("Hello! Send me an English word, and I'll translate it into German!")

# Telegram Bot Function
async def run_telegram_bot():
    TOKEN = os.getenv("7984631453:AAEimDRv2G4StdZPum86h6BbnfJYd31s92c")  # Use environment variable

    if not TOKEN:
        logger.error("Bot token is missing! Set TELEGRAM_BOT_TOKEN in environment variables.")
        return

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_message_handler))

    logger.info("Starting Telegram bot...")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(run_telegram_bot())
    while True:
        time.sleep(10)  # Keeps the instance running
