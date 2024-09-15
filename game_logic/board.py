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
        self.__tile_amount = 10
        self.__positions = []
        self.__players = []

        # Root config
        self.__root = tk.Tk()

        # Window size and position
        size = [int( self.__root.winfo_screenwidth() / 3 ), 800]
        self.__window_width = int( self.__root.winfo_screenwidth() / 2 - size[0] / 2 )
        self.__window_height = int( self.__root.winfo_screenheight() / 2 - size[1] / 2 )
        self.__root.geometry( f"{size[0]}x{size[1]}+{self.__window_width}+{self.__window_height}" )

        self.__root.title( "Tabuleiro" )
        self.__root.protocol( "WM_DELETE_WINDOW", self.on_closing )

        # Board Frames
        self.__board_frame = tk.Frame( self.__root, bg="blue", padx=30, pady=15, relief="sunken", borderwidth=2 )
        self.__board_positions = tk.Frame( self.__board_frame, bg="pink", height=350, width=150, relief="sunken" )
        self.__hud = tk.Frame( self.__board_frame, bg="red", height=150, width=150 )

        # Frames - board_positions
        self.__tiles_board = tk.Frame( self.__board_positions, bg="yellow", height=350, width=150,
                                            relief="sunken" )
        # Frames - hud
        self.__hud_player_img = tk.Label( self.__hud, bg="pink", height=10, width=10 )

        self.create_players()
        # Row and Column configs - Para: frame, amount (columns or rows), weight
        self.column_frame_configure( self.__board_frame, 1, [1] )
        self.row_frame_configure( self.__board_frame, 3, [1, 2, 1] )
        self.column_frame_configure( self.__board_positions, 2, [1, 5] )
        self.column_frame_configure( self.__hud, 2, [1, 2] )

        # Others vars
        self.__check_state = tk.IntVar()
        self.__check = tk.Checkbutton( self.__hud, text="Show Message", variable=self.__check_state )
        self.__check.grid( pady=10 )

        self.__deck = Deck( self.__board_positions, self )

        # Menu vars
        self.__menubar = None
        self.__filemenu = None

        # Frame propagate
        self.__board_frame.pack_propagate( False )
        self.__board_positions.grid_propagate( False )
        self.__hud.grid_propagate( False )

        # Start functions
        self.set_menu()
        self.set_positions()
        self.widget_packs()

        # player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.__root.focus()

    def create_players(self, name="kid"):
        img = "images/"
        if len( self.__players ) == 0:
            img += "kid_one.png"
        elif len( self.__players ) == 1:
            img += "kid_two.png"
        elif len( self.__players ) == 2:
            img += "kid_three.png"

        player_img = self.load_label_img( self.__hud_player_img, img )
        player1 = Player( name, player_img )
        self.__players.append( player1 )

    def show_card(self, card, button, state="questions"):
        card_interface = tk.Toplevel()
        card_interface.title("Carta")

        def end_carta(button):
            button['state'] = 'normal'
            card_interface.destroy()

        card_width_pos = int( self.__window_width + self.__window_width / 2 - (card.width / 2) )
        card_height_pos = int( self.__window_height + self.__window_height / 2 )

        card_interface.geometry( f'{card.width}x{card.height}+{card_width_pos}+{card_height_pos}' )
        card_interface.resizable( width=False, height=False )

        if state == "questions":
            card_frame = tk.Frame( card_interface, bg='blue' )
            card_title = tk.Label( card_interface, padx=10, pady=10, text='Escolha uma pergunta!' )
            for key, question in card.questions.items():
                question_button = tk.Button(
                    card_frame,
                    text=question,  # Exibindo o valor do dicionário
                    command=lambda key=key: [self.__deck.create_answers( key, self ), card_interface.destroy()],
                    width=100
                )
                question_button.pack( padx=10, pady=10 )
        else:
            card_frame = tk.Frame( card_interface, bg='green' )
            question_key = card.questions.keys()
            card_title = tk.Label( card_interface, padx=10, pady=10, text=card.questions[list( question_key )[0]] )
            for answer in card.answers:
                answer_button = tk.Button(
                    card_frame,
                    text=answer,  # Exibindo o valor do dicionário
                    command=lambda answer_=answer: [self.__deck.check_answer( list( question_key )[0], answer_, self ),
                                                    end_carta( button )],
                    width=100
                )
                answer_button.pack( padx=10, pady=10 )

        card_title.pack( padx=10, pady=10 )
        card_frame.pack( padx=10, pady=10 )

        card_interface.focus()
        card_interface.grab_set()
        card_interface.protocol( "WM_DELETE_WINDOW", lambda: end_carta( button ) )

    def board_loop(self):
        self.__root.mainloop()

    def row_frame_configure(self, frame, row_amount, weight: []):
        for i in range( row_amount ):
            frame.rowconfigure( i, weight=weight[i] )

    def column_frame_configure(self, frame: tk.Frame, column_amount: int, weight: []):
        for i in range( column_amount ):
            frame.columnconfigure( i, weight=weight[i] )

    # Create all board positions
    def set_positions(self):
        position_types = {
            0: "fim.png",
            1: "simples.png",
            2: "multipla.png",
            3: "desafio.png",
            4: "fim.png"
        }

        for i in range( self.__tile_amount + 2 ):
            # If reached last position, set the final position of the board.
            if i != 0 and i <= self.__tile_amount:
                number = int( random.uniform( 1, 4 ) )
            elif i == 0:
                number = 4
            else:
                number = 0

            image_path = os.path.join( os.path.dirname( __file__ ), "./images/" + position_types[number] )
            position = self.load_label_img( self.__tiles_board, image_path )
            # Bind and specify event for each position.
            position.bind( "<Button-1>",
                           lambda event="", position_number=i: self.position_bind( event, position_number ) )
            self.__positions.append( Position( number, position ) )
        self.__positions[0].occupants = [0, 1, 2]

    def load_label_img(self, widget, path):
        image = Image.open( path )
        photo = ImageTk.PhotoImage( image )
        label = tk.Label( widget, image=photo )
        label.image = photo
        return label

    def walk_in_board(self, value):
        for i in self.__positions:
            print(i.occupants)

        self.__players[0].image.grid( row=0, column=i )

    '''
       image_path = os.path.join(os.path.dirname(__file__), './images/carta_baixo.png')
        self.__button = self.load_label_img(self, image_path, controller)
        self.__button.grid(row=0, column=0)
        self.__button.configure()

    def load_label_img(self, widget, path, controller):
        image = Image.open(path)
        photo = ImageTk.PhotoImage( image )
        deck_button = tk.Button( widget, command=lambda: self.create_card(controller), image=photo )
        deck_button.image = photo
        return deck_button
    '''


    def position_bind(self, event, a):
        print( self.__positions[a], event.x)
        print(self.__positions[a].occupants)

    def show_message(self):
        if self.__check_state.get() == 0:
            print( "Deck" )

    def on_closing(self):
        if messagebox.askyesno( title="Quit", message="Quer Sair?" ):
            self.__root.destroy()

    def shortcut(self, event):
        if event.state == 12 and event.keysym == "Return":
            self.show_message()

    def set_menu(self):
        self.__menubar = tk.Menu( self.__root )
        self.__filemenu = tk.Menu( self.__menubar, tearoff=0 )
        self.__filemenu.add_command( label="Procurar jogador" )
        self.__filemenu.add_separator()
        self.__filemenu.add_command( label="Close", command=self.on_closing )

        self.__menubar.add_cascade( menu=self.__filemenu, label="File" )

        self.__root.config( menu=self.__menubar )

    def widget_packs(self):
        self.__board_frame.pack( fill="both", expand=True )
        self.__board_positions.grid( row=1, sticky="ew" )
        self.__hud.grid( row=2, sticky="ew" )

        self.__tiles_board.grid( column=0, sticky="ew" )
        self.__deck.grid( row=0, column=1, sticky="NS" )

        self.__hud_player_img.grid( column=0, sticky="NS" )

        row = 0
        column = 0
        for i in range( len( self.__positions ) ):
            self.__positions[i].widget.grid( column=column, row=row, pady=5, padx=5 )
            if column > 3:
                row += 1
                column = 0
            else:
                column += 1

        for i in range( len( self.__players ) ):
            self.__players[i].image.grid( row=0, column=i )
