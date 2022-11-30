import youtube_api

from create_bot import bot, dp
from keyboard import *
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMClient(StatesGroup):
    request_url = State()
    playlist = State()
    playlists_menu = State()
    video = State()
    channel = State()


# @dp.message_handler(commands=['start', 'restart', 'help'], state='*')
# @dp.callback_query_handler(text="restart", state='*')
async def command_start(message: types.Message | types.CallbackQuery, state: FSMContext):
    if state is not None:
        await state.finish()
    await FSMClient.request_url.set()
    answer = 'Пришлите новую ссылку \U0001F517'
    await bot.send_message(message.from_user.id,
                           answer,
                           reply_markup=types.ReplyKeyboardRemove())


# @dp.message_handler(state=FSMClient.request_url)
async def get_report_about_url(message: types.Message, state: FSMContext):
    url = message.text
    dict_ids = {}
    try:
        dict_ids.update(youtube_api.get_ids_from_url(url))
        async with state.proxy() as storage:
            storage.update(dict_ids)
        if 'playlist_id' in dict_ids:
            await FSMClient.playlist.set()
            answer = youtube_api.get_report_for_playlist(dict_ids)
            keyboard = get_kb_playlist(video_inside=('video_id' in dict_ids))
            await message.answer(answer,
                                 parse_mode=types.ParseMode.MARKDOWN,
                                 reply_markup=keyboard)

        elif 'video_id' in dict_ids:
            # Этот кусок и подобные 2 в дальнешем дублируются. Много кода для 1 функции, поэтому:
            # нужно заменить на отдельне функции. Но функции лучше вынести в другой модуль
            await FSMClient.video.set()
            answer = youtube_api.get_report_for_video(dict_ids)
            keyboard = get_kb_video()
            await message.answer(answer,
                                 parse_mode=types.ParseMode.MARKDOWN,
                                 reply_markup=keyboard)

        elif 'channel_id' in dict_ids:
            await FSMClient.channel.set()
            answer = youtube_api.get_report_for_channel(dict_ids)
            keyboard = get_kb_channel()
            await message.answer(answer,
                                 parse_mode=types.ParseMode.MARKDOWN,
                                 reply_markup=keyboard)

        else:
            answer = 'Некорректная ссылка'
            await message.answer(answer)
            await command_start(message, state)
    except Exception as e:
        print(e)
        await message.reply('Что-то пошло не так!')
        await command_start(message, state)


# @dp.callback_query_handler(text="channel", state=FSMClient.playlist)
async def command_channel(call: types.CallbackQuery, state: FSMContext):
    await FSMClient.channel.set()
    await bot.answer_callback_query(call.id)
    async with state.proxy() as dict_ids:
        answer = youtube_api.get_report_for_channel(dict_ids)
    await bot.send_message(call.from_user.id,
                           answer,
                           parse_mode=types.ParseMode.MARKDOWN,
                           reply_markup=get_kb_channel())


# @dp.callback_query_handler(text="video", state=FSMClient.playlist)
# # @dp.message_handler(commands='VIDEO', state=FSMClient.playlists_menu)
# # @dp.message_handler(commands='VIDEO', state=FSMClient.request_url)
async def command_video(call: types.CallbackQuery, state: FSMContext):
    await FSMClient.video.set()
    await bot.answer_callback_query(call.id)
    async with state.proxy() as data:
        answer = youtube_api.get_report_for_video(data)
    await bot.send_message(call.from_user.id,
                           answer,
                           parse_mode=types.ParseMode.MARKDOWN,
                           reply_markup=get_kb_video())


# @dp.message_handler(commands='PLAYLISTS', state=FSMClient.channel)
# @dp.message_handler(commands='PLAYLISTS', state=FSMClient.video)
# @dp.callback_query_handler(text="playlists", state=FSMClient.playlist)
async def command_playlists_menu(call: types.CallbackQuery, state: FSMContext):
    await FSMClient.playlists_menu.set()
    await bot.answer_callback_query(call.id)
    async with state.proxy() as stash:
        titles_and_ids = youtube_api.get_dict_titles_and_ids_from_channel_id(stash['channel_id'])
        stash['titles_and_ids'] = titles_and_ids
    answer = 'Выберите плейлист'
    await bot.send_message(call.from_user.id,
                           answer,
                           reply_markup=get_kb_menu_playlists(titles_and_ids))


# @dp.message_handler(state=FSMClient.playlists_menu)
async def get_time_from_playlists_menu(message: types.Message, state: FSMContext):
    playlist_title = message.text
    async with state.proxy() as stash:
        playlist_id = stash['titles_and_ids'][playlist_title]
        answer = youtube_api.get_report_for_playlist(stash, playlist_id, playlist_title)
    # Поиграться с асинхронкой
    await message.delete()
    await bot.send_message(message.from_user.id,
                           answer,
                           parse_mode=types.ParseMode.MARKDOWN)


def register_client_handler(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'restart', 'help'], state='*')
    dp.register_callback_query_handler(command_start, text="restart", state='*')
    dp.register_message_handler(get_report_about_url, state=FSMClient.request_url)
    dp.register_callback_query_handler(command_channel, text="channel", state=[FSMClient.playlist,
                                                                               FSMClient.video])
    dp.register_callback_query_handler(command_video, text="video", state=FSMClient.playlist)
    dp.register_callback_query_handler(command_playlists_menu, text="playlists", state=[FSMClient.playlist,
                                                                                        FSMClient.video,
                                                                                        FSMClient.channel])
    dp.register_message_handler(get_time_from_playlists_menu, state=FSMClient.playlists_menu)
