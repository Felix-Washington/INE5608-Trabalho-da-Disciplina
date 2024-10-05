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
        self.__local_player = Player()
        self.remote_player1, self.remote_player2 = Player(), Player()
        self.remote_player2.initialize( 2, "images/kid_2.png", "Player 2" )
        self.__players = [self.__local_player, self.remote_player1, self.remote_player2]

        # Board attributes
        self.__tile_amount = 30
        self.__positions = []
        self.__winner = None
        self.__match_status = 0
        self.__selected_player = -1
        self.__current_player_turn = -1
        # Position that the current player is on.
        self.__current_position_board = -1
        self.__temporary_turn = False
        self.__match_status = 0
        self.__turn_order = [0, 1, 2]

        self.__deck = Deck()

    def start_match(self, players, local_id):
        # Shuffle players turn order.
        random.shuffle( self.__turn_order )

        # Load configs from player 1.
        player_a_name = players[0][0]
        player_a_id = players[0][1]
        player_a_image = f"images/kid_{self.__turn_order[0]}.png"

        # Load configs from player 2.
        player_b_name = players[1][0]
        player_b_id = players[1][1]
        player_b_image = f"images/kid_{self.__turn_order[1]}.png"

        # Load configs from player 3.
        # player_c_name = players[2][0]
        # player_c_id = players[2][1]
        # player_c_image = f"images/kid_{self.__turn_order[2]}.png"

        self.__local_player.initialize( player_a_name, player_a_image, player_a_id )
        self.remote_player1.initialize( player_b_name, player_b_image, player_b_id )
        # self.remote_player2.initialize( player_c_name, player_c_image, player_c_id )

        # Set player turn.
        self.__current_player_turn = self.__turn_order[0]

        # Set game state to GAME_RUNNING.
        self.__match_status = 2
        # Create board positions.
        self.set_positions()

    def set_positions(self):
        position_types = {
            0: "fim.png",
            1: "simples.png",
            2: "multipla.png",
            3: "desafio.png",
        }

        for i in range( self.__tile_amount + 2 ):
            # If reached last position, set the final position of the board.
            if i != 0 and i <= self.__tile_amount:
                number = int( random.uniform( 1, 4 ) )
            elif i == 0:
                number = 1
            else:
                number = 0

            image_path = os.path.join( os.path.dirname( __file__ ), "./images/" + position_types[number] )

            # Create positions with widget None. It will be set in player_interface.
            self.__positions.append( Position( number, None, image_path ) )
        # Insert players to the first position.
        for player in self.__players:
            self.__positions[0].occupants.append( player )

    def process_board_status(self, id_question, answer, controller):
        result = self.__deck.check_answer( id_question, answer )
        player_id = self.__players[0].identifier
        changed = False
        self.get_board_position()

        current_position_type = self.__positions[self.__current_position_board].type

        # Walk value * result determine if player will forward or backward in the board.
        walk_value = 1 * result

        # Check if position is "simples" and player got a correct answer.
        if current_position_type == 1 and result:
            walk_value = 2
        elif current_position_type == 3:
            # It needs to reverte value again because the current player will be checked first.
            walk_value * result

        # Update positions values from all players.
        for position in range( len( self.__positions ) ):
            for player in range( len( self.__positions[position].occupants ) ):
                if player_id == self.__positions[position].occupants[player].identifier:
                    new_position = position + walk_value
                    del (self.__positions[position].occupants[player])
                    self.__positions[new_position].occupants.append( self.__players[player] )
                    changed = True

                    # Needs to be finished
                    if self.__temporary_turn:
                        changed = False
                        if current_position_type == 3:
                            new_position = position + walk_value * result
                            del (self.__positions[position].occupants[self.__selected_player])
                break

            if changed:
                break
        controller.update_widget_packs()

    def get_board_position(self):
        # Just for testing
        self.__current_player_turn = 0

        for i in range( len( self.__positions ) ):
            if self.__players[self.__current_player_turn] in self.__positions[i].occupants:
                self.__current_position_board = i

    def reset_game(self):
        pass

    @property
    def deck(self):
        return self.__deck

    @deck.setter
    def deck(self, deck):
        self.__deck = deck

    def get_status(self):
        print( "test statyus" )

    @property
    def match_status(self):
        return self.__match_status

    @property
    def current_player_turn(self):
        return self.__current_player_turn

    @property
    def players(self):
        return self.__players

    @property
    def positions(self):
        return self.__positions
