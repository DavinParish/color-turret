# Bullet class
# bullet_color, bullet_x, bullet_y


class Bullet:
    color = (0, 0, 255)  # (0, 0, 0, 255)
    init_x = 1
    init_y = 1
    x = 1
    y = 1
    fired = False

    def getPos(self, num_columns, num_rows):
        self.x = num_columns / 2
        self.y = num_rows - 5
        self.init_x = num_columns / 2
        self.init_y = num_rows - 5


    def move(self):
        self.y -= 1
        # shell = list(self.bull[0])
        # shell[1] -= 1
