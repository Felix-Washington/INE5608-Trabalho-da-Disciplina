import os
import random
from tkinter import *
from tkinter import messagebox, simpledialog

from PIL import Image, ImageTk

from board import Board
from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface


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

        # Connection with DOG.
        self.dog_server_interface = DogActor()
        player_name = simpledialog.askstring( title="Player identification", prompt="Qual o seu nome?" )
        message = self.dog_server_interface.initialize( player_name, self )
        messagebox.showinfo( message=message )

        self.__root.mainloop()

        self.__root.deiconify()

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

    # Call DOG to try start the match.
    def start_match(self):
        start_status = self.dog_server_interface.start_match( 2 )
        code = start_status.get_code()
        message = start_status.get_message()

        if code == "0" or code == "1":
            messagebox.showinfo( message=message )
        else:  # (code=='2')
            players_id = start_status.get_players()
            local_player_id = start_status.get_local_id()
            self.__board.start_match( players_id, local_player_id )
            messagebox.showinfo( message=start_status.get_message() )

            self.set_positions()
            self.start_match_widget_packs()

            # Send first move to all players.
            self.dog_server_interface.send_move( self.__board.get_start_match_data() )

            self.__board.game_status = 1
            if self.__board.current_local_player:
                self.__deck_button['state'] = 'normal'
            self.update_widget_packs()

    def update_card_interface(self, state):
        self.update_gui_message( state )
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

        # Update card title text base on card type.
        card_title_text = ""
        card_option_type = ""

        if state == "create_questions":
            self.__deck_button['state'] = 'disabled'
            card_title_text = "Escolha uma pergunta!"
            card_option_type = "create_answers"
        elif state == "create_answers":
            card_title_text = self.__board.deck.get_card_option_text( "question_title" )
            card_option_type = "selected_an_answer"
        elif state == "create_players":
            card_title_text = "Escolha um jogador!"
            card_option_type = "selected_a_player"

        card_frame = Frame( card_interface, background='#ffbd59' )
        # Create Label with card title text.
        card_title = Label( card_interface, text=card_title_text, width=300, height=8 )

        # Load all options available for card and draw on the inferface.
        for option in card.options:
            card_option = Button(
                card_frame,
                text=self.__board.get_card_information( state, option ),
                command=lambda key=option: [self.draw_and_select( card_option_type, key ), card_interface.destroy()],
                width=300, height=2, font=('Arial', 12) )
            card_option.pack( padx=10, pady=10 )

        card_title.pack( padx=10, pady=10 )
        card_frame.pack( padx=10, pady=10 )

        card_interface.focus()
        card_interface.grab_set()
        card_interface.protocol( "WM_DELETE_WINDOW", lambda: card_interface.destroy() )

    # Function called to process card interface.
    def draw_and_select(self, state, selected_options=-1):
        state = self.__board.check_board_status( state, selected_options )
        move = self.__board.get_move_to_send()
        self.dog_server_interface.send_move( move )

        if state:
            self.update_card_interface( state )

    # Insert game status to interface log list.
    def update_gui_message(self, state):
        message = self.__board.get_logs_message( state )
        if message != "":
            self.__logs_listbox.insert( 0, message )
            self.__logs_listbox.yview( 0 )

    def receive_start(self, start_status):
        self.__board.receive_start( start_status )

    def receive_withdrawal_notification(self):
        messagebox.showinfo( message=f"player {self.__board.local_player.name} disconected" )
        self.__board.receive_withdrawal_notification()
        # self.update_gui(game_state)

    def receive_move(self, received_data):
        # Used only when match has started.
        if received_data["game_status"] == 0:
            self.__board.remote_start_match( received_data )
            self.set_positions()
            self.start_match_widget_packs()
        else:
            self.__board.update_received_data( received_data )

        if self.__board.game_status == 1:
            self.__board.update_current_local_player()

        # Check if a temporary turn has been finished
        if self.__board.game_status == 4:
            # and self.__board.current_local_player:
            self.__board.game_status = 2
            self.draw_and_select("")

        elif self.__board.current_local_player:
            print("release deck button","current",self.__board.current_player.name,"local", self.__board.local_player.name)
            self.__board.game_status = 1
            self.__deck_button['state'] = 'normal'

        # 3 - Game status: temporary turn.
        elif self.__board.game_status == 3:
            if self.__board.local_player.turn:
                self.draw_and_select( "create_answers", self.__board.local_player.selected_question )

        self.update_widget_packs()

    # Fuction used to update interface elements.
    def update_widget_packs(self):
        # Destroy all widgets from positions except type image.
        for position in self.__board.positions:
            position.widget.grid_propagate( False )
            if len( position.widget.winfo_children() ):
                for widget in position.widget.winfo_children()[1:]:
                    widget.destroy()

        player_row = 0
        player_column = 0
        for player in self.__board.players:
            player_image = PhotoImage( file=player.image )
            player_label = Label( self.__board.positions[player.position_board].widget, image=player_image, width=20,
                                  height=20 )
            player_label.grid( row=player_row, column=player_column, padx=1, pady=1 )
            player_label.image = player_image
            player_column += 1
            if player_column >= 2:
                player_row += 1
                player_column = 0

        # Frame that shows current player.
        for i in self.__current_turn.winfo_children():
            if self.__board.current_local_player:
                i.configure( text='Jogador da vez: Você.', background='#90EE90', bg='#90EE90' )
            else:
                i.configure( text=f'Jogador da vez: {self.__board.current_player.name}.', background="#d95f57",
                             bg='#d95f57' )
        # Logs block
        self.__logs_frame.grid( row=1, column=0, padx=5, pady=5 )
        # self.__logs_listbox.pack( fill='both', expand=True )
        self.__deck_frame.grid( row=0, column=1, rowspan=2, padx=5, pady=5 )
        self.__deck_button.grid( row=0, column=0 )

    # Function that load all wigets in interface when a match has started.
    def start_match_widget_packs(self):
        # Propagate.
        self.__board_frame.pack_propagate( False )
        self.__hud_frame.grid_propagate( False )
        self.__current_turn.pack_propagate( False )
        self.__logs_frame.grid_propagate( False )

        # Frame that holds all positions.
        self.__board_positions_frame.grid( row=0, column=0, sticky="ew" )
        # Frame that hold frames players hud (logs, deck, and current player).
        self.__hud_frame.grid( row=2, sticky="ew" )

        self.__current_turn.grid( row=0, column=0, padx=5, pady=5, sticky='ew' )
        current_turn_label = Label( self.__current_turn,
                                    text=f'Turno do Jogador: {self.__board.current_player.name}.',
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
        for player in self.__board.players:
            player_image = PhotoImage( file=player.image )
            player_label = Label( self.__board.positions[player.position_board].widget, image=player_image, width=20,
                                  height=20 )
            player_label.grid( row=row, column=column, padx=1, pady=1 )
            player_label.image = player_image
            column += 1
            if column >= 2:
                row += 1
                column = 0

        current_turn_label.pack( fill="both", expand=True, padx=5, pady=5 )
        self.__logs_frame.grid( row=1, column=0, padx=5, pady=5 )
        self.__logs_listbox.pack( fill='both', expand=True )
        self.__deck_frame.grid( row=0, column=1, rowspan=2, padx=5, pady=5 )
        self.__deck_button.grid( row=0, column=0 )

    # Set labels to all positions.
    def set_positions(self):
        for i in range( len( self.__board.positions ) ):
            position_size = self.__game_size[0] / 10 - 15

            # Get position image path.
            image_path = self.__board.positions[i].image

            # Create position Frame.
            position_frame = Frame( self.__board_positions_frame, width=position_size, height=position_size )
            position_frame.pack_propagate( False )  # Prevent frame size auto adjust

            # Load position image.
            position_frame.picture = PhotoImage( file=image_path )  # Relative path for the image
            position_frame.label = Label( position_frame, image=position_frame.picture )

            # Add Label to Frame.
            position_frame.label.pack( fill='both', expand=True )  # Pack to fill Frame with the Label

            #  Frame Settings.
            position_frame.configure( width=position_size, height=position_size )

            # Saving frame in position widget.
            self.__board.positions[i].widget = position_frame

    def set_hud(self):
        # Show current player turn
        self.__current_turn = Frame( self.__hud_frame, width=400, height=100, bg="red" )
        # Game actions log frame.
        self.__logs_frame = Frame( self.__hud_frame, width=400, height=200, bg="gray" )
        # Game actions log widget.
        self.__logs_listbox = Listbox( self.__logs_frame, bg='lightgray', font=('Arial', 12), width=50 )
        # Deck
        self.__deck_frame = Frame( self.__hud_frame )
        # Button used to draw a card.
        self.__deck_button = Button( self.__deck_frame, width=15, height=13, text="?",
                                     command=lambda: [self.draw_and_select( "create_questions" )],
                                     bg='black', highlightthickness=2, font=48, fg='white', state='disabled' )

    # Create Menu item and add its buttons.
    def set_menu(self):
        self.__menubar = Menu( self.__root )
        self.__filemenu = Menu( self.__menubar, tearoff=0 )
        self.__filemenu.add_command( label="Iniciar partida", command=self.start_match )
        self.__filemenu.add_separator()
        self.__filemenu.add_command( label="Close", command=self.on_closing )

        self.__menubar.add_cascade( menu=self.__filemenu, label="File" )
        self.__root.config( menu=self.__menubar )

    # Config to close the window.
    def on_closing(self):
        self.__root.destroy()
