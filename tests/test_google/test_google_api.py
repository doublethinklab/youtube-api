from datetime import datetime
import unittest

from data_structures.youtube import *
from freezegun import freeze_time

from tests import responses
from youtube_api.google.google_api import *


def get_resource_manager():
    api_key_manager = ApiKeyManager(api_keys=[os.environ['API_KEY']])
    resource_manager = ResourceManager(api_key_manager)
    return resource_manager


class TestApiKeyManager(unittest.TestCase):

    @freeze_time('2021-12-11 17:09:00')
    def test_get_mins_diff(self):
        exceeded_time = datetime(2021, 12, 11, 16, 59, 0)
        mins_diff = ApiKeyManager._get_mins_diff(exceeded_time)
        self.assertEqual(10, mins_diff)

    @freeze_time('2021-12-11 17:09:00')
    def test_get_next_available_key_returns_max_diff_when_available(self):
        api_key_manager = ApiKeyManager(api_keys=['a', 'b'], wait_mins=60)
        api_key_manager.api_key_to_exceeded_time = {
            'a': datetime(2021, 12, 11, 15, 55, 0),
            'b': datetime(2021, 12, 11, 15, 59, 0)}
        api_key = api_key_manager._get_next_available_key()
        self.assertEqual('a', api_key)

    @freeze_time('2021-12-11 17:09:00')
    def test_get_next_available_key_returns_none_when_none_available(self):
        api_key_manager = ApiKeyManager(api_keys=['a', 'b'], wait_mins=60)
        api_key_manager.api_key_to_exceeded_time = {
            'a': datetime(2021, 12, 11, 16, 55, 0),
            'b': datetime(2021, 12, 11, 16, 59, 0)}
        api_key = api_key_manager._get_next_available_key()
        self.assertIsNone(api_key)

    @freeze_time('2021-12-11 17:09:00')
    def test_key_returns_key_when_available(self):
        api_key_manager = ApiKeyManager(api_keys=['a', 'b'], wait_mins=60)
        api_key_manager.api_key_to_exceeded_time = {
            'a': datetime(2021, 12, 11, 15, 55, 0),
            'b': datetime(2021, 12, 11, 15, 59, 0)}
        api_key = api_key_manager.get_key()
        self.assertEqual('a', api_key)

    @freeze_time('2021-12-11 17:09:00')
    def test_report_quota_exceeded(self):
        api_key_manager = ApiKeyManager(api_keys=['a', 'b'], wait_mins=60)
        api_key_manager.api_key_to_exceeded_time = {
            'a': datetime(2021, 12, 11, 15, 55, 0),
            'b': datetime(2021, 12, 11, 15, 59, 0)}
        api_key_manager.report_quota_exceeded('a')
        self.assertEqual(datetime(2021, 12, 11, 17, 9, 0),
                         api_key_manager.api_key_to_exceeded_time['a'])


class TestResourceManager(unittest.TestCase):

    @freeze_time('2021-12-11 17:41:00')
    def test_report_quota_exceeded(self):
        api_key_manager = ApiKeyManager(['a', 'b'])
        resource_manager = ResourceManager(api_key_manager)
        resource_manager.current_api_key = 'a'
        resource_manager.current_resource = 'Something non-null'
        resource_manager.report_quota_exceeded()
        self.assertEqual(datetime(2021, 12, 11, 17, 41, 0),
                         api_key_manager.api_key_to_exceeded_time['a'])
        self.assertIsNone(resource_manager.current_api_key)
        self.assertIsNone(resource_manager.current_resource)


class TestGoogleApiFunction(unittest.TestCase):

    def test_datetime_to_string_for_api(self):
        date_time = datetime(2021, 1, 28, 2, 33, 32)
        expected = '2021-01-28T02:33:32Z'
        result = GoogleApiFunction._datetime_to_string_for_api(date_time)
        self.assertEqual(expected, result)


class TestGetChannel(unittest.TestCase):

    def test_dw(self):
        resource_manager = get_resource_manager()
        get_channel = GetChannel(resource_manager)
        dw_channel_id = 'UCknLrEdhRCp1aegoMqRaCZg'
        dw = get_channel(dw_channel_id)
        self.assertIsInstance(dw, YouTubeChannel)
        self.assertEqual(dw_channel_id, dw.id)


