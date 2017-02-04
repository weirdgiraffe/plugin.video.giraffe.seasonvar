# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
import re


def seasons(season_page_html):
    '''takes content of season page and yields
    all seasons for the same show.

    season_page_html should be utf-8 encoded html content
    '''
    r = re.compile(
            r'<h2>.*?'
            r'href="(/serial-\d+-[^-.]+(:?-\d+-(sezon|season))?\.html)".*?',
            re.DOTALL)
    for url in r.findall(season_page_html):
        yield url


def playlists(season_page_html):
    '''takes content of season page and yields
    dict with translation name and playlist url.

    season_page_html should be utf-8 encoded html content
    '''
    div = _translate_div(season_page_html)
    if div is not None:
        r = re.compile(r'<li\s+id="translate.*?>(.*?)</li>.*?'
                       r'var\s+pl\d+\s+=\s+"(.*?)";',
                       re.DOTALL)
        for name, url in r.findall(div):
            yield {'tr': name.strip(),
                   'url': url.strip()}


def playlists_fallback(season_page_html):
    '''takes content of season page and yields
    dict with translation name and playlist url, but
    search only for playlists on page, translation
    name will be None.

    season_page_html should be utf-8 encoded html content
    '''
    r = re.compile(r'var\s+pl\d+\s+=\s+"(.+)";')
    for url in r.findall(season_page_html):
        yield {'tr': None,
               'url': url.strip()}


def _translate_div(season_page_html):
    r = re.compile(r'<ul\s+id="translateDiv"(.*?)</ul>', re.DOTALL)
    for b in r.findall(season_page_html):
        return b

