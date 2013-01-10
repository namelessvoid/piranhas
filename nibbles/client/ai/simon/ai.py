# -*- coding: utf-8 *-*

from random import choice

from nibbles.board import createfromstring
from matrixoperations import matrixintersection


class AI():
    def __init__(self):
        # The genome of the nibble. Hard coded for "finished" AI.
        self.genome = {
            # Kill instinct: used for weaker nibbles
            "KI": [[2, 3, 4, 3, 2],
                   [3, 4, 5, 4, 3],
                   [5, 6, 7, 6, 5],
                   [3, 4, 5, 4, 3],
                   [2, 3, 4, 3, 2]],
            # Flight instinct: used for stronger nibbles
            "FI": [[-2, -3, -4, -3, -2],
                   [-3, -5, -6, -5, -3],
                   [-4, -6, -7, -6, -4],
                   [-3, -5, -6, -5, -3],
                   [-2, -3, -4, -3, -2]],
            # Eat instinct: used for food
            "EI": [[0, 0, 0, 0, 0],
                   [0, 1, 1, 1, 0],
                   [0, 1, 3, 1, 0],
                   [0, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0]],
            # Move rating: used for movement costs
            "MR": [[-7, -6, -5, -6, -7],
                   [-6, -3, -2, -3, -6],
                   [-5, -2, -1, -2, -5],
                   [-6, -3, -2, -3, -6],
                   [-7, -6, -5, -6, -7]]
            }

        self.currentview = None
        self.currentmind = None

    def think(self, view, energy):
        """This method takes the current view of the nibble and it's energy
            to calculate the nibble's next move.
            Arguments:
                view -- (string) The current view of the nibble.
                energy -- (integer) The current energy of the nibble.
            Return:
                Integer between 0 and 24."""

        # Convert the view to a board instance.
        self.currentview = createfromstring(view, 5, 5)
        # Create empty mind which is used for calculations.
        mind = [[0 for x in range(0, 5)] for y in range(0, 5)]

        # Fill mind with ratings for movement.
        matrixintersection(self.genome["MR"], mind, (2, 2))
        # Fill the mind with ratings of every field on the board.
        for x in range(0, 5):
            for y in range(0, 5):
                token = self.currentview.gettoken(x, y)
                # Weak enemy, apply kill instinct
                if token == '<' or token == '=':
                    matrixintersection(self.genome["KI"], mind, (x, y))
                # Stronger enemy, apply flight instinct
                elif token == '>':
                    matrixintersection(self.genome["FI"], mind, (x, y))
                # Food, apply eat instinct
                elif token == '*':
                    matrixintersection(self.genome["EI"], mind, (x, y))
        # Find field with highest rating. If there are equal fields, choose
        # randomly.
        bestrating = max(max(r) for r in mind)
        bestfields = []
        for x in range(0, 5):
            for y in range(0, 5):
                if mind[x][y] == bestrating:
                    bestfields.append((x, y))
        chosenfield = choice(bestfields)
        # Compute movement index.
        movement = chosenfield[0] + 5 * chosenfield[1]

        # !test purpose only!
        self.mind = mind
        return movement
