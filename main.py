import tkinter as tk
import player as p1
# Paramètres du jeu
WIDTH = 500
HEIGHT = 400
GRAVITY = 1

class Game:

    def __init__(self, root):

        self.root = root
        self.root.title("Jeu de Plateforme - Tkinter")

        # Création du Canvas
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightblue")
        self.canvas.pack()
        self.player = p1.Player(self.canvas, self.root)

        # Plateformes
        self.platforms = [
            self.canvas.create_rectangle(0, 380, WIDTH, HEIGHT, fill="green"),  # Sol
            self.canvas.create_rectangle(150, 300, 250, 320, fill="brown"),
            self.canvas.create_rectangle(300, 200, 400, 220, fill="brown"),
        ]
        self.update_game()

    def update_game(self):
        # Appliquer la gravité
        self.player.player_dy += GRAVITY
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
        if x2 > WIDTH:
            self.canvas.move(self.player.cube, WIDTH - x2, 0)
            if self.player.on_ground == False:
                self.player.player_wall_slide = True
        if y2 > HEIGHT:
            self.canvas.move(self.player.cube, 0, HEIGHT - y2)
            self.player.player_dy = 0
            self.player.on_ground = True
            self.player.player_wall_slide = False

        # Relancer la boucle de jeu
        self.root.after(20, self.update_game)


# Lancer le jeu
root = tk.Tk()
game = Game(root)
root.mainloop()
