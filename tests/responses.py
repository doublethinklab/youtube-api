"""Responses from api for testing."""
import json


list_channels_dw = {
  "kind": "youtube#channelListResponse",
  "etag": "Pmdln25-qRdVjshLainibmdO_Qo",
  "pageInfo": {
    "totalResults": 1,
    "resultsPerPage": 5
  },
  "items": [
    {
      "kind": "youtube#channel",
      "etag": "S0e6KCVVXw8Oebx8-F5Bggq6nks",
      "id": "UCknLrEdhRCp1aegoMqRaCZg",
      "snippet": {
        "title": "DW News",
        "description": "Journalism that’s Made for Minds. Follow us for global news and analysis from the heart of Europe. DW News delivers the world's breaking news while going deep beneath the surface of what's going on. Correspondents on the ground and in the studio provide their detailed analysis and insights on issues that affect our viewers. \n\nDeutsche Welle is Germany’s international broadcaster, producing content in 30 languages. We independently report social, political and economic developments in Germany and Europe, incorporating both German and other perspectives. DW hopes to promote understanding between different cultures and peoples. \n\nWhile funded by the German government, the work of DW is regulated by the Deutsche Welle Act (http://p.dw.com/p/17MtP), meaning content is always independent of government influence. \n\nWe ask that you please keep comments and discussions on this channel clean and respectful. For further information please click the 'DW Netiquette' link below.",
        "customUrl": "dwnews",
        "publishedAt": "2007-09-04T12:04:10Z",
        "thumbnails": {
          "default": {
            "url": "https://yt3.ggpht.com/ytc/AKedOLSGYwgujx1VgMYEpdurTfh8NRmOehOXf16DeMKoDfw=s88-c-k-c0x00ffffff-no-rj",
            "width": 88,
            "height": 88
          },
          "medium": {
            "url": "https://yt3.ggpht.com/ytc/AKedOLSGYwgujx1VgMYEpdurTfh8NRmOehOXf16DeMKoDfw=s240-c-k-c0x00ffffff-no-rj",
            "width": 240,
            "height": 240
          },
          "high": {
            "url": "https://yt3.ggpht.com/ytc/AKedOLSGYwgujx1VgMYEpdurTfh8NRmOehOXf16DeMKoDfw=s800-c-k-c0x00ffffff-no-rj",
            "width": 800,
            "height": 800
          }
        },
        "localized": {
          "title": "DW News",
          "description": "Journalism that’s Made for Minds. Follow us for global news and analysis from the heart of Europe. DW News delivers the world's breaking news while going deep beneath the surface of what's going on. Correspondents on the ground and in the studio provide their detailed analysis and insights on issues that affect our viewers. \n\nDeutsche Welle is Germany’s international broadcaster, producing content in 30 languages. We independently report social, political and economic developments in Germany and Europe, incorporating both German and other perspectives. DW hopes to promote understanding between different cultures and peoples. \n\nWhile funded by the German government, the work of DW is regulated by the Deutsche Welle Act (http://p.dw.com/p/17MtP), meaning content is always independent of government influence. \n\nWe ask that you please keep comments and discussions on this channel clean and respectful. For further information please click the 'DW Netiquette' link below."
        },
        "country": "DE"
      },
      "contentDetails": {
        "relatedPlaylists": {
          "likes": "",
          "uploads": "UUknLrEdhRCp1aegoMqRaCZg"
        }
      },
      "statistics": {
        "viewCount": "846440600",
        "subscriberCount": "2840000",
        "hiddenSubscriberCount": False,
        "videoCount": "25848"
      },
      "topicDetails": {
        "topicIds": [
          "/m/098wr",
          "/m/05qt0"
        ],
        "topicCategories": [
          "https://en.wikipedia.org/wiki/Society",
          "https://en.wikipedia.org/wiki/Politics"
        ]
      }
    }
  ]
}


