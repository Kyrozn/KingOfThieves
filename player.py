import config as conf

class Player:

    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        # Création du joueur
        self.cube = self.canvas.create_rectangle(50, 300, 80, 330, fill="red")

        # Variables du joueur
        self.player_dx = 0
        self.player_dy = 0
        self.Right_Movement = True
        self.player_wall_slide = False
        self.on_ground = False

        self.root.bind("<space>", self.jump)
        self.move_right()

    def move_left(self):
        self.player_dx = -conf.SPEED

    def move_right(self):
        self.player_dx = conf.SPEED

    def jump(self, event):
        if self.on_ground:
            self.player_dy = conf.JUMP_STRENGTH
            self.on_ground = False
        if self.player_wall_slide:
            self.player_dy = conf.JUMP_STRENGTH
            self.on_ground = False
            self.Right_Movement = not self.Right_Movement
            self.player_wall_slide = False
