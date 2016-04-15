#!/usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#
from addon.common import Addon, getLogger
from datetime import datetime, timedelta
import seasonvar.rss as rss
from seasonvar.series import Series, url2thumb
from seasonvar.requester import HTTPError, NetworkError
import xbmcgui
import xbmcplugin


addon = Addon('plugin.video.me.seasonvar')
logger = getLogger('plugin.video.me.seasonvar')


def li(name, **kwargs):
    thumb = kwargs.get('thumb')
    li = xbmcgui.ListItem(name)
    if thumb is not None:
        li.setArt(thumb)
    return li


def add_directory_to_list(dirname, url, **kwargs):
    items_count = kwargs.get('items_count')
    litem = li(dirname, **kwargs)
    ret = xbmcplugin.addDirectoryItem(addon.handler,
                                      url, litem,
                                      True, items_count)
    if not ret:
        logger.error('failed to add {0} directory item'.format(dirname))


def add_item_to_list(name, url, **kwargs):
    litem = li(name, **kwargs)
    ret = xbmcplugin.addDirectoryItem(addon.handler, url, litem)
    if not ret:
        logger.error('failed to add {0} item'.format(name))


def list_end():
    xbmcplugin.endOfDirectory(addon.handler)


def screen_start(args):
    for offset in range(7):
        date = datetime.today()
        date += timedelta(days=1)
        add_directory_to_list(
            date.strftime('%d.%m.%Y'),
            addon.make_url({'action': 'screen_date',
                            'date': date})
        )
    add_directory_to_list(
        u'Поиск',
        addon.make_url({'action': 'screen_alphabet'})
    )
    list_end()


def screen_date(args):
    try:
        date = datetime.strptime(args.get('date'), '%d.%m.%Y')
    except Exception as e:
        logger.error(
            'screen_date: "date" is missing or malformed: {0} : {1}'.format(
                e, args))
        return
    date_items = [x for x in rss.items()
                  if x['date'].month == date.month
                  and x['date'].day == date.day]
    if date_items is None:
        logger.error('screen_date: date {0} not found'.format(date))
        return
    for item in date_items:
        name = item['entry']
        add_directory_to_list(
            name,
            addon.make_url({'action': 'screen_episodes',
                            'url': item['url']}),
            thumb=url2thumb(item['url'])
        )
    list_end()


def screen_episodes(args):
    try:
        url = args.get('url')
        series = Series(url)
    except HTTPError as e:
        logger.error(e)
        return
    except NetworkError as e:
        logger.error(e)
        return
    except TypeError:
        logger.error('screen_episodes: "url" arg is missing {0}'.format(args))
        return
    seasons_count = len(series.seasons)
    season = series.current_season
    if seasons_count:
        add_directory_to_list(
            u'сезон {0}/{1}'.format(season.number, seasons_count),
            {'action': 'screen_seasons', 'url': url},
            items_count=len(series.seasons)
        )
    for episode in season.episodes:
        add_item_to_list(
            episode['name'],
            {'action': 'play', 'url': episode['url']}
        )
    list_end()


def screen_seasons(args, seasonvar):
    name = args.get('name')
    if name is None:
        logger.error('screen_seasons: "name" arg is missing {0}'.format(args))
        return
    series = seasonvar.series(name)
    if series is None:
        logger.error('screen_seasons: not found {0}'.format(name))
        return
    for season in series.seasons:
        add_item_to_list(
            u'сезон {0}'.format(season.number),
            season['name'],
            {'action': 'screen_episodes', 'season': season.number}
        )
    list_end()


def play(args, seasonvar):
    url = args.get('url')
    if url is None:
        logger.error('play: "url" arg is missing {0}'.format(args))
        return
    playurl = seasonvar.resolve_url(url)
    if playurl is None:
        logger.error('play: failed to resolve {0}'.format(url))
        return
    item = xbmcgui.ListItem(path=playurl)
    item.setProperty('IsPlayable', 'true')
    xbmcplugin.setResolvedUrl(addon.handler, True, item)


if __name__ == "__main__":
    if 'action' in addon.args:
        try:
            action = addon.args['action']
            {'screen_start': screen_start,
             'screen_date': screen_date,
             'screen_episodes': screen_episodes,
             'screen_seasons': screen_seasons,
             'play': play,
             }[action](addon.args)
        except KeyError:
            logger.error('wrong action {0}'.format(addon.args['action']))
