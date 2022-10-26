from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


def get_kb_client_start():
    b1 = KeyboardButton('/ref_на_pl_или_на_v_из_pl')
    b2 = KeyboardButton('/ref_на_любое_v_из_ch')
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_client.add(b1).add(b2)
    return kb_client


def get_kb_menu_pls(s_dict):
    titles_pls = tuple(s_dict)
    buttons = [KeyboardButton(title) for title in titles_pls]
    button_stop = KeyboardButton('/отмена')
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_client.add(button_stop)
    [kb_client.add(button) for button in buttons]
    kb_client.add(button_stop)
    return kb_client


def get_kb_yes_or_no():
    b1 = KeyboardButton('/ДА')
    b2 = KeyboardButton('/НЕТ')
    kb_client = ReplyKeyboardMarkup()
    kb_client.row(b1, b2)
    return kb_client
