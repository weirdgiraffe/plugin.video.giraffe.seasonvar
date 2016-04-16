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
from seasonvar.mainpage import items


def test_main_page_extract_something(requests_mock):
    requests_mock.respond(r'.*', 'assets/page-main-01.html')
    l = list(items('12.04.2016'))
    assert len(l) > 0
    l = list(items('11.04.2016'))
    assert len(l) > 0


def test_rss_extract_items(requests_mock):
    requests_mock.respond(r'.*', 'assets/page-main-01.html')

    l = list(items('12.04.2016'))
    assert len(l) == 3
    assert l[0]['name'] == 'Скорпион'
    assert l[0]['changes'] == '(2 сезон) 22 серия'
    assert l[0]['url'] == '/serial-12394-Skorpion_serial_2014_ndash_.html'

    assert l[1]['name'] == 'Гаргантия на зеленой планете: Морские тропы за горизонт'
    assert l[1]['changes'] == '(1 сезон) 1 серия'
    assert l[1]['url'] == '/serial-13480-Gargantiya_na_zelnoj_planete_Morskie_tropy_za_gorizont.html'

    assert l[2]['name'] == 'Скиталец Эндры'
    assert l[2]['changes'] == '1-2 серия'
    assert l[2]['url'] == '/serial-13474-Skitaletc_Endry.html'

    l = list(items('11.04.2016'))
    assert len(l) == 3
    assert l[0]['name'] == 'Время приключений'
    assert l[0]['changes'] == '(7 сезон) 29 серия'
    assert l[0]['url'] == '/serial-12665-Vremya_priklyuchenij-7-season.html'

    assert l[1]['name'] == 'Миллиарды'
    assert l[1]['changes'] == '(1 сезон) 12 серия'
    assert l[1]['url'] == '/serial-12913-Milliardy-1-season.html'

    assert l[2]['name'] == 'Теория большого взрыва'
    assert l[2]['changes'] == '(9 сезон) 20 серия (Kuraj-Bambey)'
    assert l[2]['url'] == '/serial-12387-Teoriya_bol_shogo_vzryva-9-season.html'
