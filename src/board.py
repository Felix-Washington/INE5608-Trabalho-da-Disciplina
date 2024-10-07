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
        self.__players = []

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

        self.__deck = Deck()

    def start_match(self, players, local_id):
        # Load configs from player 1.
        player_a_name = players[0][0]
        player_a_id = players[0][1]
        player_a_image = f"images/kid_{0}.png"

        # Load configs from player 2.
        player_b_name = players[1][0]
        player_b_id = players[1][1]
        player_b_image = f"images/kid_{1}.png"

        # Load configs from player 3.
        # player_c_name = players[2][0]
        # player_c_id = players[2][1]
        # player_c_image = f"images/kid_{2}.png"

        self.__local_player.initialize( player_a_name, player_a_image, player_a_id )
        self.remote_player1.initialize( player_b_name, player_b_image, player_b_id )
        # self.remote_player2.initialize( player_c_name, player_c_image, player_c_id )

        self.__players = [self.__local_player, self.remote_player1]
        random.shuffle( self.__players )
        # Set player turn.
        self.__players[0].turn = True
        self.__current_player_turn = self.__players[0]

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

    def process_board_status(self, id_question, answer, controller):
        # 1 - Correct / -1 - Wrong
        result = self.__deck.check_answer( id_question, answer )
        # Get position type from who asks.
        self.__current_position_board = self.__positions[self.__current_player_turn.position_board].type

        # [Walk value * result] determine if a player will forward or backward in the board.
        walk_value = 1 * result

        # Check if position is "simples" and player got a correct answer.
        if self.__current_position_board == 1 and result == 1:
            walk_value = 2
        elif self.__current_position_board == 3:
            # It needs to revert the value because the current player will be checked first.
            walk_value * result

        # Update position of players.
        for player in self.__players:
            if self.__current_player_turn == player:
                # Check if player is on the first board tile and get a wrong answer.
                if player.position_board == 0 and result - 1:
                    walk_value = 0
                player.position_board += walk_value

                # Check if player is on the last board tile.
                if player.position_board > self.__tile_amount:
                    player.position_board = 30
                self.__current_player_turn = player
                break

        # Update position for selected player.
        if self.__temporary_turn:
            for player in self.__players:
                if self.__selected_player == player:
                    if self.__current_position_board == 3:
                        # Inverts result to get the original value.
                        walk_value *= result
                    # Set result to selected player.
                    player.position_board += walk_value

        controller.update_widget_packs()

    def receive_withdrawal_notification(self):
        self.__match_status = 6  # match abandoned by opponent

    # Update to next player on turn list.
    def update_turn(self):
        for i in range( len( self.__players ) ):
            if self.__players[i].turn:
                self.__players[i].turn = False
                next_index = (i + 1) % len( self.__players )
                self.__players[next_index].turn = True
                self.__current_player_turn = self.__players[next_index]
                break

    def reset_game(self):
        pass

    @property
    def deck(self):
        return self.__deck

    @deck.setter
    def deck(self, deck):
        self.__deck = deck

    def get_status(self):
        pass

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

    @property
    def current_position_board(self):
        return self.__current_position_board
