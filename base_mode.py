from random import choice
import json
import pygame

from bullet import Bullet
from target import Target
from game import Game
import pygame.font
import pygame.event
import pygame.draw
import pygame.mixer
import pygame.image
from button import PygButton

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
pygame.init()


class Base:
    # Main game info ////////////////////////////////////////////////
    score = 0
    lives = 5
    level = 1

    # settings
    difficulty = "easy"

    # Other variables //////////////////////////////////////////////
    playing = True
    message = ""
    # number of columns
    num_columns = 15
    # number of rows
    num_rows = 22
    TILE_WIDTH = 24
    TILE_HEIGHT = 24
    path = "Files\info\\"
    filename = "default.json"

    # BUILD BOARD ////////////////////////////////////////////////
    board = []
    row = []
    data = {}
    for i in range(num_columns):  # make the right number of columns
        row.append('0')
    for i in range(num_rows):  # make the right number of rows of those columns
        board.append(row)

    # WINDOW SETUP ////////////////////////////////////////////////
    screen_width = TILE_WIDTH * num_columns
    screen_height = TILE_HEIGHT * num_rows
    screen = pygame.display.set_mode([screen_width, screen_height])

    # INSTANTIATIONS //////////////////////////////////////////////
    game = Game()
    home_btn = PygButton((5, 5, 60, 30), "Home")
    game_bullet = Bullet()
    game_bullet.getPos(num_columns, num_rows)  # position the bullet relative to the size of the screen
    game_target = Target()

    def __init__(self, d):
        # self.path += self.filename  # condense file path into path variable
        self.difficulty = d

    # reset function
    def reset(self):

        game_bullet = self.game_bullet
        game_target = self.game_target
        color_dict = self.game.color_dict

        game_bullet.y = game_bullet.init_y  # reset bullets position
        game_bullet.color = (0, 0, 0, 255)  # make bullet invisible
        game_bullet.fired = False

        game_target.current_life_span = game_target.initial_life_span  # reset targets lifespan
        # change the targets color (make sure it doesn't use the same color twice in a row)
        prev_color = game_target.color
        game_target.color = color_dict[choice(list(color_dict.keys()))]  # choose a random color for the target
        while prev_color == game_target.color:
            game_target.color = color_dict[choice(list(color_dict.keys()))]  # choose a random color for the target

    # function to decrement the lifespan of the target
    def decrement_life(self):
        if self.game_target.current_life_span <= 0:
            self.reset()
            self.score -= 1  # increase self.score
            self.message = "Too Slow!"
        else:
            self.game_target.current_life_span -= 1

    def draw_game(self):
        screen = self.screen
        board = self.board
        tile_width = self.TILE_WIDTH
        tile_height = self.TILE_HEIGHT
        game_bullet = self.game_bullet
        game_target = self.game_target
        home_btn = self.home_btn
        num_columns = self.num_columns
        score = self.score
        message = self.message
        screen_height = self.screen_height
        screen_width = self.screen_width

        screen.fill((0, 0, 0))  # fill screen with black
        for y, array in enumerate(board[2:-2]):  # draw game board
            for x, symbol in enumerate(array):
                pygame.draw.rect(screen, (128, 0, 64, 28),
                                 (x * tile_width, (y * tile_height) + (tile_height * 2), tile_width, tile_height), 1)
        # draw bullet
        pygame.draw.rect(screen, game_bullet.color,
                         (game_bullet.x * tile_width, game_bullet.y * tile_width, tile_width, tile_height))
        # draw target
        pygame.draw.rect(screen, game_target.color, (
            game_target.x * tile_width, game_target.y * tile_width, tile_width * num_columns, 2 * tile_height))

        # Draw info panel
        home_btn.draw(screen)
        self.game.display_box("Score: " + str(score), (80, 10), screen)
        # draw message center
        self.game.display_box(message, ((screen_width / 2) - 50, screen_height - 30), screen)
        pygame.display.flip()

    def go(self):
        pass  # to be overridden


class Reactive(Base):
    filename = "reactive_info.json"

    def __init__(self, d):
        super().__init__(d)
        data_doc = json.load(open(self.path + self.filename, 'r'))  # load the file
        self.score = data_doc["score"]
        self.lives = data_doc["lives"]
        self.level = data_doc["level"]

    def go(self):
        playing = self.playing
        game_target = self.game_target
        game_bullet = self.game_bullet
        color_dict = self.game.color_dict
        home_btn = self.home_btn
        while playing:
            # Draw the board
            self.draw_game()
            self.decrement_life()
            # check the buttons
            # HANDLE KEY PRESSES
            events = pygame.event.get()
            for event in events:
                if 'click' in home_btn.handleEvent(event):
                    self.data = {
                        "score": self.score,
                        "lives": self.lives,
                        "level": self.level,
                    }
                    self.game.save(self.path, self.filename, self.data)
                    playing = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit()
                    elif event.key in color_dict and not game_bullet.fired:
                        game_bullet.color = color_dict[event.key]
                        game_bullet.fired = True

            # HANDLE FOR WHEN THE BULLET IS FIRED AND WHEN IT HITS
            if game_bullet.fired:
                print("fired")  # so I know the code has been reached

                # MOVE THE BULLET
                game_bullet.move()
                print("moving")

                # check for collision with target
                if game_bullet.y == game_target.y:
                    if game_bullet.color == game_target.color:
                        self.score += 1  # increase self.score
                        self.message = "Nice!!!"
                    else:
                        self.score -= 1  # increase self.score
                        game_bullet.fired = False
                        self.message = "Wrong color :("
                    self.reset()
            print("USER SCORE:")
            print(self.score)
            # WAIT
            game_timer = pygame.time
            game_timer.wait(int(self.game.speed))


class Predictive(Base):
    filename = "predictive_info.json"

    def __init__(self, d):
        super().__init__(d)
        data_doc = json.load(open(self.path + self.filename, 'r'))  # load the file
        self.score = data_doc["score"]
        self.lives = data_doc["lives"]
        self.level = data_doc["level"]

    def go(self):
        pass
