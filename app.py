from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import streamlit as st
import asyncio

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
    TOKEN = "7984631453:AAEimDRv2G4StdZPum86h6BbnfJYd31s92c"

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_message_handler))

    await application.run_polling()

# Start the bot without `asyncio.run()`
def start_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(run_telegram_bot())

# Streamlit UI
def run_streamlit():
    st.title("German Translation Bot")
    st.write("Welcome to the German Translation Bot!")

    input_text = st.text_input("Enter an English word:")
    
    if input_text:
        translation = translate_to_german(input_text)
        st.write(f"The German translation for '{input_text}' is: {translation}")

    # Start the Telegram bot (only if not running)
    if 'bot_started' not in st.session_state:
        st.session_state.bot_started = True
        asyncio.create_task(run_telegram_bot())  # Run bot inside Streamlit's event loop

if __name__ == '__main__':
    run_streamlit()
