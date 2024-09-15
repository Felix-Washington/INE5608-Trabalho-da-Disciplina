import tkinter as tk


class Position(tk.Label):
    def __init__(self, position_type, widget):
        super().__init__()
        self.__position_type = position_type
        self.__occupants = []
        self.__widget = widget

    def add_occupant(self, player):
        self.occupants.append(player)

    def remove_occupant(self, player):
        self.occupants.remove(player)

    @property
    def occupants(self):
        return self.__occupants

    @property
    def get_widget(self):
        return self.__widget

    @property
    def position_type(self):
        return self.__position_type

    @occupants.setter
    def occupants(self, occupants):
        self.__occupants = occupants
