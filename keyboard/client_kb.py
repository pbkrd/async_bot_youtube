from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardMarkup


def get_kb_channel():
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton('PLAYLISTS', callback_data='playlists')
    b2 = InlineKeyboardButton('RESTART', callback_data='restart')
    kb.add(b1).add(b2)
    return kb


def get_kb_video():
    kb = get_kb_channel()
    b = InlineKeyboardButton('CHANNEL_info', callback_data='channel')
    kb.add(b)
    return kb


def get_kb_playlist(video_inside):
    kb = get_kb_video()
    # Поискать метод insert
    if video_inside:
        b = InlineKeyboardButton('VIDEO_info', callback_data='video')
        kb.add(b)
    return kb


def get_kb_menu_playlists(s_dict):
    titles_pls = tuple(s_dict)
    buttons = [KeyboardButton(title) for title in titles_pls]
    button_stop = KeyboardButton('/restart')
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_client.add(button_stop)
    [kb_client.add(button) for button in buttons]
    kb_client.add(button_stop)
    return kb_client
