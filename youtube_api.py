import os

from functools import lru_cache
from re import findall
from googleapiclient.discovery import build

URL_VIDEO = 'https://www.youtube.com/watch?v=th5_9woFJmk'
youtube = build('youtube', 'v3', developerKey=os.getenv('TOKEN_YT'))


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


@lru_cache()
def get_total_time_of_playlist_by_id(pl_id):
    playlistItems_response = youtube.playlistItems().list(part='contentDetails',
                                                          playlistId=pl_id,
                                                          maxResults=50
                                                          ).execute()

    video_ids = [item['contentDetails']['videoId'] for item in playlistItems_response['items']]

    total_seconds = sum(get_video_duration_in_sec(v_id) for v_id in video_ids)
    hours, seconds = divmod(total_seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f'{hours:0>2d}:{minutes:0>2d}:{seconds:0>2d}sec' if hours else \
           f'{minutes:0>2d}:{seconds:0>2d}sec' if minutes else \
           f'{seconds:0>2d}sec'


def get_total_time_of_playlist_by_url(url):
    pl_id = get_playlistId_from_url(url)
    playlistItems_response = youtube.playlistItems().list(part='contentDetails',
                                                          playlistId=pl_id,
                                                          maxResults=50
                                                          ).execute()

    video_ids = [item['contentDetails']['videoId'] for item in playlistItems_response['items']]

    total_seconds = sum(get_video_duration_in_sec(v_id) for v_id in video_ids)
    hours, seconds = divmod(total_seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f'{hours:0>2d}:{minutes:0>2d}:{seconds:0>2d}sec' if hours else \
           f'{minutes:0>2d}:{seconds:0>2d}sec' if minutes else \
           f'{seconds:0>2d}sec'


def get_dict_title_id_from_url_video(url_video):
    video_id = get_videoId_from_url(url_video)
    video_response = youtube.videos().list(part='snippet', id=video_id).execute()
    channel_id = video_response['items'][0]['snippet']['channelId']
    playlists_response = youtube.playlists().list(part='snippet', channelId=channel_id, maxResults=50).execute()

    # Формирование словаря из пар (title: id) плейлиста
    playlists_as_title_and_id = {pl['snippet']['title']: pl['id'] for pl in playlists_response['items']}
    return playlists_as_title_and_id


if __name__ == '__main__':
    pass
