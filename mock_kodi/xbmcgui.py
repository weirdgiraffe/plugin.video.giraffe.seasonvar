class ListItem:
    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path
        self.properties = {}

    def setProperty(self, name, value):
        self.properties[name] = value

    def __str__(self):
        return '<ListItem\n'\
               '\tname={0}\n'\
               '\tpath={1}\n'\
               '\tproperties={2}\n'\
               '/>'.format(
                self.name, self.path, self.properties)
