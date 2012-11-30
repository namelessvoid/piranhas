"""board which holds the current nibble-world configuration"""

import sys


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
        x, y = self.calcpotition(x, y)
        self._field[x][y] = token

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
        if self.emptyposition(newX, newY):
            raise ValueError("Position is empty!")

        return self._field[newY][newX]

    def getnibbleview(self, x, y):
        """prints out the 5x5 view of a nibble"""
        view = [[], [], [], [], []]
        for i in range(0, 5, 1):
            for j in range(0, 5, 1):
                newI, newJ = self.calcposition(x - (j - 2), y - (i - 2))
                view[i].insert(j, self._field[newJ][newI])
        for row in reversed(view):
            print "".join([elem for elem in reversed(row)])

    def emptyposition(self, x, y):
        """checks if position (x/y) is empty"""
        return True if(self._field[y][x] == '.') else False

    def calcposition(self, x, y):
        """calculates new coordinates from x and y"""
        newX = x if self.inrangeofboard(self._width, x) else x % self._width
        newY = y if self.inrangeofboard(self._height, y) else y % self._height
        return (newX, newY)

    def inrangeofboard(self, side, pos):
        """checks if pos is in range of the board (side = width|height)"""
        if pos == 0 or (side - 1) / pos >= 1:
            return True


class BoardRenderer(object):
    def printboard(board):
        for i in range(board._height):
            for j in range(board._width):
                sys.stdout.write(board._field[i][j] + " ",)
            print

    printboard = staticmethod(printboard)
