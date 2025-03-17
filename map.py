import tkinter as tk
CELL_SIZE = 50
WIDTH = 500
HEIGHT = 400
class Map:
    def __init__(self, canvas):
        self.canvas = canvas
        self.platforms = []
        self.grid_lines = []  # Liste des lignes de la grille
        self.draw_grid()

    def create_platform(self, x, y, width, height):
        x1, y1 = x * CELL_SIZE, y * CELL_SIZE
        x2, y2 = x1 + width * CELL_SIZE, y1 + height * CELL_SIZE
        platform = self.canvas.create_rectangle(x1, y1, x2, y2, fill="brown")
        self.platforms.append(platform)
        return platform

    def draw_grid(self):
        self.grid_lines.clear()  # Efface les anciennes lignes
        # Dessine des lignes horizontales
        for i in range(0, HEIGHT, CELL_SIZE):
            line = self.canvas.create_line(0, i, WIDTH, i, fill="gray")
            self.grid_lines.append(line)

        # Dessine des lignes verticales
        for j in range(0, WIDTH, CELL_SIZE):
            line = self.canvas.create_line(j, 0, j, HEIGHT, fill="gray")
            self.grid_lines.append(line)

    def clear_grid(self):
        # Efface les lignes de la grille
        for line in self.grid_lines:
            self.canvas.delete(line)
        self.grid_lines.clear()
