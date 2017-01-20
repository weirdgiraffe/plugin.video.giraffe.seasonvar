#!/usr/bin/python
# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
from __future__ import unicode_literals
import sys
import os
import xbmcaddon


__a = xbmcaddon.Addon(id='plugin.video.giraffe.seasonvar')
sys.path.append(os.path.join(__a.getAddonInfo('path'),
                             'resources',
                             'site-packages'))


if __name__ == '__main__':
    from addon.plugin_video import main
    main()
