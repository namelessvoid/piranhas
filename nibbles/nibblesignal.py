# -*- coding: utf-8 *-*


class NibbleSignal(object):
    """Simple signal which calls a number of saved functions."""
    def __init__(self):
        self.listeners = []

    def register(self, function):
        """Register a function to the signal.
            Arguments:
                function --- (function object) the function to be registered"""
        self.listeners.append(function)

    def remove(self, function):
        """Removes the gifen function from the signal.
            Arguments:
                function -- (function object) the function to be removed"""
        self.listeners.remove(function)

    def call(self):
        """Calls all function saved in the signal."""
        for f in self.listeners:
            f()


class NibbleStringSignal(NibbleSignal):
    def __init__(self):
        super(NibbleStringSignal, self).__init__()

    def callstr(self, string):
        """Calls all function saved in the signal and send 'string' to them.
            Argumetns:
                string -- (string) a string that is send to all listeners."""
        for f in self.listeners:
            f(string)
