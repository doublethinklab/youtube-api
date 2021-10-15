from datetime import datetime
from functools import partial
from math import inf
import os
from typing import Any, Callable, Dict, List, Optional, Union

import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError

from youtube_api.data_structures import Channel, Comment, Video
from youtube_api import interface


def adapt_channel_to_channel(channel: Dict) -> Channel:
    snippet = channel['snippet']
    return Channel(
        id=channel['id'],
        title=channel['snippet']['title'],
        description=attr_or_none(snippet, 'description'),
        lang=attr_or_none(snippet, 'defaultLanguage'),
        country=attr_or_none(snippet, 'country'),
        created_at=api_string_to_datetime(channel['snippet']['publishedAt']))


def adapt_comment_to_comment(comment: Dict, comment_thread_id: str) -> Comment:
    return Comment(
        id=comment['id'],
        video_id=comment['snippet']['videoId'],
        author_channel_id=comment['snippet']['authorChannelId']['value'],
        comment_thread_id=comment_thread_id,
        replied_to_comment_id=attr_or_none(comment['snippet'], 'parentId'),
        created_at=api_string_to_datetime(comment['snippet']['publishedAt']),
        text=comment['snippet']['textOriginal'],
        num_likes=comment['snippet']['likeCount'],
        retrieved=datetime.utcnow())


def adapt_comment_thread_to_comments(comment_thread: Dict) -> List[Comment]:
    comments = []
    comment_thread_id = comment_thread['id']
    top_level_comment = adapt_comment_to_comment(
        comment_thread['snippet']['topLevelComment'], comment_thread_id)
    comments.append(top_level_comment)
    if 'replies' in comment_thread:
        for comment in comment_thread['replies']['comments']:
            comment = adapt_comment_to_comment(comment, comment_thread_id)
            comments.append(comment)
    return comments


def adapt_playlist_item_to_video(playlist_item: Dict) -> Video:
    return Video(
        id=playlist_item['snippet']['resourceId']['videoId'],
        channel_id=playlist_item['snippet']['channelId'],
        created_at=api_string_to_datetime(playlist_item['snippet']['publishedAt']),
        title=playlist_item['snippet']['title'],
        description=playlist_item['snippet']['description'],
        retrieved=datetime.utcnow())


def adapt_video_to_video(video: Dict) -> Video:
    return Video(
        id=video['id'],
        channel_id=video['snippet']['channelId'],
        created_at=api_string_to_datetime(video['snippet']['publishedAt']),
        title=video['snippet']['title'],
        description=video['snippet']['description'],
        retrieved=datetime.utcnow(),
        num_views=int(video['statistics']['viewCount']) if 'statistics' in video else None,
        num_likes=int(video['statistics']['likeCount']) if 'statistics' in video else None,
        num_dislikes=int(video['statistics']['dislikeCount']) if 'statistics' in video else None,
        num_comments=int(video['statistics']['commentCount']) if 'statistics' in video else None)


def api_string_to_datetime(date_time: str) -> datetime:
    # seen all of these come from the api
    date_formats = [
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%d %H:%M:%S',
    ]

    # try all possibilities
    success = False
    for date_format in date_formats:
        try:
            date_time = datetime.strptime(date_time, date_format)
            success = True
            break
        except ValueError:
            continue

    # if success, return the datetime
    if success:
        return date_time
    # otherwise throw an exception with the input for feedback
    else:
        raise ValueError(date_time)


def attr_or_none(mapping: Dict, key: str) -> Union[Any, None]:
    if key in mapping:
        return mapping[key]
    return None


def get_resource():
    return googleapiclient.discovery.build(
        'youtube', 'v3', developerKey=os.environ['API_KEY'])


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
        # TODO: catch the correct error
        try:
            request = fn(**kwargs)
            response = request.execute()
            return response
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
            channel = adapt_channel_to_channel(channel)
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
            video = adapt_playlist_item_to_video(playlist_item)
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
            comments += adapt_comment_thread_to_comments(comment_thread)
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
            video = adapt_video_to_video(video)
            videos.append(video)
        return videos
