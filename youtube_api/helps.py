import os

from functools import lru_cache
from re import findall
from typing import Dict

from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=os.getenv('TOKEN_YT'))


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
        else f'{minutes:0>2d}:{seconds:0>2d}sec' if minutes \
        else f'{seconds:0>2d}sec'
    return result, passed, missed


def get_video_duration_in_sec(video_id: str) -> int:
    video_duration_response = youtube.videos().list(part='contentDetails', id=video_id).execute()
    duration = video_duration_response['items'][0]['contentDetails']['duration']
    lst_time = findall(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)[0]
    hours, minutes, seconds = map(lambda x: int(x) if x else 0, lst_time)
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def get_dict_titles_and_ids_from_channel_id(channel_id: str) -> Dict[str, str]:
    playlists_response = youtube.playlists().list(part='snippet', channelId=channel_id, maxResults=50).execute()
    playlists_as_title_and_id = {pl['snippet']['title']: pl['id'] for pl in playlists_response['items']}
    return playlists_as_title_and_id


if __name__ == '__main__':
    pass
