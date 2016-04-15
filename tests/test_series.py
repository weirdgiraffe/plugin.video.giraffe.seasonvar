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
from seasonvar.series import Series
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


def test_episodes_current_season_extracted(requests_mock):
    requests_mock.respond(r'Skorpion.*\.html$',
                          'assets/scorpion.html')
    baseurl = 'http://seasonvar.ru'
    seasonurl = '/serial-12394-Skorpion_serial_2014_ndash_.html'
    series = Series(urljoin(baseurl, seasonurl))
    assert series.current_season.url == seasonurl
    assert series.current_season.id == '12394'
    assert series.current_season.number == 2
    assert len(series.seasons) == 2


def test_episodes_playlist_extracted(requests_mock):
    requests_mock.respond(r'http:\/\/seasonvar\.ru\/.*Skorpion.*\.html$',
                          'assets/scorpion.html')
    requests_mock.respond(r'playls2.*12394/list\.xml$',
                          'assets/playlist_scorpion.json')
    baseurl = 'http://seasonvar.ru'
    seasonurl = '/serial-12394-Skorpion_serial_2014_ndash_.html'
    print urljoin(baseurl, seasonurl)
    series = Series(urljoin(baseurl, seasonurl))
    episodes = list(series.current_season.episodes)
    assert len(episodes) == 22
    for e in episodes:
        assert e['url'] is not None
        assert e['name'] is not None
        assert e['thumb'] is not None

