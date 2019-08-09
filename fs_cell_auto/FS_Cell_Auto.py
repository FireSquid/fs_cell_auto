# ------------------
#       FS_Cell_Auto
#   Filename:       FS_Cell_Auto.py
#   Created_by:     Peter Reynolds
#   Date_Created:   August 9th, 2019
# ------------------


# import necessary modules
import pygame, sys

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode([1280, 720])

# game loop
while True:

    # fill the background with black
    screen.fill([0,0,0])


    # check for events
    for event in pygame.event.get():

        # exit event
        if event.type == pygame.QUIT:
            sys.exit()


    # update the screen
    pygame.display.flip()
