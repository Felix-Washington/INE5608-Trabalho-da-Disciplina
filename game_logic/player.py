
class Player:
    def __init__(self):
        self.__identifier = ''
        self.__name = ''
        self.__image = None
        self.__position_board = 0
        self.__turn = False
        self.__winner = False

    def initialize(self, an_id, a_Image, a_name):
        self.reset()
        self.identifier = an_id
        self.image= a_Image
        self.name = a_name

    def reset(self):
        self.identifier = ""
        self.name = ""
        self.symbol = None
        self.turn = False
        self.winner = False
        self.position_board = 0

    def toogle_turn(self):
        if self.turn == False:
            self.turn = True
        elif self.turn == True:
            self.turn = False

    def move_position(self, num_positions, is_right):
        if is_right:
            self.__position_board += num_positions
        else:
            self.__position_board -= num_positions

    def get_position_board(self):
        return self.__position_board

    def get_identifier(self):
        return self.__identifier

    def get_name(self):
        return self.__name

    def get_turn(self):
        return self.__turn

    def get_image(self):
        return self.__image

    def get_name(self):
        return self.__name

    def get_winner(self):
        return self.__winner
    
    def set_winner(self):
        self.__winner = True