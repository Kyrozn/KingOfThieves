import tkinter as tk
import config as conf


class Map:
    def __init__(self, canvas):
        self.canvas = canvas
        self.platforms = []
        self.grid_lines = []  # Liste des lignes de la grille
        self.draw_grid()

    def create_platform(self, x, y, width, height):
        x1, y1 = x * conf.CELL_SIZE, y * conf.CELL_SIZE
        x2, y2 = x1 + width * conf.CELL_SIZE, y1 + height * conf.CELL_SIZE
        platform = self.canvas.create_rectangle(x1, y1, x2, y2, fill="brown")
        self.platforms.append(platform)
        return platform

    def draw_grid(self):
        self.grid_lines.clear()  # Efface les anciennes lignes
        # Dessine des lignes horizontales
        for i in range(0, conf.HEIGHT, conf.CELL_SIZE):
            line = self.canvas.create_line(0, i, conf.WIDTH, i, fill="gray")
            self.grid_lines.append(line)

        # Dessine des lignes verticales
        for j in range(0, conf.WIDTH, conf.CELL_SIZE):
            line = self.canvas.create_line(j, 0, j, conf.HEIGHT, fill="gray")
            self.grid_lines.append(line)

    def clear_grid(self):
        # Efface les lignes de la grille
        for line in self.grid_lines:
            self.canvas.delete(line)
        self.grid_lines.clear()
