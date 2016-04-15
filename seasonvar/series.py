# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#
from __future__ import unicode_literals
import re
from cached_property import cached_property
try:
    from seasonvar.requester import SeasonvarRequester
except ImportError:
    from requester import SeasonvarRequester


SEASON = r'(\/serial-(?P<id>\d+)-(?:.+?)'\
         '(?:-(?:\d+)-(?:sezon|season))?\.html)'


def secure(html):
    regexp = re.compile(r'secureMark\s*=\s*"([a-f0-9]+)"')
    for result in regexp.findall(html):
        return result


def url2season(url):
    regexp = re.compile(r'^(?:http:.*?)?{}$'.format(SEASON))
    m = regexp.match(url)
    if m:
        return {'url': url,
                'id': m.group('id'),
                'trname': m.group('name'),
                'number': m.group('season')}


def url2thumb(url):
    regexp = re.compile(r'^(?:http:.*?)?{}$'.format(SEASON))
    m = regexp.match(url)
    if m:
        return 'http://cdn.seasonvar.ru'\
               '/oblojka/{}.jpg'.format(m.group('id'))


class Season:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.id = kwargs.get('id')
        self.trname = kwargs.get('trname')
        self.name = kwargs.get('name')
        self.number = kwargs.get('number')
        self.thumb = url2thumb(self.url)
        self.html = kwargs.get('html')
        self.__requester = kwargs.get('requester', SeasonvarRequester())
        self.__secure = None

    @property
    def episodes(self):
        playlist_url = 'http://seasonvar.ru/playls2/{0}x/trans/{1}/'\
                       'list.xml'.format(self.secure, self.id)
        playlist = self.__requester.get_json(playlist_url)
        for episode in playlist['playlist']:
            yield {'url': episode['file'],
                   'name': episode['comment'],
                   'thumb': self.thumb}

    @property
    def secure(self):
        if self.html is None:
            url = self.__requester.absurl(self.url)
            self.html = self.__requester.get(url)
        return secure(self.html)


class Series:
    def __init__(self, url):
        self.__requester = SeasonvarRequester()
        absurl = self.__requester.absurl(url)
        relurl = self.__requester.relurl(url)
        self.__url = relurl
        self.__html = self.__requester.get(absurl)
        self.__current_season = None

    @cached_property
    def seasons(self):
        return list(self._seasons_from_html())

    @cached_property
    def current_season(self):
        for season in self.seasons:
            if season.url == self.__url:
                season.html = self.__html
                return season

    def _seasons_from_html(self):
        regexp = re.compile(r'<h2>.*?<a[^>]+?href="{0}"'.format(SEASON),
                            re.DOTALL)
        for num, (surl, sid) in enumerate(regexp.findall(self.__html), 1):
            yield Season(url=surl, id=sid, number=num,
                         requester=self.__requester)
