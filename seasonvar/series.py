#!/usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#
import re
try:
    from seasonvar.requester import SeasonvarRequester
except ImportError:
    from requester import SeasonvarRequester


SEASON = r'(\/serial-(?P<id>\d+)-(?P<name>.+?)'\
         '(?:-(?P<season>\d+)-(?:sezon|season))?\.html)'


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
        self.__html = kwargs.get('html')
        self.__requester = kwargs.get('requester', SeasonvarRequester())
        self.__secure = None

    @property
    def episodes(self):
        playlist_url = 'http://seasonvar.ru/playls2/{0}x/trans/{1}/'\
                       'list.xml'.format(self.secure, self.id)
        playlist = self.__requester.get_json(playlist_url)
        print(playlist)

    @property
    def secure(self):
        if self.__html is None:
            self.__html = self.__requester.get(self.url)
        return secure(self.__html)


class Series:
    def __init__(self, url):
        self.__requester = SeasonvarRequester()
        self.__url = url
        self.__html = self.__requester.get(url)
        self.__seasons = None

    @property
    def seasons(self):
        if self.__seasons is None:
            self.__seasons = list(self._seasons())
        return self.__seasons

    def _seasons(self):
        regexp = re.compile(r'<a[^>]+?href="{0}"'.format(SEASON))
        for (surl, sid, sname, snum) in regexp.findall(self.__html):
            yield Season(url=surl, id=sid, trname=sname, number=snum)

    @property
    def current_season(self):
        kwargs = url2season(self.__url)
        kwargs['html'] = self.__html
        return Season(**kwargs)
