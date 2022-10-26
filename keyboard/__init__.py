import os

from keyboard.client_kb import get_kb_client_start, get_kb_menu_pls, get_kb_yes_or_no
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

bot = Bot(token=os.getenv('TOKEN_BOT'))
dp = Dispatcher(bot)