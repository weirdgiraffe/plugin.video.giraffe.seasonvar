# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
import sys

try:  # real kodi
    import xbmc
    import xbmcaddon
except ImportError:  # mocked kodi
    from mock_kodi import xbmcaddon
    from mock_kodi import xbmc

try:  # python2
    from urlparse import urlparse, parse_qs
except ImportError:  # python3
    from urllib.parse import urlparse, parse_qs


class logger:
    @staticmethod
    def debug(s):
        xbmc.log(s, xbmc.LOGDEBUG)

    @staticmethod
    def info(s):
        xbmc.log(s, xbmc.LOGNOTICE)

    @staticmethod
    def error(s):
        s += '\n\taddon arguments:\n\t{0}'.format('\n\t'.join(sys.argv[1:]))
        xbmc.log(s, xbmc.LOGERROR)


class Plugin:
    def __init__(self, *args):
        self._addon = xbmcaddon.Addon()
        self._url = args[0]
        self._handler = int(args[1], base=10)
        # addon url has format:
        #   plugin://plugin.hello.blah?arg1=xxx&arg2=xxx
        # where args are urlencoded
        o = urlparse(args[2])
        self._args = dict()
        for k, v in parse_qs(o.query).items():
            if len(v) == 1:
                self._args[k] = v[0]
            else:
                self._args[k] = v

    @property
    def icon(self):
        return self._addon.getAddonInfo('icon')

    @property
    def args(self):
        return self._args

    def settings_value(self, setting_id):
        return self._addon.getSetting(setting_id)

    def show_notification(self, title, message):
        timeout = len(message) / 10 * 2000
        title = title.replace('"', '\\"')
        message = message.replace('"', '\\"')
        xbmc.executebuiltin('Notification("{0}","{1}","{2}","{3}")'.format(
            title.encode('ascii', 'ignore'),
            message.encode('ascii', 'ignore'),
            timeout,
            self.icon))


plugin = Plugin(*sys.argv)
