import tkinter as tk


class card(tk.Frame):
    def __init__(self, parent, questions, answers):
        super().__init__( parent )
        self.__questions = questions
        self.__answers = answers
        self.__answered = False
        self.width = 100

