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
from seasonvar.rss import items
from datetime import datetime


def test_rss_extract_something(requests_mock):
    requests_mock.respond(r'.*', 'assets/rss01.xml')
    l = list(items())
    assert len(l) == 3


def test_rss_extract_entries(requests_mock):
    requests_mock.respond(r'.*', 'assets/rss01.xml')
    l = list(items())
    assert len(l) == 3
    assert l[0]['entry'] == u'Скорпион (2 сезон), 22 серия'
    assert l[0]['url'] == u'http://seasonvar.ru/serial-12394-Skorpion_serial_2014_ndash_.html'
    assert l[0]['date'] == datetime(2016, 4, 12, 21, 55, 22)
    assert l[1]['entry'] == u'Гаргантия на зеленой планете: Морские тропы за горизонт (1 сезон), 1 серия'
    assert l[1]['url'] == u'http://seasonvar.ru/serial-13480-Gargantiya_na_zelnoj_planete_Morskie_tropy_za_gorizont.html'
    assert l[1]['date'] == datetime(2016, 4, 12, 21, 54, 44)
    assert l[2]['entry'] == u'Скиталец Эндры (1 сезон), 1-2 серия'
    assert l[2]['url'] == u'http://seasonvar.ru/serial-13474-Skitaletc_Endry.html'
    assert l[2]['date'] == datetime(2016, 4, 12, 21, 45, 23)
