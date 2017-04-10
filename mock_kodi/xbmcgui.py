class ListItem:
    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path
        self.property = {}

    def setThumbnailImage(self, value):
        self.property['ThumbnailImage'] = value

    def setIconImage(self, value):
        self.property['IconImage'] = value

    def setArt(self, value):
        self.property['Art'] = value

    def setProperty(self, name, value):
        self.property[name] = value

    def __str__(self):
        return '<ListItem\n'\
               '\tname={0}\n'\
               '\tpath={1}\n'\
               '\tproperties={2}\n'\
               '/>'.format(
                self.name, self.path, self.property)
