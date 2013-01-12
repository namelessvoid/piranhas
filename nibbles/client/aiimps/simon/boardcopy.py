"""board which holds the current nibble-world configuration"""

from nibbles.nibble import Nibble


class Board(object):
    """ Hard copy of the nibbles.board class It is modified to
        grant higher execution speed which is necessary for the
        training simulation."""
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
        x, y = self.calcposition(x, y)
        newX, newY = self.calcposition(newX, newY)
        self._field[newY][newX] = self._field[y][x]
        # If token was actually not moved
        if (x, y) != (newX, newY):
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

    def getnibbleview(self, nibble, anonymised=False):
        """Returns a string which holds the 5x5 view of the nibble at pos x, y.
            Arguments:
                x, y -- (int) The x and y coordinate of the nibble (center
                        of the view
                energy -- (int) The energy of the nibble which view is been
                        printed. If the energy is None, just print the ids of
                        each nibble on the board. If the energy is not None,
                        the ids of the other nibbles are hidden and just
                        displayed as <, > or = relative to the energy.
            Return:
                string which holds the view."""
        x, y = nibble.getpos()
        energy = nibble.getenergy()
        view = ""
        for i in range(0, 5, 1):
            for j in range(0, 5, 1):
                newI, newJ = self.calcposition(x + (j - 2), y + (i - 2))
                element = self._field[newJ][newI]
                if isinstance(element, Nibble):
                    # if board is not anonymised or the nibble in the middle
                    # of the view is reached, print the nibble id
                    if (anonymised is False) or (element == nibble):
                        element = element.getname()
                    # if the board is anonymised, just print <, > oder =
                    else:
                        if element.getenergy() > energy:
                            element = ">"
                        elif element.getenergy() < energy:
                            element = "<"
                        else:
                            element = "="

                view += element
        return view

    def emptyposition(self, x, y):
        """checks if position (x/y) is empty"""
        return True if(self._field[y][x] == '.') else False

    def calcposition(self, x, y):
        """calculates new coordinates from x and y"""
        return (x % self._width, y % self._height)

    def tostring(self):
        """Returns the full content of the board as string."""
        string = ""
        for i in range(self._height):
            for j in range(self._width):
                element = self._field[i][j]
                if isinstance(element, Nibble):
                    element = element.getname()
                string += element
        return string


def createfromstring(field, width, height):
    """Converts a string to a board instance.
        Arguments:
            field -- (string) the string representation of the board
            width -- (int) the width of the board
            height -- (int) the height of the board"""
    # if string doesn't match the size of the board
    if (len(field) % width) != 0:
        return -1
    board = Board(width, height)
    for i in range(len(field) / width):
        i *= width
        board._field[i/width] = [j for j in field[i : width + i]]
    return board
