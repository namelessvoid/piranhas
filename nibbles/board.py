"""board which holds the current nibble-world configuration"""

import sys
from nibbles.nibble import Nibble


class Board(object):

    def __init__(self, x=0, y=0):
        """constructor - sets board-width to x and board-height to y"""
        self._width = int(x)
        self._height = int(y)
        self.reset()

    def reset(self):
        """resets the board"""
        self._field = [['.' for i in range(self._width)]
                      for j in range(self._height)]

    def getwidth(self):
        # Get width
        return self._width

    def getheight(self):
        # get height
        return self._height

    def settoken(self, token, x, y):
        """changes the value of board-position x,y to token"""
        x, y = self.calcposition(x, y)
        self._field[y][x] = token

    def movetoken(self, x, y, newX, newY):
        """
        copys the value at (x,y) and pastes it at (newX,newY).
        Then the (x,y)-field is drawn empty.
        """
        nextX, nextY = self.calcposition(newX, newY)
        x, y = self.calcposition(x, y)
        self._field[nextY][nextX] = self._field[y][x]
        self._field[y][x] = '.'

    def move(self, posX, posY, x, y):
        """
        move object relative to its current position
        Argument x: fields in x direction +/-
        Argument y: fields in y direction +/-
        """
        newX, newY = self.calcposition(x + posX, y + posY)
        if self.emptyposition(posX, posY):
            raise ValueError("Position is empty!")

        elif not self.emptyposition(newX, newY):
            raise ValueError("Position is not empty!")

        else:
            self._field[newY][newX] = self._field[posY][posX]
            self._field[posY][posX] = '.'

    def gettoken(self, x, y):
        """returns the value of the specified board-location"""
        newX, newY = self.calcposition(x, y)
        return self._field[newY][newX]

    def getnibbleview(self, x, y):
        """Returns a string which holds the 5x5 view of the nibble at pos x, y.
            Arguments:
                x, y -- (int) The x and y coordinate of the nibble (center
                        of the view
            Return:
                string which holds the view."""
        view = ""
        for i in range(0, 5, 1):
            for j in range(0, 5, 1):
                newI, newJ = self.calcposition(x + (j - 2), y + (i - 2))
                element = self._field[newJ][newI]
                if isinstance(element, Nibble):
                    element = element.getName()
                view += element
        return view

    def emptyposition(self, x, y):
        """checks if position (x/y) is empty"""
        return True if(self._field[y][x] == '.') else False

    def calcposition(self, x, y):
        """calculates new coordinates from x and y"""
        return (x % self._width, y % self._height)

class BoardRenderer(object):
    def printboard(board):
        for i in range(board._height):
            for j in range(board._width):
                sys.stdout.write(board._field[i][j] + " ",)
            print

    printboard = staticmethod(printboard)
