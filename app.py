from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging

# Logging setup for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Translation function
def translate_to_german(english_word):
    try:
        # Using deep_translator to translate
        translation = GoogleTranslator(source='en', target='de').translate(english_word)
        return translation if translation else "Sorry, I couldn't translate that at the moment."
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return "Sorry, I couldn't translate that at the moment."

# Function to handle the message and return a translation
async def telegram_message_handler(update: Update, context):
    user_input = update.message.text
    bot_response = translate_to_german(user_input)
    await update.message.reply_text(f"German for '{user_input}' is: {bot_response}")

# Function for the /start command
async def start(update: Update, context):
    await update.message.reply_text("Hello! Send me an English word, and I'll translate it into German!")

# Telegram bot setup
def main():
    # Replace with your bot token
    TOKEN = "7984631453:AAEimDRv2G4StdZPum86h6BbnfJYd31s92c"

    # Setting up the application
    application = Application.builder().token(TOKEN).build()

    # Adding handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_message_handler))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
