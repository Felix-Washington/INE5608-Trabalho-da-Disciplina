from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

import random
import os

from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor

from PIL import Image, ImageTk
from deck import Deck
from board import Board
from position import Position

class PlayerInterface(DogPlayerInterface):
    def __init__(self):
        self.board = Board()
        # Root config
        self.__root = Tk()
        self.load_main_window()

        # game_state = self.board.get_status()
        # self.update_gui(game_state)

        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        print(player_name)


    def load_main_window(self):
        self.__root.geometry("800x800")
        self.__root.title("Board")
        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.__root.resizable(False, False)

                # Board Frames
        self.__board_frame = Frame(self.__root, bg="blue", padx=30, pady=15, relief="sunken", borderwidth=2)
        # self.__nav_bar = .Frame( self.__board_frame, bg="green", height=150, width=150)
        self.__board_positions = Frame(self.__board_frame, bg="pink", height=350, width=150, relief="sunken")
        self.__hud = Frame(self.__board_frame, bg="red", height=150, width=150)

        # Frames - board_positions
        self.__board_positions2 = Frame(self.__board_positions, bg="yellow", height=350, width=150, relief="sunken")
        # Frames - hud
        self.__hud_player_img = Label(self.__hud, bg="pink", height=10, width=10)

        # Row and Column configs - Para: frame, amount (columns or rows), weight
        self.column_frame_configure(self.__board_frame, 1, [1])
        self.row_frame_configure(self.__board_frame, 3, [1, 2, 1])
        self.column_frame_configure(self.__board_positions, 2, [1,5])
        self.column_frame_configure(self.__hud, 2, [1, 2])

        self.__deck = Deck(self.__board_positions, self)

        self.__board_frame.pack_propagate(False)
        # self.__nav_bar.grid_propagate( False )
        self.__board_positions.grid_propagate( False )
        self.__hud.grid_propagate( False )

        self.set_menu()
        self.set_positions()
        self.widget_packs()

    def show_card(self, card, button):

        def end_carta(button):
            button['state'] = 'normal'
            self.tela_carta.destroy()

        print(card.questions)
        self.tela_carta = Toplevel()
        self.tela_carta.geometry('400x300+0+0')
        self.tela_carta.resizable(width=False, height=False)
        self.titulo = Label(self.tela_carta, padx=10, pady=10, text='Carta')
        self.titulo.pack(padx=10, pady=10)
        self.card = Frame(self.tela_carta, height=200, width=300, bg='blue')
        self.card.pack(padx=10, pady=10)
        for question in card.questions:
            self.question = Button(self.card, text=question, command=lambda question=question: print(f'Pergunta {question} clicada'), width=100)
            self.question.pack(padx=10, pady=10)
        self.tela_carta.focus()
        self.tela_carta.grab_set()
        self.tela_carta.protocol("WM_DELETE_WINDOW", lambda: end_carta(button))


    def board_loop(self):
        self.__root.mainloop()

    def row_frame_configure(self, frame, row_amount, weight):
        for i in range(row_amount):
            frame.rowconfigure(i, weight=weight[i])

    def column_frame_configure(self, frame: Frame, column_amount: int, weight):
        for i in range(column_amount):
            frame.columnconfigure(i, weight=weight[i])

    # Create all board positions
    def set_positions(self):
        position_types = {
            0: "fim.png",
            1: "simples.png",
            2: "multipla.png",
            3: "desafio.png"
        }
        tile_amount = 10
        for i in range(tile_amount + 2):
            # If reached last position, set the final position of the board.
            if i != 0 and i <= tile_amount:
                number = int( random.uniform( 1, 4 ) )
            elif i == 0:
                number = 0
            else:
                number = 0

            image_path = os.path.join(os.path.dirname(__file__), "./images/" + position_types[number])
            position = self.load_label_img(self.__board_positions2, image_path)
            # Bind and specify event for each position.
            position.bind( "<Button-1>", lambda event="", position_number=i: self.position_bind(event, position_number))
            self.board.positions.append(Position(number, position))

    def load_label_img(self, widget, path):
        image = Image.open(path)
        photo = ImageTk.PhotoImage( image )
        label = Label( widget, image=photo )
        label.image = photo
        return label

    def position_bind(self, event, a):
        print(self.board.positions[a].widget.image , "teste")

    def show_message(self):
        if self.__check_state.get() == 0:
            print("Deck")
        # else:
        #     print(self.__textbox.get("1.0", END))

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="Quer Sair?"):
            self.__root.destroy()

    def shortcut(self, event):
        if event.state == 12 and event.keysym == "Return":
            self.show_message()

    def set_menu(self):
        self.__menubar = Menu(self.__root)
        self.__filemenu = Menu(self.__menubar, tearoff=0)
        self.__filemenu.add_command(label="Procurar jogador")
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Close", command=self.on_closing)

        self.__menubar.add_cascade(menu=self.__filemenu, label="File")

        self.__root.config(menu=self.__menubar)

    def widget_packs(self):
        self.__board_frame.pack(fill="both", expand=True)
        # self.__nav_bar.grid(row=0, sticky="ew")
        self.__board_positions.grid(row=1, sticky="ew")
        self.__hud.grid(row=2, sticky="ew")

        self.__board_positions2.grid(column=0, sticky="ew")
        self.__deck.grid( row=0, column=1, sticky="NS" )

        self.__hud_player_img.grid(column=0, sticky="NS" )

        # self.__textbox.grid(column=1, padx=10)

        row = 0
        column = 0
        for i in range(len(self.board.positions)):
            self.board.positions[i].widget.grid(column=column, row=row, pady=5, padx=5)
            if column > 3:
                row += 1
                column = 0
            else:
                column += 1
            print(row, column)

        for player in self.board.players:
            image_path = os.path.join(os.path.dirname(__file__), player.image)
            player_image = self.load_label_img(self.__hud_player_img, image_path)
            player_image.grid(row=0, column=i)

    #INFOS GRÁFICAS DO JOGO -> COPIAR DO BOARD E SEPARAR COMO VIEW / CONTROLLER