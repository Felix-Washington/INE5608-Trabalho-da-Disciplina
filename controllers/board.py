import random
from PIL import Image, ImageTk
from controllers.deck import deck

import tkinter as tk
from tkinter import messagebox


class board:
    def __init__(self, player_amount, deck_cards):
        self.__player_amount = player_amount
        self.__tile_amount = 5
        self.__positions = []

        # Root config
        self.__root = tk.Tk()
        self.__root.geometry("800x800")
        self.__root.title("Board")
        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Boards
        self.__board_frame = tk.Frame(self.__root, bg="blue", padx=30, pady=15, relief="sunken",borderwidth=2)

        self.__nav_bar = tk.Frame( self.__board_frame, bg="green", height=150, width=150)
        self.__board_positions = tk.Frame(self.__board_frame, bg="yellow", height=350, width=150,relief="sunken")
        self.__hud = tk.Frame(self.__board_frame, bg="red", height=150, width=150)

        self.__board_positions2 = tk.Frame(self.__board_positions, bg="yellow", height=350, width=150,relief="sunken")


        # Row and Column configs
        self.__board_frame.columnconfigure(0, weight=1)
        self.__board_frame.rowconfigure(0, weight=1)
        self.__board_frame.rowconfigure(1, weight=2)
        self.__board_frame.rowconfigure(2, weight=1)

        #self.__board_positions.rowconfigure(0, weight=1)
        self.__board_positions.columnconfigure(0, weight=2)
        self.__board_positions.columnconfigure(1, weight=1)


        # Others vars
        self.__check_state = tk.IntVar()
        self.__textbox = tk.Text(self.__nav_bar, height=2, width=50)
        self.__deck = tk.Button(self.__board_positions, text="Deck", width=30, height=10, command=self.show_message)
        self.__check = tk.Checkbutton(self.__hud, text="Show Message", variable=self.__check_state)
        self.__check.grid(pady=10)

        self.set_positions()
        self.widget_packs()

        # Menu vars
        self.__menubar = None
        self.__filemenu = None
        self.set_menu()

        # Frame propagate
        self.__board_frame.pack_propagate(False)
        self.__nav_bar.grid_propagate( False )
        self.__board_positions.grid_propagate( False )
        self.__hud.grid_propagate( False )

    def start(self):
        self.__root.mainloop()

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
            image = Image.open( "controllers/" + position_types[number] )
            photo = ImageTk.PhotoImage( image )

            position = tk.Label(self.__board_positions2, image=photo)
            position.image = photo
            # Bind and especific event for each position.
            position.bind( "<Button-1>", lambda event="", position_number=i: self.position_bind(event, position_number))

            self.__positions.append(position)

    def position_bind(self, event, a):
        print(self.__positions[a].image)

    def show_message(self):
        if self.__check_state.get() == 0:

            print(self.__textbox. get("1.0", tk.END))
        else:
            messagebox.showinfo(title="Message", message=self.__textbox.get("1.0", tk.END))

    def on_closing(self):
        self.__root.destroy()
        #if messagebox.askyesno(title="Quit", message="Wanna Quit?"):
        #    self.__root.destroy()

    def shortcut(self, event):
        if event.state == 12 and event.keysym == "Return":
            self.show_message()

    def set_menu(self):
        self.__menubar = tk.Menu(self.__root)
        self.__filemenu = tk.Menu(self.__menubar, tearoff=0)
        self.__filemenu.add_command(label="Close", command=self.on_closing)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Close wt question", command=exit)

        self.__menubar.add_cascade(menu=self.__filemenu, label="File")

        self.__root.config(menu=self.__menubar)

    def widget_packs(self):

        self.__board_frame.pack(fill="both", expand=True)
        self.__nav_bar.grid(row=0, column=0, sticky="ew")
        self.__board_positions.grid(row=1, column=0, sticky="ew")
        self.__board_positions2.grid(row=1, column=0, sticky="ew")
        self.__hud.grid(row=2, column=0, sticky="ew")

        self.__deck.grid( column=1, sticky="NS" )
        self.__textbox.grid(padx=10)
        for i in range(len(self.__positions)):

            self.__positions[i].grid(column=i, row=0, pady=1)

