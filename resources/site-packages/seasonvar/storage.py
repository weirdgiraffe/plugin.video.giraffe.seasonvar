# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
import sqlite3
import logging

logger = logging.getLogger(__name__)

class SeasonsDatabase:
    def __init__(self, path):
        self.__connection = sqlite3.connect(path)
        self.__init_tables()

    def update_season_url(self, season_name, new_url):
        with self.__connection:
            self.__connection.execute(
                'UPDATE seasons SET url=?  WHERE name=?',
                (new_url, season_name,))

    def get_season_url(self, season_name):
        with self.__connection:
            stmt = 'SELECT url FROM seasons WHERE name name=?'
            for url in self.__connection.execute(stmt, (season_name,)):
                return url

    def __init_tables(self):
        with self.__connection:
            self.__connection.execute(
                '''CREATE TABLE IF NOT EXISTS
                seasons (name text UNIQUE, url text)''')
