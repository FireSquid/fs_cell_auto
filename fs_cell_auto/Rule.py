# ------------------
#       FS_Cell_Auto
#   Filename:       Rule.py
#   Created_by:     Peter Reynolds
#   Date_Created:   September 20th, 2019
# ------------------


# import necessary modules
import pygame, math
from pygame import Vector2


# tuple of relative positions of neigbor cells
NEIGHBOR_POSITIONS = (  Vector2([0,1]), Vector2([1,1]), Vector2([1,0]), Vector2([1,-1]),
                        Vector2([0,-1]), Vector2([-1,-1]), Vector2([-1,0]), Vector2([-1,1]))



# Cell_change_rule:
#   * {current_state : {next_state : (neighbor_counts)}, {next_state : (neighbor_counts)}, ...}
#   * earlier rules take precedence



class Rule:

    def __init__(self, ccr):
        self.cell_change_rules = ccr


    # returns an int representing the new value that cell should have after the given state
    def check_rules(self, cell, cell_state, cell_neighbors):

        # loop through each of the next possible states in the rule
        for next_state in self.cell_change_rules[cell_state[cell] if cell in cell_state else False]:

            # check for the matching number of active neighbors
            if cell_neighbors[cell] in (self.cell_change_rules[cell_state[cell] if cell in cell_state else False][next_state]):

                # return the next state
                return next_state

        return cell_state[cell] if cell in cell_state else False
