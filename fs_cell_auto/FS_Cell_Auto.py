# ------------------
#       FS_Cell_Auto
#   Filename:       FS_Cell_Auto.py
#   Created_by:     Peter Reynolds
#   Date_Created:   August 9th, 2019
# ------------------


# import necessary modules
import pygame, sys
from Cell_State  import Cell_State

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode([1280, 720])

# clock to control the framerate
clock = pygame.time.Clock()
framerate = 60

# position of the camera (i.e. where the top right corner is located)
camera_pos = [0,0]

# initialize a Cell_State with test values
cell_state = Cell_State([(6,6), (7,6), (8,6), (8,5), (7,4)])

# used for manual stepping
stepped = False
step_mode = True

# game loop
while True:

    # fill the background with black
    screen.fill([0,0,0])


    # check for events
    for event in pygame.event.get():

        # exit event
        if event.type == pygame.QUIT:
            sys.exit()

        # manual stepping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:     # manual step through the simulation
                if not stepped:
                    stepped = True
                    step_mode = True
                    cell_state.update_state()
            if event.key == pygame.K_r:     # return to automatic updates
                step_mode = False
        if event.type == pygame.KEYUP:      # reset stepping
            if event.key == pygame.K_s:
                stepped = False

    # update the Cell_State
    if not step_mode: cell_state.update_state()

    # draw the Cell_State
    cell_state.draw_state(screen, camera_pos)

    # set the framerate
    clock.tick(framerate)

    # update the screen
    pygame.display.flip()
