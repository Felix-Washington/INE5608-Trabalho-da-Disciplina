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

        self.__window_width, self.__window_height = 0, 0

        # Frames
        self.__board_frame, self.__board_positions, self.__hud, self.__deck = None, None, None, None
        self.__tiles_board = None

        # Label
        self.__hud_player_img = None

        # Menus
        self.__menubar, self.__filemenu = None, None

        # game_state = self.board.get_status()
        # self.update_gui(game_state)

        self.load_main_window()

        # Prevent main windows from minimize
        self.__root.deiconify()

        self.dog_server_interface = DogActor()

    def load_main_window(self):
        size = [int( self.__root.winfo_screenwidth() / 3 ), 800]
        #self.__window_width = int( self.__root.winfo_screenwidth() / 2 - size[0] / 2 )
        #self.__window_height = int( self.__root.winfo_screenheight() / 2 - size[1] / 2 )
        #self.__root.geometry( f"{size[0]}x{size[1]}+{self.__window_width}+{self.__window_height}" )
        self.__root.geometry("800x800")
        self.__root.title( "Tabuleiro" )
        self.__root.protocol( "WM_DELETE_WINDOW", self.on_closing )

        self.__root.resizable( False, False )
        self.__board = Frame(self.__root, bg="black", padx=10, pady=10, border=2)
        self.__board.pack(fill="both", expand=True)

        self.__casas = Frame(self.__board, width=750, height=400, bg="black")
        self.__casas.pack(fill="both", expand=True)

        self.frames = []
        self.cores = ["yellow", "blue", "red", "yellow", "blue", "red", "yellow", "blue", "red", "yellow"]
        for i in range(0, 5):
            if i == 1:
                frame = Frame(self.__casas, width=69, height=69, bg="yellow")
                frame.grid(row=1, column=9, padx=5, pady=5)
                self.frames.append(frame)
            elif i == 3:
                frame = Frame(self.__casas, width=69, height=69, bg="red")
                frame.grid(row=3, column=0, padx=5, pady=5)
                self.frames.append(frame)
            else:
                for j in range(0, 10):
                    if i == 0 and j == 0:
                        frame = Frame(self.__casas, width=69, height=69, bg="gray")
                        frame.grid(row=0, column=0, padx=5, pady=5)
                        self.frames.append(frame)
                    elif i == 4 and j == 9:
                        frame = Frame(self.__casas, width=69, height=69, bg="gray")
                        frame.grid(row=4, column=9, padx=5, pady=5)
                        self.frames.append(frame)
                    else:
                        frame = Frame(self.__casas, width=69, height=69, bg=self.cores[j])
                        frame.grid(row=i, column=j, padx=5, pady=5)
                        self.frames.append(frame)

        #segundo corpo do frame teste
        self.__contato = Frame(self.__board, width=750, height=400, bg="black")
        self.__contato.pack(fill="both", expand=True)
        #turno do jogador
        self.__turno = Frame(self.__contato, width=300, height=100, bg="red")
        self.__turno.grid(row=0, column=0, padx=20, pady=5)
        #andamento do jogo
        self.__andamento = Frame(self.__contato, width=300, height=200, bg="gray")
        self.__andamento.grid(row=1, column=0, padx=20, pady=5)
        #carta
        self.carta = Frame(self.__contato, width=250, height=310, bg="black", highlightbackground="white",
                           highlightthickness=2)
        self.carta.grid(row=0, column=1, rowspan=2, padx=80, pady=5)
        '''
        # Board Frames
        self.__board_frame = Frame( self.__root, bg="blue", padx=30, pady=15, relief="sunken", borderwidth=2 )
        self.__board_positions = Frame( self.__board_frame, bg="pink", height=350, width=150, relief="sunken" )
        self.__hud = Frame( self.__board_frame, bg="red", height=150, width=150 )

        # Frames - hud
        self.__hud_player_img = Label( self.__hud, bg="pink", height=10, width=10 )

        # Row and Column configs - Para: frame, amount (columns or rows), weight
        column_frame_configure( self.__board_frame, 1, [1] )
        row_frame_configure( self.__board_frame, 3, [1, 2, 1] )
        column_frame_configure( self.__board_positions, 2, [1, 5] )
        column_frame_configure( self.__hud, 2, [1, 2] )

        self.__deck = Deck( self.__board_positions, self )

        self.__board_frame.pack_propagate( False )
        self.__board_positions.grid_propagate( False )
        self.__hud.grid_propagate( False )

        # Frames - board_positions
        self.__tiles_board = Frame( self.__board_positions, bg="yellow", height=350, width=150, relief="sunken" )
        # Frames - hud
        self.__hud_player_img = Label( self.__hud, bg="pink", height=10, width=10 )
        '''
        self.set_menu()
        self.set_positions()
        self.widget_packs()

    def show_card(self, card, button, state="questions"):
        card_interface = Toplevel()
        card_interface.title( "Carta" )

        def end_carta(button_):
            button_['state'] = 'normal'
            card_interface.destroy()

        card_width_pos = int( self.__window_width + self.__window_width / 2 - (card.width / 2) )
        card_height_pos = int( self.__window_height + self.__window_height / 2 )

        card_interface.geometry( f'{card.width}x{card.height}+{card_width_pos}+{card_height_pos}' )
        card_interface.resizable( width=False, height=False )

        if state == "questions":
            card_frame = Frame( card_interface, bg='blue' )
            card_title = Label( card_interface, padx=10, pady=10, text='Escolha uma pergunta!' )
            for key, question in card.questions.items():
                question_button = Button(
                    card_frame,
                    text=question,  # Exibindo o valor do dicionário
                    command=lambda key=key: [self.__deck.create_answers( key, self ), card_interface.destroy()],
                    width=100
                )
                question_button.pack( padx=10, pady=10 )
        else:
            card_frame = Frame( card_interface, bg='green' )
            question_key = card.questions.keys()
            card_title = Label( card_interface, padx=10, pady=10, text=card.questions[list( question_key )[0]] )
            for answer in card.answers:
                answer_button = Button(
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

            image_path = os.path.join( os.path.dirname( __file__ ), "./images/" + position_types[number] )
            position = self.load_label_img( self.__tiles_board, image_path )
            # Bind and specify event for each position.
            position.bind( "<Button-1>",
                           lambda event="", position_number=i: self.position_bind( event, position_number ) )
            self.board.positions.append( Position( number, position ) )
        self.board.positions[0].occupants = [0, 1, 2]

    def load_label_img(self, widget, path):
        image = Image.open( path )
        photo = ImageTk.PhotoImage( image )
        label = Label( widget, image=photo )
        label.image = photo
        return label

    def position_bind(self, event, a):
        print( self.board.positions[a].widget.image, "teste" )

    def on_closing(self):
        if messagebox.askyesno( title="Quit", message="Quer Sair?" ):
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

    def widget_packs(self):
        '''
        self.__board_frame.pack( fill="both", expand=True )
        self.__board_positions.grid( row=1, sticky="ew" )
        self.__hud.grid( row=2, sticky="ew" )

        self.__tiles_board.grid( column=0, sticky="ew" )
        self.__deck.grid( row=0, column=1, sticky="NS" )

        self.__hud_player_img.grid( column=0, sticky="NS" )

        row = 0
        column = 0
        for i in range( len( self.board.positions ) ):
            self.board.positions[i].widget.grid( column=column, row=row, pady=5, padx=5 )
            if column > 3:
                row += 1
                column = 0
            else:
                column += 1

        for player in self.board.players:
            image_path = os.path.join( os.path.dirname( __file__ ), player.image )
            player_image = self.load_label_img( self.__hud_player_img, image_path )
            player_image.grid( row=0, column=i )'''
