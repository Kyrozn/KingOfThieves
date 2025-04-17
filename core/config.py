CELL_SIZE = 65
OBJECT_SIZE = 130

GRID_WIDTH = 7 * 2 
GRID_HEIGHT = 4 * 2 + 2 # taille cell * taille d'un bloc + sol pour item

WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

GRAVITY = 1
JUMP_STRENGTH = -14.60
SPEED = 5

def round_up_to_5(n):
    return ((n + 4) // 5) * 5
