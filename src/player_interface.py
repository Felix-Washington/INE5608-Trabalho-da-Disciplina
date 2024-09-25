from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

import random
import os
from PIL import Image, ImageTk

from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor

from deck import Deck
from board import Board


def row_frame_configure(frame, row_amount, weight):
    for i in range( row_amount ):
        frame.rowconfigure( i, weight=weight[i] )


def column_frame_configure(frame: Frame, column_amount: int, weight):
    for i in range( column_amount ):
        frame.columnconfigure( i, weight=weight[i] )


class PlayerInterface( DogPlayerInterface ):
    def __init__(self):
        super().__init__()
        # Root config
        self.__root = Tk()

        # Window size and position
        self.__game_size = [int( self.__root.winfo_screenwidth() / 3 ), 800]
        self.__game_pos_x = int( self.__root.winfo_screenwidth() / 2 - self.__game_size[0] / 2 )
        self.__game_pos_y = int( self.__root.winfo_screenheight() / 2 - self.__game_size[1] / 2 )

        self.board = Board()
        # Frames
        self.__board_frame, self.__board_positions, self.__hud = None, None, None
        # Hud frames
        self.__current_turn, self.__logs = None, None
        # Menus
        self.__menubar, self.__filemenu = None, None

        self.load_main_window()

        # Prevent main windows from minimize
        self.__root.deiconify()

        self.dog_server_interface = DogActor()

        self.test = None

    def load_main_window(self):
        self.__root.geometry( f"{self.__game_size[0]}x{self.__game_size[1]}+{self.__game_pos_x}+{self.__game_pos_y}" )
        self.__root.title( "Tabuleiro" )
        self.__root.protocol( "WM_DELETE_WINDOW", self.on_closing )

        self.__root.resizable( False, False )

        # Board Frames
        board_color = "blue"
        self.__board_frame = Frame( self.__root, padx=20, bg=board_color)
        self.__board_positions = Frame( self.__board_frame,  bg=board_color)
        self.__hud = Frame( self.__board_frame, height=(self.__game_size[1]/2) - 100, bg="green")

        # Row and Column configs - Para: frame, amount (columns or rows), weight
        column_frame_configure( self.__board_frame, 1, [1] )
        row_frame_configure( self.__board_frame, 3, [1, 2, 1] )
        column_frame_configure( self.__hud, 2, [1, 2] )

        self.set_menu()
        self.widget_packs()

    def draw_card(self, card, button, state="questions"):
        card_interface = Toplevel()
        card_interface.title( "Carta" )

        def end_card(button_):
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
                    command=lambda key=key: [self.board.deck.create_answers( key, self ), card_interface.destroy()],
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
                    command=lambda answer_=answer: [self.board.deck.check_answer( list( question_key )[0], answer_, self ),
                                                    end_card( button )], width=100 )
                answer_button.pack( padx=10, pady=10 )

        card_title.pack( padx=10, pady=10 )
        card_frame.pack( padx=10, pady=10 )

        card_interface.focus()
        card_interface.grab_set()
        card_interface.protocol( "WM_DELETE_WINDOW", lambda: end_card( button ) )

    def board_loop(self):
        self.__root.mainloop()

    # Set labels to all positions
    def set_positions(self):
        for i in range( len( self.board.positions ) ):
            position_size = self.__game_size[0] / 10 - 20

            # Obter o caminho da imagem da posição
            image_path = self.board.positions[i].image  # Assume que cada posição tem um atributo `image`

            # Verificar se a imagem existe
            if not os.path.isfile( image_path ):
                print( f"Imagem não encontrada: {image_path}" )
                continue  # Pule esta posição se a imagem não existir

            # Criando o Frame
            position_frame = Frame( self.__board_positions, width=position_size, height=position_size )
            position_frame.pack_propagate( False )  # Para não ajustar o tamanho do Frame ao conteúdo

            # Carregando a imagem
            try:
                position_frame.picture = PhotoImage( file=image_path )  # Usando o caminho dinâmico
                position_frame.label = Label( position_frame, image=position_frame.picture )
            except Exception as e:
                print( f"Erro ao carregar a imagem {image_path}: {e}" )
                continue  # Pule esta posição se houver um erro ao carregar a imagem

            # Adicionando o Label ao Frame
            position_frame.label.pack( fill='both', expand=True )  # Para que o Label preencha o Frame

            # Configurando o Frame
            position_frame.configure( width=position_size, height=position_size )

            # Salvando a referência ao Frame
            self.board.positions[i].widget = position_frame

    def set_hud(self):
        # Show current player turn
        self.__current_turn = Frame( self.__hud, width=400, height=100, bg="red" )
        # Game log
        self.__logs = Frame( self.__hud, width=400, height=200, bg="gray" )

        # Deck
        self.board.deck = Deck( self.__hud, self )

    def load_label_img(self, widget, path):
        image = Image.open( path )
        photo = ImageTk.PhotoImage( image )
        label = Label( widget, image=photo )
        label.image = photo
        return label

    def on_closing(self):
        self.__root.destroy()

    def set_menu(self):
        self.__menubar = Menu( self.__root )
        self.__filemenu = Menu( self.__menubar, tearoff=0 )
        self.__filemenu.add_command( label="Procurar jogador", command=self.search_player )
        self.__filemenu.add_separator()
        self.__filemenu.add_command( label="Close", command=self.on_closing )

        self.__menubar.add_cascade( menu=self.__filemenu, label="File" )
        self.__root.config( menu=self.__menubar )

    def search_player(self, ):
        player_name = simpledialog.askstring( title="Player identification", prompt="Qual o seu nome?" )
        message = self.dog_server_interface.initialize( player_name, self )
        messagebox.showinfo( message=message )
        self.board.start_match()

        self.set_positions()
        self.set_hud()
        self.start_match_widget_packs()

    def widget_packs(self):
        self.__board_frame.pack( fill="both", expand=True )
        self.__board_positions.grid( row=0, column=0, sticky="ew" )
        self.__hud.grid( row=2, sticky="ew" )

        # Propagate
        self.__board_frame.pack_propagate( False )
        self.__hud.grid_propagate( False )

    def start_match_widget_packs(self):
        self.__current_turn.grid( row=0, column=0, padx=5, pady=5 )
        self.__logs.grid( row=1, column=0, padx=5, pady=5 )
        self.board.deck.grid( row=0, column=1, rowspan=2, padx=5, pady=5 )

        row = 0
        column = 0
        reverse = False
        for i in range( len( self.board.positions ) ):
            self.board.positions[i].widget.grid( column=column, row=row, pady=5, padx=5 )
            self.board.positions[i].widget.label.pack_propagate( False )
            if (reverse and column == 0) or (not reverse and column == 9):
                if row % 2 == 1:
                    reverse = not reverse
                row += 1
            else:
                column += -1 if reverse else 1

            # Adicionando imagens dos ocupantes
            if self.board.positions[i].occupants:
                for j, occupant_id in enumerate( self.board.positions[i].occupants ):
                    occupant_image_path = f"./images/kid_{occupant_id}.png"

                    # Verifique se a imagem do ocupante existe
                    if os.path.isfile( occupant_image_path ):
                        occupant_image = PhotoImage( file=occupant_image_path )

                        # Criando um Label para o ocupante
                        occupant_label = Label( self.board.positions[i].widget, image=occupant_image, width=10, height= 10 )
                        occupant_label.image = occupant_image  # Manter a referência da imagem

                        # Posicionando o Label do ocupante
                        occupant_label.grid( row=j, column=0, padx=1, pady=1 )
                    else:
                        print( f"Imagem do ocupante não encontrada: {occupant_image_path}" )



