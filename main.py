import tkinter as tk
from chest import Chest
import data
from door import Door
import player as p1
from map import Map
from trap import *
import config as conf
import pandas as pd
import time

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
        # Création de la porte (qui servira de spawn)
        self.door = Door(self.canvas, x=10.25, y=6.75, width=1.25 * CELL_SIZE, height=1.25 * CELL_SIZE)
        door_coords = self.door.get_coords()
        self.spawn_x = (door_coords[0] + door_coords[2]) / 2
        self.spawn_y = door_coords[3] - 30
        # Création du joueur
        self.player = p1.Player(self.canvas, self.root, x=self.spawn_x, y=self.spawn_y)
        # Instanciation du coffre à une position choisie (ex. en haut à droite)
        self.chest = Chest(self.canvas, x=2.25, y=0.75, width= 1.5 * CELL_SIZE, height= 1.25 *CELL_SIZE)
        chestx1, chesty1, chestx2, chesty2 = self.chest.get_coords()
        chestCenterX = (chestx1 + chestx2) / 2
        chestCenterY = (chesty1 + chesty2) / 2

        # Plateformes
        self.platforms = [
            self.map.create_platform(0, 8, 7, 1),  # Sol avec l'inventaire
            self.map.create_platform(2, 6, 4, 1),
            self.map.create_platform(8, 4, 2, 1),
            self.map.create_platform(4, 0, 4, 1),
            self.map.create_platform(2, 2, 2, 1),
        ]

        # Pièges et état des cellules
        self.traps = [Grindur(self.canvas, 12, 2)]
        self.occupied_cells = set()  # Stocke les positions des pièges
        self.placed_traps = {
            "Grindur": False,
            "Saw": False,
        }

        # Inventaire
        self.selected_trap = None
        self.create_inventory()

        # Etat de la grille (visible ou non)
        self.grid_visible = True
        self.root.bind("<g>", self.toggle_grid)  # Toggle de la grille avec la touche "g"
        self.colision = False
        # Mise à jour de l'attaque
        self.dataFrame = pd.DataFrame(
            [
                {
                    "StartPos": (self.spawn_x, self.spawn_y),
                    "ObjectifPos": (chestCenterX, chestCenterY),
                    "Piege1": (2, 3),
                    "Piege2": (4, 5),
                    "Piege3": (6, 7),
                    "Win": None,
                    "Try": None,
                    "Temps": None,
                    "ActNb": None,
                    "JumpsPos": None,
                }
            ]
        )
        self.timer = time.time()
        self.updateAttack()

    def create_inventory(self):
        """Crée l'inventaire sur la plateforme (0,8,7,1)"""
        inventory_x = 400
        inventory_y = conf.HEIGHT - 60  # Position sur la plateforme en bas

        trap_types = [("Grindur", "yellow"), ("Saw", "gray")]

        for name, color in trap_types:
            btn = tk.Button(
                self.root,
                text=name,
                bg=color,
                command=lambda n=name: self.select_trap(n),
            )
            btn.place(x=inventory_x, y=inventory_y, width=60, height=30)
            inventory_x += 70  # Espacement des boutons

    def select_trap(self, trap_name):
        """Sélectionner un piège"""
        self.selected_trap = trap_name
        print(f"Piège sélectionné : {self.selected_trap}")

    def get_cell_coords(self, event):
        """Récupère les coordonnées de la cellule cliquée"""
        cell_x = event.x // conf.CELL_SIZE
        cell_y = event.y // conf.CELL_SIZE

        print(f"Cellule cliquée : ({cell_x}, {cell_y})")

        # Afficher un repère visuel temporaire
        self.canvas.create_rectangle(
            cell_x * conf.CELL_SIZE,
            cell_y * conf.CELL_SIZE,
            (cell_x + 1) * conf.CELL_SIZE,
            (cell_y + 1) * conf.CELL_SIZE,
        )

        # Appeler la fonction pour placer le piège
        self.place_trap(cell_x, cell_y)

    def place_trap(self, cell_x, cell_y):
        """Place un piège à la position donnée"""
        if not self.selected_trap:
            print("Aucun piège sélectionné !")
            return

        # Vérifier si un piège du même type a déjà été placé
        if self.placed_traps[self.selected_trap]:
            print(f"Un piège de type {self.selected_trap} a déjà été placé !")
            return

        cell_position = (cell_x, cell_y)

        # Vérifier si la cellule est déjà occupée
        if cell_position in self.occupied_cells:
            print(f"Un piège est déjà placé en ({cell_x}, {cell_y}) !")
            return

        # Ajouter le piège sur le canvas
        if self.selected_trap == "Grindur":
            new_trap = Grindur(self.canvas, cell_x, cell_y)
        elif self.selected_trap == "Saw":
            new_trap = Saw(self.canvas, cell_x, cell_y)
        else:
            return

        self.traps.append(new_trap)
        self.occupied_cells.add(cell_position)  # Marquer la cellule comme occupée
        self.placed_traps[self.selected_trap] = True  # Marquer ce piège comme placé
        print(f"Piège {self.selected_trap} placé à ({cell_x}, {cell_y})")

        # Désélectionner le piège après placement (pour éviter une réutilisation)
        self.selected_trap = None

    def updateAttack(self):
        """Met à jour l'attaque et les mouvements"""
        if self.player.lifeRemaining == 0:
            self.canvas.create_text(
                WIDTH // 2,
                HEIGHT // 2,
                text="Game Over!",
                fill="white",
                font=("Arial", 50),
            )
            self.updateFinalDT(False)
            return
        # Appliquer la gravité
        if not self.player.on_ground:
            self.player.player_dy += conf.GRAVITY
            if self.player.Right_Movement:
                self.player.move_right()
            else: 
                self.player.move_left()

        # Déplacement du joueur
        self.canvas.move(self.player.cube, self.player.player_dx, self.player.player_dy)

        # Vérification du déplacement et ajustement de la gravité
        if self.player.player_dy > 0 and not self.player.on_ground and self.player.player_wall_slide and (self.checkWallCollision() or self.prevent_player_out_of_bounds()):
            self.player.player_dy *= 0.7
        # Vérification des collisions avec les murs
        self.checkWallCollision()

        # Empêcher le joueur de sortir de l'écran
        self.prevent_player_out_of_bounds()

        # Vérification des collisions avec les pièges
        self.check_trap_collisions()
        # Vérifier la collision avec le coffre4
        if self.check_Chest_collisions():
            return

        # Relancer la boucle de jeu
        self.root.after(20, self.updateAttack)
    def check_Chest_collisions(self):
        x1, y1, x2, y2 = self.canvas.coords(self.player.cube)
        chest_coords = self.canvas.coords(self.chest.box)
        if (
           x2 > chest_coords[0]
           and x1 < chest_coords[2]
           and y2 > chest_coords[1]
           and y1 < chest_coords[3]
        ):
            self.canvas.create_text(
                WIDTH // 2,
                HEIGHT // 2,
                text="You Win!",
                fill="green",
                font=("Arial", 50),
            )
            self.timer = time.time() - self.timer
            self.updateFinalDT(True)
            return True
        return False
    def prevent_player_out_of_bounds(self):
        """Empêche le joueur de sortir de l'écran"""
        x1, y1, x2, y2 = self.canvas.coords(self.player.cube)

        if x1 < 0:
            self.canvas.move(self.player.cube, -x1, 0)
            if not self.player.on_ground:
                self.player.player_wall_slide = True
            self.colision = True
        elif x2 > conf.WIDTH:
            self.canvas.move(self.player.cube, conf.WIDTH - x2, 0)
            if not self.player.on_ground:
                self.player.player_wall_slide = True
            self.colision = True
        if y2 > conf.HEIGHT:
            self.canvas.move(self.player.cube, 0, conf.HEIGHT - y2)
            self.player.player_dy = 0
            self.player.on_ground = True
            self.player.player_wall_slide = False
            self.colision = True
        elif y1 <= 0:
            self.canvas.move(self.player.cube, 0, 0)
            self.player.player_dy = 0
            self.colision = True
        return self.colision

    def check_trap_collisions(self):
        """Vérifie les collisions avec les pièges"""
        x1, y1, x2, y2 = self.canvas.coords(self.player.cube)
        for trap in self.traps:
            if trap.check_collision(x1, y1, x2 - x1, y2 - y1):
                self.player.lifeRemaining -= 1
                self.nextLife()

    def toggle_grid(self, event):
        """Alterne la visibilité de la grille"""
        self.grid_visible = not self.grid_visible
        if self.grid_visible:
            self.map.draw_grid()  # Redessine la grille
        else:
            self.map.clear_grid()  # Efface la grille

    def SetActiveTrap(self, choice):
        """Active le piège choisi"""
        self.ActiveTrap = choice
        print(self.ActiveTrap)

    def checkWallCollision(self):
        """Vérifie les collisions avec les murs et plateformes"""
        x1, y1, x2, y2 = self.canvas.coords(self.player.cube)
        self.colision = False
        self.player.on_ground = False
        for platform in self.platforms:
            px1, py1, px2, py2 = self.canvas.coords(platform)
            # Collision par la gauche
            if x2 >= px1 and x1 < px1 and y2 > py1 and y1 < py2:
                self.canvas.move(self.player.cube, px1 - x2, 0)
                if not self.player.on_ground:
                    self.player.player_wall_slide = True
                self.colision = True
            # Collision par la droite
            elif x1 <= px2 and x2 > px2 and y2 > py1 and y1 < py2:
                self.canvas.move(self.player.cube, px2 - x1, 0)
                if not self.player.on_ground:
                    self.player.player_wall_slide = True
                self.colision = True
            if y2 >= py1 and y1 < py1 and x2 > px1 and x1 < px2:
                self.canvas.move(self.player.cube, 0, py1 - y2)
                self.player.player_dy = 0
                self.player.on_ground = True
                self.player.player_wall_slide = False
                self.colision = True
            # Collision par le haut
            elif y1 <= py2 and y2 > py2 and x2 > px1 and x1 < px2:
                self.canvas.move(self.player.cube, 0, py2 - y1)
                self.player.player_dy = 0
                self.colision = True
        return self.colision
    def updateFinalDT(self, win: bool):
        self.dataFrame.loc[1, ["Win", "Try", "Temps", "ActNb", "JumpsPos"]] = [win, self.player.lifeRemaining, self.timer, self.player.ActionNb, self.player.jumpPos]
        data.registerData(self.dataFrame)
    def nextLife(self):
        self.player.setposition(self.spawn_x, self.spawn_y)


# Lancer le jeu
root = tk.Tk()
game = Game(root)
root.mainloop()
