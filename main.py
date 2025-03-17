import tkinter as tk
from map import Map
from trap import Trap, Saw, CELL_SIZE

# Paramètres du jeu
WIDTH = 500
HEIGHT = 400
GRAVITY = 1
JUMP_STRENGTH = -11
SPEED = 5

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de Plateforme - Tkinter")

        # Création du Canvas
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightblue")
        self.canvas.pack()

        # Création de la carte
        self.map = Map(self.canvas)

        # Création du joueur
        self.player = self.canvas.create_rectangle(1 * CELL_SIZE, 6 * CELL_SIZE, 1.5 * CELL_SIZE, 6.5 * CELL_SIZE, fill="red")

        # Plateformes
        self.platforms = [
            self.map.create_platform(0, 7, 10, 1),  # Sol
            self.map.create_platform(3, 5, 2, 1),
            self.map.create_platform(6, 3, 2, 1)
        ]

        # Pièges
        self.traps = [
            Trap(self.canvas, 4, 6),
            Saw(self.canvas, 7, 4)
        ]

        # Variables du joueur
        self.player_dx = 0
        self.player_dy = 0
        self.on_ground = False

        # Etat de la grille (visible ou non)
        self.grid_visible = True

        # Détection des touches
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.jump)
        self.root.bind("<KeyRelease>", self.stop_movement)
        self.root.bind("<g>", self.toggle_grid)  # Toggle de la grille avec la touche "g"

        # Lancement de la boucle du jeu
        self.update_game()

    def move_left(self, event):
        self.player_dx = -SPEED

    def move_right(self, event):
        self.player_dx = SPEED

    def stop_movement(self, event):
        if event.keysym in ["Left", "Right"]:
            self.player_dx = 0

    def jump(self, event):
        if self.on_ground:
            self.player_dy = JUMP_STRENGTH
            self.on_ground = False

    def toggle_grid(self, event):
        # Alterner la visibilité de la grille
        self.grid_visible = not self.grid_visible
        if self.grid_visible:
            self.map.draw_grid()  # Redessine la grille
        else:
            self.map.clear_grid()  # Efface la grille

    def update_game(self):
        # Appliquer la gravité
        self.player_dy += GRAVITY

        # Déplacement du joueur
        self.canvas.move(self.player, self.player_dx, self.player_dy)

        # Récupérer la position actuelle du joueur
        x1, y1, x2, y2 = self.canvas.coords(self.player)

        # Gestion des collisions avec le sol et les plateformes
        self.on_ground = False
        for platform in self.platforms:
            px1, py1, px2, py2 = self.canvas.coords(platform)
            # Collision par le bas
            if y2 >= py1 and y1 < py1 and x2 > px1 and x1 < px2:
                self.canvas.move(self.player, 0, py1 - y2)  # Ajuste la position
                self.player_dy = 0
                self.on_ground = True

        # Empêcher le joueur de sortir de l'écran
        if x1 < 0:
            self.canvas.move(self.player, -x1, 0)
        if x2 > WIDTH:
            self.canvas.move(self.player, WIDTH - x2, 0)
        if y2 > HEIGHT:
            self.canvas.move(self.player, 0, HEIGHT - y2)
            self.player_dy = 0
            self.on_ground = True

        # Gestion de la collision avec les pièges
        for trap in self.traps:
            trap_coords = trap.get_coords()
            if (x2 > trap_coords[0] and x1 < trap_coords[2] and
                    y2 > trap_coords[1] and y1 < trap_coords[3]):
                self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over!", fill="white", font=("Arial", 50))
                return

        # Relancer la boucle de jeu
        self.root.after(20, self.update_game)


# Lancer le jeu
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
