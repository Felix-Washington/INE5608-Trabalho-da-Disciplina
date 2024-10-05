
class Player:
    def __init__(self):
        self.__identifier = ''
        self.__name = 'Player'
        self.__image = None
        self.__winner = False

    def initialize(self, a_name, image, an_id):
        self.reset()
        self.__name = a_name
        self.__image = image
        self.__identifier = an_id

    def reset(self):
        self.__identifier = ""
        self.__name = ""
        self.__winner = False

    @property
    def identifier(self):
        return self.__identifier

    def get_name(self):
        return self.__name

    def get_turn(self):
        return self.__turn

    @property
    def image(self):
        return self.__image

    @property
    def name(self):
        return self.__name

    @property
    def winner(self):
        return self.__winner

    @winner.setter
    def winner(self, winner):
        self.__winner = winner
