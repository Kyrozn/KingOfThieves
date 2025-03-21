import tkinter as tk
import player as p1
from map import Map
from trap import Trap, Saw, CELL_SIZE
import config as conf
# Paramètres du jeu

class Game:

    def __init__(self, root):

        self.root = root
        self.root.title("Jeu de Plateforme - Tkinter")

        # Création du Canvas
        self.canvas = tk.Canvas(
            root, width=conf.WIDTH, height=conf.HEIGHT, bg="lightblue"
        )
        self.canvas.pack()

        # Création de la carte
        self.map = Map(self.canvas)

        self.player = p1.Player(self.canvas, self.root)

        # Plateformes
        self.platforms = [
            self.canvas.create_rectangle(
                0, 380, conf.WIDTH, conf.HEIGHT, fill="green"
            ),  # Sol
            self.canvas.create_rectangle(150, 300, 250, 320, fill="brown"),
            self.canvas.create_rectangle(300, 200, 400, 220, fill="brown"),
        ]
        self.traps = [
            Trap(self.canvas, 4, 6),
            Saw(self.canvas, 7, 4)
        ]
        # Etat de la grille (visible ou non)
        self.grid_visible = True
        self.root.bind("<g>", self.toggle_grid)  # Toggle de la grille avec la touche "g"

        self.defense(self.canvas)
        self.updateAttack()

    def defense(self, canvas):
        TrapButton = tk.Button(canvas, command=lambda: self.SetActiveTrap("SimpleTrap")).place(x=300, y=300)
        ChainsawButton = tk.Button(
            canvas, command=lambda: self.SetActiveTrap("ChainsawButton")
        ).place(x=400, y=300)
        pass

    def updateAttack(self):
        # Appliquer la gravité
        self.player.player_dy += conf.GRAVITY
        if self.player.Right_Movement == True:
            self.player.move_right()
        else:
            self.player.move_left()
        # Déplacement du joueur
        self.canvas.move(self.player.cube, self.player.player_dx, self.player.player_dy)
        if (
            self.player.player_dy > 0
            and not self.player.on_ground
            and self.player.player_wall_slide
        ):
            self.player.player_dy *= 0.7
        # Récupérer la position actuelle du joueur
        x1, y1, x2, y2 = self.canvas.coords(self.player.cube)
        # Gestion des collisions avec le sol et les plateformes
        self.player.on_ground = False
        for platform in self.platforms:
            px1, py1, px2, py2 = self.canvas.coords(platform)
            # Collision par le bas
            if y2 >= py1 and y1 < py1 and x2 > px1 and x1 < px2:
                self.canvas.move(self.player.cube, 0, py1 - y2)  # Ajuste la position
                self.player.player_dy = 0
                self.player.on_ground = True

        # Empêcher le joueur de sortir de l'écran
        if x1 < 0:
            self.canvas.move(self.player.cube, -x1, 0)
            if self.player.on_ground == False:
                self.player.player_wall_slide = True
        if x2 > conf.WIDTH:
            self.canvas.move(self.player.cube, conf.WIDTH - x2, 0)
            if self.player.on_ground == False:
                self.player.player_wall_slide = True
        if y2 > conf.HEIGHT:
            self.canvas.move(self.player.cube, 0, conf.HEIGHT - y2)
            self.player.player_dy = 0
            self.player.on_ground = True
            self.player.player_wall_slide = False

        for trap in self.traps:
            trap_coords = trap.get_coords()
            if (x2 > trap_coords[0] and x1 < trap_coords[2] and
                   y2 > trap_coords[1] and y1 < trap_coords[3]):
                self.canvas.create_text(
                    conf.WIDTH // 2,
                    conf.HEIGHT // 2,
                    text="Game Over!",
                    fill="white",
                    font=("Arial", 50),
                )
                return

        # Relancer la boucle de jeu
        self.root.after(20, self.updateAttack)

    def toggle_grid(self, event):
        # Alterner la visibilité de la grille
        self.grid_visible = not self.grid_visible
        if self.grid_visible:
            self.map.draw_grid()  # Redessine la grille
        else:
            self.map.clear_grid()  # Efface la grille
    def SetActiveTrap(self, choice):
        self.ActiveTrap = choice
        print(self.ActiveTrap)

# Lancer le jeu
root = tk.Tk()
game = Game(root)
root.mainloop()
