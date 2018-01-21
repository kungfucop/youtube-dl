# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import int_or_none


class TrubaIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?truba\.com/tools/config_video.php\?id=(?P<id>\d+)'
    _TEST = {
        'url': 'http://truba.com/tools/config_video.php?id=321014',
        'md5': '03f11bb21c52dd12a05be21a5c7dcc97',
        'info_dict': {
            'id': '321014',
            'ext': 'mp4',
            'title': 'everthing about me (Preview)',
            'view_count': int,
            'like_count': int,
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        video_url = self._search_regex(
            r'<source src=\"(?P<url>[^\"]*)\"[\W]*type=\"video/mp4\"',
            webpage, 'video URL', group='url')
        # poster="https://truba.com/video/0505/ico_full/504157.jpg"
        thumbnail = self._search_regex(
            r'<video.+?(?=poster=)poster=\"(?P<poster>[^\"]+)',
            webpage, 'video poster', group='poster')

        return {
            'id': video_id,
            'title': 'truba' + video_id,
            'formats': [{
                'url': video_url,
            }],
        }
