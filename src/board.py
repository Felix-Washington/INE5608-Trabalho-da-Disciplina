# Project Imports
import random

from player import Player
from position import Position
import os

from deck import Deck


class Board:
    def __init__(self):
        super().__init__()

        # Object from local Player.
        self.__local_player = Player()
        # List of objects "Player".
        self.__players = []
        # Deck that manage cards.
        self.__deck = Deck()

        # Board attributes
        self.__tile_amount = 30
        # A list of objects "Position".
        self.__positions = []
        # 0 - Start game / 1 - Waiting player move / 2 - End play / 3 - Temporary play / 4 - End temporary play
        self.__game_status = 0
        # ID from player on current turn.
        self.__current_player_turn = -1
        # Position that the current player is on.
        self.__current_position_board = -1

    def start_match(self, players, local_id):
        # 0 - Name , 1 - ID , 2 - Connection order.
        for player in players:
            new_player_name = player[0]
            new_player_id = player[1]
            new_player_image = f"images/kid_{player[2]}.png"

            if new_player_id == local_id:
                self.__local_player.initialize( new_player_name, new_player_image, new_player_id )

            new_player = Player()
            new_player.initialize( new_player_name, new_player_image, new_player_id )

            self.__players.append( new_player )

        random.shuffle( self.__players )

        # Set player turn.
        self.__players[0].turn = True
        self.__current_player_turn = self.__players[0].identifier

        # Create board positions.
        self.set_positions_types()

    # Get all data from first receive move and create all objects based on information received.
    def start_game(self, start_config):
        # Creates players in the same order they were initially created.
        for player_id, player_data in start_config["players"].items():
            new_player = Player()

            # Set local player.
            if player_id == self.__local_player:
                self.__local_player = new_player
                self.__local_player.initialize( player_data[0], player_data[1], player_id, player_data[2] )

            new_player.initialize( player_data[0], player_data[1], player_id, player_data[2] )
            self.__players.append( new_player )

            # Set player of the current turn.
            if new_player.turn:
                self.__current_player_turn = new_player.identifier

        # Call a function to create board positions.
        self.set_positions( start_config["positions"] )
        self.__game_status = 1

    # Create a list of type positions.
    def set_positions_types(self):
        position_type_list = []
        for i in range( self.__tile_amount + 2 ):
            new_type = int( random.uniform( 1, 4 ) )
            position_type_list.append( new_type )

        position_type_list[0] = 2
        position_type_list[self.__tile_amount + 1] = 0
        # Call a function to create position objects.
        self.set_positions( position_type_list )

    # Create position objects with position types.
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

    def get_move_to_send(self):
        players = {}
        card_question = -1
        for player in self.__players:
            players[player.identifier] = player.get_player_data()
            if player.selected_question != -1:
                card_question = player.selected_question

        move_to_send = {"players": players, "current_player": self.__current_player_turn,
                        "game_status": self.__game_status,
                        "card_question": card_question, "card_answers": self.__deck.card_current_answers,
                        "position_type": self.__current_position_board, "match_status": "next"}

        return move_to_send

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

    # Update all data received from receive move made from another player.
    def update_received_data(self, move):
        for player in self.__players:
            for key, data in move["players"].items():
                if player.identifier == key:
                    player.position_board = data[0]
                    player.turn = data[1]
                    player.selected_player = data[2]
                    player.selected_question = data[3]
                    player.selected_answer = data[4]

                if data[2] == self.local_player.identifier:
                    self.__local_player.selected_question = data[3]
                    self.__local_player.turn = True

                # Update local player.
                if player.identifier == self.__local_player.identifier:
                    self.__local_player = player

        # Convert all keys from string to int.
        move["card_answers"] = {int( key ): value for key, value in move["card_answers"].items()}

        self.__deck.card_current_answers = move["card_answers"]

        if move["game_status"] == 3:
            self.__deck.create_card_options( "create_answers", move["card_question"])
            self.__current_position_board = move["position_type"]

        self.__current_player_turn = move["current_player"]

    def get_current_player_data(self, data_type):
        for player in self.__players:
            if player.identifier == self.__current_player_turn:
                if data_type == "name":
                    return player.name
                elif data_type == "position_board":
                    return player.position_board

    def get_card_information(self, text_type, data_id):
        if text_type == "create_players":
            for player in self.__players:
                if player.identifier == data_id:
                    return player.name
        else:
            return self.__deck.get_card_option_text( text_type, self.__current_position_board, data_id )

    # Get all neccessary data to start a match.
    def get_start_match_data(self):
        position_types = []
        for position in self.__positions:
            position_types.append( position.type )

        players_ids = {}
        for player in self.__players:
            players_ids[player.identifier] = [player.name, player.image, player.turn]

        move_to_send = {"positions": position_types, "players": players_ids, "game_status": 0, "match_status": "next"}
        return move_to_send

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
