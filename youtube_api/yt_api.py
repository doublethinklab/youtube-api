import os
from typing import Dict, List

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError


class Api:

    def __init__(self):
        scopes = [
            'https://www.googleapis.com/auth/youtube.readonly',
            'https://www.googleapis.com/auth/youtube',
            'https://www.googleapis.com/auth/youtube.force-ssl'
        ]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        api_service_name = 'youtube'
        api_version = 'v3'
        client_secrets_file = 'oauth.json'

        # Get credentials and create an API client
        flow = google_auth_oauthlib \
            .flow \
            .InstalledAppFlow \
            .from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

    def get_comments(self, video_id) -> List[Dict]:
        comments = []
        page_size = 100  # this is the max
        request = self.youtube.commentThreads().list(
            part='snippet,replies',
            maxResults=page_size,
            videoId=video_id)
        try:
            response = request.execute()
        except HttpError as e:
            if e.error_details[0]['reason'] == 'commentsDisabled':
                return []
            raise e
        comments += response['items']
        finished = 'nextPageToken' not in response
        while not finished:
            request = self.youtube.commentThreads().list(
                part='snippet,replies',
                maxResults=page_size,
                pageToken=response['nextPageToken'],
                videoId=video_id)
            response = request.execute()
            comments += response['items']
            finished = 'nextPageToken' not in response
        return comments

    def get_uploads_stream(self, channel_id: str) -> str:
        request = self.youtube.channels().list(
            part='contentDetails',
            id=channel_id)
        response = request.execute()
        return response['items'][0]['contentDetails']['relatedPlaylists'][
            'uploads']

    def get_channel_details(self, channel_id: str):
        request = self.youtube.channels().list(
            id=channel_id,
            part='contentDetails,snippet,statistics,topicDetails')
        response = request.execute()
        return response

    def get_channel_videos(self, channel_id: str) -> List[Dict]:
        uploads_stream = self.get_uploads_stream(channel_id)
        videos = []
        # NOTE: statistics is not a valid part here (dunno why)
        # so if you want statistics, it needs to be a separate call (below)
        request = self.youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_stream)
        response = request.execute()
        videos += response['items']
        finished = 'nextPageToken' not in response
        while not finished:
            request = self.youtube.playlistItems().list(
                part='snippet',
                pageToken=response['nextPageToken'],
                playlistId=uploads_stream)
            response = request.execute()
            videos += response['items']
            finished = 'nextPageToken' not in response
        return videos

    def video_info(self, video_id: str) -> Dict:
        return self.youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id).execute()
