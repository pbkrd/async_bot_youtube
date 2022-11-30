from .helps import get_total_time_of_playlist_by_id
from aiogram.utils.markdown import bold, code, italic


def get_report_for_playlist(dict_ids, playlist_id=None, playlist_title=None):
    playlist_id = dict_ids["playlist_id"] if playlist_id is None else playlist_id
    playlist_title = dict_ids["playlist_title"] if playlist_title is None else playlist_title
    total_time, passed, missed = get_total_time_of_playlist_by_id(playlist_id)
    report = f'{bold("Канал:")} {dict_ids["channel_title"]}\n' \
             f'{bold("Плейлист:")} {playlist_title}\n' \
             f'{bold("Подсчитанных видео:")} {len(passed)}\n' \
             f'{bold("Длина плейлиста:")} {total_time}'

    report = report + f'\n{bold("Пропущенные видео")}: {(len(missed))}' if missed else report
    return report


def get_report_for_video(dict_ids):
    report = f'{bold("Канал:")} {dict_ids["channel_title"]}\n' \
             f'{bold("Видео:")} {dict_ids["video_title"]}\n' \
             f'{bold("Дата выхода:")} {dict_ids["video_date_publ"]}'
    return report


def get_report_for_channel(dict_ids):
    report = f'{bold("Канал:")} {dict_ids["channel_title"]}\n' \
             f'{bold("Дата регистрации:")} {dict_ids["channel_date_publ"]}'
    return report

if __name__ == '__main__':
    pass