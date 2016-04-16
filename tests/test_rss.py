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


def test_rss_extract_something(requests_mock):
    requests_mock.respond(r'.*', 'assets/rss-01.xml')
    l = list(items('12.04.2016'))
    assert len(l) == 3


def test_rss_extract_entries(requests_mock):
    requests_mock.respond(r'.*', 'assets/rss-01.xml')
    l = list(items('12.04.2016'))
    assert len(l) == 3
    assert l[0]['name'] == 'Скорпион'
    assert l[0]['changes'] == '(2 сезон) 22 серия'
    assert l[0]['url'] == '/serial-12394-Skorpion_serial_2014_ndash_.html'
    assert l[1]['name'] == 'Гаргантия на зеленой планете: '\
                           'Морские тропы за горизонт'
    assert l[1]['changes'] == '(1 сезон) 1 серия'
    assert l[1]['url'] == '/serial-13480-Gargantiya_na_'\
                          'zelnoj_planete_Morskie_tropy_za_gorizont.html'
    assert l[2]['name'] == 'Скиталец Эндры'
    assert l[2]['changes'] == '1-2 серия'
    assert l[2]['url'] == '/serial-13474-Skitaletc_Endry.html'
