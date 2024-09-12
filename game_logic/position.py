class Position:
    def __init__(self, tipo_casa, widget):
        self.tipo = tipo_casa
        self.occupants = []
        self.widget = widget


    def store(self, player):
        self.occupants.append(player)

    def remove(self, player):
        self.occupants.remove(player)


    @property
    def get_widget(self):
        return self.widget