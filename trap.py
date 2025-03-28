import tkinter as tk
from config import *

class Trap:
    def __init__(self, canvas, x, y, color="black"):
        trap_size = OBJECT_SIZE / 2
        x1, y1 = x * CELL_SIZE, y * CELL_SIZE
        x2, y2 = x1 + trap_size, y1 + trap_size
        self.canvas = canvas
        self.trap = canvas.create_oval(x1, y1, x2, y2, fill=color)

    def get_coords(self):
        return self.canvas.coords(self.trap)

class Saw(Trap):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, color="gray")

class Grindur(Trap):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, color="yellow")