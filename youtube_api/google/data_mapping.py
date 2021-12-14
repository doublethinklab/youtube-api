from datetime import datetime
from typing import Any, Dict, List, Union

from data_structures.youtube import *


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


def attr_or_none(mapping: Dict, keys: List[str], cast_fn=None) \
        -> Union[Any, None]:
    for ix, key in enumerate(keys):
        if key in mapping:
            if ix == len(keys) - 1:
                value = mapping[key]
                if cast_fn:
                    return cast_fn(value)
                else:
                    return value
            else:
                mapping = mapping[key]
        else:
            return None


def map_channel_to_channel(channel: Dict) -> YouTubeChannel:
    return YouTubeChannel(
        id=channel['id'],
        title=channel['snippet']['title'],
        description=attr_or_none(channel['snippet'], ['description']),
        lang=attr_or_none(channel['snippet'], ['defaultLanguage']),
        country=attr_or_none(channel['snippet'], ['country']),
        created_at=api_string_to_datetime(channel['snippet']['publishedAt']))


def map_comment_to_comment(comment: Dict,
                           comment_thread_id: str,
                           num_replies: int = 0) -> YouTubeComment:
    return YouTubeComment(
        id=comment['id'],
        video_id=comment['snippet']['videoId'],
        author_channel_id=comment['snippet']['authorChannelId']['value'],
        comment_thread_id=comment_thread_id,
        replied_to_comment_id=attr_or_none(comment['snippet'], ['parentId']),
        created_at=api_string_to_datetime(comment['snippet']['publishedAt']),
        text=comment['snippet']['textOriginal'],
        channel=YouTubeChannel(
            id=comment['snippet']['authorChannelId']['value'],
            title=comment['snippet']['authorDisplayName']),
        stats=[map_comment_to_comment_stats(comment, num_replies)])


def map_comment_thread_to_comments(comment_thread: Dict) \
        -> List[YouTubeComment]:
    comments = []
    comment_thread_id = comment_thread['id']
    top_level_comment = map_comment_to_comment(
        comment=comment_thread['snippet']['topLevelComment'],
        comment_thread_id=comment_thread_id,
        num_replies=comment_thread['snippet']['totalReplyCount'])
    comments.append(top_level_comment)
    if 'replies' in comment_thread:
        for comment in comment_thread['replies']['comments']:
            comment = map_comment_to_comment(comment, comment_thread_id)
            comments.append(comment)
    return comments


def map_comment_to_comment_stats(comment: Dict, num_replies: int = 0) \
        -> YouTubeCommentStats:
    # NOTE: by definition comments other than root have 0
    #  so let the number be passed in if handling a root comment
    return YouTubeCommentStats(
        comment_id=comment['id'],
        collected_at=datetime.utcnow(),
        num_likes=comment['snippet']['likeCount'],
        num_replies=num_replies)


def map_comment_thread_to_comment_stats(comment_thread: Dict) \
        -> YouTubeCommentStats:
    return YouTubeCommentStats(
        comment_id=comment_thread['snippet']['topLevelComment']['id'],
        collected_at=datetime.utcnow(),
        num_likes=comment_thread['snippet']['topLevelComment']['snippet']['likeCount'],
        num_replies=comment_thread['totalReplyCount'])


def map_playlist_item_to_video(playlist_item: Dict) -> YouTubeVideo:
    return YouTubeVideo(
        id=playlist_item['snippet']['resourceId']['videoId'],
        channel_id=playlist_item['snippet']['channelId'],
        created_at=api_string_to_datetime(playlist_item['snippet']['publishedAt']),
        title=playlist_item['snippet']['title'],
        description=playlist_item['snippet']['description'],
        stats=[])


def map_video_to_video(video: Dict) -> YouTubeVideo:
    return YouTubeVideo(
        id=video['id'],
        channel_id=video['snippet']['channelId'],
        created_at=api_string_to_datetime(video['snippet']['publishedAt']),
        title=video['snippet']['title'],
        description=video['snippet']['description'],
        duration=video['contentDetails']['duration'],
        dimension=video['contentDetails']['dimension'],
        definition=video['contentDetails']['definition'],
        projection=video['contentDetails']['projection'],
        stats=[map_video_to_video_stats(video)])


def map_video_search_result_to_video(result: Dict) -> YouTubeVideo:
    return YouTubeVideo(
        id=result['id']['videoId'],
        channel_id=result['snippet']['channelId'],
        created_at=api_string_to_datetime(result['snippet']['publishedAt']),
        title=result['snippet']['title'],
        description=result['snippet']['description'],
        stats=[])


def map_video_to_video_stats(video: Dict) -> YouTubeVideoStats:
    return YouTubeVideoStats(
        video_id=video['id'],
        collected_at=datetime.utcnow(),
        num_views=attr_or_none(video, ['statistics', 'viewCount'], int),
        num_likes=attr_or_none(video, ['statistics', 'likeCount'], int),
        num_dislikes=attr_or_none(video, ['statistics', 'dislikeCount'], int),
        num_comments=attr_or_none(video, ['statistics', 'commentCount'], int))
