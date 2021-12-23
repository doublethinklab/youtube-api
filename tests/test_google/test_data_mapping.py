from datetime import datetime
import unittest

from freezegun import freeze_time

from tests import responses
from data_structures.youtube import *
from youtube_api.google.data_mapping import *


class TestMapChannelToChannel(unittest.TestCase):

    def test_dw(self):
        response = responses.list_channels_dw
        channel = response['items'][0]
        channel = map_channel_to_channel(channel)
        expected = YouTubeChannel(
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


class TestMapCommentToComment(unittest.TestCase):

    @freeze_time(datetime(2021, 10, 15, 14, 35, 30))
    def test_dw_comment_1(self):
        comment = responses.dw_comment_thread_1['snippet']['topLevelComment']
        comment = map_comment_to_comment(
            comment, 'UgzsG9SRCC7R1x_89zV4AaABAg')
        expected = YouTubeComment(
            id='UgzsG9SRCC7R1x_89zV4AaABAg',
            video_id='5UMT7RUaXBk',
            author_channel_id='UCFD9yhG2kFIR65YadjYR5BA',
            comment_thread_id='UgzsG9SRCC7R1x_89zV4AaABAg',
            replied_to_comment_id=None,
            created_at=datetime(2021, 7, 26, 8, 26, 42),
            text='Shhh dont speak about it on public. Chinese are very '
                 'sensitive people.\nImram khan, pak caliphe',
            channel=YouTubeChannel(
                id='UCFD9yhG2kFIR65YadjYR5BA',
                title='Antonio Ribeiro'),
            stats=[
                YouTubeCommentStats(
                    comment_id='UgzsG9SRCC7R1x_89zV4AaABAg',
                    collected_at=datetime(2021, 10, 15, 14, 35, 30),
                    num_likes=0,
                    num_replies=0)
            ])
        self.assertEqual(comment, expected)

    @freeze_time(datetime(2021, 10, 15, 14, 35, 30))
    def test_buggy_comment_1(self):
        comment = responses.buggy_comment1
        comment = map_comment_to_comment(
            comment, 'whatever')
        expected = YouTubeComment(
            id='UgxPf-iLTjain_B66y94AaABAg',
            video_id='PKkp3yjl0s4',
            author_channel_id=None,
            comment_thread_id='whatever',
            replied_to_comment_id=None,
            created_at=datetime(2021, 10, 5, 7, 5, 39),
            text='Good!',
            channel=None,
            stats=[
                YouTubeCommentStats(
                    comment_id='UgxPf-iLTjain_B66y94AaABAg',
                    collected_at=datetime(2021, 10, 15, 14, 35, 30),
                    num_likes=0,
                    num_replies=0)
            ])
        self.assertEqual(comment, expected)


class TestMapCommentThreadToComments(unittest.TestCase):

    @freeze_time(datetime(2021, 10, 15, 14, 35, 30))
    def test_dw_comment_thread_with_reply(self):
        comment_thread = responses.dw_comment_thread_with_reply
        comments = map_comment_thread_to_comments(comment_thread)
        expected = [
            YouTubeComment(
                id='UgxqGWcF4_j3P970oQp4AaABAg',
                video_id='5UMT7RUaXBk',
                author_channel_id='UCicrxSWGfa8A54N8viAPFTA',
                comment_thread_id='UgxqGWcF4_j3P970oQp4AaABAg',
                replied_to_comment_id=None,
                created_at=datetime(2020, 3, 6, 1, 37, 22),
                text="China is both communist and fascist.\r\nAnd now it has "
                     "spread the #corona virus to the world.\r\nDon't buy "
                     "Chinese!\r\nThat 's enough.",
                channel=YouTubeChannel(
                    id='UCicrxSWGfa8A54N8viAPFTA',
                    title='jhon free'),
                stats=[
                    YouTubeCommentStats(
                        comment_id='UgxqGWcF4_j3P970oQp4AaABAg',
                        collected_at=datetime(2021, 10, 15, 14, 35, 30),
                        num_likes=0,
                        num_replies=1),
                ]),
            YouTubeComment(
                id='UgxqGWcF4_j3P970oQp4AaABAg.95qRmatwk-z95sC9EDIvTC',
                video_id='5UMT7RUaXBk',
                author_channel_id='UC03Wk-Gp9gNg_STwgleQsFA',
                comment_thread_id='UgxqGWcF4_j3P970oQp4AaABAg',
                replied_to_comment_id='UgxqGWcF4_j3P970oQp4AaABAg',
                created_at=datetime(2020, 3, 6, 17, 59, 16),
                text='jhon free  Lol.. Most stuff in the stores is made in '
                     'China',
                channel=YouTubeChannel(
                    id='UC03Wk-Gp9gNg_STwgleQsFA',
                    title='Hal Asimov'),
                stats=[
                    YouTubeCommentStats(
                        comment_id='UgxqGWcF4_j3P970oQp4AaABAg.95qRmatwk-z95sC9EDIvTC',
                        collected_at=datetime(2021, 10, 15, 14, 35, 30),
                        num_likes=0,
                        num_replies=0),
                ]),
        ]
        self.assertEqual(expected, comments)


class TestMapPlaylistItemToVideo(unittest.TestCase):

    @freeze_time(datetime(2021, 10, 15, 14, 35, 30))
    def test_dw_case(self):
        playlist_item = responses.dw_playlist_item
        video = map_playlist_item_to_video(playlist_item)
        expected = YouTubeVideo(
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
            stats=[],
            tags=[])
        self.assertEqual(expected, video)


class TestMapVideoToVideo(unittest.TestCase):

    @freeze_time(datetime(2021, 10, 15, 14, 35, 30))
    def test_dw_video_item(self):
        video = responses.dw_video
        video = map_video_to_video(video)
        tags = [
            'DW News',
            'Cumbre Vieja',
            'la palma',
            'la palma volcano',
            'volcano eruption']
        expected = YouTubeVideo(
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
            duration='PT40S',
            dimension='2d',
            definition='hd',
            projection='rectangular',
            stats=[
                YouTubeVideoStats(
                    video_id='5x5UxqKM7-Y',
                    collected_at=datetime(2021, 10, 15, 14, 35, 30),
                    num_views=2502,
                    num_likes=97,
                    num_dislikes=2,
                    num_comments=17),
            ],
            tags=[
                YouTubeVideoTag(video_id='5x5UxqKM7-Y', tag=tag)
                for tag in tags
            ])
        self.assertEqual(expected, video)


class TestMapVideoSearchResultsToVideo(unittest.TestCase):

    def test_case_1(self):
        response = responses.search_video_response['items'][0]
        video = map_video_search_result_to_video(response)
        expected = YouTubeVideo(
            id='asnfjccX25I',
            channel_id='UClOKvk6VitvUv2BfEvR6_DQ',
            created_at=datetime(2021, 3, 25, 10, 42, 3),
            title='Picking cotton by machine in Xinjiang，China',
            description="Picking cotton by machine in Xinjiang,China.",
            stats=[],
            tags=[])
        self.assertEqual(expected, video)
