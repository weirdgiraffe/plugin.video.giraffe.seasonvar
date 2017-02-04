# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
import os
import pytest
import re
import requests
import seasonvar.parser as parser
from seasonvar.requester import Requester
from datetime import datetime


@pytest.mark.online
def test_parse_main_page_items_online():
    req = Requester()
    main_page_html = req.main_page()
    print(type(main_page_html))
    date = datetime.today()
    datestr = date.strftime('%d.%m.%Y')
    changes = list(parser.main_page_items(main_page_html, datestr))
    assert len(changes) > 0
    for c in changes:
        assert 'url' in c
        assert c['url'] != ''
        assert 'name' in c
        assert c['name'] != ''
        assert 'changes' in c
        assert c['changes'] != ''


@pytest.mark.online
@pytest.mark.parametrize('term, min_suggestions', [
    ('bone', 1),
    ('привет', 1),
    ('hhhhhhhhhhhhhhhhhhhпривет', 0),
])
def test_pase_latin_search_items_online(term, min_suggestions):
    req = Requester()
    search_response = req.search(term)
    suggestions = list(parser.search_items(search_response))
    assert len(suggestions) >= min_suggestions
    for i in suggestions:
        assert i['url'] is not None


@pytest.mark.skipif(os.getenv('TRAVIS', 'false') == 'true',
                    reason='TRAVIS could not access this CDN')
@pytest.mark.online
def test_online_episodes():
    req = Requester()
    page = req.season_page(
            'http://seasonvar.ru/serial-13945-Horoshee_mesto.html')
    t = list(parser.playlists(page))
    assert len(t) > 0
    pl = t[-1]
    assert 'url' in pl
    assert 'tr' in pl
    playlist = req.playlist(pl['url'])
    assert playlist is not None
    episodes = list(parser.episodes(playlist))
    assert len(episodes) > 0
    for e in episodes:
        assert re.match(r'.*\.(m3u8|mp4)$', e['url'])
        assert len(e['name']) != 0
        res = requests.head(e['url'])
        assert res.status_code == 200
