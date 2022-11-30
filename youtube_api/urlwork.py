import os

from datetime import datetime as dt
from re import findall
from typing import Dict

from .helps import youtube


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


def get_ids_from_url(url: str) -> Dict[str, str]:
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


if __name__ == '__main__':
    pass
