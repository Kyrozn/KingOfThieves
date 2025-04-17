import tkinter as tk
from core.config import *
from game.game import Game
from utils.graph import *

class Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Menu")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightblue")
        self.canvas.pack()

        self.create_buttons()

    def create_buttons(self):
        btn1 = tk.Button(
            self.root, text="Player", command=self.start_player_mode, width=20, height=2
        )
        btn2 = tk.Button(
            self.root, text="AI", command=self.start_ai_mode, width=20, height=2
        )
        btn3 = tk.Button(
            self.root, text="Graph", command=self.start_graph, width=20, height=2
        )

        btn1.place(x=400, y=80)
        btn2.place(x=400, y=130)
        btn3.place(x=400, y=180)

    def start_player_mode(self):
        # Supprime les éléments du menu
        for widget in self.root.winfo_children():
            widget.destroy()

        # Démarre le jeu en mode joueur
        game = Game(self.root, "human")
        game.start_countdown()

    def start_ai_mode(self):
        # Supprime les éléments du menu
        for widget in self.root.winfo_children():
            widget.destroy()

        # Démarre le jeu en mode ia
        Game(self.root, "ai")

    def start_graph(self):
        # Supprime les éléments du menu
        for widget in self.root.winfo_children():
            widget.destroy()

        # Démarre le graphique avec back_to_menu_callback
        dataframe = DataLoader("file.csv").load_data()
        Plotter(self.root, dataframe, self.back_to_menu)

    def back_to_menu(self):
        # Remplacer l'interface actuelle par l'interface du menu principal
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("Game Menu")

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="lightblue")
        self.canvas.pack()

        self.create_buttons()
