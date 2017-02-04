# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
import logging
import os
import sys

# These two lines enable debugging at httplib level
# (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with
# HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import httplib as http_client
except ImportError:  # Python 3
    import http.client as http_client

http_client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# add parent directory to python path
# to enable import of tested package
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
