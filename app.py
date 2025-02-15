from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import streamlit as st
import multiprocessing
import asyncio

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
async def run_telegram_bot():
    # Replace with your bot token
    TOKEN = "7984631453:AAEimDRv2G4StdZPum86h6BbnfJYd31s92c"

    # Setting up the application
    application = Application.builder().token(TOKEN).build()

    # Adding handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_message_handler))

    # Start the bot
    await application.run_polling()

# Function to run the Telegram bot in a separate process using multiprocessing
def start_bot_process():
    asyncio.run(run_telegram_bot())

# Start Streamlit app
def run_streamlit():
    # Streamlit user interface
    st.title("German Translation Bot")
    st.write("Welcome to the German Translation Bot!")
    
    input_text = st.text_input("Enter an English word:")
    
    if input_text:
        translation = translate_to_german(input_text)
        st.write(f"The German translation for '{input_text}' is: {translation}")
        
    # Start the Telegram bot in a separate process
    bot_process = multiprocessing.Process(target=start_bot_process)
    bot_process.start()

if __name__ == '__main__':
    run_streamlit()
