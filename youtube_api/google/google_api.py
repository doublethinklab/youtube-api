from datetime import datetime
from functools import partial
import logging
from math import inf
import os
import random
import time
from typing import Any, Callable, Dict, List, Optional, Union

import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError

from data_structures.youtube import *
from youtube_api.google.data_mapping import *
from youtube_api import interface


def get_keys(keys_dir: str = os.environ['YOUTUBE_API_KEYS_DIR']) -> List[str]:
    keys = []
    for file in os.listdir(keys_dir):
        file_path = os.path.join(keys_dir, file)
        with open(file_path) as f:
            key = f.read().strip()
            keys.append(key)
    return keys


def get_resource(api_key: Optional[str] = None):
    if not api_key:
        api_key = os.environ['API_KEY']
    return googleapiclient.discovery.build(
        'youtube', 'v3', developerKey=api_key)


def stop_when_at_limit(data: List[Any], limit: int) -> bool:
    return len(data) >= limit


def stop_when_at_size_or_date_limit(data: List[Any],
                                    limit: int,
                                    start: datetime) -> bool:
    # assumes working backwards through time
    # assumes Any is an object with a `created_at` property
    return len(data) > limit or min(x.created_at for x in data) < start


class ApiKeyManager:

    def __init__(self,
                 api_keys: List[str] = get_keys(),
                 wait_mins: int = 60):
        random.shuffle(api_keys)
        self.api_key_to_exceeded_time = {
            key: datetime(2000, 1, 1) for key in api_keys}
        self.wait_mins = wait_mins

    @staticmethod
    def _get_mins_diff(exceeded_time: datetime) -> int:
        diff_secs = (datetime.now() - exceeded_time).total_seconds()
        return int(round(diff_secs / 60, 0))

    def _get_next_available_key(self) -> Union[str, None]:
        logging.info('Looking for next available api key...')
        key_diff = [
            {'key': k, 'diff': self._get_mins_diff(t)}
            for k, t in self.api_key_to_exceeded_time.items()]
        for x in key_diff:
            logging.info('Api key "%s" status: reported exceeded %s mins ago.'
                         % (x['key'], x['diff']))
        key_diff = list(reversed(sorted(key_diff, key=lambda x: x['diff'])))
        next_key, diff = key_diff[0]['key'], key_diff[0]['diff']
        if diff < self.wait_mins:
            logging.info(f'No keys expired less than {self.wait_mins} mins '
                         f'ago.')
            return None
        else:
            logging.info(f'Returning new api key "{next_key}".')
            return next_key

    def get_key(self) -> str:
        while True:
            api_key = self._get_next_available_key()
            if not api_key:
                time.sleep(self.wait_mins * 60)
            else:
                return api_key

    def report_quota_exceeded(self, api_key: str) -> None:
        exceeded_time = datetime.now()
        exceeded_time_str = exceeded_time.strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f'Api key "{api_key}" quota reported '
                     f'exceeded at {exceeded_time_str}.')
        self.api_key_to_exceeded_time[api_key] = exceeded_time


class ResourceManager:

    def __init__(self, api_key_manager: ApiKeyManager):
        self.api_key_manager = api_key_manager
        # since getting a resource can involve waiting, only try when asked
        # for a resource
        self.current_api_key = None
        self.current_resource = None

    def _set_current_resource(self) -> None:
        self.current_api_key = self.api_key_manager.get_key()
        self.current_resource = get_resource(self.current_api_key)

    def get_resource(self) -> googleapiclient.discovery.Resource:
        if not self.current_resource:
            self._set_current_resource()
        return self.current_resource

    def report_quota_exceeded(self) -> None:
        self.api_key_manager.report_quota_exceeded(self.current_api_key)
        self.current_api_key = None
        self.current_resource = None


class GoogleApiFunction:

    def __init__(self, resource_manager: ResourceManager, debug: bool = False):
        self.resource_manager = resource_manager
        self.debug = debug

    @staticmethod
    def _datetime_to_string_for_api(date_time: datetime) -> str:
        return date_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    def extract_data(self, response) -> List[Any]:
        raise NotImplementedError

    def get_function(self, resource: googleapiclient.discovery.Resource) \
            -> Callable:
        raise NotImplementedError

    @staticmethod
    def get_next_page(response):
        return response['nextPageToken'] \
            if 'nextPageToken' in response \
            else None

    def paginate(self,
                 stop_fn: Callable = lambda x: False,
                 **kwargs) -> List[Any]:
        response = self.wait_while_rate_limited(**kwargs)
        data = self.extract_data(response)
        next_page_token = self.get_next_page(response)
        while next_page_token and not stop_fn(data):
            kwargs['pageToken'] = next_page_token
            response = self.wait_while_rate_limited(**kwargs)
            data += self.extract_data(response)
            next_page_token = self.get_next_page(response)
        return data

    def wait_while_rate_limited(self, **kwargs):
        while True:
            try:
                resource = self.resource_manager.get_resource()
                fn = self.get_function(resource)
                request = fn(**kwargs)
                response = request.execute()
                if self.debug:
                    print(response)
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
                    self.resource_manager.report_quota_exceeded()
                    # NOTE: waiting handled by resource_factory.api_key_manager
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

    def __call__(self, channel_id: str) -> YouTubeChannel:
        data = self.paginate(
            id=channel_id,
            part='contentDetails,snippet,statistics,topicDetails')
        # TODO: proper way to know that no data is returned?
        if len(data) == 0:
            raise ValueError(f'No data: {channel_id}')
        return data[0]

    def extract_data(self, response) -> List[YouTubeChannel]:
        channels = []
        for channel in response['items']:
            channel = map_channel_to_channel(channel)
            channels.append(channel)
        return channels

    def get_function(self, resource: googleapiclient.discovery.Resource) \
            -> Callable:
        return resource.channels().list


