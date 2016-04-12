#!/usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#
import pytest
assert pytest
from seasonvar.requester import Requester


def test_requester_set_ipad_useragent(requests_mock):
    requester = Requester()
    useragent = requester.session.headers['User-Agent']
    assert useragent == 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) '\
                        'AppleWebKit/537.51.1 (KHTML, like Gecko) '\
                        'Version/7.0 Mobile/11A465 Safari/9537.53'
