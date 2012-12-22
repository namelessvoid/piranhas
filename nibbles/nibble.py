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

    def getenergy(self):
        """Returns the nibble's energy"""
        return self._energy

    def setenergy(self, energy):
        """Sets the nibble's energy"""
        self._energy = energy

    def isalive(self):
        """Checks, if or if not the nibble's energy is higher then 0"""
        if self._energy > 0:
            return True
        else:
            return False

    def getname(self):
        """Returns the nibble's name, which is needed
            for the board-representation"""
        return self._name

    def getpos(self):
        """Returns the nibble's current position"""
        return (self._xpos, self._ypos)

    def setpos(self, x, y):
        """Sets the nibbles position."""
        self._xpos = x
        self._ypos = y

    energy = property(getenergy, setenergy, isalive,
                      "I'm the 'energy' property")
    pos = property(getpos, setpos, "I'm the 'position' property")
