import tkinter as tk
import random
from controllers.card import Card


class Deck( tk.Frame ):
    def __init__(self, parent, controller, card_amont=10):
        tk.Frame.__init__( self, parent )

        self.__card_amount = card_amont
        self.__questions = ['Teste', 'Teste1', 'Teste2', 'Teste3', 'Teste4', 'Teste5', 'Teste6', 'Teste7', 'Teste8']
        self.__answers = ['Answer', 'Answer1', 'Answer2', 'Answer3', 'Answer4', 'Answer5', 'Answer6', 'Answer7', 'Answer8']
        self.__card = None

        self.columnconfigure( 0, weight=1 )
        self.pack(pady=20)

        self.__button = tk.Button( self, text="Deck", command=lambda: self.create_card(controller), state="normal")
        self.__button.grid(row=0, column=0)

    def create_card(self, controller):
        questions_card = []
        answers_card = []
        added = False
        control = 0

        if len(self.__questions) < 4:
            control = 4
        while control < 4:
            number = int( random.uniform( 0, len(self.__questions) ) )
            for i in range(len(self.__questions)):
                if i == number:
                    questions_card.append(self.__questions[i])
                    answers_card.append(self.__answers[i])
                    added = True
                    break
            if added:
                self.__questions.pop(number)
                self.__answers.pop(number)
                added = False
                control += 1
        print(questions_card)
        self.__card = Card(self, questions_card, answers_card)
        self.__button['state'] = 'disabled'

        controller.show_card(self.__card)


    def button(self):
        return self.__button
