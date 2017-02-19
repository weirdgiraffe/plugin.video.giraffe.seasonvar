class ListItem:
    def __init__(self, name):
        self._name = name
        pass

    def __str__(self):
        return '<ListItem name={0}>'.format(self._name)
