
class Player:
    def __init__(self, name, image):
        self.__name = name
        self.__position_board = 0
        self.__age = 0
        self.__turn = False
        self.__image = image

    @property
    def position_board(self):
        return self.__position_board

    @position_board.setter
    def position_board(self, position):
        self.__position_board = position

    @property
    def turn(self):
        return self.__turn

    @turn.setter
    def turn(self, turn):
        self.__turn = turn

    @property
    def image(self):
        return self.__image


