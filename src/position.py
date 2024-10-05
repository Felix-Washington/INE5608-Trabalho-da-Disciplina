

class Position:
    def __init__(self, new_type, widget, image_path):
        super().__init__()
        self.__type = new_type
        self.__occupants = []
        # Used for Label
        self.__widget = widget
        self.__image = image_path

    def add_occupant(self, player):
        self.occupants.append(player)

    def remove_occupant(self, player):
        self.occupants.remove(player)

    @property
    def occupants(self):
        return self.__occupants

    @property
    def image(self):
        return self.__image

    @property
    def widget(self):
        return self.__widget

    @property
    def type(self):
        return self.__type

    @occupants.setter
    def occupants(self, occupants):
        self.__occupants = occupants

    @widget.setter
    def widget(self, widget):
        self.__widget = widget
