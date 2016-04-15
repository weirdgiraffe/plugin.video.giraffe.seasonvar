#!/usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#

import pytest
assert pytest
import re
from addon import plugin_video


def check_directory_item(item):
    assert re.match(r'^[^\s]', item['li'].name)
    assert item['is_dir'] is True
    assert isinstance(item['url'], str)


def check_thumb_directory_item(item):
    check_directory_item(item)
    assert re.match(r'^http:\/\/cdn\.seasonvar\.ru\/oblojka\/\d+\.jpg',
                    item['li'].thumb)


def test_screen_start(requests_mock, addon, kodi):
    plugin_video.screen_start({})
    # 7 date items from seasonvar site
    # 1 for search
    assert len(kodi.items) == 8
    for i in kodi.items:
        check_directory_item(i)
        assert i['count'] is None
    assert kodi.items[-1]['li'].name == u'Поиск'


def test_screen_date(requests_mock, addon, kodi):
    requests_mock.respond(r'seasonvar.ru\/rss\.php$', 'assets/rss01.xml')
    plugin_video.screen_date({})
    assert len(kodi.items) == 0
    plugin_video.screen_date({'date': 'hello'})
    assert len(kodi.items) == 0
    plugin_video.screen_date({'date': '12.04.2016'})
    assert len(kodi.items) == 3
    for i in kodi.items:
        check_thumb_directory_item(i)


def test_screen_episodes(requests_mock, addon, kodi):
    requests_mock.respond(r'seasonvar.ru\/rss\.php$', 'assets/rss01.xml')
    requests_mock.respond(r'seasonvar.ru\/.*Skorpion.*\.html$', 'assets/scorpion.html')
    requests_mock.respond(r'seasonvar.ru\/playls2.*12394/list\.xml$', 'assets/playlist_scorpion.json')
    requests_mock.respond(r'^hello$', 'assets/empty.html', code=404)
    plugin_video.screen_episodes({})
    assert len(kodi.items) == 0
    plugin_video.screen_episodes({'url': 'hello'})
    assert len(kodi.items) == 0
    plugin_video.screen_episodes({
        'url': 'http://seasonvar.ru/serial-12394-Skorpion_serial_2014_ndash_.html'
    })
    # assert len(kodi.items) == 3
    # for i in kodi.items:
    #     check_thumb_directory_item(i)


# def test_screen_date(requests_mock, addon, kodi):
#     requests_mock.respond(r'seasonvar.ru$', 'tests/samples/main_page.html')
#     seasonvar = Seasonvar()
#     plugin_video.screen_episodes({'name': 'Агентство Лунный Свет'}, seasonvar)
#     assert len(kodi.items) > 0
#     for i in kodi.items:
#         check_thumb_directory_item(i)
#     pprint.pprint(kodi.items)
