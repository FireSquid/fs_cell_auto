# ------------------
#       FS_Cell_Auto
#   Filename:       FS_Cell_Auto.py
#   Created_by:     Peter Reynolds
#   Date_Created:   August 9th, 2019
# ------------------


# import necessary modules
import pygame, sys, math
from Cell_State import Cell_State
from pygame import Vector2


# convert the camera scale from linear to exponential
def real_scale(scale):
    return math.exp(scale)


# initialize pygame
pygame.init()


# Dimensions of the screen
SCREEN_SIZE = [1280, 720]
# Vector version of the screen
screen_size = Vector2(SCREEN_SIZE)

# create the screen
screen = pygame.display.set_mode(SCREEN_SIZE)

# clock to control the framerate
clock = pygame.time.Clock()
framerate = 60



# position of the camera
camera_pos = Vector2([0, 0])
# scale of the camera
camera_scale = 0

# initialize a Cell_State
cell_state = Cell_State([Vector2(0,0)])

# used for manual stepping
step_mode = True

# true if the left mouse botton is held down
mouse_held = [False, False, False]

last_mouse_pos = False

# game loop
while True:

    # fill the background with black
    screen.fill([0,0,0])


    # check for events
    for event in pygame.event.get():

        # exit event
        if event.type == pygame.QUIT:
            sys.exit()

        # key events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:     # manual step through the simulation
                step_mode = True
                cell_state.update_state()
            if event.key == pygame.K_r:     # return to automatic updates
                step_mode = False

            if event.key == pygame.K_UP:       # Zoom in
                camera_scale -= 0.25
            if event.key == pygame.K_DOWN:      # Zoom out
                camera_scale += 0.25

        # mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:           # zoom in with the mouse wheel
                camera_scale -= 0.0625
            if event.button == 5:           # zoom out with the mouse wheel
                camera_scale += 0.0625



    mouse_held = [btn for btn in pygame.mouse.get_pressed()]

    # get the mouse position
    mouse_pos = Vector2(pygame.mouse.get_pos()) - 0.5 * screen_size

    # get the cell position of the mouse
    mouse_cell = (mouse_pos + camera_pos / real_scale(camera_scale)) // (16 / real_scale(camera_scale))

    # left mouse button held
    if mouse_held[0]:

        # create a cell
        cell_state.add_cells([mouse_cell])

    # right mouse button held
    elif mouse_held[2]:

        # delete a cell
        cell_state.remove_cells([mouse_cell])


    # middle mouse button held
    if mouse_held[1]:

        # move the camera
        mouse_pos = Vector2(pygame.mouse.get_pos())

        if not last_mouse_pos:
            last_mouse_pos = mouse_pos

        camera_pos = camera_pos - (mouse_pos - last_mouse_pos) * real_scale(camera_scale)

        last_mouse_pos = mouse_pos
    else:
        last_mouse_pos = False


    # update the Cell_State
    if not step_mode: cell_state.update_state()

    # draw the Cell_State
    cell_state.draw_state(screen, camera_pos, real_scale(camera_scale), screen_size)

    # set the framerate
    clock.tick(framerate)

    # update the screen
    pygame.display.flip()
