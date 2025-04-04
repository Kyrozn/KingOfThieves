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
        self.player_dx = 0.0
        self.player_dy = 0.0
        self.Right_Movement = True
        self.player_wall_slide = False
        self.on_ground = False
        self.lifeRemaining = 3
        self.root.bind("<space>", self.jump)
        self.ActionNb = 0
        self.jumpPos: list[tuple] = []
        self.move_right()

    def move_left(self):
        self.player_dx = -SPEED

    def move_right(self):
        self.player_dx = SPEED

    def jump(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.cube)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        print(x1, x2)
        print(y1, y2)
        if self.on_ground:
            print("Centre du cube :", center_x, center_y)
            self.player_dy = JUMP_STRENGTH
            self.on_ground = False
        if self.player_wall_slide:
            print("Centre du cube :", center_x, center_y)
            self.player_dy = JUMP_STRENGTH
            self.on_ground = False
            self.Right_Movement = not self.Right_Movement
            self.player_wall_slide = False
        self.ActionNb+=1
        self.jumpPos.append((round(center_x, 1), round(center_y, 1)))
    def setposition(self, x, y):
        self.canvas.coords(self.cube, x,y,x+30,y+30)
        self.Right_Movement = True
        self.player_wall_slide = False
        self.on_ground = False
