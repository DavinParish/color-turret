from copy import deepcopy
import json
from random import choice
from button import *
from bullet import Bullet
from target import Target
from base_mode import Reactive, Predictive
import pygame
import os
from game import Game
import pygame.font
import pygame.event
import pygame.draw
import pygame.mixer
import pygame.image

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
pygame.init()

# Variables///////////////////////////////////////////////
display = "home"
playing = False
mode = "reactive"
# number of columns
num_columns = 15
# number of rows
num_rows = 22
TILE_WIDTH = 24
TILE_HEIGHT = 24
multiple = 4  # the factor by which to multiply text to get it on the same size scale as the screen

# game variables
score = 0
lives = 5
message = ""

mode_list = ["predictive", "reactive", "t", "family"]
btn_list = []
# BUILD BOARD ////////////////////////////////////////////////
board = []
row = []
for i in range(num_columns):  # make the right number of columns
    row.append('0')
for i in range(num_rows):  # make the right number of rows of those columns
    board.append(row)

# WINDOW SETUP ////////////////////////////////////////////////
screen_width = TILE_WIDTH * num_columns
screen_height = TILE_HEIGHT * num_rows
screen = pygame.display.set_mode([screen_width, screen_height])

# Instantiations /////////////////////////////////////////
game = Game()
reactive_mode = Reactive()
predictive_mode = Predictive()
# Buttons
play_btn = PygButton(((screen_width / 2) - 30, screen_height / 2, 60, 30), "Play")
home_btn = PygButton((5, 5, 60, 30), "Home")
options_btn = PygButton(((screen_width / 2) - 30, 300, 60, 30), "Options")

predictive_radio = check_button((100, 160, 80, 30), "Predictive")
reactive_radio = check_button((200, 160, 80, 30), "reactive")

# game variables
game_bullet = Bullet()
game_bullet.getPos(num_columns, num_rows)  # position the bullet relative to the size of the screen

game_target = Target()


#  Functions ///////////////////////////////////////////////////
# TODO make this work
# gets the size of the text relative to the screen
def size_of_text(text):
    size = len(text) * multiple
    return size


# TODO see if this is plausible
# makes buttons
def make_button(name, x, y, caption):
    if len(caption) * 10 < 30:  # set a minimum width
        width = 30
    else:
        width = len(caption) * 10
    name = check_button((x, y, width, 30), caption)
    name.draw(screen)
    btn_list.append(name)
    return width


# DISPLAYS /////////////////////////////////////////////////////
def draw_home():
    screen.fill((0, 0, 255))  # fill screen with black
    for y, array in enumerate(board):  # draw grid
        for x, symbol in enumerate(array):
            pygame.draw.rect(screen, (128, 0, 64, 28), (x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 1)

    game.display_box("ColorWheel", ((screen_width / 2) - size_of_text("options Menu"), 0), screen)

    play_btn.draw(screen)
    options_btn.draw(screen)
    pygame.display.flip()


def draw_game():
    screen.fill((0, 0, 0))  # fill screen with black
    for y, array in enumerate(board[2:-2]):  # draw game board
        for x, symbol in enumerate(array):
            pygame.draw.rect(screen, (128, 0, 64, 28),
                             (x * TILE_WIDTH, (y * TILE_HEIGHT) + (TILE_HEIGHT * 2), TILE_WIDTH, TILE_HEIGHT), 1)
    # draw bullet
    pygame.draw.rect(screen, game_bullet.color,
                     (game_bullet.x * TILE_WIDTH, game_bullet.y * TILE_WIDTH, TILE_WIDTH, TILE_HEIGHT))
    # draw target
    pygame.draw.rect(screen, game_target.color, (
        game_target.x * TILE_WIDTH, game_target.y * TILE_WIDTH, TILE_WIDTH * num_columns, 2 * TILE_HEIGHT))

    # Draw info panel
    home_btn.draw(screen)
    game.display_box("Score: " + str(score), (80, 10), screen)
    # draw message center
    game.display_box(message, (10, screen_height - 30), screen)
    pygame.display.flip()


def draw_options():
    screen.fill((0, 255, 0))  # fill screen with something

    # draw header
    # TODO find a better way to center elements
    game.display_box("Options Menu", ((screen_width / 2) - size_of_text("options Menu"), 0), screen)
    game.display_box("Modes", (10, 80), screen)

    # Draw buttons
    home_btn.draw(screen)
    predictive_radio.draw(screen)
    reactive_radio.draw(screen)

    # TODO see if plausible
    x = 10
    y = 120
    for mod in mode_list:
        width = make_button(mod, x, y, mod)
        if x < screen_width - 110:
            x += width + 20
        else:
            x = 10
            y += 40

    pygame.display.flip()


# Dictionaries //////////////////////////////////////////////////
display_dict = {
    "home": draw_home,
    "game": draw_game,
    "options": draw_options,
}

mode_dict = {
    "reactive": reactive_mode,
    "predictive": predictive_mode,
}

# Main Loop ///////////////////////////////////////////////////
while 1 == 1:
    display_dict[display]()
    events = pygame.event.get()
    for event in events:
        # Handle button clicks////////////////////////////
        if 'click' in play_btn.handleEvent(event):
            # Do stuff in response to button click here.
            display = "game"
            playing = True

        elif 'click' in home_btn.handleEvent(event):
            display = "home"
            playing = False
        elif 'click' in options_btn.handleEvent(event):
            display = "options"
            playing = False
        elif 'click' in predictive_radio.handleEvent(event):
            reactive_radio.buttonDown = False
            predictive_radio.buttonDown = True
            playing = False
            mode = "predictive"
        elif 'click' in reactive_radio.handleEvent(event):
            predictive_radio.buttonDown = False
            reactive_radio.buttonDown = True
            playing = False
            mode = "reactive"
        # TODO see if this is plausible
        for btn in btn_list:
            if 'click' in btn.handleEvent(event):
                btn.buttonDown = True

        # Handle key presses//////////////////////////////
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit()

        # Handle game loops
        if playing:
            mode_dict[mode].go()
