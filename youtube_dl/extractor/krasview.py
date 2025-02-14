# coding: utf-8
from __future__ import unicode_literals

import json

from .common import InfoExtractor
from ..utils import (
    int_or_none,
    js_to_json,
)


class KrasViewIE(InfoExtractor):
    IE_DESC = 'Красвью'
    # http://krasview.ru/embed/329048
    # http://hlamer.ru/embed/703677
    # http://hlamer.ru/video/329048-Djosh_Barnett_vs_Nandor_Guelmino
    _VALID_URL = r'https?://(krasview|hlamer)\.ru/(?:video|embed)/(?P<id>\d+)'

    _TEST = {
        'url': 'http://krasview.ru/video/512228',
        'md5': '3b91003cf85fc5db277870c8ebd98eae',
        'info_dict': {
            'id': '512228',
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
        if 'hlamer.ru' in url:
            url = 'http://hlamer.ru/video/'+video_id

        webpage = self._download_webpage(url, video_id)

        flashvars = json.loads(js_to_json(self._search_regex(
            r'video_Init\(((?P<flashvars>{.+?})(?:,))', webpage, 'flashvars', group='flashvars')))

        video_url = flashvars['url']
        title = self._og_search_title(webpage, fatal=False)
        if not title:
            title = video_id
        description = self._og_search_description(webpage, default=None)
        thumbnail = flashvars.get('image') or self._og_search_thumbnail(webpage)
        duration = int_or_none(flashvars.get('duration'))
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
