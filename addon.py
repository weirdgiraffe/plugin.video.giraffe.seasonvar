#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import xbmcaddon


__a = xbmcaddon.Addon(id='plugin.video.giraffe.seasonvar')
sys.path.append(os.path.join(__a.getAddonInfo('path'),
                             'resources',
                             'site-packages'))


if __name__ == '__main__':
    from addon import plugin_video
    plugin_video.main()
