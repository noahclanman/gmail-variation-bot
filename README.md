# Gmail Variation Bot

A Telegram bot to generate Gmail address variations using dot and plus tricks.

## Features

- **Dot Variations**: Create all possible dot variations for a Gmail username.
- **Plus Variations**: Generate variations using the plus trick with custom suffixes.
- **User  Registration**: Users must register to access the bot's features.

## Commands

- `/start`: Display a welcome message.
- `/register`: Register to use the bot.
- `/help`: Show available commands.
- `/gendot <username> [yes]`: Generate dot variations. Use "yes" to include the original.
- `/genplus <username> <suffix1> <suffix2> ...`: Generate plus variations with suffixes.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/noahclanman/gmail-variation-bot.git
   cd gmail-variation-bot

2 **Install Dependencies**

   ```bash
   pip install python-telegram-bot

3. **Configure the Bot**
Replace "YOUR_BOT_TOKEN" in main.py with your Telegram bot token from BotFather.

4. **Run the Bot**
   ```bash
   python main.py
