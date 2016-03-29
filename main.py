import json
from button import *
from Reactive import Reactive
from Predictive import Predictive
import pygame
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

game = Game()
# Variables///////////////////////////////////////////////


# Info for saving
settings_filename = "settings.json"
settings_path = "Files\settings\\"
info_path = "Files\info\\"
# Defaults /////////////////////////////////
default_info_dict = {
    "score": 0,
    "lives": 5,
    "level": 1,
}

default_settings_dict = {
    "difficulty": "easy",
    "mode": "reactive",
    "saved_game": False
}
mode_list = ["reactive", "predictive", "t", "family"]
btn_list = []  # might be able to use this for an easy way to draw all mode btns

# set up the settings /////////////////////////
# Check for settings file.
game.make_sure_path_exists(settings_path, settings_filename, default_settings_dict)
#
for m in mode_list:
    game.check_file(info_path, m + "_info.json", default_info_dict)
# otherwise read in the values

data_doc = json.load(open(settings_path + settings_filename, 'r'))  # load the file
difficulty = data_doc["difficulty"]
mode = data_doc["mode"]
# MODE = mode
print(mode)
print(difficulty)

# other

display = "home"
playing = False

# number of columns
num_columns = 15
# number of rows
num_rows = 22
TILE_WIDTH = 24
TILE_HEIGHT = 24
multiple = 4  # the factor by which to multiply text to get it on the same size scale as the screen


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
largest = len("new game")*10
# modes
reactive_mode = Reactive(difficulty)
predictive_mode = Predictive(difficulty)
# Buttons
play_btn = PygButton(((screen_width / 2) - largest/2, screen_height / 2, largest, 30), "Play")
home_btn = PygButton((5, 5, 60, 30), "Home")
options_btn = PygButton(((screen_width / 2) - largest/2, 300, largest, 30), "Options")
new_btn = PygButton(((screen_width / 2) - 30, 260, largest, 30), "New Game")

reactive_radio = check_button((100, 160, 80, 30), "reactive")
predictive_radio = check_button((200, 160, 80, 30), "Predictive")

# Decide which button is down
mode_btn_dict = {
    "reactive": reactive_radio,
    "predictive": predictive_radio
}
mode_btn_dict[mode].buttonDown = True


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
def draw_home(game_mode):
    screen.fill((0, 0, 255))  # fill screen with black
    for y, array in enumerate(board):  # draw grid
        for x, symbol in enumerate(array):
            pygame.draw.rect(screen, (128, 0, 64, 28), (x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 1)
    # Check to see if there is a saved game
    info = json.load(open("Files\info\\" + game_mode + "_info.json", 'r'))  # load the file
    if default_info_dict["score"] != info["score"] or default_info_dict["level"] != info["level"]:
        # change the play button text to resume button
        play_btn.caption = "Resume"
        # position new and resume button
        play_btn._rect = pygame.Rect(((screen_width / 2) - largest/2, (screen_height / 2)-40, largest, 30))
        new_btn._rect = pygame.Rect(((screen_width / 2) - largest/2, (screen_height / 2), largest, 30))
        # draw new button
        new_btn.draw(screen)
    else:
        play_btn.caption = "Play"
        play_btn._rect = pygame.Rect((screen_width / 2) - largest/2, screen_height / 2, largest, 30)

    game.display_box("ColorWheel", ((screen_width / 2) - size_of_text("options Menu"), 0), screen)

    play_btn.draw(screen)
    options_btn.draw(screen)
    pygame.display.flip()


def draw_options(m):
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
    "options": draw_options,
}

mode_dict = {
    "reactive": reactive_mode,
    "predictive": predictive_mode,
}

# Main Loop ///////////////////////////////////////////////////
while 1 == 1:
    display_dict[display](mode)
    events = pygame.event.get()
    # for mode in mode_dict:
    #     mode_dict[mode].__init__(difficulty)
    for event in events:
        # Handle button clicks////////////////////////////
        if 'click' in play_btn.handleEvent(event):
            # Do stuff in response to button click here.
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
        elif 'click' in new_btn.handleEvent(event):
            game.save(info_path, mode + "_info.json", default_info_dict)
            playing = True

        # TODO see if this is plausible
        for btn in btn_list:
            if 'click' in btn.handleEvent(event):
                btn.buttonDown = True

        # Handle key presses//////////////////////////////
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                setting_dict = {
                    "difficulty": difficulty,
                    "mode": mode
                }
                game.save(settings_path, settings_filename, setting_dict)
                quit()

        # Handle game loops
        if playing:
            mode_dict[mode].setScores()
            info = json.load(open("Files\info\\" + mode + "_info.json", 'r'))  # load the file
            mode_dict[mode].go()
            playing = False
