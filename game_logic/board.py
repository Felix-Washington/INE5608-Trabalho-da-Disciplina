# Project Imports
from player import Player


class Board:
    def __init__(self):
        # Project attributes
        super().__init__()

        # Players
        self.local_player = Player()
        self.remote_player1 = Player()
        self.remote_player2 = Player()
        self.local_player.initialize(1, "images/kid_one.png", "You")
        self.remote_player1.initialize(2, "images/kid_two.png", "Player 2")
        self.remote_player2.initialize(3, "images/kid_three.png", "Player 3")
        self.players = [self.local_player, self.remote_player1, self.remote_player2]

        # Board attributes
        self.tile_amount = 10
        self.positions = []
        self.__winner = None
        self.__match_status = False
        self.__selected_player = -1
        self.__turn_control = -1
        self.__opponent_answered = False

    def draw_card(self):
        pass

    def start_match(self):
        pass

    def reset_game(self):
        pass

    def get_status(self):
        pass

    def get_player_turn(self):
        pass

    def get_winner(self):
        pass

    def walk_in_board(self, value):
        for i in self.positions:
            print(i.occupants)

        # self.players[0].image.grid( row=0, column=i )

