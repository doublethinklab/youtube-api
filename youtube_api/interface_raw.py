"""Interface definition."""
from datetime import datetime
from math import inf
from typing import Dict, List, Optional


class GetChannel:

    def __call__(
            self,
            channel_id: str
    ) -> List[Dict]:
        raise NotImplementedError


class GetChannelStreamId:

    def __call__(
            self,
            channel_id: str
    ) -> str | None:
        raise NotImplementedError


class GetChannelVideos:

    def __call__(
            self,
            channel_stream_id: str,
            limit: int = inf,
            start: Optional[datetime] = None,
            end: Optional[datetime] = None
    ) -> List[Dict]:
        raise NotImplementedError


class GetVideoComments:

    def __call__(
            self,
            video_id: str,
            limit: int = inf
    ) -> List[Dict]:
        raise NotImplementedError


class GetVideo:

    def __call__(
            self,
            video_id: str
    ) -> List[Dict]:
        raise NotImplementedError


class Search:
    """Search resources.

    https://developers.google.com/youtube/v3/docs/search/list

    Note on query:
    > Your request can also use the Boolean NOT (-) and OR (|) operators to
      exclude videos or to find videos that are associated with one of several
      search terms. For example, to search for videos matching either "boating"
      or "sailing", set the q parameter value to boating|sailing. Similarly, to
      search for videos matching either "boating" or "sailing" but not
      "fishing", set the q parameter value to boating|sailing -fishing. Note
      that the pipe character must be URL-escaped when it is sent in your API
      request. The URL-escaped value for the pipe character is %7C.
    """

    search_orders = [
        'date', 'rating', 'relevance', 'title', 'videoCount', 'viewCount'
    ]
    search_types = [
        'channel', 'playlist', 'video',
    ]

    def __call__(
            self,
            query: str,
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            type: str = 'video',
            order: str = 'rating',
            limit: int = inf,
            channel_id: Optional[str] = None
    ) -> List[Dict]:
        raise NotImplementedError

    @staticmethod
    def _escape_pipe(query: str) -> str:
        return query.replace('|', '%7C')


class YouTubeApi:
    """Interface definition."""

    def __init__(
            self,
            get_channel: GetChannel,
            get_channel_stream_id: GetChannelStreamId,
            get_channel_videos: GetChannelVideos,
            get_video_comments: GetVideoComments,
            get_video: GetVideo,
            search: Search
    ):
        self.get_channel = get_channel
        self.get_channel_stream_id = get_channel_stream_id
        self.get_channel_videos = get_channel_videos
        self.get_video_comments = get_video_comments
        self.get_video = get_video
        self.search = search
