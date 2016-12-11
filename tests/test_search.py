# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#
import pytest
assert pytest
from seasonvar.search import items


def test_search_no_results(requests_mock):
    requests_mock.respond(r'.*', 'assets/search-no-results.json')
    l = list(items('jjjjjjjjjjjjjjjjjjjjjj'))
    assert len(l) == 1
    assert l[0]['url'] is None


def test_search_cyrilic(requests_mock):
    requests_mock.respond(r'.*', 'assets/search-cyrilic.json')
    term = 'привет'
    l = list(items(term))
    assert len(l) == 8
    for i in l:
        assert i['url'] is not None


def test_search_results(requests_mock):
    requests_mock.respond(r'.*', 'assets/search-bone-results.json')
    l = list(items('bone'))
    assert len(l) == 18
    for i in l:
        assert i['url'] is not None
