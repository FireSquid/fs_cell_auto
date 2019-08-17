# ------------------
#       FS_Cell_Auto
#   Filename:       Cell_State.py
#   Created_by:     Peter Reynolds
#   Date_Created:   August 9th, 2019
# ------------------


# import necessary modules
import pygame, math
from pygame import Vector2


# class containing the state of the cellular automata simulation
class Cell_State:

    # tuple of relative positions of neigbor cells
    NEIGHBOR_POSITIONS = (  Vector2([0,1]), Vector2([1,1]), Vector2([1,0]), Vector2([1,-1]),
                            Vector2([0,-1]), Vector2([-1,-1]), Vector2([-1,0]), Vector2([-1,1]))

    # constructor
    def __init__(self, initial_cells):
        self.state = {}         # dictionary containing which cells are active (key = (int(x_pos), int(y_pos): value = bool(active))
        self.add_cells(initial_cells)   # initialize the state
        self.frame = 0


    # add a list of cells to the state
    def add_cells(self, cells):
        for cell in cells:
            self.state[tuple(cell.xy)] = True


    # remove a list of cells
    def remove_cells(self, cells):
        for cell in cells:
            if tuple(cell.xy) in self.state:
                del self.state[tuple(cell.xy)]


    # clear all cells
    def clear_cells(self):
        self.state = {}


    # iterate the cellular automata simulation 1 step
    def update_state(self):
        self.frame += 1
        neighbor_counts = {}    # dictionary counting the number of neighbors each cell has
        new_state = {}          # dictionary containing the new state of the simulation

        # loop through each active cell in the current state
        for cell in self.state:

            # add one to the neighbors of the current active cell
            for pos in Cell_State.NEIGHBOR_POSITIONS:

                # current position being checked
                check_pos = tuple((cell + pos).xy)

                if check_pos in neighbor_counts:      # increment the neighbor count
                    neighbor_counts[check_pos] += 1
                else:                           # set neighbor count to 1 if it hasn't been added yet
                    neighbor_counts[check_pos] = 1

        # loop through the neighbor poitions
        for cell in neighbor_counts:

            # apply rules for Conway's Game of Life (2 or 3 neighbors = survive, 3 neighbors = create, other = die)
            if neighbor_counts[cell] == 3 or (neighbor_counts[cell] == 2 and (cell in self.state and self.state[cell])):
                new_state[cell] = True

        # set the state to the new state
        self.state = new_state


    # draw the current state using pygame relative to camera_pos
    def draw_state(self, screen, camera_pos, camera_scale, view_size):

        # positional offset of the top right corner of the screen relative to the origin
        screen_origin = camera_pos / camera_scale - 0.5 * view_size

        # calculate the pixel size of each cell relative to the camera's scale
        cell_size = 16 / camera_scale

        # draw each cell
        for cell in self.state:

            # draw a green square
            pygame.draw.rect(screen, (0, 175, 0), pygame.Rect((Vector2(cell) * cell_size - screen_origin).xy, [cell_size, cell_size]))
