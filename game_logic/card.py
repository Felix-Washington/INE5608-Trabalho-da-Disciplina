import tkinter as tk


class Card(tk.Frame):
    def __init__(self, parent, questions, answers):
        super().__init__( parent )
        self.__questions = questions
        self.__answers = answers
        self.width = 100

    @property
    def questions(self):
        return self.__questions
    
    @property
    def answers(self):
        return self.__answers

