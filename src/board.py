# Project Imports
import os
import random
import time

from deck import Deck
from player import Player
from position import Position


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
        self.__tile_amount = 20
        # A list of objects "Position".
        self.__positions = []
        # 0 - Start game / 1 - Waiting player move / 2 - End play / 3 - Temporary play / 4 - End temporary play
        self.__game_status = 0
        # ID from player on current turn.
        self.__current_player_id = ""

        # Position that the current player is on.
        self.__current_position_type = -1

        # Time
        self.__last_position = self.__tile_amount + 1

    def start_match(self, players, local_player_id):
        # 0 - Name , 1 - ID , 2 - Connection order.

        for player in players:

            new_player_name = player[0]
            new_player_id = player[1]
            new_player_image = f"images/kid_{player[2]}.png"

            if new_player_id == local_player_id:
                self.__local_player.initialize( new_player_name, new_player_image, new_player_id )

            new_player = Player()
            new_player.initialize( new_player_name, new_player_image, new_player_id )

            if int( player[2] ) == 1:
                new_player.turn = True
                self.__current_player_id = new_player.identifier

            self.__players.append( new_player )

        self.update_current_local_player()

        # Create board positions.
        self.set_positions_types()

    def receive_start(self, local_player_id):
        self.__local_player.identifier = local_player_id

    def update_current_local_player(self):
        if self.__current_player_id == self.__local_player.identifier:
            self.__local_player.current_local_player = True
            self.__local_player.turn = True
        else:
            self.__local_player.current_local_player = False
            self.__local_player.turn = False

    # Get all data from first receive move and create all objects based on information received.
    def remote_start_match(self, start_config):
        # Creates players in the same order they were initially created.
        for player_id, player_data in start_config["players"].items():
            new_player = Player()

            # Set local player.
            if player_id == self.__local_player.identifier:
                self.__local_player = new_player
                self.__local_player.initialize( player_data[0], player_data[1], player_id, player_data[2] )

            new_player.initialize( player_data[0], player_data[1], player_id, player_data[2] )
            self.__players.append( new_player )

            # Set player of the current turn.
            if new_player.turn:
                self.__current_player_id = new_player.identifier

        self.update_current_local_player()

        # Call a function to create board positions.
        self.set_positions( start_config["positions"] )
        self.__game_status = 1

    # Create a list of type positions.
    def set_positions_types(self):
        position_type_list = []
        for i in range( self.__tile_amount + 2 ):
            new_type = int( random.uniform( 1, 4 ) )
            position_type_list.append( new_type )
            self.__last_position = i

        position_type_list[self.__tile_amount + 1] = 0

        # Call a function to create position objects.
        self.set_positions( position_type_list )

    # Create position objects with position types.
    def set_positions(self, position_type_list):

        self.__current_position_type = position_type_list[0]
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

    def check_board_status(self, state, selected_option=-1):
        if self.__current_position_type == 2:
            if state == "create_answers":
                self.__local_player.time_answered = time.time()
            elif state == "selected_an_answer":
                self.__local_player.time_answered = time.time() - self.__local_player.time_answered

        if state == "create_answers":
            self.__local_player.selected_question = selected_option
            if self.__current_position_type == 3 and self.__game_status == 1:
                state = "create_players"

        # Run when player has selected an answer.
        elif state == "selected_an_answer":
            self.__local_player.selected_answer = selected_option
            if self.__game_status == 3:
                self.__game_status = 4
            elif self.__current_position_type == 1:
                self.__game_status = 2
            elif self.__current_position_type == 2:
                state = "create_players"

        # Run when player select another player
        elif state == "selected_a_player":
            self.__local_player.selected_player = selected_option
            self.__game_status = 3

        if state == "create_players":
            selected_option = []
            for player in self.__players:
                # Get all players
                if player.identifier != self.__local_player.identifier:
                    selected_option.append( player.identifier )

        if state != "selected_a_player" and (self.__game_status == 1 or self.__game_status == 3):
            self.__deck.create_card_options( state, selected_option )
            return state

        # Check if a play has finished.
        elif self.__game_status == 2:
            self.process_board_status()
            if self.__game_status == 5:
                return "game_end"
            return "reset_play"

        return None
        # Get send move to remote players with updated data.

    def process_receive_move(self):
        if self.__game_status == 2:
            self.__deck.discard_question()
            self.__game_status = 1
        if self.__game_status == 1:
            self.update_current_local_player()
        # Check if a temporary turn has been finished
        if self.__game_status == 4 and self.__local_player.current_local_player:
            self.__game_status = 2
            return "reset_play"
        elif self.__local_player.current_local_player:
            self.__game_status = 1
            if self.__local_player.selected_player == -1:
                return "release_deck"
        # 3 - Game status: temporary turn.
        elif self.__game_status == 3:
            if self.__local_player.turn:
                return "create_answers"

        elif self.__game_status == 5:
            return "game_end"

        return None

    def get_move_to_send(self, state):
        players = {}
        card_question = -1
        for i in range( len( self.__players ) ):
            # Only update chances made in local_player
            if self.__players[i].identifier == self.__local_player.identifier:
                self.__players[i].selected_question = self.__local_player.selected_question
                self.__players[i].selected_answer = self.__local_player.selected_answer
                self.__players[i].selected_player = self.__local_player.selected_player
                self.__players[i].turn = self.__local_player.turn
                self.__players[i].winner = self.__local_player.winner

            players[self.__players[i].identifier] = self.__players[i].get_player_data()

            # It means that a player has been selected.
            # if self.__players[i].selected_question != -1:
            #     card_question = self.__players[i].selected_question
            card_question = self.__deck.card.question


        move_to_send = {"players": players, "current_player": self.__current_player_id,
                        "game_status": self.__game_status,
                        "card_question": card_question, "card_answers": self.__deck.card_current_answers,
                        "position_type": self.__current_position_type, "match_status": "next", "state": state}

        return move_to_send

    # Process all moves made from players.
    def process_board_status(self):
        for i in range( len( self.__players ) ):
            if self.__players[i].identifier == self.__local_player.identifier:
                self.__players[i] = self.__local_player

        winners = []
        for player in self.__players:
            if player.turn:
                # 1 = Correct / -1 = Wrong
                walk_value = self.__deck.check_answer( player.selected_answer )
                # Check if position is "simples" and player got a correct answer.
                if self.__current_position_type == 1 and walk_value == 1:
                    walk_value = 2

                # Reverse value if player checked had selected a player.
                elif self.__current_position_type == 3 and player.selected_player != -1:
                    walk_value *= -1

                player.position_board += walk_value

                # Check if player is on the first board tile and get a wrong answer.
                if player.position_board < 0:
                    player.position_board = 0
                # Check if player is on the last board tile.
                elif player.position_board >= self.__last_position:
                    player.position_board = self.__last_position
                    player.winner = True
                    winners.append( player )
        if len( winners ) > 0:
            self.verify_winner( winners )
            self.__game_status = 5
        else:
            self.__deck.discard_question()
            self.update_turn()
            self.__game_status = 2
            self.__current_position_type = self.__positions[self.get_current_player_data( "position_board" )].type

    def verify_winner(self, winners):
        slowest_response = 0
        slowest_player = None

        for player in winners:
            response_time = player.time_answered
            if response_time > slowest_response:
                slowest_response = response_time
                slowest_player = player

        if len( winners ) > 1:
            slowest_player.position_board -= 1
            slowest_player.winner = False
            winners.remove( slowest_player )

    def get_winners_message(self):
        for player in self.__players:
            if player.winner:
                if self.__local_player.winner:
                    return "Você venceu!"
                return f"Jogador {player.name} venceu!"

    # Update to next player on turn list.
    def update_turn(self):
        for i in range( len( self.__players ) ):
            if self.__players[i].identifier == self.__current_player_id:
                next_index = i + 1
                if next_index > len( self.__players ) - 1:
                    next_index = 0
                self.__players[next_index].turn = True
                self.__current_player_id = self.__players[next_index].identifier
                break

        # Reset all players.
        for player in self.__players:
            if player.identifier != self.__current_player_id:
                player.turn = False
            player.reset_turn()
        self.__local_player.reset_turn()
        self.update_current_local_player()

    # Update all data received from receive move made from another player.
    def update_received_data(self, received_data):
        self.__current_position_type = received_data["position_type"]
        self.__game_status = received_data["game_status"]
        self.__current_player_id = received_data["current_player"]

        for player in self.__players:
            data = received_data["players"][player.identifier]
            player.position_board = data[0]
            player.turn = data[1]
            player.selected_player = data[2]
            player.selected_question = data[3]
            player.selected_answer = data[4]
            player.time_answered = data[5]
            player.winner = data[6]

        for player in self.__players:
            if player.selected_player == self.__local_player.identifier:
                self.__local_player.selected_question = player.selected_question
                self.__local_player.turn = True

            # Update answer to be processed by current player side
            elif self.__current_position_type == 3 and self.__local_player.selected_player != -1 and player.selected_answer != -1:
                self.__local_player.selected_answer = player.selected_answer

        # Convert all keys from string to int.
        received_data["card_answers"] = {int( key ): value for key, value in received_data["card_answers"].items()}

        self.__deck.card.question = int(received_data["card_question"])
        self.__deck.card_current_answers = received_data["card_answers"]

    def get_card_information(self, text_type, data_id):
        if text_type == "create_players":
            for player in self.__players:
                if player.identifier == data_id:
                    return player.name
        else:
            return self.__deck.get_card_option_text( text_type, self.__current_position_type, data_id )

    def get_logs_message(self, state):
        message = ""
        selected_player_name = self.get_current_player_data( 'selected_player' )

        if self.__game_status == 3:
            for player in self.__players:
                if selected_player_name == player.identifier:
                    selected_player_name = player.name
                    break

        current_player_name = self.get_current_player_data( 'name' )

        if self.__game_status == 1:
            if self.__local_player.current_local_player:
                if state == "create_questions":
                    message = "Selecione uma pergunta."
                elif state == "create_answers":
                    message = "Selecione uma resposta."
                elif state == "create_players":
                    message = "Selecione um jogador."
                elif state == "selected_a_player":
                    message = f"Você selecionou o jogador {selected_player_name} para responder uma pergunta."
            else:
                if state == "create_questions":
                    message = f"Jogador {current_player_name} comprou uma carta."
                elif state == "create_answers":
                    message = f"Jogador {current_player_name} selecionou uma pergunta."
                elif state == "selected_an_answer":
                    message = f"Jogador {current_player_name} selecionou uma resposta."
        elif self.__game_status == 2:
            message = f"Jogada finalizada, novo jogador da vez: {current_player_name}."
        elif self.__game_status == 3:
            if self.__local_player.turn:
                if state == "selected_a_player":
                    message = f"Jogador {current_player_name} enviou uma pergunta para você."
                elif state == "create_answers":
                    message = f"Você respondeu a pergunta enviada pelo jogador {current_player_name}."
            else:
                if state == "selected_a_player":
                    message = f"Jogador {current_player_name} selecionou o jogador {selected_player_name} para responder."
                elif state == "create_answers":
                    message = f"Jogador {selected_player_name } respondeu a pergunta enviada pelo jogador {current_player_name}."
        elif self.__game_status == 5:
            message = self.get_winners_message()
        elif self.__game_status == 6:
            message = "Jogador desconectado."

        return message

    # Get all neccessary data to start a match.
    def get_start_match_data(self):
        position_types = []
        for position in self.__positions:
            position_types.append( position.type )

        players_ids = {}
        for player in self.__players:
            players_ids[player.identifier] = [player.name, player.image, player.turn]

        move_to_send = {"positions": position_types, "players": players_ids, "game_status": 0, "match_status": "next",
                        "state": ""}

        return move_to_send

    def get_current_player_data(self, data_attribute):
        for player in self.__players:
            if player.identifier == self.__current_player_id:
                if data_attribute == "name":
                    return player.name
                elif data_attribute == "selected_player":
                    return player.selected_player
                elif data_attribute == "selected_answer":
                    return player.selected_answer
                elif data_attribute == "selected_question":
                    return player.selected_question
                elif data_attribute == "position_board":
                    return player.position_board
                elif data_attribute == "image":
                    return player.image

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
    def current_player(self):
        return self.__current_player

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
    def current_position_type(self):
        return self.__current_position_type
