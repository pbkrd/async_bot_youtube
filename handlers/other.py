from aiogram import types, Dispatcher
from create_bot import bot, dp


# @dp.message_handler()
async def echo_send(message: types.Message):
    await message.answer(message.text)
    # await message.reply(message.text)
    # await bot.send_message(message.from_user.id, message.text)

def register_other_handler(dp: Dispatcher):
    dp.register_message_handler(echo_send)
