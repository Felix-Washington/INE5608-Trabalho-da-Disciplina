import tkinter as tk


class Card(tk.Frame):
    def __init__(self, parent, questions, answers):
        super().__init__( parent )
        self.__questions = questions
        self.__answers = answers
        self.__answered = False
        self.width = 100

    @property
    def questions(self):
        return self.__questions
    
    @property
    def answers(self):
        return self.__answers

    @property
    def answered(self):
        return self.__answered


    @answered.setter
    def answered(self, new_status):
        self.__answered = new_status
