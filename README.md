# collective-chatGPT-telegram-bot
Сhatbot based on chatGPT for telegram groups. 
Сreate your own unique chatbot for your group chats, wich can act as user.

The bot can:
- respond to messages from group users
- maintain a dialogue in a group
- preserve dialog context
- typing while generating response
- add emojis to messages
- choose your personal avatar and bot name
- possible settings are supported: various languages, selection of emoticons, frequency of messages and reactions

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
   - when you first start the telethon, it asks for your phone number and a code to access your telegram messages.
7. Run the script run_bot.sh:
   sh run_bot.sh
