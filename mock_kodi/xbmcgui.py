class ListItem:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<ListItem name={0}>'.format(self.name)
