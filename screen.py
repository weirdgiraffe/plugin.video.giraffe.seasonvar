# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
from kodi import plugin, logger
from seasonvar import requester

if __name__ == "__main__":
    screen = plugin.args.get('screen')
    if screen is not None:
        try:
            {'week': None,
             'date': None,
             'episodes': None,
             'seasons': None,
             'translations': None,
             }[screen]()
        except KeyError:
            logger.error('unexpected screen "{0}"'.format(screen))
        except requester.NetworkError:
            logger.error('NetworkError')
            plugin.show_notification(
                'Network error',
                'Check your connection')
        except requester.HTTPError:
            logger.error('HTTPError')
            plugin.show_notification(
                'HTTP error',
                'Something goes wrong. Please, send your logs to addon author')
