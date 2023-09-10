
import tkinter as tk


class deck(tk.Button):
    def __init__(self, master, card_amount, command):
        super().__init__()
        self.__card_amount = card_amount
        self.__master = master
        self.__text = "Deck"
        self.__width = 30
        self.__height = 10
        self.__command = command