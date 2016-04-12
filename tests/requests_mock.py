#!/usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#
import pytest
import os
import re


def memoize(f):
    """ Memoization decorator for a function taking a single argument """
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret
    return memodict().__getitem__


@memoize
def file_content(path):
    with open(path) as inputf:
        return inputf.read()


class RequestsMockResult:
    def __init__(self, path, status_code):
        self.text = file_content(path)
        self.status_code = status_code


class RequestsMock:
    def __init__(self):
        methods = ['GET', 'POST']
        self.responses = {}
        self.counters = {}
        for m in methods:
            self.responses[m] = []
            self.counters[m] = 0

    def respond(self, url_regexp, relpath, methods=['GET']):
        thisdir = os.path.dirname(__file__)
        path = os.path.join(thisdir, relpath)
        for m in methods:
            self.responses[m] += [(re.compile(url_regexp), path, 200)]

    def get(self, url, *args, **kwargs):
        for regexp, path, status in self.responses['GET']:
            if regexp.search(url):
                return RequestsMockResult(path, status)
        pytest.fail("unexpected HTTP GET url:{0} args: {1} kwargs:{2}".format(
            url, args, kwargs))

    def post(self, url, *args, **kwargs):
        for regexp, path, status in self.responses['POST']:
            if regexp.search(url):
                return RequestsMockResult(path, status)
        pytest.fail("unexpected HTTP POST url:{0} args: {1} kwargs:{2}".format(
            url, args, kwargs))


@pytest.fixture()
def requests_mock(monkeypatch):
    mock = RequestsMock()
    monkeypatch.setattr('requests.Session.get', mock.get)
    monkeypatch.setattr('requests.Session.post', mock.post)
    monkeypatch.setattr('requests.get', mock.get)
    monkeypatch.setattr('requests.post', mock.post)
    return mock
