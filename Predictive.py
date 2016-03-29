import json
from random import choice

import pygame

from base_mode import Base


class Predictive(Base):
    filename = "predictive_info.json"
    speed = 1
    game_timer = pygame.time

    def __init__(self, d):
        super().__init__(d)

    # reset function
    def reset(self):
        game_bullet = self.game_bullet
        game_target = self.game_target
        color_dict = self.game.color_dict

        game_target.y = 2  # reset bullets position
        game_bullet.color = (0, 0, 0, 255)  # make bullet invisible
        game_bullet.fired = False

        # change the targets color (make sure it doesn't use the same color twice in a row)
        prev_color = game_target.color
        game_target.color = color_dict[choice(list(color_dict.keys()))]  # choose a random color for the target
        while prev_color == game_target.color:
            game_target.color = color_dict[choice(list(color_dict.keys()))]  # choose a random color for the target

    def setScores(self):
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
                        self.data = {
                            "score": self.score,
                            "lives": self.lives,
                            "level": self.level,
                        }
                        self.game.save(self.path, self.filename, self.data)
                        playing = False

                        quit()
                    elif event.key in color_dict:
                        game_bullet.color = color_dict[event.key]
                        game_bullet.fired = True
            game_target.y += .1
            # HANDLE FOR WHEN THE BULLET IS FIRED AND WHEN IT HITS
            if game_target.y >= game_bullet.y:
                # check for collision with target
                if game_bullet.color == game_target.color:
                    self.score += 1  # increase self.score
                    self.message = "Nice!!!"
                else:
                    self.score -= 1  # increase self.score
                    game_bullet.fired = False
                    self.message = "Wrong color :("
                self.reset()
            # WAIT
            print(self.speed)
            self.game_timer.wait(int(self.speed))

