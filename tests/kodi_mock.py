# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
from __future__ import unicode_literals
import logging
import pytest
import re
try:
    from urlparse import parse_qsl, urlparse
except ImportError:  # to be python3 compatible (not for kodi)
    from urllib.parse import parse_qsl, urlparse


class Addon:
    def __init__(self):
        self.handler = 123
        self.url = 'plugin://{0}/'.format(id)
        self.args = {}
        self.icon = '/icon.jpg'
        self.fanart = '/fanart.jpg'
        self.path = '/addon/'
        self._type = 'addon-type'
        self._id = 'addon-id'
        self.author = 'addon-author'
        self.name = 'addon-name'
        self.version = 'addon-version'
        self.notification_shown = False

    def show_notification(self, *args, **kwargs):
        self.notification_shown = True


@pytest.fixture()
def addon(monkeypatch):
    a = Addon()
    monkeypatch.setattr('addon.common.Addon.handler', a.handler)
    monkeypatch.setattr('addon.common.Addon.args', a.args)
    monkeypatch.setattr('addon.common.Addon.icon', a.icon)
    monkeypatch.setattr('addon.common.show_notification', a.show_notification)
    monkeypatch.setattr('addon.plugin_video.show_notification',
                        a.show_notification)
    monkeypatch.setattr('addon.plugin_video.logger', logging.getLogger('test'))
    return a


class ListItem:
    def __init__(self, name=None, path=None):
        # name should not start with whitespaces
        if name is not None:
            assert re.match(r'^[^\s]', name)
        self.name = name
        self.path = path
        self.properties = {}

    def setArt(self, url):
        o = urlparse(url)
        # check that art url is absolute url
        assert o.netloc
        self.thumb = url

    def setIconImage(self, url): self.setArt(url)

    def setThumbnailImage(self, url): self.setArt(url)

    def setProperty(self, name, value):
        self.properties[name] = value


class Kodi:
    def __init__(self):
        self.items = []

    def ListItem(self, *args, **kwargs):
        return ListItem(*args, **kwargs)

    def addDirectoryItem(self, handler, url, li, is_dir, count=-1):
        assert isinstance(handler, int)
        assert url is not None
        assert li is not None
        assert isinstance(is_dir, bool)
        assert isinstance(count, int)
        if count == -1:
            count = None
        self.items.append({
            'handler': handler,
            'url': url,
            'urlparams': self.__url_params(url),
            'li': li,
            'is_dir': is_dir,
            'count': count
        })
        return True

    def endOfDirectory(self, handler):
        pass

    def setResolvedUrl(self, handler, play, li):
        self.resolved = li

    def __url_params(self, url):
        o = urlparse(url)
        return dict(parse_qsl(o.query))


@pytest.fixture()
def kodi(monkeypatch):
    kodi_instance = Kodi()
    monkeypatch.setattr('xbmcgui.ListItem',
                        kodi_instance.ListItem)
    monkeypatch.setattr('xbmcplugin.addDirectoryItem',
                        kodi_instance.addDirectoryItem)
    monkeypatch.setattr('xbmcplugin.endOfDirectory',
                        kodi_instance.endOfDirectory)
    monkeypatch.setattr('xbmcplugin.setResolvedUrl',
                        kodi_instance.setResolvedUrl)
    return kodi_instance
