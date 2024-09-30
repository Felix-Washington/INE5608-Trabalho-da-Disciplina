from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # type: ignore
import os


def row_frame_configure(frame, row_amount, weight):
    for i in range( row_amount ):
        frame.rowconfigure( i, weight=weight[i] )


def column_frame_configure(frame: Frame, column_amount: int, weight):
    for i in range( column_amount ):
        frame.columnconfigure( i, weight=weight[i] )


class PlayerInterface:
    def __init__(self):
        super().__init__()
        # Root config
        self.__root = Tk()

        # Window size and position
        self.__game_size = [int( self.__root.winfo_screenwidth() / 3 ), 800]
        self.__game_pos_x = int( self.__root.winfo_screenwidth() / 2 - self.__game_size[0] / 2 )
        self.__game_pos_y = int( self.__root.winfo_screenheight() / 2 - self.__game_size[1] / 2 )

        self.__board_frame, self.__board_positions, self.__hud = None, None, None
        # Hud frames
        self.__current_turn, self.__logs = None, None
        # Menus
        self.__menubar, self.__filemenu = None, None
        self.__logs_label = None
        self.__deck = None
        self.__deck_button = None
        self.__players = [0, 1]
        self.__local_player =  None

        self.load_main_window()

        # Prevent main windows from minimize
        self.__root.deiconify()

        self.__questions = {
            0: 'Qual a cor do céu?',
            1: 'Qual a cor da luz que reflete todas as cores?',
            2: 'Qual a cor do sol?',
            3: 'Qual é a cor que representa elegância e luto?'}

        self.__answers = {
            0: "Azul", 1: "Branco", 2: "Amarelo", 3: "Preto"}

        self.__questions_with_answers = {
            0: 0,  # Qual a cor do céu? -> Azul
            1: 1,  # Qual a cor da luz que reflete todas as cores? -> Branco
            2: 2,  # Qual a cor do sol? -> Amarelo
            3: 3,  # Qual é a cor que representa elegância e luto? -> Preto
        }
        '''
        path = os.path.join( os.path.dirname( __file__ ), "../src/images/kid_0.png" )
        photo = ImageTk.PhotoImage( Image.open( path ) )
        label = Label( self.__board_positions[0], image=photo )
        label.image = photo

        self.__players[0] = label
        '''

    def load_main_window(self):

        self.__root.geometry( f"{self.__game_size[0]}x{self.__game_size[1]}+{self.__game_pos_x}+{self.__game_pos_y}" )
        self.__root.title( "Tabuleiro" )
        self.__root.protocol( "WM_DELETE_WINDOW", self.on_closing )

        self.__root.resizable( False, False )

        # Board Frames
        board_color = "lightblue"
        self.__board_frame = Frame( self.__root, padx=20, bg=board_color )
        self.__board_positions = Frame( self.__board_frame, bg=board_color )
        self.__hud = Frame( self.__board_frame, height=(self.__game_size[1] / 2) - 100, bg=board_color )

        # Row and Column configs - Para: frame, amount (columns or rows), weight
        column_frame_configure( self.__board_frame, 1, [1] )
        row_frame_configure( self.__board_frame, 3, [1, 2, 1] )
        column_frame_configure( self.__hud, 2, [1, 2] )

        self.set_positions()
        self.set_hud()
        self.set_menu()
        self.widget_packs()

    def create_answers(self, key):
        answer = [self.__questions[key], self.__answers[key]]
        self.create_card( answer, "answers" )

    def create_card(self, answer=None, state="questions"):
        card_interface = Toplevel()
        card_interface.title( "Carta" )

        def end_card(button_):
            button_['state'] = 'normal'
            card_interface.destroy()

        card_width_pos = int( self.__game_pos_x + self.__game_pos_x / 2 - 200 )
        card_height_pos = int( self.__game_pos_y + self.__game_pos_y / 2 )

        card_interface.geometry( f'{400}x{600}+{card_width_pos}+{card_height_pos}' )
        card_interface.resizable( width=False, height=False )

        if state == "questions":
            card_interface.configure( background='#ffbd59' )
            card_frame = Frame( card_interface, background='#ffbd59' )
            card_title = Label( card_interface, text='Escolha uma pergunta', width=300, height=8 )
            self.__deck_button['state'] = 'disabled'
            for key, question in self.__questions.items():
                question_button = Button(
                    card_frame,
                    text='?',
                    command=lambda key=key: [self.set_message( 'Jogador escolheu uma pergunta' ),
                                             self.create_answers( key ), card_interface.destroy()],
                    width=300,
                    height=2,
                    font=('Arial', 12)
                )
                question_button.pack( padx=10, pady=20 )
        else:
            card_interface.configure( background='#7ed957' )
            card_frame = Frame( card_interface, bg='#7ed957' )

            card_title = Label( card_interface, text=answer[0], width=300, height=8 )
            for answer in self.__answers:
                answer_button = Button(
                    card_frame,
                    text=self.__answers[answer],
                    command=lambda: [self.set_message( 'Jogador respondeu a pergunta' ), self.select_player(),
                                     end_card( self.__deck_button )], width=300, height=2, font=('Arial', 12) )
                answer_button.pack( padx=10, pady=20 )

        card_title.pack( padx=10, pady=20 )
        card_frame.pack( padx=10, pady=10 )

        card_interface.focus()
        card_interface.grab_set()
        card_interface.protocol( "WM_DELETE_WINDOW", lambda: end_card( self.__deck_button ) )

    def select_player(self):
        players_interface = Toplevel()
        players_interface.title( "Jogadores" )
        players_frame = Frame( players_interface, background='#ffbd59' )
        players_frame_title = Label( players_interface, text='Escolha um jogador', width=300, height=8 )

        def end_card():
            players_interface.destroy()

        players_interface_width_pos = int( self.__game_pos_x + self.__game_pos_x / 2 - 200 )
        players_interface_height_pos = int( self.__game_pos_y + self.__game_pos_y / 2 )

        players_interface.geometry( f'{400}x{600}+{players_interface_width_pos}+{players_interface_height_pos}' )
        players_interface.resizable( width=False, height=False )

        path = os.path.join( os.path.dirname( __file__ ), "../src/images/kid_0.png" )
        photo = ImageTk.PhotoImage( Image.open( path ) )
        label = Label( players_interface, image=photo )
        label.image = photo

        self.__players[0] = label

        path = os.path.join( os.path.dirname( __file__ ), "../src/images/kid_1.png" )
        photo = ImageTk.PhotoImage( Image.open( path ) )
        label = Label( players_interface, image=photo )
        label.image = photo

        self.__players[1] = label

        self.__players[0].bind( "<Button-1>",
                                lambda event="": [self.set_message( 'Jogador 0 selecionado!' ), end_card()] )
        self.__players[1].bind( "<Button-1>",
                                lambda event="": [self.set_message( 'Jogador 1 selecionado!' ), end_card()] )

        players_frame_title.pack( padx=10, pady=20 )
        self.__players[0].pack( padx=10, pady=20 )
        self.__players[1].pack( padx=10, pady=20 )

        players_frame.pack( padx=10, pady=20 )
        players_interface.focus()
        players_interface.grab_set()
        players_interface.protocol( "WM_DELETE_WINDOW", lambda: end_card() )

    def board_loop(self):
        self.__root.mainloop()

    # Set labels to all positions
    def set_positions(self):
        row = 0
        column = 0
        reverse = False
        position_size = self.__game_size[0] / 10 - 20

        positions_list = []
        for i in range( 30 ):
            position_frame = Frame( self.__board_positions, bg='white', width=position_size, height=position_size )
            position_frame.grid( column=column, row=row, pady=5, padx=5 )
            position_frame.pack_propagate( False )
            position_label = Label( position_frame, text=f'{i}', font=24, fg='black' )
            position_label.pack( padx=5, pady=5, fill='both', expand=True )
            if (reverse and column == 0) or (not reverse and column == 9):
                if row % 2 == 1:
                    reverse = not reverse
                row += 1
            else:
                column += -1 if reverse else 1
            positions_list.append( position_frame )

        positions_list[0].grid_propagate( False )

        path = os.path.join( os.path.dirname( __file__ ), "../src/images/kid_0.png" )
        photo = ImageTk.PhotoImage( Image.open( path ) )
        label = Label( positions_list[0], image=photo )
        label.image = photo

        self.__players[0] = label
        self.__players[0].grid( column=0, row=0, padx=3 )

        path = os.path.join( os.path.dirname( __file__ ), "../src/images/kid_1.png" )
        photo = ImageTk.PhotoImage( Image.open( path ) )
        label = Label( positions_list[0], image=photo )
        label.image = photo

        self.__players[1] = label
        self.__players[1].grid( column=1, row=0, padx=3 )

        path = os.path.join( os.path.dirname( __file__ ), "../src/images/kid_2.png" )
        photo = ImageTk.PhotoImage( Image.open( path ) )
        label = Label( positions_list[0], image=photo )
        label.image = photo

        self.__local_player = label
        self.__local_player.grid( column=0, row=1, padx=3 , pady=3 )

        size = 20
        self.__players[0].configure( width=size, height=size )
        self.__players[1].configure( width=size, height=size )
        self.__local_player.configure( width=size, height=size )

    def set_hud(self):
        # Show current player turn
        self.__current_turn = Frame( self.__hud, width=400, height=100, bg="#d95f57" )
        # Game log
        self.__logs = Frame( self.__hud, width=400, height=200, bg="lightgray" )

        # Deck
        self.__deck = Frame( self.__hud )
        self.__deck_button = Button( self.__deck, width=15, height=13, text="?",
                                     command=lambda: [self.set_message( 'Jogador comprou uma carta' ),
                                                      self.create_card()],
                                     bg='black', highlightthickness=2, font=48, fg='white' )
        self.__deck_button.grid( row=0, column=0 )

    def on_closing(self):
        self.__root.destroy()

    def set_menu(self):
        self.__menubar = Menu( self.__root )
        self.__filemenu = Menu( self.__menubar, tearoff=0 )
        self.__filemenu.add_command( label="Start Match",
                                     command=lambda: self.set_message( 'Requisição de inicio de partida' ) )
        self.__filemenu.add_separator()
        self.__filemenu.add_command( label="Close", command=self.on_closing )

        self.__menubar.add_cascade( menu=self.__filemenu, label="File" )
        self.__root.config( menu=self.__menubar )

    def widget_packs(self):
        self.__board_frame.pack( fill="both", expand=True )
        self.__board_positions.grid( row=0, column=0, sticky="ew" )
        self.__hud.grid( row=2, sticky="ew" )

        # Propagate
        self.__board_frame.pack_propagate( False )
        self.__hud.grid_propagate( False )

        self.__current_turn.grid( row=0, column=0, padx=5, pady=5, sticky='ew' )
        self.__current_turn.pack_propagate( False )
        current_turn_label = Label( self.__current_turn, text='Turno do Jogador: ', fg='white', background='#d95f57',
                                    font=24 )
        current_turn_label.pack( fill="both", expand=True, padx=5, pady=5 )

        self.__logs.grid( row=1, column=0, padx=5, pady=5 )
        self.__logs.pack_propagate( False )
        self.__logs_label = Label( self.__logs, text='Compre uma carta e escolha uma pergunta', fg='black',
                                   background='lightgray', font=('Arial', 14) )
        self.__logs_label.pack( fill='both', expand=True, padx=5, pady=5 )

        self.__deck.grid( row=0, column=1, rowspan=2, padx=5, pady=5 )

    def set_message(self, message):
        messagebox.showinfo( message=message )
        self.__logs_label.configure( text=message )


PlayerInterface().board_loop()
