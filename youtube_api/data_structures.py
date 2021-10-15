"""Common data structures."""
from datetime import datetime
from typing import Optional


class YouTubeData:

    def __eq__(self, other):
        if isinstance(other, type(self)):
            eq = self.__dict__ == other.__dict__
            if eq:
                return True
            else:
                for attr, value in self.__dict__.items():
                    if other.__dict__[attr] != value:
                        print(f'{attr}\t{value} != %s' % other.__dict__[attr])
                return False
        return False

    def to_dict(self):
        return self.__dict__


class Channel(YouTubeData):
    # https://developers.google.com/youtube/v3/docs/channels

    def __init__(self,
                 id: str,
                 title: str,
                 created_at: datetime,
                 description: Optional[str] = None,
                 lang: Optional[str] = None,
                 country: Optional[str] = None):
        self.id = id
        self.title = title
        self.description = description
        self.lang = lang
        self.country = country
        self.created_at = created_at


class Comment(YouTubeData):
    # https://developers.google.com/youtube/v3/docs/comments

    def __init__(self,
                 id: str,
                 video_id: str,
                 author_channel_id: str,
                 comment_thread_id: str,
                 created_at: datetime,
                 text: str,
                 num_likes: int,
                 retrieved: datetime,
                 replied_to_comment_id: Optional[str] = None):
        self.id = id
        self.video_id = video_id
        self.author_channel_id = author_channel_id
        self.comment_thread_id = comment_thread_id
        self.replied_to_comment_id = replied_to_comment_id
        self.created_at = created_at
        self.text = text  # snippet.textOriginal
        self.num_likes = num_likes
        self.retrieved = retrieved


class Video(YouTubeData):
    # https://developers.google.com/youtube/v3/docs/videos

    def __init__(self,
                 id : str,
                 channel_id: str,
                 created_at: datetime,
                 title: str,
                 description: str,
                 retrieved: datetime,
                 num_views: Optional[int] = None,
                 num_likes: Optional[int] = None,
                 num_dislikes: Optional[int] = None,
                 num_comments: Optional[int] = None):
        self.id = id
        self.channel_id = channel_id
        self.created_at = created_at
        self.title = title
        self.description = description
        self.num_views = num_views
        self.num_likes = num_likes
        self.num_dislikes = num_dislikes
        self.num_comments = num_comments
        self.retrieved = retrieved
