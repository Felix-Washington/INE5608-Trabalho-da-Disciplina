# Tkinter Imports
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
#from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
#from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener
import os
import keyboard

from game_logic.view.frames import frames
from game_logic.controllers.deck import deck

# Project Imports
from game_logic.model.player import player

# Misc imports
import random

'''(PyNetgamesServerListener)'''
class board :
    def __init__(self):
        # Project attributes
        super().__init__()
        self.__tile_amount = 10
        self.__positions = []
        self.__players = []
        self.__winner = None
        self.__match_status = False
        self.__selected_player = -1
        self.__turn_control = -1
        self.__opponent_answered = False

        # Root config
        self.__root = tk.Tk()
        self.__root.geometry("800x800")
        self.__root.title("Board")
        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Board Frames
        self.__board_frame = tk.Frame(self.__root, bg="blue", padx=30, pady=15, relief="sunken", borderwidth=2)
        self.__nav_bar = tk.Frame( self.__board_frame, bg="green", height=150, width=150)
        self.__board_positions = tk.Frame(self.__board_frame, bg="pink", height=350, width=150, relief="sunken")
        self.__hud = tk.Frame(self.__board_frame, bg="red", height=150, width=150)

        # Frames - board_positions
        self.__board_positions2 = tk.Frame(self.__board_positions, bg="yellow", height=350, width=150, relief="sunken")
        # Frames - hud
        self.__hud_player_img = tk.Label(self.__hud, bg="pink", height=10, width=10)


        self.create_players()
        self.create_players()
        self.create_players()
        # Row and Column configs - Para: frame, amount (columns or rows), weight
        self.column_frame_configure(self.__board_frame, 1, [1])
        self.row_frame_configure(self.__board_frame, 3, [1, 2, 1])
        self.column_frame_configure(self.__board_positions, 2, [1,5])
        self.column_frame_configure(self.__hud, 2, [1, 2])

        # Others vars
        self.__check_state = tk.IntVar()
        self.__textbox = tk.Text(self.__nav_bar, height=2, width=50)
        self.__check = tk.Checkbutton(self.__hud, text="Show Message", variable=self.__check_state)
        self.__check.grid(pady=10)

        self.__deck = deck(self.__board_positions, self)

        # Menu vars
        self.__menubar = None
        self.__filemenu = None

        # Frame propagate
        self.__board_frame.pack_propagate(False)
        self.__nav_bar.grid_propagate( False )
        self.__board_positions.grid_propagate( False )
        self.__hud.grid_propagate( False )

        # Start functions
        self.set_menu()
        self.set_positions()
        self.widget_packs()

        #self.add_listener()
        #self.send_connect()


    def create_players(self, name="kid"):
        img = "images/"
        if len(self.__players) == 0:
            img += "kid_one.png"

        elif len( self.__players ) == 1:
            img += "kid_two.png"
        elif len( self.__players ) == 2:
            img += "kid_three.png"

        player_img = self.load_label_img(self.__hud_player_img, img)
        player1 = player(name, player_img)
        self.__players.append(player1)


    def show_card(self, frame):
        print(frame)
        self.__board_frame = tk.Frame(frame, bg="yellow", padx=30, pady=15, relief="sunken", borderwidth=2)
        self.__board_frame.pack()

    def board_loop(self):
        self.__root.mainloop()


    def row_frame_configure(self, frame, row_amount, weight: []):
        for i in range(row_amount):
            frame.rowconfigure(i, weight=weight[i])

    def column_frame_configure(self, frame: tk.Frame, column_amount: int, weight: []):
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

        for i in range(self.__tile_amount + 2):
            # If reached last position, set the final position of the board.
            if i != 0 and i <= self.__tile_amount:
                number = int( random.uniform( 1, 4 ) )
            elif i == 0:
                number = 0
            else:
                number = 0

            image_path = os.path.join(os.path.dirname(__file__), "../images/" + position_types[number])
            position = self.load_label_img(self.__board_positions2, image_path)
            # Bind and specify event for each position.
            position.bind( "<Button-1>", lambda event="", position_number=i: self.position_bind(event, position_number))
            self.__positions.append(position)

    def load_label_img(self, widget, path):
        image = Image.open(path)
        photo = ImageTk.PhotoImage( image )
        label = tk.Label( widget, image=photo )
        label.image = photo
        return label

    def position_bind(self, event, a):
        print(self.__positions[a].image , "teste")


    def show_message(self):
        if self.__check_state.get() == 0:
            print("Deck")
        else:
            print(self.__textbox.get("1.0", tk.END))

    def on_closing(self):
        #if messagebox.askyesno(title="Quit", message="Quer Sair?"):
            self.__root.destroy()

    def shortcut(self, event):
        if event.state == 12 and event.keysym == "Return":
            self.show_message()

    def set_menu(self):
        self.__menubar = tk.Menu(self.__root)
        self.__filemenu = tk.Menu(self.__menubar, tearoff=0)
        self.__filemenu.add_command(label="Procurar jogador")
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Close", command=self.on_closing)

        self.__menubar.add_cascade(menu=self.__filemenu, label="File")

        self.__root.config(menu=self.__menubar)

    def widget_packs(self):
        self.__board_frame.pack(fill="both", expand=True)
        self.__nav_bar.grid(row=0, sticky="ew")
        self.__board_positions.grid(row=1, sticky="ew")
        self.__hud.grid(row=2, sticky="ew")

        self.__board_positions2.grid(column=0, sticky="ew")
        self.__deck.grid( column=1, sticky="NS" )

        self.__hud_player_img.grid(column=0, sticky="NS" )

        self.__textbox.grid(column=1, padx=10)

        row = 0
        column = 0
        for i in range(len(self.__positions)):
            self.__positions[i].grid(column=column, row=row, pady=1)
            if column > 3:
                row += 1
                column = 0
            else:
                column += 1

        for i in range(len(self.__players)):
            self.__players[i].image.grid(row=0, column=i)


    # Pynetgames
    '''
    def add_listener(self):
        #self.server_proxy = PyNetgamesServerProxy()
        self.server_proxy.add_listener(self)

    def send_connect(self):
        self.server_proxy.send_connect("wss://py-netgames-server.fly.dev")

    def start_match(self):
        messagebox.showinfo(title="Message", message="Procurar Jogador")


    def send_match(self):
        self.server_proxy.send_match(2)

    def receive_connection_success(self):
        print("***************CONNECTED***************")
        self.send_match()

    def receive_disconnect(self):
        pass

    def receive_error(self, error):
        pass

    def receive_match(self, match):  # Pyng use case "receive match"
        print( '*************** START MATCH ***************' )
        print( '*************** ORDER: ', match.position )
        print( '*************** match_id: ', match.match_id )

    def receive_move(self, move):
        pass
    '''
