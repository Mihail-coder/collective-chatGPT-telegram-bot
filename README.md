# collective-chatGPT-telegram-bot
Сhatbot based on chatGPT for telegram groups. 

The bot can:
- respond to messages from group users
- maintain a dialogue in a group
- add emojis to messages

Requirements: Linux/Unix, python 3.8+, Telegram app and user account.

Installation:
1. Download and extract the repository.
2. Install all required packages:
   - pip install pyTelegramBotAPI
   - pip install -U g4f
   - pip install curl-cffi
   - pip install Telethon
   - pip install langdetect
   - pip install nest-asyncio
4. In the settings file specify all the necessary settings.
5. Before the bot starts:
   - be shure privacy mode of your bot is disabled
   - add your bot to the group
   - contact him in the group via @yourbotname any text
7. Run the script run_bot.sh:
   sh run_bot.sh