quota_exceeded = {
  "error": {
    "code": 403,
    "message": "The request cannot be completed because you have exceeded your \u003ca href=\"/youtube/v3/getting-started#quota\"\u003equota\u003c/a\u003e.",
    "errors": [
      {
        "message": "The request cannot be completed because you have exceeded your \u003ca href=\"/youtube/v3/getting-started#quota\"\u003equota\u003c/a\u003e.",
        "domain": "youtube.quota",
        "reason": "quotaExceeded"
      }
    ]
  }
}


dw_comment_thread_1 = {'kind': 'youtube#commentThread',
   'etag': 'cCyjaK0kMLbXTxjT22wY2hSK6hQ',
   'id': 'UgzsG9SRCC7R1x_89zV4AaABAg',
   'snippet': {'videoId': '5UMT7RUaXBk',
    'topLevelComment': {'kind': 'youtube#comment',
     'etag': '2-nmZ9ZyVf84WqQwFLJvHtLLkgg',
     'id': 'UgzsG9SRCC7R1x_89zV4AaABAg',
     'snippet': {'videoId': '5UMT7RUaXBk',
      'textDisplay': 'Shhh dont speak about it on public. Chinese are very sensitive people.<br>Imram khan, pak caliphe',
      'textOriginal': 'Shhh dont speak about it on public. Chinese are very sensitive people.\nImram khan, pak caliphe',
      'authorDisplayName': 'Antonio Ribeiro',
      'authorProfileImageUrl': 'https://yt3.ggpht.com/ytc/AKedOLRtnpjQkQnh5-5Lq09tSFxd4aSFAjukl-OMFb7sVQ=s48-c-k-c0x00ffffff-no-rj',
      'authorChannelUrl': 'http://www.youtube.com/channel/UCFD9yhG2kFIR65YadjYR5BA',
      'authorChannelId': {'value': 'UCFD9yhG2kFIR65YadjYR5BA'},
      'canRate': True,
      'viewerRating': 'none',
      'likeCount': 0,
      'publishedAt': '2021-07-26T08:26:42Z',
      'updatedAt': '2021-07-26T08:26:42Z'}},
    'canReply': True,
    'totalReplyCount': 0,
    'isPublic': True}}


dw_comment_thread_with_reply = {'kind': 'youtube#commentThread',
 'etag': 'niPBYcJ-g131o9DUNBBspVPCjnU',
 'id': 'UgxqGWcF4_j3P970oQp4AaABAg',
 'snippet': {'videoId': '5UMT7RUaXBk',
  'topLevelComment': {'kind': 'youtube#comment',
   'etag': '0nidzC0iHjKcdIJiim4fXF7YdEQ',
   'id': 'UgxqGWcF4_j3P970oQp4AaABAg',
   'snippet': {'videoId': '5UMT7RUaXBk',
    'textDisplay': 'China is both communist and fascist.\r<br>And now it has spread the <a href="http://www.youtube.com/results?search_query=%23corona">#corona</a> virus to the world.\r<br>Don&#39;t buy Chinese!\r<br>That &#39;s enough.',
    'textOriginal': "China is both communist and fascist.\r\nAnd now it has spread the #corona virus to the world.\r\nDon't buy Chinese!\r\nThat 's enough.",
    'authorDisplayName': 'jhon free',
    'authorProfileImageUrl': 'https://yt3.ggpht.com/ytc/AKedOLRhnLdIHx6n5NX56wAITuNX4g1rIGDv9C6Rhg=s48-c-k-c0x00ffffff-no-rj',
    'authorChannelUrl': 'http://www.youtube.com/channel/UCicrxSWGfa8A54N8viAPFTA',
    'authorChannelId': {'value': 'UCicrxSWGfa8A54N8viAPFTA'},
    'canRate': True,
    'viewerRating': 'none',
    'likeCount': 0,
    'publishedAt': '2020-03-06T01:37:22Z',
    'updatedAt': '2020-03-06T01:37:22Z'}},
  'canReply': True,
  'totalReplyCount': 1,
  'isPublic': True},
 'replies': {'comments': [{'kind': 'youtube#comment',
    'etag': 'u1pHFwTa2deDFTWQpRBoY_Cr9l8',
    'id': 'UgxqGWcF4_j3P970oQp4AaABAg.95qRmatwk-z95sC9EDIvTC',
    'snippet': {'videoId': '5UMT7RUaXBk',
     'textDisplay': 'jhon free  Lol.. Most stuff in the stores is made in China',
     'textOriginal': 'jhon free  Lol.. Most stuff in the stores is made in China',
     'parentId': 'UgxqGWcF4_j3P970oQp4AaABAg',
     'authorDisplayName': 'Hal Asimov',
     'authorProfileImageUrl': 'https://yt3.ggpht.com/ytc/AKedOLTuZ4Gv4RVQSU7p1PFQX0r84n3ms80aSTiPJA=s48-c-k-c0x00ffffff-no-rj',
     'authorChannelUrl': 'http://www.youtube.com/channel/UC03Wk-Gp9gNg_STwgleQsFA',
     'authorChannelId': {'value': 'UC03Wk-Gp9gNg_STwgleQsFA'},
     'canRate': True,
     'viewerRating': 'none',
     'likeCount': 0,
     'publishedAt': '2020-03-06T17:59:16Z',
     'updatedAt': '2020-03-06T17:59:16Z'}}]}}


