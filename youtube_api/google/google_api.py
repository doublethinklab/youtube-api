from datetime import datetime
from functools import partial
import logging
from math import inf
import os
import time
from typing import Any, Callable, Dict, List, Optional, Union

import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError

from youtube_api.data_structures import Channel, Comment, Video
from youtube_api.google.data_mapping import *
from youtube_api import interface


def get_resource(api_key: Optional[str] = None):
    if not api_key:
        api_key = os.environ['API_KEY']
    return googleapiclient.discovery.build(
        'youtube', 'v3', developerKey=api_key)


class GoogleApiFunction:

    def __init__(self, resource):
        self.resource = resource

    def extract_data(self, response) -> List[Any]:
        raise NotImplementedError

    @staticmethod
    def get_next_page(response):
        return response['nextPageToken'] \
            if 'nextPageToken' in response \
            else None

    def paginate(self,
                 fn: Callable,
                 stop_fn: Callable = lambda x: False,
                 **kwargs) -> List[Any]:
        response = self.wait_while_rate_limited(fn, **kwargs)
        data = self.extract_data(response)
        next_page_token = self.get_next_page(response)
        while next_page_token and not stop_fn(data):
            kwargs['pageToken'] = next_page_token
            response = self.wait_while_rate_limited(fn, **kwargs)
            data += self.extract_data(response)
            next_page_token = self.get_next_page(response)
        return data

    @staticmethod
    def wait_while_rate_limited(fn, **kwargs):
        while True:
            try:
                request = fn(**kwargs)
                response = request.execute()
                return response
            except HttpError as e:
                if e.error_details[0]['reason'] == 'commentsDisabled':
                    logging.warning(f'Comments disabled.')
                    return []
                elif e.error_details[0]['reason'] == 'videoNotFound':
                    logging.warning('Video not found.')
                    return []
                elif e.error_details[0]['reason'] == 'quotaExceeded':
                    logging.warning('Rate limited. Waiting one hour...')
                    time.sleep(60 * 60)
                elif e.error_details[0]['reason'] == 'SERVICE_UNAVAILABLE':
                    # assuming this is transient
                    logging.warning('Service unavailable. Waiting 5 mins...')
                    time.sleep(5 * 60)
                elif e.error_details[0]['reason'] == 'backendError':
                    # assuming this is transient
                    logging.warning('Backend error. Waiting 5 mins...')
                    time.sleep(5 * 60)
                else:
                    raise Exception('Unexpected HttpError reason: %s'
                                    % e.error_details[0]['reason'])
            except Exception as e:
                print('*' * 8)
                print(response)
                print(response.__dict__)
                print(e)
                print(type(e))
                print(str(e))
                print(e.__dict__)
                raise e


class GetChannel(GoogleApiFunction, interface.GetChannel):

    def __call__(self, channel_id: str) -> Channel:
        data = self.paginate(
            fn=self.resource.channels().list,
            id=channel_id,
            part='contentDetails,snippet,statistics,topicDetails')
        # TODO: proper way to know that no data is returned?
        if len(data) == 0:
            raise ValueError(f'No data: {channel_id}')
        return data[0]

    def extract_data(self, response) -> List[Channel]:
        channels = []
        for channel in response['items']:
            channel = map_channel_to_channel(channel)
            channels.append(channel)
        return channels


class GetChannelVideos(GoogleApiFunction, interface.GetChannelVideos):

    def __call__(self,
                 channel_id: str,
                 limit: int = inf,
                 start: Optional[datetime] = None,
                 end: Optional[datetime] = None) -> List[Video]:
        uploads_stream = self.get_uploads_stream(channel_id)
        stop_fn = partial(self.stop, limit=limit, start=start)
        data = self.paginate(
            fn=self.resource.playlistItems().list,
            stop_fn=stop_fn,
            part='snippet',
            playlistId=uploads_stream)
        data = [x for x in data
                if start <= x.created_at <= end]
        if len(data) > limit:
            data = data[-limit:]
        return data

    def extract_data(self, response) -> List[Video]:
        videos = []
        for playlist_item in response['items']:
            video = map_playlist_item_to_video(playlist_item)
            videos.append(video)
        return videos

    def get_uploads_stream(self, channel_id: str) -> str:
        request = self.resource.channels().list(
            part='contentDetails',
            id=channel_id)
        response = request.execute()
        return response['items'][0]['contentDetails']['relatedPlaylists'][
            'uploads']

    @staticmethod
    def stop(data: List[Video],
             limit: int,
             start: datetime) -> bool:
        return len(data) > limit or min(x.created_at for x in data) < start


class GetVideoComments(GoogleApiFunction, interface.GetVideoComments):

    def __call__(self, video_id: str, limit: int = inf) -> List[Comment]:
        page_size = 100  # this is the max
        if page_size > limit:
            page_size = limit
        stop_fn = partial(self.stop, limit=limit)
        data = self.paginate(
            fn=self.resource.commentThreads().list,
            stop_fn=stop_fn,
            part='snippet,replies',
            maxResults=page_size,
            videoId=video_id)
        return data

    def extract_data(self, response) -> List[Comment]:
        comments = []
        for comment_thread in response['items']:
            comments += map_comment_thread_to_comments(comment_thread)
        return comments

    @staticmethod
    def stop(data: List[Video], limit: int) -> bool:
        return len(data) >= limit


class GetVideo(GoogleApiFunction, interface.GetVideo):

    def __call__(self, video_id: str) -> Video:
        data = self.paginate(
            fn=self.resource.videos().list,
            part='snippet,contentDetails,statistics',
            id=video_id)
        if len(data) == 0:
            raise ValueError(f'No video found for {video_id}.')
        return data[0]

    def extract_data(self, response) -> List[Video]:
        videos = []
        for video in response['items']:
            video = map_video_to_video(video)
            videos.append(video)
        return videos
