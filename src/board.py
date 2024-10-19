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
        self.__players = []

        # Board attributes
        self.__tile_amount = 30
        self.__positions = []
        self.__winner = None
        self.__game_status = 0  # 0 - Start game / 1 - Waiting player move / 2 - End play / 3 - Temporary play / 4 - End temporary play
        self.__current_player_turn = -1
        # Position that the current player is on.
        self.__current_position_board = -1

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
        player1 = Player()
        player1.initialize( player_b_name, player_b_image, player_b_id )
        # player2.initialize( player_c_name, player_c_image, player_c_id )

        self.__players = [self.__local_player, player1]
        random.shuffle( self.__players )

        # Set player turn.
        self.__players[0].turn = True
        self.__current_player_turn = self.__players[0].identifier

        # if self.__current_player_turn.identifier == self.__local_player.identifier:
        #    self.__local_player = self.__current_player_turn

        # Create board positions.
        self.set_positions_types()

    def start_game(self, start_config):
        # Aux used because self.__player initially has data.
        players_order = []
        count_image = 0

        # Creates players in the same order they were initially created.
        for player_order_id in start_config["players"]:
            # Initially self.__players is a list with name, id and order data.
            for player in self.__players:
                # [0] get name from player / [1] get id from player.
                if player[1] == player_order_id:
                    player_name = player[0]
                    player_id = player[1]
                    player_image = f"images/kid_{count_image}.png"

                    count_image += 1

                    # Create local player by id.
                    if player_order_id == self.__local_player:
                        self.__local_player = Player()
                        self.__local_player.initialize( player_name, player_image, player_id )
                        players_order.append( self.__local_player )
                    else:
                        new_player = Player()
                        new_player.initialize( player_name, player_image, player_id )
                        players_order.append( new_player )

        self.__current_player_turn = start_config["current_player"]
        # Setting players objects.
        self.__players = players_order
        # Call a function to create board positions.
        self.__game_status = 1
        self.set_positions( start_config["positions"] )

    def set_positions_types(self):
        position_type_list = []
        for i in range( self.__tile_amount + 2 ):
            new_type = int( random.uniform( 1, 4 ) )
            position_type_list.append( new_type )

        position_type_list[0] = 1
        position_type_list[self.__tile_amount + 1] = 0
        self.set_positions( position_type_list )

    # Create position objects.
    def set_positions(self, position_type_list):
        position_types = {
            0: "fim.png",
            1: "simples.png",
            2: "multipla.png",
            3: "desafio.png",
        }

        for new_type in position_type_list:
            image_path = os.path.join( os.path.dirname( __file__ ), "./images/" + position_types[new_type] )
            new_position = Position( new_type, None, image_path )
            self.__positions.append( new_position )

    # Get all neccessary data to start a match.
    def get_start_match_data(self):
        position_types = []
        for position in self.__positions:
            position_types.append( position.type )

        players = []
        for player in self.__players:
            players.append( player.identifier )

        current_player = self.__current_player_turn
        status = self.__game_status
        return position_types, players, current_player, status

    def get_updated_data(self):
        players = []
        for player in self.__players:
            players.append( {player.identifier: player.get_player_data()} )

        return players, self.__current_player_turn, self.__game_status, self.__deck.card.question, \
               self.__deck.card.options, self.__current_position_board

    def check_board_status(self, id_question):
        pass

    # Process all moves made from players.
    def process_board_status(self):
        # 1 - Correct / -1 - Wrong
        result = self.__deck.check_answer( self.__local_player.selected_answer )

        # [Walk value * result] determine if a player will forward or backward in the board.
        walk_value = 1 * result

        # Check if position is "simples" and player got a correct answer.
        if self.__current_position_board == 1 and result == 1:
            walk_value = 2

        # Update position of players.
        for player in self.__players:
            if player.turn:
                # Check if player is on the first board tile and get a wrong answer.
                if player.position_board == 0 and result - 1:
                    walk_value = 0

                if self.__current_position_board != 3:
                    player.position_board += walk_value
                else:
                    if player.selected_player == -1:
                        player.position_board += walk_value
                    else:
                        player.position_board += walk_value * -1

                # Check if player is on the last board tile.
                if player.position_board > self.__tile_amount:
                    player.position_board = 30

    def receive_withdrawal_notification(self):
        self.__game_status = 6  # match abandoned by opponent

    # Update to next player on turn list.
    def update_turn(self):
        for i in range( len( self.__players ) ):
            if self.players[i].identifier == self.__current_player_turn:
                next_index = i + 1
                if next_index > len( self.__players ) - 1:
                    next_index = 0
                self.__players[next_index].turn = True
                self.__current_player_turn = self.__players[next_index].identifier
                break

        # Reset all players.
        for player in self.__players:
            if player.identifier != self.__current_player_turn:
                player.turn = False
            player.reset_turn()

        self.__current_position_board = -1

    def update_board_position(self):
        self.__current_position_board = self.__positions[self.get_current_player_data( "position_board" )].type

    def update_board_data(self, move):
        for player in self.__players:
            for key, data in move["players"][0].items():
                if player.identifier == key:
                    player.position_board = data[0]
                    player.turn = data[1]
                    player.selected_player = data[2]
                    player.selected_question = data[3]
                    player.selected_answer = data[4]

                if data[2] == self.local_player.identifier:
                    self.__local_player.turn = True

        if move["game_status"] == 3:
            self.__deck.card.question = move["card_question"]
            self.__deck.card.options = move["card_answers"]
            self.__current_position_board = move["position_type"]

        self.__current_player_turn = move["current_player"]

    def get_current_player_data(self, data_type):
        for player in self.__players:
            if player.identifier == self.__current_player_turn:
                if data_type == "name":
                    return player.name
                elif data_type == "position_board":
                    return player.position_board

    def reset_game(self):
        pass

    @property
    def deck(self):
        return self.__deck

    @deck.setter
    def deck(self, deck):
        self.__deck = deck

    @property
    def game_status(self):
        return self.__game_status

    @game_status.setter
    def game_status(self, game_status):
        self.__game_status = game_status

    @property
    def current_player_turn(self):
        return self.__current_player_turn

    @property
    def players(self):
        return self.__players

    @players.setter
    def players(self, players):
        self.__players = players

    @property
    def local_player(self):
        return self.__local_player

    @local_player.setter
    def local_player(self, local_player):
        self.__local_player = local_player

    @property
    def positions(self):
        return self.__positions

    @property
    def current_position_board(self):
        return self.__current_position_board
