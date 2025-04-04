import tkinter as tk
from map import Map
from trap import *
import player as p1
from chest import Chest
from door import Door 
from config import *

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de Plateforme - Tkinter")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightblue")
        self.canvas.pack()
        self.map = Map(self.canvas)
        self.health_icons = []

        self.door = Door(self.canvas, x=10.25, y=6.75, width=1.5 * CELL_SIZE, height=1.25 * CELL_SIZE)
        door_coords = self.door.get_coords()
        self.spawn_x = (door_coords[0] + door_coords[2]) / 2
        self.spawn_y = door_coords[3] - 30
        # Création du joueur
        self.player = p1.Player(self.canvas, self.root, x=self.spawn_x, y=self.spawn_y)
        
        # Instanciation du coffre à une position choisie
        self.chest = Chest(self.canvas, x=2.25, y=0.75, width= 1.5 * CELL_SIZE, height= 1.25 *CELL_SIZE)


        # Plateformes
        self.platforms = [
            self.map.create_platform(0, 8, 7, 1),  # Sol (avec inventaire par exemple)
            self.map.create_platform(2, 6, 4, 1),
            self.map.create_platform(8, 4, 2, 1),
            self.map.create_platform(4, 0, 4, 1),
            self.map.create_platform(2, 2, 2, 1)
        ]

        # Pièges
        self.traps = [Grindur(self.canvas, 12,2), Saw(self.canvas, 5,5), Bomb(self.canvas, 2,4)]
        self.occupied_cells = set()  # Stocke les positions des pièges
        self.placed_traps = {"Grindur": False, "Saw": False, "Bomb": False}  # Limite à un seul piège par type

        # Inventaire
        self.selected_trap = None
        self.create_inventory()

        self.create_health()

        self.grid_visible = True

        # Détection des touches
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.jump)
        self.root.bind("<KeyRelease>", self.stop_movement)
        self.root.bind("<g>", self.toggle_grid)

        # Lier l'événement de clic pour récupérer les coordonnées et placer un piège
        self.canvas.bind("<Button-1>", self.get_cell_coords)

        # Lancement de la boucle du jeu
        self.update_game()

    def create_inventory(self):
        inventory_x = 350
        inventory_y = HEIGHT - 70  # Position sur la plateforme en bas

        trap_types = [("Grindur", "teal"), ("Saw", "gray"), ("Bomb", "white")]

        for name, color in trap_types:
            btn = tk.Button(self.root, text=name, bg=color, command=lambda n=name: self.select_trap(n))
            btn.place(x=inventory_x, y=inventory_y, width=60, height=30)
            inventory_x += 70  # Espacement des boutons

    def create_health(self):
        self.health_icons = []  # Stocke les icônes de vie pour les mettre à jour

        health_x = 400  # Position de départ à gauche
        health_y = 20  # Position en haut

        for i in range(self.player.lifeRemaining):  # Affiche autant de coeurs que de vies restantes
            heart = self.canvas.create_oval(health_x, health_y, health_x + 30, health_y + 30, fill="red", outline="black")
            self.health_icons.append(heart)
            health_x += 40  # Espacement entre les coeurs

    def update_health_display(self):
        # Supprime les coeurs actuels
        for heart in self.health_icons:
            self.canvas.delete(heart)

        # Affiche les coeurs restants
        self.create_health()



    def select_trap(self, trap_name):
        # Remplacer la sélection précédente par le nouveau
        self.selected_trap = trap_name
        print(f"Piège sélectionné : {self.selected_trap}")

    def get_cell_coords(self, event):
        cell_x = event.x // CELL_SIZE
        cell_y = event.y // CELL_SIZE

        # Affichage des coordonnées dans la console
        print(f"Cellule cliquée : ({cell_x}, {cell_y})")

        # Appeler la fonction pour placer le piège (sans repère visuel)
        self.place_trap(cell_x, cell_y)

    def place_trap(self, cell_x, cell_y):
        if not self.selected_trap:
            print("Aucun piège sélectionné !")
            return

        # Limiter à un seul piège par type
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
        elif self.selected_trap == "Bomb":
            new_trap = Bomb(self.canvas, cell_x, cell_y)
        else:
            return

        self.traps.append(new_trap)
        self.occupied_cells.add(cell_position)  # Marquer la cellule comme occupée
        self.placed_traps[self.selected_trap] = True  # Limiter à un seul par type
        print(f"Piège {self.selected_trap} placé à ({cell_x}, {cell_y})")

        # Désélectionner le piège après placement
        self.selected_trap = None

    def move_left(self, event):
        self.player.move_left()

    def move_right(self, event):
        self.player.move_right()

    def stop_movement(self, event):
        if event.keysym in ["Left", "Right"]:
            self.player.player_dx = 0

    def jump(self, event):
        self.player.jump(event)

    def toggle_grid(self, event):
         # Alterner la visibilité de la grille
         self.grid_visible = not self.grid_visible
         if self.grid_visible:
             self.map.draw_grid()  # Redessine la grille
         else:
             self.map.clear_grid()  # Efface la grille

    def update_game(self):

        if self.player.lifeRemaining == 0:
            self.canvas.create_text(
                WIDTH // 2,
                HEIGHT // 2,
                text="Game Over!",
                fill="white",
                font=("Arial", 50),
            )

        self.player.player_dy += GRAVITY
        self.canvas.move(self.player.cube, self.player.player_dx, self.player.player_dy)

        # Récupérer la position actuelle du joueur
        x1, y1, x2, y2 = self.canvas.coords(self.player.cube)
        self.player.on_ground = False

        for platform in self.platforms:
            px1, py1, px2, py2 = self.canvas.coords(platform)
            if y2 >= py1 and y1 < py1 and x2 > px1 and x1 < px2:
                self.canvas.move(self.player.cube, 0, py1 - y2)
                self.player.player_dy = 0
                self.player.on_ground = True

        if x1 < 0:
            self.canvas.move(self.player.cube, -x1, 0)
        if x2 > WIDTH:
            self.canvas.move(self.player.cube, WIDTH - x2, 0)
        if y2 > HEIGHT:
            self.canvas.move(self.player.cube, 0, HEIGHT - y2)
            self.player.player_dy = 0
            self.player.on_ground = True

        # Vérifier la collision avec les pièges
        for trap in self.traps:
            if trap.check_collision(x1, y1, x2 - x1, y2 - y1):
                self.player.lifeRemaining -= 1
                self.update_health_display()
                self.nextLife()

        # Vérifier la collision avec le coffre
        chest_coords = self.canvas.coords(self.chest.box)
        if (x2 > chest_coords[0] and x1 < chest_coords[2] and
                y2 > chest_coords[1] and y1 < chest_coords[3]):
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="You Win!", fill="green", font=("Arial", 50))
            return

        self.root.after(20, self.update_game)

    def nextLife(self):
        self.player.setposition(self.spawn_x, self.spawn_y)


class Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Menu")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightblue")
        self.canvas.pack()

        self.create_buttons()

    def create_buttons(self):
        btn1 = tk.Button(self.root, text="Player", command=self.start_player_mode, width=20, height=2)
        btn2 = tk.Button(self.root, text="AI", command=self.start_ai_mode, width=20, height=2)
        btn3 = tk.Button(self.root, text="Player vs AI", command=self.start_pvp_ai_mode, width=20, height=2)

        btn1.place(x=400, y=80)
        btn2.place(x=400, y=130)
        btn3.place(x=400, y=180)

    def start_player_mode(self):
        # Supprime les éléments du menu
        for widget in self.root.winfo_children():
            widget.destroy()

        # Démarre le jeu en mode joueur
        game = Game(self.root)

    def start_ai_mode(self):
        print("AI mode is not implemented yet!")

    def start_pvp_ai_mode(self):
        print("Player vs AI mode is not implemented yet!")

if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root)
    root.mainloop()
