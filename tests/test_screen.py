# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
import pytest
import re
from datetime import datetime, timedelta
from screen import render_screen
from kodi import Plugin
from mock_kodi.xbmcplugin import directory

assert pytest


def strip_colors(instr):
    return re.sub(r'\[COLOR [A-F0-9]{8}\](.+?)\[\/COLOR\]', r'\1', instr)


def test_screen_layout_week():
    plugin = Plugin('plugin://url', '1', 'plugin://url?screen=week')
    del directory[:]
    render_screen(plugin)

    # expect list of 8 entries for last 7 days and one entry for search
    assert len(directory) == 8
    checked_date = datetime.today()
    for i in directory[:-1]:
        datestr = checked_date.strftime('%d.%m.%Y')
        assert i.list_item.name == datestr
        assert i.directory is True
        assert i.url_params['screen'] == 'day'
        assert i.url_params['date'] == datestr
        checked_date -= timedelta(days=1)

    assert directory[-1].directory is True
    assert directory[-1].url_params['screen'] == 'search'
    assert strip_colors(directory[-1].list_item.name) == 'поиск'
