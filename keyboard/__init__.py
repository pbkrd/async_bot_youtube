import os

from keyboard.client_kb import *
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

bot = Bot(token=os.getenv('TOKEN_BOT'))
dp = Dispatcher(bot)