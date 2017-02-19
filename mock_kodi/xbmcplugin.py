
def addDirectoryItem(handler, url, list_item, is_directory, items_count=None):
    print('handler={0} url={1} item={2} directory={3} item={4}'.format(
        handler, url, list_item, is_directory, items_count))
    return True


def endOfDirectory(handler):
    print('directory published')
