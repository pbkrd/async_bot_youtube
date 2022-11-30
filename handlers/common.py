from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot


async def command_start(message: types.Message | types.CallbackQuery, state: FSMContext):
    if state is not None:
        await state.finish()
    await FSMClient.request_url.set()
    answer = 'Пришлите новую ссылку \U0001F517'
    await bot.send_message(message.from_user.id,
                           answer,
                           reply_markup=types.ReplyKeyboardRemove())


class FSMClient(StatesGroup):
    request_url = State()
    playlist = State()
    playlists_menu = State()
    video = State()
    channel = State()
