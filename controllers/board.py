# Tkinter Imports
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Project Imports
from controllers.deck import deck
from model.player import player

# Misc imports
import random


class board:
    def __init__(self, deck_card_amount):
        # Project attributes
        self.__tile_amount = 5
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
        self.__board_positions = tk.Frame(self.__board_frame, bg="yellow", height=350, width=150, relief="sunken")
        self.__hud = tk.Frame(self.__board_frame, bg="red", height=150, width=150)

        # Frames - board_positions
        self.__board_positions2 = tk.Frame(self.__board_positions, bg="yellow", height=350, width=150, relief="sunken")

        # Frames - hud
        self.__hud_player_img = tk.Label(self.__hud, bg="pink", height=10, width=10)
        player_img = self.load_label_img (self.__hud_player_img, "controllers/kid_one.png")

        self.__players.append(player_img)

        # Row and Column configs - Para: frame, amount (columns or rows), weight
        self.column_frame_configure(self.__board_frame, 1, [1])
        self.row_frame_configure(self.__board_frame, 3, [1, 2, 1])
        self.column_frame_configure(self.__board_positions, 2, [1, 2, 1])
        self.column_frame_configure(self.__hud, 2, [1, 2])

        # Others vars
        self.__check_state = tk.IntVar()
        self.__textbox = tk.Text(self.__nav_bar, height=2, width=50)
        self.__deck = tk.Button(self.__board_positions, text="Deck", width=30, height=10, command=self.show_message)
        self.__check = tk.Checkbutton(self.__hud, text="Show Message", variable=self.__check_state)
        self.__check.grid(pady=10)

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

        for i in range(self.__tile_amount):
            # If reached last position, set the final position of the board.
            if i == self.__tile_amount - 1:
                number = 0
            else:
                number = int(random.uniform(1, 4))

            position = self.load_label_img(self.__board_positions2, "controllers/" + position_types[number])
            # Bind and especific event for each position.
            position.bind( "<Button-1>", lambda event="", position_number=i: self.position_bind(event, position_number))

            self.__positions.append(position)

    def load_label_img(self, widget, path):
        image = Image.open(path)
        photo = ImageTk.PhotoImage( image )
        label = tk.Label( widget, image=photo )
        label.image = photo
        return label

    def position_bind(self, event, a):
        print(self.__positions[a].image)

    def show_message(self):
        if self.__check_state.get() == 0:
            print("Deck")
        else:
            print(self.__textbox.get("1.0", tk.END))

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="Quer Sair?"):
            self.__root.destroy()

    def shortcut(self, event):
        if event.state == 12 and event.keysym == "Return":
            self.show_message()

    def set_menu(self):
        self.__menubar = tk.Menu(self.__root)
        self.__filemenu = tk.Menu(self.__menubar, tearoff=0)
        self.__filemenu.add_command(label="Procurar jogador", command=self.start_match)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Close", command=self.on_closing)

        self.__menubar.add_cascade(menu=self.__filemenu, label="File")

        self.__root.config(menu=self.__menubar)

    def start_match(self):
        messagebox.showinfo(title="Message", message="Procurar Jogador")

    def widget_packs(self):
        self.__board_frame.pack(fill="both", expand=True)
        self.__nav_bar.grid(row=0, column=0, sticky="ew")
        self.__board_positions.grid(row=1, column=0, sticky="ew")
        self.__board_positions2.grid(row=1, column=0, sticky="ew")
        self.__hud.grid(row=2, column=0, sticky="ew")

        self.__deck.grid( column=1, sticky="NS" )
        self.__hud_player_img.grid(column=0, sticky="NS" )

        self.__textbox.grid(column=1, padx=10)
        for i in range(len(self.__positions)):
            self.__positions[i].grid(column=i, row=0, pady=1)

        self.__players[0].grid(column=0)
