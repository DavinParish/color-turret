import pygame
import os
import errno
import pygame.font
import pygame.event
import pygame.draw
import pygame.mixer
import pygame.image

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
pygame.init()


class Game:
    color_dict = {
        pygame.K_r: (215, 23, 23),  # red
        pygame.K_b: (23, 23, 236),  # blue

    }
    speed = 10

    # Function that handles the display of text on the window
    def display_box(self, message, position, screen):
        font_object = pygame.font.SysFont('Times New Roman', 18)
        if message:
            text = font_object.render(message, 1, (255, 0, 0, 255))

            screen.blit(text, position)

    def make_sure_path_exists(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
