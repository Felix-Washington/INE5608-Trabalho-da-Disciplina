class Player:
    def __init__(self):
        self.__identifier = ''
        self.__name = 'Player'
        self.__image = None
        self.__turn = False
        self.__position_board = 0
        self.__option = -1
        self.__selected_question = -1
        self.__selected_answer = -1

    def initialize(self, a_name, image, an_id):
        self.reset()
        self.__name = a_name
        self.__image = image
        self.__identifier = an_id

    def reset(self):
        self.__identifier = ""
        self.__name = ""
        self.__turn = False
        self.__position_board = 0

    @property
    def identifier(self):
        return self.__identifier

    @property
    def position_board(self):
        return self.__position_board

    @position_board.setter
    def position_board(self, position_board):
        self.__position_board = position_board

    @property
    def turn(self):
        return self.__turn

    @turn.setter
    def turn(self, turn):
        self.__turn = turn

    @property
    def image(self):
        return self.__image

    @property
    def name(self):
        return self.__name

    @property
    def winner(self):
        return self.__winner

    @property
    def option(self):
        return self.__option

    @option.setter
    def option(self, option):
        self.__option = option

    @property
    def selected_question(self):
        return self.__selected_question

    @selected_question.setter
    def selected_question(self, selected_question):
        self.__selected_question = selected_question

    @property
    def selected_answer(self):
        return self.__selected_answer

    @selected_answer.setter
    def selected_answer(self, selected_answer):
        self.__selected_answer = selected_answer
