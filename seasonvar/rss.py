#!/usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#

try:
    from seasonvar.requester import Requester
except ImportError:
    from requester import Requester
import re
from datetime import datetime


FEEDURL = 'http://seasonvar.ru/rss.php'


def items():
    requester = Requester()
    regexp = re.compile(
        r'<title><!\[CDATA\[([^\]]+?)\]\]><\/title>[^<]*?'
        '<link>([^<]+?)<\/link>[^<]*?'
        '<pubDate>([^<]+?)<\/pubDate>',
        re.DOTALL)
    xml = requester.get(FEEDURL)
    for (entry, link, datestr) in regexp.findall(xml):
        yield {
            'entry': entry,
            'url': link,
            'date': datetime.strptime(
                datestr,
                '%a, %d %b %Y %H:%M:%S %z')
        }
