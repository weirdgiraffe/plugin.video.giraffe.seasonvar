# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
from __future__ import unicode_literals
import os
import pytest
import sys
from kodi_mock import addon, kodi
from requests_mock import requests_mock

assert requests_mock
assert pytest
assert addon
assert kodi

sys.path.append(os.path.join(os.getcwd(), './resources/site-packages'))
