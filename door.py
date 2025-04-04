import tkinter as tk
from config import *


class Door:
    def __init__(self, canvas, x, y, width=CELL_SIZE, height=2 * CELL_SIZE):
        self.canvas = canvas
        # Conversion des indices de grille en pixels
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + width
        y2 = y1 + height
        # Création de la porte (corps)
        self.body = self.canvas.create_rectangle(x1, y1, x2, y2, fill="maroon")
        # Optionnel : création d'une poignée de porte
        handle_radius = CELL_SIZE * 0.1
        handle_x = x2 - 2 * handle_radius
        handle_y = (y1 + y2) / 2
        self.handle = self.canvas.create_oval(
            handle_x,
            handle_y - handle_radius,
            handle_x + 2 * handle_radius,
            handle_y + handle_radius,
            fill="silver",
        )

    def get_coords(self):
        return self.canvas.coords(self.body)
