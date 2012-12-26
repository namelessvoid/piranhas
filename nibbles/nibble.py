class Nibble(object):
    """The representation of the player's nibble on the Nibble-server"""

    def __init__(self, name, energy=35, stamina=3):
        """
        The construtor needs the final variables
        -name
        -port-number
        """
        self._name = name
        self._energy = energy
        self._xpos = -1
        self._ypos = -1
        self._stamina = stamina

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
        """Sets the nibble's position."""
        self._xpos = x
        self._ypos = y

    def setstamina(self, stamina):
        """Sets the nibble's stamina."""
        self._stamina = stamina

    def getstamina(self):
        """Retursn the nibble's stamina."""
        return self._stamina

    energy = property(getenergy, setenergy, isalive,
                      "I'm the 'energy' property")
    pos = property(getpos, setpos, "I'm the 'position' property")
    stamina = property(getstamina, setstamina, "I'm the 'stamina' property")
