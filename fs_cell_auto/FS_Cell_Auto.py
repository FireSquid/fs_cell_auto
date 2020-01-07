# ------------------
#       FS_Cell_Auto
#   Filename:       FS_Cell_Auto.py
#   Created_by:     Peter Reynolds
#   Date_Created:   August 9th, 2019
# ------------------


# import necessary modules
import pygame, sys, math, easygui
from Cell_State import Cell_State
from pygame import Vector2


# convert the camera scale from linear to exponential
def real_scale(scale):
    return math.exp(scale)


# load a .fsca file into the cell state
def load_file(cell_state, filename):

    if filename == None:
        print("No file selected for loading")
        return

    try:
        # open file for writing
        file = open(f"{filename}", "r")
    except Exception as ex:
        # print exception if file fails to open
        print(ex)

    # read the file
    load_string = file.read()
    # close the file
    file.close()
    # parse the string
    cell_state.deserialize_cells(load_string)


# save the cell state into an .fsca file
def save_file(cell_state, filename):

    if not filename.endswith(".fsca"):
        filename += ".fsca"
    # remove any excess filename extenstions
    while filename.endswith(".fsca.fsca"):
        filename = filename[:-5]

    # get the serialized string of the state
    save_string = cell_state.serialize_cells()

    try:
        # open file for writing
        file = open(f"{filename}", "w")
    except Exception as ex:
        # print exception if file fails to open
        print(ex)

    # write string to the file
    file.write(save_string)
    # close the file
    file.close()


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

cell_colors = {1 : (255, 127, 0), 2 : (125, 125, 255), 3 : (240, 240, 240)}
# initialize a Cell_State
cell_state = Cell_State(cell_colors)

selected_state = 1

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
            if event.key == pygame.K_s:     # step through the simulation, also stops the simulation from running automatically
                step_mode = True
                cell_state.update_state()
            if event.key == pygame.K_r:     # return to automatic updates
                step_mode = False
            if event.key == pygame.K_c:     # clear all cells
                camera_pos = Vector2(0,0)
                step_mode = True
                cell_state.clear_cells()
            if event.key == pygame.K_i:     # open a file (import)
                step_mode = True
                filename = easygui.fileopenbox(msg="Select File", default="./Saves/", filetypes="*.fsca")
                load_file(cell_state, filename)
            if event.key == pygame.K_e:     # save to file (export)
                step_mode = True
                filename = easygui.filesavebox(msg="Save to a file", default="./Saves/Savefile", filetypes="*.fsca")
                save_file(cell_state, filename)
            if event.key == pygame.K_UP:       # Zoom in
                camera_scale -= 0.25
            if event.key == pygame.K_DOWN:      # Zoom out
                camera_scale += 0.25
            if event.key == pygame.K_y:
                selected_state += 1
                if selected_state > len(cell_colors):
                    selected_state = 1

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
        cell_state.add_cells_v(selected_state, [mouse_cell])

    # right mouse button held
    elif mouse_held[2]:

        # delete a cell
        cell_state.remove_cells([mouse_cell])


    # middle mouse button held
    if mouse_held[1]:

        # get the position of the mouse
        mouse_pos = Vector2(pygame.mouse.get_pos())

        # set the last mouse position to the current position if it wasn't already set to prevent the view from jumping
        if not last_mouse_pos:
            last_mouse_pos = mouse_pos

        # move the camera position based on the difference between the current mouse position and the previous mouse position
        camera_pos = camera_pos - (mouse_pos - last_mouse_pos) * real_scale(camera_scale)

        last_mouse_pos = mouse_pos

    else:
        # reset the last mouse position
        last_mouse_pos = False


    # update the Cell_State
    if not step_mode: cell_state.update_state()

    # draw the Cell_State
    cell_state.draw_state(screen, camera_pos, real_scale(camera_scale), screen_size)

    # show the currently selected cell state that will be added by clicking
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(10, 10, 40, 40))
    pygame.draw.rect(screen, cell_colors[selected_state], pygame.Rect(15, 15, 30, 30))

    # set the framerate
    clock.tick(framerate)

    # update the screen
    pygame.display.flip()
