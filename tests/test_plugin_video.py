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
from seasonvar.requester import NetworkError
from datetime import datetime, timedelta


def assert_kodi_directory_item_is_dir(kodi_directory_item_mock):
    assert kodi_directory_item_mock['is_dir'] is True


def assert_kodi_directory_item_is_not_dir(kodi_directory_item_mock):
    assert kodi_directory_item_mock['is_dir'] is False


def assert_kodi_directory_item_has_thumb(kodi_directory_item_mock):
    assert hasattr(kodi_directory_item_mock['li'], 'thumb')


def check_item(item):
    assert re.match(r'^[^\s]', item['li'].name)
    assert isinstance(item['url'], str)


def check_thumb(item):
    assert re.match(r'^http:\/\/cdn\.seasonvar\.ru\/oblojka\/\d+\.jpg',
                    item['li'].thumb)


def test_screen_start_does_not_make_requestst(requests_mock, addon, kodi):
    # if any request was made test will fail in requests_mock
    plugin_video.screen_start({})


def strip_colors(instr):
    return re.sub(r'\[COLOR [A-F0-9]{8}\](.+?)\[\/COLOR\]',
                  r'\1',
                  instr)


def test_screen_start_items_layout(requests_mock, addon, kodi):
    # should return a list of 7 entries for
    # last 7 days. and one entry for search
    plugin_video.screen_start({})
    assert len(kodi.items) == 8
    checked_date = datetime.today()
    for item in kodi.items[:-1]:
        assert_kodi_directory_item_is_dir(item)
        urlparams = item['urlparams']
        assert 'action' in urlparams
        assert urlparams['action'] == 'screen_date'
        assert 'date' in urlparams
        datestr = checked_date.strftime('%d.%m.%Y')
        assert urlparams['date'] == datestr
        checked_date -= timedelta(days=1)
    assert strip_colors(kodi.items[-1]['li'].name) == 'поиск'


def test_screen_date_missing_params(requests_mock, addon, kodi):
    plugin_video.screen_date({})
    assert len(kodi.items) == 0


def test_screen_date_items_layout_from_mainpage(requests_mock, addon, kodi):
    requests_mock.respond(r'http:\/\/seasonvar.ru\/rss\.php$',
                          'assets/rss-01.xml')
    requests_mock.respond(r'http:\/\/seasonvar.ru$',
                          'assets/page-main-01.html')
    plugin_video.screen_date({'date': '11.04.2016'})
    assert len(kodi.items) == 3
    for item in kodi.items:
        assert_kodi_directory_item_is_dir(item)
        assert_kodi_directory_item_has_thumb(item)
        urlparams = item['urlparams']
        assert 'action' in urlparams
        assert urlparams['action'] == 'screen_episodes'
        assert 'url' in urlparams
        # urls for screen_episodes should be relative
        assert urlparams['url'].find('/') == 0


def test_screen_episodes_missing_params(requests_mock, addon, kodi):
    plugin_video.screen_episodes({})
    assert len(kodi.items) == 0


def test_screen_episodes_items_layout(requests_mock, addon, kodi):
    requests_mock.respond(r'seasonvar.ru\/.*Skorpion.*\.html$',
                          'assets/scorpion2.html')
    requests_mock.respond(r'seasonvar.ru\/playls2.*/list\.xml.*$',
                          'assets/playlist-scorpion.json')

    seasonurl = '/serial-12394-Skorpion_serial_2014_ndash_.html'
    plugin_video.screen_episodes({'url': seasonurl})

    assert len(kodi.items) == 23

    for item in kodi.items[1:]:
        assert_kodi_directory_item_is_not_dir(item)
        assert_kodi_directory_item_has_thumb(item)
        urlparams = item['urlparams']
        assert 'action' in urlparams
        assert urlparams['action'] == 'play'
        assert 'IsPlayable' in item['li'].properties
        assert item['li'].properties['IsPlayable'] == 'True'
        assert 'url' in urlparams
        # urls for screen_episodes should be absolute
        assert urlparams['url'].find('/') != 0

    assert_kodi_directory_item_is_dir(kodi.items[0])
    assert strip_colors(kodi.items[0]['li'].name) == u'сезон: 2 / 3'
    assert 'action' in kodi.items[0]['urlparams']
    assert 'url' in kodi.items[0]['urlparams']
    assert kodi.items[0]['urlparams']['action'] == 'screen_seasons'
    # urls for screen_seasons should be relative
    assert kodi.items[0]['urlparams']['url'].find('/') == 0


def test_screen_seasons_missing_params(requests_mock, addon, kodi):
    plugin_video.screen_seasons({})
    assert len(kodi.items) == 0


def test_screen_seasons_items_layout(requests_mock, addon, kodi):
    requests_mock.respond(r'seasonvar.ru\/.*Skorpion.*\.html$',
                          'assets/scorpion.html')
    requests_mock.respond(r'seasonvar.ru\/playls2.*12394/list\.xml$',
                          'assets/playlist_scorpion.json')
    seasonurl = '/serial-12394-Skorpion_serial_2014_ndash_.html'
    plugin_video.screen_seasons({'url': seasonurl})
    assert len(kodi.items) == 2
    for item in kodi.items:
        assert_kodi_directory_item_is_dir(item)
        assert_kodi_directory_item_has_thumb(item)
        urlparams = item['urlparams']
        assert 'action' in urlparams
        assert urlparams['action'] == 'screen_episodes'
        assert 'url' in urlparams
        # urls for screen_episodes should be relative
        assert urlparams['url'].find('/') == 0

    assert kodi.items[0]['li'].name == 'сезон 1'
    assert kodi.items[1]['li'].name == '* сезон 2'


def test_play_missing_params(requests_mock, addon, kodi):
    plugin_video.play({})
    assert len(kodi.items) == 0
    assert hasattr(kodi, 'resolved') is False


def test_play_items_layout(requests_mock, addon, kodi):
    testurl = 'http://hello'
    plugin_video.play({'url': testurl})
    assert len(kodi.items) == 0
    assert hasattr(kodi, 'resolved')
    assert kodi.resolved.path == testurl


def test_main_handle_network_exception(requests_mock,
                                       addon, kodi, monkeypatch):
    def raise_network_error(*args, **kwargs):
        raise NetworkError()

    monkeypatch.setattr('seasonvar.requester.Requester._get',
                        raise_network_error)

    addon.args['action'] = 'screen_date'
    addon.args['date'] = '12.04.2016'
    plugin_video.main()
    assert addon.notification_shown

    addon.notification_shown = False
    addon.args['action'] = 'screen_date'
    addon.args['date'] = '11.04.2016'
    plugin_video.main()
    assert addon.notification_shown

    seasonurl = '/serial-12394-Skorpion_serial_2014_ndash_.html'
    addon.notification_shown = False
    addon.args['action'] = 'screen_episodes'
    addon.args['url'] = seasonurl
    plugin_video.main()
    assert addon.notification_shown

    addon.notification_shown = False
    addon.args['action'] = 'screen_seasons'
    addon.args['url'] = seasonurl
    plugin_video.main()
    assert addon.notification_shown
