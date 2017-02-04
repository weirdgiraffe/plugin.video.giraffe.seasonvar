# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
import json
import os
import pytest
import seasonvar.parser as parser


def assetpath(path):
    return os.path.join(os.path.dirname(__file__), 'assets', path)


@pytest.mark.parametrize('asset, expected_dates', [
    ('dayblock_single.html', ['15.01.2017']),
    ('dayblock_multiple.html', ['15.01.2017', '14.01.2017'])
])
def test_parse_main_page_dayblock(asset, expected_dates):
    with open(assetpath(asset)) as f:
        dates = []
        for d, content in parser._main_page_dayblocks(f.read()):
            dates.append(d)
            assert len(content) > 0
        assert dates == expected_dates


@pytest.mark.parametrize('asset, expected_items', [
    ('dayblock_single.html', [
        {'changes': '2 серия (Hamster)',
         'name': 'Табу',
         'url': '/serial-14866-Tabu.html'},
        {'changes': '1 серия (NewStudio)',
         'name': 'Лемони Сникет: 33 несчастья',
         'url': '/serial-14959-Lemoni_Sniket_33_neschast_ya.html'},
        {'changes': '(1 сезон) 8 серия',
         'name': 'Однофунтовое Евангелие',
         'url': '/serial-14606-Odnofuntovoe_Evangelie.html'}]),
])
def test_parse_dayblock_items(asset, expected_items):
    with open(assetpath(asset)) as f:
        html = f.read()
        dayblocks = [c for x, c in parser._main_page_dayblocks(html)]
        assert len(dayblocks) == 1
        assert len(dayblocks[0]) > 0
        items = [x for x in parser._main_page_dayblock_items(dayblocks[0])]
        assert len(items) == len(expected_items)
        assert items == expected_items


@pytest.mark.parametrize('asset, expected_suggestions', [
    ('search-no-results.json', 0),
    ('search-cyrilic-results.json', 8),
    ('search-bone-results.json', 18),
])
def test_parse_search_response(asset, expected_suggestions):
    with open(assetpath(asset)) as f:
        items = [x for x in parser.search_items(json.loads(f.read()))]
        assert len(items) == expected_suggestions
        for i in items:
            assert i['url'] is not None


@pytest.mark.parametrize('asset, expected_count', [
    ('serial-15030-Izgoi_2016-2-season.html', 2),
    ('serial-15031-Sdelano_iz_vtorsyr_ya.html', 1),
    ('serial-15123-Major_i_magiya.html', 1),
])
def test_parse_seasons(asset, expected_count):
    with open(assetpath(asset)) as f:
        seasons = list(parser.seasons(f.read()))
        assert len(seasons) == expected_count


@pytest.mark.parametrize('asset, expected_count', [
    ('serial-15030-Izgoi_2016-2-season.html', 4),
    ('serial-15031-Sdelano_iz_vtorsyr_ya.html', 0),
    ('serial-15123-Major_i_magiya.html', 0),
])
def test_parse_playlists(asset, expected_count):
    with open(assetpath(asset)) as f:
        playlists = list(parser.playlists(f.read()))
        assert len(playlists) == expected_count


@pytest.mark.parametrize('asset, expected_count', [
    ('serial-15030-Izgoi_2016-2-season.html', 5),
    ('serial-15031-Sdelano_iz_vtorsyr_ya.html', 1),
    ('serial-15123-Major_i_magiya.html', 0),
])
def test_parse_playlists_fallback(asset, expected_count):
    with open(assetpath(asset)) as f:
        playlists = list(parser.playlists_fallback(f.read()))
        assert len(playlists) == expected_count

