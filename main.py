import os
import openai
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from flask import Flask
from threading import Thread

# Set up logging for better error tracking
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "GPT Assistant Bot is running!"

# Set up OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define a function to handle the /start command
def start(update, context):
    logger.info("Received /start command from user: %s", update.effective_user.username)
    update.message.reply_text('Hello! I am GPT Assistant. Ask me anything!')

# Define a function to handle user messages
def handle_message(update, context):
    user_message = update.message.text
    logger.info("Received message from user: %s", user_message)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ]
        )
        gpt_reply = response.choices[0].message['content'].strip()
        logger.info("Sending reply to user: %s", gpt_reply)
        update.message.reply_text(gpt_reply)
    except Exception as e:
        logger.error("Error processing message: %s", e)
        update.message.reply_text("Sorry, I couldn't process that. Please try again later.")

def main():
    # Retrieve the Telegram Bot Token from environment variables
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not telegram_token:
        logger.error("TELEGRAM_BOT_TOKEN is not set in environment variables.")
        return

    # Set up the Telegram bot with the token
    updater = Updater(telegram_token, use_context=True)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    logger.info("Bot started polling.")
    updater.idle()

def run_flask():
    # Run Flask app to keep Railway awake
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # Run Flask app in a separate thread
    t = Thread(target=run_flask)
    t.start()
    logger.info("Flask server started.")
    main()
