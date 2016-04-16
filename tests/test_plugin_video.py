#!/usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#
from __future__ import unicode_literals
import pytest
assert pytest
import re
import addon.plugin_video as plugin_video


def check_item(item):
    assert re.match(r'^[^\s]', item['li'].name)
    assert isinstance(item['url'], str)


def check_thumb(item):
    assert re.match(r'^http:\/\/cdn\.seasonvar\.ru\/oblojka\/\d+\.jpg',
                    item['li'].thumb)


def check_directory_item(item):
    check_item(item)
    assert item['is_dir'] is True


def check_thumb_directory_item(item):
    check_directory_item(item)
    check_thumb(item)


def check_thumb_item(item):
    check_item(item)
    check_thumb(item)


def test_screen_start_has_search(requests_mock, addon, kodi):
    plugin_video.screen_start({})
    assert len([x for x in kodi.items if x['li'].name == 'Поиск']) == 1


def test_screen_start_search_is_the_last_item(requests_mock, addon, kodi):
    plugin_video.screen_start({})
    assert kodi.items[-1]['li'].name == u'Поиск'


def test_screen_start_describes_a_week(requests_mock, addon, kodi):
    plugin_video.screen_start({})
    assert len(kodi.items) == 8
    assert len(set(x['li'].name for x in kodi.items)) == 8


def test_screen_start_li_format(requests_mock, addon, kodi):
    plugin_video.screen_start({})
    # 7 date items from seasonvar site
    # 1 for search
    for i in kodi.items:
        check_directory_item(i)
        assert i['count'] is None


def test_screen_date_bad_params(requests_mock, addon, kodi):
    requests_mock.respond(r'http:\/\/seasonvar.ru\/rss\.php$',
                          'assets/rss01.xml')
    plugin_video.screen_date({})
    assert len(kodi.items) == 0
    plugin_video.screen_date({'date': 'hello'})
    assert len(kodi.items) == 0


def test_screen_date(requests_mock, addon, kodi):
    requests_mock.respond(r'http:\/\/seasonvar.ru\/rss\.php$',
                          'assets/rss01.xml')
    plugin_video.screen_date({'date': '12.04.2016'})
    assert len(kodi.items) == 3
    for i in kodi.items:
        check_thumb_directory_item(i)


def test_screen_episodes_bad_params(requests_mock, addon, kodi):
    plugin_video.screen_episodes({})
    assert len(kodi.items) == 0


def test_screen_episodes(requests_mock, addon, kodi):
    requests_mock.respond(r'seasonvar.ru\/.*Skorpion.*\.html$',
                          'assets/scorpion.html')
    requests_mock.respond(r'seasonvar.ru\/playls2.*12394/list\.xml$',
                          'assets/playlist_scorpion.json')
    seasonurl = '/serial-12394-Skorpion_serial_2014_ndash_.html'
    plugin_video.screen_episodes({'url': seasonurl})
    assert len(kodi.items) == 23
    assert kodi.items[0]['li'].name == u'сезон 2/2'
    for i in kodi.items[1:]:
        check_thumb_item(i)


def test_screen_seasons(requests_mock, addon, kodi):
    requests_mock.respond(r'seasonvar.ru\/.*Skorpion.*\.html$',
                          'assets/scorpion.html')
    requests_mock.respond(r'seasonvar.ru\/playls2.*12394/list\.xml$',
                          'assets/playlist_scorpion.json')
    seasonurl = '/serial-12394-Skorpion_serial_2014_ndash_.html'
    plugin_video.screen_seasons({'url': seasonurl})
    assert len(kodi.items) == 2
    for i in kodi.items:
        check_thumb_directory_item(i)
    assert kodi.items[0]['li'].name == 'сезон 1'
    assert kodi.items[1]['li'].name == '* сезон 2'
