# -*- coding: utf-8 -*-

import json
import re

from mopidy_youtube import logger

from youtube import Client
from youtube import Video

# Indirect access to YouTube data, without API
#
class scrAPI(Client):
    endpoint = 'https://www.youtube.com/'

    @classmethod
    def format_duration(cls, match):
        duration = ''
        if match.group('durationHours') is not None:
            duration += match.group('durationHours')+'H'
        if match.group('durationMinutes') is not None:
            duration += match.group('durationMinutes')+'M'
        if match.group('durationSeconds') is not None:
            duration += match.group('durationSeconds')+'S'
        return duration
        
    @classmethod
    def run_search(cls, query):
        result = cls.session.get(scrAPI.endpoint+'results', params=query)
        regex = (
            r'(?:\<li\>)(?:.|\n)*?\<a href\=(["\'])\/watch\?v\=(?P<id>.{11})'
            r'(?:\&amp\;list\=(?:(?P<playlist>PL.*?)\1)?'
            # r'(?:(?P<radiolist>RD.*?)\&)?'
            r'(?:.|\n)*?class\=\1formatted-video-count-label\1\>[^\d]*'
            r'(?P<itemCount>\d*))?(?:.|\n)*?title\=\1(?P<title>.+?)\1.+?'
            r'(?:(?:Duration[^\d]+(?:(?P<durationHours>\d+)\:)?'
            r'(?P<durationMinutes>\d{1,2})\:'
            r'(?P<durationSeconds>\d{2})[^\d].*?)?)?'
            r'\<a href\=\1(?:(?:(?P<uploaderUrl>/'
            r'(?:user|channel)/[^"\']+)\1[^>]+>)?'
            r'(?P<uploader>[^<]+).+class\=\1'
            r'(?:yt-lockup-description|yt-uix-sessionlink)'
            r'[^>]*>(?P<description>.*?)\<\/div\>)?'
        )
        items = []

        for match in re.finditer(regex, result.text):
            duration = cls.format_duration(match)
            if match.group('playlist') is not None:
                item = {
                    'id': {
                      'kind': 'youtube#playlist',
                      'playlistId': match.group('playlist')
                    },
                    'contentDetails': {
                        'itemCount': match.group('itemCount')
                    }
                }
            else:
                item = {
                    'id': {
                      'kind': 'youtube#video',
                      'videoId': match.group('id')
                    },
                }
                if duration != '':
                    item.update({
                        'contentDetails': {
                            'duration': 'PT'+duration,
                        },
                    })
            item.update({
                'snippet': {
                      'title': match.group('title'),
                      # TODO: full support for thumbnails
                      'thumbnails': {
                          'default': {
                              'url': 'https://i.ytimg.com/vi/'
                                     + match.group('id')
                                     + '/default.jpg',
                              'width': 120,
                              'height': 90,
                          },
                      },
                },
            })

            # # Instead of if/else, could this just be:
            # item['snippet'].update({
            #     'channelTitle': match.group('uploader') or 'NA'
            # })
            if match.group('uploader') is not None:
                item['snippet'].update(
                    {'channelTitle': match.group('uploader')})
            else:
                item['snippet'].update({
                    'channelTitle': 'NA'
                })
            items.append(item)
        return items

    # search for videos and playlists
    #
    @classmethod
    def search(cls, q):
        search_results = []

        # assume 20 results per page
        pages = int(Video.search_results / 20) + (Video.search_results % 20 > 0)  # noqa: E501

        logger.info('session.get triggered: search')

        rs = [{"search_query": q.replace(' ', '+'),
               "page": page + 1} for page in range(pages)]

        for result in [cls.run_search(r) for r in rs]:
            search_results.extend(result)

        return json.loads(json.dumps(
            {'items': [x for _, x in zip(range(Video.search_results), search_results)]},  # noqa: E501
            sort_keys=False,
            indent=1
        ))

    # list videos
    #
    @classmethod
    def list_videos(cls, ids):

        regex = (
            r'<div id="watch7-content"(?:.|\n)*?'
            r'<meta itemprop="name" content="'
            r'(?P<title>.*?)(?:">)(?:.|\n)*?'
            r'<meta itemprop="duration" content="'
            r'(?P<duration>.*?)(?:">)(?:.|\n)*?'
            r'<link itemprop="url" href="http://www.youtube.com/'
            r'(?:user|channel)/(?P<channelTitle>.*?)(?:">)(?:.|\n)*?'
            r'</div>'
        )
        items = []

        for id in ids:
            query = {'v': id}
            logger.info('session.get triggered: list_videos')
            result = cls.session.get(
                scrAPI.endpoint+'watch',
                params=query
            )
            for match in re.finditer(regex, result.text):
                item = {
                    'id': id,
                    'snippet': {
                        'title': match.group('title'),
                        'channelTitle': match.group('channelTitle'),
                    },
                    'contentDetails': {
                        'duration': match.group('duration'),
                    }
                }
                items.append(item)
        return json.loads(json.dumps(
            {'items': items},
            sort_keys=False,
            indent=1
        ))

    # list playlists
    #
    @classmethod
    def list_playlists(cls, ids):

        regex = (
            r'<div id="pl-header"(?:.|\n)*?"'
            r'(?P<thumbnail>https://i\.ytimg\.com\/vi\/.{11}/).*?\.jpg'
            r'(?:(.|\n))*?(?:.|\n)*?class="pl-header-title"'
            r'(?:.|\n)*?\>\s*(?P<title>.*)(?:.|\n)*?<a href="/'
            r'(user|channel)/(?:.|\n)*? >'
            r'(?P<channelTitle>.*?)</a>(?:.|\n)*?'
            r'(?P<itemCount>\d*) videos</li>'
        )
        items = []

        for id in ids:
            query = {
                'list': id,
            }
            logger.info('session.get triggered: list_playlists')
            result = cls.session.get(
                scrAPI.endpoint+'playlist',
                params=query
            )
            for match in re.finditer(regex, result.text):
                item = {
                    'id': id,
                    'snippet': {
                        'title': match.group('title'),
                        'channelTitle': match.group('channelTitle'),
                        'thumbnails': {
                            'default': {
                                'url': match.group('thumbnail')+'default.jpg',
                                'width': 120,
                                'height': 90,
                            },
                        },
                    },
                    'contentDetails': {
                        'itemCount': match.group('itemCount'),
                    }
                }
                items.append(item)

        return json.loads(json.dumps(
            {'items': items},
            sort_keys=False,
            indent=1
        ))

    # list playlist items
    #
    @classmethod
    def run_list_playlistitems(cls, query):
        result = cls.session.get(scrAPI.endpoint+'playlist', params=query)

        regex = (
            r'<tr class\=\"pl-video.*\" data-title\=\"(?P<title>.+?)".*?'
            r'<a href\=\"\/watch\?v\=(?P<id>.{11})\&amp;(?:.|\n)*?'
            r'(?P<thumbnail>https://i\.ytimg\.com\/vi\/.{11}/).*?\.jpg'
            r'(?:.|\n)*?<div class="pl-video-owner">(?:.|\n)*?'
            r'/(?:user|channel)/(?:.|\n)*? >(?P<channelTitle>.*?)</a>'
            r'(?:.|\n)*?<div class="timestamp">.*?">(?:(?:'
            r'(?P<durationHours>[0-9]+)\:)?'
            r'(?P<durationMinutes>[0-9]+)\:'
            r'(?P<durationSeconds>[0-9]{2}))'
            r'(?:.|\n)*?</div></td></tr>'
        )
        items = []

        for match in re.finditer(regex, result.text):
            duration = cls.format_duration(match)
            item = {
                'id': match.group('id'),
                'snippet': {
                    'resourceId': {
                        'videoId': match.group('id'),
                    },
                    'title': match.group('title'),
                    'channelTitle': match.group('channelTitle'),
                    'thumbnails': {
                        'default': {
                            'url': match.group('thumbnail')+'default.jpg',
                            'width': 120,
                            'height': 90,
                        },
                    },
                },
            }
            if duration != '':
                item.update({
                    'contentDetails': {
                        'duration': 'PT'+duration}})

            items.append(item)
        return items

    @classmethod
    def list_playlistitems(cls, id, page, max_results):
        query = {
            'list': id
        }
        logger.info('session.get triggered: list_playlist_items')
        items = cls.run_list_playlistitems(query)
        result = json.loads(json.dumps(
            {'nextPageToken': None, 'items': [x for _, x in zip(range(max_results), items)]},  # noqa: E501
            sort_keys=False,
            indent=1
        ))
        return result

