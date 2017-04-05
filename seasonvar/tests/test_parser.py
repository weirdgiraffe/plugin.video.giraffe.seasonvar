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
    ('dayblock_single.html', ['03.04.2017']),
    ('dayblock_multiple.html', ['03.04.2017', '02.04.2017'])
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
        {
            'changes': '(6 сезон) 11 серия (Amedia)',
            'name': 'Родина',
            'url': '/serial-14903-Rodina-00006-sezon.html'
        },
        {
            'changes': '10 серия (Котова)',
            'name': 'До самой смерти',
            'url': '/serial-14996-Do_samoj_smerti.html'
        }]),
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


def test_parse_seasons():
    asset = 'serial-example-seasonlist.html'
    expected_count = 4
    with open(assetpath(asset)) as f:
        seasons = list(parser.seasons(f.read()))
        assert len(seasons) == expected_count


def test_parse_player_params():
    asset = 'serial-example-playerparams.html'
    with open(assetpath(asset)) as f:
        params = parser.player_params(f.read())
        assert params


@pytest.mark.parametrize('asset, expected_count', [
    ('player-response-example-single.html', 1),
    ('player-response-example-multi.html', 7),
])
def test_parse_playlists(asset, expected_count):
    with open(assetpath(asset)) as f:
        playlists = list(parser.playlists(f.read()))
        assert len(playlists) == expected_count


@pytest.mark.parametrize('asset, expected_count', [
    ('playlist-dom2.json', 462),
    ('playlist-scorpion.json', 22),
])
def test_parse_episodes(asset, expected_count):
    with open(assetpath(asset)) as f:
        items = list(parser.episodes(json.loads(f.read())))
        assert len(items) == expected_count
        for i in items:
            assert 'name' in i
            assert 'name' != ''
            assert 'url' in i
            assert 'url' != ''
