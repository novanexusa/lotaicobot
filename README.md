# GPT-4 Telegram Assistant Bot

This is a Telegram bot that uses OpenAI's GPT-4 model to provide helpful responses to user queries. The bot is deployed on a hosting platform (like Heroku or Railway) and uses Flask to stay awake via a health check endpoint.

## Features

- Responds to user messages with GPT-4 generated content.
- `/start` command greets the user.
- Logging for better debugging.

## Prerequisites

- A Telegram Bot Token obtained from [BotFather](https://t.me/BotFather).
- An OpenAI API Key from [OpenAI Platform](https://platform.openai.com/).

## Setup

1. **Environment Variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.

2. **Installation:**
   ```bash
   pip install -r requirements.txt
