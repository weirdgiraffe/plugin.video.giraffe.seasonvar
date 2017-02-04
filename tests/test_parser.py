# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
import codecs
import os
import pytest
from seasonvar import parser
import pprint



def assetpath(path):
    return os.path.join(os.path.dirname(__file__), 'assets', path)


@pytest.mark.parametrize('asset, expected_count', [
    ('serial-15030-Izgoi_2016-2-season.html', 2),
    ('serial-15031-Sdelano_iz_vtorsyr_ya.html', 1),
    ('serial-15123-Major_i_magiya.html', 1),
])
def test_parse_seasons(asset, expected_count):
    with codecs.open(assetpath(asset), 'r', 'utf-8') as f:
        seasons = list(parser.seasons(f.read()))
        assert len(seasons) == expected_count


@pytest.mark.parametrize('asset, expected_count', [
    ('serial-15030-Izgoi_2016-2-season.html', 4),
    ('serial-15031-Sdelano_iz_vtorsyr_ya.html', 0),
    ('serial-15123-Major_i_magiya.html', 0),
])
def test_parse_playlists(asset, expected_count):
    with codecs.open(assetpath(asset), 'r', 'utf-8') as f:
        playlists = list(parser.playlists(f.read()))
        assert len(playlists) == expected_count


@pytest.mark.parametrize('asset, expected_count', [
    ('serial-15030-Izgoi_2016-2-season.html', 5),
    ('serial-15031-Sdelano_iz_vtorsyr_ya.html', 1),
    ('serial-15123-Major_i_magiya.html', 0),
])
def test_parse_playlists_fallback(asset, expected_count):
    with codecs.open(assetpath(asset), 'r', 'utf-8') as f:
        playlists = list(parser.playlists_fallback(f.read()))
        assert len(playlists) == expected_count
