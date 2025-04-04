import tkinter as tk
from config import *
import math

class Trap:
    def __init__(self, canvas, x, y, color="black"):
        trap_size = OBJECT_SIZE / 2
        x1, y1 = x * CELL_SIZE, y * CELL_SIZE
        x2, y2 = x1 + trap_size, y1 + trap_size

        self.canvas = canvas
        self.trap = canvas.create_oval(x1, y1, x2, y2, fill=color)

        # Calcul du centre et du rayon
        self.center_x = (x1 + x2) / 2
        self.center_y = (y1 + y2) / 2
        self.radius = trap_size / 2

    def get_coords(self):
        return self.center_x, self.center_y, self.radius

    def check_collision(self, player_x, player_y, player_width, player_height):
        player_center_x = player_x + player_width / 2
        player_center_y = player_y + player_height / 2

        # Calcul de la distance entre le joueur et le piège
        distance = math.sqrt((player_center_x - self.center_x) ** 2 + (player_center_y - self.center_y) ** 2)

        # Collision si la distance est inférieure au rayon + moitié de la taille du joueur
        return distance < (self.radius + max(player_width, player_height) / 2)

class Saw(Trap):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, color="gray")

class Grindur(Trap):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, color="teal")

class Bomb(Trap):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, color="black")
