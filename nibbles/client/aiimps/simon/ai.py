# -*- coding: utf-8 *-*

from random import choice

from nibbles.client.aiimps.simon.boardcopy import *
from matrixoperations import matrixintersection


class AI():
    def __init__(self):
        # The genome of the nibble. Hard coded for "finished" AI.
        # KI = Kill instinct: used for weaker nibbles
        # FI = Flight instinct: used for stronger nibbles
        # EI = Eat instinct : used for food
        # MR = Move rating: used for movement costs
        self.genome = {
            "FI" :
                [[45, -31, -22, -31,  45],
                [25, -42,  36, -42,  25],
               [-22,  36,  12,  36, -22],
               [ 25, -42,  36, -42,  25],
                [45, -31, -22, -31,  45]],

            "KI" :
               [[-16,  41,  28,  41, -16],
                [-8, -17, -25, -17,  -8],
                [28, -25,  16, -25,  28],
                [-8, -17, -25, -17,  -8],
               [-16,  41,  28,  41, -16]],

            "EI" :
                [[39,  65,   0,  65,  39],
               [-12,  42,  31,  42, -12],
               [  0,  31,  66,  31,   0],
               [-12,  42,  31,  42, -12],
                [39,  65,   0,  65,  39]],

            "MR" :  [
              [ -52, -11, -24, -11, -52],
              [  15,  56,  26,  56,  15],
              [ -24,  26,  45,  26, -24],
              [  15,  56,  26,  56,  15],
              [ -52, -11, -24, -11, -52]]
                    }

        self.currentview = None
        self.currentmind = None
        self.energy = 0
        self.stamina = 3

    def think(self, view, energy):
        """This method takes the current view of the nibble and it's energy
            to calculate the nibble's next move.
            Arguments:
                view -- (string) The current view of the nibble.
                energy -- (integer) The current energy of the nibble.
            Return:
                Integer between 0 and 24."""
        self.energy = energy

        # Regenerate stamina:
        if self.stamina < 3:
            self.stamina += 1

        # Convert the view to a board instance.
        self.currentview = createfromstring(view, 5, 5)
        # Create mind from MR matrix.
        mind = [[0 for x in xrange(0, 5)] for y in xrange(0, 5)]
        mrgenome = self.genome["MR"]
        for x in xrange(0, 5):
            for y in xrange(0, 5):
                mind[x][y] = mrgenome[x][y]

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

        # The AI can't move to every field if it has not enoug stamina.
        movrange = (0, 5)
        if self.stamina < 3:
            movrange = (1, 3)

        # Find the highest rating.
        bestrating = []
        for x in range(movrange[0], movrange[1]):
            for y in range(movrange[0], movrange[1]):
                bestrating.append(mind[x][y])
        bestrating = max(bestrating)

        # Find the fields with the best rating
        bestfields = []
        for x in range(movrange[0], movrange[1]):
            for y in range(movrange[0], movrange[1]):
                if mind[x][y] == bestrating:
                    bestfields.append((x, y))
        chosenfield = choice(bestfields)
        # Compute movement index.
        movement = chosenfield[0] + 5 * chosenfield[1]

        # Use up stamina if AI sprints:
        if movement in [0, 1, 2, 3, 4, 5, 9, 10, 14,
                       15, 19, 20, 21, 22, 23, 24]:
            self.stamina = 0
        return movement

    def genometostring(self):
        """Converts the genome of the ai to a eays to read / parse string.
            Return:
                String which contains all genomes."""
        str_list = []
        # Iterate genome dictionary
        for key in self.genome.keys():
            str_list.append(key + "\n")
            # Iterate through matrices lists
            matrix = self.genome[key]
            for y in xrange(0, 5):
                str_list.append("  ")
                for x in xrange(0, 5):
                    str_list.append("%4d" % (matrix[x][y]))
                    str_list.append(",")
                str_list[-1] = "\n"
            str_list.append("\n")
        return ''.join(str_list)


class TrainingsAI(AI):
    def __init__(self):
        AI.__init__(self)
        self.genome = {
            "KI": [[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]],
            "FI": [[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]],
            "EI": [[0, 0, 0, 0, 0],
                   [0,30, 80, 30, 0],
                   [0, 80, 100, 80, 0],
                   [0, 30, 80, 30, 0],
                   [0, 0, 0, 0, 0]],
            "MR": [[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]]
            }
