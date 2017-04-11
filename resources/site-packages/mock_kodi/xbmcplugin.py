try:  # python2
    from urlparse import urlparse, parse_qs
except ImportError:  # python3
    from urllib.parse import urlparse, parse_qs


class DirectoryItem:
    def __init__(self, handler, url, list_item, is_directory, items_count):
        self.handler = handler
        self.url = url
        self.list_item = list_item
        self.directory = is_directory
        self.items_count = items_count
        self.url_params = dict()
        o = urlparse(url)
        for k, v in parse_qs(o.query).items():
            if len(v) == 1:
                self.url_params[k] = v[0]
            else:
                self.url_params[k] = v

    def __str__(self):
        return '<DirectoryItem\n'\
               '  handler={0}\n'\
               '  url={1}\n'\
               '  item={2}\n'\
               '  directory={3}\n'\
               '  items_count={4}\n/>'.format(
                       self.handler,
                       self.url,
                       self.list_item,
                       self.directory,
                       self.items_count)


directory = []
_resolved = ''


def clear_resolved():
    global _resolved
    _resolved = None


def resolved():
    global _resolved
    return _resolved


def addDirectoryItem(handler, url, list_item, is_directory, items_count=None):
    global directory
    directory += [
            DirectoryItem(handler, url, list_item, is_directory, items_count)
            ]
    return True


def endOfDirectory(handler, success, refresh):
    for d in directory:
        print(d)


def setResolvedUrl(handle, success, li):
    global _resolved
    _resolved = li.path
