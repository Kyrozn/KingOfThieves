import tkinter as tk
from core.config import *

class Chest:
    def __init__(self, canvas, x, y, width=2 * CELL_SIZE, height=CELL_SIZE):
        self.canvas = canvas
        # Convertir les indices de grille en pixels
        x1, y1 = x * CELL_SIZE, y * CELL_SIZE
        x2, y2 = x1 + width, y1 + height
        # Création du coffre (base)
        self.box = self.canvas.create_rectangle(x1, y1, x2, y2, fill="gold")

    def get_coords(self):
        return self.canvas.coords(self.box)
