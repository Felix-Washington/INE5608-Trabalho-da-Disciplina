
class player:
    def __init__(self):
        self.__name = ""
        self.__position_board = 0
        self.__age = 0
        self.__turn = False

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