dw_playlist_item = {'kind': 'youtube#playlistItem',
   'etag': 'KanXo8Np00In82MeWirhhX7emH0',
   'id': 'VVVrbkxyRWRoUkNwMWFlZ29NcVJhQ1pnLjV4NVV4cUtNNy1Z',
   'snippet': {'publishedAt': '2021-10-15T08:00:24Z',
    'channelId': 'UCknLrEdhRCp1aegoMqRaCZg',
    'title': 'La Palma volcano: Massive lava flow pushes over the boundary of evacuated area | DW News',
    'description': "The Cumbre Vieja volcano on Spain's Canary Islands has been erupting for almost four weeks, but lava flow reached a new level on Thursday.\nScientists say magma has been pouring out of the main cone of the La Palma volcano at growing speed and volume. The river of red-hot lava has now pushed over the boundary of the evacuated area, forcing several hundred more people to flee their homes. An earthquake also shook the island of La Palma on Thursday, the strongest since volcanic activity picked up. \n\nSubscribe: https://www.youtube.com/user/deutschewelleenglish?sub_confirmation=1\n\nFor more news go to: http://www.dw.com/en/\nFollow DW on social media:\n►Facebook: https://www.facebook.com/deutschewellenews/\n►Twitter: https://twitter.com/dwnews\n►Instagram: https://www.instagram.com/dwnews\nFür Videos in deutscher Sprache besuchen Sie: https://www.youtube.com/dwdeutsch",
    'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/5x5UxqKM7-Y/default.jpg',
      'width': 120,
      'height': 90},
     'medium': {'url': 'https://i.ytimg.com/vi/5x5UxqKM7-Y/mqdefault.jpg',
      'width': 320,
      'height': 180},
     'high': {'url': 'https://i.ytimg.com/vi/5x5UxqKM7-Y/hqdefault.jpg',
      'width': 480,
      'height': 360},
     'standard': {'url': 'https://i.ytimg.com/vi/5x5UxqKM7-Y/sddefault.jpg',
      'width': 640,
      'height': 480},
     'maxres': {'url': 'https://i.ytimg.com/vi/5x5UxqKM7-Y/maxresdefault.jpg',
      'width': 1280,
      'height': 720}},
    'channelTitle': 'DW News',
    'playlistId': 'UUknLrEdhRCp1aegoMqRaCZg',
    'position': 0,
    'resourceId': {'kind': 'youtube#video', 'videoId': '5x5UxqKM7-Y'},
    'videoOwnerChannelTitle': 'DW News',
    'videoOwnerChannelId': 'UCknLrEdhRCp1aegoMqRaCZg'}}


