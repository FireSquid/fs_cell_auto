# ------------------
#       FS_Cell_Auto
#   Filename:       Cell_State.py
#   Created_by:     Peter Reynolds
#   Date_Created:   August 9th, 2019
# ------------------


# import necessary modules
import pygame, math
from pygame import Vector2
from Rule import Rule


# class containing the state of the cellular automata simulation
class Cell_State:

    NEIGHBOR_POSITIONS = (  Vector2([0,1]), Vector2([1,1]), Vector2([1,0]), Vector2([1,-1]),
                            Vector2([0,-1]), Vector2([-1,-1]), Vector2([-1,0]), Vector2([-1,1]))

    # constructor
    def __init__(self, state_colors):
        self.state = {}         # dictionary containing which cells are active (key = (int(x_pos), int(y_pos): value = bool(active))
        self.frame = 0

        # color of each active cell
        self.state_colors = state_colors

        # creates a rule to test functionality
        test_cell_change_rule = {}

        # Rules for Wireworld
        test_cell_change_rule[0] = {}
        test_cell_change_rule[1] = {2 : { 2 : {1, 2} }}
        test_cell_change_rule[2] = {3 : {}}
        test_cell_change_rule[3] = {1 : { 1 : {1, 2, 3, 4, 5, 6, 7, 8} }}

        self.rule = Rule(test_cell_change_rule)


    # add a list of cells to the state
    def add_cells(self, state, cells):
        for cell in cells:
            self.state[cell] = state


    # add a list of vectors to the state
    def add_cells_v(self, state, cells):
        for cell in cells:
            self.state[tuple(cell.xy)] = state

    # remove a list of cells
    def remove_cells(self, cells):
        for cell in cells:
            if tuple(cell.xy) in self.state:
                del self.state[tuple(cell.xy)]


    # clear all cells
    def clear_cells(self):
        self.state = {}


    # convert cell_state to a string that can be saved to a file
    def serialize_cells(self):

        serialization = ""

        # a dictionary containing lists of active cells in all rows that contain active cells
        rows = {}

        # iterate through all the cells
        for cell in self.state:
            if not cell[1] in rows:
                rows[cell[1]] = []
            # add active cell to the row
            rows[cell[1]].append((cell[0], 1))

        # add each row to the serialization
        for row in rows:

            # format:  R(row1_height)=(cell1_X):(cell1_state)|(cell2_X):(cell2_state)...|(cellN_X):(cellN_state)R(row2_height)...
            serialization += f"R{int(row)}=" + "|".join([":".join([str(int(data)) for data in cell]) for cell in rows[row]])

        print(serialization)

        return serialization

    # convert saved string back into the cell_state
    def deserialize_cells(self, serialization):

        parsed_cells = []

        # split the input string into separate rows
        rows = serialization.split("R")[1:]

        # iterate through each row
        for row in rows:

            #print(f"Row = {row}")

            row_parts = row.split("=")

            #print(f" - RowParts = {row_parts}")

            cells = row_parts[1].split("|")

            for cell in cells:

                cell_data = cell.split(":")

                # added parsed cell to the list
                parsed_cells.append((int(cell_data[0]), int(row_parts[0])))

        self.clear_cells()

        self.add_cells(1, parsed_cells)



    # iterate the cellular automata simulation 1 step
    def update_state(self):
        self.frame += 1
        neighbor_counts = {}    # dictionary counting the number of neighbors each cell has
        new_state = {}          # dictionary containing the new state of the simulation

        # loop through each active cell in the current state
        for cell in self.state:

            if cell not in neighbor_counts:
                neighbor_counts[cell] = {}

            # add one to the neighbors of the current active cell
            for pos in Cell_State.NEIGHBOR_POSITIONS:

                # current position being checked
                check_pos = tuple((cell + pos).xy)

                if check_pos not in neighbor_counts:                        # initialize neighbor counts at check_pos
                    neighbor_counts[check_pos] = {self.get_state_of_cell(cell) : 1}
                elif self.state[cell] not in neighbor_counts[check_pos]:    # add a neighbor count to check_pos
                    neighbor_counts[check_pos][self.get_state_of_cell(cell)] = 1
                else:                                                       # increment the neighbor count
                    neighbor_counts[check_pos][self.get_state_of_cell(cell)] += 1

        # loop through the cells with adjacent active cells
        for cell in neighbor_counts:

            new_state[cell] = self.rule.check_rules(cell, self, neighbor_counts)

            if not new_state[cell]:
                del new_state[cell]

        # set the state to the new state
        self.state = new_state

    def get_state_of_cell(self, cell):
        return self.state[cell] if cell in self.state else 0


    # draw the current state using pygame relative to camera_pos
    def draw_state(self, screen, camera_pos, camera_scale, view_size):

        # positional offset of the top right corner of the screen relative to the origin
        screen_origin = camera_pos / camera_scale - 0.5 * view_size

        # calculate the pixel size of each cell relative to the camera's scale
        cell_size = 16 / camera_scale

        # draw each cell
        for cell in self.state:

            # draw a square for each active cell
            pygame.draw.rect(screen, self.state_colors[self.state[cell]], pygame.Rect((Vector2(cell) * cell_size - screen_origin).xy, [cell_size, cell_size]))
