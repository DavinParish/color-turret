import json

import pygame

from base_mode import Base
from target import Target


class Reactive(Base):
    filename = "reactive_info.json"
    game_target = Target()

    def __init__(self, d):
        super().__init__(d)

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
                        self.data = {
                            "score": self.score,
                            "lives": self.lives,
                            "level": self.level,
                        }
                        self.game.save(self.path, self.filename, self.data)
                        playing = False

                        quit()
                    elif event.key in color_dict and not game_bullet.fired:
                        game_bullet.color = color_dict[event.key]
                        game_bullet.fired = True

            # HANDLE FOR WHEN THE BULLET IS FIRED AND WHEN IT HITS
            if game_bullet.fired:
                # MOVE THE BULLET
                game_bullet.move()
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
            # WAIT
            game_timer = pygame.time
            game_timer.wait(int(self.game.speed))

