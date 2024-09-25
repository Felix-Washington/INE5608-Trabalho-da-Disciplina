# Project Imports
import random

from player import Player
from position import Position
import os


from deck import Deck


class Board:
    def __init__(self):
        # Project attributes
        super().__init__()

        # Players
        self.local_player = Player()
        self.remote_player1, self.remote_player2 = Player(), Player()
        self.local_player.initialize( 1, "images/kid_0.png", "You" )
        self.remote_player1.initialize( 2, "images/kid_1.png", "Player 2" )
        self.remote_player2.initialize( 3, "images/kid_2.png", "Player 3" )
        self.players = [self.local_player, self.remote_player1, self.remote_player2]

        # Board attributes
        self.tile_amount = random.randrange(25, 30)
        self.positions = []
        self.__winner = None
        self.__match_status = False
        self.__selected_player = -1
        self.__current_turn = -1
        self.__opponent_answered = False
        self.__match_status = 0
        self.__turn_order = []

        self.__deck = None

    def start_match(self, players=0):
        '''
        player_a_name = players[0][0]
        player_a_id = players[0][1]
        playerA_order = players[0][2]
        playerB_name = players[1][0]
        playerB_id = players[1][1]
        playerC_name = players[2][0]
        playerC_id = players[2][1]
        self.local_player.reset()
        self.remote_player.reset()
        self.local_player.initialize( 1, player_a_id, player_a_name )
        self.remote_player1.initialize( 2, playerB_id, playerB_name )
        self.remote_player2.initialize( 3, playerC_id, playerC_name )
        if playerA_order == "1":
            self.local_player.toogle_turn()
            self.__match_status = 3  # waiting piece or origin selection (first action)
        else:
            self.remote_player.toogle_turn()
            self.__match_status = 5  # waiting remote action
        '''
        self.set_positions()
        self.__turn_order = []

    def reset_game(self):
        pass

    @property
    def deck(self):
        return self.__deck

    @deck.setter
    def deck(self, deck):
        self.__deck = deck

    def get_winner(self):
        if self.__winner:
            return self.__winner

    def walk_in_board(self, value):
        for i in self.positions:
            print( i.occupants )

    def get_match_status(self):
        pass

    def set_positions(self):
        position_types = {
            0: "fim.png",
            1: "simples.png",
            2: "multipla.png",
            3: "desafio.png",
        }

        for i in range( self.tile_amount + 2 ):
            # If reached last position, set the final position of the board.
            if i != 0 and i <= self.tile_amount:
                number = int( random.uniform( 1, 4 ) )
            elif i == 0:
                number = 1
            else:
                number = 0

            image_path = os.path.join( os.path.dirname( __file__ ), "./images/" + position_types[number] )

            self.positions.append( Position( number, None, image_path ) )
        self.positions[0].occupants = [0, 1]
        self.positions[1].occupants = [2]

