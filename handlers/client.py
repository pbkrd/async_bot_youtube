import youtube_api

from create_bot import bot, dp
from keyboard import get_kb_client_start, get_kb_menu_pls, get_kb_yes_or_no
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMClient(StatesGroup):
    playlists = State()
    answer_v = State()
    menu = State()


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await message.answer('Условные обозначения:'
                         '\nv - video/видео'
                         '\npl - playlist/плейлист'
                         '\nch - channel/канал'
                         '\nref - reference/ссылка URL'
                         '\n/start или /help'
                         '\n/отмена для возврата в исходное меню')
    await message.answer('Какой способ загрузки?', reply_markup=get_kb_client_start())
    # await message.delete()


# Начало диалога "Поиск по URL плейлиста"
# @dp.message_handler(commands=['Ссылка_(URL)_на_плейлист'], state=None)
async def get_playlist_time_start(message: types.Message):
    await FSMClient.playlists.set()
    await message.answer('Пришлите ref на pl')


# Ловим ответ c URL плейлиста, выдаем результат и завершаем
# @dp.message_handler(state=FSMClient.playlists)
async def get_playlist_time_finish(message: types.Message, state: FSMContext):
    url_pl = message.text
    try:
        r_time = youtube_api.get_total_time_of_playlist_by_url(url_pl)
        await message.reply(r_time)
    except IndexError:
        await message.reply('Некорректная ref на pl')
    finally:
        await message.answer('Попробовать еще раз?', reply_markup=get_kb_yes_or_no())
        await state.finish()


# @dp.message_handler(commands=['ДА', 'НЕТ'])
async def get_res_on_yes_or_no(message: types.Message):
    answer = message.text
    await get_playlist_time_start(message) if answer == '/ДА' else \
        await message.answer('Какой способ загрузки?', reply_markup=get_kb_client_start())


# get_menu_of_playlists_by_url_video
# @dp.message_handler(commands=['Ссылка_(URL)_на_любое_видео_с_канала'], state=None)
async def answer_url_video(message: types.Message):
    await FSMClient.answer_v.set()
    await message.answer('Пришлите ref на любое v из ch')


# @dp.message_handler(state=FSMClient.answer_v)
async def get_menu_by_url(message: types.Message, state: FSMContext):
    url_v = message.text
    try:
        d = youtube_api.get_dict_title_id_from_url_video(url_v)
        async with state.proxy() as data:
            data.update(d)
        await FSMClient.next()
        await bot.send_message(message.from_user.id,
                               'Выберите один из плейлистов по названию',
                               reply_markup=get_kb_menu_pls(d)
                               )
    except IndexError:
        await message.answer('Некорректная ref на pl')
        await cancel_handler(message, state=state)


# @dp.message_handler(state=FSMClient.menu)
async def get_time_of_playlist(message: types.Message, state: FSMContext):
    title_pl = message.text
    async with state.proxy() as data:
        id_pl = data[title_pl]
    r_time = youtube_api.get_total_time_of_playlist_by_id(id_pl)
    await message.reply(r_time)
    # await state.finish()


# @dp.message_handler(state='*', commands=['отмена'])
# @dp.message_handler(Text(equals="отмена", ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Какой способ загрузки?', reply_markup=get_kb_client_start())


def register_client_handler(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(cancel_handler, state='*', commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state='*')
    dp.register_message_handler(get_playlist_time_start, commands=['ref_на_pl_или_на_v_из_pl'], state=None)
    dp.register_message_handler(get_playlist_time_finish, state=FSMClient.playlists)
    dp.register_message_handler(get_res_on_yes_or_no, commands=['ДА', 'НЕТ'])
    dp.register_message_handler(answer_url_video, commands=['ref_на_любое_v_из_ch'], state=None)
    dp.register_message_handler(get_menu_by_url, state=FSMClient.answer_v)
    dp.register_message_handler(get_time_of_playlist, state=FSMClient.menu)
    dp.register_message_handler(cancel_handler, state='*', commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state='*')
