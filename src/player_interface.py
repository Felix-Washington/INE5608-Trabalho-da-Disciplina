from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

import random
import os
from PIL import Image, ImageTk

from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor

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
        # Root config.
        self.__root = Tk()

        # Window size and position.
        self.__game_size = [int( self.__root.winfo_screenwidth() / 3 ), 800]
        self.__game_pos_x = int( self.__root.winfo_screenwidth() / 2 - self.__game_size[0] / 2 )
        self.__game_pos_y = int( self.__root.winfo_screenheight() / 2 - self.__game_size[1] / 2 )

        # Frames.
        self.__board_frame, self.__board_positions_frame, self.__hud_frame = None, None, None
        # Hud frames.
        self.__current_turn, self.__logs_frame, self.__deck_frame = None, None, None
        # Menus
        self.__menubar, self.__filemenu = None, None
        # Listbox for register all game logs.
        self.__logs_listbox = None
        # Button to active deck.
        self.__deck_button = None

        # Create board instance.
        self.__board = Board()

        self.load_main_window()

        # Prevent main windows from minimize.
        self.__root.deiconify()

        # Connection with DOG.
        self.dog_server_interface = DogActor()
        player_name = simpledialog.askstring( title="Player identification", prompt="Qual o seu nome?" )
        message = self.dog_server_interface.initialize( player_name, self )
        messagebox.showinfo( message=message )

    def load_main_window(self):
        # Configuration of game window.
        self.__root.geometry( f"{self.__game_size[0]}x{self.__game_size[1]}+{self.__game_pos_x}+{self.__game_pos_y}" )
        self.__root.title( "Tabuleiro" )
        self.__root.protocol( "WM_DELETE_WINDOW", self.on_closing )
        self.__root.resizable( False, False )

        # Board Frames.
        board_color = "lightblue"
        self.__board_frame = Frame( self.__root, padx=20, bg=board_color )
        self.__board_positions_frame = Frame( self.__board_frame, bg=board_color )
        self.__hud_frame = Frame( self.__board_frame, height=(self.__game_size[1] / 2) - 100, bg=board_color )

        # Row and Column configs - Para: frame, amount (columns or rows), weight
        column_frame_configure( self.__board_frame, 1, [1] )
        row_frame_configure( self.__board_frame, 3, [1, 2, 1] )
        column_frame_configure( self.__hud_frame, 2, [1, 2] )

        self.set_hud()
        self.set_menu()
        # Board that holds entire screen.
        self.__board_frame.pack( fill="both", expand=True )

    # Function called to process card interface.
    def draw_card(self, state="questions"):
        # Create window popup for the card.
        card_interface = Toplevel()
        card_interface.title( "Carta" )

        card = self.__board.deck.card

        # Get x and y position of the card.
        card_width_pos = int( self.__game_pos_x + self.__game_pos_x / 2 - (card.width / 2) )
        card_height_pos = int( self.__game_pos_y + self.__game_pos_y / 2 )

        # Set card window position and size.
        card_interface.geometry( f'{card.width}x{card.height}+{card_width_pos}+{card_height_pos}' )
        card_interface.resizable( width=False, height=False )
        card_interface.configure( background='#ffbd59' )

        card_title = None
        card_frame = Frame( card_interface, background='#ffbd59' )

        # Configuration for question card
        if state == "questions":
            card_title = Label( card_interface, text='Escolha uma pergunta!', width=300, height=8 )
            # self.__deck_button['state'] = 'disabled'

            for key, question in card.options.items():
                question_button = Button(
                    card_frame,
                    text=question,
                    command=lambda key=key: [self.check_position( "questions", key ), card_interface.destroy()],
                    width=300,
                    height=2,
                    font=('Arial', 12)
                )
                question_button.pack( padx=10, pady=10 )

                # If position is not "desafio", it will hide all questions.
                # if self.__board.positions[self.__board.current_position_board].type < 3:
                #    question_button.configure(text="?")

        # Configuration for answer card
        elif state == "answers":
            card_title = Label( card_interface, text=self.__board.deck.get_question(), width=300, height=8 )

            for answer in card.options:
                answer_button = Button(
                    card_frame,
                    text=answer,
                    command=lambda answer_=answer: [
                        self.check_position( "answers", self.__board.deck.get_question(), answer_ ),
                        card_interface.destroy()
                    ], width=300, height=2, font=('Arial', 12) )
                answer_button.pack( padx=10, pady=10 )

        card_title.pack( padx=10, pady=10 )
        card_frame.pack( padx=10, pady=10 )

        card_interface.focus()
        card_interface.grab_set()
        card_interface.protocol( "WM_DELETE_WINDOW", lambda: card_interface.destroy() )

    # Set labels to all positions.
    def set_positions(self):
        for i in range( len( self.__board.positions ) ):
            position_size = self.__game_size[0] / 10 - 15

            # Get position image path.
            image_path = self.__board.positions[i].image

            # Verify if path is valid
            if not os.path.isfile( image_path ):
                print( f"Imagem não encontrada: {image_path}" )
                continue  # Jump if image not exist

            # Create position Frame.
            position_frame = Frame( self.__board_positions_frame, width=position_size, height=position_size )
            position_frame.pack_propagate( False )  # Prevent frame size auto adjust

            # Load position image.
            try:
                position_frame.picture = PhotoImage( file=image_path )  # Relative path for the image
                position_frame.label = Label( position_frame, image=position_frame.picture )
            except Exception as e:
                print( f"Erro ao carregar a imagem {image_path}: {e}" )
                continue  # If load fail ignore the position

            # Add Label to Frame.
            position_frame.label.pack( fill='both', expand=True )  # Pack to fill Frame with the Label

            #  Frame Settings.
            position_frame.configure( width=position_size, height=position_size )

            # Saving frame in position widget.
            self.__board.positions[i].widget = position_frame

    def check_position(self, card_type, key=-1, answer_=-1):
        if card_type == "create":
            self.__board.deck.create_card()
            self.update_gui_message( "drew_card", self.__board.current_player_turn.name )
            self.draw_card()

        elif card_type == "questions":
            if self.__board.current_position_board == 1 or self.__board.current_position_board == 2:
                self.__board.deck.create_answers( key )
                self.__board.local_player.selected_question = key
                self.update_gui_message( "select_question", self.__board.current_player_turn.name )
                self.draw_card( "answers" )

            if self.__board.current_position_board == 2 or self.__board.current_position_board == 3:
                self.__board.temporary_turn = True

        elif card_type == "answers":
            if self.__board.current_position_board == 1:
                self.__board.process_board_status( key, answer_ )
                self.update_gui_message( "select_answer", self.__board.current_player_turn.name )
                self.update_widget_packs()

                position_types, turn_order, current_player, status = self.__board.get_start_match_data()
                move_to_send = {"positions": position_types, "turn_order": turn_order, "current_player": current_player,
                                "game_status": status, "match_status": "next"}
                # Send first move to all players.
                self.dog_server_interface.send_move( move_to_send )

    # Set
    def set_hud(self):
        # Show current player turn
        self.__current_turn = Frame( self.__hud_frame, width=400, height=100, bg="red" )
        # Game actions log frame.
        self.__logs_frame = Frame( self.__hud_frame, width=400, height=200, bg="gray" )
        # Game actions log widget.
        self.__logs_listbox = Listbox( self.__logs_frame, bg='lightgray', font=('Arial', 12) )
        # Deck
        self.__deck_frame = Frame( self.__hud_frame )
        # Button used to draw a card.
        self.__deck_button = Button( self.__deck_frame, width=15, height=13, text="?",
                                     command=lambda: [self.check_position( "create" )],
                                     bg='black', highlightthickness=2, font=48, fg='white', state='normal' )

    # Config to close the window.
    def on_closing(self):
        self.__root.destroy()

    def board_loop(self):
        self.__root.mainloop()

    # Insert game status to interface log list.
    def update_gui_message(self, text, player="", player2=""):
        message = ""
        match text:
            case "drew_card":
                message = f"Jogador {player} comprou uma carta."
            case "draw_card":
                message = "Compre uma carta."
            case "select_question":
                message = f"Jogador {player} selecionou uma pergunta."
            case "select_answer":
                message = f"Jogador {player} selecionou uma resposta."
            case "pending_turn":
                message = f"Jogador {player} selecionou o jogador {player2} para responder uma pergunta."

        self.__logs_listbox.insert( 0, message )
        self.__logs_listbox.yview( 0 )

    # Create Menu item and add its buttons.
    def set_menu(self):
        self.__menubar = Menu( self.__root )
        self.__filemenu = Menu( self.__menubar, tearoff=0 )
        self.__filemenu.add_command( label="Iniciar partida", command=self.start_match )
        self.__filemenu.add_separator()
        self.__filemenu.add_command( label="Close", command=self.on_closing )

        self.__menubar.add_cascade( menu=self.__filemenu, label="File" )
        self.__root.config( menu=self.__menubar )

    # Call DOG to try start the match.
    def start_match(self):
        start_status = self.dog_server_interface.start_match( 2 )
        code = start_status.get_code()
        message = start_status.get_message()

        if code == "0" or code == "1":
            messagebox.showinfo( message=message )
        else:  # (code=='2')
            players = start_status.get_players()
            local_player_id = start_status.get_local_id()
            self.__board.start_match( players, local_player_id )
            messagebox.showinfo( message=start_status.get_message() )

            self.set_positions()

            # Get all neccessary data to send to all players.
            position_types, turn_order, current_player, status = self.__board.get_start_match_data()
            move_to_send = {"positions": position_types, "turn_order": turn_order, "current_player": current_player,
                            "game_status": status, "match_status": "next"}
            # Send first move to all players.
            self.dog_server_interface.send_move( move_to_send )

            self.start_match_widget_packs()
            self.update_widget_packs()

            if self.__board.local_player.turn:
                self.prepare_current_move()

    def receive_start(self, start_status):
        players = start_status.get_players()
        local_player_id = start_status.get_local_id()
        self.__board.players = players
        self.__board.local_player = local_player_id

    def prepare_current_move(self):
        if self.__board.local_player.turn:
            self.__board.update_board_position()
            self.__deck_button['state'] = 'normal'
            self.update_gui_message( "draw_card" )

    def receive_withdrawal_notification(self):
        self.__board.receive_withdrawal_notification()
        # self.update_gui(game_state)

    def receive_move(self, a_move):
        if a_move["game_status"] == 0:
            self.__board.start_game( a_move )
            self.set_positions()
            self.start_match_widget_packs()
            self.__board.match_status = 1
            print( self.__board.local_player )
        if a_move["game_status"] == 1:
            #
            self.prepare_current_move()

        self.update_widget_packs()

    # Fuction used to update interface elements.
    def update_widget_packs(self):
        # Destroy all widget from positions except type image.
        for position in self.__board.positions:
            position.widget.grid_propagate( False )
            if len( position.widget.winfo_children() ):
                for widget in position.widget.winfo_children()[1:]:
                    widget.destroy()

        player_row = 0
        player_column = 0
        for i in self.__board.players:
            player_image = PhotoImage( file=i.image )
            player_label = Label( self.__board.positions[i.position_board].widget, image=player_image, width=20,
                                  height=20 )
            player_label.grid( row=player_row, column=player_column, padx=1, pady=1 )
            player_label.image = player_image
            player_column += 1
            if player_column >= 2:
                player_row += 1
                player_column = 0

        # Frame that shows current player.
        for i in self.__current_turn.winfo_children():
            i.configure( text=f'Turno do Jogador: {self.__board.current_player_turn.name}.' )
        # Logs block
        self.__logs_frame.grid( row=1, column=0, padx=5, pady=5 )
        self.__logs_listbox.pack( fill='both', expand=True )
        self.__deck_frame.grid( row=0, column=1, rowspan=2, padx=5, pady=5 )
        self.__deck_button.grid( row=0, column=0 )

    # Function that load all wigets in interface when a match has started.
    def start_match_widget_packs(self):
        # Frame that holds all positions.
        self.__board_positions_frame.grid( row=0, column=0, sticky="ew" )
        # Frame that hold frames players hud (logs, deck, and current player).
        self.__hud_frame.grid( row=2, sticky="ew" )

        self.__current_turn.grid( row=0, column=0, padx=5, pady=5, sticky='ew' )
        current_turn_label = Label( self.__current_turn,
                                    text=f'Turno do Jogador: {self.__board.current_player_turn.name}.',
                                    fg='white', background='#d95f57',
                                    font=24 )

        # Create a label widget to board positions.
        row = 0
        column = 0
        reverse = False
        for position in self.__board.positions:
            position.widget.grid( column=column, row=row, pady=5, padx=5 )
            position.widget.label.pack_propagate( False )
            if (reverse and column == 0) or (not reverse and column == 9):
                if row % 2 == 1:
                    reverse = not reverse
                row += 1
            else:
                column += -1 if reverse else 1

        # Create label for players.
        for i in self.__board.players:
            player_image = PhotoImage( file=i.image )
            player_label = Label( self.__board.positions[i.position_board].widget, image=player_image, width=20,
                                  height=20 )
            player_label.grid( row=row, column=column, padx=1, pady=1 )
            player_label.image = player_image
            column += 1
            if column >= 2:
                row += 1
                column = 0

        # Propagate.
        self.__board_frame.pack_propagate( False )
        self.__hud_frame.grid_propagate( False )
        self.__current_turn.pack_propagate( False )
        self.__logs_frame.pack_propagate( False )

        current_turn_label.pack( fill="both", expand=True, padx=5, pady=5 )
        self.__logs_frame.grid( row=1, column=0, padx=5, pady=5 )
        self.__logs_listbox.pack( fill='both', expand=True )
        self.__deck_frame.grid( row=0, column=1, rowspan=2, padx=5, pady=5 )
        self.__deck_button.grid( row=0, column=0 )

        # Set game state to Waiting player move.
        self.__board.match_status = 1
