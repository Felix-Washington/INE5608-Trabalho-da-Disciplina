from random import Random

from controladores.deck import deck

import tkinter as tk
from tkinter import messagebox


class board:
    def __init__(self, player_amount, deck_cards):
        self.__player_amount = player_amount
        self.__tile_amount = 10
        '''
        0 - Pergunta
        Simples
        1 - Pergunta
        Múltipla
        2 - Desafio
        3 - Final
        '''
        self.__tiles = {}
        self.__deck = deck_cards

        # Root config
        font = ('Arial', 18)
        self.__root = tk.Tk()
        self.__root.geometry("800x600")
        self.__root.title("Board")
        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Vars

        self.__board_frame = tk.Frame(self.__root, bg="blue", padx=30, pady=15, relief="sunken",borderwidth=2)

        self.__board_frame.columnconfigure(0, weight=1)
        self.__board_frame.rowconfigure(0, weight=1)
        self.__board_frame.rowconfigure(1, weight=10)
        self.__board_frame.rowconfigure(2, weight=1)

        self.__board_frame.pack_propagate (False)

        self.__nav_bar = tk.Frame( self.__board_frame, bg="green", height=150, width=150)
        self.__board_positions = tk.Frame(self.__board_frame, bg="yellow", height=250, width=150,relief="sunken",borderwidth=2)
        self.__hud = tk.Frame(self.__board_frame, bg="red", height=150, width=150)

        self.__nav_bar.grid_propagate(False)
        self.__board_positions.grid_propagate(False)
        self.__hud.grid_propagate(False)

        self.__board_positions.columnconfigure(0, weight=2)
        self.__board_positions.columnconfigure(1, weight=1)

        self.__check_state = tk.IntVar()
        self.__textbox = tk.Text(self.__nav_bar, height=2, width=50, font=font )

        # Menu vars
        '''
        self.__menubar = tk.Menu(self.__root)
        self.__filemenu = tk.Menu(self.__menubar, tearoff=0)
        self.__filemenu.add_command(label="Close", command=self.on_closing)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Close wt question", command=exit)

        self.__menubar.add_cascade(menu=self.__filemenu, label="File")

        self.__root.config(menu=self.__menubar)
        '''



    def start(self):
        font = ('Arial', 18)

        #self.__textbox.bind("<KeyPress>", self.shortcut)
        '''
        btn1 = tk.Button(self.__board_frame, text="1", font=font )
        btn1.grid(row=0, column=0, sticky=tk.W+tk.E)

        btn2 = tk.Button( self.__board_frame, text="positions", font=font )
        btn2.grid( row=1, column=1, sticky=tk.W + tk.E )

        btn3 = tk.Button( self.__board_frame, text="deck", font=font )
        btn3.grid( row=2, column=2, sticky=tk.W + tk.E )
        '''

        self.__textbox.grid(padx=10)

        self.__board_frame.pack(fill="both", expand=True)
        self.__nav_bar.grid(row=0, column=0, sticky="ew")
        self.__board_positions.grid(row=1, column=0, sticky="ew")
        self.__hud.grid(row=2, column=0, sticky="ew")


        check = tk.Checkbutton(self.__hud, text="Show Message", font=font, variable=self.__check_state)
        check.grid(pady=10)

        button = tk.Button(self.__board_positions, text="Deck", font=font, command=self.show_message)
        button.grid(column=1, sticky="NS")
        self.__root.mainloop()

    def show_message(self):
        if self.__check_state.get() == 0:

            print(self.__textbox. get("1.0", tk.END))
        else:
            messagebox.showinfo(title="Message", message=self.__textbox.get("1.0", tk.END))

    def on_closing(self):
        self.__root.destroy()
        #if messagebox.askyesno(title="Quit", message="Wanna Quit?"):
        #    self.__root.destroy()

    def shortcut(self, event):
        if event.state == 12 and event.keysym == "Return":
            self.show_message()


    def create_tiles(self):
        for i in range( self.__tile_amount ):
            if i == self.__tile_amount:
                # Add last tile
                self.__tiles[i] = 3
                pass
            else:
                self.__tiles[i] = Random(3)

    def check_winner(self, player_position, player_id):
        if player_position >= self.__tile_amount:
            return player_id

    def check_tile(self, tile_type):
        if tile_type == 0:
            # simple_question
            pass
        elif tile_type == 1:
            pass
        elif tile_type == 2:
            pass
        elif tile_type == 3:
            pass