class TestGetChannelVideos(unittest.TestCase):

    def test_get_uploads_stream(self):
        resource_manager = get_resource_manager()
        get_channel_videos = GetChannelVideos(resource_manager)
        dw_channel_id = 'UCknLrEdhRCp1aegoMqRaCZg'
        stream = get_channel_videos.get_uploads_stream(dw_channel_id)
        expected = 'UUknLrEdhRCp1aegoMqRaCZg'
        self.assertEqual(expected, stream)

    def get_videos_returned(self):
        resource_manager = get_resource_manager()
        get_channel_videos = GetChannelVideos(resource_manager)
        dw_channel_id = 'UCknLrEdhRCp1aegoMqRaCZg'
        videos = get_channel_videos(
            channel_id=dw_channel_id,
            limit=5)
        self.assertEqual(5, len(videos))
        for video in videos:
            self.assertIsInstance(video, YouTubeVideo)


class TestGetVideoComments(unittest.TestCase):

    def test_dw_case(self):
        resource_manager = get_resource_manager()
        get_video_comments = GetVideoComments(resource_manager)
        video_id = '5x5UxqKM7-Y'
        comments = get_video_comments(video_id=video_id, limit=5)
        self.assertGreaterEqual(len(comments), 5)  # may have replies
        for comment in comments:
            self.assertIsInstance(comment, YouTubeComment)


class TestGetVideo(unittest.TestCase):

    def test_dw_case(self):
        resource_manager = get_resource_manager()
        get_video = GetVideo(resource_manager)
        video_id = '5x5UxqKM7-Y'
        video = get_video(video_id=video_id)
        self.assertIsNotNone(video)
        self.assertIsInstance(video, YouTubeVideo)
        self.assertEqual(video_id, video.id)


class TestSearch(unittest.TestCase):

    def test_channel_id_and_start_and_end_dates(self):
        # Kelly Sydney (UClOKvk6VitvUv2BfEvR6_DQ)
        # video1:
        #     title: 90% of the cotton in Xinjiang, China is picked by machines.
        #            How can it be called forced labor?
        #     published: 2021-03-25 04:04UTC
        # video2:
        #     title: Picking cotton by machine in Xinjiang，China
        #     published: 2021-03-25 10:42UTC
        resource_manager = get_resource_manager()
        search = Search(resource_manager)
        data = search(
            query='xinjiang cotton',
            start=datetime(2021, 3, 25, 10, 0, 0),
            end=datetime(2021, 3, 25, 12, 0, 0),
            channel_id='UClOKvk6VitvUv2BfEvR6_DQ')
        self.assertEqual(1, len(data))
        video = data[0]
        self.assertEqual(
            'Picking cotton by machine in Xinjiang，China', video.title)

    # def test_complex_query1(self):
    #     # NOTE: this was originally a playground. I determined:
    #     #    - Cannot do a complex query like `admire salon | primary students`,
    #     #      that returns zero results.
    #     #    - Using parentheses to group the same - e.g. `(admire salon)|...`
    #     #    - So for now just giving up on complex queries with this.
    #     # GuliGina
    #     # channel_id: UC_uwGDgtAVOQmb0zEMvftDQ
    #     # video1:
    #     #    title: Come and admire the beauty and hair salon #Xinjiang
    #     #    created_at: 2021-12-08
    #     # video2:
    #     #    title: Xinjiang has been promoting the development of preschool
    #     #           education for a long time. #Xinjiang
    #     #    created_at: 2021-12-09
    #     # video3:
    #     #    title: The brothers are getting better and better #Xinjiang
    #     #    created_at: 2021-12-08
    #     # video4:
    #     #    title: Do you know what primary school students in Xinjiang do
    #     #           in a day?
    #     #    created_at: 2021-11-25
    #     # video5:
    #     #    title: I am very proud that my students are employed when they
    #     #           graduate.
    #     #    created_at: 2021-11-29
    #     resource_manager = get_resource_manager()
    #     search = Search(resource_manager)
    #     query = 'admire salon'
    #     data = search(
    #         query=query,
    #         start=datetime(2021, 11, 20, 0, 0, 0),
    #         end=datetime(2021, 12, 10, 0, 0, 0),
    #         channel_id='UC_uwGDgtAVOQmb0zEMvftDQ')
    #     titles = {x.title for x in data}
    #     expected = {
    #         'Do you know what primary school students in Xinjiang do in a day?',
    #         'Come and admire the beauty and hair salon #Xinjiang',
    #     }
    #     print(titles)
    #     self.assertEqual(2, len(data))
    #     self.assertEqual(expected, titles)
