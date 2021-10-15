from datetime import datetime
import unittest

from freezegun import freeze_time

from tests import responses
from youtube_api.google_api import *


class TestAdaptChannelToChannel(unittest.TestCase):

    def test_dw(self):
        response = responses.list_channels_dw
        channel = response['items'][0]
        channel = adapt_channel_to_channel(channel)
        expected = Channel(
            id='UCknLrEdhRCp1aegoMqRaCZg',
            title='DW News',
            description='Journalism that’s Made for Minds. Follow us for '
                        'global news and analysis from the heart of Europe. '
                        'DW News delivers the world\'s breaking news while '
                        'going deep beneath the surface of what\'s going on. '
                        'Correspondents on the ground and in the studio '
                        'provide their detailed analysis and insights on '
                        'issues that affect our viewers. \n\nDeutsche Welle '
                        'is Germany’s international broadcaster, producing '
                        'content in 30 languages. We independently report '
                        'social, political and economic developments in '
                        'Germany and Europe, incorporating both German and '
                        'other perspectives. DW hopes to promote '
                        'understanding between different cultures and peoples. '
                        '\n\nWhile funded by the German government, the work '
                        'of DW is regulated by the Deutsche Welle Act '
                        '(http://p.dw.com/p/17MtP), meaning content is always '
                        'independent of government influence. \n\nWe ask that '
                        'you please keep comments and discussions on this '
                        'channel clean and respectful. For further information '
                        'please click the \'DW Netiquette\' link below.',
            lang=None,
            country='DE',
            created_at=datetime(2007, 9, 4, 12, 4, 10))
        self.assertEqual(expected, channel)


class TestAdaptCommentToComment(unittest.TestCase):

    @freeze_time(datetime(2021, 10, 15, 14, 35, 30))
    def test_dw_comment_1(self):
        comment = responses.dw_comment_thread_1['snippet']['topLevelComment']
        comment = adapt_comment_to_comment(
            comment, 'UgzsG9SRCC7R1x_89zV4AaABAg')
        expected = Comment(
            id='UgzsG9SRCC7R1x_89zV4AaABAg',
            video_id='5UMT7RUaXBk',
            author_channel_id='UCFD9yhG2kFIR65YadjYR5BA',
            comment_thread_id='UgzsG9SRCC7R1x_89zV4AaABAg',
            replied_to_comment_id=None,
            created_at=datetime(2021, 7, 26, 8, 26, 42),
            text='Shhh dont speak about it on public. Chinese are very '
                 'sensitive people.\nImram khan, pak caliphe',
            num_likes=0,
            retrieved=datetime(2021, 10, 15, 14, 35, 30))
        self.assertEqual(comment, expected)


class TestAdaptCommentThreadToComments(unittest.TestCase):

    @freeze_time(datetime(2021, 10, 15, 14, 35, 30))
    def test_dw_comment_thread_with_reply(self):
        comment_thread = responses.dw_comment_thread_with_reply
        comments = adapt_comment_thread_to_comments(comment_thread)
        expected = [
            Comment(
                id='UgxqGWcF4_j3P970oQp4AaABAg',
                video_id='5UMT7RUaXBk',
                author_channel_id='UCicrxSWGfa8A54N8viAPFTA',
                comment_thread_id='UgxqGWcF4_j3P970oQp4AaABAg',
                replied_to_comment_id=None,
                created_at=datetime(2020, 3, 6, 1, 37, 22),
                text="China is both communist and fascist.\r\nAnd now it has "
                     "spread the #corona virus to the world.\r\nDon't buy "
                     "Chinese!\r\nThat 's enough.",
                num_likes=0,
                retrieved=datetime(2021, 10, 15, 14, 35, 30)),
            Comment(
                id='UgxqGWcF4_j3P970oQp4AaABAg.95qRmatwk-z95sC9EDIvTC',
                video_id='5UMT7RUaXBk',
                author_channel_id='UC03Wk-Gp9gNg_STwgleQsFA',
                comment_thread_id='UgxqGWcF4_j3P970oQp4AaABAg',
                replied_to_comment_id='UgxqGWcF4_j3P970oQp4AaABAg',
                created_at=datetime(2020, 3, 6, 17, 59, 16),
                text='jhon free  Lol.. Most stuff in the stores is made in '
                     'China',
                num_likes=0,
                retrieved=datetime(2021, 10, 15, 14, 35, 30)),
        ]
        self.assertEqual(expected, comments)


