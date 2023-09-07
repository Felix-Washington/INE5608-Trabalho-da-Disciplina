
import tkinter as tk


class deck(tk.Button):
    def __init__(self, master):
        super().__init__()
        self.__card_amount = 10
        self.__master = master