import json
from telegram.ext import Updater
from telegram import Bot

# with open('config.json', 'r') as f:
#     config = json.load(f)
#     TOKEN = config['token']
#     auth = config['auth']
#     chat_id = config['chat_id']

# async def send_telegram_message(msg:str):
#     bot = Bot(token=TOKEN)
#     updater = Updater(bot=bot, update_queue=True)
#     await bot.send_message(chat_id=chat_id,text=msg)


'''STREAMLIT CODE'''

async def send_telegram_message(msg:str):
    bot = Bot(token=ST.secrets['token'])
    updater = Updater(bot=bot, update_queue=True)
    await bot.send_message(chat_id=st.secrets['chat_id'],text=msg)