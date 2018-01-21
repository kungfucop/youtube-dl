# coding: utf-8
from __future__ import unicode_literals

import json

from .common import InfoExtractor
from ..utils import (
    int_or_none,
    js_to_json,
)


class BashtubeIE(InfoExtractor):
    IE_DESC = 'Bashtube'
    _VALID_URL = r'https?://(bashtube)\.ru/(?:video|embed)/frame/(?P<id>.*?)\.html'

    _TEST = {
        'url': 'http://bashtube.ru/video/frame/19bb09ad7cf54dab9cc7587c5d1859a0.html',
        'md5': '3b91003cf85fc5db277870c8ebd98eae',
        'info_dict': {
            'id': '19bb09ad7cf54dab9cc7587c5d1859a0',
            'ext': 'mp4',
            'title': 'Снег, лёд, заносы',
            'description': 'Снято в городе Нягань, в Ханты-Мансийском автономном округе.',
            'duration': 27,
            'thumbnail': r're:^https?://.*\.jpg',
        },
        'params': {
            'skip_download': 'Not accessible from Travis CI server',
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        flashvars = json.loads(js_to_json(self._search_regex(
            r'(?s)var\s+params\s*=\s*(?P<params>{.+?})[;,]', webpage, 'params', group='params')))

        video_url = flashvars['file']
        title = self._og_search_title(webpage, fatal=False)
        if not title:
            title = video_id
        description = self._og_search_description(webpage, default=None)
        thumbnail = flashvars.get('poster') or self._og_search_thumbnail(webpage)
        duration = int_or_none(flashvars.get('time'))
        width = int_or_none(self._og_search_property(
            'video:width', webpage, 'video width', default=None))
        height = int_or_none(self._og_search_property(
            'video:height', webpage, 'video height', default=None))

        return {
            'id': video_id,
            'url': video_url,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'duration': duration,
            'width': width,
            'height': height,
        }
