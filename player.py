import tkinter as tk
from config import *

class Player:
    def __init__(self, canvas, root, x=None, y=None):
        self.canvas = canvas
        self.root = root
        # Utiliser x et y fournis, sinon des valeurs par défaut
        if x is None:
            x = 50  # valeur par défaut
        if y is None:
            y = 300  # valeur par défaut
        # Création du joueur (ici un carré de 30x30 par exemple)
        self.cube = self.canvas.create_rectangle(x, y, x + 30, y + 30, fill="red")

        # Variables du joueur
        self.player_dx = 0
        self.player_dy = 0
        self.on_ground = False

    def move_left(self):
        self.player_dx = -SPEED

    def move_right(self):
        self.player_dx = SPEED

    def jump(self, event):
        if self.on_ground:
            self.player_dy = JUMP_STRENGTH
            self.on_ground = False
