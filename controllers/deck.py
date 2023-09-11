
import tkinter as tk

from controllers.card import card


class deck:
    def __init__(self, card_amount ):
        super().__init__()
        self.__card_amount = card_amount
        self.__questions = {}
        self.__used_questions = []
        self.__answers = {}
        self.__card = card
