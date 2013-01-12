# -*- coding: utf-8 *-*

from random import choice

from nibbles.client.aiimps.simon.boardcopy import *
from matrixoperations import matrixintersection


class AI():
    def __init__(self):
        # The genome of the nibble. Hard coded for "finished" AI.
        #self.genome = {
            ## Kill instinct: used for weaker nibbles
            #"KI": [[200, 300, 400, 300, 200],
                   #[300, 400, 500, 400, 300],
                   #[500, 600, 700, 600, 500],
                   #[300, 400, 500, 400, 300],
                   #[200, 300, 400, 300, 200]],
            ## Flight instinct: used for stronger nibbles
            #"FI": [[-200, -300, -400, -300, -200],
                   #[-300, -500, -600, -500, -300],
                   #[-400, -600, -700, -600, -400],
                   #[-300, -500, -600, -500, -300],
                   #[-200, -300, -400, -300, -200]],
            ## Eat instinct: used for food
            #"EI": [[0, 0, 0, 0, 0],
                   #[0, 100, 100, 100, 0],
                   #[0, 100, 300, 100, 0],
                   #[0, 100, 100, 100, 0],
                   #[0, 0, 0, 0, 0]],
            ## Move rating: used for movement costs
            #"MR": [[-700, -600, -500, -600, -700],
                   #[-600, -300, -200, -300, -600],
                   #[-500, -200, -100, -200, -500],
                   #[-600, -300, -200, -300, -600],
                   #[-700, -600, -500, -600, -700]]
            #}

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
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]],
            "MR": [[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]]
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
        # !test purpose only!
#        self.mind = mind

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

