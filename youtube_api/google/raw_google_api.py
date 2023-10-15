from datetime import datetime
import logging
from math import inf
import time
from typing import Callable, Dict, List, Optional

import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError

from youtube_api.google.api_key_management import ApiKeyManager, ResourceManager
from youtube_api import interface_raw as interface


class GoogleApiFunction:

    def __init__(
            self,
            resource_manager: ResourceManager,
            debug: bool = False
    ):
        self.resource_manager = resource_manager
        self.debug = debug

    @staticmethod
    def _datetime_to_string_for_api(date_time: datetime) -> str:
        return date_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    def _drop_over_limit(
            self,
            data: List[Dict],
            limit: int = inf,
            start: Optional[datetime] = None
    ) -> List[Dict]:
        if limit != inf:
            data = data[:limit]
        # assumes pagination works back in time
        if start:
            start_str = self._datetime_to_string_for_api(start)
            data = [x for x in data if x['snippet']['publishedAt'] >= start_str]
        return data

    @staticmethod
    def _empty(response: Dict) -> bool:
        return not response or 'items' not in response

    def _get_function(
            self,
            resource: googleapiclient.discovery.Resource
    ) -> Callable:
        raise NotImplementedError

    @staticmethod
    def _get_next_page(response):
        return response['nextPageToken'] \
            if 'nextPageToken' in response \
            else None

    def _stop(
            self,
            data: List[Dict],
            limit: int = inf,
            start: Optional[datetime] = None
    ) -> bool:
        if limit != inf:
            return len(data) >= limit
        # assumes pagination works back in time
        if start:
            start_str = self._datetime_to_string_for_api(start)
            min_publish_date = min(x['snippet']['publishedAt'] for x in data)
            return start_str >= min_publish_date
        return False

    def _paginate(
            self,
            limit: int = inf,
            start: Optional[datetime] = None,
            **fn_args
    ) -> List[Dict]:
        data = []
        response = self._wait_while_rate_limited(**fn_args)
        if self._empty(response):
            return data
        data = response['items']
        next_page_token = self._get_next_page(response)
        while next_page_token and not self._stop(data, limit, start):
            fn_args['pageToken'] = next_page_token
            response = self._wait_while_rate_limited(**fn_args)
            if self._empty(response):
                return data
            data += response['items']
            next_page_token = self._get_next_page(response)
        data = self._drop_over_limit(data, limit, start)
        return data

    def _wait_while_rate_limited(self, **fn_args) -> Dict | None:
        while True:
            try:
                resource = self.resource_manager.get_resource()
                fn = self._get_function(resource)
                request = fn(**fn_args)
                response = request.execute()
                if self.debug:
                    print(response)
                return response
            except HttpError as e:
                if e.error_details[0]['reason'] == 'commentsDisabled':
                    logging.warning(f'Comments disabled.')
                    return None
                elif e.error_details[0]['reason'] == 'videoNotFound':
                    logging.warning('Video not found.')
                    return None
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
                elif e.error_details[0]['reason'] == 'badRequest':
                    # this doesn't appear to be transient, error for now
                    logging.warning(f'"Bad request," API key was '
                                    f'"{self.resource_manager.current_api_key}"'
                                    f'.')
                    raise e
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

    def __call__(self, channel_id: str) -> List[Dict]:
        return self._paginate(
            id=channel_id,
            part='contentDetails,snippet,statistics,topicDetails')

    def _get_function(
            self,
            resource: googleapiclient.discovery.Resource
    ) -> Callable:
        return resource.channels().list


class GetChannelStreamId(GoogleApiFunction, interface.GetChannelStreamId):

    def __call__(self, channel_id: str) -> str | None:
        response = self._paginate(
            part='contentDetails',
            id=channel_id)
        if len(response) == 0:
            return None
        data = response[0]
        if 'contentDetails' not in data:
            return None
        content_details = data['contentDetails']
        if 'relatedPlaylists' not in content_details:
            return None
        related_playlists = content_details['relatedPlaylists']
        if 'uploads' not in related_playlists:
            return None
        return related_playlists['uploads']

    def _get_function(
            self,
            resource: googleapiclient.discovery.Resource
    ) -> Callable:
        return resource.channels().list


class GetChannelVideos(GoogleApiFunction, interface.GetChannelVideos):

    def __call__(
            self,
            channel_stream_id: str,
            limit: int = inf,
            start: Optional[datetime] = None,
            end: Optional[datetime] = None
    ) -> List[Dict]:
        page_size = 50  # 50 is the max - https://developers.google.com/youtube/v3/docs/channels/list
        return self._paginate(
            limit=limit,
            start=start,
            part='snippet',
            playlistId=channel_stream_id,
            maxResults=page_size)

    def _get_function(self, resource: googleapiclient.discovery.Resource) \
            -> Callable:
        return resource.playlistItems().list


class GetVideoComments(GoogleApiFunction, interface.GetVideoComments):

    def __call__(
            self,
            video_id: str,
            limit: int = inf
    ) -> List[Dict]:
        page_size = 100  # this is the max
        if page_size > limit:
            page_size = limit
        return self._paginate(
            limit=limit,
            part='snippet,replies',
            maxResults=page_size,
            videoId=video_id)

    def _get_function(self, resource: googleapiclient.discovery.Resource) \
            -> Callable:
        return resource.commentThreads().list


class GetVideo(GoogleApiFunction, interface.GetVideo):

    def __call__(
            self,
            video_id: str
    ) -> List[Dict]:
        return self._paginate(
            part='snippet,contentDetails,statistics',
            id=video_id)

    def _get_function(self, resource: googleapiclient.discovery.Resource) \
            -> Callable:
        return resource.videos().list


class Search(GoogleApiFunction, interface.Search):

    def __call__(
            self,
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
        fn_args = dict(
            part='snippet',
            q=query,
            maxResults=50,
            order=order,
            type=type)
        self.current_type = type
        if channel_id:
            fn_args['channelId'] = channel_id
        if start:
            fn_args['publishedAfter'] = self._datetime_to_string_for_api(start)
        if end:
            fn_args['publishedBefore'] = self._datetime_to_string_for_api(end)
        data = self._paginate(limit=limit, start=start, **fn_args)
        return data

    def _get_function(
        self,
        resource: googleapiclient.discovery.Resource
    ) -> Callable:
        return resource.search().list


class GoogleYouTubeApi(interface.YouTubeApi):

    def __init__(self):
        self.api_key_manager = ApiKeyManager()
        self.resource_manager = ResourceManager(self.api_key_manager)
        super().__init__(
            get_channel=GetChannel(self.resource_manager),
            get_channel_stream_id=GetChannelStreamId(self.resource_manager),
            get_channel_videos=GetChannelVideos(self.resource_manager),
            get_video_comments=GetVideoComments(self.resource_manager),
            get_video=GetVideo(self.resource_manager),
            search=Search(self.resource_manager))
