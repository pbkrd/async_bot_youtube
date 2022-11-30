import os

from functools import lru_cache
from re import findall
from typing import Dict
from datetime import datetime as dt
from googleapiclient.discovery import build
from aiogram.utils.markdown import bold, code, italic
from aiogram.utils.emoji import emojize


youtube = build('youtube', 'v3', developerKey=os.getenv('TOKEN_YT'))


def get_format_date(date_publ: str):
    date = dt.strptime(date_publ, "%Y-%m-%dT%H:%M:%SZ")
    res = date.strftime("%d %b %Y")
    return res


def get_updates_by_username(username):
    res = {}
    channel_resp = youtube.channels().list(part='snippet', forUsername=username).execute()
    res['channel_id'] = channel_resp['items'][0]['id']
    res['channel_title'] = channel_resp['items'][0]['snippet']['title']
    res['channel_date_publ'] = get_format_date(channel_resp['items'][0]['snippet']['publishedAt'])
    return res


def get_updates_by_channel_id(channel_id):
    res = {}
    channel_resp = youtube.channels().list(part='snippet', id=channel_id).execute()
    res['channel_title'] = channel_resp['items'][0]['snippet']['title']
    res['channel_date_publ'] = get_format_date(channel_resp['items'][0]['snippet']['publishedAt'])
    return res


def get_updates_by_video_id(video_id):
    res = {}
    video_resp = youtube.videos().list(part='snippet', id=video_id).execute()
    res['video_title'] = video_resp['items'][0]['snippet']['title']
    res['video_date_publ'] = get_format_date(video_resp['items'][0]['snippet']['publishedAt'])
    res['channel_id'] = video_resp['items'][0]['snippet']['channelId']
    return res


def get_updates_by_playlist_id(playlist_id):
    res = {}
    playlist_resp = youtube.playlists().list(part='snippet', id=playlist_id).execute()
    res['playlist_title'] = playlist_resp['items'][0]['snippet']['title']
    res['channel_id'] = playlist_resp['items'][0]['snippet']['channelId']
    res.update(get_updates_by_channel_id(res['channel_id']))
    return res


def get_ids_from_url(url) -> dict:
    dict_ids = {}

    if findall(r'youtu.be\/', url):
        dict_ids['video_id'] = findall(r'youtu.be\/([-\w]+)', url)[0]
        dict_ids.update(get_updates_by_video_id(dict_ids['video_id']))
        dict_ids.update(get_updates_by_channel_id(dict_ids['channel_id']))

    elif findall(r"youtube.com\/c\/", url):
        dict_ids['username'] = findall(r'youtube\.com\/c\/([-\w]+)', url)[0]
        dict_ids.update(get_updates_by_username(dict_ids['username']))

    elif findall(r'youtube.com\/', url):
        video_id = findall(r'v=([-\w]+)', url)
        if video_id:
            dict_ids['video_id'] = video_id[0]
            dict_ids.update(get_updates_by_video_id(dict_ids['video_id']))
            dict_ids.update(get_updates_by_channel_id(dict_ids['channel_id']))

        playlist_id = findall(r'list=([-\w]+)', url)
        if playlist_id:
            dict_ids['playlist_id'] = playlist_id[0]
            dict_ids.update(get_updates_by_playlist_id(dict_ids['playlist_id']))

    return dict_ids


# переименовать функцию
@lru_cache()
def get_total_time_of_playlist_by_id(playlist_id):
    playlistItems_response = youtube.playlistItems().list(part='contentDetails',
                                                          playlistId=playlist_id,
                                                          maxResults=50
                                                          ).execute()

    video_ids = [item['contentDetails']['videoId'] for item in playlistItems_response['items']]

    total_seconds = 0
    passed = {}
    missed = {}
    for i, v_id in enumerate(video_ids):
        try:
            total_seconds += get_video_duration_in_sec(v_id)
            passed[v_id] = i
        except IndexError:
            missed[v_id] = i

    # в отдельную функцию
    hours, seconds = divmod(total_seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    result = f'{hours:0>2d}:{minutes:0>2d}:{seconds:0>2d}sec' if hours \
        else f'{minutes:0>2d}:{seconds:0>2d}sec' if minutes\
        else f'{seconds:0>2d}sec'
    return result, passed, missed


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


def get_playlistId_from_url(url):
    return findall(r'list=([-\w]+)', url)[0]


def get_videoId_from_url(url):
    return findall(r"v=([-\w]+)", url)[0]


def get_video_duration_in_sec(video_id: str) -> int:
    video_duration_response = youtube.videos().list(part='contentDetails', id=video_id).execute()
    duration = video_duration_response['items'][0]['contentDetails']['duration']
    lst_time = findall(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)[0]
    hours, minutes, seconds = map(lambda x: int(x) if x else 0, lst_time)
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def get_dict_titles_and_ids_from_channel_id(channel_id) -> dict:
    playlists_response = youtube.playlists().list(part='snippet', channelId=channel_id, maxResults=50).execute()
    # Формирование словаря из пар (title: id) плейлиста
    playlists_as_title_and_id = {pl['snippet']['title']: pl['id'] for pl in playlists_response['items']}
    return playlists_as_title_and_id


if __name__ == '__main__':
    # Не забудь поменять исходник
    pass