from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import bot
from handlers import FSMClient
from .common import command_start, FSMClient
from youtube_api import get_report_for_playlist


async def get_time_from_playlists_menu(message: types.Message, state: FSMContext):
    playlist_title = message.text
    async with state.proxy() as stash:
        playlist_id = stash['titles_and_ids'][playlist_title]
        answer = get_report_for_playlist(stash, playlist_id, playlist_title)
    # Поиграться с асинхронкой
    await message.delete()
    await bot.send_message(message.from_user.id,
                           answer,
                           parse_mode=types.ParseMode.MARKDOWN)


async def echo_send(message: types.Message):
    await message.answer(message.text)


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'restart', 'help'], state='*')
    dp.register_message_handler(get_time_from_playlists_menu, state=FSMClient.playlists_menu)
    dp.register_message_handler(echo_send)
