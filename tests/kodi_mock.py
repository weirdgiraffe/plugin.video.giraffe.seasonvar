#!/usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#
import pytest
import logging

class Addon:
    def __init__(self, id):
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


@pytest.fixture()
def addon(monkeypatch):
    monkeypatch.setattr('addon.common.Addon.handler', 123)
    monkeypatch.setattr('addon.plugin_video.logger', logging.getLogger('test'))
    print('patched')


class ListItem:
    def __init__(self, name):
        self.name = name

    def setArt(self, url):
        self.thumb = url

    def setIconImage(self, url): self.setArt(url)
    def setThumbnailImage(self, url): self.setArt(url)


class Kodi:
    def __init__(self):
        self.items = []

    def ListItem(self, name):
        return ListItem(name)

    def addDirectoryItem(self, handler, url, li, is_dir, count=None):
        self.items.append({'handler': handler,
                           'url': url,
                           'li': li,
                           'is_dir': is_dir,
                           'count': count})
        return True

    def endOfDirectory(self, handler):
        pass


@pytest.fixture()
def kodi(monkeypatch):
    kodi_instance = Kodi()
    monkeypatch.setattr('xbmcgui.ListItem', kodi_instance.ListItem)
    monkeypatch.setattr('xbmcplugin.addDirectoryItem', kodi_instance.addDirectoryItem)
    monkeypatch.setattr('xbmcplugin.endOfDirectory', kodi_instance.endOfDirectory)
    return kodi_instance
