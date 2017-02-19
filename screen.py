# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
from kodi import plugin, logger
from seasonvar import requester
from datetime import datetime, timedelta


def week():
    date = datetime.today()
    for date_offset in range(7):
        datestr = date.strftime('%d.%m.%Y')
        dayurl = plugin.make_url({'screen': 'day', 'date': datestr})
        plugin.add_screen_directory(datestr, dayurl)
        date -= timedelta(days=1)

    searchurl = plugin.make_url({'screen': 'search'})
    plugin.add_screen_directory('[COLOR FFFFD700]поиск[/COLOR]', searchurl)
    plugin.publish_screen()


if __name__ == "__main__":
    screen = plugin.args.get('screen')
    if screen is not None:
        try:
            {'week': week,
             'day': None,
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
