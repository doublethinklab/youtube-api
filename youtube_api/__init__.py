from youtube_api.google import google_api
from youtube_api.interface import YouTubeApiBase


class YouTubeApi(YouTubeApiBase):
    """Singular implementation of the interface to be used by consumers.

    To change implementation details, swap out the functions passed to the base
    constructor.
    """

    def __init__(self):
        # only get one of these and share around
        resource = google_api.get_resource()
        super().__init__(
            get_channel=google_api.GetChannel(resource),
            get_channel_videos=google_api.GetChannelVideos(resource),
            get_video_comments=google_api.GetVideoComments(resource),
            get_video=google_api.GetVideo(resource))
