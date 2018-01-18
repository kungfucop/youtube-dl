# coding: utf-8
from __future__ import unicode_literals

import json

from .common import InfoExtractor
from ..utils import (
    int_or_none,
    js_to_json,
)


class MoverIE(InfoExtractor):
    IE_DESC = 'mover_uz'
    # https://mover.uz/video/embed/SM9smOvj/
    _VALID_URL = r'https?://mover\.uz/video/embed/(?P<id>\w+)/'

    _TEST = {
        'url': 'https://mover.uz/video/embed/SM9smOvj/',
        'md5': '3b91003cf85fc5db277870c8ebd98eae',
        'info_dict': {
            'id': 'SM9smOvj',
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

        video_url = 'https://v.mover.uz/' + video_id + '_m.mp4'
        title = self._og_search_title(webpage, fatal=False)
        if not title:
            title = video_id
        description = self._og_search_description(webpage, default=None)
        thumbnail = 'https://v.mover.uz/' + video_id + '_m2.jpg'

        return {
            'id': video_id,
            'url': video_url,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
        }
