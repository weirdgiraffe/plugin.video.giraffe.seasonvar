#!/usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#
import re


SEASON = r'(\/serial-(?P<id>\d+)-(?P<name>.+?)(?:-(?P<season>\d+)-(?:sezon|season))?\.html)'


def actual(html):
    regexp = re.compile(
        r'<div class="film-list-item">[^<]+?'
        '<a href="{0}"[^>]*?>([^<]+?)<\/a>[^<]+?'
        '<span[^>]*?>([^<]+?)<\/span>[^<]+?'
        '<\/div>'.format(SEASON),
        re.DOTALL)
    for item in regexp.findall(html):
        entry = {'url': item[0],
                 'id': int(item[1]),
                 'urlname': item[2],
                 'season': int(item[3]) if item[3] else 0,
                 'name': item[4].strip(),
                 'changes': item[5].strip(),
                 }
        entry['thumb'] = 'http://cdn.seasonvar.ru'\
                         '/oblojka/{}.jpg'.format(entry['id'])
        print(entry)


def seasons(html):
    regexp = re.compile(r'<a[^>]+?href="{0}"'.format(SEASON))
    for item in regexp.findall(html):
        url, _id, name, season = item
        print(name, end=' ')
        if season:
            print('season', season, end=' ')
        print(':', url)


def secure(html):
    regexp = re.compile(r'secureMark\s*=\s*"([a-f0-9]+)"')
    for result in regexp.findall(html):
        print(result)


def thumb(season_url):
    print(season_url)
    regexp = re.compile(r'^(?:http:.*?)?{}$'.format(SEASON))
    print(regexp)
    m = regexp.match(season_url)
    if m:
        return 'http://cdn.seasonvar.ru'\
               '/oblojka/{}.jpg'.format(m.group('id'))