class GetChannelVideos(GoogleApiFunction, interface.GetChannelVideos):

    def __call__(self,
                 channel_id: str,
                 limit: int = inf,
                 start: Optional[datetime] = None,
                 end: Optional[datetime] = None) -> List[YouTubeVideo]:
        uploads_stream = self.get_uploads_stream(channel_id)
        stop_fn = partial(
            stop_when_at_size_or_date_limit,
            limit=limit,
            start=start)
        data = self.paginate(
            stop_fn=stop_fn,
            part='snippet',
            playlistId=uploads_stream)
        data = [x for x in data
                if start <= x.created_at <= end]
        if len(data) > limit:
            data = data[-limit:]
        return data

    def extract_data(self, response) -> List[YouTubeVideo]:
        videos = []
        for playlist_item in response['items']:
            video = map_playlist_item_to_video(playlist_item)
            videos.append(video)
        return videos

    def get_function(self, resource: googleapiclient.discovery.Resource) \
            -> Callable:
        return resource.playlistItems().list

    def get_uploads_stream(self, channel_id: str) -> str:
        resource = self.resource_manager.get_resource()
        request = resource.channels().list(
            part='contentDetails',
            id=channel_id)
        response = request.execute()
        return response['items'][0]['contentDetails']['relatedPlaylists'][
            'uploads']


class GetVideoComments(GoogleApiFunction, interface.GetVideoComments):

    def __call__(self, video_id: str, limit: int = inf) -> List[YouTubeComment]:
        page_size = 100  # this is the max
        if page_size > limit:
            page_size = limit
        stop_fn = partial(stop_when_at_limit, limit=limit)
        data = self.paginate(
            stop_fn=stop_fn,
            part='snippet,replies',
            maxResults=page_size,
            videoId=video_id)
        return data

    def extract_data(self, response) -> List[YouTubeComment]:
        comments = []
        for comment_thread in response['items']:
            comments += map_comment_thread_to_comments(comment_thread)
        return comments

    def get_function(self, resource: googleapiclient.discovery.Resource) \
            -> Callable:
        return resource.commentThreads().list


class GetVideo(GoogleApiFunction, interface.GetVideo):

    def __call__(self, video_id: str) -> YouTubeVideo:
        data = self.paginate(
            part='snippet,contentDetails,statistics',
            id=video_id)
        if len(data) == 0:
            raise ValueError(f'No video found for {video_id}.')
        return data[0]

    def extract_data(self, response) -> List[YouTubeVideo]:
        videos = []
        for video in response['items']:
            video = map_video_to_video(video)
            videos.append(video)
        return videos

    def get_function(self, resource: googleapiclient.discovery.Resource) \
            -> Callable:
        return resource.videos().list


class Search(GoogleApiFunction, interface.Search):

    def __call__(self,
                 query: str,
                 start: Optional[datetime] = None,
                 end: Optional[datetime] = None,
                 type: str = 'video',
                 order: str = 'rating',
                 limit: int = inf,
                 channel_id: Optional[str] = None):
        if order not in self.search_orders:
            raise ValueError(f'Unexpected `order`: {order}.')
        if type not in self.search_types:
            raise ValueError(f'Unexpected `type`: {type}.')
        if type in ['channel', 'playlist']:
            raise NotImplementedError('Have not implemented channel or '
                                      'playlist search yet.')
        query = self._escape_pipe(query)
        stop_fn = partial(stop_when_at_limit, limit=limit)
        kwargs = dict(
            part='snippet',
            q=query,
            maxResults=50,
            order=order,
            type=type,
            stop_fn=stop_fn)
        self.current_type = type
        if channel_id:
            kwargs['channelId'] = channel_id
        if start:
            kwargs['publishedAfter'] = self._datetime_to_string_for_api(start)
        if end:
            kwargs['publishedBefore'] = self._datetime_to_string_for_api(end)
        data = self.paginate(**kwargs)
        return data

    def extract_data(self, response) -> List[YouTubeVideo]:
        data = []
        for x in response['items']:
            if self.current_type == 'video':
                x = map_video_search_result_to_video(x)
            elif self.current_type == 'channel':
                raise NotImplementedError
            elif self.current_type == 'playlist':
                raise NotImplementedError
            else:
                raise ValueError(f'Unexpected `type`: {self.current_type}.')
            data.append(x)
        return data

    def get_function(self, resource: googleapiclient.discovery.Resource) \
            -> Callable:
        return resource.search().list


class GoogleYouTubeApi(interface.YouTubeApi):

    def __init__(self, api_keys: Optional[List[str]] = get_keys()):
        self.api_key_manager = ApiKeyManager(api_keys)
        self.resource_manager = ResourceManager(self.api_key_manager)
        super().__init__(
            get_channel=GetChannel(self.resource_manager),
            get_channel_videos=GetChannelVideos(self.resource_manager),
            get_video_comments=GetVideoComments(self.resource_manager),
            get_video=GetVideo(self.resource_manager),
            search=Search(self.resource_manager))
