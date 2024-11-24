class Player:
    def __init__(self):
        self.__identifier = ''
        self.__name = 'Jogador'
        self.__image = ""
        self.__turn = False
        self.__position_board = 0
        self.__selected_player = -1
        self.__selected_question = -1
        self.__selected_answer = -1
        self.__time_answered = 0
        self.__winner = False

    def initialize(self, a_name, image, an_id, turn=False):
        self.reset()
        self.__name = a_name
        self.__image = image
        self.__identifier = an_id
        self.__turn = turn

    def reset(self):
        self.__identifier = ""
        self.__name = ""
        self.__turn = False
        self.__position_board = 0

    def reset_turn(self):
        self.__selected_player = -1
        self.__selected_question = -1
        self.__selected_answer = -1

    def get_player_data(self):
        return [self.__position_board, self.__turn, self.__selected_player, self.__selected_question,
                self.__selected_answer, self.__time_answered]

    @property
    def identifier(self):
        return self.__identifier

    @identifier.setter
    def identifier(self, identifier):
        self.__identifier = identifier

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

    @winner.setter
    def winner(self, winner):
        self.__winner = winner

    @property
    def selected_player(self):
        return self.__selected_player

    @selected_player.setter
    def selected_player(self, selected_player):
        self.__selected_player = selected_player

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

    @property
    def time_answered(self):
        return self.__time_answered

    @time_answered.setter
    def time_answered(self, time_answered):
        self.__time_answered = time_answered
