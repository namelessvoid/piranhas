class Nibble(object):
    """The representation of the player's nibble on the Nibble-server"""

    def __init__(self, name, energy):
        """
        The construtor needs the final variables
        -name
        -port-number
        """
        self._name = name
        self._energy = energy
        self._xpos = -1
        self._ypos = -1

    def getEnergy(self):
        """Returns the nibble's energy"""
        return self._energy

    def setEnergy(self, energy):
        """Sets the nibble's energy"""
        self._energy = energy

    def isAlive(self):
        """Checks, if or if not the nibble's energy is higher then 0"""
        if self._energy > 0:
            return True
        else:
            return False

    def getName(self):
        """Returns the nibble's name, which is needed
            for the board-representation"""
        return self._name

    def getPos(self):
        """Returns the nibble's current position"""
        return (self._xpos, self._ypos)

    def setPos(self, x, y):
        """Sets the nibbles position."""
        self._xpos = x
        self._ypos = y

    energy = property(getEnergy, setEnergy, isAlive,
                      "I'm the 'energy' property")
    pos = property(getPos, setPos, "I'm the 'position' property")
