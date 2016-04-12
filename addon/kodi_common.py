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
import os
import urlparse
import xbmc
import xbmcaddon


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


def __parse_args():
    d = urlparse.parse_qs(sys.argv[2][1:])
    return dict([(k, v[0]) for k, v in d.items() if len(v) == 1])

addon = xbmcaddon.Addon(id=ADDON_NAME)
sys.path.append(os.path.join(addon.getAddonInfo('path'), 'resources', 'lib'))

addon_url = sys.argv[0]
addon_handler = int(sys.argv[1], base=10)
addon_args = __parse_args()
addon_icon = addon.getAddonInfo('icon')
addon_fanart = addon.getAddonInfo('fanart')
addon_path = addon.getAddonInfo('path')
addon_type = addon.getAddonInfo('type')
addon_id = addon.getAddonInfo('id')
addon_author = addon.getAddonInfo('author')
addon_name = addon.getAddonInfo('name')
addon_version = addon.getAddonInfo('version')
