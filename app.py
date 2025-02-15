import streamlit as st
from deep_translator import GoogleTranslator
import random

# Set up Streamlit page
st.set_page_config(page_title="German Language Chatbot", page_icon="🇩🇪", layout="wide")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to translate English to German
def translate_to_german(english_word):
    return GoogleTranslator(source='en', target='de').translate(english_word)

# Function for chatbot personality
def bot_personality():
    responses = [
        ""
    ]
    return random.choice(responses)

# Function to handle user input
def handle_user_input(user_input):
    if user_input:
        translation = translate_to_german(user_input)
        bot_response = f"{bot_personality()} German for '{user_input}' is: {translation}"
        return bot_response
    return "Please enter a word to translate."

# UI Elements
st.title("💬 German Language Chatbot")
st.write("Ask me about English words, and I'll give you the German translation!")

with st.form("chat_form"):
    user_input = st.text_input("Enter an English word:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    bot_response = handle_user_input(user_input)

    # Save user input and bot response
    st.session_state.chat_history.append({"role": "User", "text": user_input})
    st.session_state.chat_history.append({"role": "Bot", "text": bot_response})

# Display chat messages
for message in st.session_state.chat_history:
    with st.chat_message("user" if message["role"] == "User" else "assistant"):
        st.write(message["text"])
