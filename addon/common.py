# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#
"""This file define all constants for kodi
it also holds plugin name and common path operations"""

import sys
import xbmc
import xbmcaddon
try:
    from urllib import urlencode
    import urlparse
except ImportError:
    from urllib.parse import urlencode
    from urllib.parse import urlparse


class __logger:
    def __init__(self, logger_name):
        pass

    def debug(self, s):
        return xbmc.log(s, xbmc.LOGDEBUG)

    def info(self, s):
        return xbmc.log(s, xbmc.LOGNOTICE)

    def warning(self, s):
        return xbmc.log(s, xbmc.WARNING)


def getLogger(name):
    return __logger(name)


def show_notification(title, message, icon, timeout=2000):
    if show_notification.proportionalTextLengthTimeout:
        timeout = min(len(message)/10*2000, timeout)
    title = title.replace('"', '\\"')
    message = message.replace('"', '\\"')
    xbmc.executebuiltin('Notification("%s","%s","%s","%s")' % (
        title.encode('ascii', 'ignore'),
        message.encode('ascii', 'ignore'),
        timeout,
        icon))
show_notification.proportionalTextLengthTimeout = False


class Addon:
    def __init__(self, addon_id):
        self.__idstr = addon_id

    def make_url(self, params, addon_url=None):
        if addon_url is None:
            addon_url = self.url
        return '{0}?{1}'.format(addon_url, urlencode(params))

    @property
    def url(self):
        return sys.argv[0]

    @property
    def handler(self):
        return int(sys.argv[1], base=10)

    @property
    def args(self):
        d = urlparse.parse_qs(sys.argv[2][1:])
        return dict([(k, v[0]) for k, v in d.items() if len(v) == 1])

    @property
    def icon(self): return self.__from_xbmcaddon('icon')

    @property
    def fanart(self): return self.__from_xbmcaddon('fanart')

    @property
    def path(self): return self.__from_xbmcaddon('path')

    @property
    def type(self): return self.__from_xbmcaddon('type')

    @property
    def id(self): return self.__from_xbmcaddon('id')

    @property
    def author(self): return self.__from_xbmcaddon('author')

    @property
    def name(self): return self.__from_xbmcaddon('name')

    @property
    def version(self): return self.__from_xbmcaddon('version')

    def __from_xbmcaddon(self, name):
        a = xbmcaddon.Addon(id=self.__idstr)
        return a.getAddonInfo(name)
