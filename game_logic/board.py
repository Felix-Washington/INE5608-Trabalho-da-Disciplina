# Tkinter Imports
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
import os

from deck import Deck

# Project Imports
from player import Player
from position import Position

# Misc imports
import random


class Board:
    def __init__(self):
        # Project attributes
        super().__init__()

        #Players
        self.local_player = Player()
        self.remote_player1 = Player()
        self.remote_player2 = Player()
        self.local_player.initialize(1, "images/kid_one.png", "You")
        self.remote_player1.initialize(2, "images/kid_two.png", "Player 2")
        self.remote_player2.initialize(3, "images/kid_three.png", "Player 3")
        self.players = [self.local_player, self.remote_player1, self.remote_player2]

        #Board attributes
        self.tile_amount = 10
        self.positions = []
        self.__winner = None
        self.__match_status = False
        self.__selected_player = -1
        self.__turn_control = -1
        self.__opponent_answered = False


    # Create all board positions
    def set_positions(self):
        position_types = {
            0: "fim.png",
            1: "simples.png",
            2: "multipla.png",
            3: "desafio.png"
        }

        for i in range(self.__tile_amount + 2):
            # If reached last position, set the final position of the board.
            if i != 0 and i <= self.__tile_amount:
                number = int( random.uniform( 1, 4 ) )
            elif i == 0:
                number = 0
            else:
                number = 0

            image_path = os.path.join(os.path.dirname(__file__), "./images/" + position_types[number])
            position = self.load_label_img(self.__board_positions2, image_path)
            # Bind and specify event for each position.
            position.bind( "<Button-1>", lambda event="", position_number=i: self.position_bind(event, position_number))
            self.__positions.append(Position(number, position))


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