class TestAdaptPlaylistItemToVideo(unittest.TestCase):

    @freeze_time(datetime(2021, 10, 15, 14, 35, 30))
    def test_dw_case(self):
        playlist_item = responses.dw_playlist_item
        video = adapt_playlist_item_to_video(playlist_item)
        expected = Video(
            id='5x5UxqKM7-Y',
            channel_id='UCknLrEdhRCp1aegoMqRaCZg',
            created_at=datetime(2021, 10, 15, 8, 0, 24),
            title='La Palma volcano: Massive lava flow pushes over the '
                  'boundary of evacuated area | DW News',
            description="The Cumbre Vieja volcano on Spain's Canary Islands "
                        "has been erupting for almost four weeks, but lava "
                        "flow reached a new level on Thursday.\nScientists "
                        "say magma has been pouring out of the main cone of "
                        "the La Palma volcano at growing speed and volume. "
                        "The river of red-hot lava has now pushed over the "
                        "boundary of the evacuated area, forcing several "
                        "hundred more people to flee their homes. An "
                        "earthquake also shook the island of La Palma on "
                        "Thursday, the strongest since volcanic activity "
                        "picked up. \n\nSubscribe: https://www.youtube.com"
                        "/user/deutschewelleenglish?sub_confirmation=1\n\n"
                        "For more news go to: http://www.dw.com/en/\nFollow "
                        "DW on social media:\n►Facebook: https://"
                        "www.facebook.com/deutschewellenews/\n►Twitter: "
                        "https://twitter.com/dwnews\n►Instagram: "
                        "https://www.instagram.com/dwnews\nFür Videos in "
                        "deutscher Sprache besuchen Sie: "
                        "https://www.youtube.com/dwdeutsch",
            retrieved=datetime(2021, 10, 15, 14, 35, 30),
            num_views=None,
            num_likes=None,
            num_dislikes=None,
            num_comments=None)
        self.assertEqual(expected, video)


class TestAdaptVideoToVideo(unittest.TestCase):

    @freeze_time(datetime(2021, 10, 15, 14, 35, 30))
    def test_dw_video_item(self):
        video = responses.dw_video
        video = adapt_video_to_video(video)
        expected = Video(
            id='5x5UxqKM7-Y',
            channel_id='UCknLrEdhRCp1aegoMqRaCZg',
            created_at=datetime(2021, 10, 15, 8, 0, 24),
            title='La Palma volcano: Massive lava flow pushes over the '
                  'boundary of evacuated area | DW News',
            description="The Cumbre Vieja volcano on Spain's Canary Islands "
                        "has been erupting for almost four weeks, but lava "
                        "flow reached a new level on Thursday.\nScientists "
                        "say magma has been pouring out of the main cone of "
                        "the La Palma volcano at growing speed and volume. "
                        "The river of red-hot lava has now pushed over the "
                        "boundary of the evacuated area, forcing several "
                        "hundred more people to flee their homes. An "
                        "earthquake also shook the island of La Palma on "
                        "Thursday, the strongest since volcanic activity "
                        "picked up. \n\nSubscribe: https://www.youtube.com"
                        "/user/deutschewelleenglish?sub_confirmation=1\n\n"
                        "For more news go to: http://www.dw.com/en/\nFollow "
                        "DW on social media:\n►Facebook: https://"
                        "www.facebook.com/deutschewellenews/\n►Twitter: "
                        "https://twitter.com/dwnews\n►Instagram: "
                        "https://www.instagram.com/dwnews\nFür Videos in "
                        "deutscher Sprache besuchen Sie: "
                        "https://www.youtube.com/dwdeutsch",
            retrieved=datetime(2021, 10, 15, 14, 35, 30),
            num_views=2502,
            num_likes=97,
            num_dislikes=2,
            num_comments=17)
        self.assertEqual(expected, video)


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
