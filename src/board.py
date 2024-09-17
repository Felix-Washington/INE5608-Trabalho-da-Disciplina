# Project Imports
from player import Player
# from deck import Deck


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
        self.tile_amount = 25
        self.positions = []
        self.__winner = None
        self.__match_status = False
        self.__selected_player = -1
        self.__turn_control = -1
        self.__opponent_answered = False

    #     self.deck = Deck(self)

    # def draw_card(self):
    #     carta = self.deck.draw_card()
    #     if carta:
    #         return carta

    # def create_answers(self, a):
    #     return self.deck.create_answers(a)
        

    def start_match(self, players, local_id):
        playerA_name = players[0][0]
        playerA_id = players[0][1]
        playerA_order = players[0][2]
        playerB_name = players[1][0]
        playerB_id = players[1][1]
        playerC_name = players[2][0]
        playerC_id = players[2][1]
        self.local_player.reset()
        self.remote_player.reset()
        self.local_player.initialize(1, playerA_id, playerA_name)
        self.remote_player1.initialize(2, playerB_id, playerB_name)
        self.remote_player2.initialize(3, playerC_id, playerC_name)
        if playerA_order == "1":
            self.local_player.toogle_turn()
            self.match_status = 3  #    waiting piece or origin selection (first action)
        else:
            self.remote_player.toogle_turn()
            self.match_status = 5  #    waiting remote action



    def reset_game(self):
        pass

    def get_status(self):
        pass

    def get_player_turn(self):
        pass

    def get_winner(self):
        if self.__winner:
            return self.__winner

    def walk_in_board(self, value):
        for i in self.positions:
            print(i.occupants)

        # self.players[0].image.grid( row=0, column=i )


    def get_match_status(self):
        self.__match_status 
