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
    import xbmcgui
    import xbmcplugin
except ImportError:  # mocked kodi
    from mock_kodi import xbmc
    from mock_kodi import xbmcaddon
    from mock_kodi import xbmcgui
    from mock_kodi import xbmcplugin

try:  # python2
    from urlparse import urlparse, parse_qs, urlencode
except ImportError:  # python3
    from urllib.parse import urlparse, parse_qs, urlencode


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


def list_item(name, **kwargs):
    thumb = kwargs.get('thumb')
    playable = kwargs.get('playable')
    li = xbmcgui.ListItem(name)
    if thumb is not None:
        li.setArt(thumb)
        # it is sayed that both of these methods are deprecated
        # see: http://kodi.wiki/view/Jarvis_API_changes
        # but only these methods actually works with Jarvis
        li.setIconImage(thumb)
        li.setThumbnailImage(thumb)
    if playable is not None:
        li.setProperty('IsPlayable', str(playable))
    return li


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

    def add_screen_directory(self, name, url, **kwargs):
        li = list_item(name, **kwargs)
        args = [self._handler, url, li, True]
        items_count = kwargs.get('items_count')
        if items_count:
            args += [items_count]
        ret = xbmcplugin.addDirectoryItem(*args)
        if not ret:
            logger.error('failed to add {0} directory item'.format(name))

    def publish_screen(self):
        xbmcplugin.endOfDirectory(self._handler)

    def make_url(self, argv):
        return '{0}?{1}'.format(self._url, urlencode(argv))

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
