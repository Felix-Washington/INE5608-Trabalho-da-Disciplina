from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

from deck import Deck

import random
import os

from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor

from PIL import Image, ImageTk
from deck import Deck
from board import Board
from position import Position


def row_frame_configure(frame, row_amount, weight):
    for i in range( row_amount ):
        frame.rowconfigure( i, weight=weight[i] )


def column_frame_configure(frame: Frame, column_amount: int, weight):
    for i in range( column_amount ):
        frame.columnconfigure( i, weight=weight[i] )


class PlayerInterface( DogPlayerInterface ):
    def __init__(self):
        super().__init__()
        self.board = Board()
        # Root config
        self.__root = Tk()
        # x 853: 70 / y 800:70
        self.__game_pos_x, self.__game_pos_y = 0, 0
        self.__game_size = [int( self.__root.winfo_screenwidth() / 3 ), 800]
        self.__game_pos_x = int( self.__root.winfo_screenwidth() / 2 - self.__game_size[0] / 2 )
        self.__game_pos_y = int( self.__root.winfo_screenheight() / 2 - self.__game_size[1] / 2 )

        # Frames
        self.__board_frame, self.__board_positions, self.__hud = None, None, None
        # Hud frames
        self.__current_turn, self.__logs, self.__deck = None, None, None
        # Menus
        self.__menubar, self.__filemenu = None, None

        # game_state = self.board.get_status()
        # self.update_gui(game_state)

        self.load_main_window()

        # Prevent main windows from minimize
        self.__root.deiconify()

        self.dog_server_interface = DogActor()

    def load_main_window(self):
        self.__root.geometry( f"{self.__game_size[0]}x{self.__game_size[1]}+{self.__game_pos_x}+{self.__game_pos_y}" )
        self.__root.title( "Tabuleiro" )
        self.__root.protocol( "WM_DELETE_WINDOW", self.on_closing )

        self.__root.resizable( False, False )

        # Board Frames
        board_color = "black"
        self.__board_frame = Frame( self.__root, padx=20, bg=board_color)
        self.__board_positions = Frame( self.__board_frame,  bg=board_color)
        self.__hud = Frame( self.__board_frame, height=(self.__game_size[1]/2) - 100, bg="green")

        # Row and Column configs - Para: frame, amount (columns or rows), weight
        column_frame_configure( self.__board_frame, 1, [1] )
        row_frame_configure( self.__board_frame, 3, [1, 2, 1] )
        column_frame_configure( self.__hud, 2, [1, 2] )

        self.set_menu()
        self.set_positions()
        self.set_hud()
        self.widget_packs()

    def draw_card(self, card, button, state="questions"):
        card_interface = Toplevel()
        card_interface.title( "Carta" )

        def end_carta(button_):
            button_['state'] = 'normal'
            card_interface.destroy()

        card_width_pos = int( self.__game_pos_x + self.__game_pos_x / 2 - (card.width / 2) )
        card_height_pos = int( self.__game_pos_y + self.__game_pos_y / 2 )

        card_interface.geometry( f'{card.width}x{card.height}+{card_width_pos}+{card_height_pos}' )
        card_interface.resizable( width=False, height=False )

        if state == "questions":
            card_frame = Frame( card_interface, bg='blue' )
            card_title = Label( card_interface, text='Escolha uma pergunta!' )
            for key, question in card.questions.items():
                question_button = Button(
                    card_frame,
                    text=question,
                    command=lambda key=key: [self.__deck.create_answers( key, self ), card_interface.destroy()],
                    width=100
                )
                question_button.pack( padx=10, pady=10 )
        else:
            card_frame = Frame( card_interface, bg='green' )
            question_key = card.questions.keys()
            card_title = Label( card_interface, text=card.questions[list( question_key )[0]] )
            for answer in card.answers:
                answer_button = Button(
                    card_frame,
                    text=answer,
                    command=lambda answer_=answer: [self.__deck.check_answer( list( question_key )[0], answer_, self ),
                                                    end_carta( button )], width=100 )
                answer_button.pack( padx=10, pady=10 )

        card_title.pack( padx=10, pady=10 )
        card_frame.pack( padx=10, pady=10 )

        card_interface.focus()
        card_interface.grab_set()
        card_interface.protocol( "WM_DELETE_WINDOW", lambda: end_carta( button ) )

    def board_loop(self):
        self.__root.mainloop()

    # Create all board positions
    def set_positions(self):
        position_types = {
            0: "fim.png",
            1: "simples.png",
            2: "multipla.png",
            3: "desafio.png",
        }

        for i in range( self.board.tile_amount + 2 ):
            # If reached last position, set the final position of the board.
            if i != 0 and i <= self.board.tile_amount:
                number = int( random.uniform( 1, 4 ) )
            elif i == 0:
                number = 1
            else:
                number = 0

            # Bind and specify event for each position.
            position_size = self.__game_size[0]/10 - 20  # (Window width size / tiles length) - board padx
            image_path = os.path.join( os.path.dirname( __file__ ), "./images/" + position_types[number] )
            position = self.load_label_img( self.__board_positions, image_path )
            position.configure( width=position_size, height=position_size )
            position.pack_propagate( False )
            # Bind and specify event for each position.
            position.bind( "<Button-1>",
                           lambda event="", position_number=i: self.position_bind( event, position_number ) )
            self.board.positions.append( Position( number, position ) )
        self.board.positions[0].occupants = [0, 1, 2]

    def set_hud(self):
        # Show current player turn
        self.__current_turn = Frame( self.__hud, width=400, height=100, bg="red" )
        # Game log
        self.__logs = Frame( self.__hud, width=400, height=200, bg="gray" )

        # deck
        self.__deck = Deck( self.__hud, self )

    def load_label_img(self, widget, path):
        image = Image.open( path )
        photo = ImageTk.PhotoImage( image )
        label = Label( widget, image=photo )
        label.image = photo
        return label

    def position_bind(self, event, a):
        print( self.board.positions[a].position_type, "teste" )

    def on_closing(self):
        # if messagebox.askyesno( title="Quit", message="Quer Sair?" ):
        self.__root.destroy()

    def set_menu(self):
        self.__menubar = Menu( self.__root )
        self.__filemenu = Menu( self.__menubar, tearoff=0 )
        self.__filemenu.add_command( label="Procurar jogador", command=self.search_player )
        self.__filemenu.add_separator()
        self.__filemenu.add_command( label="Close", command=self.on_closing )

        self.__menubar.add_cascade( menu=self.__filemenu, label="File" )
        self.__root.config( menu=self.__menubar )

    def search_player(self):
        player_name = simpledialog.askstring( title="Player identification", prompt="Qual o seu nome?" )
        message = self.dog_server_interface.initialize( player_name, self )
        messagebox.showinfo( message=message )

    def widget_packs(self):
        self.__board_frame.pack( fill="both", expand=True )

        self.__board_positions.grid( row=0, column=0, sticky="ew" )
        self.__hud.grid( row=2, sticky="ew" )

        self.__current_turn.grid( row=0, column=0, padx=5, pady=5 )
        self.__logs.grid( row=1, column=0, padx=5, pady=5 )
        self.__deck.grid( row=0, column=1, rowspan=2, padx=5, pady=5 )

        row = 0
        column = 0
        reverse = False
        for i in range( len( self.board.positions ) ):
            self.board.positions[i].widget.grid( column=column, row=row, pady=5, padx=5 )

            if (reverse and column == 0) or (not reverse and column == 9):
                if row % 2 == 1:
                    reverse = not reverse
                row += 1
            else:
                column += -1 if reverse else 1

        # Propagate
        self.__board_frame.pack_propagate( False )
        self.__hud.grid_propagate( False )