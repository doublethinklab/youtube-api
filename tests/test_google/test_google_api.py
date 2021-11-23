from datetime import datetime
import unittest

from tests import responses
from youtube_api.google.google_api import *


class TestGetChannel(unittest.TestCase):

    def test_dw(self):
        dw_channel_id = 'UCknLrEdhRCp1aegoMqRaCZg'
        resource = get_resource()
        get_channel = GetChannel(resource)
        dw = get_channel(dw_channel_id)
        self.assertIsInstance(dw, Channel)
        self.assertEqual(dw_channel_id, dw.id)


class TestGetChannelVideos(unittest.TestCase):

    def test_get_uploads_stream(self):
        dw_channel_id = 'UCknLrEdhRCp1aegoMqRaCZg'
        resource = get_resource()
        get_channel_videos = GetChannelVideos(resource)
        stream = get_channel_videos.get_uploads_stream(dw_channel_id)
        expected = 'UUknLrEdhRCp1aegoMqRaCZg'
        self.assertEqual(expected, stream)

    def get_videos_returned(self):
        dw_channel_id = 'UCknLrEdhRCp1aegoMqRaCZg'
        resource = get_resource()
        get_channel_videos = GetChannelVideos(resource)
        videos = get_channel_videos(
            channel_id=dw_channel_id,
            limit=5)
        self.assertEqual(5, len(videos))
        for video in videos:
            self.assertIsInstance(video, Video)


class TestGetVideoComments(unittest.TestCase):

    def test_dw_case(self):
        video_id = '5x5UxqKM7-Y'
        resource = get_resource()
        get_video_comments = GetVideoComments(resource)
        comments = get_video_comments(video_id=video_id, limit=5)
        self.assertGreaterEqual(len(comments), 5)  # may have replies
        for comment in comments:
            self.assertIsInstance(comment, Comment)


class TestGetVideo(unittest.TestCase):

    def test_dw_case(self):
        video_id = '5x5UxqKM7-Y'
        resource = get_resource()
        get_video = GetVideo(resource)
        video = get_video(video_id=video_id)
        self.assertIsNotNone(video)
        self.assertIsInstance(video, Video)
        self.assertEqual(video_id, video.id)
