import pygame
import json
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

    def check_file(self, path, filename, data):
        self.make_sure_path_exists(path, filename, data)
        if not os.path.isfile(path+filename):
            with open(path + filename, 'w') as outfile:
                json.dump(data, outfile)

    def make_sure_path_exists(self, path, filename, data):
        # if not os.path.exists(path):
        #     os.makedirs(path)
        try:
            os.makedirs(path)
            with open(path + filename, 'w') as outfile:
                json.dump(data, outfile)
            print("//////////////////////////////////////////////////////////")
            print(path)
            print("//////////////////////////////////////////////////////////")

        except OSError as exception:
            print("//////////////////////////////////////////////////////////")
            print("darn")
            print("//////////////////////////////////////////////////////////")
            if exception.errno != errno.EEXIST:
                raise

    # creates the file if its not there
    def initialize_json(self, filename, data):
        # create the file
        # input values
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

    # saves the file
    def save(self, path, filename, data):
        self.make_sure_path_exists(path, filename, data)  # check if path exists and make the directories if it doesn't

        with open(path + filename, 'w') as outfile:
            json.dump(data, outfile)
        #
        # TODO see if this is a plausible way of doing this
        # if not os.path.isfile(filename):  # if the file doesn't exist create it
        #     self.initialize_json(filename, data)
        # else:  # otherwise update information
        #     data_doc = json.load(open(filename))  # load the file
        #     for index, element in enumerate(data_doc):
        #         element[index] = data[index]
        #
                # # i shouldn't need this with the initialize function
                # if os.path.getsize(path) <= 0:  # if the file is empty set up default values
