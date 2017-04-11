# coding: utf-8

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#
import requests
try:
    from urlparse import urlparse, urljoin
    from urllib import quote

    def utf8(unicodestr):
        return unicodestr.encode('utf-8')

except ImportError:  # for python 3
    from urllib.parse import quote, urlparse, urljoin

    def utf8(unicodestr):
        return unicodestr


class NetworkError(Exception):
    """exception which occures on any kind of network error
    i.e. not able to connect, not able to resolve, etc."""
    pass


class HTTPError(Exception):
    """exception which occures on any kind of http codes excluding 200"""
    pass


class Requester(object):
    def __init__(self):
        self.BASEURL = 'http://seasonvar.ru'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) '
                          'AppleWebKit/601.1.46 (KHTML, like Gecko) '
                          'Version/9.0 Mobile/13B143 Safari/601.1',
            'Host': 'seasonvar.ru',
            'Accept-Language': 'ru-RU',
            'Origin': 'http://seasonvar.ru',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, sdch'
        })
        self.session.cookies.update({
            'html5default': '1',
            'uppodhtml5_volume': '1',
            'IIIIIIIIIIIIIIIII': 'WerTylv_tr',
            'sva': 'lVe324PqsI24',
            })

    def main_page(self):
        '''return utf-8 encoded main page as str'''
        return utf8(self._get(self.BASEURL).text)

    def search(self, term):
        '''search for term using autocompletion
        return dict representing utf-8 encoded json
        response from server

        term should be utf-8 encoded string
        '''
        term = quote(term)
        url = urljoin(self.BASEURL, 'autocomplete.php')
        url += '?query={0}'.format(term)
        return self._get(url).json()

    def season_page(self, season_url):
        '''return utf-8 encoded season page as str

        season url should be urlencoded utf-8 str
        '''
        url = urljoin(self.BASEURL, season_url)
        return utf8(self._get(url).text)

    def player(self, referer, player_params):
        '''return utf-8 encoded response from player.php
        player_params is a dict with parameters
        '''
        url = urljoin(self.BASEURL, '/player.php')
        refurl = urljoin(self.BASEURL, referer)
        return utf8(self._xhtml(url, refurl, player_params).text)

    def playlist(self, url):
        '''get playlist and return dict representing utf-8 encoded json'''
        url = urljoin(self.BASEURL, url)
        return self._get(url).json()

    def _get(self, url):
        try:
            page = self.session.get(url)
            if page.status_code == 200:
                page.encoding = 'utf-8'
                return page
            else:
                raise HTTPError('GET {0}\n{1}'.format(url, page))
        except requests.exceptions.RequestException as e:
            raise NetworkError(repr(e))

    def _xhtml(self, url, referer, data):
        try:
            page = self.session.post(
                    url,
                    headers={
                        'Referer': referer,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    data=data)
            if page.status_code == 200:
                page.encoding = 'utf-8'
                return page
            else:
                raise HTTPError('POST {0}\n{1}'.format(url, page))
        except requests.exceptions.RequestException as e:
            raise NetworkError(repr(e))
