import os
import random
from tkinter import *
from tkinter import messagebox, simpledialog

from board import Board
from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface


def row_column_frame_configure(frame: Frame, value_amount, weight, is_column):
    if is_column:
        for i in range( value_amount ):
            frame.columnconfigure( i, weight=weight[i] )
    else:
        for i in range( value_amount ):
            frame.rowconfigure( i, weight=weight[i] )


class PlayerInterface( DogPlayerInterface ):
    def __init__(self):
        super().__init__()
        # Root config.
        self.__root = Tk()

        # Window size and position.
        self.__game_size = [int( self.__root.winfo_screenwidth() / 2 ), 800]
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

        # Connection with DOG.
        self.dog_server_interface = DogActor()
        player_name = simpledialog.askstring( title="Player identification", prompt="Qual o seu nome?" )
        message = self.dog_server_interface.initialize( player_name, self )
        messagebox.showinfo( message=message )

        # Prevent main windows from minimize.
        self.__root.deiconify()

        self.__players_qtd = 3

    def load_main_window(self):
        # Configuration of game window.
        self.__root.geometry( f"{self.__game_size[0]}x{self.__game_size[1]}+{self.__game_pos_x}+{self.__game_pos_y}" )
        self.__root.title( "Certo ou Errado" )
        self.__root.protocol( "WM_DELETE_WINDOW", self.__root.destroy )
        self.__root.resizable( False, False )

        # Board Frames.
        board_color = "lightblue"
        self.__board_frame = Frame( self.__root, padx=20, bg=board_color )
        self.__board_positions_frame = Frame( self.__board_frame, bg=board_color )

        # Row and Column configs - Parameters: frame, amount (columns or rows), weight, True = column / False = row
        row_column_frame_configure( self.__board_frame, 1, [1], True )
        row_column_frame_configure( self.__board_frame, 3, [1, 2, 1], False )

        self.set_hud()
        self.set_menu()
        # Board that holds entire screen.
        self.__board_frame.pack( fill="both", expand=True )

    # Call DOG to try start the match.
    def start_match(self):
        start_status = self.dog_server_interface.start_match( self.__players_qtd)
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

            move = self.__board.get_start_match_data()
            # Send first move to all players.
            self.dog_server_interface.send_move( move )

            self.__board.game_status = 1
            if self.__board.current_local_player:
                self.__deck_button['state'] = 'normal'
            self.update_widget_packs()

    def update_card_interface(self, state):
        def no_close():
            return

        # Create window popup for the card.
        card_interface = Toplevel()
        card_interface.protocol( "WM_DELETE_WINDOW", no_close )
        card_interface.title( "Carta" )

        card = self.__board.deck.card

        # Get x and y position of the card.
        card_width_pos = int( (self.__root.winfo_x() + self.__game_size[0] / 2) - (card.width / 2) )
        card_height_pos = int( self.__root.winfo_y() )

        # Set card window position and size.
        card_interface.geometry( f'{card.width}x{card.height}+{card_width_pos}+{card_height_pos}' )
        card_interface.resizable( width=False, height=False )
        card_interface.configure( background='#ffbd59' )

        # Update card title text base on card type.
        card_title_text = ""
        card_option_type = ""

        if state == "create_questions":
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

        card_title.pack()
        card_frame.pack()

        card_interface.focus()
        card_interface.grab_set()

    # Function called to process card interface.
    def draw_and_select(self, state, selected_options=-1):
        self.__deck_button['state'] = 'disabled'
        state = self.__board.check_board_status( state, selected_options )
        move = self.__board.get_move_to_send( state )
        self.dog_server_interface.send_move( move )

        self.update_gui_message( state )
        self.update_widget_packs()

        if state == "game_end":
            message = self.__board.get_winners_message()
            messagebox.showinfo( message=message )
        elif state:
            self.update_card_interface( state )

    # Insert game status to interface log list.
    def update_gui_message(self, state):
        message = self.__board.get_logs_message( state )
        if message != "":
            self.__logs_listbox.insert( 0, message )
            self.__logs_listbox.yview( 0 )

    def receive_start(self, start_status):
        local_player_id = start_status.get_local_id()
        self.__board.receive_start( local_player_id )

    def receive_withdrawal_notification(self):
        self.__board.game_status = 6
        self.update_gui_message( "" )
        messagebox.showinfo( message="Um jogador foi desconectado." )

    def receive_move(self, received_data):
        # Used only when match has started.
        if received_data["game_status"] == 0:
            self.__board.remote_start_match( received_data )
            self.set_positions()
            self.start_match_widget_packs()
        else:
            self.__board.update_received_data( received_data )

        state = self.__board.process_receive_move()

        if state == "reset_play":
            self.draw_and_select( "" )
        elif state == "release_deck":
            self.__deck_button['state'] = 'normal'
        elif state == "create_answers":
            self.draw_and_select( state, self.__board.local_player.selected_question )

        self.update_gui_message( received_data['state'] )
        self.update_widget_packs()

        if state == "game_end":
            messagebox.showinfo( message=self.__board.get_winners_message() )

    # Fuction used to update interface elements.
    def update_widget_packs(self):
        # Destroy all widgets from positions except type image.
        for position in self.__board.positions:
            position.widget.grid_propagate( False )
            if len( position.widget.winfo_children() ):
                for widget in position.widget.winfo_children()[1:]:
                    widget.destroy()

        row = 0
        column = 0
        for player in self.__board.players:
            player_image = PhotoImage( file=player.image )
            player_label = Label( self.__board.positions[player.position_board].widget, image=player_image, width=50,
                                  height=50 )
            player_label.image = player_image
            player_label.grid( row=row, column=column, padx=1, pady=1 )
            column += 1
            if column >= 2:
                row += 1
                column = 0

        # Frame that shows current player.
        player_image = PhotoImage( file=self.__board.get_current_player_data( "image" ) )
        player_label = Label( self.__current_turn, image=player_image, width=40, height=40 )
        for i in self.__current_turn.winfo_children():
            if self.__board.current_local_player:
                i.configure( text='Jogador da vez: Você.', background='#90EE90', bg='#90EE90' )
            else:
                i.configure( text=f'Jogador da vez: {self.__board.get_current_player_data( "name" )}.',
                             background="#d95f57",
                             bg='#d95f57' )
            player_label.grid( row=2, column=2, padx=1, pady=1 )
            player_label.image = player_image
        # Logs block
        self.__logs_frame.grid( row=1, column=0, padx=5, pady=5 )
        self.__deck_frame.grid( row=0, column=1, rowspan=2, padx=5, pady=5 )
        self.__deck_button.grid( row=0, column=0 )

    # Function that load all wigets in interface when a match has started.
    def start_match_widget_packs(self):
        # Propagate.
        self.__board_frame.pack_propagate( False )

        # Frame that holds all positions.
        self.__board_positions_frame.grid( row=0, column=0, sticky="ew" )

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

        # Frame that hold frames players hud (logs, deck, and current player).
        self.__hud_frame.grid( row=1, column=0, padx=5, pady=5, sticky='ew' )

        self.__current_turn.grid( row=0, column=0, sticky='ew' )
        current_turn_label = Label( self.__current_turn,
                                    text=f'Turno do Jogador: {self.__board.get_current_player_data( "name" )}.',
                                    fg='white', font=24 )

        current_turn_label.pack( fill="both", expand=True, padx=5, pady=5 )
        self.__logs_frame.grid( row=1, column=0, padx=5, pady=5 )
        self.__logs_listbox.pack( fill='both', expand=True )
        self.__deck_frame.grid( row=0, column=1, rowspan=2, padx=5, pady=5 )
        self.__deck_button.grid( row=0, column=0 )

        # Create images to identify players.
        players_frame = Frame( self.__board_frame, width=150, height=50, pady=10, background="lightblue" )
        players_frame.grid( row=3, column=0 )
        column = 0
        players_frame_title = Label( players_frame, text="Jogadores" )
        players_frame_title.grid( row=0, column=0, columnspan=self.__players_qtd )
        for player in self.__board.players:
            player_image = PhotoImage( file=player.image )
            player_label = Label( players_frame, image=player_image, width=50, height=50 )
            player_label.grid( row=1, column=column, padx=1, pady=1 )
            if player.identifier == self.__board.local_player.identifier:
                player_label_name = Label( players_frame, text="Você", background='lightblue' )
            else:
                player_label_name = Label( players_frame, text=player.name, background='lightblue' )

            player_label_name.grid( row=2, column=column, padx=5, pady=1 )
            player_label.image = player_image
            column += 1

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
        self.__hud_frame = Frame( self.__board_frame, height=(self.__game_size[1] / 2) - 100, bg="lightblue" )
        row_column_frame_configure( self.__hud_frame, 2, [1, 2], True )

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

        self.__hud_frame.grid_propagate( False )
        self.__current_turn.pack_propagate( False )
        self.__logs_frame.grid_propagate( False )

    # Create Menu item and add its buttons.
    def set_menu(self):
        self.__menubar = Menu( self.__root )
        self.__filemenu = Menu( self.__menubar, tearoff=0 )
        self.__filemenu.add_command( label="Iniciar partida", command=self.start_match )

        self.__menubar.add_cascade( menu=self.__filemenu, label="File" )
        self.__root.config( menu=self.__menubar )

    def board_loop(self):
        self.__root.mainloop()