dw_video = {'kind': 'youtube#video',
   'etag': '3RFt-X3gIFRwa-czHtId1LXvIT8',
   'id': '5x5UxqKM7-Y',
   'snippet': {'publishedAt': '2021-10-15T08:00:24Z',
    'channelId': 'UCknLrEdhRCp1aegoMqRaCZg',
    'title': 'La Palma volcano: Massive lava flow pushes over the boundary of evacuated area | DW News',
    'description': "The Cumbre Vieja volcano on Spain's Canary Islands has been erupting for almost four weeks, but lava flow reached a new level on Thursday.\nScientists say magma has been pouring out of the main cone of the La Palma volcano at growing speed and volume. The river of red-hot lava has now pushed over the boundary of the evacuated area, forcing several hundred more people to flee their homes. An earthquake also shook the island of La Palma on Thursday, the strongest since volcanic activity picked up. \n\nSubscribe: https://www.youtube.com/user/deutschewelleenglish?sub_confirmation=1\n\nFor more news go to: http://www.dw.com/en/\nFollow DW on social media:\n►Facebook: https://www.facebook.com/deutschewellenews/\n►Twitter: https://twitter.com/dwnews\n►Instagram: https://www.instagram.com/dwnews\nFür Videos in deutscher Sprache besuchen Sie: https://www.youtube.com/dwdeutsch",
    'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/5x5UxqKM7-Y/default.jpg',
      'width': 120,
      'height': 90},
     'medium': {'url': 'https://i.ytimg.com/vi/5x5UxqKM7-Y/mqdefault.jpg',
      'width': 320,
      'height': 180},
     'high': {'url': 'https://i.ytimg.com/vi/5x5UxqKM7-Y/hqdefault.jpg',
      'width': 480,
      'height': 360},
     'standard': {'url': 'https://i.ytimg.com/vi/5x5UxqKM7-Y/sddefault.jpg',
      'width': 640,
      'height': 480},
     'maxres': {'url': 'https://i.ytimg.com/vi/5x5UxqKM7-Y/maxresdefault.jpg',
      'width': 1280,
      'height': 720}},
    'channelTitle': 'DW News',
    'tags': ['DW News',
     'Cumbre Vieja',
     'la palma',
     'la palma volcano',
     'volcano eruption'],
    'categoryId': '25',
    'liveBroadcastContent': 'none',
    'defaultLanguage': 'en-US',
    'localized': {'title': 'La Palma volcano: Massive lava flow pushes over the boundary of evacuated area | DW News',
     'description': "The Cumbre Vieja volcano on Spain's Canary Islands has been erupting for almost four weeks, but lava flow reached a new level on Thursday.\nScientists say magma has been pouring out of the main cone of the La Palma volcano at growing speed and volume. The river of red-hot lava has now pushed over the boundary of the evacuated area, forcing several hundred more people to flee their homes. An earthquake also shook the island of La Palma on Thursday, the strongest since volcanic activity picked up. \n\nSubscribe: https://www.youtube.com/user/deutschewelleenglish?sub_confirmation=1\n\nFor more news go to: http://www.dw.com/en/\nFollow DW on social media:\n►Facebook: https://www.facebook.com/deutschewellenews/\n►Twitter: https://twitter.com/dwnews\n►Instagram: https://www.instagram.com/dwnews\nFür Videos in deutscher Sprache besuchen Sie: https://www.youtube.com/dwdeutsch"},
    'defaultAudioLanguage': 'en'},
   'contentDetails': {'duration': 'PT40S',
    'dimension': '2d',
    'definition': 'hd',
    'caption': 'false',
    'licensedContent': True,
    'contentRating': {},
    'projection': 'rectangular'},
   'statistics': {'viewCount': '2502',
    'likeCount': '97',
    'dislikeCount': '2',
    'favoriteCount': '0',
    'commentCount': '17'}}
