import logging

LOGDEBUG = 1
LOGNOTICE = 2
LOGERROR = 3
logger = logging.getLogger("mock_kodi")


def log(s, loglevel):
    if loglevel == LOGDEBUG:
        logger.debug(s)
    elif loglevel == LOGNOTICE:
        logger.info(s)
    elif loglevel == LOGERROR:
        logger.error(s)


def executebuiltin(s):
    pass
