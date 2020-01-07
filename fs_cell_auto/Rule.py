# ------------------
#       FS_Cell_Auto
#   Filename:       Rule.py
#   Created_by:     Peter Reynolds
#   Date_Created:   September 20th, 2019
# ------------------


# import necessary modules
import pygame, math
from pygame import Vector2



# Cell_change_rule:
#   * {current_state : {next_state : {adj_state : count required, adj_state : count required, ...}},
#                       {next_state : {adj_state : count required, adj_state : count required, ...}}, ...}
#   * earlier rules take precedence

class Rule:

    def __init__(self, ccr):
        self.cell_change_rules = ccr


    # returns an int representing the new value that cell should have after the given state
    def check_rules(self, cell, cell_state, cell_neighbors):

        # loop through each of the next possible states in the rule
        for next_state in self.cell_change_rules[cell_state.get_state_of_cell(cell)]:

            conditions_met = True;

            if len(self.cell_change_rules[cell_state.get_state_of_cell(cell)][next_state]) > 0:
                # check if all the conditions are met for changing to the next state
                for adj_state in self.cell_change_rules[cell_state.get_state_of_cell(cell)][next_state]:


                    # check a condition
                    if (cell_neighbors[cell][adj_state] if adj_state in cell_neighbors[cell] else 0) not in self.cell_change_rules[cell_state.get_state_of_cell(cell)][next_state][adj_state]:

                        # a condition failed so the cell will not change to next_state
                        conditions_met = False

            # cell should change to next_state
            if conditions_met:
                return next_state


        return cell_state.get_state_of_cell(cell)
