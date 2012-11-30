# Nibble-AI
import random

class AI(object):

    def __init__(self, board=None):
        self._energy = 30
        self._board = board

    def think(self):
        return random.randint(0,20)

    def setenergy(self, energy):
        self._energy = energy

    def getenergy(self):
        return self._energy

    def setboard(self, board):
        self._board = board

if __name__ == "__main__":
    ai = AI()
    print ai.think()
